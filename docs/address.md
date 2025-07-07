# Address

Any [`ots.address.Address`](#ots.address.Address) object represents a valid Monero address. To handle
unknown addresses [`ots.address.AddressString`](#ots.address.AddressString) can be used.

#### SEE ALSO
Monero Docs

[Address types](https://docs.getmonero.org/public-address/)
about Standard address, Subaddress, and Integrated addresses.

## Address

### *class* ots.address.Address(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

Represents any valid Monero address.

#### \_\_init_\_(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

Initializes the Monero Address object with a handle.

* **Parameters:**
  **handle** ([*ots_handle_t*](raw.md#ots.raw.ots_handle_t)) – The handle to the address. It must be of type HandleType.ADDRESS.

#### \_\_str_\_() → str

* **Returns:**
  base58 representation of the address.

#### \_\_len_\_() → int

* **Returns:**
  base58 length of the address.

#### \_\_eq_\_(other: object) → bool

Checks if two Address objects are equal.

* **Parameters:**
  **other** ([*Address*](#ots.address.Address) *|* *str*) – The other Address object to compare with. The other object needs to be either an [`Address`](#ots.address.Address) object or a `str`.
* **Returns:**
  True if the addresses are equal, False otherwise.

#### *property* type *: [AddressType](enums.md#ots.enums.AddressType)*

* **Returns:**
  The AddressType of the address.

#### *property* network *: [Network](enums.md#ots.enums.Network)*

* **Returns:**
  The Network of the address.

#### *property* fingerprint *: str*

* **Returns:**
  The fingerprint of the address.

#### *property* isIntegrated *: bool*

Checks if the address is an integrated address.

* **Returns:**
  True if the address is integrated, False otherwise.

#### *property* paymentId *: str*

Returns the payment ID of the address if it is an integrated address.

* **Returns:**
  The payment ID of the address.

#### *property* base58 *: str*

Returns the base58 representation of the address.

* **Returns:**
  The base58 string representation of the address.

#### *property* length *: int*

Returns the length of the address.

* **Returns:**
  The length of the base58 address.

#### *classmethod* fromString(address: str) → [Address](#ots.address.Address)

Creates an Address object from a string representation of the address.

* **Parameters:**
  **address** (*str*) – The string representation of the address.
* **Returns:**
  An Address object.

#### *classmethod* fromIntegrated(address: [Address](#ots.address.Address)) → [Address](#ots.address.Address)

Creates an Address object from an integrated address.

* **Parameters:**
  **address** ([*Address*](#ots.address.Address)) – The integrated address.
* **Returns:**
  An Address object.

## AddressString

### *class* ots.address.AddressString

An helper class for handling Monero address strings,
without creating an Address object.

#### *classmethod* valid(address: str, network: [Network](enums.md#ots.enums.Network) | int) → bool

Checks if the given address string is a valid Monero address.

* **Parameters:**
  * **address** (*str*) – The address string to validate.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network to validate against.
* **Returns:**
  True if the address is valid, False otherwise.

#### *classmethod* network(address: str) → [Network](enums.md#ots.enums.Network)

Returns the network for the given address string.

* **Parameters:**
  **address** (*str*) – The address string.
* **Returns:**
  The Network of the address.

#### *classmethod* type(address: str) → [AddressType](enums.md#ots.enums.AddressType)

Returns the type of the address for the given address string.

* **Parameters:**
  **address** (*str*) – The address string.
* **Returns:**
  The AddressType of the address.

#### *classmethod* fingerprint(address: str) → str

Returns the fingerprint of the address for the given address string.

* **Parameters:**
  **address** (*str*) – The address string.
* **Returns:**
  The fingerprint of the address.

#### *classmethod* isIntegrated(address: str) → bool

Checks if the address string is an integrated address.

* **Parameters:**
  **address** (*str*) – The address string.
* **Returns:**
  True if the address is integrated, False otherwise.
