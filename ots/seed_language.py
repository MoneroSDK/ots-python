from .raw import *
from .exceptions import OtsException


class SeedLanguage:
    """
    SeedLanguage class to handle the languages for seed phrase handling.
    """
    _all: set['SeedLanguage'] = set()
    _byCode: dict[str, 'SeedLanguage'] = {}
    _byName: dict[str, 'SeedLanguage'] = {}
    _byEnglishName: dict[str, 'SeedLanguage'] = {}
    _byType: dict[SeedType, set['SeedLanguage']] = {}

    def __init__(self, handle: ots_handle_t):
        """
        Initializes the SeedLanguage instance with a handle.

        :param ots_handle_t handle: The handle to the seed language.
        :meta private:
        """
        assert isinstance(handle, ots_handle_t), "handle must be an instance of ots_handle_t"
        assert handle.type == HandleType.SEED_LANGUAGE, "handle must be of type SEED_LANGUAGE"
        self.handle: ots_handle_t = handle
        self._name: str | None = None
        self._english_name: str | None = None
        self._code: str | None = None
        self._supported: dict[SeedType, bool] = {}
        self._index: dict[SeedType, int] = {}

    def __str__(self):
        """
        :return: The English name of the seed language.
        """
        return self.englishName

    def __repr__(self):
        """
        :meta private:
        """
        return f"SeedLanguage({str(self)})"

    def __hash__(self):
        """
        Returns the hash of the SeedLanguage instance.
        :meta private:
        """
        return hash(self.code)

    @property
    def englishName(self) -> str:
        """
        :return: English name of the seed language.
        """
        if self._english_name is None:
            result: ots_result_t = ots_seed_language_english_name(self.handle)
            if ots_is_error(result):
                raise OtsException.from_result(result)
            self._english_name = ots_result_string(result)
        return self._english_name

    @property
    def name(self) -> str:
        """
        :return: Name of the seed language in the language itself.
        """
        if self._name is None:
            result: ots_result_t = ots_seed_language_name(self.handle)
            if ots_is_error(result):
                raise OtsException.from_result(result)
            self._name = ots_result_string(result)
        return self._name

    @property
    def code(self) -> str:
        """
        :return: The internal code (ISO 639-1) of the seed language, except for Chinese languages (which start with 'zh-'), Lojban and Esperanto.
        """
        if self._code is None:
            result: ots_result_t = ots_seed_language_code(self.handle)
            if ots_is_error(result):
                raise OtsException.from_result(result)
            self._code = ots_result_string(result)
        return self._code

    def supported(self, seedType: SeedType) -> bool:
        """
        Checks if the seed language is supported for the given seed type.

        :param SeedType seedType: The type of seed to check support for.
        :return: True if the seed language is supported for the given seed type, False otherwise.
        """
        if seedType in self._supported:
            return self._supported[seedType]
        result: ots_result_t = ots_seed_language_supported(self.handle, seedType)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._supported[seedType] = ots_result_boolean(result)
        return self._supported[seedType]

    def isDefault(self, seedType: SeedType) -> bool:
        """
        Checks if the seed language is the default for the given seed type.

        :param SeedType seedType: The type of seed to check if the language is default for.
        :return: True if the seed language is the default for the given seed type, False otherwise.
        """
        # we check every time from the C library to ensure we have the latest state
        result: ots_result_t = ots_seed_language_is_default(self.handle, seedType)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    def index(self, seedType: SeedType) -> int:
        """
        Returns the index of the seed language for the given seed type.

        :param SeedType seedType: The type of seed to get the index for.
        :return: The index of the seed language for the given seed type.
        """
        if seedType in self._index:
            return self._index[seedType]
        result: ots_result_t = ots_seed_language_index(self.handle, seedType)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._index[seedType] = ots_result_int(result)
        return self._index[seedType]

    def __eq__(self, other: object) -> bool:
        """
        Checks equality with another SeedLanguage instance or a string.

        :param other: The other SeedLanguage instance or string with the code to compare with.
        :type other: SeedLanguage | str
        :return: True if the two instances or the instance and the string have the same code, False otherwise.
        """
        if isinstance(other, str):
            return self.code.tolower() == other.code.lower()
        if not isinstance(other, SeedLanguage):
            raise NotImplementedError("other must be an instance of SeedLanguage or str")
        assert isinstance(other, SeedLanguage), "other must be an instance of SeedLanguage"
        print(HandleType(other.handle.ptr.type).name)
        assert HandleType(other.handle.ptr.type) == HandleType.SEED_LANGUAGE, "self must be a SeedLanguage instance"
        result: ots_result_t = ots_seed_language_equals(self.handle, other.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_is_equal(result)

    @classmethod
    def fromName(cls, name: str) -> 'SeedLanguage':
        """
        Creates a SeedLanguage instance from the given name.

        :param str name: The name of the seed language.
        :return: A SeedLanguage instance corresponding to the given name.
        """
        result: ots_result_t = ots_seed_language_from_name(name)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def fromEnglishName(cls, englishName: str) -> 'SeedLanguage':
        """
        Creates a SeedLanguage instance from the given English name.

        :param str englishName: The English name of the seed language.
        :return: A SeedLanguage instance corresponding to the given English name.
        """
        result: ots_result_t = ots_seed_language_from_english_name(englishName)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def fromCode(cls, code: str) -> 'SeedLanguage':
        """
        Creates a SeedLanguage instance from the given code.

        :param str code: The code of the seed language (mostly ISO 639-1).
        :return: A SeedLanguage instance corresponding to the given code.
        """
        result: ots_result_t = ots_seed_language_from_code(code)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def _load_all(cls) -> None:
        """
        Loads all SeedLanguage instances and populates the class attributes.
        :meta private:
        """
        if len(cls._all) > 0:
            return
        result: ots_result_t = ots_seed_languages()
        if ots_is_error(result):
            raise OtsException.from_result(result)
        languages = ots_result_handle_array_reference(result)
        for seedType in SeedType:
            cls._byType[seedType] = set()
        for language in languages:
            seed_language = cls(language)
            cls._all.add(seed_language)
            cls._byCode[seed_language.code] = seed_language
            cls._byName[seed_language.name] = seed_language
            cls._byEnglishName[seed_language.englishName] = seed_language
            for seedType in SeedType:
                if seed_language.supported(seedType):
                    cls._byType[seedType].add(seed_language)

    @classmethod
    def list(cls) -> set['SeedLanguage']:
        """
        :return: A set of all SeedLanguage instances.
        """
        cls._load_all()
        return cls._all

    @classmethod
    def listForType(cls, seedType: SeedType) -> set['SeedLanguage']:
        """
        Returns a set of SeedLanguage instances only for the given seed type.

        :param SeedType seedType: The type of seed to get the languages for.
        :return: A set of SeedLanguage instances for the given seed type.
        """
        cls._load_all()
        return cls._byType.get(seedType, set())

    @classmethod
    def defaultLanguage(cls, seedType: SeedType) -> 'SeedLanguage':
        """
        Returns the default SeedLanguage instance for the given seed type.

        .. warning::

            Itentionally by default are no defaults set, before querying the default language, you must set it with :py:meth:`setDefaultLanguage`.

        :param SeedType seedType: The type of seed to get the default language for.
        :return: The default SeedLanguage instance for the given seed type.
        """
        cls._load_all()
        result: ots_result_t = ots_seed_language_default(seedType)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        tmp: 'SeedLanguage' = cls(ots_result_handle(result))
        return cls.fromCode(tmp.code)

    @classmethod
    def setDefaultLanguage(cls, seedType: SeedType, language: 'SeedLanguage') -> None:
        """
        Sets the default SeedLanguage instance for the given seed type, so
        you can manage the default language for seed phrases. By default there
        are no defaults set, so you must call this method to set a default language
        for each SeedType you want to use.

        :param SeedType seedType: The type of seed to set the default language for.
        :param SeedLanguage language: The SeedLanguage instance to set as default.
        """
        if not isinstance(language, SeedLanguage):
            raise TypeError("language must be an instance of SeedLanguage")
        result: ots_result_t = ots_seed_language_set_default(seedType, language.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
