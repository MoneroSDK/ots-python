from .raw import *
from .exceptions import OtsException
from .enums import *
from .address import Address
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
        return tuple(int(i) for i in ots_result_int_array(result))

    @staticmethod
    def heightFromTimestamp(timestamp: int, network: Network | int = Network.MAIN) -> int:
        """
        Returns the estimated blockchain height for a given timestamp and network.

        :param int timestamp: The timestamp to use for height calculation.
        :param network: The network to use (default is :py:attr:`Network.MAIN`).
        :type network: Network | int
        :return: The blockchain height for the given timestamp.
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
        Returns the estimated timestamp for a given blockchain height and network.

        :param int height: The height of the OTS tree.
        :param network: The network to use (default is Network.MAIN).
        :type network: Network | int
        :return: The timestamp corresponding to the given blockchain height.
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
        Returns a random bytes of the specified size.

        .. note::

            By default on low entropy the library will raise
            an exception, this happens also if the size of bytes
            is low. There is probably no much sense in using less
            then 19 bytes ever, but if really needed,
            calling :py:meth:`setEnforceEntropy`
            with :py:const:`False` will disable
            the behavior of raising an exception on low entropy,
            which practically allows any crap random bytes to use
            in the library.

        :param int size: The number of random bytes to generate.
        :return: A byte string containing the random bytes.
        """
        return random(size)

    @staticmethod
    def random32() -> bytes:
        """
        Returns a random 32 bytes.
        """
        return random32()

    @staticmethod
    def lowEntropy(data: bytes, minEntropy: float) -> bool:  # TODO: should set OTS_MIN_ENTROPY as default (from where to take?)
        """
        Checks if the provided data has low entropy.

        :param bytes data: The byte string to check for entropy.
        :param float minEntropy: The minimum entropy threshold.
        :return: True if the data has low entropy, False otherwise.
        """
        assert isinstance(data, bytes), "Data must be a byte string."
        assert isinstance(minEntropy, float), "Minimum entropy must be a number."
        result: ots_result_t = ots_check_low_entropy(data, minEntropy)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def setEnforceEntropy(enforce: bool = True) -> None:
        """
        Sets whether to enforce minimum entropy for OTS operations.
        This is a security measure to ensure that random
        data is not of bad quality. And will ensure that
        there is sufficient entropy in the random data or
        the library will raise an exception.

        :param bool enforce: Whether to enforce minimum entropy.
        """
        assert isinstance(enforce, bool), "Enforce must be a boolean."
        ots_set_enforce_entropy(enforce)

    @staticmethod
    def setEnforceEntropyLevel(minEntropy: float) -> None:  # TODO: should set OTS_MIN_ENTROPY as default (from where to take?)
        """
        Sets the minimum entropy level for OTS operations.
        This is a security measure to ensure that random
        data is not of bad quality. And will ensure that
        there is sufficient entropy in the random data or
        the library will raise an exception.

        :param float minEntropy: The minimum entropy threshold.
        """
        assert isinstance(minEntropy, float), "Minimum entropy must be a number."
        ots_set_enforce_entropy_level(minEntropy)

    @staticmethod
    def setMaxAccountDepth(depth: int) -> None:
        """
        Sets the maximum account depth for OTS operations.
        Searching addresses or outputs in a account is restricted
        to the maximum depth, if not specified otherwise.

        :param int depth: The maximum account depth to set.
        """
        assert isinstance(depth, int), "Depth must be an integer."
        assert depth >= 0, "Depth must be a non-negative integer."
        ots_set_max_account_depth(depth)

    @staticmethod
    def setMaxIndexDepth(depth: int) -> None:
        """
        Sets the maximum index depth for OTS operations.
        Searching addresses or outputs in a index is restricted
        to the maximum depth, if not specified otherwise.

        :param int depth: The maximum index depth to set.
        """
        assert isinstance(depth, int), "Depth must be an integer."
        assert depth >= 0, "Depth must be a non-negative integer."
        ots_set_max_index_depth(depth)

    @staticmethod
    def setMaxDepth(accountDepth: int, indexDepth: int) -> None:
        """
        Sets the maximum account and index depth for OTS operations.
        This is the combined method to set both account and index depths.
        Searching addresses or outputs in a account or index is restricted
        to the maximum depth, if not specified otherwise.

        .. tip::

            By default it is pretty low(10, 100), but should be in most
            cases enough for an offline signer. If needed raise the values
            but be aware that it will increase the search time of addresses
            and outputs in methods like :py:meth:`.wallet.Wallet.hasAddress`.

        :param int accountDepth: The maximum account depth to set.
        :param int indexDepth: The maximum index depth to set.
        """
        assert isinstance(accountDepth, int), "Account depth must be an integer."
        assert accountDepth >= 0, "Account depth must be a non-negative integer."
        assert isinstance(indexDepth, int), "Index depth must be an integer."
        assert indexDepth >= 0, "Index depth must be a non-negative integer."
        ots_set_max_depth(accountDepth, indexDepth)

    @staticmethod
    def resetMaxDepth() -> None:
        """
        Resets the maximum account and index depth to their default values.

        .. note::

            This default values are declared in the OTS C++ library
            in the file `ots.hpp` as `DEFAULT_MAX_ACCOUNT_DEPTH`
            and `DEFAULT_MAX_INDEX_DEPTH`, which by time of writing
            are 10 and 100 respectively.
        """
        ots_reset_max_depth()

    @staticmethod
    def maxAccountDepth(default: int = 0) -> int:
        """
        Returns the maximum account depth for OTS operations.

        :param int default: The default value to return if not set.
                            set to 0 to get the DEFAULT_MAX_ACCOUNT_DEPTH
                            if not set.
        :return: The maximum account depth or the default value.
        """
        return ots_get_max_account_depth(default)

    @staticmethod
    def maxIndexDepth(default: int = 0) -> int:
        """
        Returns the maximum index depth for OTS operations.

        :param int default: The default value to return if not set.
                            set to 0 to get the DEFAULT_MAX_INDEX_DEPTH
                            if not set.
        :return: The maximum index depth or the default value.
        """
        return ots_get_max_index_depth(default)

    @staticmethod
    def verifyData(
        data: bytes | str,
        address: Address | str,
        signature: str | bytes,
    ) -> bool:
        """
        Verifies the data signature against the public key.

        :param data: The data to verify.
        :type data: bytes | str
        :param address: The public key address to verify against.
        :type address: Address | str
        :param signature: The signature to verify.
        :type signature: str | bytes
        :return: True if the signature is valid, False otherwise.
        """
        assert isinstance(data, (bytes, str)), "Data must be a byte string or a string."
        assert isinstance(signature, (bytes, str)), "Signature must be a byte string or a string."
        assert isinstance(address, (Address, str)), "Address must be an instance of Address or a string."
        if isinstance(address, Address):
            address = str(address)
        result: ots_result_t = ots_verify_data(data, address, signature)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)
