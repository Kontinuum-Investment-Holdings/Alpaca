from typing import List

import communication.telegram
import global_common
from alpaca.models import Account, Position, MarketData

import constants


@global_common.threaded
@global_common.job("Get Account Summary")
def get_account_summary() -> None:
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
    get_account_summary()


if __name__ == "__main__":
    do()
