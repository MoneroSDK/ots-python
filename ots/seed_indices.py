from .raw import *
from .enums import HandleType
from .exceptions import OtsException


class SeedIndices:
    """
    SeedIndices class represents a collection of seed indices of the seed phrase.
    Each seed index is an integer that corresponds to a word in the seed phrase.
    """

    def __init__(self, handle: ots_handle_t):
        """
        Initializes the SeedIndices object with a handle.

        :param ots_handle_t handle: The handle to the seed indices.
        :meta private:
        """
        assert isinstance(handle, ots_handle_t), "handle must be of type ots_handle_t"
        assert handle.type == HandleType.SEED_INDICES, "handle must be of type SEED_INDICES"
        self.handle: ots_handle_t = handle

    def __len__(self) -> int:
        """
        :return: The number of seed indices.
        """
        return self.count

    def __add__(self, other: 'SeedIndices | str') -> 'SeedIndices':
        """
        Combine two SeedIndices objects or the SeedIndice with a password string.

        :param other: Another SeedIndices object or a string (password).
        :type other: SeedIndices | str
        :return: A new SeedIndices object containing the combined values.
        """
        if not isinstance(other, (SeedIndices, str)):
            raise NotImplementedError("Can only add another SeedIndices object or a string.")
        if isinstance(other, str):
            result: ots_result_t = ots_seed_indices_merge_with_password(self.handle, other)
            if ots_is_error(result):
                raise OtsException.from_result(result)
            return SeedIndices(ots_result_handle(result))
        result: ots_result_t = ots_seed_indices_merge_values(self.handle, other.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return SeedIndices(ots_result_handle(result))

    def __sub__(self, other: 'SeedIndices | str') -> 'SeedIndices':
        """
        How the operation is essentially XOR it's the same as addition.

        :param other: Another SeedIndices object.
        :type other: SeedIndices | str
        :return: A new SeedIndices object containing the combined values.
        """
        return self.__add__(other)

    @property
    def values(self) -> list[int]:
        """
        :return: A list of integers representing the seed indices.
        """
        return ots_seed_indices_values(self.handle)

    @property
    def count(self) -> int:
        """
        :return: The number of seed indices.
        """
        result: ots_result_t = ots_seed_indices_count(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_uint32(result)

    def clear(self) -> None:
        """
        Clear the seed indices.
        """
        result: ots_result_t = ots_seed_indices_clear(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)

    def append(self, value: int) -> None:
        """
        Append a seed index to the list.

        :param int value: The seed index to append.
        """
        assert isinstance(value, int), "value must be an integer"
        result: ots_result_t = ots_seed_indices_append(self.handle, value)
        if ots_is_error(result):
            raise OtsException.from_result(result)

    def numeric(self, separator: str = '') -> str:
        """
        Get the seed indices as a numeric string with a given separator.

        :param str separator: The separator to use between indices. (default: '')
        :return: A numeric string representation of the seed indices.
        """
        assert isinstance(separator, str), "separator must be of type str"
        result: ots_result_t = ots_seed_indices_numeric(self.handle, separator)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    def hex(self, separator: str = '') -> str:
        """
        Get the seed indices as a hex string with a given separator.

        :param str separator: The separator to use between indices. (default: '')
        :return: A hex string representation of the seed indices.
        """
        assert isinstance(separator, str), "separator must be of type str"
        result: ots_result_t = ots_seed_indices_hex(self.handle, separator)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @classmethod
    def fromValues(cls, values: list[int]) -> 'SeedIndices':
        """
        Create a SeedIndices object from a list of integers.

        :param list[int] values: A list of integers representing the seed indices.
        :return: A SeedIndices object containing the provided values.
        """
        assert isinstance(values, list), "values must be a list of integers"
        assert all(isinstance(v, int) for v in values), "all values must be integers"
        result: ots_result_t = ots_seed_indices_create(values)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def fromString(cls, string: str, separator: str = '') -> 'SeedIndices':
        """
        Create a SeedIndices object from a string of integers separated by a given separator.

        :param str string: A string of integers representing the seed indices.
        :param str separator: The separator used in the string (default: '').
        :return: A SeedIndices object containing the provided values.
        """
        assert isinstance(string, str), "string must be of type str"
        assert isinstance(separator, str), "separator must be of type str"
        result: ots_result_t = ots_seed_indices_create_from_string(string, separator)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def fromHexString(cls, string: str, separator: str = '') -> 'SeedIndices':
        """
        Create a SeedIndices object from a hex string of integers separated by a given separator.

        :param str string: A hex string of integers representing the seed indices.
        :param str separator: The separator used in the string (default: '').
        :return: A SeedIndices object containing the provided values.
        """
        assert isinstance(string, str), "string must be of type str"
        assert isinstance(separator, str), "separator must be of type str"
        result: ots_result_t = ots_seed_indices_create_from_hex(string, separator)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))
