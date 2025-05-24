#!/usr/bin/env python3
# CLI of pyzstd module: python -m pyzstd --help
import argparse
import os
from time import time

from pyzstd import compress_stream, decompress_stream, \
                   CParameter, DParameter, \
                   train_dict, ZstdDict, ZstdFile, \
                   compressionLevel_values, zstd_version, \
                   __version__ as pyzstd_version, PYZSTD_CONFIG

# buffer sizes recommended by zstd
C_READ_BUFFER = 131072
D_READ_BUFFER = 131075

def progress_bar(progress, total, width=50):
    # documented behavior: if input stream is empty, the callback
    # function will not be called. so no ZeroDivisionError here.
    percent = (progress + 1) / total
    now = int(width * percent)
    bar = "+" * now + "-" * (width - now)
    print("|%s| %.2f%%" % (bar, 100*percent), end="\r", flush=True)

# open output file and assign to args.output
def open_output(args, path):
    if not args.f and os.path.isfile(path):
        answer = input(('output file already exists:\n'
                        '{}\noverwrite? (y/n) ').format(path))
        print()
        if answer != 'y':
            import sys
            sys.exit()
    args.output = open(path, 'wb')

def close_files(args):
    if args.input is not None:
        args.input.close()

    if args.output is not None:
        args.output.close()

def compress_option(args):
    # threads message
    if args.threads == 0:
        threads_msg = 'single-thread mode'
    else:
        threads_msg = 'multi-thread mode, %d threads.' % args.threads

    # long mode
    if args.long >= 0:
        use_long = 1
        windowLog = args.long
        long_msg = 'yes, windowLog is %d.' % windowLog
    else:
        use_long = 0
        windowLog = 0
        long_msg = 'no'

    # option
    option = {CParameter.compressionLevel: args.level,
              CParameter.nbWorkers: args.threads,
              CParameter.enableLongDistanceMatching: use_long,
              CParameter.windowLog: windowLog,
              CParameter.checksumFlag: args.checksum,
              CParameter.dictIDFlag: args.write_dictID}

    # pre-compress message
    msg = (' - compression level: {}\n'
           ' - threads: {}\n'
           ' - long mode: {}\n'
           ' - zstd dictionary: {}\n'
           ' - add checksum: {}').format(
                args.level, threads_msg, long_msg,
                args.zd, args.checksum)
    print(msg)

    return option

def compress(args):
    # input file size
    input_file_size = os.path.getsize(args.input.name)

    # output file
    if args.output is None:
        open_output(args, args.input.name + '.zst')

    # pre-compress message
    msg = ('Compress file:\n'
           ' - input file : {}\n'
           ' - output file: {}').format(
                args.input.name,
                args.output.name)
    print(msg)

    # option
    option = compress_option(args)

    # compress
    def cb(total_input, total_output, read_data, write_data):
        progress_bar(total_input, input_file_size)
    t1 = time()
    ret = compress_stream(args.input, args.output,
                          level_or_option=option,
                          zstd_dict=args.zd,
                          pledged_input_size=input_file_size,
                          callback=cb)
    t2 = time()
    close_files(args)

    # post-compress message
    if ret[0] != 0:
        ratio = 100 * ret[1] / ret[0]
    else:
        ratio = 100.0
    msg = ('\nCompression succeeded, {:.2f} seconds.\n'
           'Input {:,} bytes, output {:,} bytes, ratio {:.2f}%.\n').format(
            t2-t1, *ret, ratio)
    print(msg)

def decompress(args):
    # input file size
    input_file_size = os.path.getsize(args.input.name)

    # output file
    if args.output is None and args.test is None:
        from re import subn

        out_path, replaced = subn(r'(?i)^(.*)\.zst$', r'\1', args.input.name)
        if not replaced:
            out_path = args.input.name + '.decompressed'
        open_output(args, out_path)

    # option
    option = {DParameter.windowLogMax: args.windowLogMax}

    # pre-decompress message
    if args.output is not None:
        output_name = args.output.name
    else:
        output_name = 'None'
    print(('Decompress file:\n'
           ' - input file : {}\n'
           ' - output file: {}\n'
           ' - zstd dictionary: {}').format(
            args.input.name, output_name, args.zd))

    # decompress
    def cb(total_input, total_output, read_data, write_data):
        progress_bar(total_input, input_file_size)
    t1 = time()
    ret = decompress_stream(args.input, args.output,
                            zstd_dict=args.zd, option=option,
                            callback=cb)
    t2 = time()
    close_files(args)

    # post-decompress message
    if ret[1] != 0:
        ratio = 100 * ret[0] / ret[1]
    else:
        ratio = 100.0
    msg = ('\nDecompression succeeded, {:.2f} seconds.\n'
           'Input {:,} bytes, output {:,} bytes, ratio {:.2f}%.\n').format(
            t2-t1, *ret, ratio)
    print(msg)

