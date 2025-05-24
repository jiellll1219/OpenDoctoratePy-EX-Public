from ._ppmd import (
    PPMD8_RESTORE_METHOD_CUT_OFF,
    PPMD8_RESTORE_METHOD_RESTART,
    Ppmd7Decoder,
    Ppmd7Encoder,
    Ppmd8Decoder,
    Ppmd8Encoder,
)

__all__ = (
    "PPMD8_RESTORE_METHOD_CUT_OFF",
    "PPMD8_RESTORE_METHOD_RESTART",
    "Ppmd7Encoder",
    "Ppmd7Decoder",
    "Ppmd8Encoder",
    "Ppmd8Decoder",
    "PpmdError",
)


class PpmdError(Exception):
    "Call to the underlying PPMd library failed."
    pass
