from dataclasses import dataclass
from random import randint
from datetime import datetime
from time import time
from ots import *
import pytest


def test_seed():
    ts: int = int(time())
    seed: Polyseed = Polyseed.generate(time=ts)
    assert isinstance(seed, Seed)
    assert (ts - seed.timestamp) >= 0  # no future timestamps
    assert (ts - seed.timestamp) < (30 * 24 * 3600)  # 30 days
    assert seed.time.timestamp() == seed.timestamp
    assert (Ots.heightFromTimestamp(int(time())) - seed.height) < (30 * 24 * 3600)  # 30 days
    address: Address = seed.address
    assert address.fingerprint == seed.fingerprint
    for network in Network:
        seed = Polyseed.generate(network=network)
        assert seed.network == network

# TODO: continue with more tests
