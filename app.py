#!/usr/bin/env python3

# SQLAlchemy postgresql connection: https://vsupalov.com/flask-sqlalchemy-postgres/

import os
import requests
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import psycopg2

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

class Artpieces(db.Model):
    __tablename__ = 'artpieces'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    image_id = db.Column(db.Text, nullable = True)
    dimensions_detail = db.Column(db.Text, nullable = True)

## ANALYSIS: analysis functions
class analysis_functions:
    ## ANALYSIS: returns API address for the thumbnail image given an art work id
    def get_iif(self, identifier):
        return f"https://www.artic.edu/iiif/2/{identifier}/full/843,/0/default.jpg"

    ## ANALYSIS: helper function
    def get_volume_string(self, detail):
        return str(detail['depth_cm'] * detail['width_cm'] * detail['height_cm'])

    ## ANALYSIS: helper function
    def get_area_string(self, detail):
        return str(detail['width_cm'] * detail['height_cm'])

    ## ANALYSIS: returns list of parts of the artwork and their calculated volumes or areas
    def get_dimensions_detail(self, details):
        # raise NotImplementedError
        toReturn = []
        for i in json.loads(details):
            # print(type(i['depth_cm'])) # it's int
            isVolume = True if i['depth_cm'] != 0 else False
            if isVolume:
                toReturn.append({ 'part_name': i['clarification'], 'processed' : "Volume: " + self.get_volume_string(i) + " cm^3" } )
            else:
                toReturn.append({ 'part_name': i['clarification'], 'processed' : "Area: " + self.get_area_string(i) + " cm^2" } )

        # print(type(toReturn))
        return toReturn

    ## ANALYSIS: data processing entry point
    def ArtpiecesJson(self, rows):
        tempList = []
        for i in rows:
            data = { 
                'id': i.id,
                'name': i.name,
                'image_link': self.get_iif(i.image_id),
                'dimensions_detail': self.get_dimensions_detail(i.dimensions_detail)
            }
            tempList.append(data)
        return json.dumps(tempList)

AnalysisFunctions = analysis_functions()

@app.route("/retrieve_records", methods=["GET"])
def send_records():
    artworks = db.session.query(Artpieces).all()
    # process database output and send it out as JSON
    return AnalysisFunctions.ArtpiecesJson(artworks)

@app.route("/delete_records/<mock>", methods=["GET"])
def delete_records(mock):
    if mock == "default":
        response = requests.get(datacollector_addr + "delete_records")
    else:
        response = requests.get("http://127.0.0.1:5100/delete_records")

    return "deleted! " + str(response.status_code)

def delete_records_integration_test():
    response = requests.get("http://127.0.0.1:5100/" + "delete_records")
    return "deleted! " + str(response.status_code)

@app.route("/scrape", methods=["GET"])
def scrape():
    response = requests.get(datacollector_addr + "scrape")
    return "data scraped! " + str(response.status_code)

if __name__ == "__main__":
    print("hello world!")
    datacollector_addr = "http://127.0.0.1:5050/"
    app.run(port=5051)
    # test commit