def train(args):
    from glob import glob

    # check output file
    if args.output is None:
        msg = 'need to specify output file using -o/--output option'
        raise Exception(msg)

    # gather samples
    print('Gathering samples, please wait.', flush=True)
    lst = []
    for file in glob(args.train, recursive=True):
        with open(file, 'rb') as f:
            dat = f.read()
            lst.append(dat)
            print('samples count: %d' % len(lst), end='\r', flush=True)
    if len(lst) == 0:
        raise Exception('No samples gathered, please check GLOB_PATH.')

    samples_size = sum(len(sample) for sample in lst)
    if samples_size == 0:
        raise Exception("Samples content is empty, can't train.")

    # pre-train message
    msg = ('Gathered, train zstd dictionary:\n'
           ' - samples: {}\n'
           ' - samples number: {}\n'
           ' - samples content: {:,} bytes\n'
           ' - dict file: {}\n'
           ' - dict max size: {:,} bytes\n'
           ' - dict id: {}\n'
           'Training, please wait.').format(
                args.train, len(lst), samples_size,
                args.output.name, args.maxdict,
                'random' if args.dictID is None else args.dictID)
    print(msg, flush=True)

    # train
    t1 = time()
    zd = train_dict(lst, args.maxdict)
    t2 = time()

    # Dictionary_ID: 4 bytes, stored in little-endian format.
    # it can be any value, except 0 (which means no Dictionary_ID).
    if args.dictID is not None and len(zd.dict_content) >= 8:
        content = zd.dict_content[:4] + \
                    args.dictID.to_bytes(4, 'little') + \
                    zd.dict_content[8:]
        zd = ZstdDict(content)

    # save to file
    args.output.write(zd.dict_content)
    close_files(args)

    # post-train message
    msg = ('Training succeeded, {:.2f} seconds.\n'
           'Dictionary: {}\n').format(t2-t1, zd)
    print(msg)

def get_ZstdTarFile():
    # lazy import for tar operations
    from tarfile import TarFile

    class ZstdTarFile(TarFile):
        def __init__(self, name, mode='r', *, level_or_option=None, zstd_dict=None, **kwargs):
            self.zstd_file = ZstdFile(name, mode,
                                      level_or_option=level_or_option,
                                      zstd_dict=zstd_dict)
            try:
                super().__init__(fileobj=self.zstd_file, mode=mode, **kwargs)
            except:
                self.zstd_file.close()
                raise

        def close(self):
            try:
                super().close()
            finally:
                self.zstd_file.close()

    return ZstdTarFile

def tarfile_create(args):
    # check input dir
    args.tar_input_dir = args.tar_input_dir.rstrip(os.sep)
    if not os.path.isdir(args.tar_input_dir):
        msg = 'Tar archive input dir invalid: ' + args.tar_input_dir
        raise NotADirectoryError(msg)
    dirname, basename = os.path.split(args.tar_input_dir)

    # check output file
    if args.output is None:
        out_path = os.path.join(dirname, basename + '.tar.zst')
        open_output(args, out_path)

    # get ZstdTarFile class
    ZstdTarFile = get_ZstdTarFile()

    # pre-compress message
    msg = ('Archive tar file:\n'
           ' - input directory: {}\n'
           ' - output file: {}').format(
                args.tar_input_dir,
                args.output.name)
    print(msg)

    # option
    option = compress_option(args)

    # compress
    print('Archiving, please wait.', flush=True)
    t1 = time()
    with ZstdTarFile(args.output, mode='w',
                     level_or_option=option,
                     zstd_dict=args.zd) as f:
        f.add(args.tar_input_dir, basename)
        uncompressed_size = f.fileobj.tell()
    t2 = time()

    output_file_size = args.output.tell()
    close_files(args)

    # post-compress message
    if uncompressed_size != 0:
        ratio = 100 * output_file_size / uncompressed_size
    else:
        ratio = 100.0

    msg = ('Archiving succeeded, {:.2f} seconds.\n'
           'Input ~{:,} bytes, output {:,} bytes, ratio {:.2f}%.\n').format(
            t2-t1, uncompressed_size, output_file_size, ratio)
    print(msg)

