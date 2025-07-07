# Transaction

Pure data classes for representing unsigned transactions to inspect them before signing.

## TxDescription

### *class* ots.transaction.TxDescription(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

Represents a Monero transaction description.

#### *property* txSet *: bytes*

Returns the transaction set as a byte string.

#### *property* txSetSize *: int*

Returns the size of the transaction set.

#### *property* amountIn *: int*

Returns the total input amount for the transaction.

#### *property* amountOut *: int*

Returns the total output amount for the transaction.

#### *property* flows *: list[[Flow](#ots.transaction.Flow)]*

Returns the list of flows in the transaction.

#### *property* change *: [Flow](#ots.transaction.Flow) | None*

Returns the change flow if it exists, otherwise None.

#### *property* fee *: int*

Returns the transaction fee.

#### *property* transfers *: list[[TransferDescription](#ots.transaction.TransferDescription)]*

Returns the list of transfer descriptions for the transaction.

## TransferDescription

### *class* ots.transaction.TransferDescription(amountIn: int = 0, amountOut: int = 0, ringSize: int = 0, unlockTime: int = 0, flows: list[~ots.transaction.Flow] = <factory>, change: ~ots.transaction.Flow | None = None, fee: int = 0, paymentId: str | None = None, dummyOutputs: int = 0, txExtra: bytes | None = None)

Represents a transfer description in a Monero transaction description.
A transaction can have one or more transfers, each with its own details.

#### amountIn *: int* *= 0*

Amount of the input for this transfer.

#### amountOut *: int* *= 0*

Amount of the output for this transfer.

#### ringSize *: int* *= 0*

Ring size for the transfer

#### unlockTime *: int* *= 0*

Unlock time for the transfer, in blocks.
**deprecated**

#### NOTE
Removed in Monero v0.18.4

#### flows *: list[[Flow](#ots.transaction.Flow)]*

How many XMR go to which address, in this transfer.

#### change *: [Flow](#ots.transaction.Flow) | None* *= None*

To which address the change goes, if any, and how much.

#### fee *: int* *= 0*

Fee for this transfer, in atomic units.

#### paymentId *: str | None* *= None*

Payment ID for this transfer, if any.

#### dummyOutputs *: int* *= 0*

Number of dummy outputs in this transfer.

#### txExtra *: bytes | None* *= None*

Extra data for the transaction, if any.

## Flow

### *class* ots.transaction.Flow(address: [Address](address.md#ots.address.Address) | str, amount: int)

Represents simply a an address and an amount in a Monero transaction/transfer description.

#### NOTE
In the original Monero codebase and cryptonote it is refered to splitted_dsts and change_dts.

#### address *: [Address](address.md#ots.address.Address)*

The address of the flow, can be a string or an Address object.

#### amount *: int*

The amount of the flow, a non-negative integer.

## TxWarning

### *class* ots.transaction.TxWarning(handle: [ots_handle_t](raw.md#ots.raw.ots_handle_t))

Represents a warning in a Monero transaction description.
The reasoning behind was to alert the user about potential issues,
like unlock time in the future, high transaction fees, or other anomalies.

#### NOTE
Monero removed (IMO) unfortunately the enforcement of unlock time in the
meanwhile, other issues are already yield and error/exception, so a warning
is there also not needed. And high transacion fees can not really be reasoned
on a offline signing device neither (IMO), exept one would set a hard limit.

So this class has no fields and no methods and is just a placeholder at the moment.

#### WARNING
This class is not yet implemented, and may be even removed in future versions of OTS.
