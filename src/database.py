from pymongo import MongoClient
import pandas as pd
import os
from dotenv import load_dotenv
from src.helpers.json_response import json_response
load_dotenv()

client = MongoClient(os.getenv('DB_URL'))
db = client.cov19_db
collection = db.countries


def insert_data():

    df_conf = pd.read_csv("./data/confirmed_global.csv")
    df_dea = pd.read_csv("./data/deaths_global.csv")
    df_re = pd.read_csv("./data/recovered_global.csv")

    """
    Insertar los primeros datos con los pacientes confirmados en funcion de la fecha
    """
    records_to_insert = []
    for i in range(len(df_conf)):
        r = {
            'Province/State': df_conf.iloc[i]['Province/State'],
            'Country/Region': df_conf.iloc[i]['Country/Region'],
            'Lat': float(df_conf.iloc[i]['Lat']),
            'Long': float(df_conf.iloc[i]['Long'])
        }
        
        for prop, val in df_conf.iloc[i].iteritems():
            if prop not in ['Province/State','Country/Region','Lat','Long']:
                records_to_insert.append({
                    **r,
                    "date": prop,
                    "confirmed": int(val)
                    })

    collection.insert_many(records_to_insert)
    

    """
    Actualizacion de los datos añadiendole las muertes confirmadas en funcion de la fecha
    """
    for i in range(len(df_dea)):
        for prop, val in df_dea.iloc[i].iteritems():
            if prop not in ['Province/State','Country/Region','Lat','Long']:
                print(prop, val)
                collection.update_one({
                    'Province/State': df_dea.iloc[i]['Province/State'],
                    'Country/Region': df_dea.iloc[i]['Country/Region'],
                    'date': prop
                    },{"$set": {"deaths": int(val)}})


    """
    Actualizacion de los datos añadiendole los casos de recuperacion confirmadas en funcion de la fecha
    """

    for i in range(len(df_re)):
        for prop, val in df_re.iloc[i].iteritems():
            if prop not in ['Province/State','Country/Region','Lat','Long']:
                print(prop, val)
                collection.update_one({
                    'Province/State': df_re.iloc[i]['Province/State'],
                    'Country/Region': df_re.iloc[i]['Country/Region'],
                    'date': prop
                    },{"$set": {"recovered": int(val)}})

    return "Done!"

def fetch_all():

    try:
        all_countries = list(collection.find())
        return json_response(all_countries)

    except Exception as err:
        print(f' Something went wrong --> {err}')

def find_by_date(date):

    try:
        all_countries = list(collection.find({"date": date}))
        return json_response(all_countries)

    except Exception as err:
        print(f' Something went wrong --> {err}')


def find_by_country(country):

    try:
        all_countries = list(collection.find({'Country/Region': country}))
        return json_response(all_countries)

    except Exception as err:
        print(f' Something went wrong --> {err}')


def process_data():

    """
    Funcion para poner en minuscula el nombre de los paises y provicias y poner la fecha en formato DD/M/AA
    """

    try:
        all_countries = collection.find()
        he = all_countries[98826:]
        
        for i in he:
            query= {}
            if type(i['Province/State']) == str:
                query['Province/State'] = i['Province/State'].lower()
            query['Country/Region'] = i['Country/Region'].lower()
            new_date = i['date'].split('/')
            print('LAQ --> ',query)
            try:
                collection.update_one({
                        'Province/State': i['Province/State'],
                        'Country/Region': i['Country/Region'],
                        'date': i['date']
                        },{"$set": {**query, 'date': f'{new_date[1]}/{new_date[0]}/{new_date[2]}' }})
            except:
                print('error with***********-->', quey, date)
                continue
        return 'Done!'

    except Exception as err:
        print(f' Something went wrong --> {err}')