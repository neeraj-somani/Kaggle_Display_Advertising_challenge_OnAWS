from aws_cdk import (
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    core,
    ec2,
    ecs
    ecs_events
    s3
    aws_events_targets
    aws_s3_assets

)

#import * as path from path
import producer from producer_construct

class MainStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Not sure about purpose of below line, hence commenting out
        assetBasePath = './'
        #path.join(__dirname, '..', '..'); # this is typescript language

        ## Data Lake for Bidrequest store
        rawBucket = s3.Bucket(self, 'BidRequestExperimentStorage', {
      versioned: true,
      encryption: s3.BucketEncryption.S3_MANAGED
    });

        # ====================================
        # Creation of the Ingestion layer
        '''
        Need to create Ingestion layer first because it is used by ECS fargate and 
        fargate will only run if it can find Igention layer, 
        because we add dependancy to avoid issues
        '''
        # ====================================

        ingestion = Ingestion(self, 'IngestionLayer', bucket = rawBucket)

        ## Creation of the Fargate producer layer
        producer = Producer(self, 'ProducerLayer', 
          #assetBasePath,
          streamName = ingestion.ingestionStream.deliveryStreamName || 'undefined',
          streamArn = ingestion.ingestionStream.attrArn,
        )
        producer.node.addDependency(ingestion);



        




        