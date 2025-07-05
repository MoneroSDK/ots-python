from dataclasses import dataclass
from random import randint
from ots import *
import pytest


def test_ots_version():
    assert Ots.version() == '0.1.0'
    assert Ots.versionComponets() == tuple(int(i) for i in Ots.version().split('.'))

def test_height_timestamp():
    assert Ots.timestampFromHeight(0) == 1397818193
    assert Ots.heightFromTimestamp(1397818193) == 0

def test_random():
    data: bytes = Ots.random(1024)
    assert isinstance(data, bytes)
    assert len(data) == 1024
    assert not Ots.lowEntropy(data, 3.5)
    assert not Ots.lowEntropy(Ots.random32(), 3.5)
    with pytest.raises(OtsException):
        Ots.random(5)
    Ots.setEnforceEntropy(False)
    assert len(Ots.random(5)) == 5
    Ots.setEnforceEntropy(True)
    with pytest.raises(OtsException):
        Ots.random(5)
    Ots.setEnforceEntropyLevel(0.5)
    assert len(Ots.random(5)) == 5
    Ots.setEnforceEntropyLevel(3.5)

def test_max_depth():
    assert Ots.maxAccountDepth() == 10
    assert Ots.maxIndexDepth() == 100
    Ots.setMaxDepth(200, 200)
    assert Ots.maxAccountDepth() == 200
    assert Ots.maxIndexDepth() == 200
    Ots.setMaxAccountDepth(30)
    assert Ots.maxAccountDepth() == 30
    Ots.setMaxIndexDepth(30)
    assert Ots.maxIndexDepth() == 30
    Ots.resetMaxDepth()
    assert Ots.maxAccountDepth() == 10
    assert Ots.maxIndexDepth() == 100

def test_ots_verif_data():
    data: bytes = Ots.random(1024)
    seed: Seed = MoneroSeed.generate()
    wallet: Wallet = seed.wallet
    sig: str = wallet.signData(data)
    assert isinstance(sig, str)
    addr: str = str(seed.address)
    assert Ots.verifyData(data, addr, sig)
    data = data[512:] + data[:512]
    assert not Ots.verifyData(data, addr, sig)
