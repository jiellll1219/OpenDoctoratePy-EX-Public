from array import array
from bisect import bisect_right
from os.path import isfile
from struct import Struct
from warnings import warn

from pyzstd.zstdfile import ZstdDecompressReader, ZstdFile, \
                            _MODE_CLOSED, _MODE_READ, _MODE_WRITE, \
                            PathLike, io

__all__ = ('SeekableFormatError', 'SeekableZstdFile')

class SeekableFormatError(Exception):
    'An error related to Zstandard Seekable Format.'
    def __init__(self, msg):
        super().__init__('Zstandard Seekable Format error: ' + msg)

__doc__ = '''\
Zstandard Seekable Format (Ver 0.1.0, Apr 2017)
Square brackets are used to indicate optional fields.
All numeric fields are little-endian unless specified otherwise.
A. Seek table is a skippable frame at the end of file:
     Magic_Number  Frame_Size  [Seek_Table_Entries]  Seek_Table_Footer
     4 bytes       4 bytes     8-12 bytes each       9 bytes
     Magic_Number must be 0x184D2A5E.
B. Seek_Table_Entries:
     Compressed_Size  Decompressed_Size  [Checksum]
     4 bytes          4 bytes            4 bytes
     Checksum is optional.
C. Seek_Table_Footer:
     Number_Of_Frames  Seek_Table_Descriptor  Seekable_Magic_Number
     4 bytes           1 byte                 4 bytes
     Seekable_Magic_Number must be 0x8F92EAB1.
D. Seek_Table_Descriptor:
     Bit_number  Field_name
     7           Checksum_Flag
     6-2         Reserved_Bits  (should ensure they are set to 0)
     1-0         Unused_Bits    (should not interpret these bits)'''
__format_version__ = '0.1.0'

