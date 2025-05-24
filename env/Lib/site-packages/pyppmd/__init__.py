from typing import Union

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version  # type: ignore  # noqa

try:
    from .c.c_ppmd import (  # noqa
        PPMD8_RESTORE_METHOD_CUT_OFF,
        PPMD8_RESTORE_METHOD_RESTART,
        Ppmd7Decoder,
        Ppmd7Encoder,
        Ppmd8Decoder,
        Ppmd8Encoder,
        PpmdError,
    )
except ImportError:
    try:
        from .cffi.cffi_ppmd import (  # noqa
            PPMD8_RESTORE_METHOD_CUT_OFF,
            PPMD8_RESTORE_METHOD_RESTART,
            Ppmd7Decoder,
            Ppmd7Encoder,
            Ppmd8Decoder,
            Ppmd8Encoder,
            PpmdError,
        )
    except ImportError:
        msg = "pyppmd module: Neither C implementation nor CFFI " "implementation can be imported."
        raise ImportError(msg)

__all__ = (
    "compress",
    "decompress",
    "PPMD8_RESTORE_METHOD_RESTART",
    "PPMD8_RESTORE_METHOD_CUT_OFF",
    "Ppmd7Encoder",
    "Ppmd7Decoder",
    "Ppmd8Encoder",
    "Ppmd8Decoder",
    "PpmdError",
)

__doc__ = """\
Python bindings to PPMd compression library, the API is similar to
Python's bz2/lzma/zlib module.

Documentation: https://pyppmd.readthedocs.io
Github: https://github.com/miurahr/pyppmd
PyPI: https://pypi.org/project/pyppmd"""

__copyright__ = "Copyright (C) 2020,2021 Hiroshi Miura"

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no-cover
    # package is not installed
    __version__ = "unknown"


class PpmdCompressor:
    """Compressor class to compress data by PPMd algorithm."""

    def __init__(
        self,
        max_order: int = 6,
        mem_size: int = 8 << 20,
        *,
        restore_method=PPMD8_RESTORE_METHOD_RESTART,
        variant: str = "I",
    ):
        if variant not in ["H", "I", "h", "i"]:
            raise ValueError("Unsupported PPMd variant")
        if variant in ["I", "i"]:
            self.encoder = Ppmd8Encoder(max_order, mem_size, restore_method)
        else:
            self.encoder = Ppmd7Encoder(max_order, mem_size)
        self.eof = False

    def compress(self, data_or_str: Union[bytes, bytearray, memoryview, str]):
        if type(data_or_str) == str:
            data = data_or_str.encode("UTF-8")
        elif _is_bytelike(data_or_str):
            data = data_or_str
        else:
            raise ValueError("Argument data_or_str is neither bytes-like object nor str.")
        return self.encoder.encode(data)

    def flush(self):
        self.eof = True
        return self.encoder.flush()


class PpmdDecompressor:
    """Decompressor class to decompress data by PPMd algorithm."""

    def __init__(
        self,
        max_order: int = 6,
        mem_size: int = 8 << 20,
        *,
        restore_method=PPMD8_RESTORE_METHOD_RESTART,
        variant: str = "I",
    ):
        if variant not in ["H", "I", "h", "i"]:
            raise ValueError("Unsupported PPMd variant")
        if variant in ["I", "i"]:
            self.decoder = Ppmd8Decoder(max_order=max_order, mem_size=mem_size, restore_method=restore_method)
        else:
            self.decoder = Ppmd7Decoder(max_order=max_order, mem_size=mem_size)
        self.eof = False
        self.need_input = True

    def decompress(self, data: Union[bytes, memoryview]):
        if self.decoder.eof:
            self.eof = True
            return b""
        if self.decoder.needs_input and len(data) == 0:
            raise PpmdError("No enough data is provided for decompression.")
        elif not self.decoder.needs_input and len(data) > 0:
            raise PpmdError("Unused data is given.")
        return self.decoder.decode(data)


def compress(
    data_or_str: Union[bytes, bytearray, memoryview, str],
    *,
    max_order: int = 6,
    mem_size: int = 16 << 20,
    variant: str = "I",
) -> bytes:
    """Compress a block of data, return a bytes object.
    When pass `str` object, encoding "UTF-8" first, then compress it.

    Arguments
    data_or_str: A bytes-like object or string data to be compressed.
    max_order:   An integer object represent compression level.
    mem_size:    An integer object represent memory size to use.
    variant:   A variant name of PPMd compression algorithms, accept only "H" or "I"
    """
    if variant not in ["H", "I", "h", "i"]:
        raise ValueError("Unsupported PPMd variant")
    if type(data_or_str) == str:
        data = data_or_str.encode("UTF-8")
    elif _is_bytelike(data_or_str):
        data = data_or_str
    else:
        raise ValueError("Argument data_or_str is neither bytes-like object nor str.")
    if variant in ["I", "i"]:
        comp = Ppmd8Encoder(max_order, mem_size)
    else:
        comp = Ppmd7Encoder(max_order, mem_size)
    result = comp.encode(data)
    return result + comp.flush()


def decompress_str(
    data: Union[bytes, bytearray, memoryview],
    *,
    max_order: int = 6,
    mem_size: int = 16 << 20,
    encoding: str = "UTF-8",
    variant: str = "I",
) -> Union[bytes, str]:
    """Decompress a PPMd data, return a bytes object.

    Arguments
    data:      A bytes-like object, compressed data.
    max_order: An integer object represent max order of PPMd.
    mem_size:  An integer object represent memory size to use.
    encoding:  Encoding of compressed text data, when it is None return as bytes. Default is UTF-8
    variant:   A variant name of PPMd compression algorithms, accept only "H" or "I"
    """
    if not _is_bytelike(data):
        raise ValueError("Argument data should be bytes-like object.")
    if variant not in ["H", "I", "h", "i"]:
        raise ValueError("Unsupported PPMd variant")
    if variant in ["I", "i"]:
        return _decompress8(data, max_order, mem_size).decode(encoding)
    else:
        return _decompress7(data, max_order, mem_size).decode(encoding)


def decompress(
    data: Union[bytes, bytearray, memoryview],
    *,
    max_order: int = 6,
    mem_size: int = 16 << 20,
    variant: str = "I",
) -> Union[bytes, str]:
    """Decompress a PPMd data, return a bytes object.

    Arguments
    data:      A bytes-like object, compressed data.
    max_order: An integer object represent max order of PPMd.
    mem_size:  An integer object represent memory size to use.
    variant:   A variant name of PPMd compression algorithms, accept only "H" or "I"
    """
    if not _is_bytelike(data):
        raise ValueError("Argument data should be bytes-like object.")
    if variant not in ["H", "I", "h", "i"]:
        raise ValueError("Unsupported PPMd variant")
    if variant in ["I", "i"]:
        return _decompress8(data, max_order, mem_size)
    else:
        return _decompress7(data, max_order, mem_size)


def _decompress7(data: Union[bytes, bytearray, memoryview], max_order: int, mem_size: int):
    decomp = Ppmd7Decoder(max_order, mem_size)
    res = decomp.decode(data)
    return res


def _decompress8(data: Union[bytes, bytearray, memoryview], max_order: int, mem_size: int):
    decomp = Ppmd8Decoder(max_order, mem_size)
    res = decomp.decode(data)
    return res


def _is_bytelike(data):
    if isinstance(data, bytes) or isinstance(data, bytearray) or isinstance(data, memoryview):
        return True
    return False
