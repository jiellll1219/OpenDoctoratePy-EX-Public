import io
try:
    from os import PathLike
except ImportError:
    # For Python 3.5
    class PathLike:
        pass

from pyzstd import ZstdCompressor, ZstdFileReader, \
                   ZstdFileWriter, _ZSTD_DStreamSizes

__all__ = ('ZstdFile', 'open')

class ZstdDecompressReader(io.RawIOBase):
    """Adapt decompressor to RawIOBase reader API"""

    def __init__(self, fp, zstd_dict, option, read_size):
        self._fp = fp
        self._decomp = ZstdFileReader(fp, zstd_dict, option, read_size)

    def close(self):
        self._decomp = None
        return super().close()

    def readable(self):
        return True

    # Some file-like objects don't have .seekable(), invoke when necessary.
    def seekable(self):
        return self._fp.seekable()

    def tell(self):
        return self._decomp.pos

    def readinto(self, b):
        return self._decomp.readinto(b)

    def readall(self):
        return self._decomp.readall()

    # If the new position is within io.BufferedReader's buffer,
    # this method may not be called.
    def seek(self, offset, whence=0):
        # offset is absolute file position
        if whence == 0:    # SEEK_SET
            pass
        elif whence == 1:  # SEEK_CUR
            offset = self._decomp.pos + offset
        elif whence == 2:  # SEEK_END
            if self._decomp.size < 0:
                # Get file size
                self._decomp.forward(None)
            offset = self._decomp.size + offset
        else:
            raise ValueError("Invalid whence value: {}".format(whence))

        # offset is bytes number to skip forward
        if offset < self._decomp.pos:
            # Rewind
            self._decomp.eof = False
            self._decomp.pos = 0
            self._decomp.reset_session()
            self._fp.seek(0)
        else:
            offset -= self._decomp.pos
        # If offset <= 0, .forward() method does nothing.
        self._decomp.forward(offset)

        return self._decomp.pos

_ZSTD_DStreamOutSize = _ZSTD_DStreamSizes[1]

_MODE_CLOSED = 0
_MODE_READ   = 1
_MODE_WRITE  = 2

