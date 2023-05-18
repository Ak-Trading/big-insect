from fastapi import Depends, FastAPI
from ib_insync import IB, Contract, MarketOrder, LimitOrder
import asyncio

app = FastAPI()


def get_ib():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ib = IB()
    ib.connect()
    try:
        yield ib
    finally:
        ib.disconnect()


@app.get("/")
def root():
    return {"message": "Hello"}


@app.post("/webhook")
def webhook(data: dict, ib: IB = Depends(get_ib)):
    contract = Contract(secType="STK", symbol=data["contract"], exchange="SMART", currency="USD")

    contract = ib.qualifyContracts(contract)[0]

    if data["side"].upper() == "SELL":
        data["quantity"] *= -1

    if data["order_type"] == "market":
        order = MarketOrder(data["side"], data["quantity"])
    else:
        order = LimitOrder(data["side"], data["quantity"], data["limit"])

    ib.placeOrder(contract, order)
