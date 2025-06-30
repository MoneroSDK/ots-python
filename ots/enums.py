from enum import Enum
from ._ots import lib as _lib


class Network(Enum):
    """
    Enum representing the network type for OTS operations.
    """
    MAIN = _lib.OTS_NETWORK_MAIN
    TEST = _lib.OTS_NETWORK_TEST
    STAGE = _lib.OTS_NETWORK_STAGE

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
    SUBADDRESS = _lib.OTS_ADDRESS_TYPE_SUBADDRESS
    INTEGRATED = _lib.OTS_ADDRESS_TYPE_INTEGRATED

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value


class SeedType(Enum):
    """
    Enum representing the seed type for OTS operations.
    """
    MONERO = _lib.OTS_SEED_TYPE_MONERO
    POLYSEED = _lib.OTS_SEED_TYPE_POLYSEED

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
    WIPEABLE_STRING = _lib.OTS_HANDLE_WIPEABLE_STRING
    SEED_INDICES = _lib.OTS_HANDLE_SEED_INDICES
    SEED_LANGUAGE = _lib.OTS_HANDLE_SEED_LANGUAGE
    ADDRESS = _lib.OTS_HANDLE_ADDRESS
    SEED = _lib.OTS_HANDLE_SEED
    WALLET = _lib.OTS_HANDLE_WALLET
    TX = _lib.OTS_HANDLE_TX
    TX_DESCRIPTION = _lib.OTS_HANDLE_TX_DESCRIPTION
    TX_WARNING = _lib.OTS_HANDLE_TX_WARNING

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
    HANDLE = _lib.OTS_RESULT_HANDLE
    STRING = _lib.OTS_RESULT_STRING
    BOOLEAN = _lib.OTS_RESULT_BOOLEAN
    NUMBER = _lib.OTS_RESULT_NUMBER
    COMPARISON = _lib.OTS_RESULT_COMPARISON
    ARRAY = _lib.OTS_RESULT_ARRAY
    ADDRESS_TYPE = _lib.OTS_RESULT_ADDRESS_TYPE
    NETWORK = _lib.OTS_RESULT_NETWORK
    SEED_TYPE = _lib.OTS_RESULT_SEED_TYPE
    ADDRESS_INDEX = _lib.OTS_RESULT_ADDRESS_INDEX

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
    INT = _lib.OTS_DATA_INT
    UINT8 = _lib.OTS_DATA_UINT8
    UINT16 = _lib.OTS_DATA_UINT16
    UINT32 = _lib.OTS_DATA_UINT32
    UINT64 = _lib.OTS_DATA_UINT64
    HANDLE = _lib.OTS_DATA_HANDLE

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value
