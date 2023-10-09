#!/usr/bin/env python3
from subprocess import Popen
from AnalyzerFunctions import delete_records
import time

def test_server_client():
    server = Popen(["python3", "MockDatacollector.py"])
    time.sleep(5)

    try:
        response = delete_records("http://127.0.0.1:5100/")
        result = response.text
    except:
        result = "fail"
    
    server.kill()
    assert (result == "tested deletion! success!")

if __name__ == "__main__":
    test_server_client()