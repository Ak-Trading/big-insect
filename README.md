# big-insect

## Tradingview alert message

The current tradingview message looks like this:

```
{
"contract":"{{ticker}}",
"side":"{{strategy.order.action}}",
"quantity":{{strategy.position_size}},
"order_type":"market",
"limit":{{strategy.order.price}}
}
```

so to make order you need to send this message to the `/webhook` endpoint.

## Generate exe

to generate the exe you need to write

```
pyinstaller --onefile --clean -p . --distpath . server.py
```
