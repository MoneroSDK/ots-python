# Raw

The raw module provides the exact C ABI functions from `ots._ots` in a more Pythonic way. But mak no mistake it is almast like running C code directly. It is not recommended to use this module unless you are familiar with the C ABI and the underlying data structures to archive something that is not possible otherwise.

#### NOTE
This module is intented as a fundation for the procedural (skipped for now) and object-oriented modules.

## Struct wrappers

### *class* ots.raw.ots_result_t(result: \_CDataBase)

Bases: `_opaque_handle_t`

Represents the result of an OTS operation.
Internally it wraps the C ABI ots_result_t struct in a pointer of a pointer type,
so it can be reasonably freed when the object is deleted.

#### ptrptr *: \_CDataBase*

The pointer to the pointer to be able to free the result.

#### HINT
No need to do anything to free the result, then delete the object,
or let it go out of scope and gc will take care of it.

#### *property* cType *: str*

Returns the type of the ptr as a string.
Can be used to distinguish between different types of handles.

* **Returns:**
  The type of the ptr as a string.

#### *property* ptr *: \_CDataBase*

Returns the pointer to the underlying C data type.
Used for almost all operations.

* **Returns:**
  The pointer to the C data type.

### *class* ots.raw.ots_handle_t(handle: \_CDataBase, reference: bool = False)

Bases: `_opaque_handle_t`

Represents a handle to an OTS object.
Internally it wraps the C ABI ots_handle_t struct in a pointer of a pointer type,
so it can be reasonably freed when the object is deleted.

#### ptrptr *: \_CDataBase*

The pointer to the pointer to be able to free the handle.

#### HINT
No need to do anything to free the handle, then delete the object,
or let it go out of scope and gc will take care of it.

#### reference *: bool*

Indicates if the handle is a reference. A reference must not free the underlying
C data type when the object is deleted. But no worry, it is taken care of it
automatically by the wrapper and the library.

#### *property* type *: [HandleType](enums.md#ots.enums.HandleType)*

Returns the type of the handle as a HandleType enum.

#### *property* cType *: str*

Returns the type of the ptr as a string.
Can be used to distinguish between different types of handles.

* **Returns:**
  The type of the ptr as a string.

#### *property* ptr *: \_CDataBase*

Returns the pointer to the underlying C data type.
Used for almost all operations.

* **Returns:**
  The pointer to the C data type.

### *class* ots.raw.ots_tx_description_t(description: \_CDataBase)

Bases: `_opaque_handle_t`

Represents a transaction description struct ots_tx_description_t in OTS, in a pythonic way.

… note:

```default
The underlaying C data type is not cached and on each access the C data type is accessed again.
But the resource impact should be still low, how it is only a lightweight wrapper around the C ABI struct.
```

An example of a sequential usage of this class with minimal impact on the performance is:

```python
desc: ots_description_t = ots_tx_description_t(tx_description_handle)
print(f'tx set: {desc.tx_set}')
print(f'amount in: {desc.amount_in}')
print(f'amount out: {desc.amount_out}')
for flow in desc.flows:
    print(f'flow: {flow.address}: {flow.amount}')
if desc.change:
    print(f'change: {desc.change.address}: {desc.change.amount}')
else:
    print('no change in transaction')
print(f'fee: {desc.fee}')
for transfer in desc.transfers:
    print(f'    Transfer:
        amount in: {transfer.amount_in}
        amount out: {transfer.amount_out}
        ring size: {transfer.ring_size}
        unlock time: {transfer.unlock_time}
        flows:')
    for flow in transfer.flows:
        print(f'                        {flow.address}: {flow.amount}')
    if transfer.change:
        print(f'                Change: {transfer.change.address}: {transfer.change.amount}')
    else:
        print('         No change in transfer')
    print(f'            fee: {transfer.fee}')
    if transfer.payment_id:
        print(f'                payment ID: {transfer.payment_id}')
    print(f'            dummy outputs: {transfer.dummy_outputs}')
    if transfer.tx_extra:
        print(f'                TX Extra: {transfer.tx_extra}')
```

If used with random access it would properties of the transfers.

#### *property* tx_set *: bytes*

Returns the transaction set as bytes.
This is a byte representation of the unsigned transaction set.

#### *property* amount_in *: int*

Returns the amount in the transaction description.
This is the total amount of the transaction.

#### *property* amount_out *: int*

Returns the amount out in the transaction description.
This is the total amount sent in the transaction.

#### *property* flows *: list[[ots_flow_vector_t](#ots.raw.ots_flow_vector_t)]*

Returns the flows in the transaction description.
This is a list of addresses and their corresponding amounts in the transaction.

#### *property* change *: [ots_flow_vector_t](#ots.raw.ots_flow_vector_t) | None*

Returns the change in the transaction description.
This is a tuple of the address and the amount of the change.
If there is no change, it returns None.

#### *property* fee *: int*

Returns the fee in the transaction description.
This is the total fee of the transaction.

#### *property* cType *: str*

Returns the type of the ptr as a string.
Can be used to distinguish between different types of handles.

* **Returns:**
  The type of the ptr as a string.

#### *property* ptr *: \_CDataBase*

Returns the pointer to the underlying C data type.
Used for almost all operations.

* **Returns:**
  The pointer to the C data type.

## Helper functions

### ots.raw.\_unwrap(value: \_CDataBase | [ots_result_t](#ots.raw.ots_result_t) | [ots_handle_t](#ots.raw.ots_handle_t)) → \_CDataBase

Unwraps the given value to its C data type.

* **Parameters:**
  **value** ( *\_CDataBase* *|* [*ots_result_t*](#ots.raw.ots_result_t) *|* [*ots_handle_t*](#ots.raw.ots_handle_t)) – The value to unwrap.
* **Returns:**
  The C data type representation of the value.

### ots.raw.\_is_result(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase | None) → bool

Checks if the given result is a valid ots_result_t or ots_result_t \* \_CDataBase object. Accepts None to not raise an error and return simply silently False.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase* *|* *None*) – The result to check.
* **Returns:**
  True if the result is valid, False otherwise.

### ots.raw.\_is_handle(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase | None) → bool

Checks if the given handle is a valid ots_handle_t or ots_handle_t \* \_CDataBase object. Accepts None to not raise an error and return simply silently False.

* **Parameters:**
  **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase* *|* *None*) – The handle to check.
* **Returns:**
  True if the handle is valid, False otherwise.

### ots.raw.\_raise_on_error(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → None

