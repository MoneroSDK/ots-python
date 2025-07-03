from .raw import *
from .exceptions import OtsException


class WipeableString:
    """
    A class for a wipeable string that can be securely erased from memory.
    """

    def __init__(self, handle: ots_handle_t):
        """
        Initializes a WipeableString instance with a given handle.
        :param ots_handle_t handle: The handle to the wipeable string. It must be of type HandleType.WIPEABLE_STRING.
        """
        assert isinstance(handle, ots_handle_t), "handle must be an instance of ots_handle_t"
        assert handle.type == HandleType.WIPEABLE_STRING, "handle must be of type WipeableString"
        self.handle: ots_handle_t = handle

    def __str__(self) -> str:
        """
        .. attention::

            This method is intentionally not implemented.


        .. seealso:: use :py:meth:`insecure` to get the string in an insecure way.

        :raises Exception: Raises an exception if the string is attempted to be converted to a regular string.
        """
        raise Exception('WipeableString cannot be converted to string directly. Use insecure() method instead.')

    def __repr__(self) -> str:
        """
        :meta private:
        """
        return f"<WipeableString {self.__hash__()}>"

    def __hash__(self):
        """
        :meta private:
        """
        return hash(self.handle)

    def __eq__(self, other):
        """
        Compares two WipeableString instances for equality.

        :param other: The other WipeableString instance or a string to compare with.
        :type other: WipeableString | str
        :return: True if the strings are equal, False otherwise.
        """
        if isinstance(other, str):
            other = WipeableString.fromString(other)
        if not isinstance(other, WipeableString):
            raise NotImplementedError("Comparison is only supported between WipeableString instances or a string.")
        result = ots_wipeable_string_compare(self.handle, other.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_is_equal(result)

    def insecure(self) -> str:
        """
        Returns the string in an insecure way, allowing it to be read as a normal string.
        This method should be used with caution, as it does not guarantee that the string will be wiped from memory.

        :return: The string contained in the WipeableString.
        """
        return ots_wipeable_string_c_str(self.handle)

    @classmethod
    def fromString(cls, string: str) -> 'WipeableString':
        """
        Creates a WipeableString from a regular string.

        :param str string: The string to create the WipeableString from.
        :return: A WipeableString instance containing the provided string.
        """
        result: ots_result_t = ots_wipeable_string_create(string)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))
