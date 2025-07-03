SeedJar
=======

The Seed Jar keeps the seeds in a secure place and provides methods to access them.
If the seed jar is used there is no need to have a list or other construct to hold the
seed in memory. There is only one instance of :py:class:`ots.seed_jar.SeedJar` and
all methods are static.

So as long the library is in use the seeds are in memory, and can be accessed
in any module.

SeedJar
-------

.. autoclass:: ots.seed_jar.SeedJar
   :members:
   :member-order: bysource


SeedJarItem
-----------

.. autoclass:: ots.seed_jar.SeedJarItem
   :members:
   :member-order: bysource
