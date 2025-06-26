from _cffi_backend import _CDataBase
from ._ots import ffi, lib
from .enums import *

REQUIRE__OTS_RESULT_T__OR__CDATA_BASE = "result must be a valid ots_result_t or _CDataBase object"
REQUIRE__OTS_HANDLE_T__OR__CDATA_BASE = "handle must be a valid ots_handle_t or _CDataBase object"


class _opaque_handle_t:

    @property
    def ptr(self) -> _CDataBase:
        """
        Returns the pointer to the underlying C data type.
        """
        return self.ptrptr[0]

    @property
    def type(self) -> str:
        """
        Returns the type of the handle as a string.
        """
        return ffi.typeof(self.ptrptr[0]).cname

class ots_result_t(_opaque_handle_t):
    """
    Represents the result of an OTS operation.
    """

    def __init__(self, result: _CDataBase):
        self.ptrptr = ffi.new('ots_result_t **')
        self.ptrptr[0] = result

    def __del__(self):
        """
        Frees the underlying C data type when the object is deleted.
        """
        if self.ptrptr:
            lib.ots_free_result(self.ptrptr)
            ffi.release(self.ptrptr)


class ots_handle_t(_opaque_handle_t):
    """
    Represents a handle to an OTS object.
    """

    def __init__(self, handle: _CDataBase, reference: bool = False):
        self.ptrptr = ffi.new('ots_handle_t **')
        self.ptrptr[0] = handle
        self.reference = reference

    def __del__(self):
        """
        Frees the underlying C data type when the object is deleted.
        """
        if self.ptrptr:
            if not self.reference:
                lib.ots_free_handle(self.ptrptr)
            ffi.release(self.ptrptr)

class ots_tx_description_t(_opaque_handle_t):
    """
    Represents a transaction description in OTS.
    """

    def __init__(self, description: _CDataBase):
        self.ptrptr = ffi.new('ots_tx_description_t **')
        self.ptrptr[0] = description

    def __del__(self):
        """
        Frees the underlying C data type when the object is deleted.
        """
        if self.ptrptr:
            lib.ots_free_tx_description(self.ptrptr)
            ffi.release(self.ptrptr)


def _unwrap(
    value:
        _CDataBase
        | ots_result_t
        | ots_handle_t
) -> _CDataBase:
    """
    Unwraps the given value to its C data type.

    :param value: The value to unwrap.
    :return: The C data type representation of the value.
    """
    if isinstance(value, _opaque_handle_t):
        return value.ptr
    return value


def _is_handle(handle: ots_handle_t | _CDataBase | None) -> bool:
    if (
        isinstance(handle, ots_handle_t)
        and handle.type == 'ots_handle_t *'
        and handle.ptr != ffi.NULL
    ):
        return True
    if isinstance(handle, _CDataBase):
        return ffi.typeof(handle) == ffi.typeof('ots_handle_t *') and handle != ffi.NULL
    return False


def _is_result(result: ots_result_t | _CDataBase | None) -> bool:
    if isinstance(result, ots_result_t):
        return result.type == 'ots_result_t *' and result.ptr != ffi.NULL
    if isinstance(result, _CDataBase):
        return ffi.typeof(result) == ffi.typeof('ots_result_t *') and result != ffi.NULL
    return False


def _raise_on_error(result: ots_result_t | _CDataBase) -> None:
    """
    Raises an exception if the result indicates an error.

    :param result: The result to check for errors.
    :raises Exception: If the result is an error.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    if ots_is_error(result):
        message = ots_error_message(result)
        error_class = ots_error_class(result)
        error_code = ots_error_code(result)
        raise Exception(f"OTS Error: {message} (Class: {error_class}, Code: {error_code})")


def ots_handle_valid(
    handle: ots_handle_t | _CDataBase,
    handle_type: HandleType | int
) -> bool:
    """
    Checks if the given handle is valid.

    :param handle: The handle to check.
    :param handle_type: The expected type of the handle.
    :return: True if the handle is valid, False otherwise.
    """
    assert isinstance(handle_type, HandleType) or isinstance(handle_type, int), "handle_type must be an instance of HandleType or an integer"
    assert _is_handle(handle), REQUIRE__OTS_HANDLE_T__OR__CDATA_BASE
    return lib.ots_handle_valid(ffi.cast('ots_handle_t*', _unwrap(handle)), int(handle_type))


def ots_is_error(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result indicates an error.

    :param result: The result to check.
    :return: True if the result is an error, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_is_error(_unwrap(result))


def ots_error_message(result: ots_result_t | _CDataBase) -> str | None:
    """
    Returns the error message from the result.

    :param result: The result to check.
    :return: The error message as a string, or None if there is no error.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    out = lib.ots_result_string(_unwrap(result))
    return ffi.string(out).decode('utf-8') if out != ffi.NULL else None

def ots_error_class(result: ots_result_t | _CDataBase) -> str | None:
    """
    Returns the error class from the result.

    :param result: The result to check.
    :return: The error class as a string, or None if there is no error.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    out = lib.ots_error_class(_unwrap(result))
    return ffi.string(out).decode('utf-8') if out != ffi.NULL else None


def ots_error_code(result: ots_result_t | _CDataBase) -> int:
    """
    Returns the error code from the result.

    :param result: The result to check.
    :return: The error code as an integer, or 0 if there is no error.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_error_code(_unwrap(result))


def ots_is_result(result: ots_result_t | _CDataBase | None) -> bool:
    """
    Checks if the given result is a valid result object.

    :param result: The result to check.
    :return: True if the result is valid, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_is_result(_unwrap(result))

def ots_result_is_type(
    result: ots_result_t | _CDataBase,
    result_type: ResultType | int
) -> bool:
    """
    Checks if the result is of a specific type.

    :param result: The result to check.
    :param result_type: The expected type of the result.
    :return: True if the result is of the specified type, False otherwise.
    """
    assert isinstance(result_type, ResultType) or isinstance(result_type, int), "result_type must be an instance of ResultType or an integer"
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_type(_unwrap(result), int(result_type))


def ots_result_is_handle(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a handle.

    :param result: The result to check.
    :return: True if the result is a handle, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return ots_result_is_handle(_unwrap(result))


def ots_result_is_wipeable_string(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a wipeable string.

    :param result: The result to check.
    :return: True if the result is a wipeable string, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return ots_result_is_wipeable_string(_unwrap(result))


def ots_result_is_seed_indices(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a seed indices.

    :param result: The result to check.
    :return: True if the result is a seed indices, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return ots_result_is_seed_indices(ffi.cast('ots_result_t*', _unwrap(result)))


def ots_result_is_seed_language(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a seed language.

    :param result: The result to check.
    :return: True if the result is a seed language, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return ots_result_is_seed_language(_unwrap(result))


def ots_result_is_address(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is an address.

    :param result: The result to check.
    :return: True if the result is an address, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return ots_result_is_address(ffi.cast('ots_result_t*', _unwrap(result)))


def ots_result_is_seed(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a seed.

    :param result: The result to check.
    :return: True if the result is a seed, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return ots_result_is_seed(_unwrap(result))


def ots_result_is_wallet(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a wallet.

    :param result: The result to check.
    :return: True if the result is a wallet, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return ots_result_is_wallet(_unwrap(result))


def ots_result_is_transaction(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a transaction.

    :param result: The result to check.
    :return: True if the result is a transaction, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return ots_result_is_transaction(_unwrap(result))


def ots_result_is_transaction_description(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a transaction description.

    :param result: The result to check.
    :return: True if the result is a transaction description, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return ots_result_is_transaction_description(_unwrap(result))


def ots_result_is_transaction_warning(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a transaction warning.

    :param result: The result to check.
    :return: True if the result is a transaction warning, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return ots_result_is_transaction_warning(_unwrap(result))


def ots_result_is_string(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a string.

    :param result: The result to check.
    :return: True if the result is a string, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_string(_unwrap(result))


def ots_result_is_boolean(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a boolean.

    :param result: The result to check.
    :return: True if the result is a boolean, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_boolean(_unwrap(result))


def ots_result_is_number(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a number.

    :param result: The result to check.
    :return: True if the result is a number, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_number(_unwrap(result))


def ots_result_data_is_type(
    result: ots_result_t | _CDataBase,
    data_type: DataType | int
) -> bool:
    """
    Checks if the result data is of a specific type.

    :param result: The result to check.
    :param data_type: The expected type of the result data.
    :return: True if the result data is of the specified type, False otherwise.
    """
    assert isinstance(data_type, DataType) or isinstance(data_type, int), "data_type must be an instance of DataType or an integer"
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_type(_unwrap(result), int(data_type))


def ots_result_data_is_reference(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is a reference.

    :param result: The result to check.
    :return: True if the result data is a reference, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_reference(_unwrap(result))


def ots_result_data_is_int(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is an integer.

    :param result: The result to check.
    :return: True if the result data is an integer, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_int(_unwrap(result))


def ots_result_data_is_char(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is a character.

    :param result: The result to check.
    :return: True if the result data is a character, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_char(_unwrap(result))


def ots_result_data_is_uint8(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is an unsigned 8-bit integer.

    :param result: The result to check.
    :return: True if the result data is an unsigned 8-bit integer, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_uint8(_unwrap(result))


def ots_result_data_is_uint16(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is an unsigned 16-bit integer.

    :param result: The result to check.
    :return: True if the result data is an unsigned 16-bit integer, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_uint16(_unwrap(result))


def ots_result_data_is_uint32(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is an unsigned 32-bit integer.

    :param result: The result to check.
    :return: True if the result data is an unsigned 32-bit integer, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_uint32(_unwrap(result))


def ots_result_data_is_uint64(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is an unsigned 64-bit integer.

    :param result: The result to check.
    :return: True if the result data is an unsigned 64-bit integer, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_uint64(_unwrap(result))


def ots_result_data_is_handle(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is a handle.

    :param result: The result to check.
    :return: True if the result data is a handle, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_handle(_unwrap(result))


def ots_result_data_handle_is_type(
    result: ots_result_t | _CDataBase,
    handle_type: int
) -> bool:
    """
    Checks if the result data handle is of a specific type.

    :param result: The result to check.
    :param type: The expected type of the handle.
    :return: True if the handle is of the specified type, False otherwise.
    """
    assert isinstance(handle_type, HandleType) or isinstance(handle_type, int), "handle_type must be an instance of HandleType or an integer"
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_type(_unwrap(handle_type))


def ots_result_data_handle_is_reference(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is a reference.

    :param result: The result to check.
    :return: True if the handle is a reference, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_reference(_unwrap(result))


def ots_result_data_handle_is_wipeable_string(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is a wipeable string.

    :param result: The result to check.
    :return: True if the handle is a wipeable string, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_wipeable_string(_unwrap(result))


def ots_result_data_handle_is_seed_indices(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is seed indices.

    :param result: The result to check.
    :return: True if the handle is seed indices, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_seed_indices(_unwrap(result))


def ots_result_data_handle_is_seed_language(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is a seed language.

    :param result: The result to check.
    :return: True if the handle is a seed language, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_seed_language(_unwrap(result))


def ots_result_data_handle_is_address(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is an address.

    :param result: The result to check.
    :return: True if the handle is an address, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_address(_unwrap(result))


def ots_result_data_handle_is_seed(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is a seed.

    :param result: The result to check.
    :return: True if the handle is a seed, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_seed(_unwrap(result))


def ots_result_data_handle_is_wallet(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is a wallet.

    :param result: The result to check.
    :return: True if the handle is a wallet, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_wallet(_unwrap(result))


def ots_result_data_handle_is_transaction(
    result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data handle is a transaction.

    :param result: The result to check.
    :return: True if the handle is a transaction, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_transaction(_unwrap(result))


def ots_result_data_handle_is_transaction_description(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is a transaction description.

    :param result: The result to check.
    :return: True if the handle is a transaction description, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_transaction_description(_unwrap(result))


def ots_result_data_handle_is_transaction_warning(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is a transaction warning.

    :param result: The result to check.
    :return: True if the handle is a transaction warning, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_transaction_warning(_unwrap(result))


def ots_result_handle(result: ots_result_t | _CDataBase) -> ots_handle_t:
    """
    Returns the handle from the result.

    :param result: The result to get the handle from.
    :return: An ots_handle_t object containing the handle, or None if there is no handle.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return ots_handle_t(lib.ots_result_handle(_unwrap(result)), ots_result_handle_is_reference(result))


def ots_result_handle_is_type(
    result: ots_result_t | _CDataBase,
    type: HandleType | int
) -> bool:
    """
    Checks if the result handle is of a specific type.

    :param result: The result to check.
    :param type: The expected type of the handle.
    :return: True if the handle is of the specified type, False otherwise.
    """
    assert isinstance(type, HandleType) or isinstance(type, int), "type must be an instance of HandleType or an integer"
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_handle_is_type(_unwrap(result), int(type))


