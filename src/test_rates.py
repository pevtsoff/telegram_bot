import logging
from src.bank_api.common import logger, calculate_average_rate, calculate_weighted_average_rate
from src.telegram_api import get_rates, make_message, make_header_message, make_summary_message


def test_rates_api():
    initial_rates = get_rates('первичный рынок')
    logger.info(f'первичный рынок {initial_rates=}')
    secondary_rates = get_rates('вторичный рынок')
    logger.info(f'вторичный рынок {secondary_rates=}')
    assert_rates(initial_rates)
    assert_rates(secondary_rates)


def test_telegram_messages_manual(caplog):
    with caplog.at_level(logging.INFO, logger='src.bank_api.common'):
        _messages_for('первичный рынок')
        _messages_for('вторичный рынок')


def _messages_for(market: str):
    rates = get_rates(market)
    rate_message = make_message(rates)['text'].decode('utf-8')
    market_desc = market
    avg_rate = calculate_average_rate(rates)
    weighted_avg = calculate_weighted_average_rate(rates)
    logger.info(f'{weighted_avg=}')
    logger.info(make_header_message(market_desc)['text'].decode('utf-8'))
    logger.info(rate_message)
    logger.info(make_summary_message(avg_rate, market_desc)['text'].decode('utf-8'))
    assert_rates(rates)


def assert_rates(rates):
    assert rates[0]['bank_name'].__contains__('Сбербанк')
    assert rates[1]['bank_name'].__contains__('ВТБ')

    for rate in rates:
        assert rate['rate']['to'] > 0
        assert rate['rate']['from'] > 0