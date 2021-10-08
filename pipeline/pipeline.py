from aws_cdk import core as cdk
from aws_cdk.aws_codepipeline import Pipeline
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from aws_cdk.aws_codecommit import IRepository, Repository

class PipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

#        repository = Repository(repository_name="cdk-service-catalog")

        pipeline =  CodePipeline(self, "Pipeline", 
                        pipeline_name="ServiceCatalog",
                        synth=ShellStep("Synth",                                     
                            #input=CodePipelineSource.git_hub("klang/cdk-service-catalog", "master"),
                            input=CodePipelineSource.code_commit(repository=Repository.from_repository_name(self, id="repository", repository_name="cdk-service-catalog"),
                            branch="master",
                            code_build_clone_output=True),
                            commands=["npm install -g aws-cdk", 
                                "python -m pip install -r requirements.txt", 
                                "cdk synth"]
                        )
                    )
