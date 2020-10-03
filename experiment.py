"""
Author: James Fleckenstein
jpf47@pitt.edu
"""

import boto3
import csv

access_key_id = ""
secret_access_key = ""


# load s3
s3 = boto3.resource("s3", aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

# create bucket
try:
    s3.create_bucket(Bucket="fleckenstein-my-experiment-bucket", CreateBucketConfiguration={
        "LocationConstraint": "us-west-2"
    })
except:
    print("This may already exist")

bucket = s3.Bucket("my-experiment-bucket")
#bucket.Acl().put(ACL="public-read")

# grab the dynamo resource
dyndb = boto3.resource("dynamodb", region_name="us-west-2", aws_access_key_id=access_key_id,
                       aws_secret_access_key=secret_access_key)

# create a new table
table = dyndb.create_table(
    TableName="ExperimentTable",
    KeySchema=[
        {
            "AttributeName": "PartitionKey",
            "KeyType": "HASH"
        },
        {
            "AttributeName": "RowKey",
            "KeyType": "RANGE"
        }
    ],
    AttributeDefinitions=[
        {
            "AttributeName": "PartitionKey",
            "AttributeType": "S"
        },
        {
            "AttributeName": "RowKey",
            "AttributeType": "S"
        }
    ],
    ProvisionedThroughput={
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }
)

# make sure the table is done being created before we contiune
table.meta.client.get_waiter("table_exists").wait(TableName="ExperimentTable")
print(table.item_count)

# location of the new public bucket
url = "https://s3-us-west-2.amazonaws.com/fleckenstein-my-experiment-bucket/"

# read all the csv data
with open("experiment_data.csv", "r") as file:
    c = csv.reader(file, delimiter=",", quotechar="|")
    # insert all csv data into the table
    for i in c:
        with open(i[3], "rb") as exp:
            s3.Object("fleckenstein-my-experiment-bucket", i[3]).put(Body=exp)
            s3.Object("fleckenstein-my-experiment-bucket", i[3]).Acl().put(ACL="public-read")
            insert = {
                'PartitionKey': i[0],
                'RowKey': i[1],
                'date': i[2],
                'comment': i[4],
                'url': url+i[3]
            }
            try:
                table.put_item(Item=insert)
            except:
                print("Item could not be inserted")

# test with a query
check = table.get_item(
    Key={
        "PartitionKey": "experiment1",
        "RowKey": "2"
    }
)
print(check["Item"])
