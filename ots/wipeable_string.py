from .raw import *
from .exceptions import OtsException


class WipeableString:
    """
    A class for a wipeable string that can be securely erased from memory.
    """

    def __init__(self, handle: ots_handle_t):
        assert isinstance(handle, ots_handle_t), "handle must be an instance of ots_handle_t"
        assert handle.type == HandleType.WIPEABLE_STRING, "handle must be of type WipeableString"
        self.handle: ots_handle_t = handle

    def __str__(self):
        raise Exception('WipeableString cannot be converted to string directly. Use insecure() method instead.')

    def __repr__(self):
        return f"<WipeableString {self.__hash__()}>"

    def __hash__(self):
        """
        Returns the hash of the WipeableString instance.
        """
        return hash(self.handle)

    def __eq__(self, other):
        """
        Compares two WipeableString instances for equality.
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
        """
        return ots_wipeable_string_c_str(self.handle)

    @classmethod
    def fromString(cls, string: str) -> 'WipeableString':
        """
        Creates a WipeableString from a regular string.
        """
        result: ots_result_t = ots_wipeable_string_create(string)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))
