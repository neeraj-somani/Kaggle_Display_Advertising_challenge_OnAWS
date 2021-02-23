#!/usr/bin/env python3

from aws_cdk import core

from display_advertising_challenge.main_stack import MainStack


app = core.App()
#DisplayAdvertisingChallengeStack(app, "display-advertising-challenge", env={'region': 'us-west-2'})

MainStack(app, "display-advertising-challenge", env={'region': 'us-west-2'})
app.synth()
