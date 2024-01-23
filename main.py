"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
# Imports
import requests
import json
from dotenv import load_dotenv
import os
requests.packages.urllib3.disable_warnings() # Disable warnings for testing purposes
from apscheduler.schedulers.background import BlockingScheduler

# Load in Environment Variables
load_dotenv()
BASE_URL = 'https://' + os.getenv('ISE_IP') + ':9060/ers/config'
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
SCHEDULER_DAILY_MIN = int(os.environ['SCHEDULER_DAILY_MIN'])


# Set headers for API calls
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Get all expired guest users
def get_all_guests():
    guests_endpoint="/guestuser/?filter=status.CONTAINS.EXPIRED"
    try:
        response=requests.get(BASE_URL+guests_endpoint,
                headers=HEADERS, auth=(USERNAME, PASSWORD),
                verify=False).json()
        ids=[]
        if response["SearchResult"]["total"] != 0:
            for guest in response["SearchResult"]["resources"]:
                ids.append(guest["id"])
            delete_guests(ids)   
        else:
            print("No Expired Guest Users")
    except Exception as e:
            print("Unable to retrieve guest users")
            print("This is the exception: " + str(e))

# Delete all expired guest users
def delete_guests(IDs):
    for id in IDs:
        guests_endpoint= f"/guestuser/{id}"
        try:
            response=requests.delete(BASE_URL+guests_endpoint,
                    headers=HEADERS, auth=(USERNAME, PASSWORD),
                    verify=False)
            if response.status_code == 204:
                print(f"Guest User with ID {id} deleted successfully")
            else:
                print(f"Unable to delete Guest User with ID {id}")
        except Exception as e:
            print("Unable to delete guest users")
            print("This is the exception: " + str(e))


# Schedule the process to run automatically 
def scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(get_all_guests, 'interval',minutes=SCHEDULER_DAILY_MIN)
    scheduler.start()

if __name__ == "__main__":
    scheduler()
