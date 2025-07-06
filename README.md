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

## Requirements

You will need build essentials to build the Monero OTS library and the Python wrapper. On Debian-based systems, you can install them with:
```bash
sudo apt-get install build-essential git
```

Then download the monero source:
```bash
git clone --recursive --branch master https://github.com/monero-project/monero.git
cd monero
```

Next, you need to build the Monero OTS library. Follow the instructions in the `ots/README.md` file in the Monero repository to compile the library. This will generate the required shared libraries and header files, but essentially you want to do the following:
```bash
cmake ../ots
make && sudo make install
```

With the shared ots libraries installed on the system, you can now install the Python wrapper.

## Installing the Python Wrapper
You can install the Monero OTS Python wrapper using pip:

```bash
# if you are not already in a virtual environment:
python3 -m venv .venv
source .venv/bin/activate
# Install the OTS Python wrapper itself
pip install git+https://github.com/MoneroSDK/ots-python.git
```

Or system-wide (not recommended):
```bash
# BE AWARE that you mess with your system Python packages, which can lead to conflicts with other packages.
# Most times you really want to use a virtual environment! So see above!
pip install --break-system-packages git+https://github.com/MoneroSDK/ots-python.git
```

# Usage
```python
from ots import Ots, SeedJar, SeedLanguage, MoneroSeed, Polyseed, Wallet

# or

from ots import *  # to use the object oriented approach

print(Ots.version())  # Print the version of the OTS library
```

# Further Documentation
- [Monero OTS Python Wrapper](https://docs.getmonero.org/sdk/ots/python)
- [Monero OTS Python API Reference](https://docs.getmonero.org/sdk/ots/python/reference)
- [Monero OTS Documentation](https://docs.getmonero.org/sdk/ots)
- [Monero OTS Reference](https://docs.getmonero.org/sdk/ots/reference)
