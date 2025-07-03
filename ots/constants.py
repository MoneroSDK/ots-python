"""
Constants from the `ots.h` header file.
"""

from ._ots import lib as _lib


OTS_MAX_ERROR_MESSAGE = _lib.OTS_MAX_ERROR_MESSAGE
"""Maximum length of the error message string."""
OTS_MAX_ERROR_CLASS = _lib.OTS_MAX_ERROR_CLASS
"""Maximum length of the error class string."""
OTS_MAX_VERSION_STRING = _lib.OTS_MAX_VERSION_STRING
"""Maximum length of the version string."""
OTS_MONERO_SEED_WORDS = _lib.OTS_MONERO_SEED_WORDS
"""Number of words of Monero seed phrases."""
OTS_POLYSEED_WORDS = _lib.OTS_POLYSEED_WORDS
"""Number of words of Monero polyseed phrases."""
OTS_LEGACY_SEED_WORDS = _lib.OTS_LEGACY_SEED_WORDS
"""Number of words of Monero legacy seed phrases."""
