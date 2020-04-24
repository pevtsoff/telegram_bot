from src import telegram_api

def telegram_lambda(event, context):
    telegram_api.main()