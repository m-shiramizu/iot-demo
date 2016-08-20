# -*- coding: utf-8 -*-

import ConfigParser
from gcloud import storage
from gcloud.storage import Blob

configfile = ConfigParser.SafeConfigParser()
configfile.read("./config/config.ini")

UPLOAD_BUCKET = configfile.get("gcs","upload_bucket") 
PROJECT_ID = configfile.get("gcs","project_id")
UPLOAD_FILE = configfile.get("gcs","upload_file")
OUTPUT_FILE = configfile.get("gcs","output_file")

PIN = int(configfile.get("sensor","pin"))
INTERVAL = float(configfile.get("sensor","interval"))
SHUTTER_DISTANCE = int(configfile.get("sensor","shutter_distance"))

client = storage.Client(project=PROJECT_ID)
bucket = client.get_bucket(UPLOAD_BUCKET)
blob = Blob(OUTPUT_FILE, bucket)
with open(UPLOAD_FILE, 'rb') as my_file:
  blob.upload_from_file(my_file)
