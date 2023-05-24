# big-insect

you need to follow the below guide to run this program

## Run with docker

first you need to install docker `https://www.docker.com/products/docker-desktop/` and make sure it's running.

Then for the first time only run the `setup.exe` file.

After that you can run the app from `run.exe` file.


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
