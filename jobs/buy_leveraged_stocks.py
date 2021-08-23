from decimal import Decimal

import global_common
from alpaca.models import Position, MarketData, Account, MarketClock, Order, OrderSide, OrderType, OrderTimeInForce

from jobs import get_account_summary


@global_common.threaded
@global_common.job("Buying stocks leveraged")
def buy_leveraged_stock(symbol: str, leverage: int) -> None:
    Position.close_all_by_symbol(symbol)
    market_data: MarketData = MarketData.get(symbol)
    number_of_stock: int = int((Account.cash * Decimal(str(leverage))) / market_data.ask_price)
    Order.place(symbol, number_of_stock, OrderSide.BUY, OrderType.MARKET, None, OrderTimeInForce.DAY)


def do() -> None:
    get_account_summary.do()
    market_clock = MarketClock.get()
    if market_clock.is_open:
        buy_leveraged_stock("QQQ", 3)


if __name__ == "__main__":
    do()
