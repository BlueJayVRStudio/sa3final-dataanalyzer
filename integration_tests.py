#!/usr/bin/env python3
from subprocess import Popen
from app import delete_records
import time

def test_server_client():
    server = Popen(["python3","MockDatacollector.py"])
    time.sleep(5)
    try:
        result = delete_records("test")
    except:
        result = "fail"
    
    server.kill()
    assert (result == "deleted! 200")

if __name__ == "__main__":
    test_server_client()