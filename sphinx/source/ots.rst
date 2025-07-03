Ots
===

All methods on :py:class:`ots.ots.Ots` are static. Apart from getting
the current installed :py:meth:`ots.ots.Ots.version` of the library, there are methods
provided to change and get the current configuration like:

- enforcement of entropy, which by default is set to on and set to a reasonable value.

- maximum account and index depth, which defaults by the time of writing
  to 10 accounts and 100 indexes, which in most cases of an online signing
  device or application should be sufficient, however, it can be changed.

And there are two methods to get secure random bytes.

.. warning:: 

   The methods :py:meth:`ots.ots.Ots.random` and :py:meth:`ots.ots.Ots.random32`,
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


.. caution::

   Always remember that the user of your product trust you with the funds
   in his wallet, so you should always ensure that the random bytes are
   not predictable and secure, otherwise the user could lose his funds!


.. autoclass:: ots.ots.Ots
   :members:
   :member-order: bysource
