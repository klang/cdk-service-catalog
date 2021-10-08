
# Welcome to your CDK Python project!

This is a blank project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!


{
    "repositoryMetadata": {
        "accountId": "703965850448",
        "repositoryId": "3e5e1326-cae6-43e5-b444-a69270e0aa94",
        "repositoryName": "cdk-service-catalog",
        "lastModifiedDate": "2021-10-07T16:13:19.347000+02:00",
        "creationDate": "2021-10-07T16:13:19.347000+02:00",
        "cloneUrlHttp": "https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/cdk-service-catalog",
        "cloneUrlSsh": "ssh://git-codecommit.eu-west-1.amazonaws.com/v1/repos/cdk-service-catalog",
        "Arn": "arn:aws:codecommit:eu-west-1:703965850448:cdk-service-catalog"
    }
}
(END)


# trust

https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.pipelines/README.html#context-lookups

    cdk bootstrap --trust-for-lookup=703965850448
    
    export CDK_NEW_BOOTSTRAP=1
    cdk bootstrap --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess aws://703965850448/eu-west-1

        pipeline =  CodePipeline(self, "Pipeline", 
                        pipeline_name="ServiceCatalog",
                        synth=CodeBuildStep("Synth",                                     
                            #input=CodePipelineSource.git_hub("klang/cdk-service-catalog", "master"),
                            input=CodePipelineSource.code_commit(repository=Repository.from_repository_name(self, id="repository", repository_name="cdk-service-catalog"),
                            branch="master",
                            
                            code_build_clone_output=True),
                            commands=["npm install -g aws-cdk", 
                                "python -m pip install -r requirements.txt", 
                                "cdk synth"]
                        )
                    )





