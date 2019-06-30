import requests
import pytest
import json
import http.client
import logging
import jsonschema
from jsonschema import validate


logging.basicConfig(filename='API_test.log',level=logging.INFO)
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)
requests_log=logging.getLogger("request.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
header = {"content/type" : "application/json", "charset": "UFT-8"}
Base_url= "https://jsonplaceholder.typicode.com"


@pytest.mark.TestID(ID="ATC001")
def test_get_req1():
    "verify the get request for 1st problem"
    response= requests.get(Base_url+"/posts",headers=header)#--using request lib for get request
    status = response.status_code#using request lib taking out the code from the response
    data = response.json()#using request lib taking out the json data from the response

    schema = {
        "type" : "object",
        "properties" : {
            "userId" : {"type" : "number"},
            "Id" : {"type" : "number"},
            "title" : {"type" : "string"},
            "body" : {"type" : "string"}
        },
    }
    assert (status,len(data)) == (200,100)# asserting the response code and  record i.e 100 records json input response
    for item in data:  #iterating through 100 records and checking the schema for all records
        try:
            validate(item, schema)
            #sys.stdout.write("Record #{}: OK\n".format(item))
        except jsonschema.exceptions.ValidationError as ve:
            print("Record #{}: ERROR\n".format(item))
            pytest.fail(str(ve), pytrace=True) # failing the test when schema fail

@pytest.mark.TestID(ID="ATC002")
def test_get_req2():
    "verify the get request for 2nd problem"
    response= requests.get(Base_url+"/posts/1",headers=header)#--using request lib for get request
    status = response.status_code #using request lib taking out the code from the response
    data = response.json()#using request lib taking out the json data from the response
    schema = {
        "type" : "object",
        "properties" : {
            "userId" : {"type" : "number"},
            "Id" : {"type" : "number"},
            "title" : {"type" : "string"},
            "body" : {"type" : "string"}
        },
    }

    assert (status,len(list(data))) == (200,4)# asserting the response code and only one record i.e 4 keys in one json input response

    assert 1 == data['id'] #assert the id contains "1" in value
    try:
        validate(data, schema)# using jsonschema lib comparing response schema
        #sys.stdout.write("Record #{}: OK\n".format(item))
    except jsonschema.exceptions.ValidationError as ve:
        print("Record #{}: ERROR\n".format(data))
        pytest.fail(str(ve), pytrace=True) # failing the test when exception

@pytest.mark.TestID(ID="ATC003")
def test_get_req3():
    "verify the get request for 3rd problem"
    response= requests.get(Base_url+"/invalidposts",headers=header)#get method
    status = response.status_code
    data = response.json()
    assert status == 404 # asserting the 404 response code # detail log for troubleshoot is saved as API_test.log in file path

@pytest.mark.TestID(ID="ATC004")
def test_get_req4():
    "verify  the post request for 4th problem"
    ## payload body
    body={
        "title" : "foo" ,
        "body" : "bar" ,
        "userId" : 1
    }
    response = requests.post(Base_url+"/posts",json=body,headers=header)#post method
    status = response.status_code
    data= response.json()
    assert (status, data['id'], data["title"], data["userId"])==(201, 101, "foo", 1)# asserting the response code and created data through post method.
    schema = {
        "type" : "object",
        "properties" : {
            "title" : {"type" : "string"},
            "body" : {"type" : "string"},
            "userId" : {"type" : "number"},
            "id" : {"type" : "number"}
        },
    }

    try:
        validate(data, schema)# using jsonschema lib comparing response schema
        #sys.stdout.write("Record #{}: OK\n".format(item))
    except jsonschema.exceptions.ValidationError as ve:
        print("Record #{}: ERROR\n".format(data))
        pytest.fail(str(ve), pytrace=True)


@pytest.mark.TestID(ID="ATC005")
def test_get_req5():
    "verify the put request for 5th problem"
    body={
        "id" : 1 ,
        "title" : "abc" ,
        "body" : "xyz" ,
        "userId" : 1
    }
    response = requests.put(Base_url+"/posts/1",json=body,headers=header)#put method
    status = response.status_code
    data= response.json()
    print(data)
    assert (status, data['id'], data["title"], data["userId"], data["body"])==(200, 1, "abc", 1,"xyz")#asserting the response code and updated record.

    schema = {
        "type" : "object",
        "properties" : {
            "id" : {"type" : "integer"},
            "title" : {"type" : "string"},
            "body" : {"type" : "string"},
            "userId" : {"type" : "number"}
        },
    }

    try:
        validate(data, schema)# using jsonschema lib comparing response schema
            #sys.stdout.write("Record #{}: OK\n".format(item))
    except jsonschema.exceptions.ValidationError as ve:
        print("Record #{}: ERROR\n".format(data))
        pytest.fail(str(ve), pytrace=True)


@pytest.mark.TestID(ID="ATC006")
def test_get_req6():
    "verify the delete request for 6th problem"
    response = requests.delete(Base_url+"/posts/1", headers=header)# delete method
    status = response.status_code
    data= response.json()
    assert (status,data)==(200,{}) #asserting the response code and response data.





