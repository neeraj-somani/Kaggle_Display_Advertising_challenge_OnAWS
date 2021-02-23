from aws_cdk import (
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    core,
    aws_s3_assets as S3Asset,
)

import * as path from 'path';

def getLambdaBaseCommand(functionName: string, payload = '{}') -> string :
	return 'aws lambda invoke --function-name ${functionName} --payload '${payload}' /tmp/out --log-type Tail --query 'LogResult' --output text'


class Producer(core.Construct):
	

	def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        print('this is default path: ', path)
        # Assets to upload to s3 bucket
	    # https://docs.aws.amazon.com/cdk/api/latest/docs/aws-s3-assets-readme.html
	    bidrequestsData = S3Asset.Asset(self, 'Advertising_BidRequestsData', {
	      path: path.join('data', 'bidrequests.txt')
	    });

	    print('this is the path created before VPC : ', path.join('data', 'bidrequests.txt'))


	    # ====================================
        # Producer declaration below, launch is done through a lambda function
        # ====================================


	    # ====================================
        # VPC
        # ====================================
        vpc = aws_ec2.Vpc(self,
            id='DisplayAdvChallenge_vpc',
            cidr='10.0.0.0/16',
            max_azs=2,
            nat_gateways=1,
            vpn_gateway=False
        )


        # ====================================
        # ECS
        # ====================================
        # Create ecs cluester.
        ecs_cluster = aws_ecs.Cluster(
            self,
            id='DisplayAdvChallenge_ecs_cluster',
            cluster_name='sample_fargate_batch_cluster',
            vpc=vpc
        )


        # Create fargate task definition.
        fargate_task_definition = aws_ecs.FargateTaskDefinition(
            self,
            id='DisplayAdvChallenge_ProducerTaskDefinition',
            cpu=256,
            memory_limit_mib=512,
            family='fargate-task-definition'
        )

        # Add container to task definition.
        fargate_task_definition.add_container(
            id='DisplayAdvChallenge_container',
            image=aws_ecs.ContainerImage.from_Asset('producer'),
            logging=aws_ecs.LogDriver.aws_logs(
                stream_prefix='DisplayAdvChallenge_ecs',
                log_group=aws_logs.LogGroup(
                    self,
                    id='DisplayAdvChallenge_log_group',
                    log_group_name='/ecs/fargate/fargate-batch'
                )
            ),
            environment={
                'S3_BUCKET_NAME': bidrequestsData.s3BucketName,
        		'S3_OBJECT_KEY': bidrequestsData.s3ObjectKey,
        		'STREAM_NAME': props.streamName,
            },
        )

        ## Grant task access to new uploaded assets
    	bidrequestsData.grantRead(taskDefinition.taskRole);













