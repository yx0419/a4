# awsServices

This application uses multiple AWS services including S3, DynamoDB, EC2. Server-side code was written using Flask and Boto3.
This website has three functions: 'Load Data', 'Clear Data', two input text boxes labled First name and Last name, and a 'Query'.

When the “Load Data” button is hit, the website will load data from an object stored at a given URL from Amazon S3. 

User can copy this data into Object his/her own storage (S3). This will parse and load data into a <Key, Value> NoSQL store (Dynamo DB).
When the “Clear Data” button is hit the object is removed from the object store. The NoSQL table is also emptied or removed.


How to run the program:
python3 app.py 

Location of the URL:
http://ec2-54-202-50-153.us-west-2.compute.amazonaws.com/


S3 Storage:
https://s3.console.aws.amazon.com/s3/buckets/bucket436/?region=us-west-2&tab=overview

database:

https://us-west-2.console.aws.amazon.com/dynamodb/home?region=us-west-2#tables:

https://us-west-2.console.aws.amazon.com/dynamodb/home?region=us-west-2#tables:selected=yunTable;tab=overview  (after created a table named “yunTable”)

Website is hosted on EC2, so the hosting will be carried out by Amazon, and Amazon will automatically scale the load. 

