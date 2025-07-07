# Ots

All methods on [`ots.ots.Ots`](#ots.ots.Ots) are static. Apart from getting
the current installed [`ots.ots.Ots.version()`](#ots.ots.Ots.version) of the library, there are methods
provided to change and get the current configuration like:

- enforcement of entropy, which by default is set to on and set to a reasonable value.
- maximum account and index depth, which defaults by the time of writing
  to 10 accounts and 100 indexes, which in most cases of an online signing
  device or application should be sufficient, however, it can be changed.

And there are two methods to get secure random bytes.

#### WARNING
The methods [`ots.ots.Ots.random()`](#ots.ots.Ots.random) and [`ots.ots.Ots.random32()`](#ots.ots.Ots.random32),
return only cryptographically secure random bytes, if the hardware can deliver
them.

That means, that even with enforced entropy, the random bytes are not
secure, how it only ensures a certain entropy and an absense of certain patterns
in the random bytes. The hardware could deliver random bytes that fullfill
the requirements, but they could be still predictable, e.g. if the device returns
after every reset the same random bytes.

In that case, the random bytes are not secure, even if the entropy is enforced.
This is an extrem example to illustrate the point, that the methods do not
guarantee secure random bytes, if the system does not provide them.

If suspected the system PRNG is not secure, it is recommended to use a different
source of secure random bytes, e.g. from a hardware security module (HSM) or a
secure random number generator (RNG) or hashed camera stream or similar.

### *class* ots.ots.Ots

A class with only static helper methods for the OTS library.

#### *static* version() → str

Returns the version of the OTS library.

#### *static* versionComponets() → tuple[int, int, int]

Returns the version components of the OTS library as a tuple.

#### *static* heightFromTimestamp(timestamp: int, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN) → int

Returns the estimated blockchain height for a given timestamp and network.

* **Parameters:**
  * **timestamp** (*int*) – The timestamp to use for height calculation.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network to use (default is `Network.MAIN`).
* **Returns:**
  The blockchain height for the given timestamp.

#### *static* timestampFromHeight(height: int, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN) → int

Returns the estimated timestamp for a given blockchain height and network.

* **Parameters:**
  * **height** (*int*) – The height of the OTS tree.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network to use (default is Network.MAIN).
* **Returns:**
  The timestamp corresponding to the given blockchain height.

#### *static* random(size: int) → bytes

Returns a random bytes of the specified size.

#### NOTE
By default on low entropy the library will raise
an exception, this happens also if the size of bytes
is low. There is probably no much sense in using less
then 19 bytes ever, but if really needed,
calling [`setEnforceEntropy()`](#ots.ots.Ots.setEnforceEntropy)
with `False` will disable
the behavior of raising an exception on low entropy,
which practically allows any crap random bytes to use
in the library.

* **Parameters:**
  **size** (*int*) – The number of random bytes to generate.
* **Returns:**
  A byte string containing the random bytes.

#### *static* random32() → bytes

Returns a random 32 bytes.

#### *static* lowEntropy(data: bytes, minEntropy: float) → bool

Checks if the provided data has low entropy.

* **Parameters:**
  * **data** (*bytes*) – The byte string to check for entropy.
  * **minEntropy** (*float*) – The minimum entropy threshold.
* **Returns:**
  True if the data has low entropy, False otherwise.

#### *static* setEnforceEntropy(enforce: bool = True) → None

Sets whether to enforce minimum entropy for OTS operations.
This is a security measure to ensure that random
data is not of bad quality. And will ensure that
there is sufficient entropy in the random data or
the library will raise an exception.

* **Parameters:**
  **enforce** (*bool*) – Whether to enforce minimum entropy.

#### *static* setEnforceEntropyLevel(minEntropy: float) → None

Sets the minimum entropy level for OTS operations.
This is a security measure to ensure that random
data is not of bad quality. And will ensure that
there is sufficient entropy in the random data or
the library will raise an exception.

* **Parameters:**
  **minEntropy** (*float*) – The minimum entropy threshold.

#### *static* setMaxAccountDepth(depth: int) → None

Sets the maximum account depth for OTS operations.
Searching addresses or outputs in a account is restricted
to the maximum depth, if not specified otherwise.

* **Parameters:**
  **depth** (*int*) – The maximum account depth to set.

#### *static* setMaxIndexDepth(depth: int) → None

Sets the maximum index depth for OTS operations.
Searching addresses or outputs in a index is restricted
to the maximum depth, if not specified otherwise.

* **Parameters:**
  **depth** (*int*) – The maximum index depth to set.

#### *static* setMaxDepth(accountDepth: int, indexDepth: int) → None

Sets the maximum account and index depth for OTS operations.
This is the combined method to set both account and index depths.
Searching addresses or outputs in a account or index is restricted
to the maximum depth, if not specified otherwise.

* **Parameters:**
  * **accountDepth** (*int*) – The maximum account depth to set.
  * **indexDepth** (*int*) – The maximum index depth to set.

#### *static* resetMaxDepth() → None

Resets the maximum account and index depth to their default values.

#### NOTE
This default values are declared in the OTS C++ library
in the file ots.hpp as DEFAULT_MAX_ACCOUNT_DEPTH
and DEFAULT_MAX_INDEX_DEPTH, which by time of writing
are 10 and 100 respectively.

#### *static* maxAccountDepth(default: int = 0) → int

Returns the maximum account depth for OTS operations.

* **Parameters:**
  **default** (*int*) – The default value to return if not set.
  set to 0 to get the DEFAULT_MAX_ACCOUNT_DEPTH
  if not set.
* **Returns:**
  The maximum account depth or the default value.

#### *static* maxIndexDepth(default: int = 0) → int

Returns the maximum index depth for OTS operations.

* **Parameters:**
  **default** (*int*) – The default value to return if not set.
  set to 0 to get the DEFAULT_MAX_INDEX_DEPTH
  if not set.
* **Returns:**
  The maximum index depth or the default value.

#### *static* verifyData(data: bytes | str, address: [Address](address.md#ots.address.Address) | str, signature: str | bytes) → bool

Verifies the data signature against the public key.

* **Parameters:**
  * **data** (*bytes* *|* *str*) – The data to verify.
  * **address** ([*Address*](address.md#ots.address.Address) *|* *str*) – The public key address to verify against.
  * **signature** (*str* *|* *bytes*) – The signature to verify.
* **Returns:**
  True if the signature is valid, False otherwise.