class SeekTable:
    _s_2uint32 = Struct('<II')
    _s_3uint32 = Struct('<III')
    _s_footer  = Struct('<IBI')

    # read_mode is True for read mode, False for write/append modes.
    def __init__(self, read_mode):
        self._read_mode = read_mode
        self._clear_seek_table()

    def _clear_seek_table(self):
        self._has_checksum = False
        # The seek table frame size, used for append mode.
        self._seek_frame_size = 0
        # The file size, used for seeking to EOF.
        self._file_size = 0

        self._frames_count = 0
        self._full_c_size = 0
        self._full_d_size = 0

        if self._read_mode:
            # Item: cumulated_size
            # Length: frames_count + 1
            # q is int64_t. On Linux/macOS/Windows, Py_off_t is signed, so
            # ZstdFile/SeekableZstdFile use int64_t as file position/size.
            self._cumulated_c_size = array('q', [0])
            self._cumulated_d_size = array('q', [0])
        else:
            # Item: (c_size1, d_size1,
            #        c_size2, d_size2,
            #        c_size3, d_size3,
            #        ...)
            # Length: frames_count * 2
            # I is uint32_t.
            self._frames = array('I')

    def append_entry(self, compressed_size, decompressed_size):
        if compressed_size == 0:
            if decompressed_size == 0:
                # (0, 0) frame is no sense
                return
            else:
                # Impossible frame
                raise ValueError

        self._frames_count += 1
        self._full_c_size += compressed_size
        self._full_d_size += decompressed_size

        if self._read_mode:
            self._cumulated_c_size.append(self._full_c_size)
            self._cumulated_d_size.append(self._full_d_size)
        else:
            self._frames.append(compressed_size)
            self._frames.append(decompressed_size)

    # seek_to_0 is True or False.
    # In read mode, seeking to 0 is necessary.
    def load_seek_table(self, fp, seek_to_0):
        # Get file size
        fsize = fp.seek(0, 2) # 2 is SEEK_END
        if fsize == 0:
            return
        elif fsize < 17: # 17=4+4+9
            msg = ('File size is less than the minimal size '
                   '(17 bytes) of Zstandard Seekable Format.')
            raise SeekableFormatError(msg)

        # Read footer
        fp.seek(-9, 2) # 2 is SEEK_END
        footer = fp.read(9)
        frames_number, descriptor, magic_number = self._s_footer.unpack(footer)
        # Check format
        if magic_number != 0x8F92EAB1:
            msg = ('The last 4 bytes of the file is not Zstandard Seekable '
                   'Format Magic Number (b"\\xb1\\xea\\x92\\x8f)". '
                   'SeekableZstdFile class only supports Zstandard Seekable '
                   'Format file or 0-size file. To read a zstd file that is '
                   'not in Zstandard Seekable Format, use ZstdFile class.')
            raise SeekableFormatError(msg)

        # Seek_Table_Descriptor
        self._has_checksum = \
           descriptor & 0b10000000
        if descriptor & 0b01111100:
            msg = ('In Zstandard Seekable Format version %s, the '
                   'Reserved_Bits in Seek_Table_Descriptor must be 0.') \
                    % __format_version__
            raise SeekableFormatError(msg)

        # Frame size
        entry_size = 12 if self._has_checksum else 8
        skippable_frame_size = 17 + frames_number * entry_size
        if fsize < skippable_frame_size:
            raise SeekableFormatError(('File size is less than expected '
                                       'size of the seek table frame.'))

        # Read seek table
        fp.seek(-skippable_frame_size, 2) # 2 is SEEK_END
        skippable_frame = fp.read(skippable_frame_size)
        skippable_magic_number, content_size = \
                self._s_2uint32.unpack_from(skippable_frame, 0)

        # Check format
        if skippable_magic_number != 0x184D2A5E:
            msg = "Seek table frame's Magic_Number is wrong."
            raise SeekableFormatError(msg)
        if content_size != skippable_frame_size - 8:
            msg = "Seek table frame's Frame_Size is wrong."
            raise SeekableFormatError(msg)

        # No more fp operations
        if seek_to_0:
            fp.seek(0)

        # Parse seek table
        offset = 8
        for idx in range(frames_number):
            if self._has_checksum:
                compressed_size, decompressed_size, checksum = \
                    self._s_3uint32.unpack_from(skippable_frame, offset)
                offset += 12
            else:
                compressed_size, decompressed_size = \
                    self._s_2uint32.unpack_from(skippable_frame, offset)
                offset += 8

            # Check format
            if compressed_size == 0 and decompressed_size != 0:
                msg = ('Wrong seek table. The index %d frame (0-based) '
                       'is 0 size, but decompressed size is non-zero, '
                       'this is impossible.') % idx
                raise SeekableFormatError(msg)

            # Append to seek table
            self.append_entry(compressed_size, decompressed_size)

            # Check format
            if self._full_c_size > fsize - skippable_frame_size:
                msg = ('Wrong seek table. Since index %d frame (0-based), '
                       'the cumulated compressed size is greater than '
                       'file size.') % idx
                raise SeekableFormatError(msg)

        # Check format
        if self._full_c_size != fsize - skippable_frame_size:
            raise SeekableFormatError('The cumulated compressed size is wrong')

        # Parsed successfully, save for future use.
        self._seek_frame_size = skippable_frame_size
        self._file_size = fsize

    # Find frame index by decompressed position
    def index_by_dpos(self, pos):
        # Array's first item is 0, so need this.
        if pos < 0:
            pos = 0

        i = bisect_right(self._cumulated_d_size, pos)
        if i != self._frames_count + 1:
            return i
        else:
            # None means >= EOF
            return None

    def get_frame_sizes(self, i):
        return (self._cumulated_c_size[i-1],
                self._cumulated_d_size[i-1])

    def get_full_c_size(self):
        return self._full_c_size

    def get_full_d_size(self):
        return self._full_d_size

    # Merge the seek table to max_frames frames.
    # The format allows up to 0xFFFF_FFFF frames. When frames
    # number exceeds, use this method to merge.
    def _merge_frames(self, max_frames):
        if self._frames_count <= max_frames:
            return

        # Clear the table
        arr = self._frames
        a, b = divmod(self._frames_count, max_frames)
        self._clear_seek_table()

        # Merge frames
        pos = 0
        for i in range(max_frames):
            # Slice length
            length = (a + (1 if i < b else 0)) * 2

            # Merge
            c_size = 0
            d_size = 0
            for j in range(pos, pos+length, 2):
                c_size += arr[j]
                d_size += arr[j+1]
            self.append_entry(c_size, d_size)

            pos += length

    def write_seek_table(self, fp):
        # Exceeded format limit
        if self._frames_count > 0xFFFFFFFF:
            # Emit a warning
            warn(('SeekableZstdFile\'s seek table has %d entries, '
                  'which exceeds the maximal value allowed by '
                  'Zstandard Seekable Format (0xFFFFFFFF). The '
                  'entries will be merged into 0xFFFFFFFF entries, '
                  'this may reduce seeking performance.') % self._frames_count,
                 RuntimeWarning, 3)

            # Merge frames
            self._merge_frames(0xFFFFFFFF)

        # The skippable frame
        offset = 0
        size = 17 + 8 * self._frames_count
        ba = bytearray(size)

        # Header
        self._s_2uint32.pack_into(ba, offset, 0x184D2A5E, size-8)
        offset += 8
        # Entries
        for i in range(0, len(self._frames), 2):
            self._s_2uint32.pack_into(ba, offset,
                                      self._frames[i],
                                      self._frames[i+1])
            offset += 8
        # Footer
        self._s_footer.pack_into(ba, offset,
                                 self._frames_count, 0, 0x8F92EAB1)

        # Write
        fp.write(ba)

    @property
    def seek_frame_size(self):
        return self._seek_frame_size

    @property
    def file_size(self):
        return self._file_size

    def __len__(self):
        return self._frames_count

    def get_info(self):
        return (self._frames_count,
                self._full_c_size,
                self._full_d_size)

