import datetime
import time
import requests
import schedule
from pymongo import MongoClient

COMPANIES = ('Apple', 'Google', 'Amazon', 'Tesla')
GET_BODY = False

DB_NAME = "companynews"
DB_HOST = "mongodb://localhost:27017/"

client = MongoClient(DB_HOST)
db = client[DB_NAME]
collection = db['collection']


def get_daily_company_info():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    daily_info = {}
    for company in COMPANIES:
        res = requests.get('http://localhost:5000/company_articles', params={
            'company': company, 'get_body': GET_BODY,
            'start_date': yesterday.strftime('%Y-%m-%d'), 'end_date': today.strftime('%Y-%m-%d')
        })
        daily_info[company] = res.json()
    return daily_info


def save_daily_info():
    daily_info = get_daily_company_info()
    today = datetime.date.today()
    _id = today.strftime('%Y-%m-%d')
    daily_info['_id'] = _id
    collection.update_one({'_id': _id}, {'$set': daily_info}, upsert=True)


if __name__ == "__main__":
    schedule.every().day.at("12:00").do(save_daily_info)

    while True:
        schedule.run_pending()
        time.sleep(300)
