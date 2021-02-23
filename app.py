#!/usr/bin/env python3

from aws_cdk import core

from display_advertising_challenge.display_advertising_challenge_stack import DisplayAdvertisingChallengeStack


app = core.App()
DisplayAdvertisingChallengeStack(app, "display-advertising-challenge", env={'region': 'us-west-2'})

app.synth()
