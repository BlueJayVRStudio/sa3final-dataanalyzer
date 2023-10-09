#!/usr/bin/env python3
from subprocess import Popen
from AnalyzerFunctions import delete_records
import time

def test_server_client():
    server = Popen(["python3", "MockDatacollector.py"])
    time.sleep(5)

    try:
        response = delete_records("http://127.0.0.1:5100/")
        result = "deleted! " + str(response.status_code)
    except:
        result = "fail"
    
    server.kill()
    assert (result == "deleted! 200")

if __name__ == "__main__":
    test_server_client()