Raises an exception if the result indicates an error.
Uses Internally [`ots_is_error()`](#ots.raw.ots_is_error) to check for errors.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check for errors.
* **Raises:**
  **Exception** – If the result is an error.

## Functions

### *class* ots.raw.ots_flow_vector_t(address: str = '', amount: int = 0)

Represents a flow vector ots_flow_vector_t in OTS, in a pythonic way.

### *class* ots.raw.ots_transfer_description_t(amount_in: int = 0, amount_out: int = 0, ring_size: int = 0, unlock_time: int = 0, flows: list[~ots.raw.ots_flow_vector_t] = <factory>, change: ~ots.raw.ots_flow_vector_t | None = None, fee: int = 0, payment_id: str | None = None, dummy_outputs: int = 0, tx_extra: str | None = None)

Represents a transfer description ots_transfer_description_t in OTS, in a pythonic way.

### ots.raw.ots_handle_valid(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, handle_type: [HandleType](enums.md#ots.enums.HandleType) | int) → bool

Checks if the given handle is valid.

* **Parameters:**
  * **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle to check.
  * **handle_type** ([*HandleType*](enums.md#ots.enums.HandleType) *|* *int*) – The expected type of the handle.
* **Returns:**
  True if the handle is valid, False otherwise.

### ots.raw.ots_is_error(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result indicates an error.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is an error, False otherwise.

### ots.raw.ots_error_message(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → str | None

Returns the error message from the result.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  The error message as a string, or None if there is no error.

### ots.raw.ots_error_class(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → str | None

Returns the error class from the result.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  The error class as a string, or None if there is no error.

### ots.raw.ots_error_code(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → int

Returns the error code from the result.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  The error code as an integer, or 0 if there is no error.

### ots.raw.ots_is_result(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase | None) → bool

Checks if the given result is a valid result object. None is accepted to not raise an error.
This function returns also False if there is a valid ots_result_t\* struct, but the ots_result_t.error.code is not 0, in this case [`ots_is_error()`](#ots.raw.ots_is_error) will return True.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase* *|* *None*) – The result to check.
* **Returns:**
  True if the result is valid, False otherwise.

### ots.raw.ots_result_is_type(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, result_type: [ResultType](enums.md#ots.enums.ResultType) | int) → bool

Checks if the result is of a specific type.

#### HINT
Better use the direct functions like:

- [`ots_result_is_wipeable_string()`](#ots.raw.ots_result_is_wipeable_string)
- [`ots_result_is_seed_indices()`](#ots.raw.ots_result_is_seed_indices)
- [`ots_result_is_seed_language()`](#ots.raw.ots_result_is_seed_language)
- [`ots_result_is_address()`](#ots.raw.ots_result_is_address)
- [`ots_result_is_seed()`](#ots.raw.ots_result_is_seed)
- [`ots_result_is_wallet()`](#ots.raw.ots_result_is_wallet)
- [`ots_result_is_transaction_description()`](#ots.raw.ots_result_is_transaction_description)
- [`ots_result_is_transaction_warning()`](#ots.raw.ots_result_is_transaction_warning)
- [`ots_result_is_string()`](#ots.raw.ots_result_is_string)
- [`ots_result_is_boolean()`](#ots.raw.ots_result_is_boolean)
- [`ots_result_is_number()`](#ots.raw.ots_result_is_number)
- [`ots_result_is_comparison()`](#ots.raw.ots_result_is_comparison)
- [`ots_result_is_array()`](#ots.raw.ots_result_is_array)
- ots_result_data_is…
- ots_result_data_handle_is…

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is of the specified type, False otherwise.

### ots.raw.ots_result_is_handle(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a handle.

#### HINT
Better use the direct functions.

#### SEE ALSO
[`ots_result_is_type()`](#ots.raw.ots_result_is_type)

Retrieve the handle with [`ots_result_handle()`](#ots.raw.ots_result_handle) if it is a handle.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is a handle, False otherwise.

### ots.raw.ots_result_is_wipeable_string(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a wipeable string handle.
Retrieve the wipeable string handle simply with [`ots_result_handle()`](#ots.raw.ots_result_handle) if it is a wipeable string, like:

```python
ws: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is a wipeable string, False otherwise.

### ots.raw.ots_result_is_seed_indices(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a seed indices handle.
Retrieve the seed indices handle simply with [`ots_result_handle()`](#ots.raw.ots_result_handle) if it is a seed indices, like:

```python
indices: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is a seed indices, False otherwise.

### ots.raw.ots_result_is_seed_language(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a seed language handle.
Retrieve the seed language handle simply with [`ots_result_handle()`](#ots.raw.ots_result_handle) if it is a seed language, like:

```python
language: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is a seed language, False otherwise.

### ots.raw.ots_result_is_address(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is an address handle.
Retrieve the address handle simply with [`ots_result_handle()`](#ots.raw.ots_result_handle) if it is an address, like:

```python
address: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is an address, False otherwise.

### ots.raw.ots_result_is_seed(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a seed handle.
Retrieve the seed handle simply with [`ots_result_handle()`](#ots.raw.ots_result_handle) if it is a seed, like:

```python
seed: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is a seed, False otherwise.

### ots.raw.ots_result_is_wallet(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a wallet handle.
Retrieve the wallet handle simply with [`ots_result_handle()`](#ots.raw.ots_result_handle) if it is a wallet, like:

```python
wallet: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is a wallet, False otherwise.

### ots.raw.ots_result_is_transaction_description(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a transaction description handle.
Retrieve the transaction description handle simply with [`ots_result_handle()`](#ots.raw.ots_result_handle) if it is a transaction description, like:

```python
tx_description: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is a transaction description, False otherwise.

### ots.raw.ots_result_is_transaction_warning(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a transaction warning handle.
Retrieve the transaction warning handle simply with [`ots_result_handle()`](#ots.raw.ots_result_handle) if it is a transaction warning, like:

```python
tx_warning: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is a transaction warning, False otherwise.

### ots.raw.ots_result_is_string(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a string.
Retrieve the string simply with [`ots_result_string()`](#ots.raw.ots_result_string) if it is a string, like:

```python
string: str | None = ots_result_string(result)

# if checked before with `ots_result_is_string`
# no need to check for None
string: str = ots_result_string(result)
```

#### NOTE
Avoid [`ots_result_string_copy()`](#ots.raw.ots_result_string_copy) to avoid double copying the
string as CFFI anyways copies the string.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is a string, False otherwise.

### ots.raw.ots_result_is_boolean(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a boolean.
Retrieve the boolean simply with [`ots_result_boolean()`](#ots.raw.ots_result_boolean) if it is a boolean, like:

```python
boolean: bool = ots_result_boolean(result)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is a boolean, False otherwise.

### ots.raw.ots_result_is_number(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a (unsigned) number.
Retrieve the number simply with [`ots_result_number()`](#ots.raw.ots_result_number) if it is a number, like:

```python
number: int = ots_result_number(result)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is a number, False otherwise.

### ots.raw.ots_result_data_is_type(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, data_type: [DataType](enums.md#ots.enums.DataType) | int) → bool

Checks if the result data is of a specific type.

#### HINT
Better use the direct functions like:

- ots_result_data_is_…

* **Parameters:**
  * **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
  * **data_type** ([*DataType*](enums.md#ots.enums.DataType) *|* *int*) – The expected type of the result data.
* **Returns:**
  True if the result data is of the specified type, False otherwise.

### ots.raw.ots_result_data_is_reference(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data is a reference.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result data is a reference, False otherwise.

### ots.raw.ots_result_data_is_int(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data is an integer.
Retrieve the integer simply with [`ots_result_int_array()`](#ots.raw.ots_result_int_array) or [`ots_result_int_array_reference()`](#ots.raw.ots_result_int_array_reference) if it is an integer array, like:

```python
int_value: list[int] = ots_result_int_array(result)

# or

int_value: list[int] = ots_result_int_array_reference(result)
```

It is also possible to get the entries one by one with [`ots_result_array_get_int()`](#ots.raw.ots_result_array_get_int) if it is an integer array, like:

```python
for i in range(ots_result_size(result)):
    int_value: int = ots_result_array_get_int(result, i)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result data is an integer, False otherwise.

### ots.raw.ots_result_data_is_char(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data is a character.
Retrieve the character simply with [`ots_result_char_array()`](#ots.raw.ots_result_char_array) or [`ots_result_char_array_reference()`](#ots.raw.ots_result_char_array_reference) if it is a character array, like:

```python
chars: bytes = ots_result_char_array(result)
```

Or as uint8 values:

```python
chars: list[int] = ots_result_char_array_uint8(result)
```

Or as a single character with [`ots_result_array_get_char()`](#ots.raw.ots_result_array_get_char) and [`ots_result_array_get_uint8()`](#ots.raw.ots_result_array_get_uint8) if it is a character array, like:

```python
for i in range(ots_result_size(result)):
    char: bytes = ots_result_array_get_char(result, i)

# or

for i in range(ots_result_size(result)):
    char: int = ots_result_array_get_uint8(result, i)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result data is a character, False otherwise.

### ots.raw.ots_result_data_is_uint8(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data is an unsigned 8-bit integer.
Retrieve the unsigned 8-bit integer simply with [`ots_result_uint8_array()`](#ots.raw.ots_result_uint8_array) or [`ots_result_uint8_array_reference()`](#ots.raw.ots_result_uint8_array_reference) if it is an unsigned 8-bit integer array. Or as a single unsigned 8-bit integer with [`ots_result_array_get_uint8()`](#ots.raw.ots_result_array_get_uint8) if it is an unsigned 8-bit integer array.

#### SEE ALSO
[`ots_result_data_is_char()`](#ots.raw.ots_result_data_is_char)

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result data is an unsigned 8-bit integer, False otherwise.

### ots.raw.ots_result_data_is_uint16(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data is an unsigned 16-bit integer.
Retrieve the unsigned 16-bit integer simply with [`ots_result_uint16_array()`](#ots.raw.ots_result_uint16_array) or [`ots_result_uint16_array_reference()`](#ots.raw.ots_result_uint16_array_reference) if it is an unsigned 16-bit integer array, like:

```python
uint16_values: list[int] = ots_result_uint16_array(result)

#or

uint16_values: list[int] = ots_result_uint16_array_reference(result)
```

Or as a single unsigned 16-bit integer with [`ots_result_array_get_uint16()`](#ots.raw.ots_result_array_get_uint16) if it is an unsigned 16-bit integer array, like:

```python
for i in range(ots_result_size(result)):
    uint16_value: int = ots_result_array_get_uint16(result, i)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result data is an unsigned 16-bit integer, False otherwise.

### ots.raw.ots_result_data_is_uint32(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data is an unsigned 32-bit integer.
Retrieve the unsigned 32-bit integer simply with [`ots_result_uint32_array()`](#ots.raw.ots_result_uint32_array) or [`ots_result_uint32_array_reference()`](#ots.raw.ots_result_uint32_array_reference) if it is an unsigned 32-bit integer array, like:

```python
uint32_values: list[int] = ots_result_uint32_array(result)

# or

uint32_values: list[int] = ots_result_uint32_array_reference(result)
```

Or as a single unsigned 32-bit integer with [`ots_result_array_get_uint32()`](#ots.raw.ots_result_array_get_uint32) if it is an unsigned 32-bit integer array, like:

```python
for i in range(ots_result_size(result)):
    uint32_value: int = ots_result_array_get_uint32(result, i)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result data is an unsigned 32-bit integer, False otherwise.

### ots.raw.ots_result_data_is_uint64(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data is an unsigned 64-bit integer.
Retrieve the unsigned 64-bit integer simply with [`ots_result_uint64_array()`](#ots.raw.ots_result_uint64_array) or [`ots_result_uint64_array_reference()`](#ots.raw.ots_result_uint64_array_reference) if it is an unsigned 64-bit integer array, like:

```python
uint64_values: list[int] = ots_result_uint64_array(result)

# or

uint64_values: list[int] = ots_result_uint64_array_reference(result)
```

Or as a single unsigned 64-bit integer with [`ots_result_array_get_uint64()`](#ots.raw.ots_result_array_get_uint64) if it is an unsigned 64-bit integer array, like:

```python
for i in range(ots_result_size(result)):
    uint64_value: int = ots_result_array_get_uint64(result, i)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result data is an unsigned 64-bit integer, False otherwise.

### ots.raw.ots_result_data_is_handle(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data is a handle.
Retrieve the handle simply with [`ots_result_handle_array()`](#ots.raw.ots_result_handle_array) or [`ots_result_handle_array_reference()`](#ots.raw.ots_result_handle_array_reference) if it is a handle array, like:

```python
handles: list[ots_handle_t] = ots_result_handle_array(result)

# or

handles: list[ots_handle_t] = ots_result_handle_array_reference(result)
```

Or as a single handle with [`ots_result_array_get_handle()`](#ots.raw.ots_result_array_get_handle) if it is a handle array, like:

```python
for i in range(ots_result_size(result)):
    handle: ots_handle_t = ots_result_array_get_handle(result, i)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result data is a handle, False otherwise.

### ots.raw.ots_result_data_handle_is_type(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, handle_type: [HandleType](enums.md#ots.enums.HandleType) | int) → bool

Checks if the result data handle is of a specific type.

#### HINT
Better use the direct functions like:

- ots_result_data_handle_is_…

* **Parameters:**
  * **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
  * **handle_type** ([*HandleType*](enums.md#ots.enums.HandleType) *|* *int*) – The expected type of the handle.
* **Returns:**
  True if the handle is of the specified type, False otherwise.

### ots.raw.ots_result_data_handle_is_reference(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data handle is a reference.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the handle is a reference, False otherwise.

### ots.raw.ots_result_data_handle_is_wipeable_string(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data handle is a wipeable string.
Retrieve the wipeable string handle simply with [`ots_result_handle_array()`](#ots.raw.ots_result_handle_array) or [`ots_result_handle_array_reference()`](#ots.raw.ots_result_handle_array_reference) if it is a wipeable string handle array, like:

```python
wipeable_strings: list[ots_handle_t] = ots_result_handle_array(result)

# or

wipeable_strings: list[ots_handle_t] = ots_result_handle_array_reference(result)
```

Or as a single wipeable string handle with [`ots_result_array_get_handle()`](#ots.raw.ots_result_array_get_handle) if it is a wipeable string handle array, like:

```python
for i in range(ots_result_size(result)):
    wipeable_string: ots_handle_t = ots_result_array_get_handle(result, i)
```

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the handle is a wipeable string, False otherwise.

### ots.raw.ots_result_data_handle_is_seed_indices(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data handle is seed indices.

#### SEE ALSO
How to retrieve the handles:

[`ots_result_data_is_handle()`](#ots.raw.ots_result_data_is_handle)

and

[`ots_result_data_handle_is_wipeable_string()`](#ots.raw.ots_result_data_handle_is_wipeable_string)

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the handle is seed indices, False otherwise.

### ots.raw.ots_result_data_handle_is_seed_language(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data handle is a seed language.

#### SEE ALSO
How to retrieve the handles:

[`ots_result_data_is_handle()`](#ots.raw.ots_result_data_is_handle)

and

[`ots_result_data_handle_is_wipeable_string()`](#ots.raw.ots_result_data_handle_is_wipeable_string)

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the handle is a seed language, False otherwise.

### ots.raw.ots_result_data_handle_is_address(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data handle is an address.

#### SEE ALSO
How to retrieve the handles:

[`ots_result_data_is_handle()`](#ots.raw.ots_result_data_is_handle)

and

[`ots_result_data_handle_is_wipeable_string()`](#ots.raw.ots_result_data_handle_is_wipeable_string)

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the handle is an address, False otherwise.

### ots.raw.ots_result_data_handle_is_seed(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data handle is a seed.

#### SEE ALSO
How to retrieve the handles:

[`ots_result_data_is_handle()`](#ots.raw.ots_result_data_is_handle)

and

[`ots_result_data_handle_is_wipeable_string()`](#ots.raw.ots_result_data_handle_is_wipeable_string)

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the handle is a seed, False otherwise.

### ots.raw.ots_result_data_handle_is_wallet(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data handle is a wallet.

#### SEE ALSO
How to retrieve the handles:

[`ots_result_data_is_handle()`](#ots.raw.ots_result_data_is_handle)

and

[`ots_result_data_handle_is_wipeable_string()`](#ots.raw.ots_result_data_handle_is_wipeable_string)

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the handle is a wallet, False otherwise.

### ots.raw.ots_result_data_handle_is_transaction_description(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data handle is a transaction description.

#### SEE ALSO
How to retrieve the handles:

[`ots_result_data_is_handle()`](#ots.raw.ots_result_data_is_handle)

and

[`ots_result_data_handle_is_wipeable_string()`](#ots.raw.ots_result_data_handle_is_wipeable_string)

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the handle is a transaction description, False otherwise.

### ots.raw.ots_result_data_handle_is_transaction_warning(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result data handle is a transaction warning.

#### SEE ALSO
How to retrieve the handles:

[`ots_result_data_is_handle()`](#ots.raw.ots_result_data_is_handle)

and

[`ots_result_data_handle_is_wipeable_string()`](#ots.raw.ots_result_data_handle_is_wipeable_string)

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the handle is a transaction warning, False otherwise.

### ots.raw.ots_result_handle(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → [ots_handle_t](#ots.raw.ots_handle_t)

Returns the handle from the result.

```python
handle: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **result** – The result to get the handle from.
* **Returns:**
  An ots_handle_t object containing the handle, or None if there is no handle.

### ots.raw.ots_result_handle_is_type(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, type: [HandleType](enums.md#ots.enums.HandleType) | int) → bool

Checks if the result handle is of a specific type.

#### HINT
Better use the direct functions like:

- ots_result_handle_is_…

* **Parameters:**
  * **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
  * **type** ([*HandleType*](enums.md#ots.enums.HandleType) *|* *int*) – The expected type of the handle.
* **Returns:**
  True if the handle is of the specified type, False otherwise.

### ots.raw.ots_result_handle_is_reference(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result handle is a reference.

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the handle is a reference, False otherwise.

### ots.raw.ots_result_string(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → str | None

Returns the string from the result.

```python
string: str | None = ots_result_string(result)

# if checked before with `ots_result_is_string`
# no need to check for None
string: str = ots_result_string(result)
```

* **Parameters:**
  **result** – The result to get the string from.
* **Result:**
  ots_result_t | \_CDataBase
* **Returns:**
  The string as a UTF-8 encoded string, or None if there is no string.

### ots.raw.ots_result_string_copy(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → str | None

Returns a copy of the string from the result.
(In Python this is the same result as ots_result_string)

#### WARNING
This function copies the string, which is not necessary in Python as CFFI already does this. Do not use, use instead [`ots_result_string()`](#ots.raw.ots_result_string).

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to get the string from.
* **Returns:**
  A copy of the string as a UTF-8 encoded string, or None if there is no string.

### ots.raw.ots_result_boolean(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, default_value: bool = False) → bool

Returns the boolean value from the result.

```python
boolean: bool = ots_result_boolean(result)
```

* **Parameters:**
  * **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to get the boolean from.
  * **default_value** (*bool*) – The default value to return if the result is not a boolean.
* **Returns:**
  The boolean value, or the default value if the result is not a boolean.

### ots.raw.ots_result_number(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, default_value: int = -1) → int

Returns the number from the result.

```python
number: int = ots_result_number(result)
```

* **Parameters:**
  * **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to get the number from.
  * **default_value** (*int*) – The default value to return if the result is not a number. By default it is -1 which can not be returned by the C function how it is unsigned.
* **Returns:**
  The number as an integer, or the default value if the result is not a number.

### ots.raw.ots_result_array(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → \_CDataBase

Returns the array from the result.

#### HINT
No need to use, use simply the dedicated functions like:

- ots_result_handle_array
- ots_result_int_array
- ots_result_char_array

and so on.

* **Parameters:**
  **result** – The result to get the array from.
* **Returns:**
  \_CDataBase objects representing the array elements.

### ots.raw.ots_result_array_get(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, index: int) → \_CDataBase

Returns the element at the specified index from the result array.

#### HINT
No need to use, use simply the dedicated functions like:

- ots_result_array_get_handle
- ots_result_array_get_int
- ots_result_array_get_char

and so on.

* **Parameters:**
  * **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to get the element from.
  * **index** (*int*) – The index of the element to retrieve.
* **Returns:**
  The element at the specified index, or None if the index is out of bounds.

### ots.raw.ots_result_array_get_handle(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, index: int) → [ots_handle_t](#ots.raw.ots_handle_t)

Returns the handle at the specified index from the result array.

```python
handle: ots_handle_t = ots_result_array_get_handle(result, index)
```

* **Parameters:**
  * **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to get the handle from.
  * **index** (*int*) – The index of the handle to retrieve.
* **Returns:**
  An ots_handle_t object containing the handle at the specified index, or None if the index is out of bounds.

### ots.raw.ots_result_array_get_int(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, index: int) → int

Returns the integer at the specified index from the result array.

```python
int_value: int = ots_result_array_get_int(result, index)
```

* **Parameters:**
  * **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to get the integer from.
  * **index** (*int*) – The index of the integer to retrieve.
* **Returns:**
  The integer at the specified index, or None if the index is out of bounds.

### ots.raw.ots_result_array_get_char(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, index: int) → bytes

Returns the character at the specified index from the result array.

```python
char: bytes = ots_result_array_get_char(result, index)
```

* **Parameters:**
  * **result** – The result to get the character from.
  * **index** – The index of the character to retrieve.
* **Returns:**
  The character at the specified index, or None if the index is out of bounds.

### ots.raw.ots_result_array_get_uint8(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, index: int) → int

Returns the unsigned 8-bit integer at the specified index from the result array.

```python
uint8_value: int = ots_result_array_get_uint8(result, index)
```

* **Parameters:**
  * **result** – The result to get the unsigned 8-bit integer from.
  * **index** – The index of the unsigned 8-bit integer to retrieve.
* **Returns:**
  The unsigned 8-bit integer at the specified index, or None if the index is out of bounds.

### ots.raw.ots_result_array_get_uint16(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, index: int) → int

Returns the unsigned 16-bit integer at the specified index from the result array.

```python
uint16_value: int = ots_result_array_get_uint16(result, index)
```

* **Parameters:**
  * **result** – The result to get the unsigned 16-bit integer from.
  * **index** – The index of the unsigned 16-bit integer to retrieve.
* **Returns:**
  The unsigned 16-bit integer at the specified index

### ots.raw.ots_result_array_get_uint32(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, index: int) → int

Returns the unsigned 32-bit integer at the specified index from the result array.

```python
uint32_value: int = ots_result_array_get_uint32(result, index)
```

* **Parameters:**
  * **result** – The result to get the unsigned 32-bit integer from.
  * **index** – The index of the unsigned 32-bit integer to retrieve.
* **Returns:**
  The unsigned 32-bit integer at the specified index

### ots.raw.ots_result_array_get_uint64(result: \_CDataBase | None, index: int) → int

Returns the unsigned 64-bit integer at the specified index from the result array.

```python
uint64_value: int = ots_result_array_get_uint64(result, index)
```

* **Parameters:**
  * **result** – The result to get the unsigned 64-bit integer from.
  * **index** – The index of the unsigned 64-bit integer to retrieve.
* **Returns:**
  The unsigned 64-bit integer at the specified index

### ots.raw.ots_result_array_reference(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → \_CDataBase

Returns a reference to the array from the result.

#### HINT
No need to use, use simply the dedicated functions instead.

* **Parameters:**
  **result** – The result to get the array reference from.
* **Returns:**
  A \_CDataBase object representing the array reference.

### ots.raw.ots_result_handle_array_reference(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[[ots_handle_t](#ots.raw.ots_handle_t)]

Returns a reference to the array of handles from the result.

```python
handles: list[ots_handle_t] = ots_result_handle_array_reference(result)
```

* **Parameters:**
  **result** – The result to get the handle array reference from.
* **Returns:**
  A list of ots_handle_t objects representing the handle array reference.

### ots.raw.ots_result_int_array_reference(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[int]

Returns a reference to the array of integers from the result.

```python
int_values: list[int] = ots_result_int_array_reference(result)
```

* **Parameters:**
  **result** – The result to get the integer array reference from.
* **Returns:**
  A list of integers representing the integer array reference.

### ots.raw.ots_result_char_array_reference(result: \_CDataBase | None) → bytes

Returns a reference to the array of characters from the result.

```python
char_array: bytes = ots_result_char_array_reference(result)
```

* **Parameters:**
  **result** – The result to get the character array reference from.
* **Returns:**
  bytes representing the character array reference.

### ots.raw.ots_result_uint8_array_reference(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[int]

Returns a reference to the array of unsigned 8-bit integers from the result.

```python
uint8_values: list[int] = ots_result_uint8_array_reference(result)
```

* **Parameters:**
  **result** – The result to get the unsigned 8-bit integer array reference from.
* **Returns:**
  A list of unsigned 8-bit integers representing the unsigned 8-bit integer array reference.

### ots.raw.ots_result_uint16_array_reference(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[int]

Returns a reference to the array of unsigned 16-bit integers from the result.

```python
uint16_values: list[int] = ots_result_uint16_array_reference(result)
```

* **Parameters:**
  **result** – The result to get the unsigned 16-bit integer array reference from.
* **Returns:**
  A list of unsigned 16-bit integers representing the unsigned 16-bit integer array reference.

### ots.raw.ots_result_uint32_array_reference(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[int]

Returns a reference to the array of unsigned 32-bit integers from the result.

```python
uint32_values: list[int] = ots_result_uint32_array_reference(result)
```

* **Parameters:**
  **result** – The result to get the unsigned 32-bit integer array reference from.
* **Returns:**
  A list of unsigned 32-bit integers representing the unsigned 32-bit integer array reference.

### ots.raw.ots_result_uint64_array_reference(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[int]

Returns a reference to the array of unsigned 64-bit integers from the result.

```python
uint64_values: list[int] = ots_result_uint64_array_reference(result)
```

* **Parameters:**
  **result** – The result to get the unsigned 64-bit integer array reference from.
* **Returns:**
  A list of unsigned 64-bit integers representing the unsigned 64-bit integer array reference.

### ots.raw.ots_result_handle_array(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[[ots_handle_t](#ots.raw.ots_handle_t)]

Returns a list of handles from the result array.

```python
handles: list[ots_handle_t] = ots_result_handle_array(result)
```

* **Parameters:**
  **result** – The result to get the handles from.
* **Returns:**
  A list of \_CDataBase objects representing the handles in the result array.

### ots.raw.ots_result_int_array(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[int]

Returns a list of integers from the result array.

```python
int_values: list[int] = ots_result_int_array(result)
```

* **Parameters:**
  **result** – The result to get the integers from.
* **Returns:**
  A list of integers representing the integers in the result array.

### ots.raw.ots_result_char_array(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bytes

Returns a byte string representing the character array from the result.

```python
char_array: bytes = ots_result_char_array(result)
```

* **Parameters:**
  **result** – The result to get the character array from.
* **Returns:**
  A byte string representing the character array.

### ots.raw.ots_result_uint8_array(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[int]

Returns a list of unsigned 8-bit integers from the result array.

```python
uint8_values: list[int] = ots_result_uint8_array(result)
```

* **Parameters:**
  **result** – The result to get the unsigned 8-bit integers from.
* **Returns:**
  A list of unsigned 8-bit integers representing the unsigned 8-bit integers in the result array.

### ots.raw.ots_result_uint16_array(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[int]

Returns a list of unsigned 16-bit integers from the result array.

```python
uint16_values: list[int] = ots_result_uint16_array(result)
```

* **Parameters:**
  **result** – The result to get the unsigned 16-bit integers from.
* **Returns:**
  A list of unsigned 16-bit integers representing the unsigned 16-bit integers in the result array.

### ots.raw.ots_result_uint32_array(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[int]

Returns a list of unsigned 32-bit integers from the result array.

```python
uint32_values: list[int] = ots_result_uint32_array(result)
```

* **Parameters:**
  **result** – The result to get the unsigned 32-bit integers from.
* **Returns:**
  A list of unsigned 32-bit integers representing the unsigned 32-bit integers in the result array.

### ots.raw.ots_result_uint64_array(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → list[int]

Returns a list of unsigned 64-bit integers from the result array.

```python
uint64_values: list[int] = ots_result_uint64_array(result)
```

* **Parameters:**
  **result** – The result to get the unsigned 64-bit integers from.
* **Returns:**
  A list of unsigned 64-bit integers representing the unsigned 64-bit integers in the result array.

### ots.raw.ots_result_is_array(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is an array.

#### HINT
Check directly for what to expect in the array, like:

- ots_result_data_is_handle
- ots_result_data_is_int
- ots_result_data_is_char
- ots_result_data_is_uint8

and so on.

* **Parameters:**
  **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
* **Returns:**
  True if the result is an array, False otherwise.

### ots.raw.ots_result_is_comparison(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a comparison result.
To retrieve the comparison result, use [`ots_result_comparison()`](#ots.raw.ots_result_comparison),
or if only interested if the result is equal, use [`ots_result_is_equal()`](#ots.raw.ots_result_is_equal).
Like:

```python
# is smaller than
if ots_result_is_comparison(result) and ots_result_comparison(result) < 0:
# is equal to
if ots_result_is_comparison(result) and ots_result_is_equal(result):
```

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the result is a comparison result, False otherwise.

### ots.raw.ots_result_comparison(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → int

Returns the comparison result.

```python
comparison: int = ots_result_comparison(result)
```

* **Parameters:**
  **result** – The result to get the comparison from.
* **Returns:**
  The comparison result as an integer.

### ots.raw.ots_result_is_equal(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is equal to another result.

```python
is_equal: bool = ots_result_is_equal(result)
```

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the result is equal, False otherwise.

### ots.raw.ots_result_size(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → int

Returns the size of the result if the result is an array or a string.

```python
size: int = ots_result_size(result)
```

* **Parameters:**
  **result** – The result to get the size from.
* **Returns:**
  The size of the result as an integer.

### ots.raw.ots_result_is_address_type(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is an address type.
If the result is an address type, you can check the type of the address using
[`ots_result_address_type_is_type()`](#ots.raw.ots_result_address_type_is_type).

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the result is an address type, False otherwise.

### ots.raw.ots_result_address_type(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → [AddressType](enums.md#ots.enums.AddressType)

Returns the address type from the result.

```python
address_type: AddressType = ots_result_address_type(result)
```

* **Parameters:**
  **result** – The result to get the address type from.
* **Returns:**
  The address type as an AddressType object.

### ots.raw.ots_result_address_type_is_type(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, type: [AddressType](enums.md#ots.enums.AddressType) | int) → bool

Checks if the result address type is of a specific type.

```python
is_type: bool = ots_result_address_type_is_type(result, AddressType.STANDARD)
```

* **Parameters:**
  * **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
  * **type** ([*AddressType*](enums.md#ots.enums.AddressType) *|* *int*) – The expected type of the address.
* **Returns:**
  True if the address is of the specified type, False otherwise.

### ots.raw.ots_result_is_address_index(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is an address index.
If the result is an address index, you can retrieve the account and index using
[`ots_result_address_index_account()`](#ots.raw.ots_result_address_index_account) and [`ots_result_address_index_index()`](#ots.raw.ots_result_address_index_index).

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the result is an address index, False otherwise.

### ots.raw.ots_result_address_index_account(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → int

Returns the account index from the result address index.

```python
account_index: int = ots_result_address_index_account(result)
```

* **Parameters:**
  **result** – The result to get the account index from.
* **Returns:**
  The account index as an integer.

### ots.raw.ots_result_address_index_index(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → int

Returns the index from the result address index.

```python
index: int = ots_result_address_index_index(result)
```

* **Parameters:**
  **result** – The result to get the index from.
* **Returns:**
  The index as an integer.

### ots.raw.ots_result_is_network(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a network type.
If the result is a network type, you can retrieve the network using
[`ots_result_network()`](#ots.raw.ots_result_network) to get the network type or to check
the network type using [`ots_result_network_is_type()`](#ots.raw.ots_result_network_is_type).

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the result is a network type, False otherwise.

### ots.raw.ots_result_network(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → [Network](enums.md#ots.enums.Network)

Returns the network from the result.

```python
network: Network = ots_result_network(result)
```

* **Parameters:**
  **result** – The result to get the network from.
* **Returns:**
  The network as a Network object.

### ots.raw.ots_result_network_is_type(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, network: [Network](enums.md#ots.enums.Network) | int) → bool

Checks if the result network is of a specific type.

```python
is_type: bool = ots_result_network_is_type(result, Network.MAIN)
```

* **Parameters:**
  * **result** – The result to check.
  * **network** – The expected type of the network.
* **Returns:**
  True if the network is of the specified type, False otherwise.

### ots.raw.ots_result_is_seed_type(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → bool

Checks if the result is a seed type.
If the result is a seed type, you can retrieve the seed type using
[`ots_result_seed_type()`](#ots.raw.ots_result_seed_type) or check the seed type using
[`ots_result_seed_type_is_type()`](#ots.raw.ots_result_seed_type_is_type).

* **Parameters:**
  **result** – The result to check.
* **Returns:**
  True if the result is a seed type, False otherwise.

### ots.raw.ots_result_seed_type(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → [SeedType](enums.md#ots.enums.SeedType)

Returns the seed type from the result.

```python
seed_type: SeedType = ots_result_seed_type(result)
```

* **Parameters:**
  **result** – The result to get the seed type from.
* **Returns:**
  The seed type as a SeedType object.

### ots.raw.ots_result_seed_type_is_type(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase, type: [SeedType](enums.md#ots.enums.SeedType) | int) → bool

Checks if the result seed type is of a specific type.

```python
is_type: bool = ots_result_seed_type_is_type(result, SeedType.MONERO)
```

* **Parameters:**
  * **result** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result to check.
  * **type** ([*SeedType*](enums.md#ots.enums.SeedType) *|* *int*) – The expected type of the seed.
* **Returns:**
  True if the seed is of the specified type, False otherwise.

### ots.raw.ots_free_string(string: \_CDataBase) → None

Frees a string allocated by OTS functions.

* **Parameters:**
  **string** ( *\_CDataBase*) – The null terminated string to free.

### ots.raw.ots_free_binary_string(string: \_CDataBase, size: int) → None

Frees a binary string allocated by OTS functions.

* **Parameters:**
  * **string** ( *\_CDataBase*) – The binary string to free.
  * **size** (*int*) – The size of the binary string.

### ots.raw.ots_free_array(arr: \_CDataBase, elem_size: int, count: int) → None

Frees an array allocated by OTS functions.

* **Parameters:**
  * **arr** ( *\_CDataBase*) – The array to free.
  * **elem_size** (*int*) – The size of each element in the array.
  * **count** (*int*) – The number of elements in the array.

### ots.raw.ots_free_result(result: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → None

Frees the result object returned by OTS functions.
:param result: The result to free.
:type result: ots_result_t | \_CDataBase

#### WARNING
Use del result instead of this function in Python if
you are using it on a ots_result_t, to clean up all.

### ots.raw.ots_free_handle(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → None

Frees the handle object returned by OTS functions.

* **Parameters:**
  **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle to free.

#### WARNING
Use del handle instead of this function in Python if
you are using it on a ots_handle_t, to clean up all.

### ots.raw.ots_free_tx_description(tx_description: [ots_tx_description_t](#ots.raw.ots_tx_description_t) | \_CDataBase) → None

Frees the transaction description object returned by OTS functions.

* **Parameters:**
  **tx_description** ([*ots_tx_description_t*](#ots.raw.ots_tx_description_t) *|*  *\_CDataBase*) – The transaction description to free.

### ots.raw.ots_secure_free(buffer: \_CDataBase, size: int) → None

Securely frees a buffer by overwriting its contents before deallocation.

* **Parameters:**
  * **buffer** ( *\_CDataBase*) – The buffer to free.
  * **size** (*int*) – The size of the buffer.

### ots.raw.ots_wipeable_string_create(string: str) → [ots_result_t](#ots.raw.ots_result_t)

Creates a wipeable string from a regular string.

```python
my_string = "my wipeable string"
result: ots_result_t = ots_wipeable_string_create(my_string)
ws: ots_handle_t = ots_result_handle(result)
ots_wipeable_string_c_str(ws) == my_string
```

* **Parameters:**
  **string** (*str*) – The string to create a wipeable string from.
* **Returns:**
  ots_result_t containing the created wipeable string.

### ots.raw.ots_wipeable_string_compare(str1: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, str2: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Compares two wipeable strings.

```python
str1: ots_handle_t = ots_wipeable_string_create("aaa")
str2: ots_handle_t = ots_wipeable_string_create("bbb")
result: ots_result_t = ots_wipeable_string_compare(str1, str2)
assert ots_result_is_comparison(result)
assert ots_result_comparison(result) < 0  # str1 is less than str2
assert ots_result_is_equal(result) is False  # str1 is not equal to str2
```

* **Parameters:**
  * **str1** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The first string to compare.
  * **str2** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The second string to compare.
* **Returns:**
  ots_result_t indicating the comparison result.

### ots.raw.ots_wipeable_string_c_str(string: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → str

Returns the C-style string representation of a wipeable string.

```python
my_string = "my wipeable string"
result: ots_result_t = ots_wipeable_string_create(my_string)
ws: ots_handle_t = ots_result_handle(result)
assert ots_wipeable_string_c_str(ws) == my_string
```

* **Parameters:**
  **string** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The wipeable string to convert.
* **Returns:**
  The string representation.

### ots.raw.ots_seed_indices_create(indices: list[int]) → [ots_result_t](#ots.raw.ots_result_t)

Creates a seed indices object from a list of integers.

```python
indices = [1, 2, 3, 4]
result: ots_result_t = ots_seed_indices_create(indices)
si: ots_handle_t = ots_result_handle(result)
assert ots_seed_indices_values(si) == indices
```

* **Parameters:**
  **indices** (*list* *[**int* *]*) – A list of integers representing the seed indices.
* **Returns:**
  ots_result_t containing the created seed indices object.

### ots.raw.ots_seed_indices_create_from_string(string: str, separator: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Creates a seed indices object from a string representation of indices.

```python
indices_string = "0001000200030004"
result: ots_result_t = ots_seed_indices_create_from_string(indices_string)
si: ots_handle_t = ots_result_handle(result)
assert ots_seed_indices_values(si) == [1, 2, 3, 4]

# or

indices_string = "0001, 0002, 0003, 0004"
result: ots_result_t = ots_seed_indices_create_from_string(indices_string, separator=', ')
si: ots_handle_t = ots_result_handle(result)
assert ots_seed_indices_values(si) == [1, 2, 3, 4]
```

* **Parameters:**
  * **string** (*str*) – A string containing the indices separated by the specified separator.
  * **separator** (*str*) – The separator used in the string (default is an empty string).
* **Returns:**
  ots_result_t containing the created seed indices object.

### ots.raw.ots_seed_indices_create_from_hex(hex: str, separator: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Creates a seed indices object from a hexadecimal string representation of indices.

```python
hex_string = "0B10B20B30B4"
result: ots_result_t = ots_seed_indices_create_from_hex(hex_string)
si: ots_handle_t = ots_result_handle(result)
assert ots_seed_indices_values(si) == [177, 178, 179, 180]

# or

hex_string = "0B1|0B2|0B3|0B4"
result: ots_result_t = ots_seed_indices_create_from_hex(hex_string, separator='|')
si: ots_handle_t = ots_result_handle(result)
assert ots_seed_indices_values(si) == [177, 178, 179, 180]
```

* **Parameters:**
  * **hex** (*str*) – A hexadecimal string containing the indices separated by the specified separator.
  * **separator** (*str*) – The separator used in the string (default is a comma).
* **Returns:**
  ots_result_t containing the created seed indices object.

### ots.raw.ots_seed_indices_values(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → list[int]

Returns the values of the seed indices as a list of integers.

```python
indices: list[int] = [1, 2, 3, 4]
result: ots_result_t = ots_seed_indices_create(indices)
si: ots_handle_t = ots_result_handle(result)
assert ots_seed_indices_values(si) == indices
```

* **Parameters:**
  **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle containing the seed indices.
* **Returns:**
  A list of integers representing the seed indices.

### ots.raw.ots_seed_indices_count(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → int

Returns the count of seed indices in the handle.

```python
indices: list[int] = [1, 2, 3, 4]
result: ots_result_t = ots_seed_indices_create(indices)
si: ots_handle_t = ots_result_handle(result)
count: int = ots_seed_indices_count(si)
assert count == len(indices)
```

* **Parameters:**
  **handle** – The handle containing the seed indices.
* **Returns:**
  The count of seed indices as an integer.

### ots.raw.ots_seed_indices_clear(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → None

Clears the seed indices in the handle.

```python
indices: list[int] = [1, 2, 3, 4]
result: ots_result_t = ots_seed_indices_create(indices)
si: ots_handle_t = ots_result_handle(result)
assert ots_seed_indices_count(si) == len(indices)
ots_seed_indices_clear(si)
assert ots_seed_indices_count(si) == 0
```

#### NOTE
Clear not only clears the indices but also securely wipes the memory used by the indices.

* **Parameters:**
  **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle containing the seed indices to clear.

### ots.raw.ots_seed_indices_append(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, value: int) → None

Appends a value to the seed indices in the handle.

```python
indices: list[int] = [1, 2, 3]
result: ots_result_t = ots_seed_indices_create(indices)
si: ots_handle_t = ots_result_handle(result)
ots_seed_indices_append(si, 4)
assert ots_seed_indices_values(si) == [1, 2, 3, 4]
```

* **Parameters:**
  * **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle containing the seed indices.
  * **value** (*int*) – The uint16 value to append to the seed indices.

### ots.raw.ots_seed_indices_numeric(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, separator: str = '') → str

Returns a string representation of the seed indices in numeric format.

```python
indices: list[int] = [1, 2, 3, 4]
result: ots_result_t = ots_seed_indices_create(indices)
si: ots_handle_t = ots_result_handle(result)
numeric_string: str = ots_seed_indices_numeric(si, separator=', ')
assert numeric_string == '1, 2, 3, 4'
```

* **Parameters:**
  * **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle containing the seed indices.
  * **separator** (*str*) – The separator to use between indices (default is an empty string).
* **Returns:**
  A string representing the seed indices in numeric format.

### ots.raw.ots_seed_indices_hex(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, separator: str = '') → str

Returns a string representation of the seed indices in hexadecimal format.

```python
indices: list[int] = [177, 178, 179, 180]
result: ots_result_t = ots_seed_indices_create(indices)
si: ots_handle_t = ots_result_handle(result)
hex_string: str = ots_seed_indices_hex(si, separator=':')
assert hex_string == '0B1:0B2:0B3:0B4'
```

* **Parameters:**
  * **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle containing the seed indices.
  * **separator** (*str*) – The separator to use between indices (default is a comma).
* **Returns:**
  A string representing the seed indices in hexadecimal format.

### ots.raw.ots_seed_languages() → [ots_result_t](#ots.raw.ots_result_t)

Returns a list of all available seed languages.

```python
result: ots_result_t = ots_seed_languages()
languages: list[ots_handle_t] = ots_result_handle_array_reference(result)
```

* **Returns:**
  ots_result_t containing the list of seed languages.

### ots.raw.ots_seed_languages_for_type(type: [SeedType](enums.md#ots.enums.SeedType) | int) → [ots_result_t](#ots.raw.ots_result_t)

Returns a list of seed languages for a specific seed type.

```python
result: ots_result_t = ots_seed_languages_for_type(SeedType.MONERO)
languages: list[ots_handle_t] = ots_result_handle_array_reference(result)
```

* **Parameters:**
  **type** – The seed type for which to get the languages.
* **Returns:**
  ots_result_t containing the list of seed languages for the specified type.

### ots.raw.ots_seed_language_default(type: [SeedType](enums.md#ots.enums.SeedType) | int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the default seed language for a specific seed type.

#### ATTENTION
The default language for any seed is intentionally not set.
To use this function, you must first set a default language for the seed type
using [`ots_seed_language_set_default()`](#ots.raw.ots_seed_language_set_default) before questioning it.

```python
result: ots_result_t = ots_seed_language_from_code('en')
en: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_set_default(SeedType.MONERO, en)
result = ots_seed_language_default(SeedType.MONERO)
default_language: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_equals(default_language, en)
assert ots_result_bool(result) is True  # default language is now set to 'en'
```

* **Parameters:**
  **type** ([*SeedType*](enums.md#ots.enums.SeedType) *|* *int*) – The seed type for which to get the default language.
* **Returns:**
  ots_result_t containing the default seed language for the specified type.
* **Raise:**
  An error if the default language is not set for the seed type.

### ots.raw.ots_seed_language_set_default(type: [SeedType](enums.md#ots.enums.SeedType) | int, language: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Sets the default seed language for a specific seed type.

```python
result: ots_result_t = ots_seed_language_from_code('en')
en: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_set_default(SeedType.MONERO, en)
default: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_equals(default, en)
assert ots_result_bool(result) is True  # default language is now set to 'en'
```

* **Parameters:**
  * **type** ([*SeedType*](enums.md#ots.enums.SeedType) *|* *int*) – The seed type for which to set the default language.
  * **language** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the language to set as default.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_language_from_code(code: str) → [ots_result_t](#ots.raw.ots_result_t)

Returns a seed language from its code.

```python
result: ots_result_t = ots_seed_language_from_code('en')
en: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_code(en)
assert ots_result_string(result) == 'en'  # en is the code for English
```

* **Parameters:**
  **code** (*str*) – The code of the seed language.
* **Returns:**
  ots_result_t containing the seed language corresponding to the given code.

### ots.raw.ots_seed_language_from_name(name: str) → [ots_result_t](#ots.raw.ots_result_t)

Returns a seed language from its name.

```python
result: ots_result_t = ots_seed_language_from_name('Deutsch')
de: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_code(de)
assert ots_result_string(result) == 'de'  # de is the code for German
```

* **Parameters:**
  **name** (*str*) – The name of the seed language.
* **Returns:**
  ots_result_t containing the seed language corresponding to the given name.

### ots.raw.ots_seed_language_from_english_name(name: str) → [ots_result_t](#ots.raw.ots_result_t)

Returns a seed language from its English name.

```python
result: ots_result_t = ots_seed_language_from_english_name('Russian')
ru: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_code(ru)
assert ots_result_string(result) == 'ru'  # ru is the code for Russian
```

* **Parameters:**
  **name** (*str*) – The English name of the seed language.
* **Returns:**
  ots_result_t containing the seed language corresponding to the given English name.

### ots.raw.ots_seed_language_code(language: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the code of the seed language.

```python
result: ots_result_t = ots_seed_language_from_code('en')
en: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_code(en)
assert ots_result_string(result) == 'en'  # en is the code for English
```

* **Parameters:**
  **language** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed language.
* **Returns:**
  ots_result_t containing the code of the seed language.

### ots.raw.ots_seed_language_name(language: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the name of the seed language.

```python
result: ots_result_t = ots_seed_language_from_code('de')
de: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_name(de)
assert ots_result_string(result) == 'Deutsch'
```

* **Parameters:**
  **language** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed language.
* **Returns:**
  ots_result_t containing the name of the seed language.

### ots.raw.ots_seed_language_english_name(language: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the English name of the seed language.

```python
result: ots_result_t = ots_seed_language_from_code('de')
de: ots_handle_t = ots_result_handle(result)
assert ots_seed_language_english_name(de) == 'German'
```

* **Parameters:**
  **language** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed language.
* **Returns:**
  ots_result_t containing the English name of the seed language.

### ots.raw.ots_seed_language_supported(language: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, type: [SeedType](enums.md#ots.enums.SeedType) | int) → [ots_result_t](#ots.raw.ots_result_t)

Checks if a seed language is supported for a specific seed type.

```python
result: ots_result_t = ots_seed_language_from_code('en')
en: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_supported(en, SeedType.MONERO)
assert ots_result_boolean(result) is True  # en is supported for MONERO
result = ots_seed_language_supported(en, SeedType.POLYSEED)
assert ots_result_boolean(result) is True  # en is supported for POLYSEED
```

* **Parameters:**
  * **language** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed language.
  * **type** ([*SeedType*](enums.md#ots.enums.SeedType) *|* *int*) – The seed type to check support for.
* **Returns:**
  ots_result_t indicating whether the language is supported for the specified seed type.

### ots.raw.ots_seed_language_is_default(language: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, type: [SeedType](enums.md#ots.enums.SeedType) | int) → [ots_result_t](#ots.raw.ots_result_t)

Checks if a seed language is the default for a specific seed type.

```python
result: ots_result_t = ots_seed_language_from_code('en')
en: ots_handle_t = ots_result_handle(result)
ots_seed_language_set_default(SeedType.MONERO, en)
result = ots_seed_language_is_default(en, SeedType.MONERO)
assert ots_result_boolean(result) is True  # en is the default for MONERO
result = ots_seed_language_is_default(en, SeedType.POLYSEED)
assert ots_result_boolean(result) is False  # en is not the default for POLYSEED
```

* **Parameters:**
  * **language** – The handle of the seed language.
  * **type** – The seed type to check if the language is default for.
* **Returns:**
  ots_result_t indicating whether the language is the default for the specified seed type.

### ots.raw.ots_seed_language_equals(language1: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, language2: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Checks if two seed languages are equal.

```python
result: ots_result_t = ots_seed_language_from_code('en')
en1: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_from_english_name('English')
en2: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_equals(en1, en2)
assert ots_result_boolean(result) is True  # en1 and en2 are equal
```

* **Parameters:**
  * **language1** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The first seed language to compare.
  * **language2** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The second seed language to compare.
* **Returns:**
  ots_result_t indicating whether the two languages are equal.

### ots.raw.ots_seed_language_equals_code(language: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, code: str) → [ots_result_t](#ots.raw.ots_result_t)

Checks if a seed language equals a specific code.

```python
result: ots_result_t = ots_seed_language_from_code('en')
en: ots_handle_t = ots_result_handle(result)
result = ots_seed_language_equals_code(en, 'en')
assert ots_result_boolean(result) is True  # en equals 'en'
```

* **Parameters:**
  * **language** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed language to compare.
  * **code** (*str*) – The code to compare against.
* **Returns:**
  ots_result_t indicating whether the language equals the specified code.

### ots.raw.ots_seed_phrase(seed: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, language: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, password: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Returns the seed phrase for a given seed and language.

… code-block:: python

> result: ots_result_t = ots_monero_seed_generate()
> seed: ots_handle_t = ots_result_handle(result)
> result = ots_seed_language_from_code(‘en’)
> en: ots_handle_t = ots_result_handle(result)
> result = ots_seed_phrase(seed, en, ‘my_password’)
> assert ots_result_is_wipeable_string(result) is True
> phrase: ots_handle_t = ots_result_handle(result)
> assert len(ots_wipeable_string_c_str(phrase).split(’ ‘)) == 25  # Monero seed phrases are 25 words long
* **Parameters:**
  * **seed** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed.
  * **language** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed language.
  * **password** (*str*) – The password to use for generating the seed phrase.
* **Returns:**
  ots_result_t containing the seed phrase.

### ots.raw.ots_seed_phrase_for_language_code(seed: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, language_code: str = '', password: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Returns the seed phrase for a given seed and language code.

… code-block:: python

> result: ots_result_t = ots_monero_seed_generate()
> seed: ots_handle_t = ots_result_handle(result)
> result = ots_seed_phrase(seed, ‘en’, ‘my_password’)
> assert ots_result_is_wipeable_string(result) is True
> phrase: ots_handle_t = ots_result_handle(result)
> assert len(ots_wipeable_string_c_str(phrase).split(’ ‘)) == 25  # Monero seed phrases are 25 words long
* **Parameters:**
  * **seed** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed.
  * **language_code** (*str*) – The code of the seed language.
  * **password** (*str*) – The password to use for generating the seed phrase.
* **Returns:**
  ots_result_t containing the seed phrase.

### ots.raw.ots_seed_indices(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, password: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Returns the seed indices for a given seed handle.

```python
result: ots_result_t = ots_monero_seed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_indices(seed, 'my_password')
assert ots_result_is_seed_indices(result)
si: ots_handle_t = ots_result_handle(result)
assert ots_seed_indices_count(si) == 24  # Monero seeds have 24 indices + 1 checksum (which is dropped on indices)
```

* **Parameters:**
  * **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed.
  * **password** (*str*) – The password to use for generating the seed indices.
* **Returns:**
  ots_result_t containing the seed indices.

### ots.raw.ots_seed_fingerprint(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the fingerprint of a given seed handle.

```python
result: ots_result_t = ots_monero_seed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_fingerprint(seed)
fingerprint: ots_handle_t = ots_result_string(result)
assert len(fingerprint) == 6 and all(c in '0123456789ABCDEF' for c in fingerprint)  # Monero seed fingerprints are 6 hex characters long
```

* **Parameters:**
  **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed.
* **Returns:**
  ots_result_t containing the fingerprint of the seed.

### ots.raw.ots_seed_is_legacy(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Checks if the given seed handle is a legacy seed.

```python
result: ots_result_t = ots_monero_seed_generate()
monero_seed: ots_handle_t = ots_result_handle(result)
result = ots_polyseed_generate()
polyseed: ots_handle_t = ots_result_handle(result)
result = ots_seed_indices(monero_seed)
si: ots_handle_t = ots_result_handle(result)
indices: list[int] = ots_seed_indices_values(si)[:12]  # take 12 indices for legacy seed
result = ots_seed_indices_create(indices)
si = ots_result_handle(result)
result = ots_legacy_seed_decode_indices(si)
legacy_seed: ots_handle_t = ots_result_handle(result)

result = ots_seed_is_legacy(monero_seed)
assert ots_result_bool(result) is False  # Monero seed is not legacy
result = ots_seed_is_legacy(polyseed)
assert ots_result_bool(result) is False  # Polyseed is not legacy
result = ots_seed_is_legacy(legacy_seed)
assert ots_result_bool(result) is True  # Legacy seed is legacy
```

* **Parameters:**
  **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed.
* **Returns:**
  ots_result_t indicating whether the seed is legacy.

### ots.raw.ots_seed_type(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the type of the given seed handle.

```python
result: ots_result_t = ots_monero_seed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_type(seed)
seed_type: SeedType = ots_result_seed_type(result)
assert seed_type == SeedType.MONERO  # Monero seed type
```

* **Parameters:**
  **handle** – The handle of the seed.
* **Returns:**
  ots_result_t containing the type of the seed.

### ots.raw.ots_seed_address(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the address associated with the given seed handle.

```python
result: ots_result_t = ots_monero_seed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_address(seed)
address: ots_handle_t = ots_result_handle(result)
result = ots_address_base58_string(address)
assert len(ots_result_string(address)) == 95  # Monero addresses are 95 characters long
```

* **Parameters:**
  **handle** – The handle of the seed.
* **Returns:**
  ots_result_t containing the address of the seed.

### ots.raw.ots_seed_timestamp(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the timestamp associated with the given seed handle.

```python
result: ots_result_t = ots_monero_seed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_timestamp(seed)
assert ots_result_is_number(result)
timestamp: int = ots_result_number(result)
assert timestamp >= 0  # Timestamp should be a non-negative integer
```

* **Parameters:**
  **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed.
* **Returns:**
  ots_result_t containing the timestamp of the seed.

### ots.raw.ots_seed_height(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the height associated with the given seed handle.

```python
result: ots_result_t = ots_monero_seed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_height(seed)
assert ots_result_is_number(result)
height: int = ots_result_number(result)
assert height >= 0  # Height should be a non-negative integer
```

* **Parameters:**
  **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed.
* **Returns:**
  ots_result_t containing the height of the seed.

### ots.raw.ots_seed_network(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the network associated with the given seed handle.

```python
result: ots_result_t = ots_monero_seed_generate(network=Network.STAGE)
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_network(seed)
network: Network = ots_result_network(result)
assert network == Network.STAGE  # The seed was generated for the STAGE network
```

* **Parameters:**
  **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed.
* **Returns:**
  ots_result_t containing the network of the seed.

### ots.raw.ots_seed_wallet(handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the wallet associated with the given seed handle.

```python
result: ots_result_t = ots_monero_seed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_wallet(seed)
assert ots_result_is_wallet(result)
wallet: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed.
* **Returns:**
  ots_result_t containing the wallet of the seed.

### ots.raw.ots_seed_indices_merge_values(seed_indices1: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, seed_indices2: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Merges two seed indices handles into one.

```python
result: ots_result_t = ots_seed_indices_create([1, 2, 3])
seed_indices1: ots_handle_t = ots_result_handle(result)
result = ots_seed_indices_create([4, 5, 6])
seed_indices2: ots_handle_t = ots_result_handle(result)
result = ots_seed_indices_merge_values(seed_indices1, seed_indices2)
merged_indices: ots_handle_t = ots_result_handle(result)
assert ots_seed_indices_values(merged_indices) == [5, 7, 5]  # [1, 2, 3] ^ [4, 5, 6] = [5, 7, 5]
```

* **Parameters:**
  * **seed_indices1** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The first seed indices handle.
  * **seed_indices2** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The second seed indices handle.
* **Returns:**
  ots_result_t containing the merged seed indices.

### ots.raw.ots_seed_indices_merge_with_password(seed_indices: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, password: str) → [ots_result_t](#ots.raw.ots_result_t)

Merges seed indices with a password.

```python
result: ots_result_t = ots_seed_indices_create([1, 2, 3])
seed_indices: ots_handle_t = ots_result_handle(result)
result = ots_seed_indices_merge_with_password(seed_indices, 'my_password')
assert ots_result_is_seed_indices(result)
merged_indices: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  * **seed_indices** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed indices to merge.
  * **password** (*str*) – The password to use for merging.
* **Returns:**
  ots_result_t containing the merged seed indices.

### ots.raw.ots_seed_indices_merge_multiple_values(seed_indices: list[[ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase], elements: int) → [ots_result_t](#ots.raw.ots_result_t)

Merges multiple seed indices handles into one.

```python
result: ots_result_t = ots_seed_indices_create([1, 2, 3])
seed_indices1: ots_handle_t = ots_result_handle(result)
result = ots_seed_indices_create([4, 5, 6])
seed_indices2: ots_handle_t = ots_result_handle(result)
result = ots_seed_indices_create([5, 7, 5])
seed_indices3: ots_handle_t = ots_result_handle(result)
result = ots_seed_indices_merge_multiple_values([seed_indices1, seed_indices2, seed_indices3], 3)
merged_indices: ots_handle_t = ots_result_handle(result)
assert ots_seed_indices_values(merged_indices) == [0, 0, 0]
```

* **Parameters:**
  * **seed_indices** (*list* *[*[*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase* *]*) – A list of seed indices handles to merge.
  * **elements** (*int*) – The number of elements in the list.
* **Returns:**
  ots_result_t containing the merged seed indices.

### ots.raw.ots_seed_indices_merge_values_and_zero(seed_indices1: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, seed_indices2: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, delete_after: bool) → [ots_result_t](#ots.raw.ots_result_t)

Merges two seed indices handles into one and optionally deletes them after merging.

```python
result: ots_result_t = ots_seed_indices_create([1, 2, 3])
seed_indices1: ots_handle_t = ots_result_handle(result)
result = ots_seed_indices_create([4, 5, 6])
seed_indices2: ots_handle_t = ots_result_handle(result)
result = ots_seed_indices_merge_values_and_zero(seed_indices1, seed_indices2, delete_after=True)
merged_indices: ots_handle_t = ots_result_handle(result)
del seed_indices1, seed_indices2  # Don't use seed_indices1 and seed_indices2 anymore because it will result in a segmentation fault, because the memory is wiped and freed already, but CFFI will not inform the _CDataBase object about it.
```

#### WARNING
Do not use the provided seed indices handles after calling this function
anymore, as they memory will be wiped and with delete_after set to True,
also freed. Using them will result in a segmentation fault. Anyway, the
CFFI will not inform the \_CDataBase object about it, so it will lead
to a segmentation fault when trying to access the handle again.

* **Parameters:**
  * **seed_indices1** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The first seed indices handle.
  * **seed_indices2** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The second seed indices handle.
  * **delete_after** (*bool*) – Whether to delete the original handles after merging.
* **Returns:**
  ots_result_t containing the merged seed indices.

### ots.raw.ots_seed_indices_merge_with_password_and_zero(seed_indices: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, password: str, delete_after: bool) → [ots_result_t](#ots.raw.ots_result_t)

Merges seed indices with a password and optionally deletes the original handle after merging.

```python
result: ots_result_t = ots_seed_indices_create([1, 2, 3])
seed_indices: ots_handle_t = ots_result_handle(result)
result = ots_seed_indices_merge_with_password_and_zero(seed_indices, 'my_password', delete_after=True)
del seed_indices  # Don't use seed_indices anymore because it will result in a segmentation fault, because the memory is wiped and freed already, but CFFI will not inform the _CDataBase object about it.
merged_indices: ots_handle_t = ots_result_handle(result)
```

#### WARNING
Do not use the provided seed indices handle after calling this function
anymore, as the memory will be wiped and with delete_after set to True,
also freed. Using it will result in a segmentation fault. Anyway, the
CFFI will not inform the \_CDataBase object about it, so it will lead
to a segmentation fault when trying to access the handle again.

* **Parameters:**
  * **seed_indices** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed indices to merge.
  * **password** (*str*) – The password to use for merging.
  * **delete_after** (*bool*) – Whether to delete the original handle after merging.
* **Returns:**
  ots_result_t containing the merged seed indices.

### ots.raw.ots_seed_indices_merge_multiple_values_and_zero(seed_indices: list[[ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase] | \_CDataBase, elements: int, delete_after: bool) → [ots_result_t](#ots.raw.ots_result_t)

Merges multiple seed indices handles into one and optionally deletes them after merging.

#### SEE ALSO
[`ots_seed_indices_merge_multiple_values()`](#ots.raw.ots_seed_indices_merge_multiple_values)

#### WARNING
see [`ots_seed_indices_merge_values_and_zero()`](#ots.raw.ots_seed_indices_merge_values_and_zero) about the provided seed handles.

* **Parameters:**
  * **seed_indices** (*list* *[*[*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase* *]*  *|*  *\_CDataBase*) – A list of seed indices handles to merge.
  * **elements** (*int*) – The number of elements in the list.
  * **delete_after** (*bool*) – Whether to delete the original handles after merging.
* **Returns:**
  ots_result_t containing the merged seed indices.

### ots.raw.ots_legacy_seed_decode(phrase: str, height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN) → [ots_result_t](#ots.raw.ots_result_t)

Decodes a legacy seed phrase into its components.

```python
result: ots_result_t = ots_monero_seed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_phrase_for_language_code(seed, 'en')
ws: ots_handle_t = ots_result_handle(result)
phrase: str = ots_wipeable_string_c_str(phrase).split(' ')[:12]
result = ots_legacy_seed_decode(phrase, 1024, network=Network.TEST)
legacy_seed: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  * **phrase** (*str*) – The legacy seed phrase to decode.
  * **height** (*int*) – The height at which the seed was created.
  * **time** (*int*) – The time at which the seed was created.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the seed is intended (Main, Test, or Stagenet).
* **Returns:**
  ots_result_t containing the decoded seed information.

### ots.raw.ots_legacy_seed_decode_indices(indices: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN) → [ots_result_t](#ots.raw.ots_result_t)

Decodes a legacy seed indices handle into its components.

* **Parameters:**
  * **indices** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle containing the legacy seed indices to decode.
  * **height** (*int*) – The height at which the seed was created.
  * **time** (*int*) – The time at which the seed was created.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the seed is intended (Main, Test, or Stagenet).
* **Returns:**
  ots_result_t containing the decoded seed information.

### ots.raw.ots_monero_seed_create(random: bytes, height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN) → [ots_result_t](#ots.raw.ots_result_t)

Creates a new Monero seed with the specified parameters.

```python
from time import time as current_time
result: ots_result_t = ots_random_32()
random: bytes = ots_result_char_array(result)
result = ots_monero_seed_create(random, time=current_time(), network=Network.MAIN)
assert ots_result_is_seed(result)
seed: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  * **random** (*bytes*) – Random 32 bytes to use for seed creation.
  * **height** (*int*) – The height at which the seed is created.
  * **time** (*int*) – The time at which the seed is created.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the seed is intended (Main, Test, or Stagenet).
* **Returns:**
  ots_result_t containing the created Monero seed.

### ots.raw.ots_monero_seed_generate(height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN) → [ots_result_t](#ots.raw.ots_result_t)

Generates a new Monero seed with the specified parameters.

```python
result: ots_result_t = ots_monero_seed_generate()
seed: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  * **height** – The height at which the seed is generated.
  * **time** – The time at which the seed is generated.
  * **network** – The network for which the seed is intended (Main, Test, or Stagenet).
* **Returns:**
  ots_result_t containing the generated Monero seed.

### ots.raw.ots_monero_seed_decode(phrase: str, height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN, passphrase: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Decodes a Monero seed phrase into its components.

```python
result: ots_result_t = ots_monero_seed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_fingerprint(seed)
fp1: str = ots_result_string(result)
result = ots_seed_phrase_for_language_code(seed, 'en', 'my_password')
ws: ots_handle_t = ots_result_handle(result)
phrase: str = ots_wipeable_string_c_str(ws)
result = ots_monero_seed_decode(phrase, passphrase='my_passphrase')
seed2: ots_handle_t = ots_result_handle(result)
result = ots_seed_fingerprint(seed2)
fp2: str = ots_result_string(result)
assert fp1 == fp2  # The fingerprint should match the original seed
```

* **Parameters:**
  * **phrase** (*str*) – The Monero seed phrase to decode.
  * **height** (*int*) – The height at which the seed was created.
  * **time** (*int*) – The time at which the seed was created.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the seed is intended (Main, Test, or Stagenet).
  * **passphrase** (*str*) – An optional passphrase for additional security.
* **Returns:**
  ots_result_t containing the decoded seed information.

### ots.raw.ots_monero_seed_decode_indices(indices: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, height: int = 0, time: int = 0, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN, passphrase: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Decodes a Monero seed indices handle into its components.

```python
result: ots_result_t = ots_monero_seed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_fingerprint(seed)
fp1: str = ots_result_string(result)
result = ots_seed_indices(seed)
si: ots_handle_t = ots_result_handle(result)
result = ots_monero_seed_decode_indices(si)
seed2: ots_handle_t = ots_result_handle(result)
result = ots_seed_fingerprint(seed2)
fp2: str = ots_result_string(result)
assert fp1 == fp2  # The fingerprint should match the original seed
```

* **Parameters:**
  * **indices** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle containing the Monero seed indices to decode.
  * **height** (*int*) – The height at which the seed was created.
  * **time** (*int*) – The time at which the seed was created.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the seed is intended (Main, Test, or Stagenet).
  * **passphrase** (*str*) – An optional passphrase for additional security.
* **Returns:**
  ots_result_t containing the decoded seed information.

### ots.raw.ots_polyseed_create(random: bytes, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN, time: int = 0, passphrase: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Creates a new Polyseed with the specified parameters.

```python
from time import time as current_time
result: ots_result_t = ots_random_bytes(19)
random: bytes = ots_result_char_array(result)
result = ots_polyseed_create(random)
```

* **Parameters:**
  * **random** (*bytes*) – Random 19 bytes to use for seed creation.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the seed is intended (Main, Test, or Stagenet).
  * **time** (*int*) – The time at which the seed is created, defaults to 0 (current time).
  * **passphrase** (*str*) – Optional passphrase for seed offset (empty string for none).
* **Returns:**
  ots_result_t containing the created Polyseed.

### ots.raw.ots_polyseed_generate(network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN, time: int = 0, passphrase: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Generates a new Polyseed with the specified parameters.

```python
result: ots_result_t = ots_polyseed_generate()
seed: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the seed is intended (Main, Test, or Stagenet).
  * **time** (*int*) – The time at which the seed is generated, defaults to 0 (current time).
  * **passphrase** (*str*) – Optional passphrase for seed offset (empty string for none).
* **Returns:**
  ots_result_t containing the generated Polyseed.

### ots.raw.ots_polyseed_decode(phrase: str, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN, password: str = '', passphrase: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Decodes a Polyseed phrase into its components.

```python
result: ots_result_t = ots_polyseed_generate(passphrase='offset')
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_fingerprint(seed)
fp1: str = ots_result_string(result)
result = ots_seed_phrase_for_language_code(seed, 'en', 'my_password')
ws: ots_handle_t = ots_result_handle(result)
phrase: str = ots_wipeable_string_c_str(ws)
result = ots_polyseed_decode(phrase, password='my_password', passphrase='offset')
seed2: ots_handle_t = ots_result_handle(result)
result = ots_seed_fingerprint(seed2)
fp2: str = ots_result_string(result)
assert fp1 == fp2  # The fingerprint should match the original seed
```

* **Parameters:**
  * **phrase** (*str*) – The Polyseed phrase to decode.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the seed is intended (Main, Test, or Stagenet).
  * **password** (*str*) – Optional decryption password (empty string for none).
  * **passphrase** (*str*) – Optional passphrase for seed offset (empty string for none).
* **Returns:**
  ots_result_t containing the decoded seed information.

### ots.raw.ots_polyseed_decode_indices(indices: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN, password: str = '', passphrase: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Decodes a Polyseed indices handle into its components.

```python
result: ots_result_t = ots_polyseed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_fingerprint(seed)
fp1: str = ots_result_string(result)
result = ots_seed_indices(seed)
si: ots_handle_t = ots_result_handle(result)
result = ots_polyseed_decode_indices(si)
seed2: ots_handle_t = ots_result_handle(result)
result = ots_seed_fingerprint(seed2)
fp2: str = ots_result_string(result)
assert fp1 == fp2  # The fingerprint should match the original seed
```

* **Parameters:**
  * **indices** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle containing the Polyseed indices to decode.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the seed is intended (Main, Test, or Stagenet).
  * **password** (*str*) – Optional decryption password (empty string for none).
  * **passphrase** (*str*) – Optional passphrase for seed offset (empty string for none).
* **Returns:**
  ots_result_t containing the decoded seed information.

### ots.raw.ots_polyseed_decode_with_language(phrase: str, language: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN, password: str = '', passphrase: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Decodes a Polyseed phrase using a specific language.

```python
result: ots_result_t = ots_polyseed_generate()
seed: ots_handle_t = ots_result_handle(result)
result = ots_seed_phrase_for_language_code(seed, 'en')
ws: ots_handle_t = ots_result_handle(result)
phrase: str = ots_wipeable_string_c_str(ws)
result = ots_seed_language_from_code('en')
en: ots_handle_t = ots_result_handle(result)
result = ots_polyseed_decode_with_language(phrase, en)
seed2: ots_handle_t = ots_result_handle(result)
```

#### NOTE
This function is only needed if the Polyseed phrase could be more
then one language, should not really happen, IMO.

* **Parameters:**
  * **phrase** (*str*) – The Polyseed phrase to decode.
  * **language** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed language to use for decoding.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the seed is intended (Main, Test, or Stagenet).
  * **password** (*str*) – Optional decryption password (empty string for none).
  * **passphrase** (*str*) – Optional passphrase for seed offset (empty string for none).
* **Returns:**
  ots_result_t containing the decoded seed information.

### ots.raw.ots_polyseed_decode_with_language_code(phrase: str, language_code: str, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN, password: str = '', passphrase: str = '') → [ots_result_t](#ots.raw.ots_result_t)

Decodes a Polyseed phrase using a specific language code.

#### SEE ALSO
[`ots_polyseed_decode_with_language()`](#ots.raw.ots_polyseed_decode_with_language), only difference is that this function uses a language code instead of a language handle.

* **Parameters:**
  * **phrase** (*str*) – The Polyseed phrase to decode.
  * **language_code** (*str*) – The code of the seed language to use for decoding.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the seed is intended (Main, Test, or Stagenet).
  * **password** (*str*) – Optional decryption password (empty string for none).
  * **passphrase** (*str*) – Optional passphrase for seed offset (empty string for none).
* **Returns:**
  ots_result_t containing the decoded seed information.

### ots.raw.ots_polyseed_convert_to_monero_seed(polyseed: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Converts a Polyseed handle to a MoneroSeed handle.

```python
result: ots_result_t = ots_polyseed_generate()
polyseed: ots_handle_t = ots_result_handle(result)
result = ots_polyseed_convert_to_monero_seed(polyseed)
monero_seed: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **polyseed** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the Polyseed to convert.
* **Returns:**
  ots_result_t containing the converted Monero seed handle.

### ots.raw.ots_address_create(address: str) → [ots_result_t](#ots.raw.ots_result_t)

Creates an address from a given string.

```python
addr: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
result: ots_result_t = ots_address_create(addr)
address: ots_handle_t = ots_result_handle(result)
result = ots_address_base58_string(address)
assert ots_result_string(result) == addr
```

* **Parameters:**
  **address** (*str*) – The address string to create.
* **Returns:**
  ots_result_t containing the created address handle.

### ots.raw.ots_address_type(address: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the type of the given address handle.

```python
addr: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
result: ots_result_t = ots_address_create(addr)
address: ots_handle_t = ots_result_handle(result)
result = ots_address_type(address)
at: AddressType = ots_result_address_type(result)
assert at == AddressType.STANDARD
```

* **Parameters:**
  **address** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the address.
* **Returns:**
  ots_result_t containing the type of the address.

### ots.raw.ots_address_network(address: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the network of the given address handle.

```python
addr: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
result: ots_result_t = ots_address_create(addr)
address: ots_handle_t = ots_result_handle(result)
result = ots_address_network(address)
assert ots_result_network(result) == Network.MAIN
```

* **Parameters:**
  **address** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the address.
* **Returns:**
  ots_result_t containing the network of the address.

### ots.raw.ots_address_fingerprint(address: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the fingerprint of the given address handle.

```python
addr: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
result: ots_result_t = ots_address_create(addr)
address: ots_handle_t = ots_result_handle(result)
result = ots_address_fingerprint(address)
fingerprint: str = ots_result_string(result)
```

* **Parameters:**
  **address** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the address.
* **Returns:**
  ots_result_t containing the fingerprint of the address.

### ots.raw.ots_address_is_integrated(address: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Checks if the given address handle is an integrated address.

```python
addr: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
result: ots_result_t = ots_address_create(addr)
address: ots_handle_t = ots_result_handle(result)
result = ots_address_is_integrated(address)
assert ots_result_boolean(result) is False  # This address is not integrated

addr = '4Jmnw8aLmCzAA4a2rRjLmbT4uJadSZxzrW1nJh3NJYDr87hEdiFhaCcGyK87kb8u1i1DWtwKTUnoZ6uobbotLGqX5QeCPeUbcLb1iqv4E7'
result: ots_result_t = ots_address_create(addr)
address: ots_handle_t = ots_result_handle(result)
result = ots_address_is_integrated(address)
assert ots_result_boolean(result) is True  # This address is integrated
```

* **Parameters:**
  **address** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the address.
* **Returns:**
  ots_result_t indicating whether the address is integrated.

### ots.raw.ots_address_payment_id(address: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the payment ID of the given address handle.

```python
addr: str = '4Jmnw8aLmCzAA4a2rRjLmbT4uJadSZxzrW1nJh3NJYDr87hEdiFhaCcGyK87kb8u1i1DWtwKTUnoZ6uobbotLGqX5QeCPeUbcLb1iqv4E7'
result: ots_result_t = ots_address_create(addr)
address: ots_handle_t = ots_result_handle(result)
result = ots_address_payment_id(address)
assert ots_result_string(result) == '59f3832901727c06'  # payment ID of the address
```

* **Parameters:**
  **address** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the address.
* **Returns:**
  ots_result_t containing the payment ID of the address.

### ots.raw.ots_address_from_integrated(address: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Extracts the base address from an integrated address handle.

```python
addr: str = '4Jmnw8aLmCzAA4a2rRjLmbT4uJadSZxzrW1nJh3NJYDr87hEdiFhaCcGyK87kb8u1i1DWtwKTUnoZ6uobbotLGqX5QeCPeUbcLb1iqv4E7'
result: ots_result_t = ots_address_create(addr)
address: ots_handle_t = ots_result_handle(result)
result = ots_address_from_integrated(address)
base_address: ots_handle_t = ots_result_handle(result)
assert ots_address_base58_string(base_address) == '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
```

* **Parameters:**
  **address** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the integrated address.
* **Returns:**
  ots_result_t containing the base address.

### ots.raw.ots_address_length(address: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the length of the given address handle.

```python
addr: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
result: ots_result_t = ots_address_create(addr)
address: ots_handle_t = ots_result_handle(result)
result = ots_address_length(address)
assert ots_result_number(result) == 95  # Length of the address in base58
```

* **Parameters:**
  **address** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the address.
* **Returns:**
  ots_result_t containing the length of the address.

### ots.raw.ots_address_base58_string(address_handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the base58 string representation of the given address handle.

```python
addr: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
result: ots_result_t = ots_address_create(addr)
address: ots_handle_t = ots_result_handle(result)
result = ots_address_base58_string(address)
assert ots_result_string(result) == addr  # The base58 string should match the original address
```

* **Parameters:**
  **address_handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the address.
* **Returns:**
  ots_result_t containing the base58 string representation of the address.

### ots.raw.ots_address_equal(address1: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, address2: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Compares two address handles for equality.

```python
addr1: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
addr2: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
result1: ots_result_t = ots_address_create(addr1)
address1: ots_handle_t = ots_result_handle(result1)
result2: ots_result_t = ots_address_create(addr2)
address2: ots_handle_t = ots_result_handle(result2)
result = ots_address_equal(address1, address2)
assert ots_result_boolean(result) is True  # The addresses should be equal
```

* **Parameters:**
  * **address1** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The first address handle.
  * **address2** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The second address handle.
* **Returns:**
  ots_result_t indicating whether the addresses are equal.

### ots.raw.ots_address_equal_string(address_handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, address_string: str) → [ots_result_t](#ots.raw.ots_result_t)

Compares an address handle with a string representation of an address for equality.

```python
addr1: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
addr2: str = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
result1: ots_result_t = ots_address_create(addr1)
address1: ots_handle_t = ots_result_handle(result1)
result = ots_address_equal(address1, addr2)
assert ots_result_boolean(result) is True  # The addresses should be equal
```

* **Parameters:**
  * **address_handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the address.
  * **address_string** (*str*) – The string representation of the address.
* **Returns:**
  ots_result_t indicating whether the address handle matches the string.

### ots.raw.ots_address_string_valid(address: str, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN) → [ots_result_t](#ots.raw.ots_result_t)

Checks if the given address string is valid for the specified network.

```python
result: ots_result_t = ots_address_string_valid('43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK', Network.MAIN)
assert ots_result_boolean(result) is True  # The address string should be valid
```

* **Parameters:**
  * **address** (*str*) – The address string to validate.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which to validate the address (Main, Test, or Stagenet).
* **Returns:**
  ots_result_t indicating whether the address string is valid.

### ots.raw.ots_address_string_network(address: str) → [ots_result_t](#ots.raw.ots_result_t)

Returns the network of the given address string.

```python
result: ots_result_t = ots_address_string_network('43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK')
assert ots_result_network(result) == Network.MAIN  # The address string is on Main network
```

* **Parameters:**
  **address** (*str*) – The address string to check.
* **Returns:**
  ots_result_t containing the network of the address.

### ots.raw.ots_address_string_type(address: str) → [ots_result_t](#ots.raw.ots_result_t)

Returns the type of the given address string.

```python
result: ots_result_t = ots_address_string_type('43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK')
assert ots_result_address_type(result) == AddressType.STANDARD  # The address string is of type STANDARD
```

* **Parameters:**
  **address** (*str*) – The address string to check.
* **Returns:**
  ots_result_t containing the type of the address.

### ots.raw.ots_address_string_fingerprint(address: str) → [ots_result_t](#ots.raw.ots_result_t)

Returns the fingerprint of the given address string.

```python
result: ots_result_t = ots_address_string_fingerprint('43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK')
assert ots_result_string(result) == '9AE0BD'
```

* **Parameters:**
  **address** (*str*) – The address string to check.
* **Returns:**
  ots_result_t containing the fingerprint of the address.

### ots.raw.ots_address_string_is_integrated(address: str) → [ots_result_t](#ots.raw.ots_result_t)

Checks if the given address string is an integrated address.

```python
result: ots_result_t = ots_address_string_is_integrated('4Jmnw8aLmCzAA4a2rRjLmbT4uJadSZxzrW1nJh3NJYDr87hEdiFhaCcGyK87kb8u1i1DWtwKTUnoZ6uobbotLGqX5QeCPeUbcLb1iqv4E7')
assert ots_result_boolean(result) is True  # The address string is integrated
```

* **Parameters:**
  **address** (*str*) – The address string to check.
* **Returns:**
  ots_result_t indicating whether the address string is integrated.

### ots.raw.ots_address_string_payment_id(address: str) → [ots_result_t](#ots.raw.ots_result_t)

Returns the payment ID of the given address string.

```python
result: ots_result_t = ots_address_string_payment_id('4Jmnw8aLmCzAA4a2rRjLmbT4uJadSZxzrW1nJh3NJYDr87hEdiFhaCcGyK87kb8u1i1DWtwKTUnoZ6uobbotLGqX5QeCPeUbcLb1iqv4E7')
assert ots_result_string(result) == '59f3832901727c06'  # The payment ID of the address string
```

* **Parameters:**
  **address** (*str*) – The address string to check.
* **Returns:**
  ots_result_t containing the payment ID of the address.

### ots.raw.ots_address_string_integrated(address: str) → [ots_result_t](#ots.raw.ots_result_t)

Extracts the base address from an integrated address string.

```python
result: ots_result_t = ots_address_string_integrated('4Jmnw8aLmCzAA4a2rRjLmbT4uJadSZxzrW1nJh3NJYDr87hEdiFhaCcGyK87kb8u1i1DWtwKTUnoZ6uobbotLGqX5QeCPeUbcLb1iqv4E7')
base_address: ots_handle_t = ots_result_handle(result)
assert ots_address_base58_string(base_address) == '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
```

* **Parameters:**
  **address** (*str*) – The integrated address string to check.
* **Returns:**
  ots_result_t containing the base address.

### ots.raw.ots_wallet_create(key: bytes, height: int = 0, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN) → [ots_result_t](#ots.raw.ots_result_t)

Creates a new wallet with the specified key, height, and network.

```python
result: ots_result_t = ots_random_32()
key: bytes = ots_result_char_array(result)
result = ots_wallet_create(key, 0, Network.MAIN)
wallet: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  * **key** (*bytes*) – The key to use for the wallet.
  * **height** (*int*) – The height at which the wallet is created.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which the wallet is intended (Main, Test, or Stagenet).
* **Returns:**
  ots_result_t containing the created wallet handle.

### ots.raw.ots_wallet_height(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the height of the given wallet handle.

```python
result: ots_result_t = ots_wallet_height(wallet)
height: int = ots_result_number(result)
```

* **Parameters:**
  **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
* **Returns:**
  ots_result_t containing the height of the wallet.

### ots.raw.ots_wallet_address(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the primary address of the given wallet handle.

```python
result: ots_result_t = ots_wallet_address(wallet)
address: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
* **Returns:**
  ots_result_t containing the primary address of the wallet.

### ots.raw.ots_wallet_subaddress(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, account: int, index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns a subaddress from the given wallet handle based on account and index.

```python
result: ots_result_t = ots_wallet_subaddress(wallet, 0, 0)
standard_address: ots_handle_t = ots_result_handle(result)
result = ots_wallet_subaddress(wallet, 0, 1)
subaddress_account_0_index_1: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **account** (*int*) – The account number for the subaddress.
  * **index** (*int*) – The index of the subaddress within the account.
* **Returns:**
  ots_result_t containing the requested subaddress.

### ots.raw.ots_wallet_accounts(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, max: int, offset: int = 0) → [ots_result_t](#ots.raw.ots_result_t)

Returns a list of accounts from the given wallet handle.

```python
result: ots_result_t = ots_wallet_accounts(wallet, 10, 0)
accounts: list[ots_handle_t] = ots_result_handle_array(result)
assert len(accounts) == 10
result = ots_address_type(accounts[0])
assert ots_result_address_type(result) == AddressType.STANDARD  # The first account should be a standard address
result = ots_address_type(accounts[1])
assert ots_result_address_type(result) == AddressType.SUBADDRESS  # The second account should be a subaddress
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **max** (*int*) – The maximum number of accounts to return.
  * **offset** (*int*) – The offset from which to start returning accounts.
* **Returns:**
  ots_result_t containing the requested accounts.

### ots.raw.ots_wallet_subaddresses(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, account: int, max: int, offset: int = 0) → [ots_result_t](#ots.raw.ots_result_t)

Returns a list of subaddresses from the given wallet handle based on account.

```python
result: ots_result_t = ots_wallet_subaddresses(wallet, 0, 10, 0)
subaddresses: list[ots_handle_t] = ots_result_handle_array(result)
assert len(subaddresses) == 10
result = ots_address_type(subaddresses[0])
assert ots_result_address_type(result) == AddressType.STANDARD  # The first subaddress should be a standard address in the first account (0, 0)
result = ots_address_type(subaddresses[1])
assert ots_result_address_type(result) == AddressType.SUBADDRESS  # The second subaddress should be a subaddress in the first account (0, 1)
result = ots_wallet_subaddresses(wallet, 1, 5, 0)
subaddresses = ots_result_handle_array(result)
assert len(subaddresses) == 5
result = ots_address_type(subaddresses[0])
assert ots_result_address_type(result) == AddressType.SUBADDRESS # The first subaddress should be a subaddress in the second account (1, 0)
result = ots_address_type(subaddresses[1])
assert ots_result_address_type(result) == AddressType.SUBADDRESS  # The second subaddress should be a subaddress in the second account (1, 1)
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **account** (*int*) – The account number for which to return subaddresses.
  * **max** (*int*) – The maximum number of subaddresses to return.
  * **offset** (*int*) – The offset from which to start returning subaddresses.
* **Returns:**
  ots_result_t containing the requested subaddresses.

### ots.raw.ots_wallet_has_address(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, address: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, max_account_depth: int = 0, max_index_depth: int = 0) → [ots_result_t](#ots.raw.ots_result_t)

Checks if the given wallet handle contains the specified address handle.

```python
# will search in 1000 addresses, 100 indexes per account, over 10 accounts
result: ots_result_t = ots_wallet_has_address(
    wallet_handle,
    searched_address_handle,
    10, 100
)
found: bool = ots_result_boolean(result)
# if the address is e.g. in second account at 200th index, it will return False
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **address** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the address to check.
  * **max_account_depth** – The maximum account depth to consider. Default is 0, which uses the value returned by ots_get_max_account_depth(0).
  * **max_index_depth** – The maximum index depth to consider. Default is 0, which uses the value returned by ots_get_max_index_depth(0).
* **Returns:**
  ots_result_t indicating whether the address is present in the wallet.

### ots.raw.ots_wallet_has_address_string(wallet_handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, address: str, max_account_depth: int = 0, max_index_depth: int = 0) → [ots_result_t](#ots.raw.ots_result_t)

Checks if the given wallet handle contains the specified address string.

```python
# will search in 1000 addresses, 100 indexes per account, over 10 accounts
result: ots_result_t = ots_wallet_has_address_string(wallet_handle, '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK', 10, 100)
found: bool = ots_result_boolean(result)
```

* **Parameters:**
  * **wallet_handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **address** (*str*) – The string representation of the address to check.
  * **max_account_depth** (*int*) – The maximum account depth to consider. Default is 0, which uses the value returned by ots_get_max_account_depth(0).
  * **max_index_depth** (*int*) – The maximum index depth to consider. Default is 0, which uses the value returned by ots_get_max_index_depth(0).
* **Returns:**
  ots_result_t indicating whether the address is present in the wallet.

### ots.raw.ots_wallet_address_index(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, address: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, max_account_depth: int = 0, max_index_depth: int = 0) → [ots_result_t](#ots.raw.ots_result_t)

Returns the index of the specified address in the wallet.

```python
# will search in 1000 addresses, 100 indexes per account, over 10 accounts
result: ots_result_t = ots_wallet_address_index(wallet_handle, searched_address_handle, 10, 100)
if ots_result_is_address_index(result):  # The address is found
    index: tuple[int, int] = (ots_result_address_index_account(result), ots_result_address_index_index(result))
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **address** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the address to find.
  * **max_account_depth** (*int*) – The maximum account depth to consider. Default is 0, which uses the value returned by ots_get_max_account_depth(0).
  * **max_index_depth** (*int*) – The maximum index depth to consider. Default is 0, which uses the value returned by ots_get_max_index_depth(0).
* **Returns:**
  ots_result_t containing the index of the address in the wallet.

### ots.raw.ots_wallet_address_string_index(wallet_handle: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, address: str, max_account_depth: int = 0, max_index_depth: int = 0) → [ots_result_t](#ots.raw.ots_result_t)

Returns the index of the specified address string in the wallet.

```python
# will search in 1000 addresses, 100 indexes per account, over 10 accounts
result: ots_result_t = ots_wallet_address_string_index(wallet_handle, '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK', 10, 100)
if ots_result_is_address_index(result):  # The address is found
    index: tuple[int, int] = (ots_result_address_index_account(result), ots_result_address_index_index(result))
```

* **Parameters:**
  * **wallet_handle** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **address** (*str*) – The string representation of the address to find.
  * **max_account_depth** (*int*) – The maximum account depth to consider.
  * **max_index_depth** (*int*) – The maximum index depth to consider.
* **Returns:**
  ots_result_t containing the index of the address in the wallet.

### ots.raw.ots_wallet_secret_view_key(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the secret view key of the given wallet handle.

```python
result: ots_result_t = ots_wallet_secret_view_key(wallet_handle)
ws_handle: ots_handle_t = ots_result_handle(result)
print(ots_wipeable_string_c_string(ws_handle))  # Prints the secret view key of the wallet
```

* **Parameters:**
  **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
* **Returns:**
  ots_result_t containing the secret view key of the wallet.

### ots.raw.ots_wallet_public_view_key(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the public view key of the given wallet handle.

```python
result: ots_result_t = ots_wallet_public_view_key(wallet_handle)
ws_handle: ots_handle_t = ots_result_handle(result)
print(ots_wipeable_string_c_string(ws_handle))  # Prints the public view key of the wallet
```

* **Parameters:**
  **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
* **Returns:**
  ots_result_t containing the public view key of the wallet.

### ots.raw.ots_wallet_secret_spend_key(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the secret spend key of the given wallet handle.

```python
result: ots_result_t = ots_wallet_secret_spend_key(wallet_handle)
ws_handle: ots_handle_t = ots_result_handle(result)
print(ots_wipeable_string_c_string(ws_handle))  # Prints the secret spend key of the wallet
```

* **Parameters:**
  **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
* **Returns:**
  ots_result_t containing the secret spend key of the wallet.

### ots.raw.ots_wallet_public_spend_key(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the public spend key of the given wallet handle.

```python
result: ots_result_t = ots_wallet_public_spend_key(wallet_handle)
ws_handle: ots_handle_t = ots_result_handle(result)
print(ots_wipeable_string_c_string(ws_handle))  # Prints the public spend key of the wallet
```

* **Parameters:**
  **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
* **Returns:**
  ots_result_t containing the public spend key of the wallet.

### ots.raw.ots_wallet_import_outputs(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, outputs: bytes | str) → [ots_result_t](#ots.raw.ots_result_t)

Imports outputs into the given wallet handle.

```python
result: ots_result_t = ots_wallet_import_outputs(wallet_handle, output_data)
if ots_is_result_success(result):  # export successful
    imported: int = ots_result_number(result)  # Number of outputs imported
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **outputs** (*bytes* *|* *str*) – A bytes or string containing the outputs to import.
* **Returns:**
  ots_result_t indicating the result of the import operation.

### ots.raw.ots_wallet_export_key_images(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Exports key images from the given wallet handle.

```python
result: ots_result_t = ots_wallet_export_key_images(wallet_handle)
if ots_is_result(result):  # export successful
    key_images: bytes = ots_result_char_array(result)  # The exported key images
```

* **Parameters:**
  **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
* **Returns:**
  ots_result_t containing the exported key images.

### ots.raw.ots_wallet_describe_tx(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, unsigned_tx: bytes) → [ots_result_t](#ots.raw.ots_result_t)

Describes a transaction for the given wallet handle.

```python
result: ots_result_t = ots_wallet_describe_tx(wallet_handle, unsigned_tx)
if ots_is_result(result):  # description parsed successfully
    description: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **unsigned_tx** (*bytes*) – A bytes object containing the unsigned transaction to describe.
* **Returns:**
  ots_result_t containing the description of the transaction.

### ots.raw.ots_wallet_check_tx(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, unsigned_tx: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Checks a transaction for the given wallet handle.

```python
result: ots_result_t = ots_wallet_check_tx(wallet_handle, unsigned_tx_description_handle)
tx_warnings: list[ots_handle_t] = ots_result_handle_array(result)  # Warnings from the transaction check
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **unsigned_tx** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the unsigned transaction to check.
* **Returns:**
  ots_result_t indicating the result of the check operation.

### ots.raw.ots_wallet_check_tx_string(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, unsigned_tx: bytes) → [ots_result_t](#ots.raw.ots_result_t)

Checks a transaction for the given wallet handle using a string representation of the unsigned transaction.

```python
result: ots_result_t = ots_wallet_check_tx_string(wallet_handle, unsigned_tx_data)
if ots_is_result(result):  # check successful
    tx_warnings: list[ots_handle_t] = ots_result_handle_array(result)  # Warnings from the transaction check
else:  # invalid unsigned_tx
    print(ots_error_message(result))  # Prints the error message if the unsigned transaction is invalid
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **unsigned_tx** (*bytes*) – A bytes object containing the unsigned transaction to check.
* **Returns:**
  ots_result_t indicating the result of the check operation.

### ots.raw.ots_wallet_sign_transaction(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, unsigned_tx: bytes) → [ots_result_t](#ots.raw.ots_result_t)

Signs a transaction for the given wallet handle.

```python
result: ots_result_t = ots_wallet_sign_transaction(wallet_handle, unsigned_tx)
if ots_is_result(result):  # signing successful
    signed_tx: bytes = ots_result_char_array(result)  # The signed transaction
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **unsigned_tx** (*bytes*) – A bytes object containing the unsigned transaction to sign.
* **Returns:**
  ots_result_t containing the signed transaction.

### ots.raw.ots_wallet_sign_data(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, data: bytes | str) → [ots_result_t](#ots.raw.ots_result_t)

Signs data with the given wallet handle.

```python
data: str = "Hello, World!"
result: ots_result_t = ots_wallet_sign_data(wallet_handle, data)
signature: str = ots_result_string(result)  # The signature of the data
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **data** (*bytes* *|* *str*) – The data to sign.
* **Returns:**
  ots_result_t containing the signature of the data.

### ots.raw.ots_wallet_sign_data_with_index(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, data: bytes | str, account: int, subaddr: int) → [ots_result_t](#ots.raw.ots_result_t)

Signs data with the specified account and subaddress in the given wallet handle.

```python
data: str = "Hello, World!"
result: ots_result_t = ots_wallet_sign_data_with_index(wallet_handle, data, 0, 0)
signature: str = ots_result_string(result)  # The signature of the data
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **data** (*bytes* *|* *str*) – The data to sign.
  * **account** (*int*) – The account number to use for signing.
  * **subaddr** (*int*) – The subaddress index to use for signing.
* **Returns:**
  ots_result_t containing the signature of the data.

### ots.raw.ots_wallet_sign_data_with_address(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, data: bytes | str, address: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Signs data with the specified address in the given wallet handle.

```python
data: str = "Hello, World!"
result: ots_result_t = ots_wallet_sign_data_with_address(wallet_handle, data, address_handle)
signature: str = ots_result_string(result)  # The signature of the data
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **data** (*bytes* *|* *str*) – The data to sign.
  * **address** – The handle of the address to use for signing.
* **Returns:**
  ots_result_t containing the signature of the data.

### ots.raw.ots_wallet_sign_data_with_address_string(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, data: bytes | str, address: str) → [ots_result_t](#ots.raw.ots_result_t)

Signs data with the specified address string in the given wallet handle.

```python
data: str = "Hello, World!"
result: ots_result_t = ots_wallet_sign_data_with_address_string(wallet_handle, data, '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK')
signature: str = ots_result_string(result)  # The signature of the data
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **data** (*bytes* *|* *str*) – The data to sign.
  * **address** (*str*) – The string representation of the address to use for signing.
* **Returns:**
  ots_result_t containing the signature of the data.

### ots.raw.ots_wallet_verify_data(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, data: bytes | str, signature: str, legacy_fallback: bool = False) → [ots_result_t](#ots.raw.ots_result_t)

Verifies the signature of data with the standard address of the given wallet handle.

```python
data: str = "Hello, World!"
result: ots_result_t = ots_wallet_verify_data(wallet_handle, data, signature)
assert ots_result_boolean(result)  # True if the signature is valid, False otherwise
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **data** (*bytes* *|* *str*) – The data whose signature is to be verified.
  * **signature** (*str*) – The signature to verify.
  * **legacy_fallback** (*bool*) – Whether to use legacy fallback verification.
* **Returns:**
  ots_result_t indicating the result of the verification.

### ots.raw.ots_wallet_verify_data_with_index(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, data: bytes | str, account: int, subaddr: int, signature: str, legacy_fallback: bool = False) → [ots_result_t](#ots.raw.ots_result_t)

Verifies the signature of data with the specified account and subaddress in the given wallet handle.

```python
data: str = "Hello, World!"
result: ots_result_t = ots_wallet_verify_data_with_index(wallet_handle, data, 0, 0, signature)
assert ots_result_boolean(result)  # True if the signature is valid, False otherwise
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **data** (*bytes* *|* *str*) – The data whose signature is to be verified.
  * **account** (*int*) – The account number to use for verification.
  * **subaddr** (*int*) – The subaddress index to use for verification.
  * **signature** (*str*) – The signature to verify.
  * **legacy_fallback** (*bool*) – Whether to use legacy fallback verification.
* **Returns:**
  ots_result_t indicating the result of the verification.

### ots.raw.ots_wallet_verify_data_with_address(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, data: bytes | str, address: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, signature: str, legacy_fallback: bool = False) → [ots_result_t](#ots.raw.ots_result_t)

Verifies the signature of data with the specified address in the given wallet handle.

```python
data: str = "Hello, World!"
result: ots_result_t = ots_wallet_verify_data_with_address(wallet_handle, data, address_handle, signature)
assert ots_result_boolean(result)  # True if the signature is valid, False otherwise
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **data** (*bytes* *|* *str*) – The data whose signature is to be verified.
  * **address** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the address to use for verification.
  * **signature** (*str*) – The signature to verify.
  * **legacy_fallback** (*bool*) – Whether to use legacy fallback verification.
* **Returns:**
  ots_result_t indicating the result of the verification.

### ots.raw.ots_wallet_verify_data_with_address_string(wallet: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, data: bytes | str, address: str, signature: str, legacy_fallback: bool = False) → [ots_result_t](#ots.raw.ots_result_t)

Verifies the signature of data with the specified address string in the given wallet handle.

```python
data: str = "Hello, World!"
result: ots_result_t = ots_wallet_verify_data_with_address_string(wallet_handle, data, '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK', signature)
assert ots_result_boolean(result)  # True if the signature is valid, False otherwise
```

* **Parameters:**
  * **wallet** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the wallet.
  * **data** (*bytes* *|* *str*) – The data whose signature is to be verified.
  * **address** (*str*) – The string representation of the address to use for verification.
  * **signature** (*str*) – The signature to verify.
  * **legacy_fallback** (*bool*) – Whether to use legacy fallback verification.
* **Returns:**
  ots_result_t indicating the result of the verification.

### ots.raw.ots_tx_description(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_tx_description_t](#ots.raw.ots_tx_description_t)

Returns the transaction description for the given transaction handle.

```python
tx_description: ots_tx_description_t = ots_tx_description(tx_description_handlen)
```

* **Parameters:**
  **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
* **Returns:**
  ots_tx_description_t containing the transaction description.

### ots.raw.ots_tx_description_tx_set(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → bytes

Returns the transaction set for the given transaction description handle.

```python
tx_set: bytes = ots_tx_description_tx_set(tx_description_handle)
```

* **Parameters:**
  **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
* **Returns:**
  A string representing the transaction set.

### ots.raw.ots_tx_description_tx_set_size(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → int

Returns the size of the transaction set for the given transaction description handle.

```python
tx_set_size: int = ots_tx_description_tx_set_size(tx_description_handle)
```

* **Parameters:**
  **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
* **Returns:**
  An integer representing the size of the transaction set.

### ots.raw.ots_tx_description_amount_in(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → int

Returns the total amount in for the given transaction description handle.

```python
total_amount_in: int = ots_tx_description_amount_in(tx_description_handle)
```

* **Parameters:**
  **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
* **Returns:**
  An integer representing the total amount in.

### ots.raw.ots_tx_description_amount_out(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → int

Returns the total amount out for the given transaction description handle.

```python
total_amount_out: int = ots_tx_description_amount_out(tx_description_handle)
```

* **Parameters:**
  **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
* **Returns:**
  An integer representing the total amount out.

### ots.raw.ots_tx_description_flows_count(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → int

Returns the number of flows in the given transaction description handle.

```python
flows_count: int = ots_tx_description_flows_count(tx_description_handle)
```

* **Parameters:**
  **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
* **Returns:**
  An integer representing the number of flows.

### ots.raw.ots_tx_description_flow_address(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → str

Returns the address of a flow in the given transaction description handle.

```python
address: str = ots_tx_description_flow_address(tx_description_handle, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the flow to retrieve the address for.
* **Returns:**
  A string representing the address of the flow.

### ots.raw.ots_tx_description_flow_amount(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → int

Returns the amount of a flow in the given transaction description handle.

```python
amount: int = ots_tx_description_flow_amount(tx_description_handle, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the flow to retrieve the amount for.
* **Returns:**
  An integer representing the amount of the flow.

### ots.raw.ots_tx_description_has_change(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → bool

Checks if the given transaction description handle has change.

```python
has_change: bool = ots_tx_description_has_change(tx_description_handle)
```

* **Parameters:**
  **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
* **Returns:**
  True if there is change, False otherwise.

### ots.raw.ots_tx_description_change_address(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → str | None

Returns the change address for the given transaction description handle.

```python
change_address: str | None = ots_tx_description_change_address(tx_description_handle)
```

* **Parameters:**
  **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
* **Returns:**
  A string representing the change address, or None if there is no change address.

### ots.raw.ots_tx_description_change_amount(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → int

Returns the change amount for the given transaction description handle.

```python
if ots_tx_description_has_change(tx_description_handle):
    change_amount: int = ots_tx_description_change_amount(tx_description_handle)
```

* **Parameters:**
  **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
* **Returns:**
  An integer representing the change amount.

### ots.raw.ots_tx_description_fee(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → int

Returns the fee for the given transaction description handle.

```python
fee: int = ots_tx_description_fee(tx_description_handle)
```

* **Parameters:**
  **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
* **Returns:**
  An integer representing the fee.

### ots.raw.ots_tx_description_transfers_count(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → int

Returns the number of transfers in the given transaction description handle.

```python
transfers_count: int = ots_tx_description_transfers_count(tx_description_handle)
```

* **Parameters:**
  **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
* **Returns:**
  An integer representing the number of transfers.

### ots.raw.ots_tx_description_transfer_amount_in(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → int

Returns the amount in for a specific transfer in the given transaction description handle.

```python
amounts_in: list[int] = [
    ots_tx_description_transfer_amount_in(tx_description_handle, i)
    for i in range(ots_tx_description_transfers_count(tx_description_handle))
]
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the amount in for.
* **Returns:**
  An integer representing the amount in for the transfer.

### ots.raw.ots_tx_description_transfer_amount_out(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → int

Returns the amount out for a specific transfer in the given transaction description handle.

```python
amounts_out: list[int] = [
    ots_tx_description_transfer_amount_out(tx_description_handle, i)
    for i in range(ots_tx_description_transfers_count(tx_description_handle))
]
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the amount out for.
* **Returns:**
  An integer representing the amount out for the transfer.

### ots.raw.ots_tx_description_transfer_ring_size(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → int

Returns the ring size for a specific transfer in the given transaction description handle.

```python
assert ots_tx_description_transfers_count(tx_description_handle) > 0, "There should be at least one transfer"
ring_size: int = ots_tx_description_transfer_ring_size(tx_description_handle, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the ring size for.
* **Returns:**
  An integer representing the ring size for the transfer.

### ots.raw.ots_tx_description_transfer_unlock_time(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → int

Returns the unlock time for a specific transfer in the given transaction description handle.

#### ATTENTION
Monero removed the unlocktime, so this function will probably be removed in the future.

```python
assert ots_tx_description_transfers_count(tx_description_handle) > 0, "There should be at least one transfer"
unlock_time: int = ots_tx_description_transfer_unlock_time(tx_description_handle, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the unlock time for.
* **Returns:**
  An integer representing the unlock time for the transfer.

### ots.raw.ots_tx_description_transfer_flows_count(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → int

Returns the number of flows for a specific transfer in the given transaction description handle.

```python
assert ots_tx_description_transfers_count(tx_description_handle) > 0, "There should be at least one transfer"
flows_count: int = ots_tx_description_transfer_flows_count(tx_description_handle, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the number of flows for.
* **Returns:**
  An integer representing the number of flows for the transfer.

### ots.raw.ots_tx_description_transfer_flow_address(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int, flow_index: int) → str

Returns the address of a specific flow in a transfer within the given transaction description handle.

```python
assert ots_tx_description_transfers_count(tx_description_handle) > 0, "There should be at least one transfer"
assert ots_tx_description_transfer_flows_count(tx_description_handle, 0) > 0, "There should be at least one flow in the transfer"
flow_address: str = ots_tx_description_transfer_flow_address(tx_description_handle, 0, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the flow address for.
  * **flow_index** (*int*) – The index of the flow within the transfer.
* **Returns:**
  A string representing the address of the flow.

### ots.raw.ots_tx_description_transfer_flow_amount(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int, flow_index: int) → int

Returns the amount of a specific flow in a transfer within the given transaction description handle.

```python
assert ots_tx_description_transfers_count(tx_description_handle) > 0, "There should be at least one transfer"
assert ots_tx_description_transfer_flows_count(tx_description_handle, 0) > 0, "There should be at least one flow in the transfer"
flow_amount: int = ots_tx_description_transfer_flow_amount(tx_description_handle, 0, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the flow amount for.
  * **flow_index** (*int*) – The index of the flow within the transfer.
* **Returns:**
  An integer representing the amount of the flow.

### ots.raw.ots_tx_description_transfer_has_change(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → bool

Checks if a specific transfer in the given transaction description handle has change.

```python
assert ots_tx_description_transfers_count(tx_description_handle) > 0, "There should be at least one transfer"
has_change: bool = ots_tx_description_transfer_has_change(tx_description_handle, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to check for change.
* **Returns:**
  A boolean indicating whether the transfer has change.

### ots.raw.ots_tx_description_transfer_change_address(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → str

Returns the change address for a specific transfer in the given transaction description handle.

```python
assert ots_tx_description_transfers_count(tx_description_handle) > 0, "There should be at least one transfer"
change_address: str = ots_tx_description_transfer_change_address(tx_description_handle, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the change address for.
* **Returns:**
  A string representing the change address.

### ots.raw.ots_tx_description_transfer_change_amount(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → int

Returns the change amount for a specific transfer in the given transaction description handle.

```python
assert ots_tx_description_transfers_count(tx_description_handle) > 0, "There should be at least one transfer"
assert ots_tx_description_transfer_has_change(tx_description_handle, 0), "The transfer should have change"
change_amount: int = ots_tx_description_transfer_change_amount(tx_description_handle, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the change amount for.
* **Returns:**
  An integer representing the change amount.

### ots.raw.ots_tx_description_transfer_fee(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → int

Returns the fee for a specific transfer in the given transaction description handle.

```python
assert ots_tx_description_transfers_count(tx_description_handle) > 0, "There should be at least one transfer"
fee: int = ots_tx_description_transfer_fee(tx_description_handle, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the fee for.
* **Returns:**
  An integer representing the fee for the transfer.

### ots.raw.ots_tx_description_transfer_payment_id(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → str | None

Returns the payment ID for a specific transfer in the given transaction description handle.

* **Parameters:**
  * **tx_description** – The handle of the transaction description.
  * **index** – The index of the transfer to retrieve the payment ID for.
* **Returns:**
  An integer representing the payment ID for the transfer.

### ots.raw.ots_tx_description_transfer_dummy_outputs(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → int

Returns the number of dummy outputs for a specific transfer in the given transaction description handle.

* **Parameters:**
  * **tx_description** – The handle of the transaction description.
  * **index** – The index of the transfer to retrieve the number of dummy outputs for.
* **Returns:**
  An integer representing the number of dummy outputs for the transfer.

### ots.raw.ots_tx_description_transfer_extra(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → bytes

Returns the extra data for a specific transfer in the given transaction description handle.

```python
assert ots_tx_description_transfers_count(tx_description_handle) > 0, "There should be at least one transfer"
extra_data: bytes = ots_tx_description_transfer_extra(tx_description_handle, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the extra data for.
* **Returns:**
  A string representing the extra data for the transfer.

### ots.raw.ots_tx_description_transfer_extra_size(tx_description: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, index: int) → int

Returns the size of the extra data for a specific transfer in the given transaction description handle.

```python
assert ots_tx_description_transfers_count(tx_description_handle) > 0, "There should be at least one transfer"
extra_data_size: int = ots_tx_description_transfer_extra_size(tx_description_handle, 0)
```

* **Parameters:**
  * **tx_description** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the transaction description.
  * **index** (*int*) – The index of the transfer to retrieve the extra data size for.
* **Returns:**
  An integer representing the size of the extra data for the transfer.

### ots.raw.ots_seed_jar_add_seed(seed: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, name: str) → [ots_result_t](#ots.raw.ots_result_t)

Adds a seed to the seed jar with the specified name.

```python
seed_reference: ots_handle_t = ots_seed_jar_add_seed(seed, "My Seed")
```

#### ATTENTION
In the code example above, the seed (ots_handle_t\*) has the ownership,
which gets transferred to the seed jar. The seed jar sets the original
seed handle ots_handle_t->reference = true; but the CFFI doesn’t reflect
this. The returned seed_reference, is exactly the same as the original seed,
marked as reference. So it is a good idea (if you want to keep the seed
handle) to make simply the following:

```python
seed = ots_seed_jar_add_seed(seed, "My Seed")
```

* **Parameters:**
  * **seed** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The seed handle to add.
  * **name** (*str*) – The name to associate with the seed.
* **Returns:**
  ots_result_t with a reference to the added seed.

### ots.raw.ots_seed_jar_remove_seed(seed: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Removes a seed from the seed jar.

```python
seed = ots_seed_jar_add_seed(seed, "My Seed")
if ots_seed_jar_remove_seed(seed):  #  The seed is wiped and freed
    del seed  # Make sure to not use the seed handle anymore
```

#### ATTENTION
Do not use the original seed handle to remove it from the seed jar,
and do not use any seed handle after removing it from the seed jar.

```python
seed_reference: ots_handle_t = ots_seed_jar_add_seed(seed, "My Seed")
# Do not use `seed` anymore anywhere from this point on!
#ots_seed_jar_remove_seed(seed)  # DO NOT use `seed` here, use only
                                # `seed_reference`
ots_seed_jar_remove_seed(seed_reference)
# Do not use `seed_reference` anymore anywhere from this point on!
```

* **Parameters:**
  **seed** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The seed handle to remove.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_purge_seed_for_index(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Purges a seed from the seed jar based on its index.

```python
result: ots_result_t = ots_seed_jar_purge_seed_for_index(0)  # Purges the seed at index 0
assert ots_result_boolean(result), "Failed to purge seed at index 0"
```

* **Parameters:**
  **index** (*int*) – The index of the seed to purge.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_purge_seed_for_name(name: str) → [ots_result_t](#ots.raw.ots_result_t)

Purges a seed from the seed jar based on its name.

```python
result: ots_result_t = ots_seed_jar_purge_seed_for_name("My Seed")  # Purges the seed with name "My Seed"
assert ots_result_boolean(result), "Failed to purge seed with name 'My Seed'"
```

* **Parameters:**
  **name** (*str*) – The name of the seed to purge.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_purge_seed_for_fingerprint(fingerprint: str) → [ots_result_t](#ots.raw.ots_result_t)

Purges a seed from the seed jar based on its fingerprint.

```python
result: ots_result_t = ots_seed_jar_purge_seed_for_fingerprint(fingerprint)
assert ots_result_boolean(result), "Failed to purge seed with fingerprint"
```

* **Parameters:**
  **fingerprint** (*str*) – The fingerprint of the seed to purge.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_purge_seed_for_address(address: str) → [ots_result_t](#ots.raw.ots_result_t)

Purges a seed from the seed jar based on its address.

```python
result: ots_result_t = ots_seed_jar_purge_seed_for_address(str(address))
assert ots_result_boolean(result), "Failed to purge seed with address"
```

* **Parameters:**
  **address** (*str*) – The address of the seed to purge.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_transfer_seed_in(seed: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, name: str) → [ots_result_t](#ots.raw.ots_result_t)

Transfers a seed into the seed jar with the specified name.

```python
seed_reference: ots_handle_t = ots_seed_jar_transfer_seed_in(seed, "My Seed")
```

#### WARNING
Do not use the provided seed handle after this operation, the underlying ots_handle_t\* is not valid anymore.

* **Parameters:**
  * **seed** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The seed handle to transfer in.
  * **name** (*str*) – The name to associate with the seed.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_transfer_seed_out(seed: [ots_result_t](#ots.raw.ots_result_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Transfers a seed out of the seed jar. This removes the seed from the jar, but different from ots_seed_jar_purge_seed_for_\* functions, and ots_seed_jar_remove_seed, it does not wipe the seed, but transfers the ownership to the returned seed handle.

```python
seed_reference: ots_result_t = ots_seed_jar_seed_for_name("My Seed")
seed: ots_handle_t = ots_seed_jar_transfer_seed_out(seed_reference)
# Do not use `seed_reference` anymore, as the ownership has been transferred to `seed`.
# The `seed` handle as now the ownership of the seed.
```

* **Parameters:**
  **seed** ([*ots_result_t*](#ots.raw.ots_result_t) *|*  *\_CDataBase*) – The result of the seed operation to transfer out.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_transfer_seed_out_for_index(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Transfers a seed out of the seed jar based on its index. This removes the seed from the jar, but different from ots_seed_jar_purge_seed_for_\* functions, and ots_seed_jar_remove_seed, it does not wipe the seed, but transfers the ownership to the returned seed handle.

```python
assert ots_seed_jar_seed_count() > 0, "There should be at least one seed in the jar"
seed: ots_result_t = ots_seed_jar_transfer_seed_out_for_index(0)  # Transfers the seed at index 0 out of the seed jar
```

* **Parameters:**
  **index** (*int*) – The index of the seed to transfer out.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_transfer_seed_out_for_name(name: str) → [ots_result_t](#ots.raw.ots_result_t)

Transfers a seed out of the seed jar based on its name. This removes the seed from the jar, but different from ots_seed_jar_purge_seed_for_\* functions, and ots_seed_jar_remove_seed, it does not wipe the seed, but transfers the ownership to the returned seed handle.

```python
result: ots_result_t = ots_seed_jar_transfer_seed_out_for_name("My Seed")
seed: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **name** (*str*) – The name of the seed to transfer out.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_transfer_seed_out_for_fingerprint(fingerprint: str) → [ots_result_t](#ots.raw.ots_result_t)

Transfers a seed out of the seed jar based on its fingerprint. This removes the seed from the jar, but different from ots_seed_jar_purge_seed_for_\* functions, and ots_seed_jar_remove_seed, it does not wipe the seed, but transfers the ownership to the returned seed handle.

```python
result: ots_result_t = ots_seed_jar_transfer_seed_out_for_fingerprint(fingerprint)
seed: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **fingerprint** (*str*) – The fingerprint of the seed to transfer out.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_transfer_seed_out_for_address(address: str) → [ots_result_t](#ots.raw.ots_result_t)

Transfers a seed out of the seed jar based on its address.

```python
result: ots_result_t = ots_seed_jar_transfer_seed_out_for_address(address)
seed: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **address** (*str*) – The address of the seed to transfer out.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_clear() → [ots_result_t](#ots.raw.ots_result_t)

Clears all seeds from the seed jar.

```python
result: ots_result_t = ots_seed_jar_clear()
assert ots_result_boolean(result), "Failed to clear the seed jar"
```

* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_seeds() → [ots_result_t](#ots.raw.ots_result_t)

Returns all seeds in the seed jar.

```python
result: ots_result_t = ots_seed_jar_seeds()
seeds: list[ots_handle_t] = ots_result_handle_array_reference(result)
```

* **Returns:**
  ots_result_t containing the list of seeds.

### ots.raw.ots_seed_jar_seed_count() → [ots_result_t](#ots.raw.ots_result_t)

Returns the count of seeds in the seed jar.

```python
result: ots_result_t = ots_seed_jar_seed_count()
seed_count: int = ots_result_number(result)
```

* **Returns:**
  ots_result_t containing the count of seeds.

### ots.raw.ots_seed_jar_seed_for_index(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns a seed handle reference from the seed jar based on its index.

```Python
assert ots_seed_jar_seed_count() > 0, "There should be at least one seed in the jar"
result: ots_result_t = ots_seed_jar_seed_for_index(0)  # Retrieves the seed at index 0
if ots_is_result(result):
    seed_reference: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed to retrieve.
* **Returns:**
  ots_result_t containing the seed.

### ots.raw.ots_seed_jar_seed_for_fingerprint(fingerprint: str) → [ots_result_t](#ots.raw.ots_result_t)

Returns a seed handle reference from the seed jar based on its fingerprint.

```python
result: ots_result_t = ots_seed_jar_seed_for_fingerprint(fingerprint)
if ots_is_result(result):
    seed_reference: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **fingerprint** (*str*) – The fingerprint of the seed to retrieve.
* **Returns:**
  ots_result_t containing the seed.

### ots.raw.ots_seed_jar_seed_for_address(address: str) → [ots_result_t](#ots.raw.ots_result_t)

Returns a seed handle reference from the seed jar based on its address.

```python
result: ots_result_t = ots_seed_jar_seed_for_address(address)
if ots_is_result(result):
    seed_reference: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **address** (*str*) – The address of the seed to retrieve.
* **Returns:**
  ots_result_t containing the seed.

### ots.raw.ots_seed_jar_seed_for_name(name: str) → [ots_result_t](#ots.raw.ots_result_t)

Returns a seed handle reference from the seed jar based on its name.

```python
result: ots_result_t = ots_seed_jar_seed_for_name("My Seed")
if ots_is_result(result):
    seed_reference: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **name** (*str*) – The name of the seed to retrieve.
* **Returns:**
  ots_result_t containing the seed.

### ots.raw.ots_seed_jar_seed_name(seed: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase) → [ots_result_t](#ots.raw.ots_result_t)

Returns the name of the specified seed in the seed jar.

```python
result: ots_result_t = ots_seed_jar_seed_name(seed_reference)
if ots_is_result(result):
    seed_name: str = ots_result_string(result)
```

* **Parameters:**
  **seed** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed.
* **Returns:**
  ots_result_t containing the name of the seed.

### ots.raw.ots_seed_jar_seed_rename(seed: [ots_handle_t](#ots.raw.ots_handle_t) | \_CDataBase, name: str) → [ots_result_t](#ots.raw.ots_result_t)

Renames the specified seed in the seed jar.

```python
result: ots_result_t = ots_seed_jar_seed_rename(seed_reference, "New Seed Name")
if ots_is_result(result):  # no error means it is a success
    assert ots_result_boolean(result), "Failed to rename the seed"  # returns True
```

* **Parameters:**
  * **seed** ([*ots_handle_t*](#ots.raw.ots_handle_t) *|*  *\_CDataBase*) – The handle of the seed to rename.
  * **name** (*str*) – The new name for the seed.
* **Returns:**
  ots_result_t indicating the result of the operation.

### ots.raw.ots_seed_jar_item_name(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the name of the seed jar item at the specified index.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_name(0)  # Retrieves the name of the seed jar item at index 0
name: str = ots_result_string(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed jar item.
* **Returns:**
  ots_result_t containing the name of the seed jar item.

### ots.raw.ots_seed_jar_item_fingerprint(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the fingerprint of the seed jar item at the specified index.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_fingerprint(0)  # Retrieves the fingerprint of the seed jar item at index 0
fingerprint: str = ots_result_string(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed jar item.
* **Returns:**
  ots_result_t containing the fingerprint of the seed jar item.

### ots.raw.ots_seed_jar_item_address(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the address handle of the seed jar item at the specified index.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_address(0)  # Retrieves the address of the seed jar item at index 0
address: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed jar item.
* **Returns:**
  ots_result_t containing the address of the seed jar item.

### ots.raw.ots_seed_jar_item_address_string(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the address string of the seed jar item at the specified index.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_address_string(0)  # Retrieves the address string of the seed jar item at index 0
address_string: str = ots_result_string(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed jar item.
* **Returns:**
  ots_result_t containing the address string of the seed jar item.

### ots.raw.ots_seed_jar_item_seed_type(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the seed type of the seed jar item at the specified index.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_seed_type(0)  # Retrieves the seed type of the seed jar item at index 0
seed_type: SeedType = ots_result_seed_type(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed jar item.
* **Returns:**
  ots_result_t containing the seed type of the seed jar item.

### ots.raw.ots_seed_jar_item_seed_type_string(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the seed type string of the seed jar item at the specified index.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_seed_type_string(0)  # Retrieves the seed type string of the seed jar item at index 0
seed_type: str = ots_result_string(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed jar item.
* **Returns:**
  ots_result_t containing the seed type string of the seed jar item.

### ots.raw.ots_seed_jar_item_is_legacy(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Checks if the seed jar item at the specified index is a legacy item.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_is_legacy(0)  # Checks if the seed jar item at index 0 is legacy
legacy: bool = ots_result_boolean(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed jar item.
* **Returns:**
  ots_result_t indicating whether the item is legacy.

### ots.raw.ots_seed_jar_item_network(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the network of the seed jar item at the specified index.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_network(0)  # Retrieves the network of the seed jar item at index 0
network: Network = ots_result_network(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed jar item.
* **Returns:**
  ots_result_t containing the network of the seed jar item.

### ots.raw.ots_seed_jar_item_network_string(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the network string of the seed jar item at the specified index.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_network_string(0)  # Retrieves the network string of the seed jar item at index 0
network: str = ots_result_string(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed jar item.
* **Returns:**
  ots_result_t containing the network string of the seed jar item.

### ots.raw.ots_seed_jar_item_height(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the height of the seed jar item at the specified index.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_height(0)  # Retrieves the height of the seed jar item at index 0
height: int = ots_result_number(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed jar item.
* **Returns:**
  ots_result_t containing the height of the seed jar item.

### ots.raw.ots_seed_jar_item_timestamp(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the timestamp of the seed jar item at the specified index.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_timestamp(0)  # Retrieves the timestamp of the seed jar item at index 0
timestamp: int = ots_result_number(result)
```

* **Parameters:**
  **index** (*int*) – The index of the seed jar item.
* **Returns:**
  ots_result_t containing the timestamp of the seed jar item.

### ots.raw.ots_seed_jar_item_wallet(index: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns the wallet associated with the seed jar item at the specified index.

```python
assert ots_seed_jar_item_count() > 0, "There should be at least one seed jar item"
result: ots_result_t = ots_seed_jar_item_wallet(0)  # Retrieves the wallet of the seed jar item at index 0
wallet: ots_handle_t = ots_result_handle(result)
```

* **Parameters:**
  **index** – The index of the seed jar item.
* **Returns:**
  ots_result_t containing the wallet of the seed jar item.

### ots.raw.ots_version() → [ots_result_t](#ots.raw.ots_result_t)

Returns the version of the OTS library as string with the format “major.minor.patch”.

… code-block:: python

> version: ots_result_t = ots_version()
* **Returns:**
  ots_result_t containing the version string.

### ots.raw.ots_version_components() → [ots_result_t](#ots.raw.ots_result_t)

Returns the version components as int array of the OTS library.

… code-block:: python

> result: ots_result_t = ots_version_components()
> version: list[int] = ots_result_int_array(result)
* **Returns:**
  ots_result_t contains tuple containing the major, minor, and patch version numbers.

### ots.raw.ots_height_from_timestamp(timestamp: int, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN) → [ots_result_t](#ots.raw.ots_result_t)

Returns the height corresponding to a given timestamp and network.

```python
result: ots_result_t = ots_height_from_timestamp(1633036800, Network.MAIN)
height: int = ots_result_number(result)
```

* **Parameters:**
  * **timestamp** (*int*) – The timestamp to convert.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which to calculate the height.
* **Returns:**
  ots_result_t containing the height.

### ots.raw.ots_timestamp_from_height(height: int, network: [Network](enums.md#ots.enums.Network) | int = Network.MAIN) → [ots_result_t](#ots.raw.ots_result_t)

Returns the timestamp corresponding to a given height and network.

```python
result: ots_result_t = ots_timestamp_from_height(1000, Network.MAIN)
timestamp: int = ots_result_number(result)
```

* **Parameters:**
  * **height** (*int*) – The height to convert.
  * **network** ([*Network*](enums.md#ots.enums.Network) *|* *int*) – The network for which to calculate the timestamp.
* **Returns:**
  ots_result_t containing the timestamp.

### ots.raw.ots_random_bytes(size: int) → [ots_result_t](#ots.raw.ots_result_t)

Returns a random byte string of the specified size.

```python
result: ots_result_t = ots_random_bytes(32)
random: bytes = ots_result_char_array(result)
```

* **Parameters:**
  **size** (*int*) – The number of random bytes to generate.
* **Returns:**
  A byte string containing the random bytes.

### ots.raw.ots_random_32() → [ots_result_t](#ots.raw.ots_result_t)

Returns a random 32-byte string.

```python
result: ots_result_t = ots_random_32()
random: bytes = ots_result_char_array(result)
```

* **Returns:**
  ots_result_t containing a random 32-byte string.

### ots.raw.ots_check_low_entropy(data: bytes, min_entropy: float) → [ots_result_t](#ots.raw.ots_result_t)

Checks if the provided data has low entropy.

… code-block:: python

> result: ots_result_t = ots_check_low_entropy(data, 3.5)
> low_entropy: bool = ots_result_boolean(result)
* **Parameters:**
  * **data** (*bytes*) – The data to check.
  * **min_entropy** (*float*) – The minimum entropy level to consider.
* **Returns:**
  ots_result_t indicating whether the data has low entropy.

### ots.raw.ots_entropy_level(data: bytes) → [ots_result_t](#ots.raw.ots_result_t)

Returns the entropy level of the provided data.

… code-block:: python

> result: ots_result_t = ots_entropy_level(data)
> entropy: float = float(ots_result_string(result))
* **Parameters:**
  **data** – The data to analyze.
* **Returns:**
  ots_result_t containing the entropy level.

### ots.raw.ots_set_enforce_entropy(enforce: bool) → None

Sets whether to enforce entropy checks.

```python
ots_set_enforce_entropy(True)  # Enable entropy checks
ots_set_enforce_entropy(False)  # Disable entropy checks
```

* **Parameters:**
  **enforce** – A boolean indicating whether to enforce entropy checks.

### ots.raw.ots_set_enforce_entropy_level(level: float) → None

Sets the minimum entropy level for checks.

```python
ots_set_enforce_entropy_level(3.5)  # Set the minimum entropy level to 3.5
```

* **Parameters:**
  **level** (*float*) – The minimum entropy level to enforce.

### ots.raw.ots_set_max_account_depth(depth: int) → None

Sets the maximum account depth.

```python
ots_set_max_account_depth(5)  # Set the maximum account depth to 5
```

* **Parameters:**
  **depth** (*int*) – The maximum account depth to set.

### ots.raw.ots_set_max_index_depth(depth: int) → None

Sets the maximum index depth.

```python
ots_set_max_index_depth(10)  # Set the maximum index depth to 10
```

* **Parameters:**
  **depth** (*int*) – The maximum index depth to set.

### ots.raw.ots_set_max_depth(account_depth: int, index_depth: int) → None

Sets the maximum account and index depth.

```python
ots_set_max_depth(5, 10)  # Set the maximum account depth to 5 and index depth to 10
```

* **Parameters:**
  * **account_depth** (*int*) – The maximum account depth to set.
  * **index_depth** (*int*) – The maximum index depth to set.

### ots.raw.ots_reset_max_depth() → None

Resets the maximum account and index depth to their default values, of the library.

```python
ots_reset_max_depth()
```

### ots.raw.ots_get_max_account_depth(default: int = 0) → int

Returns the maximum account default.

```python
max_depth: int = ots_get_max_account_depth()
```

* **Parameters:**
  **default** (*int*) – The current account default. If set to 0, it will return the library’s default value, if not set.
* **Returns:**
  An integer representing the maximum account default.

### ots.raw.ots_get_max_index_depth(default: int = 0) → int

Returns the maximum index depth.

```python
max_depth: int = ots_get_max_index_depth()
```

* **Parameters:**
  **default** (*int*) – The default return default if values are not set. If set to 0, it will return the library’s default value, if not set.
* **Returns:**
  An integer representing the maximum index depth.

### ots.raw.ots_verify_data(data: bytes | str, address: str, signature: str | bytes) → [ots_result_t](#ots.raw.ots_result_t)

Verifies the provided data against the given address and signature.

```python
data = b'Hello, World!'
address = '43aM3fqR2WcDKsNqdUYHSVN4QCEdRMtYaXH9o5CqVg2LVRrB8D7WHvCXvRBMymLvZPWmSTdjsbqLrgGaSUMXYe6VKtJeWkK'
result: ots_result_t = ots_verify_data(data, address, signature)
verified: bool = ots_result_boolean(result)
```

* **Parameters:**
  * **data** (*bytes* *|* *str*) – The data to verify.
  * **address** (*str*) – The address to verify against.
  * **signature** (*str* *|* *bytes*) – The signature to verify.
* **Returns:**
  ots_result_t indicating the result of the verification.
