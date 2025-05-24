# PyBcj library.
# Copyright 2020-2022 Hiroshi Miura
# SPDX-License-Identifier: LGPL-2.1-or-later
#
try:
    from importlib.metadata import PackageNotFoundError  # type: ignore
    from importlib.metadata import version  # type: ignore
except ImportError:
    from importlib_metadata import PackageNotFoundError  # type: ignore
    from importlib_metadata import version  # type: ignore
try:
    from ._bcj import (
        ARMDecoder,
        ARMEncoder,
        ARMTDecoder,
        ARMTEncoder,
        BCJDecoder,
        BCJEncoder,
        IA64Decoder,
        IA64Encoder,
        PPCDecoder,
        PPCEncoder,
        SparcDecoder,
        SparcEncoder,
    )
except ImportError:
    try:
        from ._bcjfilter import (
            ARMDecoder,
            ARMEncoder,
            ARMTDecoder,
            ARMTEncoder,
            BCJDecoder,
            BCJEncoder,
            IA64Decoder,
            IA64Encoder,
            PPCDecoder,
            PPCEncoder,
            SparcDecoder,
            SparcEncoder,
        )
    except ImportError:
        msg = "pybcj module: Neither C implementation nor Python implementation can be imported."
        raise ImportError(msg)

__all__ = (
    ARMDecoder,
    ARMEncoder,
    ARMTDecoder,
    ARMTEncoder,
    BCJDecoder,
    BCJEncoder,
    IA64Decoder,
    IA64Encoder,
    PPCDecoder,
    PPCEncoder,
    SparcDecoder,
    SparcEncoder,
)

__copyright__ = "Copyright (C) 2021 Hiroshi Miura"

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no-cover
    # package is not installed
    __version__ = "unknown"

__doc__ = """\
Python bindings to BCJ filter library.

Documentation: https://pybcj.readthedocs.io
Github: https://github.com/miurahr/pybcj
PyPI: https://pypi.org/project/pybcj"""
