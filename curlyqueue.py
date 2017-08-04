#!/usr/bin/env python
import json
import requests
import sys
import boto3
from argparse import ArgumentParser

def curlyqueue(queue):
    fail_count = 0
    messages = []
    for test in queue:
        url = test.get("url")
        if not url:
            print("No url given")
            sys.exit(1)
        print(url)

        response = requests.get(url)

        code = test.get("code")
        if code:
            output = "  Status code: expected {}, actual {}".format(code, response.status_code)
            print(output)
            if code != response.status_code:
                fail_count += 1
                messages.append(output)

    return {"fail_count": fail_count, "messages": messages}


def lambda_handler(event, context):
    s3 = boto3.resource("s3")
    s3.Bucket(event.get("bucket")).download_file(event.get("key"), "/tmp/config.json")
    with open("/tmp/config.json") as configf:    
            config = json.load(configf)
    results = curlyqueue(config)
    if results.get("fail_count") > 0:
        if os.environ.get("OUTPUTTOPIC"):
            region_name = context.invoked_function_arn.split(":")[3]
            account_id = context.invoked_function_arn.split(":")[4]
            sns_topic_name = os.environ.get("OUTPUTTOPIC")
            sns_topic_arn = "arn:aws:sns:{}:{}:{}".format(region_name, account_id, sns_topic_name)
            sns.publish(TopicArn=sns_topic_arn, Message="\n".join(results.get("messages")), 
                Subject="curlyqueue failures", MessageStructure='string')


if __name__ == "__main__":
    parser = ArgumentParser("Curlyqueue")
    parser.add_argument("-c", "--config", help="Config file")
    parser.add_argument("-l", "--lambda_debug", default=False, action="store_true",
                        help="Run using lambda_handler to debug")
    parser.add_argument("-b", "--bucket", help="Bucket for use with lambda_debug")
    parser.add_argument("-k", "--key", help="Key for use with lambda_debug")

    args = parser.parse_args()

    if args.lambda_debug:
        lambda_handler({"bucket": args.bucket, "key": args.key}, None)
    elif args.config:
        with open(args.config) as configf:    
            config = json.load(configf)
        print("\nFailures: {}".format(curlyqueue(config).get("fail_count")))
    else:
        print("Invalid arguments")
