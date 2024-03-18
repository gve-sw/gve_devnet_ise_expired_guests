# Copyright (c) 2023 Cisco and/or its affiliates.

# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at

#                https://developer.cisco.com/docs/licenses

# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

from time import sleep
import requests
import json
from dotenv import load_dotenv
import os
requests.packages.urllib3.disable_warnings()
from datetime import date

# load all environment variables
load_dotenv()
BASE_URL = 'https://' + os.getenv('ISE_IP') + ':9060/ers/config'
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

# set headers for API calls
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
users_list=[]

# Get all expired guest users
def get_all_guests(guests_endpoint):
    try:
        response=requests.get(guests_endpoint,
                headers=HEADERS, auth=(USERNAME, PASSWORD),
                verify=False).json()
        
        
        if response["SearchResult"]["total"] != 0:
            for guest in response["SearchResult"]["resources"]:
                if len(users_list) < 5000:
                    user_entry={}
                    user_entry["name"]=guest["name"]
                    user_entry["id"]=guest["id"]
                    users_list.append(user_entry)

            if len(response["SearchResult"]["resources"]) < 100:
                print()
            elif response["SearchResult"]["nextPage"]:
                guests_endpoint=response["SearchResult"]["nextPage"]["href"]
                get_all_guests(guests_endpoint)
          
            delete_in_bulk(users_list)
            
        else:
            print("No Expired Guest Users")
    except Exception as e:
            print("Unable to retrieve guest users")
            print("This is the exception: " + str(e))


def delete_in_bulk(users_list):
    try:
        endpoint="/guestuser/bulk/submit"
        ids_xml=''
        for id in users_list:
            ids_xml=ids_xml+f'<id>{id["id"]}</id>'

        #Add the ID's to the full XML payload 
        payload='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <ns4:guestUserBulkRequest operationType="delete" resourceMediaType="vnd.com.cisco.ise.identity.guestuser.2.0+xml" xmlns:ns6="sxp.ers.ise.cisco.com" xmlns:ns5="trustsec.ers.ise.cisco.com" xmlns:ns8="network.ers.ise.cisco.com" xmlns:ns7="anc.ers.ise.cisco.com" xmlns:ers="ers.ise.cisco.com" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:ns4="identity.ers.ise.cisco.com"><idList>{}</idList></ns4:guestUserBulkRequest>'''.format(ids_xml)

        HEADERS = {
            "Content-Type": "application/xml",
            "Accept": "application/xml"
        }   
        response = requests.put(BASE_URL+endpoint,
                headers=HEADERS, auth=(USERNAME, PASSWORD),
                data=payload, verify=False)
       
        response_status=int(response.status_code)
        if response_status==202:
            bulkId=str(response.headers["Location"])
            check_bulk_request_status(bulkId,users_list)
        else:
            print("Delete Bulk Reuest was not accepted")
            print(response_status)
    except Exception as e:
            print("Unable to delete guest users")
            print("This is the exception: " + str(e))

def check_bulk_request_status(bulkID,users_list):
    try: 
        thebulkId=bulkID.split('/')
        thebulkId=thebulkId[len(thebulkId)-1]

        endpoint= f"/guestuser/bulk/{thebulkId}"   
        response = requests.get(BASE_URL+endpoint,
                        headers=HEADERS, auth=(USERNAME, PASSWORD),
                        verify=False).json()
      
        today= date.today()
        d1 = today.strftime("%d/%m/%Y")
        d1=d1.replace("/", "-")
                    
        logs_path= f'./logs/{d1}.txt'
        check_file= os.path.isfile(logs_path)
        if check_file:
            logs_file = open(logs_path, "a")
        else:
            logs_file = open(logs_path, "x")
                    
        if response["BulkStatus"]["executionStatus"]=="COMPLETED":
            for resource in response["BulkStatus"]["resourcesStatus"]:
                    
                    if resource["status"] and resource["resourceExecutionStatus"]=="SUCCESS":
                        
                        for user in users_list:
                            if resource['id']==user['id']:
                                status=f"Guest User {user['name']} with ID {resource['id']} deleted successfully\n"
                                print(status)
                                logs_file.write(status)
                    else:
                        status=f"Guest User {user['name']} with ID {resource['id']} couldn't be deleted"
                        print(status)
                        logs_file.write(status)
        else:
            print("Delete Bulk Request is not yet compelete")
            sleep(30)
            check_bulk_request_status(bulkID, users_list)
        logs_file.close()
    except Exception as e:
        # print("Unable to check bulk status")
        # print("This is the exception: " + str(e))
        print()


if __name__ == "__main__":
    get_all_guests(BASE_URL+"/guestuser?size=100&filter=status.CONTAINS.EXPIRED")
