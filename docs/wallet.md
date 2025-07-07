# Wallet

The wallet provides all the necessary functionality to generate addresses,
import outputs, export key images, describe unsigned transactions, sign
unsigned transactions, sign and verify data.

## Wallet

<a id="module-ots.wallet"></a>

### *class* ots.wallet.Wallet(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

Represents a monero wallet.

#### \_\_str_\_()

* **Returns:**
  Standard address of the wallet as a string.

#### *property* height *: int*

Get the block height of the wallet.

* **Returns:**
  The block height of the wallet.

#### address(account: int = 0, index: int = 0) → [Address](address.md#ots.address.Address)

Get the address at the specified account and index.
Account 0 and index 0 are the standard address of the wallet.

* **Parameters:**
  * **account** (*int*) – The account number (default is 0).
  * **index** (*int*) – The index of the address in the account (default is 0).

#### accounts(max: int = 10, offset: int = 0) → list[[Address](address.md#ots.address.Address)]

Get a list of addresses in the wallet, with pagination.
Default the first 10 addresses of the accounts starting from offset 0.

* **Parameters:**
  * **max** (*int*) – The number of addresses to return (default is 10).
  * **offset** (*int*) – Offset for pagination (default is 0).

#### subAddresses(account: int = 0, max: int = 10, offset: int = 0) → list[[Address](address.md#ots.address.Address)]

Get a list of sub-addresses for a specific account.
Defaults to the first 10 sub-addresses of account 0 (the wallet).

* **Parameters:**
  * **account** (*int*) – The account number (default is 0).
  * **max** (*int*) – The maximum number of addresses to return (default is 10).

#### hasAddress(address: [Address](address.md#ots.address.Address) | str, maxAccountDepth: int = 0, maxIndexDepth: int = 0) → bool

Check if the wallet contains a specific address, in the
provided maximum account and index depth.

