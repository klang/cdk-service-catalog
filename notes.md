# SharedService Service Catalog Delegated master

## ServicePrincipals

Assume the role of the root account and list the EnabledServicePrincipals for the organization.

    (.venv) ➜  cdk-service-catalog git:(master) ✗ awsume controltower
    Session token will expire at 2022-09-06 19:40:17
    [controltower] Role credentials will expire 2022-09-06 11:58:01
    (.venv) ➜  cdk-service-catalog git:(master) ✗ aws organizations list-aws-service-access-for-organization
    {
        "EnabledServicePrincipals": [
            {
                "ServicePrincipal": "access-analyzer.amazonaws.com",
                "DateEnabled": "2021-02-04T10:12:58.228000+01:00"
            },
            {
                "ServicePrincipal": "config.amazonaws.com",
                "DateEnabled": "2021-08-18T14:01:34.042000+02:00"
            },
            {
                "ServicePrincipal": "controltower.amazonaws.com",
                "DateEnabled": "2020-01-28T10:10:39.219000+01:00"
            },
            {
                "ServicePrincipal": "fms.amazonaws.com",
                "DateEnabled": "2021-03-16T18:26:28.150000+01:00"
            },
            {
                "ServicePrincipal": "member.org.stacksets.cloudformation.amazonaws.com",
                "DateEnabled": "2020-02-18T14:53:58.069000+01:00"
            },
            {
                "ServicePrincipal": "ram.amazonaws.com",
                "DateEnabled": "2021-03-16T18:21:09.363000+01:00"
            },
            {
                "ServicePrincipal": "sso.amazonaws.com",
                "DateEnabled": "2020-01-28T10:11:23.295000+01:00"
            }
        ]
    }

Add few permissions to the list of EnabledServicePrincipals

    aws organizations enable-aws-service-access --service-principal servicecatalog.amazonaws.com
    aws organizations enable-aws-service-access --service-principal member.org.stacksets.cloudformation.amazonaws.com

And verify that the new ServicePrincipals are present

    aws organizations list-aws-service-access-for-organization

    (.venv) ➜  cdk-service-catalog git:(master) ✗ aws organizations list-aws-service-access-for-organization
    
    {
        "EnabledServicePrincipals": [
            {
                "ServicePrincipal": "access-analyzer.amazonaws.com",
                "DateEnabled": "2021-02-04T10:12:58.228000+01:00"
            },
            {
                "ServicePrincipal": "config.amazonaws.com",
                "DateEnabled": "2021-08-18T14:01:34.042000+02:00"
            },
            {
                "ServicePrincipal": "controltower.amazonaws.com",
                "DateEnabled": "2020-01-28T10:10:39.219000+01:00"
            },
            {
                "ServicePrincipal": "fms.amazonaws.com",
                "DateEnabled": "2021-03-16T18:26:28.150000+01:00"
            },
            {
                "ServicePrincipal": "member.org.stacksets.cloudformation.amazonaws.com",
                "DateEnabled": "2020-02-18T14:53:58.069000+01:00"
            },
            {
                "ServicePrincipal": "ram.amazonaws.com",
                "DateEnabled": "2021-03-16T18:21:09.363000+01:00"
            },
            {
                "ServicePrincipal": "servicecatalog.amazonaws.com",
                "DateEnabled": "2022-09-06T11:04:48.105000+02:00"
            },
            {
                "ServicePrincipal": "sso.amazonaws.com",
                "DateEnabled": "2020-01-28T10:11:23.295000+01:00"
            }
        ]
    }
    
## DelegatedAdministrators

Check the state of DelegatedAdministrators

    aws organizations list-delegated-administrators
    
    (.venv) ➜  cdk-service-catalog git:(master) ✗ aws organizations list-delegated-administrators
    
    {
        "DelegatedAdministrators": []
    }

Check that the organization has a `SharedServices` or `shared-services account`

    aws organizations list-accounts | grep -i shared

Note the account id

    delegated=$(aws organizations list-accounts | jq -r '.Accounts[] | select(.Name=="SharedServices") | .Id')
    echo $delegated

Register the SharedServices account as a delegated administrator

    aws organizations register-delegated-administrator --account-id $delegated --service-principal servicecatalog.amazonaws.com

Verify that it's been done

    aws organizations list-delegated-administrators
    
    (.venv) ➜  cdk-service-catalog git:(master) ✗ aws organizations list-delegated-administrators
    
    {
        "DelegatedAdministrators": [
            {
                "Id": "940740948575",
                "Arn": "arn:aws:organizations::588412859260:account/o-arh1cw6cp5/940740948575",
                "Email": "cp-controltower-shared-services@cloudpartners.com",
                "Name": "SharedServices",
                "Status": "ACTIVE",
                "JoinedMethod": "CREATED",
                "JoinedTimestamp": "2020-09-03T12:45:01.135000+02:00",
                "DelegationEnabledDate": "2022-09-06T11:06:30.673000+02:00"
            }
        ]
    }
    

# Create a Portfolio

    awsume shared-services
    export account_id=$(aws sts get-caller-identity --query Account --output text)
    export CDK_NEW_BOOTSTRAP=1
    cdk bootstrap --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess aws://$account_id/eu-west-1

    cdk synth
    #cdk deploy PipelineStack
    cdk deploy CdkServiceCatalogStack
    
    export portfolio=$(aws servicecatalog list-portfolios | jq -r '.PortfolioDetails[] | select(.DisplayName=="Nice Helpers") | .Id')
    echo $portfolio
    
    awsume controltower
    
    
    aws ssm put-parameter --name '/org/sharedservices/servicecatalog/sharedportfolioid' --value $portfolio --description 'Service Catalog shared portfolio id' --type String --overwrite

    export oid=$(aws organizations describe-organization --query Organization.Id --output text)
    echo $oid

    awsume shared-services
    aws servicecatalog create-portfolio-share --portfolio-id $portfolio  --organization-node Type=ORGANIZATION,Value=$oid



# aws-cli manipulations

awsume training
account=$(aws sts get-caller-identity --query=Account --output text)

awsume controltower
aws organizations describe-account --account-id $account


aws organizations list-roots --query 'Roots[*].Id' --output text
root=$(aws organizations list-roots --query 'Roots[*].Id' --output text)

aws organizations list-organizational-units-for-parent --parent-id $root

aws organizations list-organizational-units-for-parent --parent-id $root --query 'OrganizationalUnits[*].[Id,Name]' --output text
