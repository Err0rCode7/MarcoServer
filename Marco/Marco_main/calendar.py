from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'static/json/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

def get_schedule():


    # Call the Calendar API
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    today = datetime.datetime.today() #
    KST = datetime.timezone(datetime.timedelta(hours=9)) # timezone 설정변수 UTC+9 
    # now : 현재시간 -2 날짜 객체
    
    hour = today.hour
    if hour < 2 :
        hour = 0
    else :
        hour = hour - 2
    now = datetime.datetime(today.year, today.month, today.day, hour, today.minute, today.second, tzinfo=KST)
    nowformat= now.isoformat()
    #print(now.hour+2)
    # 현재 시각-2부터 가까운 순으로 3개 추출 
    events_result = service.events().list(calendarId='primary', timeMin=nowformat,
                                        maxResults=3, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    #print(events[0]['start'])
    schedule = []
    if not events:
        return False
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        #print(start, event['summary'])
        schedule.append((start[5:7],start[8:10],start[11:13],start[14:16],start[17:19],event['summary']))
    return schedule
