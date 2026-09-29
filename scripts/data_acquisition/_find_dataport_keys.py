# -*- coding: utf-8 -*-
import os
import boto3
from botocore.config import Config

for k in list(os.environ):
    if "proxy" in k.lower():
        os.environ.pop(k, None)
s3 = boto3.session.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
).client("s3", config=Config(region_name="us-east-1", signature_version="s3v4"))

paginator = s3.get_paginator("list_objects_v2")
for page in paginator.paginate(Bucket="ieee-dataport", Prefix="data/"):
    for obj in page.get("Contents", []):
        k = obj["Key"]
        if "Event_Data" in k or "FO_Dataset" in k or "FO_dataset" in k or "14bus_data" in k:
            print(k, obj["Size"])