class ZstdFile(io.BufferedIOBase):
    """A file object providing transparent zstd (de)compression.

    A ZstdFile can act as a wrapper for an existing file object, or refer
    directly to a named file on disk.

    Note that ZstdFile provides a *binary* file interface - data read is
    returned as bytes, and data to be written should be an object that
    supports the Buffer Protocol.
    """
    FLUSH_BLOCK = ZstdCompressor.FLUSH_BLOCK
    FLUSH_FRAME = ZstdCompressor.FLUSH_FRAME

    _READER_CLASS = ZstdDecompressReader

    def __init__(self, filename, mode="r", *,
                 level_or_option=None, zstd_dict=None,
                 read_size=131075, write_size=131591):
        """Open a zstd compressed file in binary mode.

        filename can be either an actual file name (given as a str, bytes, or
        PathLike object), in which case the named file is opened, or it can be
        an existing file object to read from or write to.

        mode can be "r" for reading (default), "w" for (over)writing, "x" for
        creating exclusively, or "a" for appending. These can equivalently be
        given as "rb", "wb", "xb" and "ab" respectively.

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
        """
        self._fp = None
        self._closefp = False
        self._mode = _MODE_CLOSED

        # Read or write mode
        if mode in ("r", "rb"):
            if not isinstance(level_or_option, (type(None), dict)):
                raise TypeError(
                    ("In read mode (decompression), level_or_option argument "
                     "should be a dict object, that represents decompression "
                     "option. It doesn't support int type compression level "
                     "in this case."))
            if write_size != 131591:
                raise ValueError(
                    "write_size argument is only valid in write modes.")
            mode_code = _MODE_READ
        elif mode in ("w", "wb", "a", "ab", "x", "xb"):
            if not isinstance(level_or_option, (type(None), int, dict)):
                raise TypeError(("level_or_option argument "
                                 "should be int or dict object."))
            if read_size != 131075:
                raise ValueError(
                    "read_size argument is only valid in read mode.")
            mode_code = _MODE_WRITE
        else:
            raise ValueError("Invalid mode: {!r}".format(mode))

        # File object
        if isinstance(filename, (str, bytes, PathLike)):
            if "b" not in mode:
                mode += "b"
            self._fp = io.open(filename, mode)
            self._closefp = True
        elif hasattr(filename, "read") or hasattr(filename, "write"):
            self._fp = filename
        else:
            raise TypeError(("filename must be a str, bytes, "
                             "file or PathLike object"))

        # Set ._mode here for ._closefp in .close(). If the following code
        # fails, IOBase's cleanup code will call .close(), so that ._fp can
        # be closed.
        self._mode = mode_code

        # Reader or writer
        if mode_code == _MODE_READ:
            raw = self._READER_CLASS(
                            self._fp,
                            zstd_dict=zstd_dict,
                            option=level_or_option,
                            read_size=read_size)
            self._buffer = io.BufferedReader(raw, _ZSTD_DStreamOutSize)
        elif mode_code == _MODE_WRITE:
            self._pos = 0
            self._writer = ZstdFileWriter(
                            self._fp,
                            level_or_option=level_or_option,
                            zstd_dict=zstd_dict,
                            write_size=write_size)

    def close(self):
        """Flush and close the file.

        May be called more than once without error. Once the file is
        closed, any other operation on it will raise a ValueError.
        """
        if self._mode == _MODE_CLOSED:
            return

        try:
            # In .__init__ method, if fails after setting ._mode attribute,
            # these attributes don't exist.
            if hasattr(self, "_buffer"):
                try:
                    self._buffer.close()
                finally:
                    # Set to None for ._check_mode()
                    self._buffer = None
            elif hasattr(self, "_writer"):
                try:
                    self.flush(self.FLUSH_FRAME)
                finally:
                    # Set to None for ._check_mode()
                    self._writer = None
        finally:
            try:
                if self._closefp:
                    self._fp.close()
            finally:
                self._fp = None
                self._closefp = False
                self._mode = _MODE_CLOSED

    # None argument means the file should be closed
    def _check_mode(self, expected_mode=None):
        # If closed, raise ValueError.
        if self._mode == _MODE_CLOSED:
            raise ValueError("I/O operation on closed file")

        # Check _MODE_READ/_MODE_WRITE mode
        if expected_mode == _MODE_READ:
            if self._mode != _MODE_READ:
                raise io.UnsupportedOperation("File not open for reading")
        elif expected_mode == _MODE_WRITE:
            if self._mode != _MODE_WRITE:
                raise io.UnsupportedOperation("File not open for writing")

        # Re-raise other AttributeError exception
        raise

    # If modify this method, also modify SeekableZstdFile.write() method.
    def write(self, data):
        """Write a bytes-like object to the file.

        Returns the number of uncompressed bytes written, which is
        always the length of data in bytes. Note that due to buffering,
        the file on disk may not reflect the data written until .flush()
        or .close() is called.
        """
        # Compress & write
        try:
            input_size, _ = self._writer.write(data)
        except AttributeError:
            self._check_mode(_MODE_WRITE)

        self._pos += input_size
        return input_size

    # If modify this method, also modify SeekableZstdFile.flush() method.
    def flush(self, mode=FLUSH_BLOCK):
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

        # Flush zstd block/frame, and write.
        self._writer.flush(mode)

    def read(self, size=-1):
        """Read up to size uncompressed bytes from the file.

        If size is negative or omitted, read until EOF is reached.
        Returns b"" if the file is already at EOF.
        """
        if size is None:
            size = -1
        try:
            return self._buffer.read(size)
        except AttributeError:
            self._check_mode(_MODE_READ)

    def read1(self, size=-1):
        """Read up to size uncompressed bytes, while trying to avoid
        making multiple reads from the underlying stream. Reads up to a
        buffer's worth of data if size is negative.

        Returns b"" if the file is at EOF.
        """
        if size < 0:
            size = _ZSTD_DStreamOutSize

        try:
            return self._buffer.read1(size)
        except AttributeError:
            self._check_mode(_MODE_READ)

    def readinto(self, b):
        """Read bytes into b.

        Returns the number of bytes read (0 for EOF).
        """
        try:
            return self._buffer.readinto(b)
        except AttributeError:
            self._check_mode(_MODE_READ)

    def readinto1(self, b):
        """Read bytes into b, while trying to avoid making multiple reads
        from the underlying stream.

        Returns the number of bytes read (0 for EOF).
        """
        try:
            return self._buffer.readinto1(b)
        except AttributeError:
            self._check_mode(_MODE_READ)

    def readline(self, size=-1):
        """Read a line of uncompressed bytes from the file.

        The terminating newline (if present) is retained. If size is
        non-negative, no more than size bytes will be read (in which
        case the line may be incomplete). Returns b'' if already at EOF.
        """
        if size is None:
            size = -1
        try:
            return self._buffer.readline(size)
        except AttributeError:
            self._check_mode(_MODE_READ)

    def seek(self, offset, whence=io.SEEK_SET):
        """Change the file position.

        The new position is specified by offset, relative to the
        position indicated by whence. Possible values for whence are:

            0: start of stream (default): offset must not be negative
            1: current stream position
            2: end of stream; offset must not be positive

        Returns the new file position.

        Note that seeking is emulated, so depending on the arguments,
        this operation may be extremely slow.
        """
        try:
            # BufferedReader.seek() checks seekable
            return self._buffer.seek(offset, whence)
        except AttributeError:
            self._check_mode(_MODE_READ)

    def peek(self, size=-1):
        """Return buffered data without advancing the file position.

        Always returns at least one byte of data, unless at EOF.
        The exact number of bytes returned is unspecified.
        """
        # Relies on the undocumented fact that BufferedReader.peek() always
        # returns at least one byte (except at EOF)
        try:
            return self._buffer.peek(size)
        except AttributeError:
            self._check_mode(_MODE_READ)

    def __iter__(self):
        try:
            self._buffer
        except AttributeError:
            self._check_mode(_MODE_READ)
        return self

    def __next__(self):
        ret = self._buffer.readline()
        if ret:
            return ret
        raise StopIteration

    def tell(self):
        """Return the current file position."""
        if self._mode == _MODE_READ:
            return self._buffer.tell()
        elif self._mode == _MODE_WRITE:
            return self._pos

        # Closed, raise ValueError.
        self._check_mode()

    def fileno(self):
        """Return the file descriptor for the underlying file."""
        try:
            return self._fp.fileno()
        except AttributeError:
            # Closed, raise ValueError.
            self._check_mode()

    @property
    def closed(self):
        """True if this file is closed."""
        return self._mode == _MODE_CLOSED

    def writable(self):
        """Return whether the file was opened for writing."""
        if self._mode == _MODE_WRITE:
            return True
        elif self._mode == _MODE_READ:
            return False

        # Closed, raise ValueError.
        self._check_mode()

    def readable(self):
        """Return whether the file was opened for reading."""
        if self._mode == _MODE_READ:
            return True
        elif self._mode == _MODE_WRITE:
            return False

        # Closed, raise ValueError.
        self._check_mode()

    def seekable(self):
        """Return whether the file supports seeking."""
        if self._mode == _MODE_READ:
            return self._buffer.seekable()
        elif self._mode == _MODE_WRITE:
            return False

        # Closed, raise ValueError.
        self._check_mode()


