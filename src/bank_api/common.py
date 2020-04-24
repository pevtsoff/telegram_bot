import logging

credit_params = {"prepaid": 3000000, "full_price": 7000000,"months_qty": 120}


def calculate_average_rate(short_bank_data: list) -> float:
    return round(sum(float(bank['rate']['median']) for bank in short_bank_data)
                 / short_bank_data.__len__(), 2)


def calculate_weighted_average_rate(short_bank_data: list) -> float:
    sber = short_bank_data[0]
    vtb = short_bank_data[1]
    others = sum(
        float(bank['rate']['median']) for bank in short_bank_data[2:]
    ) / short_bank_data[2:].__len__()

    sber_weighted_avg = sber['rate']['median'] * 0.56
    vtb_weighted_avg = vtb['rate']['median'] * 0.256
    others_weighted_avg = others * 0.184
    total_weighted_avg = round(
        sber_weighted_avg + vtb_weighted_avg + others_weighted_avg,
        2
    )

    return total_weighted_avg


def conf_logger(level):
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    formatter = logging.Formatter(
        '[%(asctime)s - %(name)s - %(levelname)s - module:%(filename)s#%(lineno)d '
        '- func: "%(funcName)s"] message: "%(message)s"'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(level)

    return logger

logger = conf_logger(logging.DEBUG)
