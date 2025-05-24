try:
    # Import C implementation
    from .c import *
except ImportError:
    try:
        # Import CFFI implementation
        from .cffi import *
    except ImportError:
        raise ImportError(
            "\n\npyzstd module: Can't import compiled .so/.pyd file.\n"
            "1, If pyzstd module is dynamically linked to zstd library: Make sure\n"
            "   not to remove zstd library, and the run-time zstd library's version\n"
            "   can't be lower than that at compile-time; On Windows, the directory\n"
            "   that has libzstd.dll should be added by os.add_dll_directory() function.\n"
            "2, Please install pyzstd module through pip, to ensure that compiled\n"
            "   .so/.pyd file matches the architecture/OS/Python.\n")
from .zstdfile import *
from .seekable_zstdfile import *

__version__ = '0.16.2'

__doc__ = '''\
Python bindings to Zstandard (zstd) compression library, the API style is
similar to Python's bz2/lzma/zlib modules.

Command line interface of this module: python -m pyzstd --help

Documentation: https://pyzstd.readthedocs.io
GitHub: https://github.com/Rogdham/pyzstd
PyPI: https://pypi.org/project/pyzstd'''

__all__ = ('ZstdCompressor', 'RichMemZstdCompressor',
           'ZstdDecompressor', 'EndlessZstdDecompressor',
           'CParameter', 'DParameter', 'Strategy', 'ZstdError',
           'compress', 'richmem_compress', 'decompress',
           'compress_stream', 'decompress_stream',
           'ZstdDict', 'train_dict', 'finalize_dict',
           'get_frame_info', 'get_frame_size', 'ZstdFile', 'open',
           'zstd_version', 'zstd_version_info',
           'zstd_support_multithread', 'compressionLevel_values',
           'SeekableZstdFile', 'SeekableFormatError')


zstd_support_multithread = (CParameter.nbWorkers.bounds() != (0, 0))


def compress(data, level_or_option=None, zstd_dict=None):
    """Compress a block of data, return a bytes object.

    Compressing b'' will get an empty content frame (9 bytes or more).

    Parameters
    data:            A bytes-like object, data to be compressed.
    level_or_option: When it's an int object, it represents compression level.
                     When it's a dict object, it contains advanced compression
                     parameters.
    zstd_dict:       A ZstdDict object, pre-trained dictionary for compression.
    """
    comp = ZstdCompressor(level_or_option, zstd_dict)
    return comp.compress(data, ZstdCompressor.FLUSH_FRAME)


def richmem_compress(data, level_or_option=None, zstd_dict=None):
    """Compress a block of data, return a bytes object.

    Use rich memory mode, it's faster than compress() in some cases, but
    allocates more memory.

    Compressing b'' will get an empty content frame (9 bytes or more).

    Parameters
    data:            A bytes-like object, data to be compressed.
    level_or_option: When it's an int object, it represents compression level.
                     When it's a dict object, it contains advanced compression
                     parameters.
    zstd_dict:       A ZstdDict object, pre-trained dictionary for compression.
    """
    comp = RichMemZstdCompressor(level_or_option, zstd_dict)
    return comp.compress(data)


def _nbytes(dat):
    if isinstance(dat, (bytes, bytearray)):
        return len(dat)
    with memoryview(dat) as mv:
        return mv.nbytes


def train_dict(samples, dict_size):
    """Train a zstd dictionary, return a ZstdDict object.

    Parameters
    samples:   An iterable of samples, a sample is a bytes-like object
               represents a file.
    dict_size: The dictionary's maximum size, in bytes.
    """
    # Check argument's type
    if not isinstance(dict_size, int):
        raise TypeError('dict_size argument should be an int object.')

    # Prepare data
    chunks = []
    chunk_sizes = []
    for chunk in samples:
        chunks.append(chunk)
        chunk_sizes.append(_nbytes(chunk))

    chunks = b''.join(chunks)
    if not chunks:
        raise ValueError("The samples are empty content, can't train dictionary.")

    # samples_bytes: samples be stored concatenated in a single flat buffer.
    # samples_size_list: a list of each sample's size.
    # dict_size: size of the dictionary, in bytes.
    dict_content = _train_dict(chunks, chunk_sizes, dict_size)

    return ZstdDict(dict_content)


def finalize_dict(zstd_dict, samples, dict_size, level):
    """Finalize a zstd dictionary, return a ZstdDict object.

    Given a custom content as a basis for dictionary, and a set of samples,
    finalize dictionary by adding headers and statistics according to the zstd
    dictionary format.

    You may compose an effective dictionary content by hand, which is used as
    basis dictionary, and use some samples to finalize a dictionary. The basis
    dictionary can be a "raw content" dictionary, see is_raw parameter in
    ZstdDict.__init__ method.

    Parameters
    zstd_dict: A ZstdDict object, basis dictionary.
    samples:   An iterable of samples, a sample is a bytes-like object
               represents a file.
    dict_size: The dictionary's maximum size, in bytes.
    level:     The compression level expected to use in production. The
               statistics for each compression level differ, so tuning the
               dictionary for the compression level can help quite a bit.
    """
    if zstd_version_info < (1, 4, 5):
        msg = ("This function only available when the underlying zstd "
               "library's version is greater than or equal to v1.4.5, "
               "the current underlying zstd library's version is v%s.") % zstd_version
        raise NotImplementedError(msg)

    # Check arguments' type
    if not isinstance(zstd_dict, ZstdDict):
        raise TypeError('zstd_dict argument should be a ZstdDict object.')
    if not isinstance(dict_size, int):
        raise TypeError('dict_size argument should be an int object.')
    if not isinstance(level, int):
        raise TypeError('level argument should be an int object.')

    # Prepare data
    chunks = []
    chunk_sizes = []
    for chunk in samples:
        chunks.append(chunk)
        chunk_sizes.append(_nbytes(chunk))

    chunks = b''.join(chunks)
    if not chunks:
        raise ValueError("The samples are empty content, can't finalize dictionary.")

    # custom_dict_bytes: existing dictionary.
    # samples_bytes: samples be stored concatenated in a single flat buffer.
    # samples_size_list: a list of each sample's size.
    # dict_size: maximal size of the dictionary, in bytes.
    # compression_level: compression level expected to use in production.
    dict_content = _finalize_dict(zstd_dict.dict_content,
                                  chunks, chunk_sizes,
                                  dict_size, level)

    return ZstdDict(dict_content)