# Copied from lzma module
def open(filename, mode="rb", *, level_or_option=None, zstd_dict=None,
         encoding=None, errors=None, newline=None):
    """Open a zstd compressed file in binary or text mode.

    filename can be either an actual file name (given as a str, bytes, or
    PathLike object), in which case the named file is opened, or it can be an
    existing file object to read from or write to.

    The mode parameter can be "r", "rb" (default), "w", "wb", "x", "xb", "a",
    "ab" for binary mode, or "rt", "wt", "xt", "at" for text mode.

    The level_or_option and zstd_dict parameters specify the settings, as for
    ZstdCompressor, ZstdDecompressor and ZstdFile.

    When using read mode (decompression), the level_or_option parameter can
    only be a dict object, that represents decompression option. It doesn't
    support int type compression level in this case.

    For binary mode, this function is equivalent to the ZstdFile constructor:
    ZstdFile(filename, mode, ...). In this case, the encoding, errors and
    newline parameters must not be provided.

    For text mode, an ZstdFile object is created, and wrapped in an
    io.TextIOWrapper instance with the specified encoding, error handling
    behavior, and line ending(s).
    """

    if "t" in mode:
        if "b" in mode:
            raise ValueError("Invalid mode: %r" % (mode,))
    else:
        if encoding is not None:
            raise ValueError("Argument 'encoding' not supported in binary mode")
        if errors is not None:
            raise ValueError("Argument 'errors' not supported in binary mode")
        if newline is not None:
            raise ValueError("Argument 'newline' not supported in binary mode")

    zstd_mode = mode.replace("t", "")
    binary_file = ZstdFile(filename, zstd_mode,
                           level_or_option=level_or_option, zstd_dict=zstd_dict)

    if "t" in mode:
        return io.TextIOWrapper(binary_file, encoding, errors, newline)
    else:
        return binary_file
