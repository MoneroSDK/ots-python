from .raw import *
from .exceptions import OtsException


class Address:
    """
    Represents any valid Monero address.
    """

    def __init__(self, handle: ots_handle_t):
        """
        Initializes the Monero Address object with a handle.

        :param ots_handle_t handle: The handle to the address. It must be of type HandleType.ADDRESS.
        """
        assert handle.type == HandleType.ADDRESS, "handle must be of type HandleType.ADDRESS"
        self.handle: ots_handle_t = handle
        self._type: AddressType | None = None
        self._network: Network | None = None
        self._fingerprint: str | None = None
        self._isIntegrated: bool | None = None
        self._paymentId: str | None = None
        self._length: int | None = None
        self._base58: str | None = None

    def __str__(self) -> str:
        """
        :return: base58 representation of the address.
        """
        return self.base58

    def __repr__(self) -> str:
        """
        :meta private:
        """
        return f"<Address: {self.base58}>"

    def __hash__(self):
        """
        :meta private:
        """
        hash(self.handle.ptr)

    def __len__(self) -> int:
        """
        :return: base58 length of the address.
        """
        return self.length

    def __eq__(self, other: object) -> bool:
        """
        Checks if two Address objects are equal.

        :param other: The other Address object to compare with. The other object needs to be either an :py:class:`Address` object or a :py:type:`str`.
        :type other: Address | str
        :return: True if the addresses are equal, False otherwise.
        """
        assert isinstance(other, (Address, str)), "other must be an Address object or a string"
        if isinstance(other, str):
            result: ots_result_t = ots_address_equal_string(self.handle, other)
            if ots_is_error(result):
                raise OtsException.from_result(result)
            return ots_result_boolean(result)
        if not isinstance(other, Address):
            raise NotImplementedError('Only Address objects and strings can be compared with Address objects')
        result: ots_result_t = ots_address_equal(self.handle, other.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @property
    def type(self) -> AddressType:
        """
        :return: The AddressType of the address.
        """
        if self._type is not None:
            return self._type
        result: ots_result_t = ots_address_type(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._type = ots_result_address_type(result)
        return self._type

    @property
    def network(self) -> Network:
        """
        :return: The Network of the address.
        """
        if self._network is not None:
            return self._network
        result: ots_result_t = ots_address_network(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._network = ots_result_network(result)
        return self._network

    @property
    def fingerprint(self) -> str:
        """
        :return: The fingerprint of the address.
        """
        if self._fingerprint is not None:
            return self._fingerprint
        result: ots_result_t = ots_address_fingerprint(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._fingerprint = ots_result_string(result)
        return self._fingerprint

    @property
    def isIntegrated(self) -> bool:
        """
        Checks if the address is an integrated address.

        :return: True if the address is integrated, False otherwise.
        """
        if self._isIntegrated is not None:
            return self._isIntegrated
        result: ots_result_t = ots_address_is_integrated(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._isIntegrated = ots_result_boolean(result)
        return self._isIntegrated

    @property
    def paymentId(self) -> str:
        """
        Returns the payment ID of the address if it is an integrated address.

        :return: The payment ID of the address.
        """
        if self._paymentId is not None:
            return self._paymentId
        result: ots_result_t = ots_address_payment_id(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._paymentId = ots_result_string(result)
        return self._paymentId

    @property
    def base58(self) -> str:
        """
        Returns the base58 representation of the address.

        :return: The base58 string representation of the address.
        """
        if self._base58 is not None:
            return self._base58
        result: ots_result_t = ots_address_base58_string(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._base58 = ots_result_string(result)
        return self._base58

    @property
    def length(self) -> int:
        """
        Returns the length of the address.

        :return: The length of the base58 address.
        """
        if self._length is not None:
            return self._length
        result: ots_result_t = ots_address_length(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._length = ots_result_number(result)
        return self._length

    @classmethod
    def fromString(cls, address: str) -> 'Address':
        """
        Creates an Address object from a string representation of the address.

        :param str address: The string representation of the address.
        :return: An Address object.
        """
        result: ots_result_t = ots_address_create(address)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def fromIntegrated(cls, address: 'Address') -> 'Address':
        """
        Creates an Address object from an integrated address.

        :param Address address: The integrated address.
        :return: An Address object.
        """
        assert address.isIntegrated, "address must be an integrated address"
        result: ots_result_t = ots_address_from_integrated(address.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))


class AddressString:
    """
    An helper class for handling Monero address strings,
    without creating an Address object.

    .. tip::

        Internally every time in the OTS library
        and Address object is created from a string, it is for
        convinience, but instead of using various methods for
        the same address string, it takes less resources simply
        creating a Address object with `Address.fromString(address)`
        and then using its methods directly on the object.

    """

    @classmethod
    def valid(cls, address: str, network: Network | int) -> bool:
        """
        Checks if the given address string is a valid Monero address.

        :param str address: The address string to validate.
        :param network: The network to validate against.
        :type network: Network | int
        :return: True if the address is valid, False otherwise.
        """
        result: ots_result_t = ots_address_string_valid(address, network)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @classmethod
    def network(cls, address: str) -> Network:
        """
        Returns the network for the given address string.

        :param str address: The address string.
        :return: The Network of the address.
        """
        result: ots_result_t = ots_address_string_network(address)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_network(result)

    @classmethod
    def type(cls, address: str) -> AddressType:
        """
        Returns the type of the address for the given address string.

        :param str address: The address string.
        :return: The AddressType of the address.
        """
        result: ots_result_t = ots_address_string_type(address)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_address_type(result)

    @classmethod
    def fingerprint(cls, address: str) -> str:
        """
        Returns the fingerprint of the address for the given address string.

        :param str address: The address string.
        :return: The fingerprint of the address.
        """
        result: ots_result_t = ots_address_string_fingerprint(address)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @classmethod
    def isIntegrated(cls, address: str) -> bool:
        """
        Checks if the address string is an integrated address.

        :param str address: The address string.
        :return: True if the address is integrated, False otherwise.
        """
        result: ots_result_t = ots_address_string_is_integrated(address)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)
