import requests
from src.bank_api.common import logger, credit_params

headers = {'Api-Key': '728a2644-fefc-43c1-9054-5806c8fda7ef'}
market_index = {"первичный рынок": 4, "вторичный рынок": 3}
min_rate_url = 'https://api.domclick.ru/calc/api/v2/mortgages/calculate?isIncomeSberbankCard=yes&isConfirmIncome=true&productId={mortgage_goal}&estateCost={full_price}&deposit={prepaid}&term=120&age=420&isInsured=true&isMarried=true&isHusbandWifeLess35Years=true&childrens=0&useOnRegDiscount=yes&useDeveloperDiscount=true&useRealtyDiscount=true&kladrId=7700000000000'
max_rate_url = 'https://api.domclick.ru/calc/api/v2/mortgages/calculate?isIncomeSberbankCard=no&isConfirmIncome=true&productId={mortgage_goal}&estateCost={full_price}&deposit={prepaid}&term=120&age=420&isInsured=true&isMarried=false&isHusbandWifeLess35Years=false&childrens=0&useOnRegDiscount=no&useDeveloperDiscount=false&useRealtyDiscount=false&kladrId=7700000000000'


def get_mortgage_data(mortgage_goal: str) -> dict:
    try:
        min_rate , max_rate = _get_sber_rates(mortgage_goal)
        logger.debug(f'Sber Min rate={min_rate}')
        logger.debug(f'Sber Max rate={max_rate}')

        return _extract_mortgage_data({
            'min_rate_data': min_rate,
            'max_rate_data': max_rate
        })


    except Exception as e:
        logger.exception(e)
        return _extract_mortgage_data({})

def _extract_mortgage_data(mortgage_info: dict) -> dict:
    short_bank_data = {}

    if mortgage_info:
        short_bank_data['rate'] = {}
        short_bank_data['bank_name'] = '<b>Сбербанк</b>'
        min_rate = mortgage_info['min_rate_data']
        max_rate = mortgage_info['max_rate_data']
        short_bank_data['rate']['median'] = round((min_rate + max_rate) / 2, 2)
        short_bank_data['rate']['to'] = max_rate
        short_bank_data['rate']['from'] = min_rate
        short_bank_data['source'] = 'domclick.ru'

    return short_bank_data


def _get_sber_rates(mortgage_goal):
    min_rate = _get_sber_rate(
        min_rate_url.format(
            prepaid=credit_params['prepaid'],
            full_price=credit_params['full_price'],
            mortgage_goal=mortgage_goal
        )
    ).json()['data']['calculation']['rate']
    max_rate = _get_sber_rate(
        max_rate_url.format(
            prepaid=credit_params['prepaid'],
            full_price=credit_params['full_price'],
            mortgage_goal=mortgage_goal
        )
    ).json()['data']['calculation']['rate']

    return min_rate, max_rate


def _get_sber_rate(url):
    return requests.get(url=url, headers=headers)