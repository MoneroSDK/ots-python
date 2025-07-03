from dataclasses import dataclass
from datetime import datetime
from .raw import *
from .exceptions import OtsException
from .enums import *
from .seed import Seed, MoneroSeed, Polyseed
from .address import Address
from .wallet import Wallet


@dataclass
class SeedJarItem:
    """
    A data class representing an item in the seed jar.

    :param int index: The index of the seed in the jar.
    :param str name: The name of the seed.
    :param str fingerprint: The fingerprint of the seed.
    :param str address: The address associated with the seed.
    :param SeedType type: The type of the seed.
    :param str type_string: The type of the seed as a string.
    :param Network network: The network of the seed.
    :param str network_string: The network of the seed as a string.
    :param int height: The creation height of the seed.
    :param int timestamp: The timestamp when the seed was created.
    :param datetime time: The datetime when the seed was created.
    """
    index: int
    """The index of the seed in the jar."""
    name: str
    """The name of the seed."""
    fingerprint: str
    """The fingerprint of the seed."""
    address: str
    """The standard address of the seed."""
    type: SeedType
    """The type of the seed."""
    type_string: str
    """The type of the seed as a string."""
    network: Network
    """The network of the seed."""
    network_string: str
    """The network of the seed as a string."""
    height: int
    """The creation height of the seed."""
    timestamp: int
    """The timestamp when the seed was created."""
    time: datetime
    """The date and time when the seed was created."""

    def __hash__(self):
        """
        Custom hash function to allow using this class in sets.
        :meta private:
        """
        return hash((self.name, self.fingerprint, self.address))


