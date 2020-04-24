import requests
import json
from src.bank_api.common import logger, credit_params

url = "https://www.vtb.ru/api/Sitecore/Mortgage/NewBuildingAjax"
headers = {'Content-Type': 'application/json'}
market_index = {"первичный рынок": "NewBuildingProgram", "вторичный рынок": "ResaleProgram"}

min_rate_seed = {"DownPayment": credit_params['prepaid'], "PropertyPrice": credit_params['full_price'],
                 "MonthlyIncome": "100000", "DataSourceId": "{AEE792C1-3565-4835-B7E5-9FA9A9F4009F}",
                 "MaternialCapital": "", "MonthlyPaymentByCost": "51540", "CreditTermByCost": "10",
                 "CreditSumByIncome": None, "MonthlyPaymentByIncome": "69995", "CreditTermByIncome": "30",
                 "Programs": ["1"], "Clients": [], "MonthlyPaymentByCostSign": "", "MonthlyPaymentByIncomeSign": ""}

max_rate_seed = {"DownPayment": credit_params['prepaid'], "PropertyPrice": credit_params['full_price'],
                 "MonthlyIncome": "100000", "DataSourceId": "{AEE792C1-3565-4835-B7E5-9FA9A9F4009F}",
                 "MaternialCapital": "", "MonthlyPaymentByCost": "51540", "CreditTermByCost": "10",
                 "CreditSumByIncome": None, "MonthlyPaymentByIncome": "69995", "CreditTermByIncome": "30",
                 "Programs": [], "Clients": [], "MonthlyPaymentByCostSign": "", "MonthlyPaymentByIncomeSign": ""}


def get_mortgage_data(mortgage_goal: str) -> dict:
    try:
        min_rate, max_rate = _get_vtb_rates(mortgage_goal)
        logger.debug(f'VTB Min rate={min_rate} ("{mortgage_goal}")')
        logger.debug(f'VTB Max rate={max_rate} ("{mortgage_goal}")')

        return _extract_mortgage_data({
            'min_rate_data': min_rate,
            'max_rate_data': max_rate
        })

    except Exception as e:
        logger.exception(e)
        return _extract_mortgage_data({})


def _min_rate_params(mortgage_goal: str) -> dict:
    return {"ProgramName": mortgage_goal, **min_rate_seed}


def _max_rate_params(mortgage_goal: str) -> dict:
    return {"ProgramName": mortgage_goal, **max_rate_seed}


def _extract_mortgage_data(mortgage_info: dict) -> dict:
    short_bank_data = {}

    if mortgage_info:
        short_bank_data['rate'] = {}
        short_bank_data['bank_name'] = '<b>ВТБ</b>'
        min_rate = mortgage_info['min_rate_data']
        max_rate = mortgage_info['max_rate_data']
        short_bank_data['rate']['median'] = round(((min_rate + max_rate) / 2), 2)
        short_bank_data['rate']['to'] = max_rate
        short_bank_data['rate']['from'] = min_rate
        short_bank_data['source'] = 'www.vtb.ru'

    return short_bank_data


def _get_vtb_rates(mortgage_goal):
    min_rate = _get_vtb_rate(
        _min_rate_params(mortgage_goal=mortgage_goal)
    ).json()['MorgageRateByCost']
    max_rate = _get_vtb_rate(
        _max_rate_params(mortgage_goal=mortgage_goal)
    ).json()['MorgageRateByCost']

    return min_rate, max_rate


def _get_vtb_rate(params):
    return requests.post(url=url, headers=headers, data=json.dumps(params))