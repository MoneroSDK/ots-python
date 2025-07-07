# Enumerations

Enums based on the OTS enums from ots.h header file.

### *class* ots.enums.Network(\*values)

Enum representing the network type for OTS operations.

#### MAIN *= 0*

Main network, used for production transactions.

#### TEST *= 1*

Test network, used for testing and development.

#### STAGE *= 2*

Stage network, used for staging and pre-production testing.

### *class* ots.enums.AddressType(\*values)

Enum representing the address type for OTS operations.

#### STANDARD *= 0*

Standard address, is the address of account and index of
any wallet. On mainnet, this address starts with ‘4’.

#### SUBADDRESS *= 1*

Subaddress, is the address of account != 0 and !=0 index of subaddress.
On mainnet, this address starts with ‘8’.

#### INTEGRATED *= 2*

Integrated address, is a standard address with an additional payment ID
integrated into it. This leads that the address has a length of 106 characters,
instead of 95 characters for standard and subaddresses.

### *class* ots.enums.SeedType(\*values)

Enum representing the seed type for OTS operations.
There are some differences in the handling, but the main purpose
for SeedType is for the Seed Languages which yet differ between
the now supported Seed Types.

#### MONERO *= 0*

Monero 24/25 word seed, used for Monero wallets.
Also the Monero Legacy Seed (12/13 word seed).

#### POLYSEED *= 1*

Polyseed, 16 word seed.

### *class* ots.enums.HandleType(\*values)

Enum representing the handle type for OTS operations.

#### INVALID *= 0*

Invalid handle

#### WIPEABLE_STRING *= 1*

Wipeable string handle, used for sensitive data that should be wiped after use.

#### SEED_INDICES *= 2*

Seed indices handle, used for managing seed indices.

#### SEED_LANGUAGE *= 3*

Seed language handle, used for managing seed languages.

#### ADDRESS *= 4*

Address handle, used for managing addresses.

#### SEED *= 5*

Seed handle, used for managing seeds.

#### WALLET *= 6*

Wallet handle, used for managing wallets.

#### TX *= 7*

Transaction handle, used for managing transactions.

#### TX_DESCRIPTION *= 8*

Transaction description handle, used for managing transaction descriptions.

#### TX_WARNING *= 9*

Transaction warning handle, used for managing transaction warnings.

### *class* ots.enums.ResultType(\*values)

Enum representing the type of result returned by OTS functions.

#### NONE *= 0*

No result

#### HANDLE *= 1*

Handle result, used for returning handles.

#### STRING *= 2*

String result, used for returning strings.

#### BOOLEAN *= 4*

Boolean result, used for returning boolean values.

#### NUMBER *= 8*

Number result, used for returning numeric values.

#### COMPARISON *= 16*

Comparison result, used for returning comparison results.

#### ARRAY *= 32*

Array result, used for returning arrays.

#### ADDRESS_TYPE *= 64*

Address type result, used for returning address types.

#### NETWORK *= 128*

Network result, used for returning network types.

#### SEED_TYPE *= 256*

Seed type result, used for returning seed types.

#### ADDRESS_INDEX *= 512*

Address index result, used for returning address indices.

### *class* ots.enums.DataType(\*values)

Enum representing the data type of the result.

#### INVALID *= 0*

Invalid data type

#### INT *= 1*

Integer data type

#### UINT8 *= 3*

Unsigned 8-bit integer data type

#### UINT16 *= 4*

Unsigned 16-bit integer data type

#### UINT32 *= 5*

Unsigned 32-bit integer data type

#### UINT64 *= 6*

Unsigned 64-bit integer data type

#### HANDLE *= 7*

Handle data type, used for returning handles.
