import requests
import os
from dateutil.rrule import rrule, DAILY, MO, WE
import datetime as dt
from datetime import timedelta

#Gets Token information and Organization ID
def get_token():
	url = "https://api.robinpowered.com/v1.0/auth"
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response = requests.request("GET", url, headers=headers)
	print(response.text)
  
#Add organization ID to get information about your organization
def get_org (Organization_ID):
	url = "https://api.robinpowered.com/v1.0/organizations/{Organization_ID}"
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response = requests.request("GET", url, headers=headers)
	print(response.text)

#add username or user ID to the username query to find a specific username
def get_users():
	url = "https://api.robinpowered.com/v1.0/organizations/{organization_id}/users?ids={user ID}" # insert user ID or query=username
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response = requests.request("GET", url, headers=headers)
	print(response.text)
  
#Get user's future seat reservation
def get_user_seat(user_id):
	url = "https://api.robinpowered.com/v1.0/reservations/seats/?user_ids={user_id}&include_disabled_seats=false"
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response = requests.request("GET", url, headers=headers)
	print(response.json())

#Get user's seat information based on their reservation ID
def get_reservation():
	url = "https://api.robinpowered.com/v1.0/reservations/seats/{reservation ID}" 
	key = os.environ.get("robin_api_key")
	headers = {"Accept": "application/json","Authorization": "Access-Token "+ key}
	response = requests.request("GET", url, headers=headers)
	print(response.text)

#Set seat with user and seat IDs, feel free to change date/time of reservation. 
#Also, if statement is for looping a number of dates, you can ignore it if setting one specific date
def set_seat(dt, seat_id, user_id):
	url = f"https://api.robinpowered.com/v1.0/seats/{seat_id}/reservations" 
	key = os.environ.get("robin_api_key")
	payload = {
	    "start": {
	        "date_time": dt + "T04:00:00Z",
	        "time_zone": "UTC"
	    },
	    "end": {
	        "date_time": dt + "T16:00:00Z",
	        "time_zone": "UTC"
	    },
	    "reservee": {"user_id": f"{user_id}"},
	    "type": "hoteled",
	    "reserver_id": f"{user_id}"
	}
	headers = {
	    "Accept": "application/json",
	    "Content-Type": "application/json",
	    "Authorization": "Access-Token " + key
	}

	response = requests.request("POST", url, json=payload, headers=headers)
	if response.json()["meta"]["status_code"] == "200":
		print(f"seat assigned sucessfully")
		return True
	else:
		print(f"seat already assigned for {dt}")
		return False

#gets all Mondays and Wedensdays of the month.can be changed to your favorite dates.
def get_all_dates():
	lst_dates = []
	results = rrule(DAILY,
        dtstart = dt.datetime.today(),
        until = dt.datetime.today() + timedelta(days=30),
        byweekday = (MO, WE),
)
	for result in results:
		lst_dates.append(str(result.date()))
	return lst_dates[::-1]


#starting point of program
date_cond = True
all_dates_lst = get_all_dates()
for date in all_dates_lst:
	if date_cond == True:
		print(f"setting seat for {username} at {date}")
		date_cond = set_seat(date, {seat_id}, {user_id})
	else:
		print("All dates assigned, exiting program")
		date_cond = True
		break
print("program ended")
