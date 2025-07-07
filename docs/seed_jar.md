# SeedJar

The Seed Jar keeps the seeds in a secure place and provides methods to access them.
If the seed jar is used there is no need to have a list or other construct to hold the
seed in memory. There is only one instance of [`ots.seed_jar.SeedJar`](#ots.seed_jar.SeedJar) and
all methods are static.

So as long the library is in use the seeds are in memory, and can be accessed
in any module.

## SeedJar

### *class* ots.seed_jar.SeedJar

A class to manage a jar of seeds. It provides methods to add, remove, purge,
transfer, and query seeds in the jar. All methods are static.

#### *static* add(seed: [Seed](seed.md#ots.seed.Seed), name: str) → [Seed](seed.md#ots.seed.Seed)

Add a seed to the jar with a given name.

* **Parameters:**
  * **seed** ([*Seed*](seed.md#ots.seed.Seed)) – The seed to add.
  * **name** (*str*) – The name to associate with the seed.
* **Returns:**
  The reference to the added seed. Now you can dispose the provided seed.

#### *static* remove(seed: [Seed](seed.md#ots.seed.Seed)) → bool

Remove a seed from the jar.

* **Parameters:**
  **seed** ([*Seed*](seed.md#ots.seed.Seed)) – The seed to remove.
* **Returns:**
  True if the seed was successfully removed, False otherwise.

#### *static* purgeForIndex(index: int) → bool

Purge the seed jar for a specific index.

* **Parameters:**
  **index** (*int*) – The index of the seed to purge.
* **Returns:**
  True if the seed was successfully purged, False otherwise.

#### *static* purgeForName(name: str) → bool

Purge the seed jar for a specific name.

* **Parameters:**
  **name** (*str*) – The name of the seed to purge.
* **Returns:**
  True if the seed was successfully purged, False otherwise.

#### *static* purgeForFingerprint(fingerprint: str) → bool

Purge the seed jar for a specific fingerprint.

* **Parameters:**
  **fingerprint** (*str*) – The fingerprint of the seed to purge.
* **Returns:**
  True if the seed was successfully purged, False otherwise.

#### *static* purgeForAddress(address: str) → bool

Purge the seed jar for a specific address.

* **Parameters:**
  **address** (*str*) – The address of the seed to purge.
* **Returns:**
  True if the seed was successfully purged, False otherwise.

#### *static* transferIn(seed: [Seed](seed.md#ots.seed.Seed) | [ots_handle_t](raw.md#ots.raw.ots_handle_t), name: str) → [Seed](seed.md#ots.seed.Seed)

Transfer a seed into the jar with a given name.

* **Parameters:**
  * **seed** ([*Seed*](seed.md#ots.seed.Seed) *|* [*ots_handle_t*](raw.md#ots.raw.ots_handle_t)) – The seed to transfer in. Don’t use the provided seed after this operation, because it will be wiped.
  * **name** (*str*) – The name to associate with the seed.
* **Returns:**
  The reference to the transferred seed. The provided seed is now wiped.

#### *static* transferOut(seed: [Seed](seed.md#ots.seed.Seed) | [ots_handle_t](raw.md#ots.raw.ots_handle_t)) → [Seed](seed.md#ots.seed.Seed)

Transfer a seed out of the jar.

* **Parameters:**
  **seed** ([*Seed*](seed.md#ots.seed.Seed) *|* [*ots_handle_t*](raw.md#ots.raw.ots_handle_t)) – The seed to transfer out. Don’t use the provided seed after this operation, because it is a reference to the seed in the jar, which will be removed.
* **Returns:**
  The seed object that owns the handle to the seed now, it is not anymore in the jar.

#### *static* transferOutForIndex(index: int) → [Seed](seed.md#ots.seed.Seed)

Transfer a seed out of the jar for a specific index.

* **Parameters:**
  **index** (*int*) – The index of the seed to transfer out.
* **Returns:**
  The seed object that owns the handle to the seed now, it is not anymore in the jar.

#### *static* transferOutForName(name: str) → [Seed](seed.md#ots.seed.Seed)

Transfer a seed out of the jar for a specific name.

* **Parameters:**
  **name** (*str*) – The name of the seed to transfer out.
* **Returns:**
  The seed object that owns the handle to the seed now, it is not anymore in the jar.

#### *static* transferOutForFingerprint(fingerprint: str) → [Seed](seed.md#ots.seed.Seed)

Transfer a seed out of the jar for a specific fingerprint.

* **Parameters:**
  **fingerprint** (*str*) – The fingerprint of the seed to transfer out.
* **Returns:**
  The seed object that owns the handle to the seed now, it is not anymore in the jar.

#### *static* transferOutForAddress(address: str) → [Seed](seed.md#ots.seed.Seed)

Transfer a seed out of the jar for a specific address.

* **Parameters:**
  **address** (*str*) – The address of the seed to transfer out.
* **Returns:**
  The seed object that owns the handle to the seed now, it is not anymore in the jar.

#### *static* clear() → bool

Clear the seed jar.

* **Returns:**
  True if the jar was successfully cleared, False otherwise.

#### *static* seeds() → list[[Seed](seed.md#ots.seed.Seed)]

Get a list of all seeds in the jar.

#### IMPORTANT
The returned list contains references to the seeds in the jar.
The seeds have no ownership of the underlaying handles, the ownership
is still with the jar.
The seeds objects can be disposed any moment without consequences,
and accessed later through the jar methods again.

* **Returns:**
  A list of Seed objects referencing the seeds in the jar.

#### *static* count() → int

Get the count of seeds in the jar.

* **Returns:**
  The number of seeds in the jar.

#### *static* forIndex(idx: int) → [Seed](seed.md#ots.seed.Seed)

Get a seed by its index in the jar.

* **Parameters:**
  **idx** (*int*) – The index of the seed to retrieve.
* **Returns:**
  The Seed object with the reference to the seed in the jar.

#### *static* forFingerprint(fingerprint: str) → [Seed](seed.md#ots.seed.Seed)

Get a seed by its fingerprint.

* **Parameters:**
  **fingerprint** (*str*) – The fingerprint of the seed to retrieve.
* **Returns:**
  The Seed object with the reference to the seed in the jar.

#### *static* forAddress(address: str) → [Seed](seed.md#ots.seed.Seed)

Get a seed by its address.

* **Parameters:**
  **address** (*str*) – The address of the seed to retrieve.
* **Returns:**
  The Seed object with the reference to the seed in the jar.

#### *static* forName(name: str) → [Seed](seed.md#ots.seed.Seed)

Get a seed by its name.

* **Parameters:**
  **name** (*str*) – The name of the seed to retrieve.
* **Returns:**
  The Seed object with the reference to the seed in the jar.

#### *static* name(seed: [Seed](seed.md#ots.seed.Seed) | [ots_handle_t](raw.md#ots.raw.ots_handle_t)) → str

Get the name of a seed. (This is the name that was given when the seed was added to the jar.)

* **Parameters:**
  **seed** ([*Seed*](seed.md#ots.seed.Seed) *|* [*ots_handle_t*](raw.md#ots.raw.ots_handle_t)) – The seed to get the name for.
* **Returns:**
  The name of the seed.

#### *static* rename(seed: [Seed](seed.md#ots.seed.Seed) | [ots_handle_t](raw.md#ots.raw.ots_handle_t), new_name: str) → bool

Rename a seed in the jar.

* **Parameters:**
  * **seed** ([*Seed*](seed.md#ots.seed.Seed) *|* [*ots_handle_t*](raw.md#ots.raw.ots_handle_t)) – The seed to rename.
  * **new_name** (*str*) – The new name for the seed.
* **Returns:**
  True if the seed was successfully renamed, False otherwise.

#### *static* itemName(index: int) → str

Get the name of a seed by its index in the jar. (The name that was given when the seed was added to the jar.)

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The name of the seed at the specified index.

#### *static* itemFingerprint(index: int) → str

Get the fingerprint of a seed by its index in the jar.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The fingerprint of the seed at the specified index.

#### *static* itemAddress(index: int) → [Address](address.md#ots.address.Address)

Get the address of a seed by its index in the jar.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The Address object of the seed at the specified index.

#### *static* itemAddressString(index: int) → str

Get the address string of a seed by its index in the jar.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The address string of the seed at the specified index.

#### *static* itemSeedType(index: int) → [SeedType](enums.md#ots.enums.SeedType)

Get the seed type of a seed by its index in the jar.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The SeedType of the seed at the specified index.

#### *static* itemSeedTypeString(index: int) → str

Get the seed type string of a seed by its index in the jar.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The seed type as string of the seed at the specified index.

#### *static* itemIsLegacy(index: int) → bool

Check if a seed at a specific index is legacy.

#### NOTE
Only relevant to Monero seeds, this are monero seeds
which have only 12/13 words.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  True if the seed is legacy, False otherwise.

#### *static* itemNetwork(index: int) → [Network](enums.md#ots.enums.Network)

Get the network of a seed by its index in the jar.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The Network object of the seed at the specified index.

#### *static* itemNetworkString(index: int) → str

Get the network string of a seed by its index in the jar.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The network as string of the seed at the specified index.

#### *static* itemHeight(index: int) → int

Get the creation height of a seed by its index in the jar.

#### NOTE
On Monero seeds this is the absolut block height
on which the seed was created, on Polyseed this
is an estimated values based on timestamp.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The height of the seed at the specified index.

#### *static* itemTimestamp(index: int) → int

Get the timestamp of a seed by its index in the jar.

#### NOTE
On Monero seeds this is timestamp is an estimated value
based on the creation height, on Polyseed this is
the timestamp encoded on creation into the polyseed.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The timestamp of the seed at the specified index.

#### *static* itemTime(index: int) → datetime

Get the datetime of a seed by its index in the jar.

#### NOTE
This is purely a convenience method to get
the timestamp as a datetime object.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The datetime of the seed at the specified index.

#### *static* items() → list[[SeedJarItem](#ots.seed_jar.SeedJarItem)]

Get a list of all items in the seed jar. This list is
purely a convenience method to get the meta data of all
seeds in the jar. To make rendering a list of seeds easier.

* **Returns:**
  A list of SeedJarItem objects representing the seeds meta data in the jar.

#### *static* itemWallet(index: int) → [Wallet](wallet.md#ots.wallet.Wallet)

Get the wallet of a seed by its index in the jar.

* **Parameters:**
  **index** (*int*) – The index of the seed in the jar.
* **Returns:**
  The Wallet object (only a reference) of the seed at the specified index.

## SeedJarItem

### *class* ots.seed_jar.SeedJarItem(index: int, name: str, fingerprint: str, address: str, type: [SeedType](enums.md#ots.enums.SeedType), type_string: str, network: [Network](enums.md#ots.enums.Network), network_string: str, height: int, timestamp: int, time: datetime)

A data class representing an item in the seed jar.

* **Parameters:**
  * **index** (*int*) – The index of the seed in the jar.
  * **name** (*str*) – The name of the seed.
  * **fingerprint** (*str*) – The fingerprint of the seed.
  * **address** (*str*) – The address associated with the seed.
  * **type** ([*SeedType*](enums.md#ots.enums.SeedType)) – The type of the seed.
  * **type_string** (*str*) – The type of the seed as a string.
  * **network** ([*Network*](enums.md#ots.enums.Network)) – The network of the seed.
  * **network_string** (*str*) – The network of the seed as a string.
  * **height** (*int*) – The creation height of the seed.
  * **timestamp** (*int*) – The timestamp when the seed was created.
  * **time** (*datetime*) – The datetime when the seed was created.

#### index *: int*

The index of the seed in the jar.

#### name *: str*

The name of the seed.

#### fingerprint *: str*

The fingerprint of the seed.

#### address *: str*

The standard address of the seed.

#### type *: [SeedType](enums.md#ots.enums.SeedType)*

The type of the seed.

#### type_string *: str*

The type of the seed as a string.

#### network *: [Network](enums.md#ots.enums.Network)*

The network of the seed.

#### network_string *: str*

The network of the seed as a string.

#### height *: int*

The creation height of the seed.

#### timestamp *: int*

The timestamp when the seed was created.

#### time *: datetime*

The date and time when the seed was created.
