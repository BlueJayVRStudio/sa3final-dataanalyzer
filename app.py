#!/usr/bin/env python3

# SQLAlchemy postgresql connection: https://vsupalov.com/flask-sqlalchemy-postgres/

import os
import requests
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import psycopg2

from AnalyzerFunctions import analysis_functions
from AnalyzerFunctions import delete_records as deleteRecords

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = f"environment variable '{name}' not set."
        raise Exception(message)

POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")
AIC_API = "https://api.artic.edu/api/v1/artworks"
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
datacollector_addr = "http://34.118.228.146:5050/"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

db = SQLAlchemy(app)


datacollector_addr = "http://34.118.228.146:5050/"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

db = SQLAlchemy(app)

class Artpieces(db.Model):
    __tablename__ = 'artpieces'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    image_id = db.Column(db.Text, nullable = True)
    dimensions_detail = db.Column(db.Text, nullable = True)

AnalysisFunctions = analysis_functions()

@app.route("/retrieve_records", methods=["GET"])
def send_records():
    artworks = db.session.query(Artpieces).all()
    # process database output and send it out as JSON
    return AnalysisFunctions.ArtpiecesJson(artworks)

@app.route("/delete_records", methods=["GET"])
def delete_records():
    print(datacollector_addr)
    response = deleteRecords(datacollector_addr)
    return response.text

@app.route("/scrape", methods=["GET"])
def scrape():
    response = requests.get(datacollector_addr + "scrape")
    return "data scraped! " + str(response.status_code)

if __name__ == "__main__":
    print("hello world!")
    datacollector_addr = "http://127.0.0.1:5050/"
    app.run(port=5051)
    # test commit
