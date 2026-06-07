from .raw import ffi, lib, _CDataBase


class OtsException(Exception):
    """
    Wraps the OTS error into an Exception with a message.
    """

    def __init__(self, error: _CDataBase):
        """
        Initializes the OtsException with an error struct, from the
        C ABI ots_result_t struct.
        :param error: The error struct from the ots_result_t.error
        :type error: ots_error_t.error
        """
        self.ptr = error

    def __str__(self):
        """
        :return: String representation of the error.
        """
        return self.message

    def __int__(self):
        """
        :return: Integer value of the error code.
        """
        return self.code

    @property
    def code(self) -> int:
        """
        :return: The code of the error.
        """
        return self.ptr.code

    @property
    def error_class(self) -> str:
        """
        :return: The class of the error.
        """
        return ffi.string(self.ptr.cls).decode('utf-8')

    @property
    def message(self) -> str:
        """
        :return: The message of the error.
        """
        return ffi.string(self.ptr.message).decode('utf-8')
