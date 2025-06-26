# Monero OTS (Offline Transaction Signing) Python Wrapper

This is a Python wrapper for the Monero OTS (Offline Transaction Signing) library, which allows you to create an offline transaction signing application or device. It is based on the C ABI of the Monero OTS library included in the ots directory of the Monero repository.

# Requirements
- Python 3.12 or higher
- cffi 0.17.1 or higher
- the Monero OTS library modules:
    - `libmonero-ots.so`
    - `libepee.so`
    - `libeasylogging.so`
    - `libmonero-crypto.so`
    - `libmonero-stubs.so`
    - `libutf8proc.so`
- the Monero OTS library header files:
    - `ots.h`
    - `ots-errors.h`

While the header files included in `include` the shared libraries are not because they are platform dependent,
you need them install separately in your system. You can find them in the Monero repository
https://github.com/monero-project/monero in the folder `ots/include`. Read the README.md to compile the library
or if available install the precompiled packages for your system.

# Installation
You can install the Monero OTS Python wrapper using pip:

```bash
pip install git+https://github.com/MoneroSDK/ots-python.git
```

# Usage
```python
from ots import Ots, SeedJar, SeedLanguage, MoneroSeed, Polyseed, Wallet

print(Ots.version())  # Print the version of the OTS library
```

# Further Documentation
- [Monero OTS Python Wrapper](https://docs.getmonero.org/sdk/ots/python)
- [Monero OTS Python API Reference](https://docs.getmonero.org/sdk/ots/python/reference)
- [Monero OTS Documentation](https://docs.getmonero.org/sdk/ots)
- [Monero OTS Reference](https://docs.getmonero.org/sdk/ots/reference)
