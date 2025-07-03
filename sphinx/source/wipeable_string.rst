WipeableString
==============

This class provides a string-like object that can be securely wiped from memory when no longer needed. It is useful for handling sensitive information such as passwords or cryptographic keys. Some methods return WipeableString objects, which can be used to ensure that sensitive data is not left in memory after use.

Intentionally, the WipeableString object can not be converted to a regular string with :py:func:`str()`, to prevent accidental exposure of sensitive data. Instead, it provides a method to retrieve the string value in a concious manner with :py:meth:`ots.wipeable_string.WipeableString.insecure`, which should only be used in the very last moment if needed. Converted to a regular string, the sensitive data would be left in memory, possible even after the garbage collector cleans it up, which is also not guaranteed to happen immediately.

To wipe the string secure, simply call `del my_wipeable_string`, assuming the object is called `my_wipeable_string`.


WipeableString
--------------

.. autoclass:: ots.wipeable_string.WipeableString
   :members:
   :special-members: __str__, __eq__
   :member-order: bysource

