# SeedLanguage

Different seed phrases support different languages, yet. To handle this differences,
the [`ots.seed_language.SeedLanguage`](#ots.seed_language.SeedLanguage) class provides a way to manage the language of seed phrases. [`ots.seed_language.SeedLanguage`](#ots.seed_language.SeedLanguage) “knows” which languages are supported by each [`ots.enums.SeedType`](enums.md#ots.enums.SeedType).

<a id="module-ots.seed_language"></a>

### *class* ots.seed_language.SeedLanguage(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

SeedLanguage class to handle the languages for seed phrase handling.

#### \_\_str_\_()

* **Returns:**
  The English name of the seed language.

#### *property* englishName *: str*

* **Returns:**
  English name of the seed language.

#### *property* name *: str*

* **Returns:**
  Name of the seed language in the language itself.

#### *property* code *: str*

* **Returns:**
  The internal code (ISO 639-1) of the seed language, except for Chinese languages (which start with ‘zh-‘), Lojban and Esperanto.

#### supported(seedType: [SeedType](enums.md#ots.enums.SeedType)) → bool

Checks if the seed language is supported for the given seed type.

* **Parameters:**
  **seedType** ([*SeedType*](enums.md#ots.enums.SeedType)) – The type of seed to check support for.
* **Returns:**
  True if the seed language is supported for the given seed type, False otherwise.

#### isDefault(seedType: [SeedType](enums.md#ots.enums.SeedType)) → bool

Checks if the seed language is the default for the given seed type.

* **Parameters:**
  **seedType** ([*SeedType*](enums.md#ots.enums.SeedType)) – The type of seed to check if the language is default for.
* **Returns:**
  True if the seed language is the default for the given seed type, False otherwise.

#### *classmethod* fromName(name: str) → [SeedLanguage](#ots.seed_language.SeedLanguage)

Creates a SeedLanguage instance from the given name.

* **Parameters:**
  **name** (*str*) – The name of the seed language.
* **Returns:**
  A SeedLanguage instance corresponding to the given name.

#### *classmethod* fromEnglishName(englishName: str) → [SeedLanguage](#ots.seed_language.SeedLanguage)

Creates a SeedLanguage instance from the given English name.

* **Parameters:**
  **englishName** (*str*) – The English name of the seed language.
* **Returns:**
  A SeedLanguage instance corresponding to the given English name.

#### *classmethod* fromCode(code: str) → [SeedLanguage](#ots.seed_language.SeedLanguage)

Creates a SeedLanguage instance from the given code.

* **Parameters:**
  **code** (*str*) – The code of the seed language (mostly ISO 639-1).
* **Returns:**
  A SeedLanguage instance corresponding to the given code.

#### *classmethod* list() → set[[SeedLanguage](#ots.seed_language.SeedLanguage)]

* **Returns:**
  A set of all SeedLanguage instances.

#### *classmethod* listForType(seedType: [SeedType](enums.md#ots.enums.SeedType)) → set[[SeedLanguage](#ots.seed_language.SeedLanguage)]

Returns a set of SeedLanguage instances only for the given seed type.

* **Parameters:**
  **seedType** ([*SeedType*](enums.md#ots.enums.SeedType)) – The type of seed to get the languages for.
* **Returns:**
  A set of SeedLanguage instances for the given seed type.

#### *classmethod* defaultLanguage(seedType: [SeedType](enums.md#ots.enums.SeedType)) → [SeedLanguage](#ots.seed_language.SeedLanguage)

Returns the default SeedLanguage instance for the given seed type.

#### WARNING
Itentionally by default are no defaults set, before querying the default language, you must set it with [`setDefaultLanguage()`](#ots.seed_language.SeedLanguage.setDefaultLanguage).

* **Parameters:**
  **seedType** ([*SeedType*](enums.md#ots.enums.SeedType)) – The type of seed to get the default language for.
* **Returns:**
  The default SeedLanguage instance for the given seed type.

#### *classmethod* setDefaultLanguage(seedType: [SeedType](enums.md#ots.enums.SeedType), language: [SeedLanguage](#ots.seed_language.SeedLanguage)) → None

Sets the default SeedLanguage instance for the given seed type, so
you can manage the default language for seed phrases. By default there
are no defaults set, so you must call this method to set a default language
for each SeedType you want to use.

* **Parameters:**
  * **seedType** ([*SeedType*](enums.md#ots.enums.SeedType)) – The type of seed to set the default language for.
  * **language** ([*SeedLanguage*](#ots.seed_language.SeedLanguage)) – The SeedLanguage instance to set as default.
