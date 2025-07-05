from .raw import *
from .exceptions import OtsException
from .wipeable_string import WipeableString
from .seed_indices import SeedIndices
from .seed_language import SeedLanguage
from .wallet import Wallet
from .address import Address
from datetime import datetime


class Seed:
    """
    Seed class to handle the seed data.
    """

    def __init__(self, handle: ots_handle_t):
        assert isinstance(handle, ots_handle_t), "handle must be an instance of ots_handle_t"
        assert handle.type == HandleType.SEED, "handle must be of type Seed"
        self.handle: ots_handle_t = handle
        self._type: SeedType | None = None
        self._isLegacy: bool | None = None
        self._fingerprint: str | None = None
        self._address: Address | None = None
        self._timestamp: int | None = None
        self._time: datetime | None = None
        self._height: int | None = None
        self._network: Network | None = None
        self._wallet: Wallet | None = None

    def __str__(self):
        """
        :return: The fingerprint of the seed.
        """
        return self.fingerprint

    def __repr__(self):
        """
        :meta private:
        """
        return f"Seed({str(self)})"

    def __hash__(self):
        """
        Returns the hash of the Seed instance.
        :meta private:
        """
        return hash((self.__class__.__name__, self.handle))

    @property
    def type(self) -> SeedType:
        """
        :return: The type of the seed.
        """
        if self._type is not None:
            return self._type
        result: ots_result_t = ots_seed_type(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._type = SeedType(ots_result_number(result))
        return self._type

    @property
    def isLegacy(self) -> bool:
        """
        Checks if the seed is a legacy seed.

        :return: True if the seed is a legacy seed, False otherwise.
        """
        if self._isLegacy is not None:
            return self._isLegacy
        result: ots_result_t = ots_seed_is_legacy(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._isLegacy = ots_result_boolean(result)
        return self._isLegacy

    def phrase(self, language: SeedLanguage, password: str = '') -> WipeableString:
        """
        Returns the seed phrase in the specified language.

        :param language: The language of the seed phrase.
        :param password: Optional password to encrypt the seed phrase. Not supported for legacy seeds. Works different on Monero Seeds and Polyseeds. While on Monero Seeds the password is the offset passphrase, on a Polyseed it is the actual password. Polyseed also support passphrase offset, but needs to be set on creating the Polyseed and decoding the polyseed. While on the Monero Seed password (offset passphrase in this case) is substracted on generating the seed phrase, before generating the seed phrase.

        :return: A WipeableString containing the seed phrase.
        """
        assert isinstance(language, SeedLanguage), "language must be an instance of SeedLanguage"
        assert language.supported(self.type), "language must be supported by the OTS library"
        assert password == '' or not self.isLegacy(), "password is not supported for legacy seeds"
        result: ots_result_t = ots_seed_phrase(self.handle, language.handle, password)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return WipeableString(ots_result_handle(result))

    def indices(self, password: str = '') -> SeedIndices:
        """
        Returns the seed indices.

        :param password: Optional password to decrypt the seed indices. Not supported for legacy seeds.
        :return: A SeedIndices object containing the seed indices.
        """
        assert password == '' or not self.isLegacy(), "password is not supported for legacy seeds"
        result: ots_result_t = ots_seed_indices(self.handle, password)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return SeedIndices(ots_result_handle(result))

    @property
    def fingerprint(self) -> str:
        """
        Returns the fingerprint of the seed.

        :return: A last 6 digit upper case hex string from sha256(base58 standard addres) representing the fingerprint of the seed.
        """
        if self._fingerprint is not None:
            return self._fingerprint
        result: ots_result_t = ots_seed_fingerprint(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._fingerprint = ots_result_string(result)
        return self._fingerprint

    @property
    def address(self) -> Address:
        """
        Returns the standard address of the seed.

        :return: An Address object representing the seed's address.
        """
        if self._address is not None:
            return self._address
        result: ots_result_t = ots_seed_address(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._address = Address(ots_result_handle(result))
        return self._address

    @property
    def timestamp(self) -> int:
        """
        Returns the timestamp of the seed.

        :return: An integer representing the timestamp of the seed.
        """
        if self._timestamp is not None:
            return self._timestamp
        result: ots_result_t = ots_seed_timestamp(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._timestamp = ots_result_number(result)
        return self._timestamp

    @property
    def time(self) -> datetime:
        """
        Returns the time of the seed as a datetime object.

        :return: A datetime object representing the time of the seed.
        """
        if self._time is not None:
            return self._time
        self._time = datetime.fromtimestamp(self.timestamp)
        return self._time

    @property
    def height(self) -> int:
        """
        Returns the height of the seed.

        :return: An integer representing the height of the seed.
        """
        if self._height is not None:
            return self._height
        result: ots_result_t = ots_seed_height(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._height = ots_result_number(result)
        return self._height

    @property
    def network(self) -> Network:
        """
        Returns the network of the seed.

        :return: A Network enum representing the network of the seed.
        """
        if self._network is not None:
            return self._network
        result: ots_result_t = ots_seed_network(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._network = Network(ots_result_number(result))
        return self._network

    @property
    def wallet(self) -> Wallet:
        """
        Returns the wallet associated with the seed.

        :return: A Wallet object representing the seed's wallet.
        """
        if self._wallet is not None:
            return self._wallet
        result: ots_result_t = ots_seed_wallet(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._wallet = Wallet(ots_result_handle(result))
        return self._wallet


class LegacySeed(Seed):
    """
    LegacySeed class to handle Monero 12/13 word legacy seeds.
    """

    @classmethod
    def decode(
        cls,
        phrase: str,
        height: int = 0,
        time: int = 0,
        network: Network = Network.MAIN
    ) -> 'LegacySeed':
        """
        Decodes a legacy seed phrase into a LegacySeed object.

        :param phrase: The seed phrase to decode.
        :param height: The block height associated with the seed.
        :param time: The timestamp associated with the seed.
        :param network: The network type for the seed.
        :return: A LegacySeed object containing the decoded seed data.
        """
        assert isinstance(phrase, str), "phrase must be a string"
        assert isinstance(height, int), "height must be an integer"
        assert isinstance(time, int), "time must be an integer"
        assert isinstance(network, Network), "network must be an instance of Network"
        result: ots_result_t = ots_legacy_seed_decode(phrase, height, time, network)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def decodeIndices(
        cls,
        indices: SeedIndices,
        height: int = 0,
        time: int = 0,
        network: Network = Network.MAIN
    ) -> 'LegacySeed':
        """
        Decodes seed indices into a LegacySeed object.

        :param indices: The SeedIndices object to decode.
        :param height: The block height associated with the seed.
        :param time: The timestamp associated with the seed.
        :param network: The network type for the seed.
        :return: A LegacySeed object containing the decoded seed data.
        """
        assert isinstance(indices, SeedIndices), "indices must be an instance of SeedIndices"
        assert isinstance(height, int), "height must be an integer"
        assert isinstance(time, int), "time must be an integer"
        assert isinstance(network, Network), "network must be an instance of Network"
        handle: ots_handle_t = ots_legacy_seed_decode_indices(indices.handle, height, time, network)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))


class MoneroSeed(Seed):
    """
    MoneroSeed class to handle Monero 24/25 word seeds.
    """

    @classmethod
    def create(
        cls,
        random: bytes,
        height: int = 0,
        time: int = 0,
        network: Network = Network.MAIN
    ) -> 'MoneroSeed':
        """
        Creates a new MoneroSeed instance.

        :param random: 32 bytes of random data to create the seed.
        :param height: The block height associated with the seed.
        :param time: The timestamp associated with the seed.
        :param network: The network type for the seed.
        :return: A MoneroSeed object containing the created seed data.
        """
        assert isinstance(random, bytes), "random must be a byte string"
        assert len(random) == 32, "random must be 32 bytes long"
        assert isinstance(height, int), "height must be an integer"
        assert isinstance(time, int), "time must be an integer"
        assert isinstance(network, Network), "network must be an instance of Network"
        result: ots_result_t = ots_monero_seed_create(random, height, time, network)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def generate(
        cls,
        height: int = 0,
        time: int = 0,
        network: Network = Network.MAIN
    ) -> 'MoneroSeed':
        """
        Generates a new MoneroSeed instance with random data.

        :param height: The block height associated with the seed.
        :param time: The timestamp associated with the seed.
        :param network: The network type for the seed.
        :return: A MoneroSeed object containing the generated seed data.
        """
        assert isinstance(height, int), "height must be an integer"
        assert isinstance(time, int), "time must be an integer"
        assert isinstance(network, Network), "network must be an instance of Network"
        result: ots_result_t = ots_monero_seed_generate(height, time, network)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def decode(
        cls,
        phrase: str,
        height: int = 0,
        time: int = 0,
        network: Network = Network.MAIN,
        passphrase: str = ''
    ) -> 'MoneroSeed':
        """
        Decodes a Monero seed phrase into a MoneroSeed object.

        :param phrase: The seed phrase to decode.
        :param height: The block height associated with the seed.
        :param time: The timestamp associated with the seed.
        :param network: The network type for the seed.
        :param passphrase: Optional passphrase for the seed.
        :return: A MoneroSeed object containing the decoded seed data.
        """
        assert isinstance(phrase, str), "phrase must be a string"
        assert isinstance(height, int), "height must be an integer"
        assert isinstance(time, int), "time must be an integer"
        assert isinstance(network, Network), "network must be an instance of Network"
        assert isinstance(passphrase, str), "passphrase must be a string"
        result: ots_result_t = ots_monero_seed_decode(phrase, height, time, network, passphrase)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def decodeIndices(
        cls,
        indices: SeedIndices,
        height: int = 0,
        time: int = 0,
        network: Network = Network.MAIN,
        passphrase: str = ''
    ) -> 'MoneroSeed':
        """
        Decodes seed indices into a MoneroSeed object.

        :param indices: The SeedIndices object to decode.
        :param height: The block height associated with the seed.
        :param time: The timestamp associated with the seed.
        :param network: The network type for the seed.
        :param passphrase: Optional passphrase for the seed.
        :return: A MoneroSeed object containing the decoded seed data.
        """
        assert isinstance(indices, SeedIndices), "indices must be an instance of SeedIndices"
        assert isinstance(height, int), "height must be an integer"
        assert isinstance(time, int), "time must be an integer"
        assert isinstance(network, Network), "network must be an instance of Network"
        assert isinstance(passphrase, str), "passphrase must be a string"
        result: ots_result_t = ots_monero_seed_decode_indices(indices.handle, height, time, network, passphrase)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))


class Polyseed(Seed):
    """
    Polyseed class to handle Polyseed (16 word) seeds,
    with timestamp and encryption support included.
    """

    def moneroSeed(self) -> MoneroSeed:
        """
        Converts the Polyseed to a MoneroSeed. (Creates a new MoneroSeed instance from the Polyseed)

        :return: A MoneroSeed object representing the Polyseed.
        """
        result: ots_result_t = ots_polyseed_convert_to_monero_seed(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return MoneroSeed(ots_result_handle(result))

    @classmethod
    def create(
        cls,
        random: bytes,
        network: Network = Network.MAIN,
        time: int = 0,
        passphrase: str = ''
    ) -> 'Polyseed':
        """
        Creates a new Polyseed instance.

        :param random: 19 bytes of random data to create the seed.
        :param network: The network type for the seed.
        :param time: The timestamp associated with the seed.
        :param passphrase: Optional passphrase for the seed.
        :return: A Polyseed object containing the created seed data.
        """
        assert isinstance(random, bytes), "random must be a byte string"
        assert len(random) == 19, "random must be 32 bytes long"
        assert isinstance(network, Network), "network must be an instance of Network"
        assert isinstance(time, int), "time must be an integer"
        assert isinstance(passphrase, str), "passphrase must be a string"
        result: ots_result_t = ots_polyseed_create(random, network, time, passphrase)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def generate(
        cls,
        network: Network = Network.MAIN,
        time: int = 0,
        passphrase: str = ''
    ) -> 'Polyseed':
        """
        Generates a new Polyseed instance with random data.

        :param network: The network type for the seed.
        :param time: The timestamp associated with the seed.
        :param passphrase: Optional passphrase for the seed.
        :return: A Polyseed object containing the generated seed data.
        """
        assert isinstance(network, Network), "network must be an instance of Network"
        assert isinstance(time, int), "time must be an integer"
        assert isinstance(passphrase, str), "passphrase must be a string"
        result: ots_result_t = ots_polyseed_generate(network, time, passphrase)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def decode(
        cls,
        phrase: str,
        network: Network = Network.MAIN,
        password: str = '',
        passphrase: str = ''
    ) -> 'Polyseed':
        """
        Decodes a Polyseed phrase into a Polyseed object.

        :param phrase: The seed phrase to decode.
        :param network: The network type for the seed.
        :param password: Optional password to decrypt the seed. Not supported for legacy seeds.
        :param passphrase: Optional passphrase for the seed.
        :return: A Polyseed object containing the decoded seed data.
        """
        assert isinstance(phrase, str), "phrase must be a string"
        assert isinstance(network, Network), "network must be an instance of Network"
        assert isinstance(password, str), "password must be a string"
        assert isinstance(passphrase, str), "passphrase must be a string"
        result: ots_result_t = ots_polyseed_decode(phrase, network, password, passphrase)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def decodeIndices(
        cls,
        indices: SeedIndices,
        network: Network = Network.MAIN,
        password: str = '',
        passphrase: str = ''
    ) -> 'Polyseed':
        """
        Decodes seed indices into a Polyseed object.

        :param indices: The SeedIndices object to decode.
        :param network: The network type for the seed.
        :param password: Optional password to decrypt the seed. Not supported for legacy seeds.
        :param passphrase: Optional passphrase for the seed.
        :return: A Polyseed object containing the decoded seed data.
        """
        assert isinstance(indices, SeedIndices), "indices must be an instance of SeedIndices"
        assert isinstance(network, Network), "network must be an instance of Network"
        assert isinstance(password, str), "password must be a string"
        assert isinstance(passphrase, str), "passphrase must be a string"
        result: ots_result_t = ots_polyseed_decode_indices(indices.handle, network, password, passphrase)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def decodeWithLanguage(
        cls,
        phrase: str,
        language: SeedLanguage,
        network: Network = Network.MAIN,
        password: str = '',
        passphrase: str = ''
    ) -> 'Polyseed':
        """
        Decodes a Polyseed phrase with a specific language into a Polyseed object.

        :param phrase: The seed phrase to decode.
        :param language: The language of the seed phrase.
        :param network: The network type for the seed.
        :param password: Optional password to decrypt the seed. Not supported for legacy seeds.
        :param passphrase: Optional passphrase for the seed.
        :return: A Polyseed object containing the decoded seed data.
        """
        assert isinstance(phrase, str), "phrase must be a string"
        assert isinstance(language, SeedLanguage), "language must be an instance of SeedLanguage"
        assert language.supported(SeedType.POLYSEED), "language must be supported by Polyseed"
        assert isinstance(network, Network), "network must be an instance of Network"
        assert isinstance(password, str), "password must be a string"
        assert isinstance(passphrase, str), "passphrase must be a string"
        result: ots_result_t = ots_polyseed_decode_with_language(phrase, language.result, network, password, passphrase)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def decodeWithLanguageCode(
        cls,
        phrase: str,
        languageCode: str,
        network: Network = Network.MAIN,
        password: str = '',
        passphrase: str = ''
    ) -> 'Polyseed':
        """
        Decodes a Polyseed phrase with a specific language code into a Polyseed object.

        :param phrase: The seed phrase to decode.
        :param languageCode: The language code of the seed phrase.
        :param network: The network type for the seed.
        :param password: Optional password to decrypt the seed. Not supported for legacy seeds.
        :param passphrase: Optional passphrase for the seed.
        :return: A Polyseed object containing the decoded seed data.
        """
        assert isinstance(phrase, str), "phrase must be a string"
        assert isinstance(languageCode, str), "languageCode must be a string"
        assert isinstance(network, Network), "network must be an instance of Network"
        assert isinstance(password, str), "password must be a string"
        assert isinstance(passphrase, str), "passphrase must be a string"
        result: ots_result_t = ots_polyseed_decode_with_language_code(phrase, languageCode, network, password, passphrase)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))
