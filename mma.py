import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from googleapiclient.errors import HttpError
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1stAvOore5Bgyx5jhPEN5p7fsAT-mmQihbDdYFORdI9k'
SAMPLE_RANGE_NAME = 'C2:CC5'
Score_Range = 'B2:B5'
Winner_Range = 'C2:CC2'
Scott_Range = 'C5:CC5'
Josh_Range = 'C3:CC3'
Hunter_Range = 'C4:CC4'

def main():
	"""Shows basic usage of the Sheets API.
	Prints values from a sample spreadsheet.
	"""
	creds = None
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.json', 'w') as token:
			token.write(creds.to_json())

	try:
		service = build('sheets', 'v4', credentials=creds)

		# Call the Sheets API
		sheet = service.spreadsheets()
		result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
									range=SAMPLE_RANGE_NAME).execute()
		values = result.get('values', [])

		if not values:
			print('No data found.')
			return
		a = []
		for row in values:
			# Print columns A and E, which correspond to indices 0 and 4.
	
			a.append(row)
		#print(a)
		print(len(a[0]))
		Winner_Score = 0
		Scott_Score = 0
		Josh_Score = 0 
		Hunter_Score = 0
		players = 3
		for x in range(0,players+1):
			for i in range(len(a[0])):
				if(a[x][i].strip() == a[0][i].strip() and a[0][i] != "" ): #and a==[0][i] != " "
						if(x == 0):
							Winner_Score +=1
						if(x == 1):
							Josh_Score +=1
							#print(a[0][i])
						if(x == 2):
							Hunter_Score +=1 
						if (x== 3):
							#print(a[0][i])
							Scott_Score +=1
		print("WINNER SCORE " + str(Winner_Score))
		print("JOSH SCORE " + str(Josh_Score))
		print("HUNTER SCORE " + str(Hunter_Score))
		print("SCOTT SCORE "  + str(Scott_Score)) 
		batch_update_values_request_body = {
			"valueInputOption": "RAW",
			"data": [
				{
					'range': 'Sheet1!B2:B5',
					'values': [[Winner_Score],[Josh_Score],[Hunter_Score],[Scott_Score]]				}

			]
		}
		send = sheet.values().batchUpdate(
			spreadsheetId=SPREADSHEET_ID,
			body = batch_update_values_request_body
			).execute()
	except HttpError as err:
			print(err)
	


if __name__ == '__main__':
	main()