#### IMPORTANT
If maxAccountDepth or maxIndexDepth is set to 0, this values will
be taken from the values set before via
[`ots.ots.Ots.setMaxAccountDepth()`](ots.md#ots.ots.Ots.setMaxAccountDepth) and
[`ots.ots.Ots.setMaxIndexDepth()`](ots.md#ots.ots.Ots.setMaxIndexDepth) or
[`ots.ots.Ots.setMaxDepth()`](ots.md#ots.ots.Ots.setMaxDepth). If this values are not set,
the default values of the OTS library will be used, see
[`ots.ots.Ots.maxAccountDepth()`](ots.md#ots.ots.Ots.maxAccountDepth) and
[`ots.ots.Ots.maxIndexDepth()`](ots.md#ots.ots.Ots.maxIndexDepth) for more details.

#### WARNING
If the address exists in the wallet but the account or index depth
are lower, False will be returned. You want to keep this values
as low as possible but not lower.

Let’s make it clear with an example:

If you have an address at account 1 and index 100, or at
account 10 and address 0, you will get in both cases False
if max account depth is set to 10 and max index depth is set to 100.
Both start with 0, so the first 10 accounts and the first 100 indices,
are from (0, 0) up to (9, 99).

#### NOTE
The max depths are a balance between performance and usability.
On weak hardware raising the max depths can lead to a long search time.
For an offline wallet 10 accounts and 100 indices should be sufficient,
in most cases, but this needs to be addressed in the product.

* **Parameters:**
  * **address** – The address to check, can be an Address instance or a string.
  * **maxAccountDepth** – Maximum account depth to check (default is 0).
  * **maxIndexDepth** – Maximum index depth to check (default is 0).

#### addressIndex(address: [Address](address.md#ots.address.Address) | str, maxAccountDepth: int = 0, maxIndexDepth: int = 0) → tuple[int, int]

Get the account and index of an address in the wallet.

#### SEE ALSO
[`hasAddress()`](#ots.wallet.Wallet.hasAddress) for more details

* **Parameters:**
  * **address** – The address to check, can be an Address instance or a string.
  * **maxAccountDepth** – Maximum account depth to check (default is 0).
  * **maxIndexDepth** – Maximum index depth to check (default is 0).

#### secretViewKey() → [WipeableString](wipeable_string.md#ots.wipeable_string.WipeableString)

Get the secret view key of the wallet.

* **Returns:**
  The secret view key as a WipeableString.

#### publicViewKey() → [WipeableString](wipeable_string.md#ots.wipeable_string.WipeableString)

Get the public view key of the wallet.

* **Returns:**
  The public view key as a WipeableString.

#### secretSpendKey() → [WipeableString](wipeable_string.md#ots.wipeable_string.WipeableString)

Get the secret spend key of the wallet.

* **Returns:**
  The secret spend key as a WipeableString.

#### publicSpendKey() → [WipeableString](wipeable_string.md#ots.wipeable_string.WipeableString)

Get the public spend key of the wallet.

* **Returns:**
  The public spend key as a WipeableString.

#### importOutputs(outputs: bytes) → int

Import outputs into the wallet.

* **Parameters:**
  **outputs** (*bytes*) – The outputs from the view only wallet to import.
* **Returns:**
  The number of outputs imported.

#### exportKeyImages() → bytes

Export key images for the view only wallet.

* **Returns:**
  The key images as bytes.

#### describeTransaction(tx: bytes) → [TxDescription](transaction.md#ots.transaction.TxDescription)

Describe an unsigned transaction.

* **Parameters:**
  **tx** (*bytes*) – The unsigned transaction to describe.

#### checkTransaction(tx: [TxDescription](transaction.md#ots.transaction.TxDescription) | bytes) → list[[TxWarning](transaction.md#ots.transaction.TxWarning)]

Check if a transaction warnings, if tx is the plain bytes it will
also check the correctness of the transaction description internally.
like describeTransaction had called before.

#### WARNING
This method may be removed in the future, as
TxWarning may be removed. See the documentation for OTS for more details.

* **Parameters:**
  **tx** ([*TxDescription*](transaction.md#ots.transaction.TxDescription) *|* *bytes*) – The transaction to check, can be a TxDescription instance or bytes.
* **Returns:**
  A list of TxWarning instances.

#### signTransaction(tx: bytes) → bytes

Sign an unsigned transaction from the hot wallet (view only).

* **Parameters:**
  **tx** (*bytes*) – The unsigned transaction to sign.
* **Returns:**
  The signed transaction as bytes.

#### signData(data: bytes | str) → str

Sign arbitrary data, with the standard address of the wallet.

* **Parameters:**
  **data** (*bytes* *|* *str*) – The data to sign.
* **Returns:**
  The signature as a string.

#### signDataWithIndex(data: bytes | str, account: int, index: int) → str

Sign data with a specific account and index.
The account and index are used to determine the address to sign with.

* **Parameters:**
  * **data** (*bytes* *|* *str*) – The data to sign.
  * **account** (*int*) – The account number to use for signing.
  * **index** (*int*) – The index of the address in the account to use for signing.
* **Returns:**
  The signature as a string.

#### signDataWithAddress(data: bytes | str, address: [Address](address.md#ots.address.Address) | str) → str

Sign data with a specific address.

* **Parameters:**
  * **data** (*bytes* *|* *str*) – The data to sign.
  * **address** ([*Address*](address.md#ots.address.Address) *|* *str*) – The address to sign with, can be an Address instance or a string.
* **Returns:**
  The signature as a string.

#### verifyData(data: bytes | str, signature: str | bytes) → bool

Verify a signature on data for the standard address of the wallet.

#### SEE ALSO
[`ots.ots.Ots.verifyData()`](ots.md#ots.ots.Ots.verifyData) to verify data with a foreign address.

* **Parameters:**
  * **data** (*bytes* *|* *str*) – The data to verify.
  * **signature** (*str* *|* *bytes*) – The signature to verify.
* **Returns:**
  True if the signature is valid, False otherwise.

#### verifyDataWithIndex(data: bytes | str, account: int, index: int, signature: str | bytes, fallback: bool = False) → bool

Verify a signature on data with a specific account and index of the wallet.

* **Parameters:**
  * **data** (*bytes* *|* *str*) – The data to verify.
  * **account** (*int*) – The account number to use for verification.
  * **index** (*int*) – The index of the address in the account to use for verification.
  * **signature** (*str* *|* *bytes*) – The signature to verify.
  * **fallback** (*bool*) – If True, will fallback to the standard address if the account and index are not found.
* **Returns:**
  True if the signature is valid, False otherwise.

#### verifyDataWithAddress(data: bytes | str, address: [Address](address.md#ots.address.Address) | str, signature: str | bytes, fallback: bool = False) → bool

Verify a signature on data with a specific address.

* **Parameters:**
  * **data** (*bytes* *|* *str*) – The data to verify.
  * **address** ([*Address*](address.md#ots.address.Address) *|* *str*) – The address to verify with, can be an Address instance or a string.
  * **signature** (*str* *|* *bytes*) – The signature to verify.
  * **fallback** (*bool*) – If True, will fallback to the standard address if the address is not found.
* **Returns:**
  True if the signature is valid, False otherwise.

#### *classmethod* create(key: bytes, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN) → [Wallet](#ots.wallet.Wallet)

Create a new wallet with the given key.
Any random 32-byte key can be used, normally this method is NOT needed,
except for testing or specific use cases (e.g. you generate/derive the key in
a different way then the provided seed methods).

* **Parameters:**
  * **key** (*bytes*) – The 32-byte key to use for the wallet.
  * **network** – The network to use for the wallet, defaults to Network.MAIN.
* **Type:**
  network: Network | int
* **Returns:**
  A new Wallet instance.
