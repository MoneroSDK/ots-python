from datetime import datetime

from .raw import *
from .exceptions import OtsException
from .enums import *
from .seed import Seed
from .address import Address
from .wallet import Wallet

class SeedJar:

    @staticmethod
    def addSeed(seed: Seed, name: str) -> Seed:
        """Add a seed to the jar with a given name."""
        assert isinstance(seed, Seed), "seed must be an instance of Seed"
        assert isinstance(name, str), "name must be a string"
        result: ots_result_t = ots_seed_jar_add_seed(seed.handle, name.encode('utf-8'))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def remove(seed: Seed) -> bool:
        """Remove a seed from the jar."""
        assert isinstance(seed, Seed), "seed must be an instance of Seed"
        result: ots_result_t = ots_seed_jar_remove_seed(seed.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def purgeForIndex(index: int) -> bool:
        """Purge the seed jar for a specific index."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_purge_seed_for_index(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def purgeForName(name: str) -> bool:
        """Purge the seed jar for a specific name."""
        assert isinstance(name, str), "name must be a string"
        result: ots_result_t = ots_seed_jar_purge_seed_for_name(name.encode('utf-8'))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def purgeForFingerprint(fingerprint: str) -> bool:
        """Purge the seed jar for a specific fingerprint."""
        assert isinstance(fingerprint, str), "fingerprint must be a string"
        result: ots_result_t = ots_seed_jar_purge_seed_for_fingerprint(fingerprint.encode('utf-8'))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def purgeForAddress(address: str) -> bool:
        """Purge the seed jar for a specific address."""
        assert isinstance(address, str), "address must be a string"
        result: ots_result_t = ots_seed_jar_purge_seed_for_address(address.encode('utf-8'))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def transferIn(seed: Seed | ots_handle_t, name: str) -> Seed:
        """Transfer a seed into the jar with a given name."""
        assert isinstance(seed, (Seed, ots_handle_t)), "seed must be an instance of Seed or ots_handle_t"
        assert isinstance(seed, Seed) or seed.type == HandleType.SEED, "seed must be a Seed handle"
        assert isinstance(name, str), "name must be a string"
        result: ots_result_t = ots_seed_jar_transfer_seed_in(
            seed.handle if isinstance(seed, Seed) else seed,
            name.encode('utf-8')
        )
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def transferOut(seed: Seed | ots_handle_t) -> Seed:
        """Transfer a seed out of the jar."""
        assert isinstance(seed, (Seed, ots_handle_t)), "seed must be an instance of Seed or ots_handle_t"
        assert isinstance(seed, Seed) or seed.type == HandleType.SEED, "seed must be a Seed handle"
        result: ots_result_t = ots_seed_jar_transfer_seed_out(seed.handle if isinstance(seed, Seed) else seed)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def transferOutForIndex(index: int) -> Seed:
        """Transfer a seed out of the jar for a specific index."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_transfer_seed_out_for_index(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def transferOutForName(name: str) -> Seed:
        """Transfer a seed out of the jar for a specific name."""
        assert isinstance(name, str), "name must be a string"
        result: ots_result_t = ots_seed_jar_transfer_seed_out_for_name(name.encode('utf-8'))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def transferOutForFingerprint(fingerprint: str) -> Seed:
        """Transfer a seed out of the jar for a specific fingerprint."""
        assert isinstance(fingerprint, str), "fingerprint must be a string"
        result: ots_result_t = ots_seed_jar_transfer_seed_out_for_fingerprint(fingerprint.encode('utf-8'))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def transferOutForAddress(address: str) -> Seed:
        """Transfer a seed out of the jar for a specific address."""
        assert isinstance(address, str), "address must be a string"
        result: ots_result_t = ots_seed_jar_transfer_seed_out_for_address(address.encode('utf-8'))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def clear() -> bool:
        """Clear the seed jar."""
        result: ots_result_t = ots_seed_jar_clear()
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def seeds() -> list[Seed]:
        """Get a list of all seeds in the jar."""
        result: ots_result_t = ots_seed_jar_seeds()
        if ots_is_error(result):
            raise OtsException.from_result(result)
        handles: list[ots_handle_t] = ots_result_handle_array_reference(result)
        return [Seed(handle) for handle in handles]

    @staticmethod
    def count() -> int:
        """Get the count of seeds in the jar."""
        result: ots_result_t = ots_seed_jar_seed_count()
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_integer(result)

    @staticmethod
    def forIndex(idx: int) -> Seed:
        """Get a seed by its index in the jar."""
        assert isinstance(idx, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_seed_for_index(idx)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def forFingerprint(fingerprint: str) -> Seed:
        """Get a seed by its fingerprint."""
        assert isinstance(fingerprint, str), "fingerprint must be a string"
        result: ots_result_t = ots_seed_jar_seed_for_fingerprint(fingerprint.encode('utf-8'))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def forAddress(address: str) -> Seed:
        """Get a seed by its address."""
        assert isinstance(address, str), "address must be a string"
        result: ots_result_t = ots_seed_jar_seed_for_address(address.encode('utf-8'))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def forName(name: str) -> Seed:
        """Get a seed by its name."""
        assert isinstance(name, str), "name must be a string"
        result: ots_result_t = ots_seed_jar_seed_for_name(name.encode('utf-8'))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Seed(ots_result_handle(result))

    @staticmethod
    def name(seed: Seed | ots_handle_t) -> str:
        """Get the name of a seed."""
        assert isinstance(seed, (Seed, ots_handle_t)), "seed must be an instance of Seed or ots_handle_t"
        assert isinstance(seed, Seed) or seed.type == HandleType.SEED, "seed must be a Seed handle"
        result: ots_result_t = ots_seed_jar_seed_name(seed.handle if isinstance(seed, Seed) else seed)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def rename(seed: Seed | ots_handle_t, new_name: str) -> bool:
        """Rename a seed in the jar."""
        assert isinstance(seed, (Seed, ots_handle_t)), "seed must be an instance of Seed or ots_handle_t"
        assert isinstance(seed, Seed) or seed.type == HandleType.SEED, "seed must be a Seed handle"
        assert isinstance(new_name, str), "new_name must be a string"
        result: ots_result_t = ots_seed_jar_seed_rename(
            seed.handle if isinstance(seed, Seed) else seed,
            new_name.encode('utf-8')
        )
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def itemName(index: int) -> str:
        """Get the name of a seed by its index in the jar."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_name(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def itemFingerprint(index: int) -> str:
        """Get the fingerprint of a seed by its index in the jar."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_fingerprint(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def itemAddress(index: int) -> Address:
        """Get the address of a seed by its index in the jar."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_address(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Address(ots_result_handle(result))

    @staticmethod
    def itemAddressString(index: int) -> str:
        """Get the address string of a seed by its index in the jar."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_address_string(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def itemSeedType(index: int) -> SeedType:
        """Get the seed type of a seed by its index in the jar."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_seed_type(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_seed_type(result)

    @staticmethod
    def itemSeedTypeString(index: int) -> str:
        """Get the seed type string of a seed by its index in the jar."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_seed_type_string(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def itemIsLegacy(index: int) -> bool:
        """Check if a seed at a specific index is legacy."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_is_legacy(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @staticmethod
    def itemNetwork(index: int) -> Network:
        """Get the network of a seed by its index in the jar."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_network(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_network(result)

    @staticmethod
    def itemNetworkString(index: int) -> str:
        """Get the network string of a seed by its index in the jar."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_network_string(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    @staticmethod
    def itemHeight(index: int) -> int:
        """Get the height of a seed by its index in the jar."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_height(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_number(result)

    @staticmethod
    def itemTimestamp(index: int) -> int:
        """Get the timestamp of a seed by its index in the jar."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_timestamp(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_number(result)

    @staticmethod
    def itemTime(index: int) -> datetime:
        """Get the datetime of a seed by its index in the jar."""
        return datetime.fromtimestamp(SeedJar.itemTimestamp(index))

    @staticmethod
    def itemWallet(index: int) -> Wallet:
        """Get the wallet of a seed by its index in the jar."""
        assert isinstance(index, int), "index must be an integer"
        result: ots_result_t = ots_seed_jar_item_wallet(index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return Wallet(ots_result_handle(result))
