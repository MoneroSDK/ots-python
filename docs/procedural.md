# Procedural

This modules is intented to provide a procedural interface to the OTS library,
which is easy to use in comparison to the raw C ABI Wrapper.

#### WARNING
This module is not yet implemented, and could be removed in the future.

### ots.procedural.free_result(result: [ots_result_t](raw.md#ots.raw.ots_result_t) | \_CDataBase) → None

Frees the result object returned by OTS functions.
:param result: The result object to free.

### ots.procedural.random(size: int) → bytes

Returns a random byte string of the specified size.

* **Parameters:**
  **size** – The number of random bytes to generate.
* **Returns:**
  A byte string containing the random bytes.

### ots.procedural.random32() → bytes

Returns a random 32-byte string.
:return: A byte string containing 32 random bytes.

### ots.procedural.version() → str

Returns the version of the OTS library.
:return: A string containing the OTS version.
