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
        """
        Initializes the Wallet with a handle.

        :param ots_handle_t handle: The handle to the wallet. Must be of type ots_handle_t.
        """
        assert isinstance(handle, ots_handle_t), "handle must be of type ots_handle_t"
        assert handle.type == HandleType.WALLET, "handle must be of type HandleType.WALLET"
        self.handle: ots_handle_t = handle
        self._height: int | None = None
        self._addresses: dict[tuple[int, int], Address] = {}

    def __str__(self):
        """
        :return: Standard address of the wallet as a string.
        """
        return str(self.address())

    def __repr__(self):
        """
        :return: String representation of the wallet.
        :meta private:
        """
        return f"Wallet({str(self)})"

    @property
    def height(self) -> int:
        """
        Get the block height of the wallet.

        :return: The block height of the wallet.
        """
        if self._height is None:
            self._height = ots_wallet_height(self.handle)
        return self._height

    def address(self, account: int = 0, index: int = 0) -> Address:
        """
        Get the address at the specified account and index.
        Account 0 and index 0 are the standard address of the wallet.

        :param int account: The account number (default is 0).
        :param int index: The index of the address in the account (default is 0).
        """
        key = (account, index)
        if key not in self._addresses:
            self._addresses[key] = Address(
                ots_result_handle(
                    ots_wallet_subaddress(self.handle, account, index)
                )
            )
        return self._addresses[key]

    def accounts(self, max: int = 10, offset: int = 0) -> list[Address]:
        """
        Get a list of addresses in the wallet, with pagination.
        Default the first 10 addresses of the accounts starting from offset 0.

        :param int max: The number of addresses to return (default is 10).
        :param int offset: Offset for pagination (default is 0).
        """
        result: ots_result_t = ots_wallet_accounts(self.handle, max, offset)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        addressHandles = ots_result_handle_array(result)
        return [Address(handle) for handle in addressHandles]

    def subAddresses(self, account: int = 0, max: int = 10, offset: int = 0) -> list[Address]:
        """
        Get a list of sub-addresses for a specific account.
        Defaults to the first 10 sub-addresses of account 0 (the wallet).

        :param int account: The account number (default is 0).
        :param int max: The maximum number of addresses to return (default is 10).
        """
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
        """
        Check if the wallet contains a specific address, in the
        provided maximum account and index depth.

        .. important::

            If `maxAccountDepth` or `maxIndexDepth` is set to 0, this values will
            be taken from the values set before via
            :py:meth:`ots.ots.Ots.setMaxAccountDepth` and
            :py:meth:`ots.ots.Ots.setMaxIndexDepth` or
            :py:meth:`ots.ots.Ots.setMaxDepth`. If this values are not set,
            the default values of the OTS library will be used, see
            :py:meth:`ots.ots.Ots.maxAccountDepth` and
            :py:meth:`ots.ots.Ots.maxIndexDepth` for more details.

        .. warning::

            If the address exists in the wallet but the account or index depth
            are lower, `False` will be returned. You want to keep this values
            as low as possible but not lower.

            Let's make it clear with an example:

            If you have an address at account 1 and index 100, or at
            account 10 and address 0, you will get in both cases `False`
            if max account depth is set to 10 and max index depth is set to 100.
            Both start with 0, so the first 10 accounts and the first 100 indices,
            are from (0, 0) up to (9, 99).

        .. note::

            The max depths are a balance between performance and usability.
            On weak hardware raising the max depths can lead to a long search time.
            For an offline wallet 10 accounts and 100 indices should be sufficient,
            in most cases, but this needs to be addressed in the product.

        :param address: The address to check, can be an Address instance or a string.
        :param maxAccountDepth: Maximum account depth to check (default is 0).
        :param maxIndexDepth: Maximum index depth to check (default is 0).
        """
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
        """
        Get the account and index of an address in the wallet.

        .. seealso:: :py:meth:`hasAddress` for more details

        :param address: The address to check, can be an Address instance or a string.
        :param maxAccountDepth: Maximum account depth to check (default is 0).
        :param maxIndexDepth: Maximum index depth to check (default is 0).
        """
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
        """
        Get the secret view key of the wallet.

        :return: The secret view key as a WipeableString.
        """
        result: ots_result_t = ots_wallet_secret_view_key(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return WipeableString(ots_result_string(result))

    def publicViewKey(self) -> WipeableString:
        """
        Get the public view key of the wallet.

        :return: The public view key as a WipeableString.
        """
        result: ots_result_t = ots_wallet_public_view_key(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return WipeableString(ots_result_string(result))

    def secretSpendKey(self) -> WipeableString:
        """
        Get the secret spend key of the wallet.

        :return: The secret spend key as a WipeableString.
        """
        result: ots_result_t = ots_wallet_secret_spend_key(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return WipeableString(ots_result_string(result))

    def publicSpendKey(self) -> WipeableString:
        """
        Get the public spend key of the wallet.

        :return: The public spend key as a WipeableString.
        """
        result: ots_result_t = ots_wallet_public_spend_key(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return WipeableString(ots_result_string(result))

    def importOutputs(self, outputs: bytes) -> int:
        """
        Import outputs into the wallet.

        :param bytes outputs: The outputs from the view only wallet to import.
        :return: The number of outputs imported.
        """
        assert isinstance(outputs, bytes), "outputs must be bytes"
        result: ots_result_t = ots_wallet_import_outputs(self.handle, outputs)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_number(result)

    def exportKeyImages(self) -> bytes:
        """
        Export key images for the view only wallet.

        :return: The key images as bytes.
        """
        result: ots_result_t = ots_wallet_export_key_images(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_char_array(result)

    def describeTransaction(self, tx: bytes) -> TxDescription:
        """
        Describe an unsigned transaction.

        :param bytes tx: The unsigned transaction to describe.
        """
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

        .. warning::

            This method may be removed in the future, as
            TxWarning may be removed. See the documentation for OTS for more details.

        :param tx: The transaction to check, can be a TxDescription instance or bytes.
        :type tx: TxDescription | bytes
        :return: A list of TxWarning instances.
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
        """
        Sign an unsigned transaction from the hot wallet (view only).

        :param bytes tx: The unsigned transaction to sign.
        :return: The signed transaction as bytes.
        """
        assert isinstance(tx, bytes), "tx must be bytes"
        result: ots_result_t = ots_wallet_sign_tx(self.handle, tx)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_char_array(result)

    def signData(self, data: bytes | str) -> str:
        """
        Sign arbitrary data, with the standard address of the wallet.

        :param data: The data to sign.
        :type data: bytes | str
        :return: The signature as a string.
        """
        assert isinstance(data, (bytes, str)), "data must be bytes or a string"
        if isinstance(data, str):
            data = data.encode('utf-8')
        result: ots_result_t = ots_wallet_sign_data(self.handle, data)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_string(result)

    def signDataWithIndex(
        self,
        data: bytes | str,
        account: int,
        index: int
    ) -> str:
        """
        Sign data with a specific account and index.
        The account and index are used to determine the address to sign with.

        :param data: The data to sign.
        :type data: bytes | str
        :param int account: The account number to use for signing.
        :param int index: The index of the address in the account to use for signing.
        :return: The signature as a string.
        """
        assert isinstance(data, (bytes, str)), "data must be bytes or a string"
        if isinstance(data, str):
            data = data.encode('utf-8')
        result: ots_result_t = ots_wallet_sign_data_with_index(
            self.handle,
            data,
            account,
            index
        )
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_char_array(result)

    def signDataWithAddress(
        self,
        data: bytes | str,
        address: Address | str
    ) -> str:
        """
        Sign data with a specific address.

        :param data: The data to sign.
        :type data: bytes | str
        :param address: The address to sign with, can be an Address instance or a string.
        :type address: Address | str
        :return: The signature as a string.
        """
        assert isinstance(data, (bytes, str)), "data must be bytes or a string"
        assert isstance(address, (Address, str)), "address must be an Address instance or a string"
        if isinstance(data, str):
            data = data.encode('utf-8')
        if isinstance(address, str):
            result: ots_result_t = ots_wallet_sign_data_with_address_string(
                self.handle,
                data,
                address
            )
            if ots_is_error(result):
                raise OtsException.from_result(result)
            return ots_result_char_array(result)
        result: ots_result_t = ots_wallet_sign_data_with_address(
            self.handle,
            data,
            address.handle
        )
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_char_array(result)

    def verifyData(
        self,
        data: bytes | str,
        signature: str | bytes
    ) -> bool:
        """
        Verify a signature on data for the standard address of the wallet.

        .. seealso:: :py:meth:`ots.ots.Ots.verifyData` to verify data with a foreign address.

        :param data: The data to verify.
        :type data: bytes | str
        :param signature: The signature to verify.
        :type signature: str | bytes
        :return: True if the signature is valid, False otherwise.
        """
        assert isinstance(data, (bytes, str)), "data must be bytes or a string"
        assert isinstance(signature, (str, bytes)), "signature must be a string or bytes"
        if isinstance(data, str):
            data = data.encode('utf-8')
        if isinstance(signature, bytes):
            signature = signature.decode('utf-8')
        result: ots_result_t = ots_wallet_verify_data(self.handle, data, signature)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    def verifyDataWithIndex(
        self,
        data: bytes | str,
        account: int,
        index: int,
        signature: str | bytes,
        fallback: bool = False
    ) -> bool:
        """
        Verify a signature on data with a specific account and index of the wallet.

        :param data: The data to verify.
        :type data: bytes | str
        :param int account: The account number to use for verification.
        :param int index: The index of the address in the account to use for verification.
        :param signature: The signature to verify.
        :type signature: str | bytes
        :param bool fallback: If True, will fallback to the standard address if the account and index are not found.
        :return: True if the signature is valid, False otherwise.
        """
        assert isinstance(data, (bytes, str)), "data must be bytes or a string"
        assert isinstance(signature, (str, bytes)), "signature must be a string or bytes"
        if isinstance(data, str):
            data = data.encode('utf-8')
        if isinstance(signature, bytes):
            signature = signature.decode('utf-8')
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
        data: bytes | str,
        address: Address | str,
        signature: str | bytes,
        fallback: bool = False
    ) -> bool:
        """
        Verify a signature on data with a specific address.

        :param data: The data to verify.
        :type data: bytes | str
        :param address: The address to verify with, can be an Address instance or a string.
        :type address: Address | str
        :param signature: The signature to verify.
        :type signature: str | bytes
        :param bool fallback: If True, will fallback to the standard address if the address is not found.
        :return: True if the signature is valid, False otherwise.
        """
        assert isinstance(data, (bytes, str)), "data must be bytes or a string"
        assert isinstance(signature, (str, bytes)), "signature must be a string or bytes"
        if isinstance(data, str):
            data = data.encode('utf-8')
        if isinstance(signature, bytes):
            signature = signature.decode('utf-8')
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

        :param bytes key: The 32-byte key to use for the wallet.
        :param network: The network to use for the wallet, defaults to Network.MAIN.
        :type: network: Network | int
        :return: A new Wallet instance.
        """
        assert isinstance(key, bytes), "key must be bytes"
        assert len(key) == 32, "key must be 32 bytes long"
        assert isinstance(network, (Network, int)), "network must be a Network enum or an integer"
        result: ots_result_t = ots_wallet_create(key, int(network))
        if ots_is_error(result):
            raise OtsException.from_result(result)
        handle: ots_handle_t = ots_result_handle(result)
        return cls(handle)
