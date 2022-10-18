# @see https://www.middlewareinventory.com/blog/aws-lambda-terraform/
# @see https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html
import json
import boto3
import os


def create_report(event: dict, context):
    sts = boto3.client(
        service_name='sts',
    )
    period = event.get('period', 14)
    account_id = event.get('account_id', '')
    severity_labels = [{"Value": label, "Comparison": "EQUALS"}
                       for label in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']]

    try:
        caller = sts.get_caller_identity().get('Account')
    except Exception as err:
        caller = str(err)

    account_client = boto3.client('account')
    client = boto3.client(
        service_name='securityhub',
        region_name='eu-central-1',
        endpoint_url='http://localstack:4566',
        use_ssl=False,
        aws_access_key_id='test',
        aws_secret_access_key='test'
    )

    try:
        findings = client.get_findings(Filters={
            "RecordState": [{
                "Value": "Active",
                "Comparison": "EQUALS"
            }],
            "LastObservedAt": [{
                "DateRange": {
                    "Value": period,
                    "Unit": "DAYS"
                }
            }],
            "AwsAccountId": [{
                "Value": account_id,
                "Comparison": "EQUALS"
            }],
            "SeverityLabel": severity_labels

        })
    except Exception as err:
        findings = str(err)
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': {
            "environ": dict(os.environ),
            "identity": caller,
            "findings": findings
        }
    }
