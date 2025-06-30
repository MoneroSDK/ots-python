from .raw import *
from .enums import HandleType
from .exceptions import OtsException
from .transaction import TxDescription, TxWarning
from .address import Address
from .wipeable_string import WipeableString


class Wallet:
    """
    Represents a monero wallet.
    """

    def __init__(self, handle: ots_handle_t):
        assert isstance(handle, ots_handle_t), "handle must be of type ots_handle_t"
        assert handle.type == HandleType.WALLET, "handle must be of type HandleType.WALLET"
        self.handle: ots_handle_t = handle
        self._height: int | None = None
        self._addresses: dict[tuple[int, int], Address] = {}

    def height(self) -> int:
        """Get the height of the wallet."""
        if self._height is None:
            self._height = lib.ots_wallet_height(self.handle)
        return self._height

    def address(self, account: int, index: int) -> Address:
        """Get the address at the specified account and index."""
        key = (account, index)
        if key not in self._addresses:
            address_handle = lib.ots_wallet_address(self.handle, account, index)
            if address_handle is None:
                raise OtsException("Failed to get address handle")
            self._addresses[key] = Address(address_handle)
        return self._addresses[key]

    def accounts(self, max: int = 10, offset: int = 0) -> list[Address]:
        """Get a list of addresses in the wallet, with pagination."""
        result: ots_result_t = ots_wallet_accounts(self.handle, max, offset)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        addressHandles = ots_result_handle_array(result)
        return [Address(handle) for handle in addressHandles]

    def subAddresses(self, account: int = 0, max: int = 10, offset: int = 0) -> list[Address]:
        """Get a list of sub-addresses for a specific account."""
        result: ots_result_t = ots_wallet_subaddresses(self.handle, account, max, offset)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        addressHandles = ots_result_handle_array(result)
        return [Address(handle) for handle in addressHandles]

    def hasAddress(
        self,
        address: Address | str,
        maxAccountDepth: int = 0,
        maxIndexDepth: int = 0
    ) -> bool:
        """Check if the wallet contains a specific address."""
        assert isstance(address, (Address, str)), "address must be an Address instance or a string"
        assert maxAccountDepth >= 0, "maxAccountDepth must be non-negative"
        assert maxIndexDepth >= 0, "maxIndexDepth must be non-negative"
        if isinstance(address, str):
            result: ots_result_t = ots_wallet_has_address_string(
                self.handle,
                address,
                maxAccountDepth,
                maxIndexDepth
            )
            if ots_is_error(result):
                raise OtsException.from_result(result)
            return ots_result_boolean(result)
        result: ots_result_t = ots_wallet_has_address(
            self.handle,
            address,
            maxAccountDepth,
            maxIndexDepth
        )
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    def addressIndex(
        self,
        address: Address | str,
        maxAccountDepth: int = 0,
        maxIndexDepth: int = 0
    ) -> tuple[int, int]:
        """Get the account and index of an address in the wallet."""
        assert isstance(address, (Address, str)), "address must be an Address instance or a string"
        assert maxAccountDepth >= 0, "maxAccountDepth must be non-negative"
        assert maxIndexDepth >= 0, "maxIndexDepth must be non-negative"
        if isinstance(address, str):
            result: ots_result_t = ots_wallet_address_string_index(
                self.handle,
                address,
                maxAccountDepth,
                maxIndexDepth
            )
            if ots_is_error(result):
                raise OtsException.from_result(result)
            return tuple(ots_result_uint32_array(result))
        result: ots_result_t = ots_wallet_address_index(
            self.handle,
            address,
            maxAccountDepth,
            maxIndexDepth
        )
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return tuple(ots_result_uint32_array(result))

    def secretViewKey(self) -> WipeableString:
        """Get the secret view key of the wallet."""
        result: ots_result_t = ots_wallet_secret_view_key(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return WipeableString(ots_result_string(result))

    def publicViewKey(self) -> WipeableString:
        """Get the public view key of the wallet."""
        result: ots_result_t = ots_wallet_public_view_key(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return WipeableString(ots_result_string(result))

    def secretSpendKey(self) -> WipeableString:
        """Get the secret spend key of the wallet."""
        result: ots_result_t = ots_wallet_secret_spend_key(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return WipeableString(ots_result_string(result))

    def publicSpendKey(self) -> WipeableString:
        """Get the public spend key of the wallet."""
        result: ots_result_t = ots_wallet_public_spend_key(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return WipeableString(ots_result_string(result))

    def importOutputs(self, outputs: bytes) -> int:
        """Import outputs into the wallet."""
        assert isinstance(outputs, bytes), "outputs must be bytes"
        result: ots_result_t = ots_wallet_import_outputs(self.handle, outputs)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_number(result)

    def exportKeyImages(self) -> bytes:
        """Export key images from the wallet."""
        result: ots_result_t = ots_wallet_export_key_images(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_char_array(result)

    def describeTransaction(self, tx: bytes) -> TxDescription:
        """Describe a transaction."""
        assert isinstance(tx, bytes), "tx must be bytes"
        result: ots_result_t = ots_wallet_describe_tx(self.handle, tx)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return TxDescription(ots_result_handle(result))

    def checkTransaction(self, tx: TxDescription | bytes) -> list[TxWarning]:
        """
        Check if a transaction warnings, if tx is the plain bytes it will
        also check the correctness of the transaction description internally.
        like describeTransaction had called before.

        :information: This method may be removed in the future, as
        TxWarning may be removed. See the documentation for OTS for more details.
        """
        assert isinstance(tx, (TxDescription, bytes)), "tx must be a TxDescription instance or bytes"
        if isinstance(tx, bytes):
            result: ots_result_t = ots_wallet_check_tx_string(self.handle, tx)
            if ots_is_error(result):
                raise OtsException.from_result(result)
            handles: list[ots_handle_t] = ots_result_handle_array(result)
            return [TxWarning(handle) for handle in handles]
        result: ots_result_t = ots_wallet_check_tx(self.handle, tx.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        handles: list[ots_handle_t] = ots_result_handle_array(result)
        return [TxWarning(handle) for handle in handles]

    def signTransaction(self, tx: bytes) -> bytes:
        """Sign a transaction."""
        assert isinstance(tx, bytes), "tx must be bytes"
        result: ots_result_t = ots_wallet_sign_tx(self.handle, tx)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_char_array(result)

    def signData(self, data: bytes) -> bytes:
        """Sign arbitrary data."""
        assert isinstance(data, bytes), "data must be bytes"
        result: ots_result_t = ots_wallet_sign_data(self.handle, data)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_char_array(result)

    def signDataWithIndex(self, data: bytes, account: int, index: int) -> bytes:
        """Sign data with a specific account and index."""
        assert isinstance(data, bytes), "data must be bytes"
        result: ots_result_t = ots_wallet_sign_data_with_index(self.handle, data, account, index)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_char_array(result)

    def signDataWithAddress(self, data: bytes, address: Address | str) -> bytes:
        """Sign data with a specific address."""
        assert isinstance(data, bytes), "data must be bytes"
        assert isstance(address, (Address, str)), "address must be an Address instance or a string"
        if isinstance(address, str):
            result: ots_result_t = ots_wallet_sign_data_with_address_string(self.handle, data, address)
            if ots_is_error(result):
                raise OtsException.from_result(result)
            return ots_result_char_array(result)
        result: ots_result_t = ots_wallet_sign_data_with_address(self.handle, data, address.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_char_array(result)

    def verifyData(self, data: bytes, signature: str | bytes) -> bool:
        """Verify a signature on data."""
        assert isinstance(data, bytes), "data must be bytes"
        assert isinstance(signature, (str, bytes)), "signature must be a string or bytes"
        if isinstance(signature, str):
            signature = signature.encode('utf-8')
        result: ots_result_t = ots_wallet_verify_data(self.handle, data, signature)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    def verifyDataWithIndex(
        self,
        data: bytes,
        account: int,
        index: int,
        signature: str | bytes,
        fallback: bool = False
    ) -> bool:
        """Verify a signature on data with a specific account and index."""
        assert isinstance(data, bytes), "data must be bytes"
        assert isinstance(signature, (str, bytes)), "signature must be a string or bytes"
        if isinstance(signature, str):
            signature = signature.encode('utf-8')
        result: ots_result_t = ots_wallet_verify_data_with_index(
            self.handle,
            data,
            account,
            index,
            signature,
            fallback
        )
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    def verifyDataWithAddress(
        self,
        data: bytes,
        address: Address | str,
        signature: str | bytes,
        fallback: bool = False
    ) -> bool:
        """Verify a signature on data with a specific address."""
        assert isinstance(data, bytes), "data must be bytes"
        assert isinstance(signature, (str, bytes)), "signature must be a string or bytes"
        if isinstance(signature, str):
            signature = signature.encode('utf-8')
        assert isstance(address, (Address, str)), "address must be an Address instance or a string"
        if isinstance(address, str):
            result: ots_result_t = ots_wallet_verify_data_with_address_string(
                self.handle,
                data,
                address,
                signature,
                fallback
            )
            if ots_is_error(result):
                raise OtsException.from_result(result)
            return ots_result_boolean(result)
        result: ots_result_t = ots_wallet_verify_data_with_address(
            self.handle,
            data,
            address.handle,
            signature,
            fallback
        )
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    @classmethod
    def create(cls, key: bytes, network: Network | int = Network.MAIN) -> 'Wallet':
        """
        Create a new wallet with the given key.
        Any random 32-byte key can be used, normally this method is NOT needed,
        except for testing or specific use cases (e.g. you generate/derive the key in
        a different way then the provided seed methods).
        """
        assert isinstance(key, bytes), "key must be bytes"
        assert len(key) == 32, "key must be 32 bytes long"
        assert isinstance(network, (Network, int)), "network must be a Network enum or an integer"
        result: ots_result_t = ots_wallet_create(key, int(network))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        handle: ots_handle_t = ots_result_handle(result)
        return cls(handle)
