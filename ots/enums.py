from enum import Enum
from ots_cffi_build._ots import ffi, lib


class Network(Enum):
    """
    Enum representing the network type for OTS operations.
    """
    MAIN = lib.OTS_NETWORK_MAIN
    TEST = lib.OTS_NETWORK_TEST
    STAGE = lib.OTS_NETWORK_STAGE

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value


class AddressType(Enum):
    """
    Enum representing the address type for OTS operations.
    """
    STANDARD = lib.OTS_ADDRESS_TYPE_STANDARD
    SUBADDRESS = lib.OTS_ADDRESS_TYPE_SUBADDRESS
    INTEGRATED = lib.OTS_ADDRESS_TYPE_INTEGRATED

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value


class SeedType(Enum):
    """
    Enum representing the seed type for OTS operations.
    """
    MONERO = lib.OTS_SEED_TYPE_MONERO
    POLYSEED = lib.OTS_SEED_TYPE_POLYSEED

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value

class HandleType(Enum):
    """
    Enum representing the handle type for OTS operations.
    """
    INVALID = lib.OTS_HANDLE_INVALID
    WIPEABLE_STRING = lib.OTS_HANDLE_WIPEABLE_STRING
    SEED_INDICES = lib.OTS_HANDLE_SEED_INDICES
    SEED_LANGUAGE = lib.OTS_HANDLE_SEED_LANGUAGE
    ADDRESS = lib.OTS_HANDLE_ADDRESS
    SEED = lib.OTS_HANDLE_SEED
    WALLET = lib.OTS_HANDLE_WALLET
    TX = lib.OTS_HANDLE_TX
    TX_DESCRIPTION = lib.OTS_HANDLE_TX_DESCRIPTION
    TX_WARNING = lib.OTS_HANDLE_TX_WARNING

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value


class ResultType(Enum):
    """
    Enum representing the type of result returned by OTS functions.
    """
    NONE = lib.OTS_RESULT_NONE
    HANDLE = lib.OTS_RESULT_HANDLE
    STRING = lib.OTS_RESULT_STRING
    BOOLEAN = lib.OTS_RESULT_BOOLEAN
    NUMBER = lib.OTS_RESULT_NUMBER
    COMPARISON = lib.OTS_RESULT_COMPARISON
    ARRAY = lib.OTS_RESULT_ARRAY
    ADDRESS_TYPE = lib.OTS_RESULT_ADDRESS_TYPE
    NETWORK = lib.OTS_RESULT_NETWORK
    SEED_TYPE = lib.OTS_RESULT_SEED_TYPE
    ADDRESS_INDEX = lib.OTS_RESULT_ADDRESS_INDEX

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value


class DataType(Enum):
    """
    Enum representing the data type of the result.
    """
    INVALID = lib.OTS_DATA_INVALID
    INT = lib.OTS_DATA_INT
    UINT8 = lib.OTS_DATA_UINT8
    UINT16 = lib.OTS_DATA_UINT16
    UINT32 = lib.OTS_DATA_UINT32
    UINT64 = lib.OTS_DATA_UINT64
    HANDLE = lib.OTS_DATA_HANDLE

    def __int__(self):
        """
        Returns the integer value of the enum member.
        """
        return self.value
