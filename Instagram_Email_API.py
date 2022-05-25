from google.oauth2 import service_account
from google.oauth2.credentials import Credentials 
from googleapiclient.discovery import build


SERVICE_ACCOUNT_FILE = 'ig_email_key.json' #json File should be in the same folder as this Python Script.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1sU7IhpRAYVKTss3MZyjlrEiUaiMsPANG_Q4LdK2BhC4' #Emails Collected - In Google Drive (blackgamer367@gmail.com)
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

def GrabAPI_Usernames(everybody_usernames_listt):
        # Call the Sheets API
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range='Emails!A2:A4000').execute()
        values = result.get('values', []) #Pulls the list into a list of list


        everybody_usernames_listt = [item for sublist in values for item in sublist]
        #^ Takes it out of a list of list and forms it into a regular list
        #How to get the info from values then turn the list of list into a regulat list

        return (everybody_usernames_listt)
#If used ^ Make sure a list is created then assign that same list to this function when called upon. 
#THE_LIST = []
#Ex: THE_LIST = GrabAPI_Usernames(THE_LIST)

def UpdateAPI_Usernames(everybody_usernames_listt):
        everybody_usernames_listt = ((list(map(lambda el:[el], everybody_usernames_listt))))
        global SAMPLE_SPREADSHEET_ID
        request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID, 
                                        range = 'Emails!A2:A4000', valueInputOption='USER_ENTERED', body={'values': everybody_usernames_listt}).execute()






#so Id have to convert it back to a list of each string being in a list


#Final


