import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


 # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google Developers Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the Developers Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_READ_WRITE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))


def update_video(youtube, options):

	videos_list_response = youtube.videos().list(
		id=options.video_id,
		part='snippet'
	).execute()

	if not videos_list_response["items"]:
		print "Video '%s' not found." % options.video_id
		sys.exit(1)

	videos_list_snippet = videos_list_response["items"][0]["snippet"]

	if "tags" not in videos_list_snippet:
		videos_list_snippet["tags"]=[]
	videos_list_snippet["tags"].append(options.tag)


	#This is to update the description
	videos_list_snippet['description'] ="this is the description"


	video_update_response = youtube.videos().update(
		part='snippet',
		body=dict(
			snippet=videos_list_snippet,
			id=options.video_id
		)).execute()


	#this is code for changing the PrivacyStatus
	videos_list_status = youtube.videos().list(
		id=options.video_id,
		part='status'
	).execute()


	videos_list_status["items"][0]["status"]["privacyStatus"] = 'public'

	videos_update_response = youtube.videos().update(

		part= 'status',
		body=dict(
			status=videos_list_status,
			id=options.video_id
		)).execute()


	



if __name__ == "__main__":
	argparser.add_argument("--video_id", help="Video ID of the youtube video",
		required="true")

	argparser.add_argument("--tag", default="hello",help="Additional tag to be added")

	args = argparser.parse_args()

	youtube = get_authenticated_service(args)
	try:
		update_video(youtube, args)
	except HttpError, e:
		print "HTTP Error"
	else:
		print "Tag '%s' was added" % args.tag