def ots_result_handle_is_reference(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result handle is a reference.

    :param result: The result to check.
    :return: True if the handle is a reference, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_handle_is_reference(_unwrap(result))


def ots_result_string(result: ots_result_t | _CDataBase) -> str | None:
    """
    Returns the string from the result.

    :param result: The result to get the string from.
    :return: The string as a UTF-8 encoded string, or None if there is no string.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    out = lib.ots_result_string(_unwrap(result))
    return ffi.string(out).decode('utf-8') if out != ffi.NULL else None


def ots_result_string_copy(
    result: ots_result_t | _CDataBase
) -> str | None:
    """
    Returns a copy of the string from the result.
    (In Python this is the same result as ots_result_string)

    :param result: The result to get the string from.
    :return: A copy of the string as a UTF-8 encoded string, or None if there is no string.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    out = lib.ots_result_string_copy(_unwrap(result))
    return ffi.string(out).decode('utf-8') if out != ffi.NULL else None


def ots_result_boolean(
    result: ots_result_t | _CDataBase,
    default_value: bool = False
) -> bool:
    """
    Returns the boolean value from the result.

    :param result: The result to get the boolean from.
    :param default_value: The default value to return if the result is not a boolean.
    :return: The boolean value, or the default value if the result is not a boolean.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_boolean(_unwrap(result), default_value)


def ots_result_number(
    result: ots_result_t | _CDataBase,
    default_value: int = -1
) -> int:
    """
    Returns the number from the result.

    :param result: The result to get the number from.
    :param default_value: The default value to return if the result is not a number.
    :return: The number as an integer, or the default value if the result is not a number.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_number(_unwrap(result), default_value)


def ots_result_array(
    result: ots_result_t | _CDataBase
) -> _CDataBase:
    """
    Returns the array from the result.
    :param result: The result to get the array from.
    :return: _CDataBase objects representing the array elements.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    return lib.ots_result_array(_unwrap(result))


def ots_result_array_get(
    result: ots_result_t | _CDataBase,
    index: int
) -> _CDataBase:
    """
    Returns the element at the specified index from the result array.

    :param result: The result to get the element from.
    :param index: The index of the element to retrieve.
    :return: The element at the specified index, or None if the index is out of bounds.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_size(result) > index >= 0, "index out of bounds"
    return lib.ots_result_array_get(_unwrap(result), index)


def ots_result_array_get_handle(
    result: ots_result_t | _CDataBase,
    index: int
) -> ots_handle_t:
    """
    Returns the handle at the specified index from the result array.

    :param result: The result to get the handle from.
    :param index: The index of the handle to retrieve.
    :return: An ots_handle_t object containing the handle at the specified index, or None if the index is out of bounds.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_size(result) > index >= 0, "index out of bounds"
    assert ots_result_data_is_handle(result), "result array must be of handle type"
    return ots_handle_t(lib.ots_result_array_get_handle(_unwrap(result), index))


def ots_result_array_get_int(
    result: ots_result_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the integer at the specified index from the result array.

    :param result: The result to get the integer from.
    :param index: The index of the integer to retrieve.
    :return: The integer at the specified index, or None if the index is out of bounds.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_size(result) > index >= 0, "index out of bounds"
    assert ots_result_data_is_int(result), "result array must be of int type"
    return lib.ots_result_array_get_int(_unwrap(result), index)


def ots_result_array_get_char(
    result: ots_result_t | _CDataBase,
    index: int
) -> bytes:
    """
    Returns the character at the specified index from the result array.

    :param result: The result to get the character from.
    :param index: The index of the character to retrieve.
    :return: The character at the specified index, or None if the index is out of bounds.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_size(result) > index >= 0, "index out of bounds"
    assert ots_result_data_is_char(result), "result array must be of char type"
    return ffi.string(lib.ots_result_array_get_char(_unwrap(result), index))


def ots_result_array_get_uint8(
    result: ots_result_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the unsigned 8-bit integer at the specified index from the result array.

    :param result: The result to get the unsigned 8-bit integer from.
    :param index: The index of the unsigned 8-bit integer to retrieve.
    :return: The unsigned 8-bit integer at the specified index, or None if the index is out of bounds.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_size(result) > index >= 0, "index out of bounds"
    assert ots_result_data_is_uint8(result), "result array must be of uint8 type"
    return lib.ots_result_array_get_uint8(_unwrap(result), index)


def ots_result_array_get_uint16(
    result: ots_result_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the unsigned 16-bit integer at the specified index from the result array.
    :param result: The result to get the unsigned 16-bit integer from.
    :param index: The index of the unsigned 16-bit integer to retrieve.
    :return: The unsigned 16-bit integer at the specified index
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_size(result) > index >= 0, "index out of bounds"
    assert ots_result_data_is_uint16(result), "result array must be of uint16 type"
    return lib.ots_result_array_get_uint16(_unwrap(result), index)


def ots_result_array_get_uint32(
    result: ots_result_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the unsigned 32-bit integer at the specified index from the result array.
    :param result: The result to get the unsigned 32-bit integer from.
    :param index: The index of the unsigned 32-bit integer to retrieve.
    :return: The unsigned 32-bit integer at the specified index
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_size(result) > index >= 0, "index out of bounds"
    assert ots_result_data_is_uint32(result), "result array must be of uint32 type"
    return lib.ots_result_array_get_uint32(_unwrap(result), index)


def ots_result_array_get_uint64(result: _CDataBase|None, index: int) -> int:
    """
    Returns the unsigned 64-bit integer at the specified index from the result array.
    :param result: The result to get the unsigned 64-bit integer from.
    :param index: The index of the unsigned 64-bit integer to retrieve.
    :return: The unsigned 64-bit integer at the specified index
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_size(result) > index >= 0, "index out of bounds"
    assert ots_result_data_is_uint64(result), "result array must be of uint64 type"
    return lib.ots_result_array_get_uint64(_unwrap(result), index)


def ots_result_array_reference(
    result: ots_result_t | _CDataBase
) -> _CDataBase:
    """
    Returns a reference to the array from the result.

    :param result: The result to get the array reference from.
    :return: A _CDataBase object representing the array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    return lib.ots_result_array_reference(_unwrap(result))


def ots_result_handle_array_reference(
    result: ots_result_t | _CDataBase
) -> list[ots_handle_t]:
    """
    Returns a reference to the array of handles from the result.

    :param result: The result to get the handle array reference from.
    :return: A list of ots_handle_t objects representing the handle array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_handle(result), "result array must be of handle type"
    handle = lib.ots_result_handle_array_reference(_unwrap(result))
    return [ots_handle_t(handle + i, True) for i in range(ots_result_size(result))]


def ots_result_int_array_reference(
    result: ots_result_t | _CDataBase
) -> list[int]:
    """
    Returns a reference to the array of integers from the result.
    :param result: The result to get the integer array reference from.
    :return: A list of integers representing the integer array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_int(result), "result array must be of handle type"
    handle = lib.ots_result_handle_array_reference(_unwrap(result))
    return [ffi.cast('int', handle[i]) for i in range(ots_result_size(result))]


def ots_result_char_array_reference(result: _CDataBase|None) -> bytes:
    """
    Returns a reference to the array of characters from the result.
    :param result: The result to get the character array reference from.
    :return: bytes representing the character array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_char(result) or ots_result_data_is_uint8(result), "result array must be of char or uint8 type"
    return ffi.string(lib.ots_result_uint8_array_reference(_unwrap(result)), ots_result_size(result))


def ots_result_uint8_array_reference(
    result: ots_result_t | _CDataBase
) -> list[int]:
    """
    Returns a reference to the array of unsigned 8-bit integers from the result.

    :param result: The result to get the unsigned 8-bit integer array reference from.
    :return: A list of unsigned 8-bit integers representing the unsigned 8-bit integer array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint8(result), "result array must be of uint8 type"
    handle = lib.ots_result_uint8_array_reference(_unwrap(result))
    return [int(ffi.cast('uint8_t', handle[i])) for i in range(ots_result_size(result))]


def ots_result_uint16_array_reference(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a reference to the array of unsigned 16-bit integers from the result.

    :param result: The result to get the unsigned 16-bit integer array reference from.
    :return: A list of unsigned 16-bit integers representing the unsigned 16-bit integer array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint16(result), "result array must be of uint16 type"
    handle = lib.ots_result_uint16_array_reference(_unwrap(result))
    return [int(ffi.cast('uint16_t', handle[i])) for i in range(ots_result_size(result))]


def ots_result_uint32_array_reference(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a reference to the array of unsigned 32-bit integers from the result.

    :param result: The result to get the unsigned 32-bit integer array reference from.
    :return: A list of unsigned 32-bit integers representing the unsigned 32-bit integer array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint32(result), "result array must be of uint32 type"
    handle = lib.ots_result_uint32_array_reference(_unwrap(result))
    return [int(ffi.cast('uint32_t', handle[i])) for i in range(ots_result_size(result))]


def ots_result_uint64_array_reference(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a reference to the array of unsigned 64-bit integers from the result.

    :param result: The result to get the unsigned 64-bit integer array reference from.
    :return: A list of unsigned 64-bit integers representing the unsigned 64-bit integer array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint64(result), "result array must be of uint64 type"
    handle = lib.ots_result_uint64_array_reference(_unwrap(result))
    return [int(ffi.cast('uint64_t', handle[i])) for i in range(ots_result_size(result))]


def ots_result_handle_array(result: ots_result_t | _CDataBase) -> list[_CDataBase]:
    """
    Returns a list of handles from the result array.

    :param result: The result to get the handles from.
    :return: A list of _CDataBase objects representing the handles in the result array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_handle(result), "result array must be of handle type"
    handle = lib.ots_result_handle_array(_unwrap(result))
    return [ots_handle_t(handle + i) for i in range(ots_result_size(result))]


def ots_result_int_array(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a list of integers from the result array.

    :param result: The result to get the integers from.
    :return: A list of integers representing the integers in the result array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_int(result), "result array must be of int type"
    handle = lib.ots_result_int_array(_unwrap(result))
    return [ffi.cast('int', handle[i]) for i in range(ots_result_size(result))]


def ots_result_char_array(result: ots_result_t | _CDataBase) -> bytes:
    """
    Returns a byte string representing the character array from the result.

    :param result: The result to get the character array from.
    :return: A byte string representing the character array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_char(result) or ots_result_data_is_uint8(result), "result array must be of char or uint8 type"
    handle = lib.ots_result_char_array(_unwrap(result))
    return ffi.string(handle, ots_result_size(result))


def ots_result_uint8_array(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a list of unsigned 8-bit integers from the result array.

    :param result: The result to get the unsigned 8-bit integers from.
    :return: A list of unsigned 8-bit integers representing the unsigned 8-bit integers in the result array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint8(result), "result array must be of uint8 type"
    handle = lib.ots_result_uint8_array(_unwrap(result))
    return [int(ffi.cast('uint8_t', handle[i])) for i in range(ots_result_size(result))]


def ots_result_uint16_array(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a list of unsigned 16-bit integers from the result array.

    :param result: The result to get the unsigned 16-bit integers from.
    :return: A list of unsigned 16-bit integers representing the unsigned 16-bit integers in the result array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint16(result), "result array must be of uint16 type"
    handle = lib.ots_result_uint16_array(_unwrap(result))
    return [int(ffi.cast('uint16_t', handle[i])) for i in range(ots_result_size(result))]


def ots_result_uint32_array(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a list of unsigned 32-bit integers from the result array.

    :param result: The result to get the unsigned 32-bit integers from.
    :return: A list of unsigned 32-bit integers representing the unsigned 32-bit integers in the result array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint32(result), "result array must be of uint32 type"
    handle = lib.ots_result_uint32_array(_unwrap(result))
    return [int(ffi.cast('uint32_t', handle[i])) for i in range(ots_result_size(result))]


def ots_result_uint64_array(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a list of unsigned 64-bit integers from the result array.

    :param result: The result to get the unsigned 64-bit integers from.
    :return: A list of unsigned 64-bit integers representing the unsigned 64-bit integers in the result array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint64(result), "result array must be of uint64 type"
    handle = lib.ots_result_uint64_array(_unwrap(result))
    return [int(ffi.cast('uint64_t', handle[i])) for i in range(ots_result_size(result))]


def ots_result_is_array(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is an array.

    :param result: The result to check.
    :return: True if the result is an array, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_array(_unwrap(result))


def ots_result_is_comparison(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a comparison result.

    :param result: The result to check.
    :return: True if the result is a comparison result, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_comparison(_unwrap(result))


def ots_result_comparison(result: ots_result_t | _CDataBase) -> int:
    """
    Returns the comparison result.

    :param result: The result to get the comparison from.
    :return: The comparison result as an integer.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_comparison(_unwrap(result))


def ots_result_is_equal(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is equal to another result.

    :param result: The result to check.
    :return: True if the result is equal, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_equal(_unwrap(result))


def ots_result_size(result: ots_result_t | _CDataBase) -> int:
    """
    Returns the size of the result.

    :param result: The result to get the size from.
    :return: The size of the result as an integer.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_size(_unwrap(result))


def ots_result_is_address_type(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is an address type.

    :param result: The result to check.
    :return: True if the result is an address type, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_address_type(_unwrap(result))


def ots_result_address_type_is_type(
    result: ots_result_t | _CDataBase,
    type: AddressType | int
) -> bool:
    """
    Checks if the result address type is of a specific type.

    :param result: The result to check.
    :param type: The expected type of the address.
    :return: True if the address is of the specified type, False otherwise.
    """
    assert isinstance(type, AddressType) or isinstance(type, int), "type must be an instance of AddressType or an integer"
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_address_type_is_type(_unwrap(result), int(type))


def ots_result_is_address_index(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is an address index.

    :param result: The result to check.
    :return: True if the result is an address index, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_address_index(_unwrap(result))


def ots_result_address_index_account(result: ots_result_t | _CDataBase) -> int:
    """
    Returns the account index from the result address index.

    :param result: The result to get the account index from.
    :return: The account index as an integer.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_address_index_account(_unwrap(result))


def ots_result_address_index_index(result: ots_result_t | _CDataBase) -> int:
    """
    Returns the index from the result address index.

    :param result: The result to get the index from.
    :return: The index as an integer.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_address_index_index(_unwrap(result))


def ots_result_is_network(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a network type.

    :param result: The result to check.
    :return: True if the result is a network type, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_network(_unwrap(result))


def ots_result_network(result: ots_result_t | _CDataBase) -> Network:
    """
    Returns the network from the result.

    :param result: The result to get the network from.
    :return: The network as a Network object.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return Network(lib.ots_result_network(_unwrap(result)))


def ots_result_network_is_type(
    result: ots_result_t | _CDataBase,
    network: Network | int
) -> bool:
    """
    Checks if the result network is of a specific type.

    :param result: The result to check.
    :param network: The expected type of the network.
    :return: True if the network is of the specified type, False otherwise.
    """
    assert isinstance(network, Network) or isinstance(network, int), "network must be an instance of Network or an integer"
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_network_is_type(_unwrap(result), int(network))


def ots_result_is_seed_type(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a seed type.

    :param result: The result to check.
    :return: True if the result is a seed type, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_seed_type(_unwrap(result))


def ots_result_seed_type(result: ots_result_t | _CDataBase) -> SeedType:
    """
    Returns the seed type from the result.

    :param result: The result to get the seed type from.
    :return: The seed type as a SeedType object.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return SeedType(lib.ots_result_seed_type(_unwrap(result)))


def ots_result_seed_type_is_type(
    result: ots_result_t | _CDataBase,
    type: SeedType | int
) -> bool:
    """
    Checks if the result seed type is of a specific type.

    :param result: The result to check.
    :param type: The expected type of the seed.
    :return: True if the seed is of the specified type, False otherwise.
    """
    assert isinstance(type, SeedType) or isinstance(type, int), "type must be an instance of OTS_SEED_TYPE or an integer"
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_seed_type_is_type(_unwrap(result), int(type))


def ots_free_string(string: _CDataBase) -> None:
    """
    Frees a string allocated by OTS functions.

    :param str: The null terminated string to free.
    :return: None
    """
    assert isinstance(string, _CDataBase) and ffi.typeof(string) == ffi.typeof('char**'), "string must be a char**"
    lib.ots_free_string(ffi.cast('char**', string))


def ots_free_binary_string(string: _CDataBase, size: int) -> None:
    """
    Frees a binary string allocated by OTS functions.

    :param str: The binary string to free.
    :param size: The size of the binary string.
    :return: None
    """
    assert isinstance(string, _CDataBase) and ffi.typeof(string) == ffi.typeof('char**'), "string must be a char**"
    lib.ots_free_binary_string(ffi.cast('char**', string), size)


def ots_free_array(arr: _CDataBase, elem_size: int, count: int) -> None:
    """
    Frees an array allocated by OTS functions.

    :param arr: The array to free.
    :param elem_size: The size of each element in the array.
    :param count: The number of elements in the array.
    :return: None
    """
    assert isinstance(arr, _CDataBase) and ffi.typeof(arr).cname.endswith('* *'), "arr must be a pointer to a pointer (void**)"
    lib.ots_free_array(ffi.cast('void**', arr), elem_size, count)


def ots_free_result(result: ots_result_t | _CDataBase) -> None:
    """
    Frees the result object returned by OTS functions.
    :param result: The result to free.
    :return: None

    :warning:   Use `del result` instead of this function in Python if
                you are using it on a ots_result_t, to clean up all.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    if isinstance(result, _CDataBase):
        assert ffi.typeof(result) == ffi.typeof('ots_result_t**'), "result must be a ots_result_t**"
        lib.ots_free_result(ffi.cast('ots_result_t**', _wrap(result)))
        return
    del result


def ots_free_handle(handle: ots_handle_t | _CDataBase) -> None:
    """
    Frees the handle object returned by OTS functions.

    :param handle: The handle to free.
    :return: None

    :warning:   Use `del handle` instead of this function in Python if
                you are using it on a ots_handle_t, to clean up all.
    """
    assert isinstance(handle, ots_handle_t) or isinstance(handle, _CDataBase), "handle must be an instance of ots_handle_t or _CDataBase"
    if isinstance(handle, _CDataBase):
        assert ffi.typeof(handle) == ffi.typeof('ots_handle_t**'), "handle must be a ots_handle_t**"
        lib.ots_free_handle(ffi.cast('ots_handle_t**', handle))
        return
    del handle


def ots_free_handle_object(handle: _CDataBase) -> None:
    raise NotImplementedError('Only internal use, do not use this function directly.')


def ots_free_tx_description(tx_description: ots_tx_description_t | _CDataBase) -> None:
    """
    Frees the transaction description object returned by OTS functions.

    :param tx_description: The transaction description to free.
    :return: None
    """
    assert isinstance(tx_description, tx_description_t) or isinstance(tx_description, _CDataBase), "tx_description must be an instance of ots_tx_description_t or _CDataBase"
    if isinstance(tx_description, _CDataBase):
        assert ffi.typeof(tx_description) == ffi.typeof('ots_tx_description_t**'), "tx_description must be a ots_tx_description_t**"
        lib.ots_free_tx_description(tx_description)
        return
    del tx_description


def ots_secure_free(buffer: _CDataBase, size: int) -> None:
    """
    Securely frees a buffer by overwriting its contents before deallocation.

    :param buffer: The buffer to free.
    :param size: The size of the buffer.
    :return: None
    """
    assert isinstance(buffer, _CDataBase) and ffi.typeof(buffer).cname.endswith('* *'), "buffer must be a pointer to a pointer (void**)"
    lib.ots_secure_free(ffi.cast('void**', buffer), size)


def ots_wipeable_string_create(string: str) -> ots_result_t:
    """
    Creates a wipeable string from a regular string.

    :param string: The string to create a wipeable string from.
    :return: ots_result_t containing the created wipeable string.
    """
    assert isinstance(string, str), "string must be a str"
    return ots_result_t(lib.ots_wipeable_string_create(string.encode('utf-8')))


def ots_wipeable_string_compare(
    str1: ots_handle_t | _CDataBase,
    str2: ots_handle_t | _CDataBase
) -> ots_result_t:
    """
    Compares two wipeable strings.

    :param str1: The first string to compare.
    :param str2: The second string to compare.
    :return: ots_result_t indicating the comparison result.
    """
    assert isinstance(str1, (ots_handle_t, _CDataBase)) and HandleType(_wrap(str1).type) == HandleType.WIPEABLE_STRING, "str1 must be an instance of ots_handle_t or _CDataBase and of type HandleType.WIPEABLE_STRING"
    assert isinstance(str2, (ots_handle_t, _CDataBase)) and HandleType(_wrap(str2).type) == HandleType.WIPEABLE_STRING, "str2 must be an instance of ots_handle_t or _CDataBase and of type HandleType.WIPEABLE_STRING"
    return ots_result_t(lib.ots_wipeable_string_compare(_unwrap(str1), _unwrap(str2)))


def ots_wipeable_string_c_str(string: ots_result_t | _CDataBase) -> str:
    """
    Returns the C-style string representation of a wipeable string.

    :param string: The wipeable string to convert.
    :return: The C-style string representation.
    """
    assert isinstance(string, (ots_result_t, _CDataBase)), "string must be an instance of ots_result_t or _CDataBase"
    assert HandleType(_wrap(string).type) == HandleType.WIPEABLE_STRING, "string must be of type HandleType.WIPEABLE_STRING"
    return ffi.string(lib.ots_wipeable_string_c_str(_unwrap(string))).decode('utf-8')


def ots_seed_indices_create(indices: list[int]) -> ots_result_t:
    """
    Creates a seed indices object from a list of integers.

    :param indices: A list of integers representing the seed indices.
    :return: ots_result_t containing the created seed indices object.
    """
    assert isinstance(indices, list) and all(isinstance(i, int) for i in indices), "indices must be a list of integers"
    c_indices = ffi.new('uint16_t[]', indices)
    return ots_result_t(lib.ots_seed_indices_create(c_indices, len(indices)))


def ots_seed_indices_create_from_string(
    string: str,
    separator: str = ''
) -> ots_result_t:
    """
    Creates a seed indices object from a string representation of indices.

    :param string: A string containing the indices separated by the specified separator.
    :param separator: The separator used in the string (default is an empty string).
    :return: ots_result_t containing the created seed indices object.
    """
    assert isinstance(string, str), "string must be a str"
    assert isinstance(separator, str), "separator must be a str"
    return ots_result_t(
        lib.ots_seed_indices_create_from_string(
            string.encode('utf-8'),
            separator.encode('utf-8')
        )
    )


def ots_seed_indices_create_from_hex(
    hex: str,
    separator: str = ''
) -> ots_result_t:
    """
    Creates a seed indices object from a hexadecimal string representation of indices.

    :param hex: A hexadecimal string containing the indices separated by the specified separator.
    :param separator: The separator used in the string (default is a comma).
    :return: ots_result_t containing the created seed indices object.
    """
    assert isinstance(hex, str), "hex must be a str"
    assert isinstance(separator, str), "separator must be a str"
    return ots_result_t(
        lib.ots_seed_indices_create_from_hex(
            hex.encode('utf-8'),
            separator.encode('utf-8')
        )
    )


def ots_seed_indices_values(handle: ots_handle_t | _CDataBase) -> list[int]:
    """
    Returns the values of the seed indices as a list of integers.

    :param handle: The handle containing the seed indices.
    :return: A list of integers representing the seed indices.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED_INDICES, "handle must be of type HandleType.SEED_INDICES"
    values = lib.ots_seed_indices_values(_unwrap(handle))
    count = lib.ots_seed_indices_count(_unwrap(handle))
    return [int(values[i]) for i in range(count)]


def ots_seed_indices_count(handle: ots_handle_t | _CDataBase) -> int:
    """
    Returns the count of seed indices in the handle.

    :param handle: The handle containing the seed indices.
    :return: The count of seed indices as an integer.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED_INDICES, "handle must be of type HandleType.SEED_INDICES"
    return lib.ots_seed_indices_count(_unwrap(handle))


def ots_seed_indices_clear(handle: ots_handle_t | _CDataBase) -> None:
    """
    Clears the seed indices in the handle.

    :param handle: The handle containing the seed indices to clear.
    :return: None
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED_INDICES, "handle must be of type HandleType.SEED_INDICES"
    lib.ots_seed_indices_clear(_unwrap(handle))


def ots_seed_indices_append(
    handle: ots_handle_t | _CDataBase,
    value: int
) -> None:
    """
    Appends a value to the seed indices in the handle.

    :param handle: The handle containing the seed indices.
    :param value: The value to append to the seed indices.
    :return: None
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED_INDICES, "handle must be of type HandleType.SEED_INDICES"
    assert isinstance(value, int), "value must be an integer"
    lib.ots_seed_indices_append(_unwrap(handle), value)


def ots_seed_indices_numeric(
    handle: ots_handle_t | _CDataBase,
    separator: str = ''
) -> str:
    """
    Returns a string representation of the seed indices in numeric format.

    :param handle: The handle containing the seed indices.
    :param separator: The separator to use between indices (default is an empty string).
    :return: A string representing the seed indices in numeric format.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED_INDICES, "handle must be of type HandleType.SEED_INDICES"
    return ffi.string(lib.ots_seed_indices_numeric(_unwrap(handle), separator.encode('utf-8'))).decode('utf-8')


def ots_seed_indices_hex(
    handle: ots_handle_t | _CDataBase,
    separator: str = ''
) -> str:
    """
    Returns a string representation of the seed indices in hexadecimal format.

    :param handle: The handle containing the seed indices.
    :param separator: The separator to use between indices (default is a comma).
    :return: A string representing the seed indices in hexadecimal format.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED_INDICES, "handle must be of type HandleType.SEED_INDICES"
    return ffi.string(lib.ots_seed_indices_hex(_unwrap(handle), separator.encode('utf-8'))).decode('utf-8')


def ots_seed_languages() -> ots_result_t:
    """
    Returns a list of all available seed languages.

    :return: ots_result_t containing the list of seed languages.
    """
    return ots_result_t(lib.ots_seed_languages())


def ots_seed_languages_for_type(type: SeedType | int) -> ots_result_t:
    """
    Returns a list of seed languages for a specific seed type.

    :param type: The seed type for which to get the languages.
    :return: ots_result_t containing the list of seed languages for the specified type.
    """
    assert isinstance(type, SeedType) or isinstance(type, int), "type must be an instance of SeedType or an integer"
    return ots_result_t(lib.ots_seed_languages_for_type(int(type)))


def ots_seed_language_default(type: SeedType | int) -> ots_result_t:
    """
    Returns the default seed language for a specific seed type.

    :param type: The seed type for which to get the default language.
    :return: ots_result_t containing the default seed language for the specified type.
    """
    assert isinstance(type, SeedType) or isinstance(type, int), "type must be an instance of SeedType or an integer"
    return ots_result_t(lib.ots_seed_language_default(int(type)))


def ots_seed_language_set_default(
    type: SeedType | int,
    language: ots_handle_t | _CDataBase
) -> ots_result_t:
    """
    Sets the default seed language for a specific seed type.

    :param type: The seed type for which to set the default language.
    :param language: The handle of the language to set as default.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(type, SeedType) or isinstance(type, int), "type must be an instance of SeedType or an integer"
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    return ots_result_t(lib.ots_seed_language_set_default(int(type), _unwrap(language)))


def ots_seed_language_from_code(code: str) -> ots_result_t:
    """
    Returns a seed language from its code.

    :param code: The code of the seed language.
    :return: ots_result_t containing the seed language corresponding to the given code.
    """
    assert isinstance(code, str), "code must be a string"
    return ots_result_t(lib.ots_seed_language_from_code(code.encode('utf-8')))


def ots_seed_language_from_name(name: str) -> ots_result_t:
    """
    Returns a seed language from its name.

    :param name: The name of the seed language.
    :return: ots_result_t containing the seed language corresponding to the given name.
    """
    assert isinstance(name, str), "name must be a string"
    return ots_result_t(lib.ots_seed_language_from_name(name.encode('utf-8')))


def ots_seed_language_from_english_name(name: str) -> ots_result_t:
    """
    Returns a seed language from its English name.

    :param name: The English name of the seed language.
    :return: ots_result_t containing the seed language corresponding to the given English name.
    """
    assert isinstance(name, str), "name must be a string"
    return ots_result_t(lib.ots_seed_language_from_english_name(name.encode('utf-8')))


def ots_seed_language_code(language: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the code of the seed language.

    :param language: The handle of the seed language.
    :return: ots_result_t containing the code of the seed language.
    """
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    return ots_result_t(lib.ots_seed_language_code(_unwrap(language)))


def ots_seed_language_name(language: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the name of the seed language.

    :param language: The handle of the seed language.
    :return: ots_result_t containing the name of the seed language.
    """
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    return ots_result_t(lib.ots_seed_language_name(_unwrap(language)))


def ots_seed_language_english_name(language: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the English name of the seed language.

    :param language: The handle of the seed language.
    :return: ots_result_t containing the English name of the seed language.
    """
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    return ots_result_t(lib.ots_seed_language_english_name(_unwrap(language)))


def ots_seed_language_supported(
    language: ots_handle_t | _CDataBase,
    type: SeedType | int
) -> ots_result_t:
    """
    Checks if a seed language is supported for a specific seed type.

    :param language: The handle of the seed language.
    :param type: The seed type to check support for.
    :return: ots_result_t indicating whether the language is supported for the specified seed type.
    """
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    assert isinstance(type, SeedType) or isinstance(type, int), "type must be an instance of SeedType or an integer"
    return ots_result_t(lib.ots_seed_language_supported(_unwrap(language), int(type)))


def ots_seed_language_is_default(
    language: ots_handle_t | _CDataBase,
    type: SeedType | int
) -> ots_result_t:
    """
    Checks if a seed language is the default for a specific seed type.

    :param language: The handle of the seed language.
    :param type: The seed type to check if the language is default for.
    :return: ots_result_t indicating whether the language is the default for the specified seed type.
    """
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    assert isinstance(type, SeedType) or isinstance(type, int), "type must be an instance of SeedType or an integer"
    return ots_result_t(lib.ots_seed_language_is_default(_unwrap(language), int(type)))


def ots_seed_language_equals(
    language1: ots_handle_t | _CDataBase,
    language2: ots_handle_t | _CDataBase
) -> ots_result_t:
    """
    Checks if two seed languages are equal.

    :param language1: The first seed language to compare.
    :param language2: The second seed language to compare.
    :return: ots_result_t indicating whether the two languages are equal.
    """
    assert isinstance(language1, (ots_handle_t, _CDataBase)), "language1 must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language1).type) == HandleType.SEED_LANGUAGE, "language1 must be of type HandleType.SEED_LANGUAGE"
    assert isinstance(language2, (ots_handle_t, _CDataBase)), "language2 must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language2).type) == HandleType.SEED_LANGUAGE, "language2 must be of type HandleType.SEED_LANGUAGE"
    return ots_result_t(lib.ots_seed_language_equals(_unwrap(language1), _unwrap(language2)))


def ots_seed_language_equals_code(
    language: ots_handle_t | _CDataBase,
    code: str
) -> ots_result_t:
    """
    Checks if a seed language equals a specific code.

    :param language: The handle of the seed language to compare.
    :param code: The code to compare against.
    :return: ots_result_t indicating whether the language equals the specified code.
    """
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    assert isinstance(code, str), "code must be a string"
    return ots_result_t(lib.ots_seed_language_equals_code(_unwrap(language), code.encode('utf-8')))


def ots_seed_phrase(
    seed: ots_handle_t | _CDataBase,
    language: ots_handle_t | _CDataBase,
    password: str = ''
) -> ots_result_t:
    """
    Returns the seed phrase for a given seed and language.

    :param seed: The handle of the seed.
    :param language: The handle of the seed language.
    :param password: The password to use for generating the seed phrase.
    :return: ots_result_t containing the seed phrase.
    """
    assert isinstance(seed, (ots_handle_t, _CDataBase)), "seed must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed).type) == HandleType.SEED, "seed must be of type HandleType.SEED"
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    assert isinstance(password, str), "password must be a string"
    return ots_result_t(lib.ots_seed_phrase(_unwrap(seed), _unwrap(language), password.encode('utf-8')))


def ots_seed_phrase_for_language_code(
    seed: ots_handle_t | _CDataBase,
    language_code: str = '',
    password: str = ''
) -> ots_result_t:
    """
    Returns the seed phrase for a given seed and language code.

    :param seed: The handle of the seed.
    :param language_code: The code of the seed language.
    :param password: The password to use for generating the seed phrase.
    :return: ots_result_t containing the seed phrase.
    """
    assert isinstance(seed, (ots_handle_t, _CDataBase)), "seed must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed).type) == HandleType.SEED, "seed must be of type HandleType.SEED"
    assert isinstance(language_code, str), "language_code must be a string"
    assert isinstance(password, str), "password must be a string"
    return ots_result_t(lib.ots_seed_phrase_for_language_code(_unwrap(seed), language_code.encode('utf-8'), password.encode('utf-8')))


def ots_seed_indices(
    handle: ots_handle_t | _CDataBase,
    password: str = ''
) -> ots_result_t:
    """
    Returns the seed indices for a given seed handle.

    :param handle: The handle of the seed.
    :param password: The password to use for generating the seed indices.
    :return: ots_result_t containing the seed indices.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    assert isinstance(password, str), "password must be a string"
    return ots_result_t(lib.ots_seed_indices(_unwrap(handle), password.encode('utf-8')))


def ots_seed_fingerprint(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the fingerprint of a given seed handle.

    :param handle: The handle of the seed.
    :return: ots_result_t containing the fingerprint of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_fingerprint(_unwrap(handle)))


def ots_seed_is_legacy(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Checks if the given seed handle is a legacy seed.

    :param handle: The handle of the seed.
    :return: ots_result_t indicating whether the seed is legacy.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_is_legacy(_unwrap(handle)))


def ots_seed_type(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the type of the given seed handle.

    :param handle: The handle of the seed.
    :return: ots_result_t containing the type of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_type(_unwrap(handle)))


def ots_seed_address(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the address associated with the given seed handle.

    :param handle: The handle of the seed.
    :return: ots_result_t containing the address of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_address(_unwrap(handle)))


def ots_seed_timestamp(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the timestamp associated with the given seed handle.

    :param handle: The handle of the seed.
    :return: ots_result_t containing the timestamp of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_timestamp(_unwrap(handle)))


def ots_seed_height(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the height associated with the given seed handle.

    :param handle: The handle of the seed.
    :return: ots_result_t containing the height of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_height(_unwrap(handle)))


def ots_seed_network(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the network associated with the given seed handle.

    :param handle: The handle of the seed.
    :return: ots_result_t containing the network of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_network(_unwrap(handle)))


def ots_seed_wallet(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the wallet associated with the given seed handle.

    :param handle: The handle of the seed.
    :return: ots_result_t containing the wallet of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_wallet(_unwrap(handle)))


def ots_seed_indices_merge_values(
    seed_indices1: ots_handle_t | _CDataBase,
    seed_indices2: ots_handle_t | _CDataBase
) -> ots_result_t:
    """
    Merges two seed indices handles into one.

    :param seed_indices1: The first seed indices handle.
    :param seed_indices2: The second seed indices handle.
    :return: ots_result_t containing the merged seed indices.
    """
    assert isinstance(seed_indices1, (ots_handle_t, _CDataBase)), "seed_indices1 must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed_indices1).type) == HandleType.SEED_INDICES, "seed_indices1 must be of type HandleType.SEED_INDICES"
    assert isinstance(seed_indices2, (ots_handle_t, _CDataBase)), "seed_indices2 must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed_indices2).type) == HandleType.SEED_INDICES, "seed_indices2 must be of type HandleType.SEED_INDICES"
    return ots_result_t(lib.ots_seed_indices_merge_values(_unwrap(seed_indices1), _unwrap(seed_indices2)))


def ots_seed_indices_merge_with_password(
    seed_indices: ots_handle_t | _CDataBase,
    password: str
) -> ots_result_t:
    """
    Merges seed indices with a password.

    :param seed_indices: The handle of the seed indices to merge.
    :param password: The password to use for merging.
    :return: ots_result_t containing the merged seed indices.
    """
    assert isinstance(seed_indices, (ots_handle_t, _CDataBase)), "seed_indices must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed_indices).type) == HandleType.SEED_INDICES, "seed_indices must be of type HandleType.SEED_INDICES"
    assert isinstance(password, str), "password must be a string"
    return ots_result_t(lib.ots_seed_indices_merge_with_password(_unwrap(seed_indices), password.encode('utf-8')))


def ots_seed_indices_merge_multiple_values(
    seed_indices: list[ots_handle_t | _CDataBase],
    elements: int,
) -> ots_result_t:
    """
    Merges multiple seed indices handles into one.

    :param seed_indices: A list of seed indices handles to merge.
    :param elements: The number of elements in the list.
    :return: ots_result_t containing the merged seed indices.
    """
    assert isinstance(seed_indices, list) and all(isinstance(i, (ots_handle_t, _CDataBase)) for i in seed_indices), "seed_indices must be a list of ots_handle_t or _CDataBase"
    assert all(HandleType(_unwrap(i).type) == HandleType.SEED_INDICES for i in seed_indices), "All elements in seed_indices must be of type HandleType.SEED_INDICES"
    return ots_result_t(
        lib.ots_seed_indices_merge_multiple_values(
            [_unwrap(si) for si in seed_indices],
            elements,
            len(seed_indices)
        )
    )


def ots_seed_indices_merge_values_and_zero(
    seed_indices1: ots_handle_t | _CDataBase,
    seed_indices2: ots_handle_t | _CDataBase,
    delete_after: bool
) -> ots_result_t:
    """
    Merges two seed indices handles into one and optionally deletes them after merging.

    :param seed_indices1: The first seed indices handle.
    :param seed_indices2: The second seed indices handle.
    :param delete_after: Whether to delete the original handles after merging.
    :return: ots_result_t containing the merged seed indices.
    """
    assert isinstance(seed_indices1, (ots_handle_t, _CDataBase)), "seed_indices1 must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed_indices1).type) == HandleType.SEED_INDICES, "seed_indices1 must be of type HandleType.SEED_INDICES"
    assert isinstance(seed_indices2, (ots_handle_t, _CDataBase)), "seed_indices2 must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed_indices2).type) == HandleType.SEED_INDICES, "seed_indices2 must be of type HandleType.SEED_INDICES"
    return ots_result_t(lib.ots_seed_indices_merge_values_and_zero(_unwrap(seed_indices1), _unwrap(seed_indices2), delete_after))


def ots_seed_indices_merge_with_password_and_zero(
    seed_indices: ots_handle_t | _CDataBase,
    password: str,
    delete_after: bool
) -> ots_result_t:
    """
    Merges seed indices with a password and optionally deletes the original handle after merging.

    :param seed_indices: The handle of the seed indices to merge.
    :param password: The password to use for merging.
    :param delete_after: Whether to delete the original handle after merging.
    :return: ots_result_t containing the merged seed indices.
    """
    assert isinstance(seed_indices, (ots_handle_t, _CDataBase)), "seed_indices must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed_indices).type) == HandleType.SEED_INDICES, "seed_indices must be of type HandleType.SEED_INDICES"
    assert isinstance(password, str), "password must be a string"
    return ots_result_t(lib.ots_seed_indices_merge_with_password_and_zero(_unwrap(seed_indices), password.encode('utf-8'), delete_after))


def ots_seed_indices_merge_multiple_values_and_zero(
    seed_indices: list[ots_handle_t | _CDataBase] | _CDataBase,
    elements: int,
    delete_after: bool
) -> ots_result_t:
    """
    Merges multiple seed indices handles into one and optionally deletes them after merging.

    :param seed_indices: A list of seed indices handles to merge.
    :param elements: The number of elements in the list.
    :param delete_after: Whether to delete the original handles after merging.
    :return: ots_result_t containing the merged seed indices.
    """
    assert isinstance(seed_indices, list) and all(isinstance(i, (ots_handle_t, _CDataBase)) for i in seed_indices), "seed_indices must be a list of ots_handle_t or _CDataBase"
    assert all(HandleType(_unwrap(i).type) == HandleType.SEED_INDICES for i in seed_indices), "All elements in seed_indices must be of type HandleType.SEED_INDICES"
    return ots_result_t(
        lib.ots_seed_indices_merge_multiple_values_and_zero(
            [_unwrap(si) for si in seed_indices],
            elements,
            len(seed_indices),
            delete_after
        )
    )


def ots_legacy_seed_decode(
    phrase: str,
    height: int = 0,
    time: int = 0,
    network: Network | int = Network.MAIN
) -> ots_result_t:
    """
    Decodes a legacy seed phrase into its components.

    :param phrase: The legacy seed phrase to decode.
    :param height: The height at which the seed was created.
    :param time: The time at which the seed was created.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :return: ots_result_t containing the decoded seed information.
    """
    assert isinstance(phrase, str), "phrase must be a string"
    assert isinstance(height, int), "height must be an integer"
    assert isinstance(time, int), "time must be an integer"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    return ots_result_t(lib.ots_legacy_seed_decode(phrase.encode('utf-8'), height, time, int(network)))


def ots_legacy_seed_decode_indices(
    indices: ots_handle_t | _CDataBase,
    height: int = 0,
    time: int = 0,
    network: Network | int = Network.MAIN
) -> ots_result_t:
    """
    Decodes a legacy seed indices handle into its components.

    :param indices: The handle containing the legacy seed indices to decode.
    :param height: The height at which the seed was created.
    :param time: The time at which the seed was created.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :return: ots_result_t containing the decoded seed information.
    """
    assert isinstance(indices, (ots_handle_t, _CDataBase)), "indices must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(indices).type) == HandleType.SEED_INDICES, "indices must be of type HandleType.SEED_INDICES"
    assert isinstance(height, int), "height must be an integer"
    assert isinstance(time, int), "time must be an integer"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    return ots_result_t(lib.ots_legacy_seed_decode_indices(_unwrap(indices), height, time, int(network)))


def ots_monero_seed_create(
    random: bytes,
    height: int = 0,
    time: int = 0,
    network: Network | int = Network.MAIN
) -> ots_result_t:
    """
    Creates a new Monero seed with the specified parameters.

    :param random: Random bytes to use for seed creation.
    :param height: The height at which the seed is created.
    :param time: The time at which the seed is created.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :return: ots_result_t containing the created Monero seed.
    """
    assert isinstance(random, bytes), "random must be bytes"
    assert isinstance(height, int), "height must be an integer"
    assert isinstance(time, int), "time must be an integer"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    return ots_result_t(lib.ots_monero_seed_create(random, height, time, int(network)))


def ots_monero_seed_generate(
    height: int = 0,
    time: int = 0,
    network: Network | int = Network.MAIN
) -> ots_result_t:
    """
    Generates a new Monero seed with the specified parameters.

    :param height: The height at which the seed is generated.
    :param time: The time at which the seed is generated.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :return: ots_result_t containing the generated Monero seed.
    """
    assert isinstance(height, int), "height must be an integer"
    assert isinstance(time, int), "time must be an integer"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    return ots_result_t(lib.ots_monero_seed_generate(height, time, int(network)))


def ots_monero_seed_decode(
    phrase: str,
    height: int = 0,
    time: int = 0,
    network: Network | int = Network.MAIN,
    passphrase: str = ''
) -> ots_result_t:
    """
    Decodes a Monero seed phrase into its components.

    :param phrase: The Monero seed phrase to decode.
    :param height: The height at which the seed was created.
    :param time: The time at which the seed was created.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :param passphrase: An optional passphrase for additional security.
    :return: ots_result_t containing the decoded seed information.
    """
    assert isinstance(phrase, str), "phrase must be a string"
    assert isinstance(height, int), "height must be an integer"
    assert isinstance(time, int), "time must be an integer"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    assert isinstance(passphrase, str), "passphrase must be a string"
    return ots_result_t(lib.ots_monero_seed_decode(phrase.encode('utf-8'), height, time, int(network), passphrase.encode('utf-8')))


def ots_monero_seed_decode_indices(
    indices: ots_handle_t | _CDataBase,
    height: int = 0,
    time: int = 0,
    network: Network | int = Network.MAIN,
    passphrase: str = ''
) -> ots_result_t:
    """
    Decodes a Monero seed indices handle into its components.

    :param indices: The handle containing the Monero seed indices to decode.
    :param height: The height at which the seed was created.
    :param time: The time at which the seed was created.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :param passphrase: An optional passphrase for additional security.
    :return: ots_result_t containing the decoded seed information.
    """
    assert isinstance(indices, (ots_handle_t, _CDataBase)), "indices must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(indices).type) == HandleType.SEED_INDICES, "indices must be of type HandleType.SEED_INDICES"
    assert isinstance(height, int), "height must be an integer"
    assert isinstance(time, int), "time must be an integer"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    assert isinstance(passphrase, str), "passphrase must be a string"
    return ots_result_t(lib.ots_monero_seed_decode_indices(_unwrap(indices), height, time, int(network), passphrase.encode('utf-8')))


def ots_polyseed_create(
    random: bytes,
    network: Network | int = Network.MAIN,
    time: int = 0,
    passphrase: str = ''
) -> ots_result_t:
    """
    Creates a new Polyseed with the specified parameters.

    :param random: Random bytes to use for seed creation.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :param time: The time at which the seed is created, defaults to 0 (current time).
    :param passphrase: Optional passphrase for seed offset (empty string for none).
    :return: ots_result_t containing the created Polyseed.
    """
    assert isinstance(random, bytes), "random must be bytes"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    assert isinstance(time, int), "time must be an integer"
    assert isinstance(passphrase, str), "passphrase must be a string"
    return ots_result_t(lib.ots_polyseed_create(random, int(network), time, passphrase.encode('utf-8')))


def ots_polyseed_generate(
    network: Network | int = Network.MAIN,
    time: int = 0,
    passphrase: str = ''
) -> ots_result_t:
    """
    Generates a new Polyseed with the specified parameters.

    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :param time: The time at which the seed is generated, defaults to 0 (current time).
    :param passphrase: Optional passphrase for seed offset (empty string for none).
    :return: ots_result_t containing the generated Polyseed.
    """
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    assert isinstance(time, int), "time must be an integer"
    assert isinstance(passphrase, str), "passphrase must be a string"
    return ots_result_t(lib.ots_polyseed_generate(int(network), time, passphrase.encode('utf-8')))


def ots_polyseed_decode(
    phrase: str,
    network: Network | int = Network.MAIN,
    password: str = '',
    passphrase: str = ''
) -> ots_result_t:
    """
    Decodes a Polyseed phrase into its components.

    :param phrase: The Polyseed phrase to decode.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :param password: Optional decryption password (empty string for none).
    :param passphrase: Optional passphrase for seed offset (empty string for none).
    :return: ots_result_t containing the decoded seed information.
    """
    assert isinstance(phrase, str), "phrase must be a string"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    assert isinstance(password, str), "password must be a string"
    assert isinstance(passphrase, str), "passphrase must be a string"
    return ots_result_t(lib.ots_polyseed_decode(phrase.encode('utf-8'), int(network), password.encode('utf-8'), passphrase.encode('utf-8')))


def ots_polyseed_decode_indices(
    indices: ots_handle_t | _CDataBase,
    network: Network | int = Network.MAIN,
    password: str = '',
    passphrase: str = ''
) -> ots_result_t:
    """
    Decodes a Polyseed indices handle into its components.

    :param indices: The handle containing the Polyseed indices to decode.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :param password: Optional decryption password (empty string for none).
    :param passphrase: Optional passphrase for seed offset (empty string for none).
    :return: ots_result_t containing the decoded seed information.
    """
    assert isinstance(indices, (ots_handle_t, _CDataBase)), "indices must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(indices).type) == HandleType.SEED_INDICES, "indices must be of type HandleType.SEED_INDICES"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    assert isinstance(password, str), "password must be a string"
    assert isinstance(passphrase, str), "passphrase must be a string"
    return ots_result_t(lib.ots_polyseed_decode_indices(_unwrap(indices), int(network), password.encode('utf-8'), passphrase.encode('utf-8')))


def ots_polyseed_decode_with_language(
    phrase: str,
    language: ots_handle_t | _CDataBase,
    network: Network | int = Network.MAIN,
    password: str = '',
    passphrase: str = ''
) -> ots_result_t:
    """
    Decodes a Polyseed phrase using a specific language.

    :param phrase: The Polyseed phrase to decode.
    :param language: The handle of the seed language to use for decoding.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :param password: Optional decryption password (empty string for none).
    :param passphrase: Optional passphrase for seed offset (empty string for none).
    :return: ots_result_t containing the decoded seed information.
    """
    assert isinstance(phrase, str), "phrase must be a string"
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    assert isinstance(password, str), "password must be a string"
    assert isinstance(passphrase, str), "passphrase must be a string"
    return ots_result_t(lib.ots_polyseed_decode_with_language(_unwrap(phrase), _unwrap(language), int(network), password.encode('utf-8'), passphrase.encode('utf-8')))


def ots_polyseed_decode_with_language_code(
    phrase: str,
    language_code: str,
    network: Network | int = Network.MAIN,
    password: str = '',
    passphrase: str = ''
) -> ots_result_t:
    """
    Decodes a Polyseed phrase using a specific language code.

    :param phrase: The Polyseed phrase to decode.
    :param language_code: The code of the seed language to use for decoding.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :param password: Optional decryption password (empty string for none).
    :param passphrase: Optional passphrase for seed offset (empty string for none).
    :return: ots_result_t containing the decoded seed information.
    """
    assert isinstance(phrase, str), "phrase must be a string"
    assert isinstance(language_code, str), "language_code must be a string"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    assert isinstance(password, str), "password must be a string"
    assert isinstance(passphrase, str), "passphrase must be a string"
    return ots_result_t(lib.ots_polyseed_decode_with_language_code(phrase.encode('utf-8'), language_code.encode('utf-8'), int(network), password.encode('utf-8'), passphrase.encode('utf-8')))


def ots_address_create(address: str) -> ots_result_t:
    """
    Creates an address from a given string.

    :param address: The address string to create.
    :return: ots_result_t containing the created address handle.
    """
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_address_create(address.encode('utf-8')))


def ots_address_type(address: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the type of the given address handle.

    :param address: The handle of the address.
    :return: ots_result_t containing the type of the address.
    """
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_address_type(_unwrap(address)))


def ots_address_network(address: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the network of the given address handle.

    :param address: The handle of the address.
    :return: ots_result_t containing the network of the address.
    """
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_address_network(_unwrap(address)))


def ots_address_fingerprint(address: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the fingerprint of the given address handle.

    :param address: The handle of the address.
    :return: ots_result_t containing the fingerprint of the address.
    """
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_address_fingerprint(_unwrap(address)))


def ots_address_is_integrated(address: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Checks if the given address handle is an integrated address.

    :param address: The handle of the address.
    :return: ots_result_t indicating whether the address is integrated.
    """
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_address_is_integrated(_unwrap(address)))


def ots_address_payment_id(address: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the payment ID of the given address handle.

    :param address: The handle of the address.
    :return: ots_result_t containing the payment ID of the address.
    """
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_address_payment_id(_unwrap(address)))


def ots_address_from_integrated(address: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Extracts the base address from an integrated address handle.

    :param address: The handle of the integrated address.
    :return: ots_result_t containing the base address.
    """
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_address_from_integrated(_unwrap(address)))


def ots_address_length(address: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the length of the given address handle.

    :param address: The handle of the address.
    :return: ots_result_t containing the length of the address.
    """
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_address_length(_unwrap(address)))


def ots_address_base58_string(address_handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the base58 string representation of the given address handle.

    :param address_handle: The handle of the address.
    :return: ots_result_t containing the base58 string representation of the address.
    """
    assert isinstance(address_handle, (ots_handle_t, _CDataBase)), "address_handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address_handle).type) == HandleType.ADDRESS, "address_handle must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_address_base58_string(_unwrap(address_handle)))


def ots_address_equal(
    address1: ots_handle_t | _CDataBase,
    address2: ots_handle_t | _CDataBase
) -> ots_result_t:
    """
    Compares two address handles for equality.

    :param address1: The first address handle.
    :param address2: The second address handle.
    :return: ots_result_t indicating whether the addresses are equal.
    """
    assert isinstance(address1, (ots_handle_t, _CDataBase)), "address1 must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address1).type) == HandleType.ADDRESS, "address1 must be of type HandleType.ADDRESS"
    assert isinstance(address2, (ots_handle_t, _CDataBase)), "address2 must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address2).type) == HandleType.ADDRESS, "address2 must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_address_equal(_unwrap(address1), _unwrap(address2)))


def ots_address_equal_string(
    address_handle: ots_handle_t | _CDataBase,
    address_string: str
) -> ots_result_t:
    """
    Compares an address handle with a string representation of an address for equality.

    :param address_handle: The handle of the address.
    :param address_string: The string representation of the address.
    :return: ots_result_t indicating whether the address handle matches the string.
    """
    assert isinstance(address_handle, (ots_handle_t, _CDataBase)), "address_handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address_handle).type) == HandleType.ADDRESS, "address_handle must be of type HandleType.ADDRESS"
    assert isinstance(address_string, str), "address_string must be a string"
    return ots_result_t(lib.ots_address_equal_string(_unwrap(address_handle), address_string.encode('utf-8')))


def ots_address_string_valid(
    address: str,
    network: Network | int = Network.MAIN
) -> ots_result_t:
    """
    Checks if the given address string is valid for the specified network.

    :param address: The address string to validate.
    :param network: The network for which to validate the address (Main, Test, or Stagenet).
    :return: ots_result_t indicating whether the address string is valid.
    """
    assert isinstance(address, str), "address must be a string"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    return ots_result_t(lib.ots_address_string_valid(address.encode('utf-8'), int(network)))


def ots_address_string_network(address: str) -> ots_result_t:
    """
    Returns the network of the given address string.

    :param address: The address string to check.
    :return: ots_result_t containing the network of the address.
    """
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_address_string_network(address.encode('utf-8')))


def ots_address_string_type(address: str) -> ots_result_t:
    """
    Returns the type of the given address string.

    :param address: The address string to check.
    :return: ots_result_t containing the type of the address.
    """
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_address_string_type(address.encode('utf-8')))


def ots_address_string_fingerprint(address: str) -> ots_result_t:
    """
    Returns the fingerprint of the given address string.

    :param address: The address string to check.
    :return: ots_result_t containing the fingerprint of the address.
    """
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_address_string_fingerprint(address.encode('utf-8')))


def ots_address_string_is_integrated(address: str) -> ots_result_t:
    """
    Checks if the given address string is an integrated address.

    :param address: The address string to check.
    :return: ots_result_t indicating whether the address string is integrated.
    """
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_address_string_is_integrated(address.encode('utf-8')))


def ots_address_string_payment_id(address: str) -> ots_result_t:
    """
    Returns the payment ID of the given address string.

    :param address: The address string to check.
    :return: ots_result_t containing the payment ID of the address.
    """
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_address_string_payment_id(address.encode('utf-8')))


def ots_address_string_integrated(address: str) -> ots_result_t:
    """
    Extracts the base address from an integrated address string.

    :param address: The integrated address string to check.
    :return: ots_result_t containing the base address.
    """
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_address_string_integrated(address.encode('utf-8')))


def ots_wallet_create(
    key: bytes,
    height: int = 0,
    network: Network | int = Network.MAIN
) -> ots_result_t:
    """
    Creates a new wallet with the specified key, height, and network.

    :param key: The key to use for the wallet.
    :param height: The height at which the wallet is created.
    :param network: The network for which the wallet is intended (Main, Test, or Stagenet).
    :return: ots_result_t containing the created wallet handle.
    """
    assert isinstance(key, bytes), "key must be bytes"
    assert len(key) == 32, "key must be 32 bytes long"
    assert isinstance(height, int), "height must be an integer"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    return ots_result_t(lib.ots_wallet_create(key, height, int(network)))


def ots_wallet_height(wallet: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the height of the given wallet handle.

    :param wallet: The handle of the wallet.
    :return: ots_result_t containing the height of the wallet.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    return ots_result_t(lib.ots_wallet_height(_unwrap(wallet)))


def ots_wallet_address(wallet: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the primary address of the given wallet handle.

    :param wallet: The handle of the wallet.
    :return: ots_result_t containing the primary address of the wallet.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    return ots_result_t(lib.ots_wallet_address(_unwrap(wallet)))


def ots_wallet_subaddress(
    wallet: ots_handle_t | _CDataBase,
    account: int,
    index: int
) -> ots_result_t:
    """
    Returns a subaddress from the given wallet handle based on account and index.

    :param wallet: The handle of the wallet.
    :param account: The account number for the subaddress.
    :param index: The index of the subaddress within the account.
    :return: ots_result_t containing the requested subaddress.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(account, int), "account must be an integer"
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_wallet_subaddress(_unwrap(wallet), account, index))


def ots_wallet_accounts(
    wallet: ots_handle_t | _CDataBase,
    max: int,
    offset: int = 0
) -> ots_result_t:
    """
    Returns a list of accounts from the given wallet handle.

    :param wallet: The handle of the wallet.
    :param max: The maximum number of accounts to return.
    :param offset: The offset from which to start returning accounts.
    :return: ots_result_t containing the requested accounts.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(max, int), "max must be an integer"
    assert isinstance(offset, int), "offset must be an integer"
    return ots_result_t(lib.ots_wallet_accounts(_unwrap(wallet), max, offset))


def ots_wallet_subaddresses(
    wallet: ots_handle_t | _CDataBase,
    account: int,
    max: int,
    offset: int = 0
) -> ots_result_t:
    """
    Returns a list of subaddresses from the given wallet handle based on account.

    :param wallet: The handle of the wallet.
    :param account: The account number for which to return subaddresses.
    :param max: The maximum number of subaddresses to return.
    :param offset: The offset from which to start returning subaddresses.
    :return: ots_result_t containing the requested subaddresses.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(account, int), "account must be an integer"
    assert isinstance(max, int), "max must be an integer"
    assert isinstance(offset, int), "offset must be an integer"
    return ots_result_t(lib.ots_wallet_subaddresses(_unwrap(wallet), account, max, offset))


def ots_wallet_has_address(
    wallet: ots_handle_t | _CDataBase,
    address: ots_handle_t | _CDataBase,
    max_account_depth: int,
    max_index_depth: int
) -> ots_result_t:
    """
    Checks if the given wallet handle contains the specified address handle.

    :param wallet: The handle of the wallet.
    :param address: The handle of the address to check.
    :param max_account_depth: The maximum account depth to consider.
    :param max_index_depth: The maximum index depth to consider.
    :return: ots_result_t indicating whether the address is present in the wallet.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    assert isinstance(max_account_depth, int), "max_account_depth must be an integer"
    assert isinstance(max_index_depth, int), "max_index_depth must be an integer"
    return ots_result_t(lib.ots_wallet_has_address(_unwrap(wallet), _unwrap(address), max_account_depth, max_index_depth))


def ots_wallet_has_address_string(
    wallet_handle: ots_handle_t | _CDataBase,
    address: str,
    max_account_depth: int,
    max_index_depth: int
) -> ots_result_t:
    """
    Checks if the given wallet handle contains the specified address string.

    :param wallet_handle: The handle of the wallet.
    :param address: The string representation of the address to check.
    :param max_account_depth: The maximum account depth to consider.
    :param max_index_depth: The maximum index depth to consider.
    :return: ots_result_t indicating whether the address is present in the wallet.
    """
    assert isinstance(wallet_handle, (ots_handle_t, _CDataBase)), "wallet_handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet_handle).type) == HandleType.WALLET, "wallet_handle must be of type HandleType.WALLET"
    assert isinstance(address, str), "address must be a string"
    assert isinstance(max_account_depth, int), "max_account_depth must be an integer"
    assert isinstance(max_index_depth, int), "max_index_depth must be an integer"
    return ots_result_t(lib.ots_wallet_has_address_string(_unwrap(wallet_handle), address.encode('utf-8'), max_account_depth, max_index_depth))


def ots_wallet_address_index(
    wallet: ots_handle_t | _CDataBase,
    address: ots_handle_t | _CDataBase,
    max_account_depth: int,
    max_index_depth: int
) -> ots_result_t:
    """
    Returns the index of the specified address in the wallet.

    :param wallet: The handle of the wallet.
    :param address: The handle of the address to find.
    :param max_account_depth: The maximum account depth to consider.
    :param max_index_depth: The maximum index depth to consider.
    :return: ots_result_t containing the index of the address in the wallet.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    assert isinstance(max_account_depth, int), "max_account_depth must be an integer"
    assert isinstance(max_index_depth, int), "max_index_depth must be an integer"
    return ots_result_t(lib.ots_wallet_address_index(_unwrap(wallet), _unwrap(address), max_account_depth, max_index_depth))


def ots_wallet_address_string_index(
    wallet_handle: ots_handle_t | _CDataBase,
    address: str,
    max_account_depth: int,
    max_index_depth: int
) -> ots_result_t:
    """
    Returns the index of the specified address string in the wallet.

    :param wallet_handle: The handle of the wallet.
    :param address: The string representation of the address to find.
    :param max_account_depth: The maximum account depth to consider.
    :param max_index_depth: The maximum index depth to consider.
    :return: ots_result_t containing the index of the address in the wallet.
    """
    assert isinstance(wallet_handle, (ots_handle_t, _CDataBase)), "wallet_handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet_handle).type) == HandleType.WALLET, "wallet_handle must be of type HandleType.WALLET"
    assert isinstance(address, str), "address must be a string"
    assert isinstance(max_account_depth, int), "max_account_depth must be an integer"
    assert isinstance(max_index_depth, int), "max_index_depth must be an integer"
    return ots_result_t(lib.ots_wallet_address_string_index(_unwrap(wallet_handle), address.encode('utf-8'), max_account_depth, max_index_depth))


def ots_wallet_secret_view_key(wallet: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the secret view key of the given wallet handle.

    :param wallet: The handle of the wallet.
    :return: ots_result_t containing the secret view key of the wallet.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    return ots_result_t(lib.ots_wallet_secret_view_key(_unwrap(wallet)))


def ots_wallet_public_view_key(wallet: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the public view key of the given wallet handle.

    :param wallet: The handle of the wallet.
    :return: ots_result_t containing the public view key of the wallet.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    return ots_result_t(lib.ots_wallet_public_view_key(_unwrap(wallet)))


def ots_wallet_secret_spend_key(wallet: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the secret spend key of the given wallet handle.

    :param wallet: The handle of the wallet.
    :return: ots_result_t containing the secret spend key of the wallet.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    return ots_result_t(lib.ots_wallet_secret_spend_key(_unwrap(wallet)))


def ots_wallet_public_spend_key(wallet: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the public spend key of the given wallet handle.

    :param wallet: The handle of the wallet.
    :return: ots_result_t containing the public spend key of the wallet.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    return ots_result_t(lib.ots_wallet_public_spend_key(_unwrap(wallet)))


def ots_wallet_import_outputs(
    wallet: ots_handle_t | _CDataBase,
    outputs: str
) -> ots_result_t:
    """
    Imports outputs into the given wallet handle.

    :param wallet: The handle of the wallet.
    :param outputs: A string containing the outputs to import.
    :return: ots_result_t indicating the result of the import operation.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(outputs, str), "outputs must be a string"
    return ots_result_t(lib.ots_wallet_import_outputs(_unwrap(wallet), outputs.encode('utf-8')))


def ots_wallet_export_key_images(wallet: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Exports key images from the given wallet handle.

    :param wallet: The handle of the wallet.
    :return: ots_result_t containing the exported key images.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    return ots_result_t(lib.ots_wallet_export_key_images(_unwrap(wallet)))


def ots_wallet_describe_tx(
    wallet: ots_handle_t | _CDataBase,
    unsigned_tx: bytes
) -> ots_result_t:
    """
    Describes a transaction for the given wallet handle.

    :param wallet: The handle of the wallet.
    :param unsigned_tx: A bytes object containing the unsigned transaction to describe.
    :return: ots_result_t containing the description of the transaction.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(unsigned_tx, bytes), "unsigned_tx must be a bytes object"
    return ots_result_t(lib.ots_wallet_describe_tx(_unwrap(wallet), unsigned_tx, len(unsigned_tx)))


def ots_wallet_check_tx(
    wallet: ots_handle_t | _CDataBase,
    unsigned_tx: ots_handle_t | _CDataBase
) -> ots_result_t:
    """
    Checks a transaction for the given wallet handle.

    :param wallet: The handle of the wallet.
    :param unsigned_tx: The handle of the unsigned transaction to check.
    :return: ots_result_t indicating the result of the check operation.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(unsigned_tx, (ots_handle_t, _CDataBase)), "unsigned_tx must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(unsigned_tx).type) == HandleType.TX, "unsigned_tx must be of type HandleType.TX"
    return ots_result_t(lib.ots_wallet_check_tx(_unwrap(wallet), _unwrap(unsigned_tx)))


def ots_wallet_check_tx_string(
    wallet: ots_handle_t | _CDataBase,
    unsigned_tx: bytes
) -> ots_result_t:
    """
    Checks a transaction for the given wallet handle using a string representation of the unsigned transaction.

    :param wallet: The handle of the wallet.
    :param unsigned_tx: A bytes object containing the unsigned transaction to check.
    :return: ots_result_t indicating the result of the check operation.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(unsigned_tx, bytes), "unsigned_tx must be a bytes object"
    return ots_result_t(lib.ots_wallet_check_tx_string(_unwrap(wallet), unsigned_tx, len(unsigned_tx)))


def ots_wallet_sign_transaction(
    wallet: ots_handle_t | _CDataBase,
    unsigned_tx: bytes
) -> ots_result_t:
    """
    Signs a transaction for the given wallet handle.

    :param wallet: The handle of the wallet.
    :param unsigned_tx: A bytes object containing the unsigned transaction to sign.
    :return: ots_result_t containing the signed transaction.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(unsigned_tx, bytes), "unsigned_tx must be a bytes object"
    return ots_result_t(lib.ots_wallet_sign_transaction(_unwrap(wallet), unsigned_tx, len(unsigned_tx)))


def ots_wallet_sign_data(
    wallet: ots_handle_t | _CDataBase,
    data: str
) -> ots_result_t:
    """
    Signs data with the given wallet handle.

    :param wallet: The handle of the wallet.
    :param data: The data to sign.
    :return: ots_result_t containing the signature of the data.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(data, str), "data must be a string"
    return ots_result_t(lib.ots_wallet_sign_data(_unwrap(wallet), data.encode('utf-8')))


def ots_wallet_sign_data_with_index(
    wallet: ots_handle_t | _CDataBase,
    data: str,
    account: int,
    subaddr: int
) -> ots_result_t:
    """
    Signs data with the specified account and subaddress in the given wallet handle.

    :param wallet: The handle of the wallet.
    :param data: The data to sign.
    :param account: The account number to use for signing.
    :param subaddr: The subaddress index to use for signing.
    :return: ots_result_t containing the signature of the data.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(data, str), "data must be a string"
    assert isinstance(account, int), "account must be an integer"
    assert isinstance(subaddr, int), "subaddr must be an integer"
    return ots_result_t(lib.ots_wallet_sign_data_with_index(_unwrap(wallet), data.encode('utf-8'), account, subaddr))


def ots_wallet_sign_data_with_address(
    wallet: ots_handle_t | _CDataBase,
    data: str,
    address: ots_handle_t | _CDataBase
) -> ots_result_t:
    """
    Signs data with the specified address in the given wallet handle.

    :param wallet: The handle of the wallet.
    :param data: The data to sign.
    :param address: The handle of the address to use for signing.
    :return: ots_result_t containing the signature of the data.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(data, str), "data must be a string"
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_wallet_sign_data_with_address(_unwrap(wallet), data.encode('utf-8'), _unwrap(address)))


def ots_wallet_sign_data_with_address_string(
    wallet: ots_handle_t | _CDataBase,
    data: str,
    address: str
) -> ots_result_t:
    """
    Signs data with the specified address string in the given wallet handle.

    :param wallet: The handle of the wallet.
    :param data: The data to sign.
    :param address: The string representation of the address to use for signing.
    :return: ots_result_t containing the signature of the data.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(data, str), "data must be a string"
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_wallet_sign_data_with_address_string(_unwrap(wallet), data.encode('utf-8'), address.encode('utf-8')))


def ots_wallet_verify_data(
    wallet: ots_handle_t | _CDataBase,
    data: str,
    signature: str,
    legacy_fallback: bool = False
) -> ots_result_t:
    """
    Verifies the signature of data with the given wallet handle.

    :param wallet: The handle of the wallet.
    :param data: The data whose signature is to be verified.
    :param signature: The signature to verify.
    :param legacy_fallback: Whether to use legacy fallback verification.
    :return: ots_result_t indicating the result of the verification.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(data, str), "data must be a string"
    assert isinstance(signature, str), "signature must be a string"
    assert isinstance(legacy_fallback, bool), "legacy_fallback must be a boolean"
    return ots_result_t(lib.ots_wallet_verify_data(_unwrap(wallet), data.encode('utf-8'), signature.encode('utf-8'), legacy_fallback))


def ots_wallet_verify_data_with_index(
    wallet: ots_handle_t | _CDataBase,
    data: str,
    account: int,
    subaddr: int,
    signature: str,
    legacy_fallback: bool = False
) -> ots_result_t:
    """
    Verifies the signature of data with the specified account and subaddress in the given wallet handle.

    :param wallet: The handle of the wallet.
    :param data: The data whose signature is to be verified.
    :param account: The account number to use for verification.
    :param subaddr: The subaddress index to use for verification.
    :param signature: The signature to verify.
    :param legacy_fallback: Whether to use legacy fallback verification.
    :return: ots_result_t indicating the result of the verification.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(data, str), "data must be a string"
    assert isinstance(account, int), "account must be an integer"
    assert isinstance(subaddr, int), "subaddr must be an integer"
    assert isinstance(signature, str), "signature must be a string"
    assert isinstance(legacy_fallback, bool), "legacy_fallback must be a boolean"
    return ots_result_t(lib.ots_wallet_verify_data_with_index(_unwrap(wallet), data.encode('utf-8'), account, subaddr, signature.encode('utf-8'), legacy_fallback))


def ots_wallet_verify_data_with_address(
    wallet: ots_handle_t | _CDataBase,
    data: str,
    address: ots_handle_t | _CDataBase,
    signature: str,
    legacy_fallback: bool = False
) -> ots_result_t:
    """
    Verifies the signature of data with the specified address in the given wallet handle.

    :param wallet: The handle of the wallet.
    :param data: The data whose signature is to be verified.
    :param address: The handle of the address to use for verification.
    :param signature: The signature to verify.
    :param legacy_fallback: Whether to use legacy fallback verification.
    :return: ots_result_t indicating the result of the verification.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(data, str), "data must be a string"
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    assert isinstance(signature, str), "signature must be a string"
    assert isinstance(legacy_fallback, bool), "legacy_fallback must be a boolean"
    return ots_result_t(lib.ots_wallet_verify_data_with_address(_unwrap(wallet), data.encode('utf-8'), _unwrap(address), signature.encode('utf-8'), legacy_fallback))


def ots_wallet_verify_data_with_address_string(
    wallet: ots_handle_t | _CDataBase,
    data: str,
    address: str,
    signature: str,
    legacy_fallback: bool = False
) -> ots_result_t:
    """
    Verifies the signature of data with the specified address string in the given wallet handle.

    :param wallet: The handle of the wallet.
    :param data: The data whose signature is to be verified.
    :param address: The string representation of the address to use for verification.
    :param signature: The signature to verify.
    :param legacy_fallback: Whether to use legacy fallback verification.
    :return: ots_result_t indicating the result of the verification.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(data, str), "data must be a string"
    assert isinstance(address, str), "address must be a string"
    assert isinstance(signature, str), "signature must be a string"
    assert isinstance(legacy_fallback, bool), "legacy_fallback must be a boolean"
    return ots_result_t(lib.ots_wallet_verify_data_with_address_string(_unwrap(wallet), data.encode('utf-8'), address.encode('utf-8'), signature.encode('utf-8'), legacy_fallback))


def ots_tx_description(
    tx_description: ots_handle_t | _CDataBase
) -> ots_tx_description_t:
    """
    Returns the transaction description for the given transaction handle.

    :param tx_description: The handle of the transaction description.
    :return: ots_tx_description_t containing the transaction description.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    return ots_tx_description_t(lib.ots_tx_description(_unwrap(tx_description)))


def ots_tx_description_tx_set(
    tx_description: ots_handle_t | _CDataBase
) -> str:
    """
    Returns the transaction set for the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :return: A string representing the transaction set.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    return lib.ots_tx_description_tx_set(_unwrap(tx_description)).decode('utf-8')


def ots_tx_description_tx_set_size(
    tx_description: ots_handle_t | _CDataBase
) -> int:
    """
    Returns the size of the transaction set for the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :return: An integer representing the size of the transaction set.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    return lib.ots_tx_description_tx_set_size(_unwrap(tx_description))


def ots_tx_description_amount_in(
    tx_description: ots_handle_t | _CDataBase
) -> int:
    """
    Returns the total amount in for the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :return: An integer representing the total amount in.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    return lib.ots_tx_description_amount_in(_unwrap(tx_description))


def ots_tx_description_amount_out(
    tx_description: ots_handle_t | _CDataBase
) -> int:
    """
    Returns the total amount out for the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :return: An integer representing the total amount out.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    return lib.ots_tx_description_amount_out(_unwrap(tx_description))


def ots_tx_description_flows_count(
    tx_description: ots_handle_t | _CDataBase
) -> int:
    """
    Returns the number of flows in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :return: An integer representing the number of flows.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    return lib.ots_tx_description_flows_count(_unwrap(tx_description))


def ots_tx_description_flow_address(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> str:
    """
    Returns the address of a flow in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the flow to retrieve the address for.
    :return: A string representing the address of the flow.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_flow_address(_unwrap(tx_description), index).decode('utf-8')


def ots_tx_description_flow_amount(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the amount of a flow in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the flow to retrieve the amount for.
    :return: An integer representing the amount of the flow.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_flow_amount(_unwrap(tx_description), index)


def ots_tx_description_fee(
    tx_description: ots_handle_t | _CDataBase
) -> int:
    """
    Returns the fee for the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :return: An integer representing the fee.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    return lib.ots_tx_description_fee(_unwrap(tx_description))


def ots_tx_description_transfers_count(
    tx_description: ots_handle_t | _CDataBase
) -> int:
    """
    Returns the number of transfers in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :return: An integer representing the number of transfers.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    return lib.ots_tx_description_transfers_count(_unwrap(tx_description))


def ots_tx_description_transfer_amount_in(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the amount in for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the amount in for.
    :return: An integer representing the amount in for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_amount_in(_unwrap(tx_description), index)


def ots_tx_description_transfer_amount_out(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the amount out for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the amount out for.
    :return: An integer representing the amount out for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_amount_out(_unwrap(tx_description), index)


def ots_tx_description_transfer_ring_size(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the ring size for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the ring size for.
    :return: An integer representing the ring size for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_ring_size(_unwrap(tx_description), index)


def ots_tx_description_transfer_unlock_time(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the unlock time for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the unlock time for.
    :return: An integer representing the unlock time for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_unlock_time(_unwrap(tx_description), index)


def ots_tx_description_transfer_flows_count(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the number of flows for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the number of flows for.
    :return: An integer representing the number of flows for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_flows_count(_unwrap(tx_description), index)


def ots_tx_description_transfer_flow_address(
    tx_description: ots_handle_t | _CDataBase,
    index: int,
    flow_index: int
) -> str:
    """
    Returns the address of a specific flow in a transfer within the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the flow address for.
    :param flow_index: The index of the flow within the transfer.
    :return: A string representing the address of the flow.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    assert isinstance(flow_index, int), "flow_index must be an integer"
    return lib.ots_tx_description_transfer_flow_address(_unwrap(tx_description), index, flow_index).decode('utf-8')


def ots_tx_description_transfer_flow_amount(
    tx_description: ots_handle_t | _CDataBase,
    index: int,
    flow_index: int
) -> int:
    """
    Returns the amount of a specific flow in a transfer within the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the flow amount for.
    :param flow_index: The index of the flow within the transfer.
    :return: An integer representing the amount of the flow.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    assert isinstance(flow_index, int), "flow_index must be an integer"
    return lib.ots_tx_description_transfer_flow_amount(_unwrap(tx_description), index, flow_index)


def ots_tx_description_transfer_has_change(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> bool:
    """
    Checks if a specific transfer in the given transaction description handle has change.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to check for change.
    :return: A boolean indicating whether the transfer has change.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_has_change(_unwrap(tx_description), index)


def ots_tx_description_transfer_change_address(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> str:
    """
    Returns the change address for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the change address for.
    :return: A string representing the change address.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_change_address(_unwrap(tx_description), index).decode('utf-8')


def ots_tx_description_transfer_change_amount(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the change amount for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the change amount for.
    :return: An integer representing the change amount.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_change_amount(_unwrap(tx_description), index)


def ots_tx_description_transfer_fee(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the fee for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the fee for.
    :return: An integer representing the fee for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_fee(_unwrap(tx_description), index)


def ots_tx_description_transfer_payment_id(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the payment ID for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the payment ID for.
    :return: An integer representing the payment ID for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_payment_id(_unwrap(tx_description), index)


def ots_tx_description_transfer_dummy_outputs(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the number of dummy outputs for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the number of dummy outputs for.
    :return: An integer representing the number of dummy outputs for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_dummy_outputs(_unwrap(tx_description), index)


def ots_tx_description_transfer_extra(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> str:
    """
    Returns the extra data for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the extra data for.
    :return: A string representing the extra data for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_extra(_unwrap(tx_description), index).decode('utf-8')


def ots_tx_description_transfer_extra_size(
    tx_description: ots_handle_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the size of the extra data for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the extra data size for.
    :return: An integer representing the size of the extra data for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return lib.ots_tx_description_transfer_extra_size(_unwrap(tx_description), index)


def ots_seed_jar_add_seed(seed: ots_handle_t | _CDataBase, name: str) -> ots_result_t:
    """
    Adds a seed to the seed jar with the specified name.

    :param seed: The seed handle to add.
    :param name: The name to associate with the seed.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(seed, (ots_handle_t, _CDataBase)), "seed must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed).type) == HandleType.SEED, "seed must be of type HandleType.SEED"
    assert isinstance(name, str), "name must be a string"
    return ots_result_t(lib.ots_seed_jar_add_seed(_unwrap(seed), name.encode('utf-8')))


def ots_seed_jar_remove_seed(seed: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Removes a seed from the seed jar.

    :param seed: The seed handle to remove.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(seed, (ots_handle_t, _CDataBase)), "seed must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed).type) == HandleType.SEED, "seed must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_jar_remove_seed(_unwrap(seed)))


def ots_seed_jar_purge_seed_for_index(index: int) -> ots_result_t:
    """
    Purges a seed from the seed jar based on its index.

    :param index: The index of the seed to purge.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_purge_seed_for_index(index))


def ots_seed_jar_purge_seed_for_name(name: str) -> ots_result_t:
    """
    Purges a seed from the seed jar based on its name.

    :param name: The name of the seed to purge.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(name, str), "name must be a string"
    return ots_result_t(lib.ots_seed_jar_purge_seed_for_name(name.encode('utf-8')))


def ots_seed_jar_purge_seed_for_fingerprint(fingerprint: str) -> ots_result_t:
    """
    Purges a seed from the seed jar based on its fingerprint.

    :param fingerprint: The fingerprint of the seed to purge.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(fingerprint, str), "fingerprint must be a string"
    return ots_result_t(lib.ots_seed_jar_purge_seed_for_fingerprint(fingerprint.encode('utf-8')))


def ots_seed_jar_purge_seed_for_address(address: str) -> ots_result_t:
    """
    Purges a seed from the seed jar based on its address.

    :param address: The address of the seed to purge.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_seed_jar_purge_seed_for_address(address.encode('utf-8')))


def ots_seed_jar_transfer_seed_in(
    seed: ots_handle_t | _CDataBase,
    name: str
) -> ots_result_t:
    """
    Transfers a seed into the seed jar with the specified name.

    :param seed: The seed handle to transfer in.
    :param name: The name to associate with the seed.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(seed, (ots_handle_t, _CDataBase)), "seed must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed).type) == HandleType.SEED, "seed must be of type HandleType.SEED"
    assert isinstance(name, str), "name must be a string"
    return ots_result_t(lib.ots_seed_jar_transfer_seed_in(_unwrap(seed), name.encode('utf-8')))


def ots_seed_jar_transfer_seed_out(seed: ots_result_t | _CDataBase) -> ots_result_t:
    """
    Transfers a seed out of the seed jar.

    :param seed: The result of the seed operation to transfer out.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(seed, (ots_result_t, _CDataBase)), "seed must be an instance of ots_result_t or _CDataBase"
    return ots_result_t(lib.ots_seed_jar_transfer_seed_out(_unwrap(seed)))


def ots_seed_jar_transfer_seed_out_for_index(index: int) -> ots_result_t:
    """
    Transfers a seed out of the seed jar based on its index.

    :param index: The index of the seed to transfer out.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_transfer_seed_out_for_index(index))


def ots_seed_jar_transfer_seed_out_for_name(name: str) -> ots_result_t:
    """
    Transfers a seed out of the seed jar based on its name.

    :param name: The name of the seed to transfer out.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(name, str), "name must be a string"
    return ots_result_t(lib.ots_seed_jar_transfer_seed_out_for_name(name.encode('utf-8')))


def ots_seed_jar_transfer_seed_out_for_fingerprint(fingerprint: str) -> ots_result_t:
    """
    Transfers a seed out of the seed jar based on its fingerprint.

    :param fingerprint: The fingerprint of the seed to transfer out.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(fingerprint, str), "fingerprint must be a string"
    return ots_result_t(lib.ots_seed_jar_transfer_seed_out_for_fingerprint(fingerprint.encode('utf-8')))


def ots_seed_jar_transfer_seed_out_for_address(address: str) -> ots_result_t:
    """
    Transfers a seed out of the seed jar based on its address.

    :param address: The address of the seed to transfer out.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_seed_jar_transfer_seed_out_for_address(address.encode('utf-8')))


def ots_seed_jar_clear() -> ots_result_t:
    """
    Clears all seeds from the seed jar.

    :return: ots_result_t indicating the result of the operation.
    """
    return ots_result_t(lib.ots_seed_jar_clear())


def ots_seed_jar_seeds() -> ots_result_t:
    """
    Returns all seeds in the seed jar.

    :return: ots_result_t containing the list of seeds.
    """
    return ots_result_t(lib.ots_seed_jar_seeds())


def ots_seed_jar_seed_count() -> ots_result_t:
    """
    Returns the count of seeds in the seed jar.

    :return: ots_result_t containing the count of seeds.
    """
    return ots_result_t(lib.ots_seed_jar_seed_count())


def ots_seed_jar_seed_for_index(index: int) -> ots_result_t:
    """
    Returns a seed from the seed jar based on its index.

    :param index: The index of the seed to retrieve.
    :return: ots_result_t containing the seed.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_seed_for_index(index))


def ots_seed_jar_seed_for_fingerprint(fingerprint: str) -> ots_result_t:
    """
    Returns a seed from the seed jar based on its fingerprint.

    :param fingerprint: The fingerprint of the seed to retrieve.
    :return: ots_result_t containing the seed.
    """
    assert isinstance(fingerprint, str), "fingerprint must be a string"
    return ots_result_t(lib.ots_seed_jar_seed_for_fingerprint(fingerprint.encode('utf-8')))


def ots_seed_jar_seed_for_address(address: str) -> ots_result_t:
    """
    Returns a seed from the seed jar based on its address.

    :param address: The address of the seed to retrieve.
    :return: ots_result_t containing the seed.
    """
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_seed_jar_seed_for_address(address.encode('utf-8')))


def ots_seed_jar_seed_for_name(name: str) -> ots_result_t:
    """
    Returns a seed from the seed jar based on its name.

    :param name: The name of the seed to retrieve.
    :return: ots_result_t containing the seed.
    """
    assert isinstance(name, str), "name must be a string"
    return ots_result_t(lib.ots_seed_jar_seed_for_name(name.encode('utf-8')))


def ots_seed_jar_seed_name(seed: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the name of the specified seed in the seed jar.

    :param seed: The handle of the seed.
    :return: ots_result_t containing the name of the seed.
    """
    assert isinstance(seed, (ots_handle_t, _CDataBase)), "seed must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed).type) == HandleType.SEED, "seed must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_jar_seed_name(_unwrap(seed)))


def ots_seed_jar_seed_rename(
    seed: ots_handle_t | _CDataBase,
    name: str
) -> ots_result_t:
    """
    Renames the specified seed in the seed jar.

    :param seed: The handle of the seed to rename.
    :param name: The new name for the seed.
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(seed, (ots_handle_t, _CDataBase)), "seed must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(seed).type) == HandleType.SEED, "seed must be of type HandleType.SEED"
    assert isinstance(name, str), "name must be a string"
    return ots_result_t(lib.ots_seed_jar_seed_rename(_unwrap(seed), name.encode('utf-8')))


def ots_seed_jar_item_name(index: int) -> ots_result_t:
    """
    Returns the name of the seed jar item at the specified index.

    :param index: The index of the seed jar item.
    :return: ots_result_t containing the name of the seed jar item.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_name(index))


def ots_seed_jar_item_fingerprint(index: int) -> ots_result_t:
    """
    Returns the fingerprint of the seed jar item at the specified index.

    :param index: The index of the seed jar item.
    :return: ots_result_t containing the fingerprint of the seed jar item.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_fingerprint(index))


def ots_seed_jar_item_address(index: int) -> ots_result_t:
    """
    Returns the address of the seed jar item at the specified index.

    :param index: The index of the seed jar item.
    :return: ots_result_t containing the address of the seed jar item.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_address(index))


def ots_seed_jar_item_address_string(index: int) -> ots_result_t:
    """
    Returns the address string of the seed jar item at the specified index.

    :param index: The index of the seed jar item.
    :return: ots_result_t containing the address string of the seed jar item.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_address_string(index))


def ots_seed_jar_item_seed_type(index: int) -> ots_result_t:
    """
    Returns the seed type of the seed jar item at the specified index.

    :param index: The index of the seed jar item.
    :return: ots_result_t containing the seed type of the seed jar item.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_seed_type(index))


def ots_seed_jar_item_seed_type_string(index: int) -> ots_result_t:
    """
    Returns the seed type string of the seed jar item at the specified index.

    :param index: The index of the seed jar item.
    :return: ots_result_t containing the seed type string of the seed jar item.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_seed_type_string(index))


def ots_seed_jar_item_is_legacy(index: int) -> ots_result_t:
    """
    Checks if the seed jar item at the specified index is a legacy item.

    :param index: The index of the seed jar item.
    :return: ots_result_t indicating whether the item is legacy.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_is_legacy(index))


def ots_seed_jar_item_network(index: int) -> ots_result_t:
    """
    Returns the network of the seed jar item at the specified index.

    :param index: The index of the seed jar item.
    :return: ots_result_t containing the network of the seed jar item.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_network(index))


def ots_seed_jar_item_network_string(index: int) -> ots_result_t:
    """
    Returns the network string of the seed jar item at the specified index.

    :param index: The index of the seed jar item.
    :return: ots_result_t containing the network string of the seed jar item.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_network_string(index))


def ots_seed_jar_item_height(index: int) -> ots_result_t:
    """
    Returns the height of the seed jar item at the specified index.

    :param index: The index of the seed jar item.
    :return: ots_result_t containing the height of the seed jar item.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_height(index))


def ots_seed_jar_item_timestamp(index: int) -> ots_result_t:
    """
    Returns the timestamp of the seed jar item at the specified index.

    :param index: The index of the seed jar item.
    :return: ots_result_t containing the timestamp of the seed jar item.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_timestamp(index))


def ots_seed_jar_item_wallet(index: int) -> ots_result_t:
    """
    Returns the wallet associated with the seed jar item at the specified index.

    :param index: The index of the seed jar item.
    :return: ots_result_t containing the wallet of the seed jar item.
    """
    assert isinstance(index, int), "index must be an integer"
    return ots_result_t(lib.ots_seed_jar_item_wallet(index))


def ots_version() -> ots_result_t:
    """
    Returns the version of the OTS library.
    """
    return ots_result_t(lib.ots_version())


def ots_version_components() -> ots_result_t:
    """
    Returns the version components of the OTS library.

    :return: ots_result_t contains tuple containing the major, minor, and patch version numbers.
    """
    return ots_result_t(lib.ots_version_components())


def ots_height_from_timestamp(
    timestamp: int,
    network: Network | int = Network.MAIN
) -> ots_result_t:
    """
    Returns the height corresponding to a given timestamp and network.

    :param timestamp: The timestamp to convert.
    :param network: The network for which to calculate the height.
    :return: ots_result_t containing the height.
    """
    assert isinstance(timestamp, int), "timestamp must be an integer"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    assert int(network) >= 0, "network must be a non-negative integer"
    return ots_result_t(lib.ots_height_from_timestamp(timestamp, int(network)))


def ots_timestamp_from_height(
    height: int,
    network: Network | int = Network.MAIN
) -> ots_result_t:
    """
    Returns the timestamp corresponding to a given height and network.

    :param height: The height to convert.
    :param network: The network for which to calculate the timestamp.
    :return: ots_result_t containing the timestamp.
    """
    assert isinstance(height, int), "height must be an integer"
    assert isinstance(network, (Network, int)), "network must be an instance of Network or an integer"
    assert int(network) >= 0, "network must be a non-negative integer"
    return ots_result_t(lib.ots_timestamp_from_height(height, int(network)))


def ots_random_bytes(size: int) -> ots_result_t:
    """
    Returns a random byte string of the specified size.

    :param size: The number of random bytes to generate.
    :return: A byte string containing the random bytes.
    """
    assert isinstance(size, int), "size must be an integer"
    assert size > 0, "size must be a positive integer"
    return ots_result_t(lib.ots_random_bytes(size))


def ots_random_32() -> ots_result_t:
    """
    Returns a random 32-byte string.
    """
    return ots_result_t(lib.ots_random_32())


def ots_check_low_entropy(
    data: bytes,
    min_entropy: float
) -> ots_result_t:
    """
    Checks if the provided data has low entropy.

    :param data: The data to check.
    :param size: The size of the data in bytes.
    :param min_entropy: The minimum entropy level to consider.
    :return: ots_result_t indicating whether the data has low entropy.
    """
    assert isinstance(data, bytes), "data must be a bytes object"
    assert isinstance(size, int), "size must be an integer"
    assert size > 0, "size must be a positive integer"
    assert isinstance(min_entropy, float), "min_entropy must be a float"
    return ots_result_t(lib.ots_check_low_entropy(data, len(data), min_entropy))


def ots_entropy_level(data: bytes) -> ots_result_t:
    """
    Returns the entropy level of the provided data.

    :param data: The data to analyze.
    :return: ots_result_t containing the entropy level.
    """
    assert isinstance(data, bytes), "data must be a bytes object"
    return ots_result_t(lib.ots_entropy_level(data), len(data))


def ots_set_enforce_entropy(enforce: bool) -> None:
    """
    Sets whether to enforce entropy checks.

    :param enforce: A boolean indicating whether to enforce entropy checks.
    """
    assert isinstance(enforce, bool), "enforce must be a boolean"
    lib.ots_set_enforce_entropy(enforce)


def ots_set_enforce_entropy_level(level: float) -> None:
    """
    Sets the minimum entropy level for checks.

    :param level: The minimum entropy level to enforce.
    """
    assert isinstance(level, float), "level must be a float"
    lib.ots_set_enforce_entropy_level(level)


def ots_set_max_account_depth(depth: int) -> None:
    """
    Sets the maximum account depth.

    :param depth: The maximum account depth to set.
    """
    assert isinstance(depth, int), "depth must be an integer"
    assert depth >= 0, "depth must be a non-negative integer"
    lib.ots_set_max_account_depth(depth)


def ots_set_max_index_depth(depth: int) -> None:
    """
    Sets the maximum index depth.

    :param depth: The maximum index depth to set.
    """
    assert isinstance(depth, int), "depth must be an integer"
    assert depth >= 0, "depth must be a non-negative integer"
    lib.ots_set_max_index_depth(depth)


def ots_set_max_depth(account_depth: int, index_depth: int) -> None:
    """
    Sets the maximum account and index depth.

    :param account_depth: The maximum account depth to set.
    :param index_depth: The maximum index depth to set.
    """
    assert isinstance(account_depth, int), "account_depth must be an integer"
    assert account_depth >= 0, "account_depth must be a non-negative integer"
    assert isinstance(index_depth, int), "index_depth must be an integer"
    assert index_depth >= 0, "index_depth must be a non-negative integer"
    lib.ots_set_max_depth(account_depth, index_depth)


def ots_reset_max_depth() -> None:
    """
    Resets the maximum account and index depth to their default values.
    """
    lib.ots_reset_max_depth()


def ots_get_max_account_depth(depth: int) -> int:
    """
    Returns the maximum account depth.

    :param depth: The current account depth.
    :return: An integer representing the maximum account depth.
    """
    assert isinstance(depth, int), "depth must be an integer"
    return lib.ots_get_max_account_depth(depth)


def ots_get_max_index_depth(depth: int) -> int:
    """
    Returns the maximum index depth.

    :param depth: The current index depth.
    :return: An integer representing the maximum index depth.
    """
    assert isinstance(depth, int), "depth must be an integer"
    return lib.ots_get_max_index_depth(depth)


def ots_verify_data(
    data: str,
    address: str,
    signature: str
) -> ots_result_t:
    """
    Verifies the provided data against the given address and signature.

    :param data: The data to verify.
    :param address: The address to verify against.
    :param signature: The signature to verify.
    :return: ots_result_t indicating the result of the verification.
    """
    assert isinstance(data, str), "data must be a string"
    assert isinstance(address, str), "address must be a string"
    assert isinstance(signature, str), "signature must be a string"
    return ots_result_t(lib.ots_verify_data(data.encode('utf-8'), address.encode('utf-8'), signature.encode('utf-8')))
