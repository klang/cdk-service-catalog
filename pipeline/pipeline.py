import aws_cdk as cdk
from aws_cdk.pipelines import CodeBuildStep, CodePipeline, CodePipelineSource
from aws_cdk.aws_codecommit import Repository

from constructs import Construct

class PipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repository = Repository.from_repository_name(self, "Repository", "cdk-service-catalog")

        pipeline =  CodePipeline(self, "Pipeline", 
                        pipeline_name="ServiceCatalog",
                        synth=CodeBuildStep("Synth",                                                               
                            input=CodePipelineSource.code_commit(repository,
                            branch="master",                     
                            code_build_clone_output=True),
                            commands=[
                                "npm install -g aws-cdk", 
                                "python -m pip install -r requirements.txt", 
                                "cdk synth"]
                        )
                    )
