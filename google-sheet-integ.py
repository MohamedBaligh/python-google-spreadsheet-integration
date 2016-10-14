from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags= None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE ='client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():

	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir,'.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credentials_path = os.path.join(credential_dir,'sheets.googleapis.com-python-quickstart.json')

	store = Storage(credentials_path)
	credentials =store.get()
	if not credentials or credentials.invalid:
		flow= client.flow_from_clientsecrets(CLIENT_SECRET_FILE,SCOPES)
		flow.user_agent=APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow,store,flags)
		else: 
			credentials = tools.run(flow,store)
		print('Storing credentials to ' +credentials_path)
	return credentials

def main():
	credentials= get_credentials()
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
					 'version=v4')
	service = discovery.build('sheets', 'v4', http=http,
								discoveryServiceUrl=discoveryUrl)

	spreadsheetId='1d-UgfOOKQGiN2i69hsY7u4Im0MA71przg5tpJmhBHOw'
	rangeName = 'A2:C2'
	result = service.spreadsheets().values().get(
			spreadsheetId=spreadsheetId, range=rangeName).execute()
	values =result.get('values', [])

	if not values:
		print('No data found')
	else:
		print('ColumnHeading, ColumnHeading2:')
		for row in values:
			print('%s, %s' % (row[0], row[2]))


	values =[
		["items","cost","stock","location","end"],
		["abc","def","ghi","jkl","mno"],
	]
	body ={
		'values':values
	}
	range_name='A1:E1'
	value_input_option = 'RAW'

	result = service.spreadsheets().values().append(
		spreadsheetId=spreadsheetId, range=range_name,
		valueInputOption=value_input_option, body=body).execute()


if __name__ =='__main__':
	main()
