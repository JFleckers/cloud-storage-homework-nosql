# cloud-storage-homework-nosql
All the code written for this project is contained in experiment.py, and requires inserting your own access and secret keys

Running experiment.py will
1. Create a new S3 Bucket named "fleckenstein-my-experiment-bucket"
1. Create a new DynamoDB table named "ExperimentTable"
1. Loop through data 
    * Add experiment file to bucket and corresponding data entry from csv to the table
1. Query the table for experiemnt1, row 2 and print response

Images:
* account.png: shows account name and new user created, with censored key info
* boto3.png: shows local installation of boto3
* query_results.png: shows results of code query
