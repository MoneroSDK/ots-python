"""
This modules is intented to provide a procedural interface to the OTS library,
which is easy to use in comparison to the raw C ABI Wrapper.

.. warning::

    This module is not yet implemented, and could be removed in the future.
"""
from .raw import *
from .raw import _CDataBase
from .exceptions import OtsException


def free_result(result: ots_result_t | _CDataBase) -> None:
    """
    Frees the result object returned by OTS functions.
    :param result: The result object to free.
    """
    ots_free_result(result)

def version() -> str:
    """
    Returns the version of the OTS library.
    :return: A string containing the OTS version.
    """
    result = ots_version()
    if ots_is_error(result):
        raise OtsException.from_result(result)
    out = ots_result_string(result)
    free_result(result)
    return out

def random(size: int) -> bytes:
    """
    Returns a random byte string of the specified size.

    :param size: The number of random bytes to generate.
    :return: A byte string containing the random bytes.
    """
    result = ots_random_bytes(size)
    if ots_is_error(result):
        raise OtsException.from_result(result)
    if not ots_result_data_is_uint8(result) or ots_result_size(result) != size:
        raise OtsException.from_result(result)
    out: bytes = ots_result_char_array_reference(result)
    ots_free_result(result)
    return out

def random32() -> bytes:
    """
    Returns a random 32-byte string.
    :return: A byte string containing 32 random bytes.
    """
    result = ots_random_32()
    if ots_is_error(result):
        raise OtsException.from_result(result)
    if not ots_result_data_is_uint8(result) or ots_result_size(result) != 32:
        raise RuntimeError("Failed to generate random bytes")
    out: bytes = ots_result_char_array_reference(result)
    ots_free_result(result)
    return out
