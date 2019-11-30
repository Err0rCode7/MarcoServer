from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

def uploding_file(filename):
    try:
        import argparse
        #flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        flags = tools.argparser.parse_args([])
    except ImportError:
        flags = None

    # Setup the Drive v3 API
    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        print("make new storage data file")
        flow = client.flow_from_clientsecrets('static/json/client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run_flow(flow, store)

    DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

    metadata = {'name': filename, 'mimeType': None}
    res = DRIVE.files().create(body=metadata, media_body=filename).execute()
    if res:
        return('Uploaded "%s" (%s)' % (filename, res['mimeType']))
