import requests
from src.bank_api import sber, vtb, sravni_ru
from src.bank_api.common import logger, calculate_average_rate
from src.config import bot_id

url = f'https://api.telegram.org/bot{bot_id}/sendMessage'
msg_template = {"chat_id": "@mortgage_pulse_rus", "parse_mode": "html"}


def make_message(rates: list) -> dict:
    return {
        **msg_template,
        "text": format_mortgage_message(rates).encode('utf-8')
    }


def make_summary_message(rate: list, market) -> dict:
    return {
        **msg_template,
        "text": f'<b>Среднерыночная Ставка: {rate.__str__()}</b>'.encode("utf-8")
    }


def make_header_message(market) -> dict:
    return {
        **msg_template,
        "text": f'<b>{market.__str__().capitalize():}</b>'.encode("utf-8")
    }


def format_mortgage_message(rates: list) -> str:
    msg = ''
    for rate in rates:
        if rate:
            bank_name = rate['bank_name']
            median_rate = rate['rate']['median']
            from_rate = rate['rate']['from']
            to_rate = rate['rate']['to']
            source = rate['source']
            msg += f'{bank_name} ({source}): от {from_rate}, до {to_rate};   '

    return msg


def get_rates(market):
    rates = []
    rates += [sber.get_mortgage_data(sber.market_index[market])]
    rates += [vtb.get_mortgage_data(vtb.market_index[market])]
    rates += sravni_ru.get_mortgage_data(sravni_ru.market_index[market])

    return rates


def send_messages_for(market: str):
    try:
        logger.info(f'Sending messages for {market}')
        rates = get_rates(market)
        data = make_message(rates)
        market_desc = market

        res = requests.post(url=url, data=make_header_message(market_desc))
        logger.info(f'header message response={res.text}')
        res = requests.post(url=url, data=data)
        logger.info(f'main message response={res.text}')
        avg_rate = calculate_average_rate(rates)
        res = requests.post(
            url=url, data=make_summary_message(avg_rate, market_desc)
        )
        logger.info(f'sum message response={res.text}')

    except Exception as e:
        logger.error(e, exc_info=True)


def main():
    send_messages_for('первичный рынок')
    send_messages_for('вторичный рынок')


if __name__ == '__main__':
    main()
