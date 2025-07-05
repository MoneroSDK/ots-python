from random import randint
from ots import *
import pytest

def test_seed_indices_values():
    indices: list[int] = [i for i in range(10)]
    seedIndices = SeedIndices.fromValues(indices)
    assert isinstance(seedIndices, SeedIndices), "Expected SeedIndices instance"
    assert seedIndices.values == indices, "SeedIndices values do not match input values"

def test_seed_indices_numeric():
    indices: list[int] = [i for i in range(10)]
    seedIndices = SeedIndices.fromValues(indices)
    assert isinstance(seedIndices, SeedIndices), "Expected SeedIndices instance"
    assert seedIndices.values == indices, "SeedIndices values do not match input values"
    for separator in ['', ',', ';', ' ']:
        numeric_string = seedIndices.numeric(separator)
        si: SeedIndices = SeedIndices.fromString(numeric_string, separator)
        assert isinstance(si, SeedIndices), "Expected SeedIndices instance from numeric string"
        assert si.values == indices, "SeedIndices values do not match input values from numeric string"

def test_seed_indices_hex():
    indices: list[int] = [i for i in range(10)]
    seedIndices = SeedIndices.fromValues(indices)
    assert isinstance(seedIndices, SeedIndices), "Expected SeedIndices instance"
    assert seedIndices.values == indices, "SeedIndices values do not match input values"
    for separator in ['', ',', ';', ' ']:
        hex_string = seedIndices.hex(separator)
        si: SeedIndices = SeedIndices.fromHexString(hex_string, separator)
        assert isinstance(si, SeedIndices), "Expected SeedIndices instance from hex string"
        assert si.values == indices, "SeedIndices values do not match input values from hex string"

def test_seed_indices_len_appened_clear():
    indices: list[int] = []
    seedIndices = SeedIndices.fromValues(indices)
    assert isinstance(seedIndices, SeedIndices), "Expected SeedIndices instance"
    assert len(seedIndices) == len(indices), "SeedIndices length does not match input values length"
    for i in range(10):
        assert len(seedIndices) == i, "SeedIndices length does not match input values length before append"
        word: int = randint(0, 2048)
        seedIndices.append(word)
        indices.append(word)
        assert seedIndices.values == indices, "SeedIndices values do not match input values after append"
        assert len(seedIndices) == seedIndices.count, "SeedIndices length does not match between `__len__` method and `count` property"
    seedIndices.clear()
    assert len(seedIndices) == 0, "SeedIndices length should be 0 after clear"

def test_seed_indices_add_sub():
    indices1: list[int] = [randint(0, 2048) for _ in range(10)]
    indices2: list[int] = [randint(0, 2048) for _ in range(10)]
    null: list[int] = [0 for _ in range(10)]
    si1: SeedIndices = SeedIndices.fromValues(indices1)
    si2: SeedIndices = SeedIndices.fromValues(indices2)
    assert isinstance(si1, SeedIndices), "Expected SeedIndices instance"
    assert isinstance(si2, SeedIndices), "Expected SeedIndices instance"
    si3: SeedIndices = si1 + si2
    assert (si1 + si3).values == si2.values, "SeedIndices values do not match after addition"
    assert (si2 - si3).values == si1.values, "SeedIndices values do not match after subtraction"
    assert (si1 + si1).values == null, "SeedIndices values do not match after adding itself"
    assert (si1 - si1).values == null, "SeedIndices values do not match after subtracting itself"
