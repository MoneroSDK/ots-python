# SeedIndices

The `SeedIndices` module provides functionality for managing seed indices,
to convert seed phrases into indices and vice versa. Also provides methods to easily
generate string representations of seed indices, and read from string representations
back to a SeedIndices object and from there to a supported Seed.

## SeedIndices

<a id="module-ots.seed_indices"></a>

### *class* ots.seed_indices.SeedIndices(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

SeedIndices class represents a collection of seed indices of the seed phrase.
Each seed index is an integer that corresponds to a word in the seed phrase.

#### \_\_len_\_() → int

* **Returns:**
  The number of seed indices.

#### \_\_add_\_(other: [SeedIndices](#ots.seed_indices.SeedIndices) | str) → [SeedIndices](#ots.seed_indices.SeedIndices)

Combine two SeedIndices objects or the SeedIndice with a password string.

* **Parameters:**
  **other** ([*SeedIndices*](#ots.seed_indices.SeedIndices) *|* *str*) – Another SeedIndices object or a string (password).
* **Returns:**
  A new SeedIndices object containing the combined values.

#### \_\_sub_\_(other: [SeedIndices](#ots.seed_indices.SeedIndices) | str) → [SeedIndices](#ots.seed_indices.SeedIndices)

How the operation is essentially XOR it’s the same as addition.

* **Parameters:**
  **other** ([*SeedIndices*](#ots.seed_indices.SeedIndices) *|* *str*) – Another SeedIndices object.
* **Returns:**
  A new SeedIndices object containing the combined values.

#### *property* values *: list[int]*

* **Returns:**
  A list of integers representing the seed indices.

#### *property* count *: int*

* **Returns:**
  The number of seed indices.

#### clear() → None

Clear the seed indices.

#### append(value: int) → None

Append a seed index to the list.

* **Parameters:**
  **value** (*int*) – The seed index to append.

#### numeric(separator: str = '') → str

Get the seed indices as a numeric string with a given separator.

* **Parameters:**
  **separator** (*str*) – The separator to use between indices. (default: ‘’)
* **Returns:**
  A numeric string representation of the seed indices.

#### hex(separator: str = '') → str

Get the seed indices as a hex string with a given separator.

* **Parameters:**
  **separator** (*str*) – The separator to use between indices. (default: ‘’)
* **Returns:**
  A hex string representation of the seed indices.

#### *classmethod* fromValues(values: list[int]) → [SeedIndices](#ots.seed_indices.SeedIndices)

Create a SeedIndices object from a list of integers.

* **Parameters:**
  **values** (*list* *[**int* *]*) – A list of integers representing the seed indices.
* **Returns:**
  A SeedIndices object containing the provided values.

#### *classmethod* fromString(string: str, separator: str = '') → [SeedIndices](#ots.seed_indices.SeedIndices)

Create a SeedIndices object from a string of integers separated by a given separator.

* **Parameters:**
  * **string** (*str*) – A string of integers representing the seed indices.
  * **separator** (*str*) – The separator used in the string (default: ‘’).
* **Returns:**
  A SeedIndices object containing the provided values.

#### *classmethod* fromHexString(string: str, separator: str = '') → [SeedIndices](#ots.seed_indices.SeedIndices)

Create a SeedIndices object from a hex string of integers separated by a given separator.

* **Parameters:**
  * **string** (*str*) – A hex string of integers representing the seed indices.
  * **separator** (*str*) – The separator used in the string (default: ‘’).
* **Returns:**
  A SeedIndices object containing the provided values.
