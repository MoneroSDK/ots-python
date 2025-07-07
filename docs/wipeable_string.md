# WipeableString

This class provides a string-like object that can be securely wiped from memory when no longer needed. It is useful for handling sensitive information such as passwords or cryptographic keys. Some methods return WipeableString objects, which can be used to ensure that sensitive data is not left in memory after use.

Intentionally, the WipeableString object can not be converted to a regular string with `str()`, to prevent accidental exposure of sensitive data. Instead, it provides a method to retrieve the string value in a concious manner with [`ots.wipeable_string.WipeableString.insecure()`](#ots.wipeable_string.WipeableString.insecure), which should only be used in the very last moment if needed. Converted to a regular string, the sensitive data would be left in memory, possible even after the garbage collector cleans it up, which is also not guaranteed to happen immediately.

To wipe the string secure, simply call del my_wipeable_string, assuming the object is called my_wipeable_string.

## WipeableString

### *class* ots.wipeable_string.WipeableString(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

A class for a wipeable string that can be securely erased from memory.

#### \_\_str_\_() → str

#### ATTENTION
This method is intentionally not implemented.

#### SEE ALSO
use [`insecure()`](#ots.wipeable_string.WipeableString.insecure) to get the string in an insecure way.

* **Raises:**
  **Exception** – Raises an exception if the string is attempted to be converted to a regular string.

#### \_\_eq_\_(other)

Compares two WipeableString instances for equality.

* **Parameters:**
  **other** ([*WipeableString*](#ots.wipeable_string.WipeableString) *|* *str*) – The other WipeableString instance or a string to compare with.
* **Returns:**
  True if the strings are equal, False otherwise.

#### insecure() → str

Returns the string in an insecure way, allowing it to be read as a normal string.
This method should be used with caution, as it does not guarantee that the string will be wiped from memory.

* **Returns:**
  The string contained in the WipeableString.

#### *classmethod* fromString(string: str) → [WipeableString](#ots.wipeable_string.WipeableString)

Creates a WipeableString from a regular string.

* **Parameters:**
  **string** (*str*) – The string to create the WipeableString from.
* **Returns:**
  A WipeableString instance containing the provided string.
