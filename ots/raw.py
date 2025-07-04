from _cffi_backend import _CDataBase
from ._ots import ffi, lib
from .enums import *

REQUIRE__OTS_RESULT_T__OR__CDATA_BASE = "result must be a valid ots_result_t or _CDataBase object"
REQUIRE__OTS_HANDLE_T__OR__CDATA_BASE = "handle must be a valid ots_handle_t or _CDataBase object"


class _opaque_handle_t:
    """
    Base class for opaque handles for results and handles in OTS.

    .. attention::

        Do not instantiate this class directly!

    """

    @property
    def ptr(self) -> _CDataBase:
        """
        Returns the pointer to the underlying C data type.
        Used for almost all operations.

        :return: The pointer to the C data type.
        """
        return self.ptrptr[0]

    @property
    def cType(self) -> str:
        """
        Returns the type of the ptr as a string.
        Can be used to distinguish between different types of handles.

        :return: The type of the ptr as a string.
        """
        return ffi.typeof(self.ptrptr[0]).cname


class ots_result_t(_opaque_handle_t):
    """
    Represents the result of an OTS operation.
    Internally it wraps the C ABI ots_result_t struct in a pointer of a pointer type,
    so it can be reasonably freed when the object is deleted.
    """

    def __init__(self, result: _CDataBase):
        """
        Initializes the ots_result_t with a C data type.
        It must be of type ots_result_t *.
        """
        assert ffi.typeof(result) == ffi.typeof('ots_result_t *'), "result must be of type ots_result_t *"
        self.ptrptr: _CDataBase = ffi.new('ots_result_t **')
        """
        The pointer to the pointer to be able to free the result.

        .. hint::

            No need to do anything to free the result, then delete the object,
            or let it go out of scope and gc will take care of it.

        """
        self.ptrptr[0] = result

    def __del__(self):
        """
        Frees the underlying C data type before the object is deleted.
        """
        if self.ptrptr:
            lib.ots_free_result(self.ptrptr)
            ffi.release(self.ptrptr)


class ots_handle_t(_opaque_handle_t):
    """
    Represents a handle to an OTS object.
    Internally it wraps the C ABI ots_handle_t struct in a pointer of a pointer type,
    so it can be reasonably freed when the object is deleted.
    """

    def __init__(self, handle: _CDataBase, reference: bool = False):
        """
        Initializes the ots_handle_t with a C data type.
        It must be of type ots_handle_t *.
        """
        assert ffi.typeof(handle) == ffi.typeof('ots_handle_t *'), "handle must be of type ots_handle_t *"
        self.ptrptr: _CDataBase = ffi.new('ots_handle_t **')
        """
        The pointer to the pointer to be able to free the handle.

        .. hint::

            No need to do anything to free the handle, then delete the object,
            or let it go out of scope and gc will take care of it.

        """
        self.ptrptr[0] = handle
        self.reference: bool = reference
        """
        Indicates if the handle is a reference. A reference must not free the underlying
        C data type when the object is deleted. But no worry, it is taken care of it
        automatically by the wrapper and the library.
        """

    def __del__(self):
        """
        Frees the underlying C data type when the object is deleted.
        """
        if self.ptrptr:
            if not self.reference:
                lib.ots_free_handle(self.ptrptr)
            ffi.release(self.ptrptr)

    @property
    def type(self) -> HandleType:
        """
        Returns the type of the handle as a HandleType enum.
        """
        return HandleType(self.ptr.type)

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
    :type value: _CDataBase | ots_result_t | ots_handle_t
    :return: The C data type representation of the value.
    """
    assert isinstance(value, (_CDataBase, ots_result_t, ots_handle_t)), "value must be an instance of _CDataBase, ots_result_t or ots_handle_t"
    assert isinstance(value, (ots_result_t, ots_handle_t)) or ffi.typeof(value) in (ffi.typeof('ots_result_t *'), ffi.typeof('ots_handle_t *')), "value must be of type ots_result_t * or ots_handle_t *"
    if isinstance(value, _opaque_handle_t):
        return value.ptr
    return value


def _is_handle(handle: ots_handle_t | _CDataBase | None) -> bool:
    """
    Checks if the given handle is a valid ots_handle_t or `ots_handle_t *` _CDataBase object. Accepts None to not raise an error and return simply silently False.

    :param handle: The handle to check.
    :type handle: ots_handle_t | _CDataBase | None
    :return: True if the handle is valid, False otherwise.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase, type(None))), "handle must be an instance of ots_handle_t or _CDataBase or None"
    if (
        isinstance(handle, ots_handle_t)
        and handle.cType == 'ots_handle_t *'
        and handle.ptr != ffi.NULL
    ):
        return True
    if isinstance(handle, _CDataBase):
        return ffi.typeof(handle) == ffi.typeof('ots_handle_t *') and handle != ffi.NULL
    return False


def _is_result(result: ots_result_t | _CDataBase | None) -> bool:
    """
    Checks if the given result is a valid ots_result_t or `ots_result_t *` _CDataBase object. Accepts None to not raise an error and return simply silently False.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase | None
    :return: True if the result is valid, False otherwise.
    """
    if isinstance(result, ots_result_t):
        return result.cType == 'ots_result_t *' and result.ptr != ffi.NULL
    if isinstance(result, _CDataBase):
        return ffi.typeof(result) == ffi.typeof('ots_result_t *') and result != ffi.NULL
    return False


def _raise_on_error(result: ots_result_t | _CDataBase) -> None:
    """
    Raises an exception if the result indicates an error.
    Uses Internally :py:func:`ots_is_error` to check for errors.

    :param result: The result to check for errors.
    :type result: ots_result_t | _CDataBase
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
    :type handle: ots_handle_t | _CDataBase
    :param handle_type: The expected type of the handle.
    :type handle_type: HandleType | int
    :return: True if the handle is valid, False otherwise.
    """
    assert isinstance(handle_type, HandleType) or isinstance(handle_type, int), "handle_type must be an instance of HandleType or an integer"
    assert _is_handle(handle), REQUIRE__OTS_HANDLE_T__OR__CDATA_BASE
    return lib.ots_handle_valid(ffi.cast('ots_handle_t*', _unwrap(handle)), int(handle_type))


