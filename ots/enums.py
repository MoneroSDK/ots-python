"""
Enums based on the OTS enums from `ots.h` header file.
"""

from enum import Enum
from ._ots import lib as _lib


class Network(Enum):
    """
    Enum representing the network type for OTS operations.
    """

    MAIN = _lib.OTS_NETWORK_MAIN
    """Main network, used for production transactions."""
    TEST = _lib.OTS_NETWORK_TEST
    """Test network, used for testing and development."""
    STAGE = _lib.OTS_NETWORK_STAGE
    """Stage network, used for staging and pre-production testing."""

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value


class AddressType(Enum):
    """
    Enum representing the address type for OTS operations.
    """
    STANDARD = _lib.OTS_ADDRESS_TYPE_STANDARD
    """
    Standard address, is the address of account and index of
    any wallet. On mainnet, this address starts with '4'.
    """
    SUBADDRESS = _lib.OTS_ADDRESS_TYPE_SUBADDRESS
    """
    Subaddress, is the address of account != 0 and !=0 index of subaddress.
    On mainnet, this address starts with '8'.
    """
    INTEGRATED = _lib.OTS_ADDRESS_TYPE_INTEGRATED
    """
    Integrated address, is a standard address with an additional payment ID
    integrated into it. This leads that the address has a length of 106 characters,
    instead of 95 characters for standard and subaddresses.
    """

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value


class SeedType(Enum):
    """
    Enum representing the seed type for OTS operations.
    There are some differences in the handling, but the main purpose
    for SeedType is for the Seed Languages which yet differ between
    the now supported Seed Types.
    """

    MONERO = _lib.OTS_SEED_TYPE_MONERO
    """
    Monero 24/25 word seed, used for Monero wallets.
    Also the Monero Legacy Seed (12/13 word seed).
    """
    POLYSEED = _lib.OTS_SEED_TYPE_POLYSEED
    """
    Polyseed, 16 word seed.
    """

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value


class HandleType(Enum):
    """
    Enum representing the handle type for OTS operations.
    """
    INVALID = _lib.OTS_HANDLE_INVALID
    """Invalid handle"""
    WIPEABLE_STRING = _lib.OTS_HANDLE_WIPEABLE_STRING
    """Wipeable string handle, used for sensitive data that should be wiped after use."""
    SEED_INDICES = _lib.OTS_HANDLE_SEED_INDICES
    """Seed indices handle, used for managing seed indices."""
    SEED_LANGUAGE = _lib.OTS_HANDLE_SEED_LANGUAGE
    """Seed language handle, used for managing seed languages."""
    ADDRESS = _lib.OTS_HANDLE_ADDRESS
    """Address handle, used for managing addresses."""
    SEED = _lib.OTS_HANDLE_SEED
    """Seed handle, used for managing seeds."""
    WALLET = _lib.OTS_HANDLE_WALLET
    """Wallet handle, used for managing wallets."""
    TX = _lib.OTS_HANDLE_TX
    """Transaction handle, used for managing transactions."""
    TX_DESCRIPTION = _lib.OTS_HANDLE_TX_DESCRIPTION
    """Transaction description handle, used for managing transaction descriptions."""
    TX_WARNING = _lib.OTS_HANDLE_TX_WARNING
    """Transaction warning handle, used for managing transaction warnings."""

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value


class ResultType(Enum):
    """
    Enum representing the type of result returned by OTS functions.
    """
    NONE = _lib.OTS_RESULT_NONE
    """No result"""
    HANDLE = _lib.OTS_RESULT_HANDLE
    """Handle result, used for returning handles."""
    STRING = _lib.OTS_RESULT_STRING
    """String result, used for returning strings."""
    BOOLEAN = _lib.OTS_RESULT_BOOLEAN
    """Boolean result, used for returning boolean values."""
    NUMBER = _lib.OTS_RESULT_NUMBER
    """Number result, used for returning numeric values."""
    COMPARISON = _lib.OTS_RESULT_COMPARISON
    """Comparison result, used for returning comparison results."""
    ARRAY = _lib.OTS_RESULT_ARRAY
    """Array result, used for returning arrays."""
    ADDRESS_TYPE = _lib.OTS_RESULT_ADDRESS_TYPE
    """Address type result, used for returning address types."""
    NETWORK = _lib.OTS_RESULT_NETWORK
    """Network result, used for returning network types."""
    SEED_TYPE = _lib.OTS_RESULT_SEED_TYPE
    """Seed type result, used for returning seed types."""
    ADDRESS_INDEX = _lib.OTS_RESULT_ADDRESS_INDEX
    """Address index result, used for returning address indices."""

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value


class DataType(Enum):
    """
    Enum representing the data type of the result.
    """
    INVALID = _lib.OTS_DATA_INVALID
    """Invalid data type"""
    INT = _lib.OTS_DATA_INT
    """Integer data type"""
    UINT8 = _lib.OTS_DATA_UINT8
    """Unsigned 8-bit integer data type"""
    UINT16 = _lib.OTS_DATA_UINT16
    """Unsigned 16-bit integer data type"""
    UINT32 = _lib.OTS_DATA_UINT32
    """Unsigned 32-bit integer data type"""
    UINT64 = _lib.OTS_DATA_UINT64
    """Unsigned 64-bit integer data type"""
    HANDLE = _lib.OTS_DATA_HANDLE
    """Handle data type, used for returning handles."""

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value
