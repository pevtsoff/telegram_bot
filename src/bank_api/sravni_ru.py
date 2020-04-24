import requests
from src.bank_api.common import logger, credit_params

url = 'https://www.sravni.ru/proxy-mortgage/mortgage/list'
market_index = {"первичный рынок": "1", "вторичный рынок": "2"}


def get_mortgage_data(mortgage_goal: str) -> dict:
    try:
        result = requests.post(
            url=url,
            json=_get_request_params(mortgage_goal)
        )
        logger.debug(f'sravni.ru rates={result.json()["items"]}')

        return _extract_mortgage_data(result.json()['items'])

    except Exception as e:
        logger.exception(e)
        return _extract_mortgage_data([])


def _get_request_params(mortgage_goal: str) -> dict:
    return {
        "filters":
            {
                "creditAmount": credit_params['full_price'],
                "initialAmount": credit_params['prepaid'],
                "rating": "50", "organization": [],
                "mortgageTerm": "120",
                "customerType": "any",
                "documents": "0",
                "demands": "0",
                "popularBanks": [],
                "mortgagePurpose": mortgage_goal,
                "mortgageProgram": [],
                "solvencyProof": "any",
                "location":
                    "6.56.1394.2752."},
        "limit": 100,
        "advertising":
            {"source": "search"}
    }


def _extract_mortgage_data(bank_list: list) -> dict:
    mortgage_data = []

    if bank_list:
        for bank in bank_list:
            short_bank_data = {}
            short_bank_data['rate'] = {}
            short_bank_data['bank_name'] = bank['organization']['name']
            rate = bank['rate']['periods'][0]['rate']
            short_bank_data['rate']['median'] = (rate['from'] + rate['to']) / 2
            short_bank_data['rate']['to'] = rate['to']
            short_bank_data['rate']['from'] = rate['from']
            short_bank_data['source'] = 'sravni.ru'
            mortgage_data.append(short_bank_data)

        mortgage_data.sort(key=lambda x: x['rate']['from'])

    return mortgage_data

