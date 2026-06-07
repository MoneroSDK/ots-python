from .raw import ffi, lib, ots_result_t, _CDataBase, _unwrap

from .exceptions_generated import *


def exception_from_result(result: ots_result_t | _CDataBase) -> 'OtsException':
    """
    Creates an OtsException from a result object.
    """
    assert isinstance(result, (ots_result_t, _CDataBase)), "result must be an instance of ots_result_t or _CDataBase"
    assert ffi.typeof(_unwrap(result)) == ffi.typeof('ots_result_t*'), "result must be of type ots_result_t *"
    error: _CDataBase = _unwrap(result).error
    error_code: int = error.code
    if error_code in EXCEPTION_MAPPING:
        return EXCEPTION_MAPPING[error_code](error)
    return OtsException(error)
