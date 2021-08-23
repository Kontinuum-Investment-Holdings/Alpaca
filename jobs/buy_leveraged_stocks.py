from decimal import Decimal
from typing import List

import communication.telegram
import global_common
from alpaca.models import Position, MarketData, Account, MarketClock, Order, OrderSide, OrderType, OrderTimeInForce

import constants


@global_common.threaded
@global_common.job("Buying stocks leveraged")
def buy_leveraged_stock(symbol: str, leverage: int) -> None:
    Position.close_all_by_symbol(symbol)
    market_data: MarketData = MarketData.get(symbol)
    number_of_stock: int = int((Account.cash * Decimal(str(leverage))) / market_data.ask_price)
    Order.place(symbol, number_of_stock, OrderSide.BUY, OrderType.MARKET, None, OrderTimeInForce.DAY)

    account: Account = Account.call()
    message: str = f"<u><b>Account Summary</b></u>" \
                   f"\n\nEquity: <i>${global_common.get_formatted_string_from_decimal(account.equity)}</i>"

    position_list: List[Position] = Position.call()
    for position in position_list:
        position_market_data: MarketData = MarketData.get(position.symbol)
        message = message + f"\n\nStock: {position.symbol}" \
                            f"\nQuantity: {position.quantity}" \
                            f"\nStock Price: ${global_common.get_formatted_string_from_decimal(position_market_data.bid_price)}" \
                            f"\nValue: ${position.market_value}"

    communication.telegram.send_message(constants.TELEGRAM_BOT_USERNAME, message, True)


def do() -> None:
    market_clock = MarketClock.get()
    if market_clock.is_open:
        buy_leveraged_stock("QQQ", 3)


if __name__ == "__main__":
    do()
