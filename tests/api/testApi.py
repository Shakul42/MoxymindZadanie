import os
import re
import time
import json


# 1st TC: GET - List Users and 
def test_get_list_users(playwright):
    request_context = playwright.request.new_context(base_url="https://reqres.in/api/")
    response = request_context.get("users?page=2")
    assert response.status == 200
    json_response = response.json()
    assert "data" in json_response
#  Test for last names of first two users
    first_surname = json_response["data"][0]["last_name"]
    assert first_surname == "Lawson"
    second_surname = json_response["data"][1]["last_name"]
    assert second_surname == "Ferguson"

#  Test of total users
    total = json_response["total"]
    # Not best solution if ids are unique and not recycled when user is deleted
    #total_id = json_response["data"][-1]["id"]  # Getting last id 
    #assert total_id == total    #Check if last id is equal to total users

    # In this case page 2 is last one, otherwise new API call with last page should be made
    nr_ids = len(json_response["data"])     #Number of ids on last page 
    total_pages = json_response["total_pages"]
    per_page = json_response["per_page"]
    count_total = ((total_pages-1) * per_page) + nr_ids
    assert count_total == total

#  Test of data types of returned values
    assert isinstance(json_response["data"], list)
    assert isinstance(json_response["page"], int)
    assert isinstance(json_response["total"], int)
    assert isinstance(json_response["per_page"], int)
    assert isinstance(json_response["total_pages"], int)

    request_context.dispose()

# 2nd TC: POST - Create an user.
def test_post_create_user(playwright):
    request_context = playwright.request.new_context(base_url="https://reqres.in/api/")
    # Instead of hardcoded token, on pipeline it should be provided from CI secrets storage
    token = os.getenv("REQRES_TOKEN", "reqres-free-v1")
    payload = {"name": "morpheus", "job": "leader"}
    start_time = time.time()
    response = request_context.post(
        "users",    #endpoint
        headers={
            "x-api-key": token,
            "Content-Type": "application/json"
        },
        data=json.dumps(payload)
    )
    end_time = time.time()
    time_diff = (end_time - start_time) * 1000  # In miliseconds
    print(f"Time taken for POST create user API call: {time_diff/1000} seconds")
    #expect.soft(time_diff < 200)   # Soft assertion NOT built-in in Pytest Playwright
    for i in range(1):  # Loop for Form of soft assertion
        try:
            assert time_diff < 200
        except Exception as e:
            #print(e)
            print("Response time exceeded 200 ms")
            continue
    assert time_diff < 500, "Response time exceeded 500 ms"  # Hard assertion, test will fail if >500ms
    
    assert response.status == 201   # Test for HTTP response code 201 Created
    json_response = response.json()
    print(json_response)

    # Validate POST create user response schema
    _validate_create_user_schema(json_response)

    # Checking returned values if same as sent in payload
    assert json_response.get("name") == "morpheus"
    assert json_response.get("job") == "leader"

    request_context.dispose()

def _validate_create_user_schema(resp_json):
    assert "name" in resp_json and isinstance(resp_json["name"], str), "Missing or invalid 'name'"
    assert "job" in resp_json and isinstance(resp_json["job"], str), "Missing or invalid 'job'"
    assert "id" in resp_json and isinstance(resp_json["id"], str), "Missing 'id'"   # Double test for id being string
    assert isinstance(resp_json["id"], (str, int)), f"Unexpected type for 'id': {type(resp_json['id'])}"
    assert "createdAt" in resp_json and isinstance(resp_json["createdAt"], str), "Missing or invalid 'createdAt'"
    # Datetime check in format of (YYYY-MM-DDTHH:MM:SS.mmmZ)
    time_format = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z"
    assert re.search(time_format, resp_json["createdAt"]), "createdAt doesn't have format like expected timestamp"