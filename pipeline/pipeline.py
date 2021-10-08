from aws_cdk import core as cdk
from aws_cdk.aws_codepipeline import Pipeline
from aws_cdk.pipelines import CodeBuildStep, CodePipeline, CodePipelineSource, ShellStep
from aws_cdk.aws_codecommit import IRepository, Repository
import aws_cdk.aws_iam as iam 

class PipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repository = Repository.from_repository_name(self, "Repository", "cdk-service-catalog")

        pipeline =  CodePipeline(self, "Pipeline", 
                        pipeline_name="ServiceCatalog",
                        synth=CodeBuildStep("Synth",
                            role_policy_statements=[
                                iam.PolicyStatement(
                                    actions=["cloudformation:GetTemplate", 
                                             "cloudformation:DeleteChangeSet", 
                                             "cloudformation:CreateChangeSet",
                                             "cloudformation:DescribeChangeSet", 
                                             "cloudformation:ExecuteChangeSet", 
                                             "cloudformation:DescribeStackEvents"],
                                    resources=["arn:aws:cloudformation:*:703965850448:stack/*/*"]
                                )],                                                                 
                            input=CodePipelineSource.code_commit(repository,
                            branch="master",                     
                            code_build_clone_output=True),
                            commands=["npm install -g aws-cdk", 
                                "python -m pip install -r requirements.txt", 
                                "cdk synth"]
                        )
                    )
