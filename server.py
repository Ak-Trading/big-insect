from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from ib_insync import IB, Contract, MarketOrder, LimitOrder, util
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

nest_asyncio.apply()

# util.logToConsole("DEBUG")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ib.connectAsync(port=7497, clientId=0)
    yield
    ib.disconnect()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


ib = IB()


@app.get("/")
def root():
    return {"message": "Hello"}


@app.post("/webhook")
async def webhook(data: dict):
    contract = Contract(secType="STK", symbol=data["contract"], exchange="SMART", currency="USD")
    if not ib.isConnected():
        await ib.connectAsync(port=7497, clientId=0)
    contract = ib.qualifyContracts(contract)[0]

    trades = ib.reqAllOpenOrders()

    for trade in trades:
        if trade.contract == contract:
            ib.cancelOrder(trade.order)

    positions = ib.positions()
    position = next((p for p in positions if p.contract == contract), None)

    if position is not None:
        quantity = data["quantity"] - position.position
    else:
        quantity = data["quantity"]

    if quantity < 0:
        quantity *= -1
        data["side"] = "SELL"
    else:
        data["side"] = "BUY"

    if data["order_type"] == "market":
        order = MarketOrder(data["side"], quantity)
    else:
        order = LimitOrder(data["side"], quantity, data["limit"], outsideRth=True)

    ib.placeOrder(contract, order)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
