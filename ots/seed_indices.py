from .raw import *
from .exceptions import OtsException

class SeedIndices:

    def __init__(self, handle: ots_handle_t):
        self.handle: ots_handle_t = handle

    @classmethod
    def fromValues(cls, list[int]) -> 'SeedIndices':
        """
        Create a SeedIndices object from a list of integers.
        """
        result: ots_result_t = ots_seed_indices_create(list)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))