class SeedJar:
    """
    A class to manage a jar of seeds. It provides methods to add, remove, purge,
    transfer, and query seeds in the jar. All methods are static.
    """

    @staticmethod
    def add(seed: Seed, name: str) -> Seed:
        """
        Add a seed to the jar with a given name.

        :param Seed seed: The seed to add.
        :param str name: The name to associate with the seed.
        :return: The reference to the added seed. Now you can dispose the provided seed.
        """
        assert isinstance(seed, Seed), "seed must be an instance of Seed"
        assert isinstance(name, str), "name must be a string"
        result: ots_result_t = ots_seed_jar_add_seed(seed.handle, name)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def remove(seed: Seed) -> bool:
        """
        Remove a seed from the jar.

        :param Seed seed: The seed to remove.
        :return: True if the seed was successfully removed, False otherwise.
        """
        assert isinstance(seed, Seed), "seed must be an instance of Seed"
        result: ots_result_t = ots_seed_jar_remove_seed(seed.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def purgeForIndex(index: int) -> bool:
        """
        Purge the seed jar for a specific index.

        :param int index: The index of the seed to purge.
        :return: True if the seed was successfully purged, False otherwise.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_purge_seed_for_index(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def purgeForName(name: str) -> bool:
        """
        Purge the seed jar for a specific name.

        :param str name: The name of the seed to purge.
        :return: True if the seed was successfully purged, False otherwise.
        """
        assert isinstance(name, str), "name must be a string"
        result: ots_result_t = ots_seed_jar_purge_seed_for_name(name)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def purgeForFingerprint(fingerprint: str) -> bool:
        """
        Purge the seed jar for a specific fingerprint.

        :param str fingerprint: The fingerprint of the seed to purge.
        :return: True if the seed was successfully purged, False otherwise.
        """
        assert isinstance(fingerprint, str), "fingerprint must be a string"
        result: ots_result_t = ots_seed_jar_purge_seed_for_fingerprint(fingerprint)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def purgeForAddress(address: str) -> bool:
        """
        Purge the seed jar for a specific address.

        :param str address: The address of the seed to purge.
        :return: True if the seed was successfully purged, False otherwise.
        """
        assert isinstance(address, str), "address must be a string"
        result: ots_result_t = ots_seed_jar_purge_seed_for_address(address)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def transferIn(seed: Seed | ots_handle_t, name: str) -> Seed:
        """
        Transfer a seed into the jar with a given name.

        :param Seed | ots_handle_t seed: The seed to transfer in. Don't use the provided seed after this operation, because it will be wiped.
        :param str name: The name to associate with the seed.
        :return: The reference to the transferred seed. The provided seed is now wiped.
        """
        assert isinstance(seed, (Seed, ots_handle_t)), "seed must be an instance of Seed or ots_handle_t"
        assert isinstance(seed, Seed) or seed.type == HandleType.SEED, "seed must be a Seed handle"
        assert isinstance(name, str), "name must be a string"
        result: ots_result_t = ots_seed_jar_transfer_seed_in(
            seed.handle if isinstance(seed, Seed) else seed,
            name
        )
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def transferOut(seed: Seed | ots_handle_t) -> Seed:
        """
        Transfer a seed out of the jar.

        :param Seed | ots_handle_t seed: The seed to transfer out. Don't use the provided seed after this operation, because it is a reference to the seed in the jar, which will be removed.
        :return: The seed object that owns the handle to the seed now, it is not anymore in the jar.
        """
        assert isinstance(seed, (Seed, ots_handle_t)), "seed must be an instance of Seed or ots_handle_t"
        assert isinstance(seed, Seed) or seed.type == HandleType.SEED, "seed must be a Seed handle"
        result: ots_result_t = ots_seed_jar_transfer_seed_out(seed.handle if isinstance(seed, Seed) else seed)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def transferOutForIndex(index: int) -> Seed:
        """
        Transfer a seed out of the jar for a specific index.

        :param int index: The index of the seed to transfer out.
        :return: The seed object that owns the handle to the seed now, it is not anymore in the jar.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_transfer_seed_out_for_index(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def transferOutForName(name: str) -> Seed:
        """
        Transfer a seed out of the jar for a specific name.

        :param str name: The name of the seed to transfer out.
        :return: The seed object that owns the handle to the seed now, it is not anymore in the jar.
        """
        assert isinstance(name, str), "name must be a string"
        result: ots_result_t = ots_seed_jar_transfer_seed_out_for_name(name)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def transferOutForFingerprint(fingerprint: str) -> Seed:
        """
        Transfer a seed out of the jar for a specific fingerprint.

        :param str fingerprint: The fingerprint of the seed to transfer out.
        :return: The seed object that owns the handle to the seed now, it is not anymore in the jar.
        """
        assert isinstance(fingerprint, str), "fingerprint must be a string"
        result: ots_result_t = ots_seed_jar_transfer_seed_out_for_fingerprint(fingerprint)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def transferOutForAddress(address: str) -> Seed:
        """
        Transfer a seed out of the jar for a specific address.

        :param str address: The address of the seed to transfer out.
        :return: The seed object that owns the handle to the seed now, it is not anymore in the jar.
        """
        assert isinstance(address, str), "address must be a string"
        result: ots_result_t = ots_seed_jar_transfer_seed_out_for_address(address)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def clear() -> bool:
        """
        Clear the seed jar.

        .. caution::

            This will remove all seeds from the jar!
            With this operation all seeds are securely wiped
            from the jar and cannot be recovered.

        :return: True if the jar was successfully cleared, False otherwise.
        """
        result: ots_result_t = ots_seed_jar_clear()
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def seeds() -> list[Seed]:
        """
        Get a list of all seeds in the jar.

        .. important::

            The returned list contains references to the seeds in the jar.
            The seeds have no ownership of the underlaying handles, the ownership
            is still with the jar.
            The seeds objects can be disposed any moment without consequences,
            and accessed later through the jar methods again.


        :return: A list of Seed objects referencing the seeds in the jar.
        """
        result: ots_result_t = ots_seed_jar_seeds()
        if ots_is_error(result):
            raise OtsException.from_result(result)
        handles: list[ots_handle_t] = ots_result_handle_array_reference(result)
        return [Seed(handle) for handle in handles]

    @staticmethod
    def count() -> int:
        """
        Get the count of seeds in the jar.

        :return: The number of seeds in the jar.
        """
        result: ots_result_t = ots_seed_jar_seed_count()
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_number(result)

    @staticmethod
    def forIndex(idx: int) -> Seed:
        """
        Get a seed by its index in the jar.

        :param int idx: The index of the seed to retrieve.
        :return: The Seed object with the reference to the seed in the jar.
        """
        assert isinstance(idx, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_seed_for_index(idx)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def forFingerprint(fingerprint: str) -> Seed:
        """
        Get a seed by its fingerprint.

        :param str fingerprint: The fingerprint of the seed to retrieve.
        :return: The Seed object with the reference to the seed in the jar.
        """
        assert isinstance(fingerprint, str), "fingerprint must be a string"
        result: ots_result_t = ots_seed_jar_seed_for_fingerprint(fingerprint)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def forAddress(address: str) -> Seed:
        """
        Get a seed by its address.

        :param str address: The address of the seed to retrieve.
        :return: The Seed object with the reference to the seed in the jar.
        """
        assert isinstance(address, str), "address must be a string"
        result: ots_result_t = ots_seed_jar_seed_for_address(address)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def forName(name: str) -> Seed:
        """
        Get a seed by its name.

        :param str name: The name of the seed to retrieve.
        :return: The Seed object with the reference to the seed in the jar.
        """
        assert isinstance(name, str), "name must be a string"
        result: ots_result_t = ots_seed_jar_seed_for_name(name)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def name(seed: Seed | ots_handle_t) -> str:
        """
        Get the name of a seed. (This is the name that was given when the seed was added to the jar.)

        :param seed: The seed to get the name for.
        :type seed: Seed | ots_handle_t
        :return: The name of the seed.
        """
        assert isinstance(seed, (Seed, ots_handle_t)), "seed must be an instance of Seed or ots_handle_t"
        assert isinstance(seed, Seed) or seed.type == HandleType.SEED, "seed must be a Seed handle"
        result: ots_result_t = ots_seed_jar_seed_name(seed.handle if isinstance(seed, Seed) else seed)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def rename(seed: Seed | ots_handle_t, new_name: str) -> bool:
        """
        Rename a seed in the jar.

        :param seed: The seed to rename.
        :type seed: Seed | ots_handle_t
        :param str new_name: The new name for the seed.
        :return: True if the seed was successfully renamed, False otherwise.
        """
        assert isinstance(seed, (Seed, ots_handle_t)), "seed must be an instance of Seed or ots_handle_t"
        assert isinstance(seed, Seed) or seed.type == HandleType.SEED, "seed must be a Seed handle"
        assert isinstance(new_name, str), "new_name must be a string"
        result: ots_result_t = ots_seed_jar_seed_rename(
            seed.handle if isinstance(seed, Seed) else seed,
            new_name
        )
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def itemName(index: int) -> str:
        """
        Get the name of a seed by its index in the jar. (The name that was given when the seed was added to the jar.)

        :param int index: The index of the seed in the jar.
        :return: The name of the seed at the specified index.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_name(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def itemFingerprint(index: int) -> str:
        """
        Get the fingerprint of a seed by its index in the jar.

        :param int index: The index of the seed in the jar.
        :return: The fingerprint of the seed at the specified index.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_fingerprint(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def itemAddress(index: int) -> Address:
        """
        Get the address of a seed by its index in the jar.

        :param int index: The index of the seed in the jar.
        :return: The Address object of the seed at the specified index.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_address(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Address(ots_result_handle(result))

    @staticmethod
    def itemAddressString(index: int) -> str:
        """
        Get the address string of a seed by its index in the jar.

        :param int index: The index of the seed in the jar.
        :return: The address string of the seed at the specified index.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_address_string(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def itemSeedType(index: int) -> SeedType:
        """
        Get the seed type of a seed by its index in the jar.

        :param int index: The index of the seed in the jar.
        :return: The SeedType of the seed at the specified index.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_seed_type(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_seed_type(result)

    @staticmethod
    def itemSeedTypeString(index: int) -> str:
        """
        Get the seed type string of a seed by its index in the jar.

        :param int index: The index of the seed in the jar.
        :return: The seed type as string of the seed at the specified index.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_seed_type_string(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def itemIsLegacy(index: int) -> bool:
        """
        Check if a seed at a specific index is legacy.

        .. note::

            Only relevant to Monero seeds, this are monero seeds
            which have only 12/13 words.

        :param int index: The index of the seed in the jar.
        :return: True if the seed is legacy, False otherwise.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_is_legacy(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def itemNetwork(index: int) -> Network:
        """
        Get the network of a seed by its index in the jar.

        :param int index: The index of the seed in the jar.
        :return: The Network object of the seed at the specified index.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_network(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_network(result)

    @staticmethod
    def itemNetworkString(index: int) -> str:
        """
        Get the network string of a seed by its index in the jar.

        :param int index: The index of the seed in the jar.
        :return: The network as string of the seed at the specified index.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_network_string(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def itemHeight(index: int) -> int:
        """
        Get the creation height of a seed by its index in the jar.

        .. note::

            On Monero seeds this is the absolut block height
            on which the seed was created, on Polyseed this
            is an estimated values based on timestamp.

        :param int index: The index of the seed in the jar.
        :return: The height of the seed at the specified index.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_height(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_number(result)

    @staticmethod
    def itemTimestamp(index: int) -> int:
        """
        Get the timestamp of a seed by its index in the jar.

        .. note::

            On Monero seeds this is timestamp is an estimated value
            based on the creation height, on Polyseed this is
            the timestamp encoded on creation into the polyseed.

        :param int index: The index of the seed in the jar.
        :return: The timestamp of the seed at the specified index.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_timestamp(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_number(result)

    @staticmethod
    def itemTime(index: int) -> datetime:
        """
        Get the datetime of a seed by its index in the jar.

        .. note::

            This is purely a convenience method to get
            the timestamp as a datetime object.

        :param int index: The index of the seed in the jar.
        :return: The datetime of the seed at the specified index.
        """
        return datetime.fromtimestamp(SeedJar.itemTimestamp(index))

    @staticmethod
    def items() -> list[SeedJarItem]:
        """
        Get a list of all items in the seed jar. This list is
        purely a convenience method to get the meta data of all
        seeds in the jar. To make rendering a list of seeds easier.

        :return: A list of SeedJarItem objects representing the seeds meta data in the jar.
        """
        return [
            SeedJarItem(
                index=i,
                name=SeedJar.itemName(i),
                fingerprint=SeedJar.itemFingerprint(i),
                address=SeedJar.itemAddressString(i),
                type=SeedJar.itemSeedType(i),
                type_string=SeedJar.itemSeedTypeString(i),
                network=SeedJar.itemNetwork(i),
                network_string=SeedJar.itemNetworkString(i),
                height=SeedJar.itemHeight(i),
                timestamp=SeedJar.itemTimestamp(i),
                time=SeedJar.itemTime(i)
            )
            for i in range(SeedJar.count())
        ]

    @staticmethod
    def itemWallet(index: int) -> Wallet:
        """
        Get the wallet of a seed by its index in the jar.

        :param int index: The index of the seed in the jar.
        :return: The Wallet object (only a reference) of the seed at the specified index.
        """
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_wallet(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Wallet(ots_result_handle(result))
