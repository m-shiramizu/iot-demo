# -*- coding: utf-8 -*-

from gcloud import storage
from gcloud.storage import Blob

client = storage.Client(project='my-project')
bucket = client.get_bucket('my-bucket')
encryption_key = 'aa426195405adee2c8081bb9e7e74b19'
blob = Blob('secure-data', bucket)
with open('my-file', 'rb') as my_file:
  blob.upload_from_file(my_file,encryption_key=encryption_key)