def tarfile_extract(args):
    # input file size
    if args.input is None:
        msg = 'need to specify input file using -d/--decompress option.'
        raise FileNotFoundError(msg)
    input_file_size = os.path.getsize(args.input.name)

    # check output dir
    if not os.path.isdir(args.tar_output_dir):
        msg = 'Tar archive output dir invalid: ' + args.tar_output_dir
        raise NotADirectoryError(msg)

    # get ZstdTarFile class
    ZstdTarFile = get_ZstdTarFile()

    # option
    option = {DParameter.windowLogMax: args.windowLogMax}

    # pre-extract message
    msg = ('Extract tar archive:\n'
           ' - input file: {}\n'
           ' - output dir: {}\n'
           ' - zstd dictionary: {}\n'
           'Extracting, please wait.').format(
                args.input.name,
                args.tar_output_dir,
                args.zd)
    print(msg, flush=True)

    # extract
    t1 = time()
    with ZstdTarFile(args.input, mode='r',
                     zstd_dict=args.zd,
                     level_or_option=option) as f:
        f.extractall(args.tar_output_dir)
        uncompressed_size = f.fileobj.tell()
    t2 = time()
    close_files(args)

    # post-extract message
    if uncompressed_size != 0:
        ratio = 100 * input_file_size / uncompressed_size
    else:
        ratio = 100.0
    msg = ('Extraction succeeded, {:.2f} seconds.\n'
           'Input {:,} bytes, output ~{:,} bytes, ratio {:.2f}%.\n').format(
            t2-t1, input_file_size, uncompressed_size, ratio)
    print(msg)

def range_action(min, max, bits_msg=False):
    class RangeAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            # convert to int
            try:
                v = int(values)
            except:
                raise TypeError('{} should be an integer'.format(option_string))

            # check range
            if not (min <= v <= max):
                # 32/64 bits message
                if bits_msg:
                    bits = 'in {}-bit build, '.format(PYZSTD_CONFIG[0])
                else:
                    bits = ''

                # message
                msg = ('{}{} value should: {} <= v <= {}. '
                       'provided value is {}.').format(
                        bits, option_string, min, max, v)
                raise ValueError(msg)

            setattr(args, self.dest, v)
    return RangeAction

