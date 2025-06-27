from .raw import *
from .exceptions import OtsException


class SeedLanguage:
    """
    SeedLanguage class to handle the language of the seed.
    """
    all: set['SeedLanguage'] = set()
    byCode: dict[str, 'SeedLanguage'] = {}
    byName: dict[str, 'SeedLanguage'] = {}
    byEnglishName: dict[str, 'SeedLanguage'] = {}
    byType: dict[SeedType, set['SeedLanguage']] = {}

    def __init__(self, handle: ots_handle_t):
        assert isinstance(handle, ots_handle_t), "handle must be an instance of ots_handle_t"
        assert handle.type == HandleType.SEED_LANGUAGE, "handle must be of type SEED_LANGUAGE"
        self.handle: ots_handle_t = handle
        self._name: str | None = None
        self._english_name: str | None = None
        self._code: str | None = None
        self._supported: dict[SeedType, bool] = {}
        self._index: dict[SeedType, int] = {}

    def __str__(self):
        return self.englishName

    def __repr__(self):
        return f"SeedLanguage({str(self)})"

    def __hash__(self):
        """
        Returns the hash of the SeedLanguage instance.
        """
        return hash(self.code)

    @property
    def englishName(self) -> str:
        """
        Returns the English name of the seed language.
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
        Returns the name of the seed language.
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
        Returns the code of the seed language.
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
        """
        # we check every time from the C library to ensure we have the latest state
        result: ots_result_t = ots_seed_language_is_default(self.handle, seedType)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return ots_result_boolean(result)

    def index(self, seedType: SeedType) -> int:
        """
        Returns the index of the seed language for the given seed type.
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
        """
        result: ots_result_t = ots_seed_language_from_name(name)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def fromEnglishName(cls, englishName: str) -> 'SeedLanguage':
        """
        Creates a SeedLanguage instance from the given English name.
        """
        result: ots_result_t = ots_seed_language_from_english_name(englishName)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def fromCode(cls, code: str) -> 'SeedLanguage':
        """
        Creates a SeedLanguage instance from the given code.
        """
        result: ots_result_t = ots_seed_language_from_code(code)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        return cls(ots_result_handle(result))

    @classmethod
    def _load_all(cls) -> None:
        """
        Loads all SeedLanguage instances and populates the class attributes.
        """
        if len(cls.all) > 0:
            return
        result: ots_result_t = ots_seed_languages()
        if ots_is_error(result):
            raise OtsException.from_result(result)
        languages = ots_result_handle_array_reference(result)
        for seedType in SeedType:
            cls.byType[seedType] = set()
        for language in languages:
            seed_language = cls(language)
            cls.all.add(seed_language)
            cls.byCode[seed_language.code] = seed_language
            cls.byName[seed_language.name] = seed_language
            cls.byEnglishName[seed_language.englishName] = seed_language
            for seedType in SeedType:
                if seed_language.supported(seedType):
                    cls.byType[seedType].add(seed_language)

    @classmethod
    def list(cls) -> set['SeedLanguage']:
        """
        Returns a set of all SeedLanguage instances.
        """
        cls._load_all()
        return cls.all

    @classmethod
    def listForType(cls, seedType: SeedType) -> set['SeedLanguage']:
        """
        Returns a set of SeedLanguage instances for the given seed type.
        """
        cls._load_all()
        return cls.byType.get(seedType, set())

    @classmethod
    def defaultLanguage(cls, seedType: SeedType) -> 'SeedLanguage':
        """
        Returns the default SeedLanguage instance for the given seed type.
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
        Sets the default SeedLanguage instance for the given seed type.
        """
        if not isinstance(language, SeedLanguage):
            raise TypeError("language must be an instance of SeedLanguage")
        result: ots_result_t = ots_seed_language_set_default(seedType, language.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
