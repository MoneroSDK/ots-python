from .raw import ffi, lib, ots_result_t, _CDataBase, _unwrap


class OtsException(Exception):
    """
    Wraps the OTS error into an Exception with a message.
    """
    # TODO: maybe it would be better to auto generate for all errors exception classes, check

    def __init__(self, error):
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
        return self.message()

    def __int__(self):
        """
        :return: Integer value of the error code.
        """
        return self.code()

    def code(self) -> int:
        """
        :return: The code of the error.
        """
        return lib.ots_error_code(self.ptr)

    def error_class(self) -> str:
        """
        :return: The class of the error.
        """
        return ffi.string(self.ptr.cls).decode('utf-8')

    def message(self) -> str:
        """
        :return: The message of the error.
        """
        return ffi.string(self.ptr.message).decode('utf-8')

    @staticmethod
    def from_result(result: ots_result_t | _CDataBase) -> 'OtsException':
        """
        Creates an OtsException from a result object.
        """
        assert isinstance(result, (ots_result_t, _CDataBase)), "result must be an instance of ots_result_t or _CDataBase"
        assert ffi.typeof(_unwrap(result)) == ffi.typeof('ots_result_t*'), "result must be of type ots_result_t *"
        return OtsException(_unwrap(result).error)
