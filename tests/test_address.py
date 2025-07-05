from dataclasses import dataclass
from random import randint
from ots import *
import pytest


@dataclass
class AddressTestCase:
    name: str
    address: str
    fingerprint: str = ''
    network: Network = Network.MAIN
    type: AddressType = AddressType.STANDARD
    payment_id: str = ''
    base_address: str = ''
    valid: bool = True


test_cases = (
    AddressTestCase(
        'Empty',
        '',
        '',
        Network.MAIN,
        AddressType.STANDARD,
        '',
        '',
        False
    ),
    AddressTestCase(
        'Invalid',
        'invalid',
        '',
        Network.MAIN,
        AddressType.STANDARD,
        '',
        '',
        False
    ),
    AddressTestCase(
        'MainSTANDARD',
        '4957vKkr9wUAA4a2rRjLmbT4uJadSZxzrW1nJh3NJYDr87hEdiFhaCcGyK87kb8u1i1DWtwKTUnoZ6uobbotLGqX3zZKdtK',
        '35B3F5',
        Network.MAIN,
        AddressType.STANDARD
    ),
    AddressTestCase(
        'MainSubAddress',
        '83HfRN12ujdNR9AtzmMotUaKo3avrzjfbHefaZ4muku5cJuBc3qaf81Xovo88FxRgoGYqp1cJycSiZF4554cd5Lt6PfQBXm',
        'DCB56E',
        Network.MAIN,
        AddressType.SUBADDRESS
    ),
    AddressTestCase(
        'MainINTEGRATED',
        '4Jmnw8aLmCzAA4a2rRjLmbT4uJadSZxzrW1nJh3NJYDr87hEdiFhaCcGyK87kb8u1i1DWtwKTUnoZ6uobbotLGqX5QeCPeUbcLb1iqv4E7',
        'CF8863',
        Network.MAIN,
        AddressType.INTEGRATED,
        '59f3832901727c06',
        '4957vKkr9wUAA4a2rRjLmbT4uJadSZxzrW1nJh3NJYDr87hEdiFhaCcGyK87kb8u1i1DWtwKTUnoZ6uobbotLGqX3zZKdtK'
    ),
    AddressTestCase(
        'TestSTANDARD',
        '9xftLeckEQ5S5S2FHDGKZAUAHZKPdYRtVJAgyYERcEvaa8YjV7z5yXrVKmfse2mnePUCJUB6L8yCWfvUj1LBQHyRDhg7bzw',
        '00F069',
        Network.TEST,
        AddressType.STANDARD
    ),
    AddressTestCase(
        'TestSubAddress',
        'BaswxFneurncD8EanZiasqLYdB2wLBPKUEpGvfTyoymEH933uibnpuWTjQA2ThJiirVSMgbYVWuGVUePddR2v9WmNHDwdPJ',
        '59984B',
        Network.TEST,
        AddressType.SUBADDRESS
    ),
    AddressTestCase(
        'TestINTEGRATED',
        'A8NZMTSEqfbS5S2FHDGKZAUAHZKPdYRtVJAgyYERcEvaa8YjV7z5yXrVKmfse2mnePUCJUB6L8yCWfvUj1LBQHyRKrDheASom7LFc6SsTx',
        '8E8255',
        Network.TEST,
        AddressType.INTEGRATED,
        'b03d44b903993f81',
        '9xftLeckEQ5S5S2FHDGKZAUAHZKPdYRtVJAgyYERcEvaa8YjV7z5yXrVKmfse2mnePUCJUB6L8yCWfvUj1LBQHyRDhg7bzw'
    ),
    AddressTestCase(
        'StageSTANDARD',
        '5BCb2ZfN7Jybmqjgb3QbCyYpPgF2s9ygS2xJ3wKM1jVyKmaX1XHtAieiaHeWx7CwirKvTA1PEHZtA37FqKaDDowoTC4MjxA',
        'D01628',
        Network.STAGE,
        AddressType.STANDARD
    ),
    AddressTestCase(
        'StageSubAddress',
        '79yuUvURCcUDSis5CJxkqiSBKs6YC64nJXoo9dYWaLtcQr179fZwHxJQYnGyDViHb6EWLNDUCJ2kh25X5kkCyu6aLDfd1cX',
        '7D8356',
        Network.STAGE,
        AddressType.SUBADDRESS
    ),
    AddressTestCase(
        'StageINTEGRATED',
        '5LuG3NUriaVbmqjgb3QbCyYpPgF2s9ygS2xJ3wKM1jVyKmaX1XHtAieiaHeWx7CwirKvTA1PEHZtA37FqKaDDowofucwGND291HHTMRikw',
        '83B77F',
        Network.STAGE,
        AddressType.INTEGRATED,
        '9c749f464a3df891',
        '5BCb2ZfN7Jybmqjgb3QbCyYpPgF2s9ygS2xJ3wKM1jVyKmaX1XHtAieiaHeWx7CwirKvTA1PEHZtA37FqKaDDowoTC4MjxA'
    )
)

def test_address():
    for case in test_cases:
        if not case.valid:
            with pytest.raises(OtsException):
                Address.fromString(case.address)
            continue
        address = Address.fromString(case.address)
        assert address.base58 == case.address
        assert address == case.address
        assert address.fingerprint == case.fingerprint
        assert address.network == case.network
        assert address.type == case.type
        assert address.paymentId == case.payment_id
        assert len(address) == 95 if case.type != AddressType.INTEGRATED else 106
        if case.type == AddressType.INTEGRATED:
            assert address.isIntegrated
            assert Address.fromIntegrated(address).base58 == case.base_address

def test_address_string():
    for case in test_cases:
        assert AddressString.valid(case.address, case.network) == case.valid
        if case.valid:
            assert AddressString.fingerprint(case.address) == case.fingerprint
            assert AddressString.network(case.address) == case.network
            assert AddressString.type(case.address) == case.type
            assert AddressString.isIntegrated(case.address) == (case.type == AddressType.INTEGRATED)
        else:
            assert not AddressString.valid(case.address, case.network)
            with pytest.raises(OtsException):
                AddressString.fingerprint(case.address)
            with pytest.raises(OtsException):
                AddressString.network(case.address)
            with pytest.raises(OtsException):
                AddressString.type(case.address)
            with pytest.raises(OtsException):
                AddressString.isIntegrated(case.address)
