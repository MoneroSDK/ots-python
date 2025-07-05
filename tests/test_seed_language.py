from ots import *
import pytest


LANGUAGES: dict[str, dict[str, any]] = {
    'nl': {
        'code': 'nl',
        'name': 'Nederlands',
        'englishName': 'Dutch',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: False
        }
    },
    'en': {
        'code': 'en',
        'name': 'English',
        'englishName': 'English',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: True
        }
    },
    'es': {
        'code': 'es',
        'name': 'Español',
        'englishName': 'Spanish',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: True
        }
    },
    'ru': {
        'code': 'ru',
        'name': 'русский язык',
        'englishName': 'Russian',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: False
        }
    },
    'de': {
        'code': 'de',
        'name': 'Deutsch',
        'englishName': 'German',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: False
        }
    },
    'lojban': {
        'code': 'lojban',
        'name': 'Lojban',
        'englishName': 'Lojban',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: False
        }
    },
    'ko': {
        'code': 'ko',
        'name': '한국어',
        'englishName': 'Korean',
        'supported': {
            SeedType.MONERO: False,
            SeedType.POLYSEED: True
        }
    },
    'cs': {
        'code': 'cs',
        'name': 'čeština',
        'englishName': 'Czech',
        'supported': {
            SeedType.MONERO: False,
            SeedType.POLYSEED: True
        }
    },
    'fr': {
        'code': 'fr',
        'name': 'Français',
        'englishName': 'French',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: True
        }
    },
    'pt': {
        'code': 'pt',
        'name': 'Português',
        'englishName': 'Portuguese',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: True
        }
    },
    'zh-Hans': {
        'code': 'zh-Hans',
        'name': '简体中文 (中国)',
        'englishName': 'Chinese (simplified)',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: True
        }
    },
    'it': {
        'code': 'it',
        'name': 'Italiano',
        'englishName': 'Italian',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: True
        }
    },
    'eo': {
        'code': 'eo',
        'name': 'Esperanto',
        'englishName': 'Esperanto',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: False
        }
    },
    'jp': {
        'code': 'jp',
        'name': '日本語',
        'englishName': 'Japanese',
        'supported': {
            SeedType.MONERO: True,
            SeedType.POLYSEED: True
        }
    },
    'zh-Hant': {
        'code': 'zh-Hant',
        'name': '中文(繁體)',
        'englishName': 'Chinese (Traditional)',
        'supported': {
            SeedType.MONERO: False,
            SeedType.POLYSEED: True
        }
    }
}

def test_seed_language_list():
    i: int = 0
    for lang in SeedLanguage.list():
        assert isinstance(lang, SeedLanguage), f"Expected SeedLanguage, got {type(lang)}"
        ref = LANGUAGES.get(lang.code)
        assert lang.name == ref['name'], f"Expected name {ref['name']}, got {lang.name}"
        assert lang.englishName == ref['englishName'], f"Expected englishName {ref['englishName']}, got {lang.englishName}"
        for st in (SeedType.MONERO, SeedType.POLYSEED):
            assert lang.supported(st) == ref['supported'][st], f"Expected supported({st}) {ref['supported'][st]}, got {lang.supported(st)}"
        i += 1

def test_seed_language_from_code():
    for key in LANGUAGES:
        ref = LANGUAGES[key]
        lang = SeedLanguage.fromCode(ref['code'])
        assert isinstance(lang, SeedLanguage), f"Expected SeedLanguage, got {type(lang)}"
        assert lang.englishName == ref['englishName'], f"Expected englishName {ref['englishName']}, got {lang.englishName}"

def test_seed_language_from_name():
    for key in LANGUAGES:
        ref = LANGUAGES[key]
        lang = SeedLanguage.fromName(ref['name'])
        assert isinstance(lang, SeedLanguage), f"Expected SeedLanguage, got {type(lang)}"
        assert lang.code == key, f"Expected code {key}, got {lang.code}"

def test_seed_language_from_english_name():
    for key in LANGUAGES:
        ref = LANGUAGES[key]
        lang = SeedLanguage.fromEnglishName(ref['englishName'])
        assert isinstance(lang, SeedLanguage), f"Expected SeedLanguage, got {type(lang)}"
        assert lang.code == key, f"Expected code {key}, got {lang.code}"

def test_seed_language_list_for_type():
    for st in (SeedType.MONERO, SeedType.POLYSEED):
        not_supported = [key for key in LANGUAGES if not LANGUAGES[key]['supported'][st]]
        langs = SeedLanguage.listForType(st)
        for lang in langs:
            assert isinstance(lang, SeedLanguage), f"Expected SeedLanguage, got {type(lang)}"
            assert lang.supported(st) is True, f"Expected supported({st}) to be True, got {lang.supported(st)}"
            assert lang.code not in not_supported, f"Expected code {lang.code} to be in supported languages for {st.name}"

def test_seed_language_default_language():
    with pytest.raises(OtsException):
        md: bool = SeedLanguage.defaultLanguage(SeedType.MONERO)
    with pytest.raises(OtsException):
        pd: bool = SeedLanguage.defaultLanguage(SeedType.POLYSEED)
    en: SeedLanguage = SeedLanguage.fromCode('en')
    assert not en.isDefault(SeedType.MONERO), "English should not be default for MONERO before setting it"
    assert not en.isDefault(SeedType.POLYSEED), "English should not be default for POLYSEED before setting it"
    SeedLanguage.setDefaultLanguage(SeedType.MONERO, SeedLanguage.fromCode('en'))
    SeedLanguage.setDefaultLanguage(SeedType.POLYSEED, SeedLanguage.fromCode('en'))
    assert SeedLanguage.defaultLanguage(SeedType.MONERO) == 'en', "Default language for MONERO should be set to English"
    assert 'en' == SeedLanguage.defaultLanguage(SeedType.POLYSEED), "Default language for POLYSEED should be set to English"
    assert en.isDefault(SeedType.MONERO), "English should be default for MONERO after setting it"
    assert en.isDefault(SeedType.POLYSEED), "English should be default for POLYSEED after setting it"

