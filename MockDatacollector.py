#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/delete_records", methods=["GET"])
def delete_records():
    return "tested deletion! success!"

if __name__ == "__main__":
    print("running mock data collector server!")
    app.run(port=5100)
