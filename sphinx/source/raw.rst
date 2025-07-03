Raw
===

The raw module provides the exact C ABI functions from :py:mod:`ots._ots` in a more Pythonic way. But mak no mistake it is almast like running C code directly. It is not recommended to use this module unless you are familiar with the C ABI and the underlying data structures to archive something that is not possible otherwise.


.. note::

   This module is intented as a fundation for the `procedural` (skipped for now) and `object-oriented` modules.

Struct wrappers
---------------

.. autoclass:: ots.raw.ots_result_t
   :members:
   :member-order: bysource
   :show-inheritance:
   :inherited-members:

.. autoclass:: ots.raw.ots_handle_t
   :members:
   :member-order: bysource
   :show-inheritance:
   :inherited-members:

.. autoclass:: ots.raw.ots_tx_description_t
   :members:
   :member-order: bysource
   :show-inheritance:
   :inherited-members:

Helper functions
----------------

.. autofunction:: ots.raw._unwrap

.. autofunction:: ots.raw._is_result

.. autofunction:: ots.raw._is_handle

.. autofunction:: ots.raw._raise_on_error


Functions
---------

.. automodule:: ots.raw
   :members:
   :exclude-members: ots_result_t, ots_handle_t, ots_tx_description_t
   :member-order: bysource
