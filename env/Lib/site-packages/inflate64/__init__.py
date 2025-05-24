try:
    from importlib import metadata
except ImportError: # for Python<3.8
    import importlib_metadata as metadata

from ._inflate64 import Deflater, Inflater  # noqa

__all__ = ["Deflater", "Inflater"]

__doc__ = """\
Python library to inflate data, the API is similar to Python's bz2/lzma/zlib module.
"""

__copyright__ = "Copyright (C) 2022 Hiroshi Miura"

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:  # pragma: no-cover
    # package is not installed
    __version__ = "0.1.0"
