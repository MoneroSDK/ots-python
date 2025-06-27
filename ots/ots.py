from .raw import *
from .exceptions import OtsException
from .enums import *
from .procedural import (
    version,
    random,
    random32,
)


class Ots:
    """
    A class with only static helper methods for the OTS library.
    """


    @staticmethod
    def version() -> str:
        """
        Returns the version of the OTS library.
        """
        return version()

    @staticmethod
    def versionComponets() -> tuple[int, int, int]:
        """
        Returns the version components of the OTS library as a tuple.
        """
        result: ots_result_t = ots_version_components()
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return tuple(ots_result_int_array(result))

    @staticmethod
    def heightFromTimestamp(timestamp: int, network: Network | int = Network.MAIN) -> int:
        """
        Returns the height of the OTS tree for a given timestamp and network.

        :param timestamp: The timestamp to use for height calculation.
        :param network: The network to use (default is Network.MAIN).
        :return: The height of the OTS tree.
        """
        assert isinstance(network, (Network, int)), "Network must be an instance of Network or an integer."
        assert isinstance(timestamp, int), "Timestamp must be an integer."
        assert timestamp >= 0, "Timestamp must be a non-negative integer."
        result: ots_result_t = ots_height_from_timestamp(timestamp, int(network))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_number(result)

    @staticmethod
    def timestampFromHeight(height: int, network: Network | int = Network.MAIN) -> int:
        """
        Returns the timestamp for a given OTS tree height and network.

        :param height: The height of the OTS tree.
        :param network: The network to use (default is Network.MAIN).
        :return: The timestamp corresponding to the given height.
        """
        assert isinstance(network, (Network, int)), "Network must be an instance of Network or an integer."
        assert isinstance(height, int), "Height must be an integer."
        assert height >= 0, "Height must be a non-negative integer."
        result: ots_result_t = ots_timestamp_from_height(height, int(network))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_number(result)

    @staticmethod
    def random(size: int) -> bytes:
        """
        Returns a random byte string of the specified size.

        :param size: The number of random bytes to generate.
        :return: A byte string containing the random bytes.
        """
        return random(size)

    @staticmethod
    def random32() -> bytes:
        """
        Returns a random 32-byte string.
        """
        return random32()

    @staticmethod
    def lowEntropy(data: bytes, minEntropy: float) -> bool:  # TODO: should set OTS_MIN_ENTROPY as default (from where to take?)
        """
        Checks if the provided data has low entropy.

        :param data: The byte string to check for entropy.
        :param minEntropy: The minimum entropy threshold.
        :return: True if the data has low entropy, False otherwise.
        """
        assert isinstance(data, bytes), "Data must be a byte string."
        assert isinstance(minEntropy, float), "Minimum entropy must be a number."
        result: ots_result_t = ots_check_low_entropy(data, minEntropy)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_bool(result)

    @staticmethod
    def setEnforceEntropy(enforce: bool = True) -> None:
        """
        Sets whether to enforce minimum entropy for OTS operations.

        :param enforce: Whether to enforce minimum entropy.
        """
        assert isinstance(enforce, bool), "Enforce must be a boolean."
        result: ots_result_t = ots_set_enforce_entropy(enforce)
        if ots_is_error(result):
            raise OtsException.from_result(result)

    @staticmethod
    def setEnforceEntropyLevel(minEntropy: float) -> bool:  # TODO: should set OTS_MIN_ENTROPY as default (from where to take?)
        """
        Sets the minimum entropy level for OTS operations.

        :param minEntropy: The minimum entropy threshold.
        """
        assert isinstance(minEntropy, float), "Minimum entropy must be a number."
        result: ots_result_t = ots_set_enforce_entropy_level(minEntropy)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_bool(result)

    @staticmethod
    def setMaxAccountDepth(depth: int) -> None:
        """
        Sets the maximum account depth for OTS operations.

        :param depth: The maximum account depth to set.
        """
        assert isinstance(depth, int), "Depth must be an integer."
        assert depth >= 0, "Depth must be a non-negative integer."
        result: ots_result_t = ots_set_max_account_depth(depth)
        if ots_is_error(result):
            raise OtsException.from_result(result)

    @staticmethod
    def setMaxIndexDepth(depth: int) -> None:
        """
        Sets the maximum index depth for OTS operations.

        :param depth: The maximum index depth to set.
        """
        assert isinstance(depth, int), "Depth must be an integer."
        assert depth >= 0, "Depth must be a non-negative integer."
        result: ots_result_t = ots_set_max_index_depth(depth)
        if ots_is_error(result):
            raise OtsException.from_result(result)

    @staticmethod
    def setMaxDepth(accountDepth: int, indexDepth: int) -> None:
        """
        Sets the maximum account and index depth for OTS operations.

        :param accountDepth: The maximum account depth to set.
        :param indexDepth: The maximum index depth to set.
        """
        assert isinstance(accountDepth, int), "Account depth must be an integer."
        assert accountDepth >= 0, "Account depth must be a non-negative integer."
        assert isinstance(indexDepth, int), "Index depth must be an integer."
        assert indexDepth >= 0, "Index depth must be a non-negative integer."
        result: ots_result_t = ots_set_max_depth(accountDepth, indexDepth)
        if ots_is_error(result):
            raise OtsException.from_result(result)

    @staticmethod
    def resetMaxDepth() -> None:
        """
        Resets the maximum account and index depth to their default values.
        """
        result: ots_result_t = ots_reset_max_depth()
        if ots_is_error(result):
            raise OtsException.from_result(result)

    @staticmethod
    def maxAccountDepth(default: int = 0) -> int:
        """
        Returns the maximum account depth for OTS operations.
        """
        return ots_get_max_account_depth(default)

    @staticmethod
    def maxIndexDepth(default: int = 0) -> int:
        """
        Returns the maximum index depth for OTS operations.
        """
        return ots_get_max_index_depth(default)
