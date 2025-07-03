from .raw import *
from .exceptions import OtsException
from .address import Address, AddressString
from dataclasses import dataclass, field


class Flow:
    """
    Represents simply a an address and an amount in a Monero transaction/transfer description.

    .. note::

        In the original Monero codebase and cryptonote it is refered to splitted_dsts and change_dts.
    """

    def __init__(self, address: Address | str, amount: int):
        """
        Initializes a Flow with an address and an amount.

        :param address: The address of the flow, can be a string or an Address object.
        :type address: Address | str
        :param int amount: The amount of the flow, a non-negative integer.
        """
        assert isinstance(address, (Address, str)), "address must be an Address or a string"
        assert isinstance(amount, int), "amount must be an integer"
        assert amount >= 0, "amount must be non-negative"
        self.address: Address = address if isinstance(address, Address) else Address.fromString(address)
        """
        The address of the flow, can be a string or an Address object.
        """
        self.amount: int = amount
        """
        The amount of the flow, a non-negative integer.
        """


@dataclass
class TransferDescription:
    """
    Represents a transfer description in a Monero transaction description.
    A transaction can have one or more transfers, each with its own details.
    """

    amountIn: int = 0
    """Amount of the input for this transfer."""
    amountOut: int = 0
    """Amount of the output for this transfer."""
    ringSize: int = 0
    """Ring size for the transfer"""
    unlockTime: int = 0  # TODO: check which version exactly this was removed
    """
    Unlock time for the transfer, in blocks.
    **deprecated**

    .. note::

        Removed in Monero v0.18.4

    """
    flows: list[Flow] = field(default_factory=list)
    """How many XMR go to which address, in this transfer."""
    change: Flow | None = None
    """To which address the change goes, if any, and how much."""
    fee: int = 0
    """Fee for this transfer, in atomic units."""
    paymentId: str | None = None
    """Payment ID for this transfer, if any."""
    dummyOutputs: int = 0
    """Number of dummy outputs in this transfer."""
    txExtra: bytes | None = None
    """Extra data for the transaction, if any."""


class TxDescription:
    """
    Represents a Monero transaction description.
    """

    def __init__(self, handle: ots_handle_t):
        self.handle: ots_handle_t = handle
        self._txSet: bytes | None = None
        self._txSetSize: int | None = None
        self._amountIn: int | None = None
        self._amountOut: int | None = None
        self._flows: list[ots_flow_t] | None = None
        self._change: Flow | None = None
        self._hasChange: bool | None = None
        self._fee: int | None = None
        self._transfers: list[TransferDescription] | None = None

    @property
    def txSet(self) -> bytes:
        """
        Returns the transaction set as a byte string.
        """
        if self._txSet is not None:
            return self._txSet
        result: ots_result_t = ots_tx_description_set(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._txSet = ots_result_bytes(result)
        return self._txSet

    @property
    def txSetSize(self) -> int:
        """
        Returns the size of the transaction set.
        """
        if self._txSetSize is not None:
            return self._txSetSize
        result: ots_result_t = ots_tx_description_set_size(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._txSetSize = ots_result_number(result)
        return self._txSetSize

    @property
    def amountIn(self) -> int:
        """
        Returns the total input amount for the transaction.
        """
        if self._amountIn is not None:
            return self._amountIn
        result: ots_result_t = ots_tx_description_amount_in(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._amountIn = ots_result_number(result)
        return self._amountIn

    @property
    def amountOut(self) -> int:
        """
        Returns the total output amount for the transaction.
        """
        if self._amountOut is not None:
            return self._amountOut
        result: ots_result_t = ots_tx_description_amount_out(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._amountOut = ots_result_number(result)
        return self._amountOut

    @property
    def flows(self) -> list[Flow]:
        """
        Returns the list of flows in the transaction.
        """
        if self._flows is not None:
            return self._flows
        flow_count: int = ots_tx_description_flow_count(self.handle)
        self._flows = [
            Flow(
                Address.fromString(ots_tx_description_flow_address(self.handle, i)),
                ots_tx_description_flow_amount(self.handle, i)
            )
        for i in range(flow_count)]
        return self._flows

    @property
    def change(self) -> Flow | None:
        """
        Returns the change flow if it exists, otherwise None.
        """
        if self._change is not None or self._hasChange is False:
            return self._change
        self._hasChange = ots_tx_description_has_change(self.handle)
        if not self._hasChange:
            return None
        self._change = Flow(
            Address.fromString(ots_tx_description_change_address(self.handle)),
            ots_tx_description_change_amount(self.handle)
        )
        return self._change

    @property
    def fee(self) -> int:
        """
        Returns the transaction fee.
        """
        if self._fee is not None:
            return self._fee
        result: ots_result_t = ots_tx_description_fee(self.handle)
        if ots_is_error(result):
            raise OtsException.from_result(result)
        self._fee = ots_result_number(result)
        return self._fee

    @property
    def transfers(self) -> list[TransferDescription]:
        """
        Returns the list of transfer descriptions for the transaction.
        """
        if self._transfers is not None:
            return self._transfers
        transfer_count: int = ots_tx_description_transfers_count(self.handle)
        self._transfers = []
        for i in range(transfer_count):
            td = TransferDescription(
                amountIn=ots_tx_description_transfer_amount_in(self.handle, i),
                amountOut=ots_tx_description_transfer_amount_out(self.handle, i),
                ringSize=ots_tx_description_transfer_ring_size(self.handle, i),
                unlockTime=ots_tx_description_transfer_unlock_time(self.handle, i),
                flows=[
                    Flow(
                        Address.fromString(ots_tx_description_transfer_flow_address(self.handle, i, j)),
                        ots_tx_description_transfer_flow_amount(self.handle, i, j)
                    )
                    for j in range(ots_tx_description_transfer_flows_count(self.handle, i))
                ],
                change=Flow(
                    Address.fromString(ots_tx_description_transfer_change_address(self.handle, i)),
                    ots_tx_description_transfer_change_amount(self.handle, i)
                ) if ots_tx_description_transfer_has_change(self.handle, i) else None,
                fee=ots_tx_description_transfer_fee(self.handle, i),
                paymentId=ots_tx_description_transfer_payment_id(self.handle, i),
                dummyOutputs=ots_tx_description_transfer_dummy_outputs(self.handle, i),
                txExtra=ots_tx_description_transfer_extra(self.handle, i) if ots_tx_description_transfer_extra_size(self.handle, i) > 0 else None
            )
            self._transfers.append(td)
        return self._transfers


class TxWarning:
    """
    Represents a warning in a Monero transaction description.
    The reasoning behind was to alert the user about potential issues,
    like unlock time in the future, high transaction fees, or other anomalies.

    .. note::

        Monero removed (IMO) unfortunately the enforcement of unlock time in the
        meanwhile, other issues are already yield and error/exception, so a warning
        is there also not needed. And high transacion fees can not really be reasoned
        on a offline signing device neither (IMO), exept one would set a hard limit.

        So this class has no fields and no methods and is just a placeholder at the moment.

    .. warning::

        This class is not yet implemented, and may be even removed in future versions of OTS.
    """

    def __init__(self, handle: ots_handle_t):
        assert isinstance(handle, ots_handle_t), "handle must be an ots_handle_t instance"
        assert handle.type == HandleType.TX_WARNING, "handle must be of type TX_WARNING"
        self.handle: ots_handle_t = handle
