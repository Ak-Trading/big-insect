from fastapi import Depends, FastAPI
from ib_insync import IB, Contract, MarketOrder, LimitOrder
import asyncio
import random

app = FastAPI()


def get_ib():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ib = IB()
    ib.connect(clientId=random.randint(1, 100))
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

    positions = ib.positions()

    position = next((p for p in positions if p.contract == contract), None)

    if position is not None:
        quantity = data["quantity"] - position.position
    else:
        quantity = data["quantity"]

    if data["side"].upper() == "SELL":
        quantity *= -1

    if data["order_type"] == "market":
        order = MarketOrder(data["side"], quantity)
    else:
        order = LimitOrder(data["side"], quantity, data["limit"])

    ib.placeOrder(contract, order)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