def parse_arg():
    p = argparse.ArgumentParser(
                    prog = 'CLI of pyzstd module',
                    description = ("The command style is similar to zstd's "
                                   "CLI, but there are some differences.\n"
                                   "Zstd's CLI should be faster, it has "
                                   "some I/O optimizations."),
                    epilog=('Examples of use:\n'
                            '  compress a file:\n'
                            '    python -m pyzstd -c IN_FILE -o OUT_FILE\n'
                            '  decompress a file:\n'
                            '    python -m pyzstd -d IN_FILE -o OUT_FILE\n'
                            '  create a tar archive:\n'
                            '    python -m pyzstd --tar-input-dir DIR -o OUT_FILE\n'
                            '  extract a tar archive, output will forcibly overwrite existing files:\n'
                            '    python -m pyzstd -d IN_FILE --tar-output-dir DIR\n'
                            '  train a zstd dictionary, ** traverses sub-directories:\n'
                            '    python -m pyzstd --train "E:\\cpython\\**\\*.c" -o OUT_FILE'),
                    formatter_class=argparse.RawDescriptionHelpFormatter)

    g = p.add_argument_group('Common arguments')
    g.add_argument('-D', '--dict', metavar='FILE', type=argparse.FileType('rb'),
                   help='use FILE as zstd dictionary for compression or decompression')
    g.add_argument('-o', '--output', metavar='FILE', type=str,
                   help='result stored into FILE')
    g.add_argument('-f', action='store_true',
                   help='disable output check, allows overwriting existing file.')

    g = p.add_argument_group('Compression arguments')
    gm = g.add_mutually_exclusive_group()
    gm.add_argument('-c', '--compress', metavar='FILE', type=str,
                    help='compress FILE')
    gm.add_argument('--tar-input-dir', metavar='DIR', type=str,
                    help=('create a tar archive from DIR. '
                          'this option overrides -c/--compress option.'))
    g.add_argument('-l', '--level', metavar='#',
                   default=compressionLevel_values.default,
                   action=range_action(compressionLevel_values.min,
                                       compressionLevel_values.max),
                   help='compression level, range: [{},{}], default: {}.'.
                   format(compressionLevel_values.min,
                          compressionLevel_values.max,
                          compressionLevel_values.default))
    g.add_argument('-t', '--threads', metavar='#', default=0,
                   action=range_action(*CParameter.nbWorkers.bounds(), True),
                   help=('spawns # threads to compress. if this option is not '
                         'specified or is 0, use single thread mode.'))
    g.add_argument('--long', metavar='#', nargs='?', const=27, default=-1,
                   action=range_action(*CParameter.windowLog.bounds(), True),
                   help='enable long distance matching with given windowLog (default #: 27)')
    g.add_argument('--no-checksum', action='store_false',
                   dest='checksum', default=True,
                   help="don't add 4-byte XXH64 checksum to the frame")
    g.add_argument('--no-dictID', action='store_false',
                   dest='write_dictID', default=True,
                   help="don't write dictID into frame header (dictionary compression only)")

    g = p.add_argument_group('Decompression arguments')
    gm = g.add_mutually_exclusive_group()
    gm.add_argument('-d', '--decompress', metavar='FILE', type=str,
                    help='decompress FILE')
    g.add_argument('--tar-output-dir', metavar='DIR', type=str,
                   help=('extract tar archive to DIR, '
                         'output will forcibly overwrite existing files. '
                         'this option overrides -o/--output option.'))
    gm.add_argument('--test', metavar='FILE', type=str,
                    help='try to decompress FILE to check integrity')
    g.add_argument('--windowLogMax', metavar='#', default=0,
                   action=range_action(*DParameter.windowLogMax.bounds(), True),
                   help='set a memory usage limit for decompression (windowLogMax)')

    g = p.add_argument_group('Dictionary builder')
    g.add_argument('--train', metavar='GLOB_PATH', type=str,
                   help='create a dictionary from a training set of files')
    g.add_argument('--maxdict', metavar='SIZE', type=int, default=112640,
                   help='limit dictionary to SIZE bytes (default: 112640)')
    g.add_argument('--dictID', metavar='DICT_ID', default=None,
                   action=range_action(1, 0xFFFFFFFF),
                   help='specify dictionary ID value (default: random)')

    args = p.parse_args()

    # input file
    if args.compress is not None:
        args.input = open(args.compress, 'rb',
                          buffering=C_READ_BUFFER)
    elif args.decompress is not None:
        args.input = open(args.decompress, 'rb',
                          buffering=D_READ_BUFFER)
    elif args.test is not None:
        args.input = open(args.test, 'rb',
                          buffering=D_READ_BUFFER)
    else:
        args.input = None

    # output file
    if args.output is not None:
        open_output(args, args.output)

    # load dictionary
    if args.dict is not None:
        zd_content = args.dict.read()
        args.dict.close()
        # Magic_Number: 4 bytes, value 0xEC30A437, little-endian format.
        is_raw = zd_content[:4] != b'\x37\xA4\x30\xEC'
        args.zd = ZstdDict(zd_content, is_raw)
    else:
        args.zd = None

    # arguments combination
    functions = [args.compress, args.decompress,
                 args.test, args.train, args.tar_input_dir]
    if sum(1 for i in functions if i is not None) > 1:
        raise Exception('Wrong arguments combination')

    return args

def main():
    print('*** pyzstd module v{}, zstd library v{}. ***\n'.
          format(pyzstd_version, zstd_version))

    args = parse_arg()

    if args.tar_input_dir:
        tarfile_create(args)
    elif args.tar_output_dir:
        tarfile_extract(args)
    elif args.compress:
        compress(args)
    elif args.decompress or args.test:
        decompress(args)
    elif args.train:
        train(args)
    else:
        print('Invalid command. See help: python -m pyzstd --help')

if __name__ == '__main__':
    main()
