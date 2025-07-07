# Seeds

Seed are essentially random bytes that are used to derive keys for the Wallet. In this library, the assumption is that this seeds are generally represented by seed phrases.

Monero Seeds ([`ots.seed.MoneroSeed`](#ots.seed.MoneroSeed)) are represented by a Monero seed phrase, and an optional passphrase for a seed offset. With this information you can restore the offline Wallet. This seed phrase consists of 24 words of the Monero word list include in the Monero source code. A 25th word is appened as a checksum.

Legacy Seeds ([`ots.seed.LegacySeed`](#ots.seed.LegacySeed)) are essentially Monero Seeds, but they represented by only 12 words (and so only half the entropy). They are used by the legacy Monero Wallets, and can be restored ([`ots.seed.LegacySeed.decode()`](#ots.seed.LegacySeed.decode)) in this library, but can not be created or generated. A 13th word is appened as a checksum. Legacy Seeds are only supported for restoring existing Wallets, and not for creating new ones! This is done on purpose!

Polyseeds ([`ots.seed.Polyseed`](#ots.seed.Polyseed)) are a new type of seed that is used to derive keys for the Wallet. They are represented by a seed phrase consisting of 16 words. While Monero Seeds can be generated from the wallets secret bytes, Polyseeds are one way only, once the seed phrase is generated, the Polyseed will derive the key, the coin type (Not only Monero), the estimated creation time, from which the block height is derived. A Polyseed can be converted to a Monro Seed, but not the other way around.

On creating a new Seed, or decoding(restoring) an exiting seed the related classes ([`ots.seed.MoneroSeed`](#ots.seed.MoneroSeed), [`ots.seed.LegacySeed`](#ots.seed.LegacySeed), [`ots.seed.Polyseed`](#ots.seed.Polyseed)) will be used. And return a related object. In the python wrapper seeds out of the seed jar are not objects of the related classes but rather simply Seed [`ots.seed.Seed`](#ots.seed.Seed) objects. [`ots.seed.Seed`](#ots.seed.Seed) provides all necessary methods and also the properties [`ots.seed.Seed.type`](#ots.seed.Seed.type), returning with [`ots.enums.SeedType.MONERO`](enums.md#ots.enums.SeedType.MONERO) or [`ots.enums.SeedType.POLYSEED`](enums.md#ots.enums.SeedType.POLYSEED) depending on the type of the seed. Further through the property [`ots.seed.Seed.isLegacy`](#ots.seed.Seed.isLegacy) it can be checked if the seed is a legacy seed or not on a seed representing a monero seed.

The seed classes provide methods to encode and decode the seed phrase, encode and decode seed indices (numbers instead of words), and also provide the wallet to execute actions on the wallet like creating addresses, import outputs, export key images, check unsigned transactions, sign transactions and arbitrary data.

## Seed

### *class* ots.seed.Seed(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

Bases: `object`

Seed class to handle the seed data.

#### \_\_str_\_()

* **Returns:**
  The fingerprint of the seed.

#### *property* address *: [Address](address.md#ots.address.Address)*

Returns the standard address of the seed.

* **Returns:**
  An Address object representing the seed’s address.

#### *property* fingerprint *: str*

Returns the fingerprint of the seed.

* **Returns:**
  A last 6 digit upper case hex string from sha256(base58 standard addres) representing the fingerprint of the seed.

#### *property* height *: int*

Returns the height of the seed.

* **Returns:**
  An integer representing the height of the seed.

#### indices(password: str = '') → [SeedIndices](seed_indices.md#ots.seed_indices.SeedIndices)

Returns the seed indices.

* **Parameters:**
  **password** – Optional password to decrypt the seed indices. Not supported for legacy seeds.
* **Returns:**
  A SeedIndices object containing the seed indices.

#### *property* isLegacy *: bool*

Checks if the seed is a legacy seed.

* **Returns:**
  True if the seed is a legacy seed, False otherwise.

#### *property* network *: [Network](enums.md#ots.enums.Network)*

Returns the network of the seed.

* **Returns:**
  A Network enum representing the network of the seed.

#### phrase(language: [SeedLanguage](seed_language.md#ots.seed_language.SeedLanguage), password: str = '') → [WipeableString](wipeable_string.md#ots.wipeable_string.WipeableString)

Returns the seed phrase in the specified language.

* **Parameters:**
  * **language** – The language of the seed phrase.
  * **password** – Optional password to encrypt the seed phrase. Not supported for legacy seeds. Works different on Monero Seeds and Polyseeds. While on Monero Seeds the password is the offset passphrase, on a Polyseed it is the actual password. Polyseed also support passphrase offset, but needs to be set on creating the Polyseed and decoding the polyseed. While on the Monero Seed password (offset passphrase in this case) is substracted on generating the seed phrase, before generating the seed phrase.
* **Returns:**
  A WipeableString containing the seed phrase.

#### *property* time *: datetime*

Returns the time of the seed as a datetime object.

* **Returns:**
  A datetime object representing the time of the seed.

#### *property* timestamp *: int*

Returns the timestamp of the seed.

* **Returns:**
  An integer representing the timestamp of the seed.

#### *property* type *: [SeedType](enums.md#ots.enums.SeedType)*

* **Returns:**
  The type of the seed.

#### *property* wallet *: [Wallet](wallet.md#ots.wallet.Wallet)*

Returns the wallet associated with the seed.

* **Returns:**
  A Wallet object representing the seed’s wallet.

## LegacySeed

### *class* ots.seed.LegacySeed(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

Bases: [`Seed`](#ots.seed.Seed)

LegacySeed class to handle Monero 12/13 word legacy seeds.

#### *classmethod* decode(phrase: str, height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) = Network.MAIN) → [LegacySeed](#ots.seed.LegacySeed)

Decodes a legacy seed phrase into a LegacySeed object.

* **Parameters:**
  * **phrase** – The seed phrase to decode.
  * **height** – The block height associated with the seed.
  * **time** – The timestamp associated with the seed.
  * **network** – The network type for the seed.
* **Returns:**
  A LegacySeed object containing the decoded seed data.

#### *classmethod* decodeIndices(indices: [SeedIndices](seed_indices.md#ots.seed_indices.SeedIndices), height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) = Network.MAIN) → [LegacySeed](#ots.seed.LegacySeed)

Decodes seed indices into a LegacySeed object.

* **Parameters:**
  * **indices** – The SeedIndices object to decode.
  * **height** – The block height associated with the seed.
  * **time** – The timestamp associated with the seed.
  * **network** – The network type for the seed.
* **Returns:**
  A LegacySeed object containing the decoded seed data.

## MoneroSeed

### *class* ots.seed.MoneroSeed(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

Bases: [`Seed`](#ots.seed.Seed)

MoneroSeed class to handle Monero 24/25 word seeds.

#### *classmethod* create(random: bytes, height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) = Network.MAIN) → [MoneroSeed](#ots.seed.MoneroSeed)

Creates a new MoneroSeed instance.

* **Parameters:**
  * **random** – 32 bytes of random data to create the seed.
  * **height** – The block height associated with the seed.
  * **time** – The timestamp associated with the seed.
  * **network** – The network type for the seed.
* **Returns:**
  A MoneroSeed object containing the created seed data.

#### *classmethod* decode(phrase: str, height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) = Network.MAIN, passphrase: str = '') → [MoneroSeed](#ots.seed.MoneroSeed)

Decodes a Monero seed phrase into a MoneroSeed object.

* **Parameters:**
  * **phrase** – The seed phrase to decode.
  * **height** – The block height associated with the seed.
  * **time** – The timestamp associated with the seed.
  * **network** – The network type for the seed.
  * **passphrase** – Optional passphrase for the seed.
* **Returns:**
  A MoneroSeed object containing the decoded seed data.

#### *classmethod* decodeIndices(indices: [SeedIndices](seed_indices.md#ots.seed_indices.SeedIndices), height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) = Network.MAIN, passphrase: str = '') → [MoneroSeed](#ots.seed.MoneroSeed)

Decodes seed indices into a MoneroSeed object.

* **Parameters:**
  * **indices** – The SeedIndices object to decode.
  * **height** – The block height associated with the seed.
  * **time** – The timestamp associated with the seed.
  * **network** – The network type for the seed.
  * **passphrase** – Optional passphrase for the seed.
* **Returns:**
  A MoneroSeed object containing the decoded seed data.

#### *classmethod* generate(height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) = Network.MAIN) → [MoneroSeed](#ots.seed.MoneroSeed)

Generates a new MoneroSeed instance with random data.

* **Parameters:**
  * **height** – The block height associated with the seed.
  * **time** – The timestamp associated with the seed.
  * **network** – The network type for the seed.
* **Returns:**
  A MoneroSeed object containing the generated seed data.

## Polyseed

### *class* ots.seed.Polyseed(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

Bases: [`Seed`](#ots.seed.Seed)

Polyseed class to handle Polyseed (16 word) seeds,
with timestamp and encryption support included.

#### *classmethod* create(random: bytes, network: [Network](enums.md#ots.enums.Network) = Network.MAIN, time: int = 0, passphrase: str = '') → [Polyseed](#ots.seed.Polyseed)

Creates a new Polyseed instance.

* **Parameters:**
  * **random** – 19 bytes of random data to create the seed.
  * **network** – The network type for the seed.
  * **time** – The timestamp associated with the seed.
  * **passphrase** – Optional passphrase for the seed.
* **Returns:**
  A Polyseed object containing the created seed data.

#### *classmethod* decode(phrase: str, network: [Network](enums.md#ots.enums.Network) = Network.MAIN, password: str = '', passphrase: str = '') → [Polyseed](#ots.seed.Polyseed)

Decodes a Polyseed phrase into a Polyseed object.

* **Parameters:**
  * **phrase** – The seed phrase to decode.
  * **network** – The network type for the seed.
  * **password** – Optional password to decrypt the seed. Not supported for legacy seeds.
  * **passphrase** – Optional passphrase for the seed.
* **Returns:**
  A Polyseed object containing the decoded seed data.

#### *classmethod* decodeIndices(indices: [SeedIndices](seed_indices.md#ots.seed_indices.SeedIndices), network: [Network](enums.md#ots.enums.Network) = Network.MAIN, password: str = '', passphrase: str = '') → [Polyseed](#ots.seed.Polyseed)

Decodes seed indices into a Polyseed object.

* **Parameters:**
  * **indices** – The SeedIndices object to decode.
  * **network** – The network type for the seed.
  * **password** – Optional password to decrypt the seed. Not supported for legacy seeds.
  * **passphrase** – Optional passphrase for the seed.
* **Returns:**
  A Polyseed object containing the decoded seed data.

#### *classmethod* decodeWithLanguage(phrase: str, language: [SeedLanguage](seed_language.md#ots.seed_language.SeedLanguage), network: [Network](enums.md#ots.enums.Network) = Network.MAIN, password: str = '', passphrase: str = '') → [Polyseed](#ots.seed.Polyseed)

Decodes a Polyseed phrase with a specific language into a Polyseed object.

* **Parameters:**
  * **phrase** – The seed phrase to decode.
  * **language** – The language of the seed phrase.
  * **network** – The network type for the seed.
  * **password** – Optional password to decrypt the seed. Not supported for legacy seeds.
  * **passphrase** – Optional passphrase for the seed.
* **Returns:**
  A Polyseed object containing the decoded seed data.

#### *classmethod* decodeWithLanguageCode(phrase: str, languageCode: str, network: [Network](enums.md#ots.enums.Network) = Network.MAIN, password: str = '', passphrase: str = '') → [Polyseed](#ots.seed.Polyseed)

Decodes a Polyseed phrase with a specific language code into a Polyseed object.

* **Parameters:**
  * **phrase** – The seed phrase to decode.
  * **languageCode** – The language code of the seed phrase.
  * **network** – The network type for the seed.
  * **password** – Optional password to decrypt the seed. Not supported for legacy seeds.
  * **passphrase** – Optional passphrase for the seed.
* **Returns:**
  A Polyseed object containing the decoded seed data.

#### *classmethod* generate(network: [Network](enums.md#ots.enums.Network) = Network.MAIN, time: int = 0, passphrase: str = '') → [Polyseed](#ots.seed.Polyseed)

Generates a new Polyseed instance with random data.

* **Parameters:**
  * **network** – The network type for the seed.
  * **time** – The timestamp associated with the seed.
  * **passphrase** – Optional passphrase for the seed.
* **Returns:**
  A Polyseed object containing the generated seed data.

#### moneroSeed() → [MoneroSeed](#ots.seed.MoneroSeed)

Converts the Polyseed to a MoneroSeed. (Creates a new MoneroSeed instance from the Polyseed)

* **Returns:**
  A MoneroSeed object representing the Polyseed.
