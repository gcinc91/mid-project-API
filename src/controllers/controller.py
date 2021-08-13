from src.app import app
from flask import Flask, request
from src.database import insert_data, fetch_all, find_by_date, find_by_country, process_data



@app.route("/data/insert", methods=['POST'])
def insert():
    res = insert_data()
    return res


@app.route("/data/fetchall", methods=['GET'])
def fetch():
    res = fetch_all()
    return res


@app.route("/data/fetch-by-date", methods=['GET'])
def find_date():
    date = request.args.get('date')
    res = find_by_date(date)
    return res

@app.route("/data/fetch/<country>", methods=['GET'])
def find_country(country):
    res = find_by_country(country)
    return res


@app.route("/process", methods=['GET'])
def process():
    res = process_data()
    return res