def ots_is_error(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result indicates an error.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is an error, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_is_error(_unwrap(result))


def ots_error_message(result: ots_result_t | _CDataBase) -> str | None:
    """
    Returns the error message from the result.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: The error message as a string, or None if there is no error.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    out = lib.ots_result_string(_unwrap(result))
    return ffi.string(out).decode('utf-8') if out != ffi.NULL else None

def ots_error_class(result: ots_result_t | _CDataBase) -> str | None:
    """
    Returns the error class from the result.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: The error class as a string, or None if there is no error.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    out = lib.ots_error_class(_unwrap(result))
    return ffi.string(out).decode('utf-8') if out != ffi.NULL else None


def ots_error_code(result: ots_result_t | _CDataBase) -> int:
    """
    Returns the error code from the result.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: The error code as an integer, or 0 if there is no error.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_error_code(_unwrap(result))


def ots_is_result(result: ots_result_t | _CDataBase | None) -> bool:
    """
    Checks if the given result is a valid result object. None is accepted to not raise an error.
    This function returns also `False` if there is a valid ots_result_t* struct, but the ots_result_t.error.code is not 0, in this case :py:func:`ots_is_error` will return `True`.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase | None
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

    .. hint::

        Better use the direct functions like:

        - :py:func:`ots_result_is_wipeable_string`

        - :py:func:`ots_result_is_seed_indices`

        - :py:func:`ots_result_is_seed_language`

        - :py:func:`ots_result_is_address`

        - :py:func:`ots_result_is_seed`

        - :py:func:`ots_result_is_wallet`

        - :py:func:`ots_result_is_transaction_description`

        - :py:func:`ots_result_is_transaction_warning`

        - :py:func:`ots_result_is_string`

        - :py:func:`ots_result_is_boolean`

        - :py:func:`ots_result_is_number`

        - :py:func:`ots_result_is_comparison`

        - :py:func:`ots_result_is_array`

        - ots_result_data_is...

        - ots_result_data_handle_is...

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is of the specified type, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert isinstance(result_type, ResultType) or isinstance(result_type, int), "result_type must be an instance of ResultType or an integer"
    return lib.ots_result_is_type(_unwrap(result), int(result_type))


def ots_result_is_handle(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a handle.

    .. hint::

        Better use the direct functions.

        .. seealso:: :py:func:`ots_result_is_type`

    Retrieve the handle with :py:func:`ots_result_handle` if it is a handle.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is a handle, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_handle(_unwrap(result))


def ots_result_is_wipeable_string(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a wipeable string handle.
    Retrieve the wipeable string handle simply with :py:func:`ots_result_handle` if it is a wipeable string, like:

    .. code-block:: python

        ws: ots_handle_t = ots_result_handle(result)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is a wipeable string, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_wipeable_string(_unwrap(result))


def ots_result_is_seed_indices(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a seed indices handle.
    Retrieve the seed indices handle simply with :py:func:`ots_result_handle` if it is a seed indices, like:

    .. code-block:: python

        indices: ots_handle_t = ots_result_handle(result)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is a seed indices, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_seed_indices(_unwrap(result))


def ots_result_is_seed_language(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a seed language handle.
    Retrieve the seed language handle simply with :py:func:`ots_result_handle` if it is a seed language, like:

    .. code-block:: python

        language: ots_handle_t = ots_result_handle(result)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is a seed language, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_seed_language(_unwrap(result))


def ots_result_is_address(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is an address handle.
    Retrieve the address handle simply with :py:func:`ots_result_handle` if it is an address, like:

    .. code-block:: python

        address: ots_handle_t = ots_result_handle(result)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is an address, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_address(ffi.cast('ots_result_t*', _unwrap(result)))


def ots_result_is_seed(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a seed handle.
    Retrieve the seed handle simply with :py:func:`ots_result_handle` if it is a seed, like:

    .. code-block:: python

        seed: ots_handle_t = ots_result_handle(result)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is a seed, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_seed(_unwrap(result))


def ots_result_is_wallet(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a wallet handle.
    Retrieve the wallet handle simply with :py:func:`ots_result_handle` if it is a wallet, like:

    .. code-block:: python

        wallet: ots_handle_t = ots_result_handle(result)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is a wallet, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_wallet(_unwrap(result))


# TODO: something seems to be off, what is a transaction handle? Hidden until investigation is done.
def ots_result_is_transaction(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a transaction handle.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is a transaction, False otherwise.
    :meta private:
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_transaction(_unwrap(result))


def ots_result_is_transaction_description(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a transaction description handle.
    Retrieve the transaction description handle simply with :py:func:`ots_result_handle` if it is a transaction description, like:

    .. code-block:: python

        tx_description: ots_handle_t = ots_result_handle(result)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is a transaction description, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_transaction_description(_unwrap(result))


def ots_result_is_transaction_warning(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a transaction warning handle.
    Retrieve the transaction warning handle simply with :py:func:`ots_result_handle` if it is a transaction warning, like:

    .. code-block:: python

        tx_warning: ots_handle_t = ots_result_handle(result)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is a transaction warning, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_transaction_warning(_unwrap(result))


def ots_result_is_string(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a string.
    Retrieve the string simply with :py:func:`ots_result_string` if it is a string, like:

    .. code-block:: python

        string: str | None = ots_result_string(result)

        # if checked before with `ots_result_is_string`
        # no need to check for None
        string: str = ots_result_string(result)

    .. note::

        Avoid :py:func:`ots_result_string_copy` to avoid double copying the
        string as CFFI anyways copies the string.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is a string, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_string(_unwrap(result))


def ots_result_is_boolean(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a boolean.
    Retrieve the boolean simply with :py:func:`ots_result_boolean` if it is a boolean, like:

    .. code-block:: python

        boolean: bool = ots_result_boolean(result)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is a boolean, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_boolean(_unwrap(result))


def ots_result_is_number(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a (unsigned) number.
    Retrieve the number simply with :py:func:`ots_result_number` if it is a number, like:

    .. code-block:: python

        number: int = ots_result_number(result)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
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

    .. hint::

        Better use the direct functions like:

        - `ots_result_data_is_...`

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :param data_type: The expected type of the result data.
    :type data_type: DataType | int
    :return: True if the result data is of the specified type, False otherwise.
    """
    assert isinstance(data_type, DataType) or isinstance(data_type, int), "data_type must be an instance of DataType or an integer"
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_type(_unwrap(result), int(data_type))


def ots_result_data_is_reference(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is a reference.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result data is a reference, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_reference(_unwrap(result))


def ots_result_data_is_int(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is an integer.
    Retrieve the integer simply with :py:func:`ots_result_int_array` or :py:func:`ots_result_int_array_reference` if it is an integer array, like:

    .. code-block:: python

        int_value: list[int] = ots_result_int_array(result)

        # or

        int_value: list[int] = ots_result_int_array_reference(result)

    It is also possible to get the entries one by one with :py:func:`ots_result_array_get_int` if it is an integer array, like:

    .. code-block:: python

        for i in range(ots_result_size(result)):
            int_value: int = ots_result_array_get_int(result, i)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result data is an integer, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_int(_unwrap(result))


def ots_result_data_is_char(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is a character.
    Retrieve the character simply with :py:func:`ots_result_char_array` or :py:func:`ots_result_char_array_reference` if it is a character array, like:

    .. code-block:: python

        chars: bytes = ots_result_char_array(result)

    Or as uint8 values:

    .. code-block:: python

        chars: list[int] = ots_result_char_array_uint8(result)

    Or as a single character with :py:func:`ots_result_array_get_char` and :py:func:`ots_result_array_get_uint8` if it is a character array, like:

    .. code-block:: python

        for i in range(ots_result_size(result)):
            char: bytes = ots_result_array_get_char(result, i)

        # or

        for i in range(ots_result_size(result)):
            char: int = ots_result_array_get_uint8(result, i)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result data is a character, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_char(_unwrap(result))


def ots_result_data_is_uint8(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is an unsigned 8-bit integer.
    Retrieve the unsigned 8-bit integer simply with :py:func:`ots_result_uint8_array` or :py:func:`ots_result_uint8_array_reference` if it is an unsigned 8-bit integer array. Or as a single unsigned 8-bit integer with :py:func:`ots_result_array_get_uint8` if it is an unsigned 8-bit integer array.

    .. seealso:: :py:func:`ots_result_data_is_char`

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result data is an unsigned 8-bit integer, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_uint8(_unwrap(result))


def ots_result_data_is_uint16(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is an unsigned 16-bit integer.
    Retrieve the unsigned 16-bit integer simply with :py:func:`ots_result_uint16_array` or :py:func:`ots_result_uint16_array_reference` if it is an unsigned 16-bit integer array, like:

    .. code-block:: python

        uint16_values: list[int] = ots_result_uint16_array(result)

        #or

        uint16_values: list[int] = ots_result_uint16_array_reference(result)

    Or as a single unsigned 16-bit integer with :py:func:`ots_result_array_get_uint16` if it is an unsigned 16-bit integer array, like:

    .. code-block:: python

        for i in range(ots_result_size(result)):
            uint16_value: int = ots_result_array_get_uint16(result, i)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result data is an unsigned 16-bit integer, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_uint16(_unwrap(result))


def ots_result_data_is_uint32(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is an unsigned 32-bit integer.
    Retrieve the unsigned 32-bit integer simply with :py:func:`ots_result_uint32_array` or :py:func:`ots_result_uint32_array_reference` if it is an unsigned 32-bit integer array, like:

    .. code-block:: python

        uint32_values: list[int] = ots_result_uint32_array(result)

        # or

        uint32_values: list[int] = ots_result_uint32_array_reference(result)

    Or as a single unsigned 32-bit integer with :py:func:`ots_result_array_get_uint32` if it is an unsigned 32-bit integer array, like:

    .. code-block:: python

        for i in range(ots_result_size(result)):
            uint32_value: int = ots_result_array_get_uint32(result, i)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result data is an unsigned 32-bit integer, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_uint32(_unwrap(result))


def ots_result_data_is_uint64(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is an unsigned 64-bit integer.
    Retrieve the unsigned 64-bit integer simply with :py:func:`ots_result_uint64_array` or :py:func:`ots_result_uint64_array_reference` if it is an unsigned 64-bit integer array, like:

    .. code-block:: python

        uint64_values: list[int] = ots_result_uint64_array(result)

        # or

        uint64_values: list[int] = ots_result_uint64_array_reference(result)

    Or as a single unsigned 64-bit integer with :py:func:`ots_result_array_get_uint64` if it is an unsigned 64-bit integer array, like:

    .. code-block:: python

        for i in range(ots_result_size(result)):
            uint64_value: int = ots_result_array_get_uint64(result, i)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result data is an unsigned 64-bit integer, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_uint64(_unwrap(result))


def ots_result_data_is_handle(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data is a handle.
    Retrieve the handle simply with :py:func:`ots_result_handle_array` or :py:func:`ots_result_handle_array_reference` if it is a handle array, like:

    .. code-block:: python

        handles: list[ots_handle_t] = ots_result_handle_array(result)

        # or

        handles: list[ots_handle_t] = ots_result_handle_array_reference(result)

    Or as a single handle with :py:func:`ots_result_array_get_handle` if it is a handle array, like:

    .. code-block:: python

        for i in range(ots_result_size(result)):
            handle: ots_handle_t = ots_result_array_get_handle(result, i)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result data is a handle, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_is_handle(_unwrap(result))


def ots_result_data_handle_is_type(
    result: ots_result_t | _CDataBase,
    handle_type: HandleType | int
) -> bool:
    """
    Checks if the result data handle is of a specific type.

    .. hint::

        Better use the direct functions like:

        - `ots_result_data_handle_is_...`

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :param handle_type: The expected type of the handle.
    :type handle_type: HandleType | int
    :return: True if the handle is of the specified type, False otherwise.
    """
    assert isinstance(handle_type, HandleType) or isinstance(handle_type, int), "handle_type must be an instance of HandleType or an integer"
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_type(_unwrap(result), int(handle_type))


def ots_result_data_handle_is_reference(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is a reference.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the handle is a reference, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_reference(_unwrap(result))


def ots_result_data_handle_is_wipeable_string(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is a wipeable string.
    Retrieve the wipeable string handle simply with :py:func:`ots_result_handle_array` or :py:func:`ots_result_handle_array_reference` if it is a wipeable string handle array, like:

    .. code-block:: python

        wipeable_strings: list[ots_handle_t] = ots_result_handle_array(result)

        # or

        wipeable_strings: list[ots_handle_t] = ots_result_handle_array_reference(result)

    Or as a single wipeable string handle with :py:func:`ots_result_array_get_handle` if it is a wipeable string handle array, like:

    .. code-block:: python

        for i in range(ots_result_size(result)):
            wipeable_string: ots_handle_t = ots_result_array_get_handle(result, i)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the handle is a wipeable string, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_wipeable_string(_unwrap(result))


def ots_result_data_handle_is_seed_indices(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is seed indices.

    .. seealso:: How to retrieve the handles:

        :py:func:`ots_result_data_is_handle`

        and

        :py:func:`ots_result_data_handle_is_wipeable_string`

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

    .. seealso:: How to retrieve the handles:

        :py:func:`ots_result_data_is_handle`

        and

        :py:func:`ots_result_data_handle_is_wipeable_string`


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

    .. seealso:: How to retrieve the handles:

        :py:func:`ots_result_data_is_handle`

        and

        :py:func:`ots_result_data_handle_is_wipeable_string`


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

    .. seealso:: How to retrieve the handles:

        :py:func:`ots_result_data_is_handle`

        and

        :py:func:`ots_result_data_handle_is_wipeable_string`


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

    .. seealso:: How to retrieve the handles:

        :py:func:`ots_result_data_is_handle`

        and

        :py:func:`ots_result_data_handle_is_wipeable_string`


    :param result: The result to check.
    :return: True if the handle is a wallet, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_wallet(_unwrap(result))


# TODO: something seems to be off, what is a transaction handle? Hidden until investigation is done.
def ots_result_data_handle_is_transaction(
    result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result data handle is a transaction.

    .. seealso:: How to retrieve the handles:

        :py:func:`ots_result_data_is_handle`

        and

        :py:func:`ots_result_data_handle_is_wipeable_string`


    :param result: The result to check.
    :return: True if the handle is a transaction, False otherwise.
    :meta private:
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_transaction(_unwrap(result))


def ots_result_data_handle_is_transaction_description(
    result: ots_result_t | _CDataBase
) -> bool:
    """
    Checks if the result data handle is a transaction description.

    .. seealso:: How to retrieve the handles:

        :py:func:`ots_result_data_is_handle`

        and

        :py:func:`ots_result_data_handle_is_wipeable_string`


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

    .. seealso:: How to retrieve the handles:

        :py:func:`ots_result_data_is_handle`

        and

        :py:func:`ots_result_data_handle_is_wipeable_string`


    :param result: The result to check.
    :return: True if the handle is a transaction warning, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_data_handle_is_transaction_warning(_unwrap(result))


def ots_result_handle(result: ots_result_t | _CDataBase) -> ots_handle_t:
    """
    Returns the handle from the result.

    .. code-block:: python

        handle: ots_handle_t = ots_result_handle(result)

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

    .. hint::

        Better use the direct functions like:

        - `ots_result_handle_is_...`

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :param type: The expected type of the handle.
    :type type: HandleType | int
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

    .. code-block:: python

        string: str | None = ots_result_string(result)

        # if checked before with `ots_result_is_string`
        # no need to check for None
        string: str = ots_result_string(result)

    :param result: The result to get the string from.
    :result: ots_result_t | _CDataBase
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

    .. warning::

        This function copies the string, which is not necessary in Python as CFFI already does this. Do not use, use instead :py:func:`ots_result_string`.

    :param result: The result to get the string from.
    :type result: ots_result_t | _CDataBase
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

    .. code-block:: python

        boolean: bool = ots_result_boolean(result)

    :param result: The result to get the boolean from.
    :type result: ots_result_t | _CDataBase
    :param default_value: The default value to return if the result is not a boolean.
    :type default_value: bool
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

    .. code-block:: python

        number: int = ots_result_number(result)

    :param result: The result to get the number from.
    :type result: ots_result_t | _CDataBase
    :param default_value: The default value to return if the result is not a number. By default it is -1 which can not be returned by the C function how it is unsigned.
    :type default_value: int
    :return: The number as an integer, or the default value if the result is not a number.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_number(_unwrap(result), default_value)


def ots_result_array(
    result: ots_result_t | _CDataBase
) -> _CDataBase:
    """
    Returns the array from the result.

    .. hint::

        No need to use, use simply the dedicated functions like:

        - `ots_result_handle_array`

        - `ots_result_int_array`

        - `ots_result_char_array`

        and so on.

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

    .. hint::

        No need to use, use simply the dedicated functions like:

        - `ots_result_array_get_handle`

        - `ots_result_array_get_int`

        - `ots_result_array_get_char`

        and so on.

    :param result: The result to get the element from.
    :type result: ots_result_t | _CDataBase
    :param int index: The index of the element to retrieve.
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

    .. code-block:: python

        handle: ots_handle_t = ots_result_array_get_handle(result, index)

    :param result: The result to get the handle from.
    :type result: ots_result_t | _CDataBase
    :param int index: The index of the handle to retrieve.
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

    .. code-block:: python

        int_value: int = ots_result_array_get_int(result, index)

    :param result: The result to get the integer from.
    :type result: ots_result_t | _CDataBase
    :param int index: The index of the integer to retrieve.
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

    .. code-block:: python

        char: bytes = ots_result_array_get_char(result, index)

    :param result: The result to get the character from.
    :param index: The index of the character to retrieve.
    :return: The character at the specified index, or None if the index is out of bounds.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_size(result) > index >= 0, "index out of bounds"
    assert ots_result_data_is_char(result), "result array must be of char type"
    return ffi.unpack(lib.ots_result_array_get_char(_unwrap(result), index))


def ots_result_array_get_uint8(
    result: ots_result_t | _CDataBase,
    index: int
) -> int:
    """
    Returns the unsigned 8-bit integer at the specified index from the result array.

    .. code-block:: python

        uint8_value: int = ots_result_array_get_uint8(result, index)

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

    .. code-block:: python

        uint16_value: int = ots_result_array_get_uint16(result, index)

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

    .. code-block:: python

        uint32_value: int = ots_result_array_get_uint32(result, index)

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

    .. code-block:: python

        uint64_value: int = ots_result_array_get_uint64(result, index)

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

    .. hint::

        No need to use, use simply the dedicated functions instead.

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

    .. code-block:: python

        handles: list[ots_handle_t] = ots_result_handle_array_reference(result)

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

    .. code-block:: python

        int_values: list[int] = ots_result_int_array_reference(result)

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

    .. code-block:: python

        char_array: bytes = ots_result_char_array_reference(result)

    :param result: The result to get the character array reference from.
    :return: bytes representing the character array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_char(result) or ots_result_data_is_uint8(result), "result array must be of char or uint8 type"
    return ffi.unpack(ffi.cast('char*', lib.ots_result_uint8_array_reference(_unwrap(result))), ots_result_size(result))


def ots_result_uint8_array_reference(
    result: ots_result_t | _CDataBase
) -> list[int]:
    """
    Returns a reference to the array of unsigned 8-bit integers from the result.

    .. code-block:: python

        uint8_values: list[int] = ots_result_uint8_array_reference(result)

    :param result: The result to get the unsigned 8-bit integer array reference from.
    :return: A list of unsigned 8-bit integers representing the unsigned 8-bit integer array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint8(result), "result array must be of uint8 type"
    return [
        int(i) for i in ffi.from_buffer(
            'uint8_t[]',
            ffi.buffer(
                lib.ots_result_uint8_array_reference(_unwrap(result)),
                ots_result_size(result)
            )
        )
    ]


def ots_result_uint16_array_reference(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a reference to the array of unsigned 16-bit integers from the result.

    .. code-block:: python

        uint16_values: list[int] = ots_result_uint16_array_reference(result)

    :param result: The result to get the unsigned 16-bit integer array reference from.
    :return: A list of unsigned 16-bit integers representing the unsigned 16-bit integer array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint16(result), "result array must be of uint16 type"
    return [
        int(i) for i in ffi.from_buffer(
            'uint16_t[]',
            ffi.buffer(
                lib.ots_result_uint16_array_reference(_unwrap(result)),
                ots_result_size(result) * ffi.sizeof('uint16_t')
            )
        )
    ]


def ots_result_uint32_array_reference(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a reference to the array of unsigned 32-bit integers from the result.

    .. code-block:: python

        uint32_values: list[int] = ots_result_uint32_array_reference(result)

    :param result: The result to get the unsigned 32-bit integer array reference from.
    :return: A list of unsigned 32-bit integers representing the unsigned 32-bit integer array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint32(result), "result array must be of uint32 type"
    return [
        int(i) for i in ffi.from_buffer(
            'uint32_t[]',
            ffi.buffer(
                lib.ots_result_uint32_array_reference(_unwrap(result)),
                ots_result_size(result) * ffi.sizeof('uint32_t')
            )
        )
    ]


def ots_result_uint64_array_reference(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a reference to the array of unsigned 64-bit integers from the result.

    .. code-block:: python

        uint64_values: list[int] = ots_result_uint64_array_reference(result)

    :param result: The result to get the unsigned 64-bit integer array reference from.
    :return: A list of unsigned 64-bit integers representing the unsigned 64-bit integer array reference.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint64(result), "result array must be of uint64 type"
    return [
        int(i) for i in ffi.from_buffer(
            'uint64_t[]',
            ffi.buffer(
                lib.ots_result_uint64_array_reference(_unwrap(result)),
                ots_result_size(result) * ffi.sizeof('uint64_t')
            )
        )
    ]


def ots_result_handle_array(result: ots_result_t | _CDataBase) -> list[ots_handle_t]:
    """
    Returns a list of handles from the result array.

    .. code-block:: python

        handles: list[ots_handle_t] = ots_result_handle_array(result)

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

    .. code-block:: python

        int_values: list[int] = ots_result_int_array(result)

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

    .. code-block:: python

        char_array: bytes = ots_result_char_array(result)

    :param result: The result to get the character array from.
    :return: A byte string representing the character array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_char(result) or ots_result_data_is_uint8(result), "result array must be of char or uint8 type"
    handle = lib.ots_result_char_array(_unwrap(result))
    return ffi.unpack(handle, ots_result_size(result))


def ots_result_uint8_array(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a list of unsigned 8-bit integers from the result array.

    .. code-block:: python

        uint8_values: list[int] = ots_result_uint8_array(result)

    :param result: The result to get the unsigned 8-bit integers from.
    :return: A list of unsigned 8-bit integers representing the unsigned 8-bit integers in the result array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint8(result), "result array must be of uint8 type"
    return [
        int(i) for i in ffi.from_buffer(
            'uint8_t[]',
            ffi.buffer(
                lib.ots_result_uint8_array_reference(_unwrap(result)),
                ots_result_size(result)
            )
        )
    ]


def ots_result_uint16_array(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a list of unsigned 16-bit integers from the result array.

    .. code-block:: python

        uint16_values: list[int] = ots_result_uint16_array(result)

    :param result: The result to get the unsigned 16-bit integers from.
    :return: A list of unsigned 16-bit integers representing the unsigned 16-bit integers in the result array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint16(result), "result array must be of uint16 type"
    return [
        int(i) for i in ffi.from_buffer(
            'uint16_t[]',
            ffi.buffer(
                lib.ots_result_uint16_array_reference(_unwrap(result)),
                ots_result_size(result) * ffi.sizeof('uint16_t')
            )
        )
    ]


def ots_result_uint32_array(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a list of unsigned 32-bit integers from the result array.

    .. code-block:: python

        uint32_values: list[int] = ots_result_uint32_array(result)

    :param result: The result to get the unsigned 32-bit integers from.
    :return: A list of unsigned 32-bit integers representing the unsigned 32-bit integers in the result array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint32(result), "result array must be of uint32 type"
    return [
        int(i) for i in ffi.from_buffer(
            'uint32_t[]',
            ffi.buffer(
                lib.ots_result_uint32_array_reference(_unwrap(result)),
                ots_result_size(result) * ffi.sizeof('uint32_t')
            )
        )
    ]


def ots_result_uint64_array(result: ots_result_t | _CDataBase) -> list[int]:
    """
    Returns a list of unsigned 64-bit integers from the result array.

    .. code-block:: python

        uint64_values: list[int] = ots_result_uint64_array(result)

    :param result: The result to get the unsigned 64-bit integers from.
    :return: A list of unsigned 64-bit integers representing the unsigned 64-bit integers in the result array.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    assert ots_result_is_array(result), "result must be an array"
    assert ots_result_data_is_uint64(result), "result array must be of uint64 type"
    return [
        int(i) for i in ffi.from_buffer(
            'uint64_t[]',
            ffi.buffer(
                lib.ots_result_uint64_array_reference(_unwrap(result)),
                ots_result_size(result) * ffi.sizeof('uint64_t')
            )
        )
    ]


def ots_result_is_array(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is an array.

    .. hint::

        Check directly for what to expect in the array, like:

        - `ots_result_data_is_handle`

        - `ots_result_data_is_int`

        - `ots_result_data_is_char`

        - `ots_result_data_is_uint8`

        and so on.

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :return: True if the result is an array, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_array(_unwrap(result))


def ots_result_is_comparison(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a comparison result.
    To retrieve the comparison result, use :py:func:`ots_result_comparison`,
    or if only interested if the result is equal, use :py:func:`ots_result_is_equal`.
    Like:

    .. code-block:: python

        # is smaller than
        if ots_result_is_comparison(result) and ots_result_comparison(result) < 0:
        # is equal to
        if ots_result_is_comparison(result) and ots_result_is_equal(result):

    :param result: The result to check.
    :return: True if the result is a comparison result, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_comparison(_unwrap(result))


def ots_result_comparison(result: ots_result_t | _CDataBase) -> int:
    """
    Returns the comparison result.

    .. code-block:: python

        comparison: int = ots_result_comparison(result)

    :param result: The result to get the comparison from.
    :return: The comparison result as an integer.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_comparison(_unwrap(result))


def ots_result_is_equal(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is equal to another result.

    .. code-block:: python

        is_equal: bool = ots_result_is_equal(result)

    :param result: The result to check.
    :return: True if the result is equal, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_equal(_unwrap(result))


def ots_result_size(result: ots_result_t | _CDataBase) -> int:
    """
    Returns the size of the result if the result is an array or a string.

    .. code-block:: python

        size: int = ots_result_size(result)

    :param result: The result to get the size from.
    :return: The size of the result as an integer.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_size(_unwrap(result))


def ots_result_is_address_type(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is an address type.
    If the result is an address type, you can check the type of the address using
    :py:func:`ots_result_address_type_is_type`.

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

    .. code-block:: python

        is_type: bool = ots_result_address_type_is_type(result, AddressType.STANDARD)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :param type: The expected type of the address.
    :type type: AddressType | int
    :return: True if the address is of the specified type, False otherwise.
    """
    assert isinstance(type, AddressType) or isinstance(type, int), "type must be an instance of AddressType or an integer"
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_address_type_is_type(_unwrap(result), int(type))


def ots_result_is_address_index(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is an address index.
    If the result is an address index, you can retrieve the account and index using
    :py:func:`ots_result_address_index_account` and :py:func:`ots_result_address_index_index`.

    :param result: The result to check.
    :return: True if the result is an address index, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_address_index(_unwrap(result))


def ots_result_address_index_account(result: ots_result_t | _CDataBase) -> int:
    """
    Returns the account index from the result address index.

    .. code-block:: python

        account_index: int = ots_result_address_index_account(result)

    :param result: The result to get the account index from.
    :return: The account index as an integer.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_address_index_account(_unwrap(result))


def ots_result_address_index_index(result: ots_result_t | _CDataBase) -> int:
    """
    Returns the index from the result address index.

    .. code-block:: python

        index: int = ots_result_address_index_index(result)

    :param result: The result to get the index from.
    :return: The index as an integer.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_address_index_index(_unwrap(result))


def ots_result_is_network(result: ots_result_t | _CDataBase) -> bool:
    """
    Checks if the result is a network type.
    If the result is a network type, you can retrieve the network using
    :py:func:`ots_result_network` to get the network type or to check
    the network type using :py:func:`ots_result_network_is_type`.

    :param result: The result to check.
    :return: True if the result is a network type, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_network(_unwrap(result))


def ots_result_network(result: ots_result_t | _CDataBase) -> Network:
    """
    Returns the network from the result.

    .. code-block:: python

        network: Network = ots_result_network(result)

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

    .. code-block:: python

        is_type: bool = ots_result_network_is_type(result, Network.MAIN)

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
    If the result is a seed type, you can retrieve the seed type using
    :py:func:`ots_result_seed_type` or check the seed type using
    :py:func:`ots_result_seed_type_is_type`.

    :param result: The result to check.
    :return: True if the result is a seed type, False otherwise.
    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_is_seed_type(_unwrap(result))


def ots_result_seed_type(result: ots_result_t | _CDataBase) -> SeedType:
    """
    Returns the seed type from the result.

    .. code-block:: python

        seed_type: SeedType = ots_result_seed_type(result)

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

    .. code-block:: python

        is_type: bool = ots_result_seed_type_is_type(result, SeedType.MONERO)

    :param result: The result to check.
    :type result: ots_result_t | _CDataBase
    :param type: The expected type of the seed.
    :type type: SeedType | int
    :return: True if the seed is of the specified type, False otherwise.
    """
    assert isinstance(type, SeedType) or isinstance(type, int), "type must be an instance of OTS_SEED_TYPE or an integer"
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    return lib.ots_result_seed_type_is_type(_unwrap(result), int(type))


def ots_free_string(string: _CDataBase) -> None:
    """
    Frees a string allocated by OTS functions.

    :param _CDataBase string: The null terminated string to free.
    """
    assert isinstance(string, _CDataBase) and ffi.typeof(string) == ffi.typeof('char**'), "string must be a char**"
    lib.ots_free_string(ffi.cast('char**', string))


def ots_free_binary_string(string: _CDataBase, size: int) -> None:
    """
    Frees a binary string allocated by OTS functions.

    :param _CDataBase string: The binary string to free.
    :param int size: The size of the binary string.
    """
    assert isinstance(string, _CDataBase) and ffi.typeof(string) == ffi.typeof('char**'), "string must be a char**"
    lib.ots_free_binary_string(ffi.cast('char**', string), size)


def ots_free_array(arr: _CDataBase, elem_size: int, count: int) -> None:
    """
    Frees an array allocated by OTS functions.

    :param _CDataBase arr: The array to free.
    :param int elem_size: The size of each element in the array.
    :param int count: The number of elements in the array.
    """
    assert isinstance(arr, _CDataBase) and ffi.typeof(arr).cname.endswith('* *'), "arr must be a pointer to a pointer (void**)"
    lib.ots_free_array(ffi.cast('void**', arr), elem_size, count)


def ots_free_result(result: ots_result_t | _CDataBase) -> None:
    """
    Frees the result object returned by OTS functions.
    :param result: The result to free.
    :type result: ots_result_t | _CDataBase

    .. warning::

        Use `del result` instead of this function in Python if
        you are using it on a ots_result_t, to clean up all.

    """
    assert _is_result(result), REQUIRE__OTS_RESULT_T__OR__CDATA_BASE
    if isinstance(result, _CDataBase):
        assert ffi.typeof(result) == ffi.typeof('ots_result_t**'), "result must be a ots_result_t**"
        lib.ots_free_result(ffi.cast('ots_result_t**', _unwrap(result)))
        return
    del result


def ots_free_handle(handle: ots_handle_t | _CDataBase) -> None:
    """
    Frees the handle object returned by OTS functions.

    :param handle: The handle to free.
    :type handle: ots_handle_t | _CDataBase

    .. warning::

        Use `del handle` instead of this function in Python if
        you are using it on a ots_handle_t, to clean up all.

    """
    assert isinstance(handle, ots_handle_t) or isinstance(handle, _CDataBase), "handle must be an instance of ots_handle_t or _CDataBase"
    if isinstance(handle, _CDataBase):
        assert ffi.typeof(handle) == ffi.typeof('ots_handle_t**'), "handle must be a ots_handle_t**"
        lib.ots_free_handle(ffi.cast('ots_handle_t**', handle))
        return
    del handle


def ots_free_handle_object(handle: _CDataBase) -> None:
    """
    :meta private:
    """
    raise NotImplementedError('Only internal use, do not use this function directly.')


def ots_free_tx_description(tx_description: ots_tx_description_t | _CDataBase) -> None:
    """
    Frees the transaction description object returned by OTS functions.

    :param tx_description: The transaction description to free.
    :type tx_description: ots_tx_description_t | _CDataBase
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

    :param _CDataBase buffer: The buffer to free.
    :param int size: The size of the buffer.
    """
    assert isinstance(buffer, _CDataBase) and ffi.typeof(buffer).cname.endswith('* *'), "buffer must be a pointer to a pointer (void**)"
    lib.ots_secure_free(ffi.cast('void**', buffer), size)


def ots_wipeable_string_create(string: str) -> ots_result_t:
    """
    Creates a wipeable string from a regular string.

    .. code-block:: python

        my_string = "my wipeable string"
        result: ots_result_t = ots_wipeable_string_create(my_string)
        ws: ots_handle_t = ots_result_handle(result)
        ots_wipeable_string_c_str(ws) == my_string

    :param str string: The string to create a wipeable string from.
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

    .. code-block:: python

        str1: ots_handle_t = ots_wipeable_string_create("aaa")
        str2: ots_handle_t = ots_wipeable_string_create("bbb")
        result: ots_result_t = ots_wipeable_string_compare(str1, str2)
        assert ots_result_is_comparison(result)
        assert ots_result_comparison(result) < 0  # str1 is less than str2
        assert ots_result_is_equal(result) is False  # str1 is not equal to str2

    :param str1: The first string to compare.
    :type str1: ots_handle_t | _CDataBase
    :param str2: The second string to compare.
    :type str2: ots_handle_t | _CDataBase
    :return: ots_result_t indicating the comparison result.
    """
    assert isinstance(str1, (ots_handle_t, _CDataBase)) and HandleType(_unwrap(str1).type) == HandleType.WIPEABLE_STRING, "str1 must be an instance of ots_handle_t or _CDataBase and of type HandleType.WIPEABLE_STRING"
    assert isinstance(str2, (ots_handle_t, _CDataBase)) and HandleType(_unwrap(str2).type) == HandleType.WIPEABLE_STRING, "str2 must be an instance of ots_handle_t or _CDataBase and of type HandleType.WIPEABLE_STRING"
    return ots_result_t(lib.ots_wipeable_string_compare(_unwrap(str1), _unwrap(str2)))


def ots_wipeable_string_c_str(string: ots_handle_t | _CDataBase) -> str:
    """
    Returns the C-style string representation of a wipeable string.

    .. code-block:: python

        my_string = "my wipeable string"
        result: ots_result_t = ots_wipeable_string_create(my_string)
        ws: ots_handle_t = ots_result_handle(result)
        assert ots_wipeable_string_c_str(ws) == my_string

    :param string: The wipeable string to convert.
    :type string: ots_handle_t | _CDataBase
    :return: The string representation.
    """
    assert isinstance(string, (ots_handle_t, _CDataBase)), "string must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(string).type) == HandleType.WIPEABLE_STRING, "string must be of type HandleType.WIPEABLE_STRING"
    return ffi.string(lib.ots_wipeable_string_c_str(_unwrap(string))).decode('utf-8')


def ots_seed_indices_create(indices: list[int]) -> ots_result_t:
    """
    Creates a seed indices object from a list of integers.

    .. code-block:: python

        indices = [1, 2, 3, 4]
        result: ots_result_t = ots_seed_indices_create(indices)
        si: ots_handle_t = ots_result_handle(result)
        assert ots_seed_indices_values(si) == indices

    :param list[int] indices: A list of integers representing the seed indices.
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

    .. code-block:: python

        indices_string = "0001000200030004"
        result: ots_result_t = ots_seed_indices_create_from_string(indices_string)
        si: ots_handle_t = ots_result_handle(result)
        assert ots_seed_indices_values(si) == [1, 2, 3, 4]

        # or

        indices_string = "0001, 0002, 0003, 0004"
        result: ots_result_t = ots_seed_indices_create_from_string(indices_string, separator=', ')
        si: ots_handle_t = ots_result_handle(result)
        assert ots_seed_indices_values(si) == [1, 2, 3, 4]

    :param str string: A string containing the indices separated by the specified separator.
    :param str separator: The separator used in the string (default is an empty string).
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

    .. code-block:: python

        hex_string = "0B10B20B30B4"
        result: ots_result_t = ots_seed_indices_create_from_hex(hex_string)
        si: ots_handle_t = ots_result_handle(result)
        assert ots_seed_indices_values(si) == [177, 178, 179, 180]

        # or

        hex_string = "0B1|0B2|0B3|0B4"
        result: ots_result_t = ots_seed_indices_create_from_hex(hex_string, separator='|')
        si: ots_handle_t = ots_result_handle(result)
        assert ots_seed_indices_values(si) == [177, 178, 179, 180]

    :param str hex: A hexadecimal string containing the indices separated by the specified separator.
    :param str separator: The separator used in the string (default is a comma).
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

    .. code-block:: python

        indices: list[int] = [1, 2, 3, 4]
        result: ots_result_t = ots_seed_indices_create(indices)
        si: ots_handle_t = ots_result_handle(result)
        assert ots_seed_indices_values(si) == indices

    :param handle: The handle containing the seed indices.
    :type handle: ots_handle_t | _CDataBase
    :return: A list of integers representing the seed indices.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED_INDICES, "handle must be of type HandleType.SEED_INDICES"
    return [
        int(i) for i in ffi.from_buffer(
            'uint16_t[]',
            ffi.buffer(
                lib.ots_seed_indices_values(_unwrap(handle)),
                ots_seed_indices_count(handle) * ffi.sizeof('uint16_t')
            )
        )
    ]


def ots_seed_indices_count(handle: ots_handle_t | _CDataBase) -> int:
    """
    Returns the count of seed indices in the handle.

    .. code-block:: python

        indices: list[int] = [1, 2, 3, 4]
        result: ots_result_t = ots_seed_indices_create(indices)
        si: ots_handle_t = ots_result_handle(result)
        count: int = ots_seed_indices_count(si)
        assert count == len(indices)

    :param handle: The handle containing the seed indices.
    :return: The count of seed indices as an integer.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED_INDICES, "handle must be of type HandleType.SEED_INDICES"
    return lib.ots_seed_indices_count(_unwrap(handle))


def ots_seed_indices_clear(handle: ots_handle_t | _CDataBase) -> None:
    """
    Clears the seed indices in the handle.

    .. code-block:: python

        indices: list[int] = [1, 2, 3, 4]
        result: ots_result_t = ots_seed_indices_create(indices)
        si: ots_handle_t = ots_result_handle(result)
        assert ots_seed_indices_count(si) == len(indices)
        ots_seed_indices_clear(si)
        assert ots_seed_indices_count(si) == 0

    .. note::

        Clear not only clears the indices but also securely wipes the memory used by the indices.

    :param handle: The handle containing the seed indices to clear.
    :type handle: ots_handle_t | _CDataBase
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

    .. code-block:: python

        indices: list[int] = [1, 2, 3]
        result: ots_result_t = ots_seed_indices_create(indices)
        si: ots_handle_t = ots_result_handle(result)
        ots_seed_indices_append(si, 4)
        assert ots_seed_indices_values(si) == [1, 2, 3, 4]

    :param handle: The handle containing the seed indices.
    :type handle: ots_handle_t | _CDataBase
    :param int value: The uint16 value to append to the seed indices.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED_INDICES, "handle must be of type HandleType.SEED_INDICES"
    assert isinstance(value, int), "value must be an integer"
    assert value >= 0, "value must be a non-negative integer"
    lib.ots_seed_indices_append(_unwrap(handle), value)


def ots_seed_indices_numeric(
    handle: ots_handle_t | _CDataBase,
    separator: str = ''
) -> str:
    """
    Returns a string representation of the seed indices in numeric format.

    .. code-block:: python

        indices: list[int] = [1, 2, 3, 4]
        result: ots_result_t = ots_seed_indices_create(indices)
        si: ots_handle_t = ots_result_handle(result)
        numeric_string: str = ots_seed_indices_numeric(si, separator=', ')
        assert numeric_string == '1, 2, 3, 4'

    :param handle: The handle containing the seed indices.
    :type handle: ots_handle_t | _CDataBase
    :param str separator: The separator to use between indices (default is an empty string).
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

    .. code-block:: python

        indices: list[int] = [177, 178, 179, 180]
        result: ots_result_t = ots_seed_indices_create(indices)
        si: ots_handle_t = ots_result_handle(result)
        hex_string: str = ots_seed_indices_hex(si, separator=':')
        assert hex_string == '0B1:0B2:0B3:0B4'

    :param handle: The handle containing the seed indices.
    :type handle: ots_handle_t | _CDataBase
    :param str separator: The separator to use between indices (default is a comma).
    :return: A string representing the seed indices in hexadecimal format.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED_INDICES, "handle must be of type HandleType.SEED_INDICES"
    return ffi.string(lib.ots_seed_indices_hex(_unwrap(handle), separator.encode('utf-8'))).decode('utf-8')


def ots_seed_languages() -> ots_result_t:
    """
    Returns a list of all available seed languages.

    .. code-block:: python

        result: ots_result_t = ots_seed_languages()
        languages: list[ots_handle_t] = ots_result_handle_array_reference(result)

    :return: ots_result_t containing the list of seed languages.
    """
    return ots_result_t(lib.ots_seed_languages())


def ots_seed_languages_for_type(type: SeedType | int) -> ots_result_t:
    """
    Returns a list of seed languages for a specific seed type.

    .. code-block:: python

        result: ots_result_t = ots_seed_languages_for_type(SeedType.MONERO)
        languages: list[ots_handle_t] = ots_result_handle_array_reference(result)

    :param type: The seed type for which to get the languages.
    :return: ots_result_t containing the list of seed languages for the specified type.
    """
    assert isinstance(type, SeedType) or isinstance(type, int), "type must be an instance of SeedType or an integer"
    return ots_result_t(lib.ots_seed_languages_for_type(int(type)))


def ots_seed_language_default(type: SeedType | int) -> ots_result_t:
    """
    Returns the default seed language for a specific seed type.

    .. attention::

        The default language for any seed is intentionally not set.
        To use this function, you must first set a default language for the seed type
        using :py:func:`ots_seed_language_set_default` before questioning it.

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_code('en')
        en: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_set_default(SeedType.MONERO, en)
        result = ots_seed_language_default(SeedType.MONERO)
        default_language: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_equals(default_language, en)
        assert ots_result_bool(result) is True  # default language is now set to 'en'

    :param type: The seed type for which to get the default language.
    :type type: SeedType | int
    :return: ots_result_t containing the default seed language for the specified type.
    :raise: An error if the default language is not set for the seed type.
    """
    assert isinstance(type, SeedType) or isinstance(type, int), "type must be an instance of SeedType or an integer"
    return ots_result_t(lib.ots_seed_language_default(int(type)))


def ots_seed_language_set_default(
    type: SeedType | int,
    language: ots_handle_t | _CDataBase
) -> ots_result_t:
    """
    Sets the default seed language for a specific seed type.

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_code('en')
        en: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_set_default(SeedType.MONERO, en)
        default: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_equals(default, en)
        assert ots_result_bool(result) is True  # default language is now set to 'en'

    :param type: The seed type for which to set the default language.
    :type type: SeedType | int
    :param language: The handle of the language to set as default.
    :type language: ots_handle_t | _CDataBase
    :return: ots_result_t indicating the result of the operation.
    """
    assert isinstance(type, SeedType) or isinstance(type, int), "type must be an instance of SeedType or an integer"
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    return ots_result_t(lib.ots_seed_language_set_default(int(type), _unwrap(language)))


def ots_seed_language_from_code(code: str) -> ots_result_t:
    """
    Returns a seed language from its code.

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_code('en')
        en: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_code(en)
        assert ots_result_string(result) == 'en'  # en is the code for English

    :param str code: The code of the seed language.
    :return: ots_result_t containing the seed language corresponding to the given code.
    """
    assert isinstance(code, str), "code must be a string"
    return ots_result_t(lib.ots_seed_language_from_code(code.encode('utf-8')))


def ots_seed_language_from_name(name: str) -> ots_result_t:
    """
    Returns a seed language from its name.

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_name('Deutsch')
        de: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_code(de)
        assert ots_result_string(result) == 'de'  # de is the code for German

    :param str name: The name of the seed language.
    :return: ots_result_t containing the seed language corresponding to the given name.
    """
    assert isinstance(name, str), "name must be a string"
    return ots_result_t(lib.ots_seed_language_from_name(name.encode('utf-8')))


def ots_seed_language_from_english_name(name: str) -> ots_result_t:
    """
    Returns a seed language from its English name.

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_english_name('Russian')
        ru: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_code(ru)
        assert ots_result_string(result) == 'ru'  # ru is the code for Russian

    :param str name: The English name of the seed language.
    :return: ots_result_t containing the seed language corresponding to the given English name.
    """
    assert isinstance(name, str), "name must be a string"
    return ots_result_t(lib.ots_seed_language_from_english_name(name.encode('utf-8')))


def ots_seed_language_code(language: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the code of the seed language.

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_code('en')
        en: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_code(en)
        assert ots_result_string(result) == 'en'  # en is the code for English

    :param language: The handle of the seed language.
    :type language: ots_handle_t | _CDataBase
    :return: ots_result_t containing the code of the seed language.
    """
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    return ots_result_t(lib.ots_seed_language_code(_unwrap(language)))


def ots_seed_language_name(language: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the name of the seed language.

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_code('de')
        de: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_name(de)
        assert ots_result_string(result) == 'Deutsch'

    :param language: The handle of the seed language.
    :type language: ots_handle_t | _CDataBase
    :return: ots_result_t containing the name of the seed language.
    """
    assert isinstance(language, (ots_handle_t, _CDataBase)), "language must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(language).type) == HandleType.SEED_LANGUAGE, "language must be of type HandleType.SEED_LANGUAGE"
    return ots_result_t(lib.ots_seed_language_name(_unwrap(language)))


def ots_seed_language_english_name(language: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the English name of the seed language.

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_code('de')
        de: ots_handle_t = ots_result_handle(result)
        assert ots_seed_language_english_name(de) == 'German'

    :param language: The handle of the seed language.
    :type language: ots_handle_t | _CDataBase
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

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_code('en')
        en: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_supported(en, SeedType.MONERO)
        assert ots_result_boolean(result) is True  # en is supported for MONERO
        result = ots_seed_language_supported(en, SeedType.POLYSEED)
        assert ots_result_boolean(result) is True  # en is supported for POLYSEED

    :param language: The handle of the seed language.
    :type language: ots_handle_t | _CDataBase
    :param type: The seed type to check support for.
    :type type: SeedType | int
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

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_code('en')
        en: ots_handle_t = ots_result_handle(result)
        ots_seed_language_set_default(SeedType.MONERO, en)
        result = ots_seed_language_is_default(en, SeedType.MONERO)
        assert ots_result_boolean(result) is True  # en is the default for MONERO
        result = ots_seed_language_is_default(en, SeedType.POLYSEED)
        assert ots_result_boolean(result) is False  # en is not the default for POLYSEED

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

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_code('en')
        en1: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_from_english_name('English')
        en2: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_equals(en1, en2)
        assert ots_result_boolean(result) is True  # en1 and en2 are equal

    :param language1: The first seed language to compare.
    :type language1: ots_handle_t | _CDataBase
    :param language2: The second seed language to compare.
    :type language2: ots_handle_t | _CDataBase
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

    .. code-block:: python

        result: ots_result_t = ots_seed_language_from_code('en')
        en: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_equals_code(en, 'en')
        assert ots_result_boolean(result) is True  # en equals 'en'

    :param language: The handle of the seed language to compare.
    :type language: ots_handle_t | _CDataBase
    :param str code: The code to compare against.
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

    ... code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_language_from_code('en')
        en: ots_handle_t = ots_result_handle(result)
        result = ots_seed_phrase(seed, en, 'my_password')
        assert ots_result_is_wipeable_string(result) is True
        phrase: ots_handle_t = ots_result_handle(result)
        assert len(ots_wipeable_string_c_str(phrase).split(' ')) == 25  # Monero seed phrases are 25 words long

    :param seed: The handle of the seed.
    :type seed: ots_handle_t | _CDataBase
    :param language: The handle of the seed language.
    :type language: ots_handle_t | _CDataBase
    :param password: The password to use for generating the seed phrase.
    :type password: str
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

    ... code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_phrase(seed, 'en', 'my_password')
        assert ots_result_is_wipeable_string(result) is True
        phrase: ots_handle_t = ots_result_handle(result)
        assert len(ots_wipeable_string_c_str(phrase).split(' ')) == 25  # Monero seed phrases are 25 words long

    :param seed: The handle of the seed.
    :type seed: ots_handle_t | _CDataBase
    :param str language_code: The code of the seed language.
    :param str password: The password to use for generating the seed phrase.
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

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_indices(seed, 'my_password')
        assert ots_result_is_seed_indices(result)
        si: ots_handle_t = ots_result_handle(result)
        assert ots_seed_indices_count(si) == 24  # Monero seeds have 24 indices + 1 checksum (which is dropped on indices)

    :param handle: The handle of the seed.
    :type handle: ots_handle_t | _CDataBase
    :param password: The password to use for generating the seed indices.
    :type password: str
    :return: ots_result_t containing the seed indices.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    assert isinstance(password, str), "password must be a string"
    return ots_result_t(lib.ots_seed_indices(_unwrap(handle), password.encode('utf-8')))


def ots_seed_fingerprint(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the fingerprint of a given seed handle.

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_fingerprint(seed)
        fingerprint: ots_handle_t = ots_result_string(result)
        assert len(fingerprint) == 6 and all(c in '0123456789ABCDEF' for c in fingerprint)  # Monero seed fingerprints are 6 hex characters long

    :param handle: The handle of the seed.
    :type handle: ots_handle_t | _CDataBase
    :return: ots_result_t containing the fingerprint of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_fingerprint(_unwrap(handle)))


def ots_seed_is_legacy(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Checks if the given seed handle is a legacy seed.

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        monero_seed: ots_handle_t = ots_result_handle(result)
        result = ots_polyseed_generate()
        polyseed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_indices(monero_seed)
        si: ots_handle_t = ots_result_handle(result)
        indices: list[int] = ots_seed_indices_values(si)[:12]  # take 12 indices for legacy seed
        result = ots_seed_indices_create(indices)
        si = ots_result_handle(result)
        result = ots_legacy_seed_decode_indices(si)
        legacy_seed: ots_handle_t = ots_result_handle(result)

        result = ots_seed_is_legacy(monero_seed)
        assert ots_result_bool(result) is False  # Monero seed is not legacy
        result = ots_seed_is_legacy(polyseed)
        assert ots_result_bool(result) is False  # Polyseed is not legacy
        result = ots_seed_is_legacy(legacy_seed)
        assert ots_result_bool(result) is True  # Legacy seed is legacy

    :param handle: The handle of the seed.
    :type handle: ots_handle_t | _CDataBase
    :return: ots_result_t indicating whether the seed is legacy.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_is_legacy(_unwrap(handle)))


def ots_seed_type(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the type of the given seed handle.

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_type(seed)
        seed_type: SeedType = ots_result_seed_type(result)
        assert seed_type == SeedType.MONERO  # Monero seed type

    :param handle: The handle of the seed.
    :return: ots_result_t containing the type of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_type(_unwrap(handle)))


def ots_seed_address(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the address associated with the given seed handle.

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_address(seed)
        address: ots_handle_t = ots_result_handle(result)
        result = ots_address_base58_string(address)
        assert len(ots_result_string(address)) == 95  # Monero addresses are 95 characters long

    :param handle: The handle of the seed.
    :return: ots_result_t containing the address of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_address(_unwrap(handle)))


def ots_seed_timestamp(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the timestamp associated with the given seed handle.

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_timestamp(seed)
        assert ots_result_is_number(result)
        timestamp: int = ots_result_number(result)
        assert timestamp >= 0  # Timestamp should be a non-negative integer

    :param handle: The handle of the seed.
    :type handle: ots_handle_t | _CDataBase
    :return: ots_result_t containing the timestamp of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_timestamp(_unwrap(handle)))


def ots_seed_height(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the height associated with the given seed handle.

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_height(seed)
        assert ots_result_is_number(result)
        height: int = ots_result_number(result)
        assert height >= 0  # Height should be a non-negative integer

    :param handle: The handle of the seed.
    :type handle: ots_handle_t | _CDataBase
    :return: ots_result_t containing the height of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_height(_unwrap(handle)))


def ots_seed_network(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the network associated with the given seed handle.

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate(network=Network.STAGE)
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_network(seed)
        network: Network = ots_result_network(result)
        assert network == Network.STAGE  # The seed was generated for the STAGE network

    :param handle: The handle of the seed.
    :type handle: ots_handle_t | _CDataBase
    :return: ots_result_t containing the network of the seed.
    """
    assert isinstance(handle, (ots_handle_t, _CDataBase)), "handle must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(handle).type) == HandleType.SEED, "handle must be of type HandleType.SEED"
    return ots_result_t(lib.ots_seed_network(_unwrap(handle)))


def ots_seed_wallet(handle: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the wallet associated with the given seed handle.

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_wallet(seed)
        assert ots_result_is_wallet(result)
        wallet: ots_handle_t = ots_result_handle(result)

    :param handle: The handle of the seed.
    :type handle: ots_handle_t | _CDataBase
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

    .. code-block:: python

        result: ots_result_t = ots_seed_indices_create([1, 2, 3])
        seed_indices1: ots_handle_t = ots_result_handle(result)
        result = ots_seed_indices_create([4, 5, 6])
        seed_indices2: ots_handle_t = ots_result_handle(result)
        result = ots_seed_indices_merge_values(seed_indices1, seed_indices2)
        merged_indices: ots_handle_t = ots_result_handle(result)
        assert ots_seed_indices_values(merged_indices) == [5, 7, 5]  # [1, 2, 3] ^ [4, 5, 6] = [5, 7, 5]


    :param seed_indices1: The first seed indices handle.
    :type seed_indices1: ots_handle_t | _CDataBase
    :param seed_indices2: The second seed indices handle.
    :type seed_indices2: ots_handle_t | _CDataBase
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

    .. code-block:: python

        result: ots_result_t = ots_seed_indices_create([1, 2, 3])
        seed_indices: ots_handle_t = ots_result_handle(result)
        result = ots_seed_indices_merge_with_password(seed_indices, 'my_password')
        assert ots_result_is_seed_indices(result)
        merged_indices: ots_handle_t = ots_result_handle(result)

    :param seed_indices: The handle of the seed indices to merge.
    :type seed_indices: ots_handle_t | _CDataBase
    :param str password: The password to use for merging.
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

    .. code-block:: python

        result: ots_result_t = ots_seed_indices_create([1, 2, 3])
        seed_indices1: ots_handle_t = ots_result_handle(result)
        result = ots_seed_indices_create([4, 5, 6])
        seed_indices2: ots_handle_t = ots_result_handle(result)
        result = ots_seed_indices_create([5, 7, 5])
        seed_indices3: ots_handle_t = ots_result_handle(result)
        result = ots_seed_indices_merge_multiple_values([seed_indices1, seed_indices2, seed_indices3], 3)
        merged_indices: ots_handle_t = ots_result_handle(result)
        assert ots_seed_indices_values(merged_indices) == [0, 0, 0]

    :param seed_indices: A list of seed indices handles to merge.
    :type seed_indices: list[ots_handle_t | _CDataBase]
    :param int elements: The number of elements in the list.
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

    .. code-block:: python

        result: ots_result_t = ots_seed_indices_create([1, 2, 3])
        seed_indices1: ots_handle_t = ots_result_handle(result)
        result = ots_seed_indices_create([4, 5, 6])
        seed_indices2: ots_handle_t = ots_result_handle(result)
        result = ots_seed_indices_merge_values_and_zero(seed_indices1, seed_indices2, delete_after=True)
        merged_indices: ots_handle_t = ots_result_handle(result)
        del seed_indices1, seed_indices2  # Don't use seed_indices1 and seed_indices2 anymore because it will result in a segmentation fault, because the memory is wiped and freed already, but CFFI will not inform the _CDataBase object about it.

    .. warning::

        Do not use the provided seed indices handles after calling this function
        anymore, as they memory will be wiped and with delete_after set to True,
        also freed. Using them will result in a segmentation fault. Anyway, the
        CFFI will not inform the `_CDataBase` object about it, so it will lead
        to a segmentation fault when trying to access the handle again.

    :param seed_indices1: The first seed indices handle.
    :type seed_indices1: ots_handle_t | _CDataBase
    :param seed_indices2: The second seed indices handle.
    :type seed_indices2: ots_handle_t | _CDataBase
    :param bool delete_after: Whether to delete the original handles after merging.
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

    .. code-block:: python

        result: ots_result_t = ots_seed_indices_create([1, 2, 3])
        seed_indices: ots_handle_t = ots_result_handle(result)
        result = ots_seed_indices_merge_with_password_and_zero(seed_indices, 'my_password', delete_after=True)
        del seed_indices  # Don't use seed_indices anymore because it will result in a segmentation fault, because the memory is wiped and freed already, but CFFI will not inform the _CDataBase object about it.
        merged_indices: ots_handle_t = ots_result_handle(result)

    .. warning::

        Do not use the provided seed indices handle after calling this function
        anymore, as the memory will be wiped and with `delete_after` set to True,
        also freed. Using it will result in a segmentation fault. Anyway, the
        CFFI will not inform the `_CDataBase` object about it, so it will lead
        to a segmentation fault when trying to access the handle again.

    :param seed_indices: The handle of the seed indices to merge.
    :type seed_indices: ots_handle_t | _CDataBase
    :param str password: The password to use for merging.
    :param bool delete_after: Whether to delete the original handle after merging.
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

    .. seealso:: :py:func:`ots_seed_indices_merge_multiple_values`

    .. warning:: see :py:func:`ots_seed_indices_merge_values_and_zero` about the provided seed handles.

    :param seed_indices: A list of seed indices handles to merge.
    :type seed_indices: list[ots_handle_t | _CDataBase] | _CDataBase
    :param int elements: The number of elements in the list.
    :param bool delete_after: Whether to delete the original handles after merging.
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

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_phrase_for_language_code(seed, 'en')
        ws: ots_handle_t = ots_result_handle(result)
        phrase: str = ots_wipeable_string_c_str(phrase).split(' ')[:12]
        result = ots_legacy_seed_decode(phrase, 1024, network=Network.TEST)
        legacy_seed: ots_handle_t = ots_result_handle(result)

    :param str phrase: The legacy seed phrase to decode.
    :param int height: The height at which the seed was created.
    :param int time: The time at which the seed was created.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :type network: Network | int
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
    :type indices: ots_handle_t | _CDataBase
    :param int height: The height at which the seed was created.
    :param int time: The time at which the seed was created.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :type network: Network | int
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

    .. code-block:: python

        from time import time as current_time
        result: ots_result_t = ots_random_32()
        random: bytes = ots_result_char_array(result)
        result = ots_monero_seed_create(random, time=current_time(), network=Network.MAIN)
        assert ots_result_is_seed(result)
        seed: ots_handle_t = ots_result_handle(result)

    :param bytes random: Random 32 bytes to use for seed creation.
    :param int height: The height at which the seed is created.
    :param int time: The time at which the seed is created.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :type network: Network | int
    :return: ots_result_t containing the created Monero seed.
    """
    assert isinstance(random, bytes), "random must be bytes"
    assert len(random) == 32, "random must be exactly 32 bytes"
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

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)

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

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_fingerprint(seed)
        fp1: str = ots_result_string(result)
        result = ots_seed_phrase_for_language_code(seed, 'en', 'my_password')
        ws: ots_handle_t = ots_result_handle(result)
        phrase: str = ots_wipeable_string_c_str(ws)
        result = ots_monero_seed_decode(phrase, passphrase='my_passphrase')
        seed2: ots_handle_t = ots_result_handle(result)
        result = ots_seed_fingerprint(seed2)
        fp2: str = ots_result_string(result)
        assert fp1 == fp2  # The fingerprint should match the original seed

    :param str phrase: The Monero seed phrase to decode.
    :param int height: The height at which the seed was created.
    :param int time: The time at which the seed was created.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :type network: Network | int
    :param str passphrase: An optional passphrase for additional security.
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

    .. code-block:: python

        result: ots_result_t = ots_monero_seed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_fingerprint(seed)
        fp1: str = ots_result_string(result)
        result = ots_seed_indices(seed)
        si: ots_handle_t = ots_result_handle(result)
        result = ots_monero_seed_decode_indices(si)
        seed2: ots_handle_t = ots_result_handle(result)
        result = ots_seed_fingerprint(seed2)
        fp2: str = ots_result_string(result)
        assert fp1 == fp2  # The fingerprint should match the original seed

    :param indices: The handle containing the Monero seed indices to decode.
    :type indices: ots_handle_t | _CDataBase
    :param int height: The height at which the seed was created.
    :param int time: The time at which the seed was created.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :type network: Network | int
    :param str passphrase: An optional passphrase for additional security.
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

    .. code-block:: python

        from time import time as current_time
        result: ots_result_t = ots_random_bytes(19)
        random: bytes = ots_result_char_array(result)
        result = ots_polyseed_create(random)

    :param bytes random: Random 19 bytes to use for seed creation.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :type network: Network | int
    :param int time: The time at which the seed is created, defaults to 0 (current time).
    :param str passphrase: Optional passphrase for seed offset (empty string for none).
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

    .. code-block:: python

        result: ots_result_t = ots_polyseed_generate()
        seed: ots_handle_t = ots_result_handle(result)

    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :type network: Network | int
    :param int time: The time at which the seed is generated, defaults to 0 (current time).
    :param str passphrase: Optional passphrase for seed offset (empty string for none).
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

    .. code-block:: python

        result: ots_result_t = ots_polyseed_generate(passphrase='offset')
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_fingerprint(seed)
        fp1: str = ots_result_string(result)
        result = ots_seed_phrase_for_language_code(seed, 'en', 'my_password')
        ws: ots_handle_t = ots_result_handle(result)
        phrase: str = ots_wipeable_string_c_str(ws)
        result = ots_polyseed_decode(phrase, password='my_password', passphrase='offset')
        seed2: ots_handle_t = ots_result_handle(result)
        result = ots_seed_fingerprint(seed2)
        fp2: str = ots_result_string(result)
        assert fp1 == fp2  # The fingerprint should match the original seed

    :param str phrase: The Polyseed phrase to decode.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :type network: Network | int
    :param str password: Optional decryption password (empty string for none).
    :param str passphrase: Optional passphrase for seed offset (empty string for none).
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

    .. code-block:: python

        result: ots_result_t = ots_polyseed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_fingerprint(seed)
        fp1: str = ots_result_string(result)
        result = ots_seed_indices(seed)
        si: ots_handle_t = ots_result_handle(result)
        result = ots_polyseed_decode_indices(si)
        seed2: ots_handle_t = ots_result_handle(result)
        result = ots_seed_fingerprint(seed2)
        fp2: str = ots_result_string(result)
        assert fp1 == fp2  # The fingerprint should match the original seed

    :param indices: The handle containing the Polyseed indices to decode.
    :type indices: ots_handle_t | _CDataBase
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :type network: Network | int
    :param str password: Optional decryption password (empty string for none).
    :param str passphrase: Optional passphrase for seed offset (empty string for none).
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

    .. code-block:: python

        result: ots_result_t = ots_polyseed_generate()
        seed: ots_handle_t = ots_result_handle(result)
        result = ots_seed_phrase_for_language_code(seed, 'en')
        ws: ots_handle_t = ots_result_handle(result)
        phrase: str = ots_wipeable_string_c_str(ws)
        result = ots_seed_language_from_code('en')
        en: ots_handle_t = ots_result_handle(result)
        result = ots_polyseed_decode_with_language(phrase, en)
        seed2: ots_handle_t = ots_result_handle(result)

    .. note::

        This function is only needed if the Polyseed phrase could be more
        then one language, should not really happen, IMO.

    :param str phrase: The Polyseed phrase to decode.
    :param language: The handle of the seed language to use for decoding.
    :type language: ots_handle_t | _CDataBase
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :type network: Network | int
    :param str password: Optional decryption password (empty string for none).
    :param str passphrase: Optional passphrase for seed offset (empty string for none).
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

    .. seealso:: :py:func:`ots_polyseed_decode_with_language`, only difference is that this function uses a language code instead of a language handle.

    :param str phrase: The Polyseed phrase to decode.
    :param str language_code: The code of the seed language to use for decoding.
    :param network: The network for which the seed is intended (Main, Test, or Stagenet).
    :type network: Network | int
    :param str password: Optional decryption password (empty string for none).
    :param str passphrase: Optional passphrase for seed offset (empty string for none).
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

    .. code-block:: python

        addr: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
        result: ots_result_t = ots_address_create(addr)
        address: ots_handle_t = ots_result_handle(result)
        result = ots_address_base58_string(address)
        assert ots_result_string(result) == addr

    :param str address: The address string to create.
    :return: ots_result_t containing the created address handle.
    """
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_address_create(address.encode('utf-8')))


def ots_address_type(address: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the type of the given address handle.

    .. code-block:: python

        addr: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
        result: ots_result_t = ots_address_create(addr)
        address: ots_handle_t = ots_result_handle(result)
        result = ots_address_type(address)
        at: AddressType = ots_result_address_type(result)
        assert at == AddressType.STANDARD

    :param address: The handle of the address.
    :type address: ots_handle_t | _CDataBase
    :return: ots_result_t containing the type of the address.
    """
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_address_type(_unwrap(address)))


def ots_address_network(address: ots_handle_t | _CDataBase) -> ots_result_t:
    """
    Returns the network of the given address handle.

    .. code-block:: python

        addr: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
        result: ots_result_t = ots_address_create(addr)
        address: ots_handle_t = ots_result_handle(result)
        result = ots_address_network(address)
        assert ots_result_network(result) == Network.MAIN

    :param address: The handle of the address.
    :type address: ots_handle_t | _CDataBase
    :return: ots_result_t containing the network of the address.
    """
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    return ots_result_t(lib.ots_address_network(_unwrap(address)))


# TODO: <-- continue here with the rest of functions
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
    outputs: bytes | str
) -> ots_result_t:
    """
    Imports outputs into the given wallet handle.

    :param wallet: The handle of the wallet.
    :param outputs: A bytes or string containing the outputs to import.
    :return: ots_result_t indicating the result of the import operation.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(outputs, (bytes, str)), "outputs must be bytes or a string"
    if isinstance(outputs, str):
        outputs = outputs.encode('utf-8')
    return ots_result_t(lib.ots_wallet_import_outputs(_unwrap(wallet), outputs, len(outputs)))


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
    data: bytes | str
) -> ots_result_t:
    """
    Signs data with the given wallet handle.

    :param wallet: The handle of the wallet.
    :param data: The data to sign.
    :return: ots_result_t containing the signature of the data.
    """
    assert isinstance(wallet, (ots_handle_t, _CDataBase)), "wallet must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(wallet).type) == HandleType.WALLET, "wallet must be of type HandleType.WALLET"
    assert isinstance(data, (bytes, str)), "data must be bytes or a string"
    if isinstance(data, str):
        data = data.encode('utf-8')
    return ots_result_t(lib.ots_wallet_sign_data(_unwrap(wallet), data, len(data)))


def ots_wallet_sign_data_with_index(
    wallet: ots_handle_t | _CDataBase,
    data: bytes | str,
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
    assert isinstance(data, (bytes, str)), "data must be bytes or a string"
    assert isinstance(account, int), "account must be an integer"
    assert isinstance(subaddr, int), "subaddr must be an integer"
    if isinstance(data, str):
        data = data.encode('utf-8')
    return ots_result_t(lib.ots_wallet_sign_data_with_index(_unwrap(wallet), data, len(data), account, subaddr))


def ots_wallet_sign_data_with_address(
    wallet: ots_handle_t | _CDataBase,
    data: bytes | str,
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
    assert isinstance(data, (bytes, str)), "data must be bytes or a string"
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    if isinstance(data, str):
        data = data.encode('utf-8')
    return ots_result_t(lib.ots_wallet_sign_data_with_address(_unwrap(wallet), data, len(data), _unwrap(address)))


def ots_wallet_sign_data_with_address_string(
    wallet: ots_handle_t | _CDataBase,
    data: bytes | str,
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
    assert isinstance(data, (bytes, str)), "data must be bytes or a string"
    assert isinstance(address, str), "address must be a string"
    return ots_result_t(lib.ots_wallet_sign_data_with_address_string(_unwrap(wallet), data.encode('utf-8'), address.encode('utf-8')))


def ots_wallet_verify_data(
    wallet: ots_handle_t | _CDataBase,
    data: bytes | str,
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
    assert isinstance(data, (bytes, str)), "data must be bytes or a string"
    assert isinstance(signature, str), "signature must be a string"
    assert isinstance(legacy_fallback, bool), "legacy_fallback must be a boolean"
    if isinstance(data, str):
        data = data.encode('utf-8')
    return ots_result_t(lib.ots_wallet_verify_data(_unwrap(wallet), data, len(data), signature.encode('utf-8'), legacy_fallback))


def ots_wallet_verify_data_with_index(
    wallet: ots_handle_t | _CDataBase,
    data: bytes | str,
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
    assert isinstance(data, (bytes, str)), "data must be bytes or a string"
    assert isinstance(account, int), "account must be an integer"
    assert isinstance(subaddr, int), "subaddr must be an integer"
    assert isinstance(signature, str), "signature must be a string"
    assert isinstance(legacy_fallback, bool), "legacy_fallback must be a boolean"
    if isinstance(data, str):
        data = data.encode('utf-8')
    return ots_result_t(lib.ots_wallet_verify_data_with_index(_unwrap(wallet), data, len(data), account, subaddr, signature.encode('utf-8'), legacy_fallback))


def ots_wallet_verify_data_with_address(
    wallet: ots_handle_t | _CDataBase,
    data: bytes | str,
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
    assert isinstance(data, (bytes, str)), "data must be bytes or a string"
    assert isinstance(address, (ots_handle_t, _CDataBase)), "address must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(address).type) == HandleType.ADDRESS, "address must be of type HandleType.ADDRESS"
    assert isinstance(signature, str), "signature must be a string"
    assert isinstance(legacy_fallback, bool), "legacy_fallback must be a boolean"
    if isinstance(data, str):
        data = data.encode('utf-8')
    return ots_result_t(lib.ots_wallet_verify_data_with_address(_unwrap(wallet), data, len(data), _unwrap(address), signature.encode('utf-8'), legacy_fallback))


def ots_wallet_verify_data_with_address_string(
    wallet: ots_handle_t | _CDataBase,
    data: bytes | str,
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
    assert isinstance(data, (bytes, str)), "data must be bytes or a string"
    assert isinstance(address, str), "address must be a string"
    assert isinstance(signature, str), "signature must be a string"
    assert isinstance(legacy_fallback, bool), "legacy_fallback must be a boolean"
    if isinstance(data, str):
        data = data.encode('utf-8')
    return ots_result_t(lib.ots_wallet_verify_data_with_address_string(_unwrap(wallet), data, len(data), address.encode('utf-8'), signature.encode('utf-8'), legacy_fallback))


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
) -> bytes:
    """
    Returns the transaction set for the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :return: A string representing the transaction set.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    return ffi.unpack(
        lib.ots_tx_description_tx_set(_unwrap(tx_description)),
        ots_tx_description_tx_set_size(_unwrap(tx_description))
    )


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


def ots_tx_description_has_change(
    tx_description: ots_handle_t | _CDataBase
) -> bool:
    """
    Checks if the given transaction description handle has change.

    :param tx_description: The handle of the transaction description.
    :return: True if there is change, False otherwise.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    return lib.ots_tx_description_has_change(_unwrap(tx_description))

def ots_tx_description_change_address(
    tx_description: ots_handle_t | _CDataBase
) -> str | None:
    """
    Returns the change address for the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :return: A string representing the change address, or None if there is no change address.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    address = lib.ots_tx_description_change_address(_unwrap(tx_description))
    if address == ffi.NULL:
        return None
    return ffi.string(address).decode('utf-8')


def ots_tx_description_change_amount(
    tx_description: ots_handle_t | _CDataBase
) -> int:
    """
    Returns the change amount for the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :return: An integer representing the change amount.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    return lib.ots_tx_description_change_amount(_unwrap(tx_description))


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
) -> str | None:
    """
    Returns the payment ID for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the payment ID for.
    :return: An integer representing the payment ID for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    payment_id: _CDataBase = lib.ots_tx_description_transfer_payment_id(_unwrap(tx_description), index)
    if payment_id == ffi.NULL:
        return None
    return ffi.string(payment_id).decode('utf-8')


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
) -> bytes:
    """
    Returns the extra data for a specific transfer in the given transaction description handle.

    :param tx_description: The handle of the transaction description.
    :param index: The index of the transfer to retrieve the extra data for.
    :return: A string representing the extra data for the transfer.
    """
    assert isinstance(tx_description, (ots_handle_t, _CDataBase)), "tx_description must be an instance of ots_handle_t or _CDataBase"
    assert HandleType(_unwrap(tx_description).type) == HandleType.TX_DESCRIPTION, "tx_description must be of type HandleType.TX_DESCRIPTION"
    assert isinstance(index, int), "index must be an integer"
    return ffi.unpack(
        lib.ots_tx_description_transfer_extra(_unwrap(tx_description), index),
        lib.ots_tx_description_transfer_extra_size(_unwrap(tx_description), index)
    )


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
    assert isinstance(seed, _CDataBase) or seed.type == HandleType.SEED, "seed must be of type HandleType.SEED"
    assert isinstance(seed, ots_handle_t) or ffi.typeof(seed) == ffi.typeof('ots_handle_t **'), "seed must be a pointer of a pointer to ots_handle_t"
    assert isinstance(name, str), "name must be a string"
    return ots_result_t(
        lib.ots_seed_jar_transfer_seed_in(
            seed.ptrptr if isinstance(seed, ots_handle_t) else seed,
            name.encode('utf-8')
        )
    )


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
    assert size >= 0, "size must be a non-negative integer"
    assert isinstance(min_entropy, float), "min_entropy must be a float"
    return ots_result_t(lib.ots_check_low_entropy(ffi.cast('uint8_t *', data), len(data), min_entropy))


def ots_entropy_level(data: bytes) -> ots_result_t:
    """
    Returns the entropy level of the provided data.

    :param data: The data to analyze.
    :return: ots_result_t containing the entropy level.
    """
    assert isinstance(data, bytes), "data must be a bytes object"
    return ots_result_t(lib.ots_entropy_level(ffi.cast('uint8_t *', data), len(data)))


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


def ots_get_max_account_depth(default: int = 0) -> int:
    """
    Returns the maximum account default.

    :param default: The current account default.
    :return: An integer representing the maximum account default.
    """
    assert isinstance(default, int), "default must be an integer"
    assert default >= 0, "default must be a non-negative integer"
    return lib.ots_get_max_account_depth(default)


def ots_get_max_index_depth(default: int = 0) -> int:
    """
    Returns the maximum index depth.

    :param default: The default return default if values are not set.
    :return: An integer representing the maximum index depth.
    """
    assert isinstance(default, int), "depth must be an integer"
    assert default >= 0, "depth must be a non-negative integer"
    return lib.ots_get_max_index_depth(default)


def ots_verify_data(
    data: bytes | str,
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
    assert isinstance(data, (bytes, str)), "data must be bytes or a string"
    assert isinstance(address, str), "address must be a string"
    assert isinstance(signature, str), "signature must be a string"
    if isinstance(data, str):
        data = data.encode('utf-8')
    return ots_result_t(lib.ots_verify_data(data, len(data), address.encode('utf-8'), signature.encode('utf-8')))
