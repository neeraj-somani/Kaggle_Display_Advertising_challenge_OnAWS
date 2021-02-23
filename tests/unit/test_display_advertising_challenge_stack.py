import json
import pytest

from aws_cdk import core
from display_advertising_challenge.display_advertising_challenge_stack import DisplayAdvertisingChallengeStack


def get_template():
    app = core.App()
    DisplayAdvertisingChallengeStack(app, "display-advertising-challenge")
    return json.dumps(app.synth().get_stack("display-advertising-challenge").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