class SeekableDecompressReader(ZstdDecompressReader):
    def __init__(self, fp, zstd_dict, option, read_size):
        # Check fp readable/seekable
        if not hasattr(fp, 'readable') or not hasattr(fp, "seekable"):
            raise TypeError(
                ("In SeekableZstdFile's reading mode, the file object should "
                 "have .readable()/.seekable() methods."))
        if not fp.readable():
            raise TypeError(
                ("In SeekableZstdFile's reading mode, the file object should "
                 "be readable."))
        if not fp.seekable():
            raise TypeError(
                ("In SeekableZstdFile's reading mode, the file object should "
                 "be seekable. If the file object is not seekable, it can be "
                 "read sequentially using ZstdFile class."))

        # Load seek table
        self._seek_table = SeekTable(read_mode=True)
        self._seek_table.load_seek_table(fp, seek_to_0=True)

        # Initialize super()
        super().__init__(fp, zstd_dict, option, read_size)
        self._decomp.size = self._seek_table.get_full_d_size()

    # super().seekable() returns self._fp.seekable().
    # Seekable has been checked in .__init__() method.
    # BufferedReader.seek() checks this in each invoke, if self._fp.seekable()
    # becomes False at runtime, .seek() method just raise OSError instead of
    # io.UnsupportedOperation.
    def seekable(self):
        return True

    # If the new position is within BufferedReader's buffer,
    # this method may not be called.
    def seek(self, offset, whence=0):
        # offset is absolute file position
        if whence == 0:    # SEEK_SET
            pass
        elif whence == 1:  # SEEK_CUR
            offset = self._decomp.pos + offset
        elif whence == 2:  # SEEK_END
            offset = self._decomp.size + offset
        else:
            raise ValueError("Invalid value for whence: {}".format(whence))

        # Get new frame index
        new_frame = self._seek_table.index_by_dpos(offset)
        # offset >= EOF
        if new_frame is None:
            self._decomp.eof = True
            self._decomp.pos = self._decomp.size
            self._fp.seek(self._seek_table.file_size)
            return self._decomp.pos

        # Prepare to jump
        old_frame = self._seek_table.index_by_dpos(self._decomp.pos)
        c_pos, d_pos = self._seek_table.get_frame_sizes(new_frame)

        # If at P1, seeking to P2 will unnecessarily read the skippable
        # frame. So check self._fp position to skip the skippable frame.
        #       |--data1--|--skippable--|--data2--|
        # cpos:             ^P1
        # dpos:           ^P1             ^P2
        if new_frame == old_frame and \
           offset >= self._decomp.pos and \
           self._fp.tell() >= c_pos:
            pass
        else:
            # Jump
            self._decomp.eof = False
            self._decomp.pos = d_pos
            self._decomp.reset_session()
            self._fp.seek(c_pos)

        # offset is bytes number to skip forward
        offset -= self._decomp.pos
        # If offset <= 0, .forward() method does nothing.
        self._decomp.forward(offset)

        return self._decomp.pos

    def get_seek_table_info(self):
        return self._seek_table.get_info()

