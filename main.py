from alpine.exchanges import Wrapper
from alpine.exchanges.utils import compute_closing, compute_amount
import click
import sys
import time


@click.command()
@click.option(
    "--position",
    help="position to open: long or short",
    default="long",
    type=click.Choice(["long", "short"], case_sensitive=False),
)
@click.option(
    "--leverage", help="leverage to use. Minimum is 1.", required=True, type=int
)
@click.option("--symbol", help="Symbol to trade", required=True, type=str)
@click.option(
    "--mode",
    help="the mode to open the order: isolated",
    default="isolated",
    type=click.Choice(["isolated"], case_sensitive=False),
)
@click.option(
    "--price",
    help="The price of the symbol we want to fill the order at. If not set use the current market price.",
    required=False,
    default=None,
    type=float,
)
@click.option(
    "--amount",
    help="Amount of the symbol to open the order with OR `coin` amount you want to use for the order. In this case, suffix the amount with `coin`",
    required=True,
    type=str,
)
@click.option(
    "--margin-coin",
    help="The margin coin to use. Default to USDT",
    required=False,
    default="USDT",
)
@click.option(
    "--take-profit",
    help="The value of the Take Profit. Value of the symbol or percentage of PnL.Once reached, the order will be closed",
    required=True,
    type=str,
)
@click.option(
    "--stop-loss",
    help="The value of the Stop Loss. Value of the symbol or percentage of PnL. Once reached, the order will be closed",
    required=True,
    type=str,
)
@click.option(
    "--wait",
    help="Wait time in seconds before recreating an order with the same parameter, once the previous one is closed. If not set, does not wait",
    default=1,
    type=int,
)
@click.option(
    "--repeat",
    help="Number of order to make before stopping the script. If not set, does not end",
    default=None,
    type=int,
)
@click.option(
    "--exchange",
    help="Exchange to use for the order",
    required=True,
    type=click.Choice(["bitget", "binance"], case_sensitive=False),
)
def main(
    position,
    leverage,
    symbol,
    mode,
    price,
    amount,
    margin_coin,
    take_profit,
    stop_loss,
    wait,
    repeat,
    exchange,
):
    return scalp(
        position,
        leverage,
        symbol,
        mode,
        price,
        amount,
        margin_coin,
        take_profit,
        stop_loss,
        wait,
        repeat,
        exchange,
    )


def scalp(
    position,
    leverage,
    symbol,
    mode,
    price,
    amount,
    margin_coin,
    take_profit,
    stop_loss,
    wait,
    repeat,
    exchange,
):
    wrapper = Wrapper(exchange)
    symbol_value = price if price else wrapper.get_current_symbol_value(symbol)
    # 1. We set the leverage
    wrapper.set_leverage(leverage, position, symbol, margin_coin)
    # 2. Amount: If we don't set the number of the symbol coin we want to buy,
    # but instead the amount of the margin coin we want to use, then we need to calculate the proper amount of the symbol to buy.
    if "coin" in amount:
        amount = compute_amount(leverage, amount, symbol_value)
    else:
        amount = float(amount)
    # 3. Take profit: if we don't set the value of the symbol we want to close the order,
    # but instead the percentage of PnL we want to close the order at, we need to calculate the value of the symbol
    if "%" in take_profit:
        take_profit = compute_closing(leverage, amount, symbol_value, take_profit)
    else:
        take_profit = float(take_profit)
    # 4. Same for Stop loss
    if "%" in stop_loss:
        stop_loss = compute_closing(leverage, amount, symbol_value, stop_loss, -1)
    else:
        stop_loss = float(stop_loss)
    # 5. Create the order
    print(
        f"[{symbol}] Creating an {mode} {position} order of {int(amount)} coins[{leverage}x]"
    )
    print(f"[{symbol}] Entry price at {symbol_value}")
    print(f"[{symbol}] Take profit at {take_profit}")
    print(f"[{symbol}] Stop loss at {stop_loss}")
    order_id = wrapper.create_order(
        position, symbol, price, amount, margin_coin, take_profit, stop_loss
    )
    print(f"[{symbol}] Order {order_id} created.")
    detail = wrapper.get_order_detail(symbol, order_id)
    while detail["state"] != "filled":
        print(f"[{symbol}] Checking if order has been filled.")
        detail = wrapper.get_order_detail(symbol, order_id)
        time.sleep(60)
    print(f"[{symbol}] Order has been filled.")
    while True:
        print(f"[{symbol}] Checking if the position has been closed.")
        current = wrapper.get_current_position(symbol, margin_coin)
        if not current:
            break
        print(
            f"[{symbol}] Position still opened, current unrealized PnL: {current['unrealizedPL']} {margin_coin}"
        )
        time.sleep(60)
    past = wrapper.get_historical_position(symbol, margin_coin)
    profit = past["netProfit"] if past else 0
    print(
        f"[{symbol}] Position has been closed, realized PnL (after fees): {profit} {margin_coin}"
    )
    repeat = repeat if repeat else sys.maxsize
    repeat = repeat - 1
    if repeat == 0:
        sys.exit(0)
    print(f"Re-initializing scalping in {wait} seconds.")
    time.sleep(wait)
    return scalp(
        position,
        leverage,
        symbol,
        mode,
        price,
        str(amount),
        margin_coin,
        str(take_profit),
        str(stop_loss),
        wait,
        repeat,
        exchange,
    )


if __name__ == "__main__":
    main()
