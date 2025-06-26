from .raw import ffi, lib
from .exceptions import OtsException
from .procedural import (
    version,
    random,
    random32,
)


class Ots:
    @classmethod
    def version(cls) -> str:
        """
        Returns the version of the OTS library.
        """
        return version()

    @classmethod
    def random(cls, size: int) -> bytes:
        """
        Returns a random byte string of the specified size.

        :param size: The number of random bytes to generate.
        :return: A byte string containing the random bytes.
        """
        return random(size)

    @classmethod
    def random32(cls) -> bytes:
        """
        Returns a random 32-byte string.
        """
        return random32()