# Compared to ZstdFile class, it's important to handle the seekable
# of underlying file object carefully. Need to check seekable in
# each situation. For example, there may be a CD-R file system that
# is seekable when reading, but not seekable when appending.
class SeekableZstdFile(ZstdFile):
    """This class can only create/write/read Zstandard Seekable Format file,
    or read 0-size file.
    It provides relatively fast seeking ability in read mode.
    """
    # The format uses uint32_t for compressed/decompressed sizes. If flush
    # block a lot, compressed_size may exceed the limit, so set a max size.
    FRAME_MAX_C_SIZE = 2*1024*1024*1024
    # Zstd seekable format's example code also use 1GiB as max content size.
    FRAME_MAX_D_SIZE = 1*1024*1024*1024

    _READER_CLASS = SeekableDecompressReader

    def __init__(self, filename, mode="r", *,
                 level_or_option=None, zstd_dict=None,
                 read_size=131075, write_size=131591,
                 max_frame_content_size=1024*1024*1024):
        """Open a Zstandard Seekable Format file in binary mode. In read mode,
        the file can be 0-size file.

        filename can be either an actual file name (given as a str, bytes, or
        PathLike object), in which case the named file is opened, or it can be
        an existing file object to read from or write to.

        mode can be "r" for reading (default), "w" for (over)writing, "x" for
        creating exclusively, or "a" for appending. These can equivalently be
        given as "rb", "wb", "xb" and "ab" respectively.

        In append mode ("a" or "ab"), filename argument can't be a file object,
        please use file path.

        Parameters
        level_or_option: When it's an int object, it represents compression
            level. When it's a dict object, it contains advanced compression
            parameters. Note, in read mode (decompression), it can only be a
            dict object, that represents decompression option. It doesn't
            support int type compression level in this case.
        zstd_dict: A ZstdDict object, pre-trained dictionary for compression /
            decompression.
        read_size: In reading mode, this is bytes number that read from the
            underlying file object each time, default value is zstd's
            recommended value. If use with Network File System, increasing
            it may get better performance.
        write_size: In writing modes, this is output buffer's size, default
            value is zstd's recommended value. If use with Network File
            System, increasing it may get better performance.
        max_frame_content_size: In write/append modes (compression), when
            the uncompressed data size reaches max_frame_content_size, a frame
            is generated automatically. If the size is small, it will increase
            seeking speed, but reduce compression ratio. If the size is large,
            it will reduce seeking speed, but increase compression ratio. You
            can also manually generate a frame using f.flush(f.FLUSH_FRAME).
        """
        # For self.close()
        self._write_in_close = False
        # For super().close()
        self._fp = None
        self._closefp = False
        self._mode = _MODE_CLOSED

        if mode in ("r", "rb"):
            # Specified max_frame_content_size argument
            if max_frame_content_size != 1024*1024*1024:
                raise ValueError(('max_frame_content_size argument is only '
                                  'valid in write modes (compression).'))
        elif mode in ("w", "wb", "a", "ab", "x", "xb"):
            if not (0 < max_frame_content_size <= self.FRAME_MAX_D_SIZE):
                raise ValueError(
                    ('max_frame_content_size argument should be '
                     '0 < value <= %d, provided value is %d.') % \
                    (self.FRAME_MAX_D_SIZE, max_frame_content_size))

            # For seekable format
            self._max_frame_content_size = max_frame_content_size
            self._reset_frame_sizes()
            self._seek_table = SeekTable(read_mode=False)

            # Load seek table in append mode
            if mode in ("a", "ab"):
                if not isinstance(filename, (str, bytes, PathLike)):
                    raise TypeError(
                            ("In append mode ('a', 'ab'), "
                             "SeekableZstdFile.__init__() method can't "
                             "accept file object as filename argument. "
                             "Please use file path (str/bytes/PathLike)."))

                # Load seek table if file exists
                if isfile(filename):
                    with io.open(filename, "rb") as f:
                        if not hasattr(f, "seekable") or not f.seekable():
                            raise TypeError(
                                ("In SeekableZstdFile's append mode "
                                 "('a', 'ab'), the opened 'rb' file "
                                 "object should be seekable."))
                        self._seek_table.load_seek_table(f, seek_to_0=False)

        super().__init__(filename, mode,
                         level_or_option=level_or_option,
                         zstd_dict=zstd_dict,
                         read_size=read_size,
                         write_size=write_size)

        # Overwrite seek table in append mode
        if mode in ("a", "ab"):
            if self._fp.seekable():
                self._fp.seek(self._seek_table.get_full_c_size())
                # Necessary if the current table has many (0, 0) entries
                self._fp.truncate()
            else:
                # Add the seek table frame
                self._seek_table.append_entry(
                        self._seek_table.seek_frame_size, 0)
                # Emit a warning
                warn(("SeekableZstdFile is opened in append mode "
                      "('a', 'ab'), but the underlying file object "
                      "is not seekable. Therefore the seek table (a "
                      "zstd skippable frame) at the end of the file "
                      "can't be overwritten. Each time open such file "
                      "in append mode, it will waste some storage "
                      "space. %d bytes were wasted this time.") % \
                        self._seek_table.seek_frame_size,
                     RuntimeWarning, 2)

        # Initialized successfully
        self._write_in_close = (self._mode == _MODE_WRITE)

    def _reset_frame_sizes(self):
        self._current_c_size = 0
        self._current_d_size = 0
        self._left_d_size = self._max_frame_content_size

    def close(self):
        """Flush and close the file.

        May be called more than once without error. Once the file is
        closed, any other operation on it will raise a ValueError.
        """
        try:
            if self._write_in_close:
                try:
                    self.flush(self.FLUSH_FRAME)
                    self._seek_table.write_seek_table(self._fp)
                finally:
                    # For multiple calls to .close()
                    self._write_in_close = False
        finally:
            # Clear write mode's seek table.
            # Put here for failures in/after super().__init__().
            self._seek_table = None
            super().close()

    def write(self, data):
        """Write a bytes-like object to the file.

        Returns the number of uncompressed bytes written, which is
        always the length of data in bytes. Note that due to buffering,
        the file on disk may not reflect the data written until .flush()
        or .close() is called.
        """
        if self._mode != _MODE_WRITE:
            self._check_mode(_MODE_WRITE)

        # Accept any data that supports the buffer protocol.
        # And memoryview's subview is faster than slice.
        with memoryview(data) as view, view.cast('B') as byte_view:
            nbytes = byte_view.nbytes
            pos = 0

            while nbytes > 0:
                # Write size
                write_size = min(nbytes, self._left_d_size)

                # Use inserted super().write() method, to prevent
                # self._fp.tell() from reporting incorrect position.
                # -------------------------
                #   super().write() begin
                # -------------------------
                # Compress & write
                _, output_size = self._writer.write(
                                        byte_view[pos:pos+write_size])
                self._pos += write_size
                # -----------------------
                #   super().write() end
                # -----------------------

                pos += write_size
                nbytes -= write_size

                # Cumulate
                self._current_c_size += output_size
                self._current_d_size += write_size
                self._left_d_size -= write_size

                # Should flush a frame
                if self._left_d_size == 0 or \
                   self._current_c_size >= self.FRAME_MAX_C_SIZE:
                    self.flush(self.FLUSH_FRAME)

            return pos

    def flush(self, mode=ZstdFile.FLUSH_BLOCK):
        """Flush remaining data to the underlying stream.

        The mode argument can be ZstdFile.FLUSH_BLOCK, ZstdFile.FLUSH_FRAME.
        Abuse of this method will reduce compression ratio, use it only when
        necessary.

        If the program is interrupted afterwards, all data can be recovered.
        To ensure saving to disk, also need to use os.fsync(fd).

        This method does nothing in reading mode.
        """
        if self._mode != _MODE_WRITE:
            # Like IOBase.flush(), do nothing in reading mode.
            # TextIOWrapper.close() relies on this behavior.
            if self._mode == _MODE_READ:
                return
            # Closed, raise ValueError.
            self._check_mode()

        # Use inserted super().flush() method, to prevent
        # self._fp.tell() from reporting incorrect position.
        # -------------------------
        #   super().flush() begin
        # -------------------------
        # Flush zstd block/frame, and write.
        _, output_size = self._writer.flush(mode)
        # -----------------------
        #   super().flush() end
        # -----------------------

        # Cumulate
        self._current_c_size += output_size
        # self._current_d_size += 0
        # self._left_d_size -= 0

        if mode == self.FLUSH_FRAME and \
           self._current_c_size != 0:
            # Add an entry to seek table
            self._seek_table.append_entry(self._current_c_size,
                                          self._current_d_size)
            self._reset_frame_sizes()

    @property
    def seek_table_info(self):
        """A tuple: (frames_number, compressed_size, decompressed_size)
        1, Frames_number and compressed_size don't count the seek table
           frame (a zstd skippable frame at the end of the file).
        2, In write modes, the part of data that has not been flushed to
           frames is not counted.
        3, If the SeekableZstdFile object is closed, it's None.
        """
        if self._mode == _MODE_WRITE:
            return self._seek_table.get_info()
        elif self._mode == _MODE_READ:
            return self._buffer.raw.get_seek_table_info()
        else:
            # Closed
            return None

    @staticmethod
    def is_seekable_format_file(filename):
        """Check if a file is Zstandard Seekable Format file or 0-size file.

        It parses the seek table at the end of the file, returns True if no
        format error.

        filename can be either a file path (str/bytes/PathLike), or can be an
        existing file object in reading mode.
        """
        # Check argument
        if isinstance(filename, (str, bytes, PathLike)):
            fp = io.open(filename, 'rb')
            is_file_path = True
        elif hasattr(filename, 'readable') and filename.readable() and \
             hasattr(filename, "seekable") and filename.seekable():
            fp = filename
            is_file_path = False
            orig_pos = fp.tell()
        else:
            raise TypeError(
                ('filename argument should be a str/bytes/PathLike object, '
                 'or a file object that is readable and seekable.'))

        # Write mode uses less RAM
        table = SeekTable(read_mode=False)
        try:
            # Read/Parse the seek table
            table.load_seek_table(fp, seek_to_0=False)
        except SeekableFormatError:
            ret = False
        else:
            ret = True
        finally:
            if is_file_path:
                fp.close()
            else:
                fp.seek(orig_pos)

        return ret
