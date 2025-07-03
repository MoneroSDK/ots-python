Seeds
=====

Seed are essentially random bytes that are used to derive keys for the Wallet. In this library, the assumption is that this seeds are generally represented by seed phrases.

Monero Seeds (:py:class:`ots.seed.MoneroSeed`) are represented by a Monero seed phrase, and an optional passphrase for a seed offset. With this information you can restore the offline Wallet. This seed phrase consists of 24 words of the Monero word list include in the Monero source code. A 25th word is appened as a checksum.

Legacy Seeds (:py:class:`ots.seed.LegacySeed`) are essentially Monero Seeds, but they represented by only 12 words (and so only half the entropy). They are used by the legacy Monero Wallets, and can be restored (:py:meth:`ots.seed.LegacySeed.decode`) in this library, but can not be created or generated. A 13th word is appened as a checksum. Legacy Seeds are only supported for restoring existing Wallets, and not for creating new ones! This is done on purpose!

Polyseeds (:py:class:`ots.seed.Polyseed`) are a new type of seed that is used to derive keys for the Wallet. They are represented by a seed phrase consisting of 16 words. While Monero Seeds can be generated from the wallets secret bytes, Polyseeds are one way only, once the seed phrase is generated, the Polyseed will derive the key, the coin type (Not only Monero), the estimated creation time, from which the block height is derived. A Polyseed can be converted to a Monro Seed, but not the other way around.

On creating a new Seed, or decoding(restoring) an exiting seed the related classes (:py:class:`ots.seed.MoneroSeed`, :py:class:`ots.seed.LegacySeed`, :py:class:`ots.seed.Polyseed`) will be used. And return a related object. In the python wrapper seeds out of the seed jar are not objects of the related classes but rather simply Seed :py:class:`ots.seed.Seed` objects. :py:class:`ots.seed.Seed` provides all necessary methods and also the properties :py:attr:`ots.seed.Seed.type`, returning with :py:attr:`ots.enums.SeedType.MONERO` or :py:attr:`ots.enums.SeedType.POLYSEED` depending on the type of the seed. Further through the property :py:attr:`ots.seed.Seed.isLegacy` it can be checked if the seed is a legacy seed or not on a seed representing a monero seed.

The seed classes provide methods to encode and decode the seed phrase, encode and decode seed indices (numbers instead of words), and also provide the wallet to execute actions on the wallet like creating addresses, import outputs, export key images, check unsigned transactions, sign transactions and arbitrary data.

Seed
----

.. autoclass:: ots.seed.Seed
   :members:
   :special-members: __str__
   :show-inheritance:

LegacySeed
----------

.. autoclass:: ots.seed.LegacySeed
   :members:
   :special-members:
   :show-inheritance:
   :exclude-members: __weakref__

MoneroSeed
----------

.. autoclass:: ots.seed.MoneroSeed
   :members:
   :special-members:
   :show-inheritance:
   :exclude-members: __weakref__

Polyseed
--------

.. autoclass:: ots.seed.Polyseed
   :members:
   :special-members:
   :show-inheritance:
   :exclude-members: __weakref__
