# Service Catalog Portfolio

This `setup.yaml` Cloudformation template sets up a "minimal viable product" version of the [awslabs ServiceCatalog](https://github.com/awslabs/aws-cloudformation-templates/tree/master/aws/services/ServiceCatalog)

# Environment

Let's set up the environment in a `training` account. The `account-id` is used to create an unique S3Bucket for the products.

    awsume training
    account=$(aws sts get-caller-identity --query 'Account' --output text)
    S3Bucket="${account}-service-catalog-products"

    aws s3 mb s3://${account}-service-catalog-products
    aws s3 sync products/ s3://${S3Bucket}/
    aws s3 ls s3://${S3Bucket}/

Now, we ensure that the `setup.yaml` template is valid and either create or update the stack.

    aws cloudformation validate-template --template-body file://setup.yaml
    aws cloudformation create-stack --stack-name ServiceCatalogPortfolio --template-body file://setup.yaml --parameters ParameterKey=S3Bucket,ParameterValue=${S3Bucket}
    aws cloudformation update-stack --stack-name ServiceCatalogPortfolio --template-body file://setup.yaml --parameters ParameterKey=S3Bucket,ParameterValue=${S3Bucket}

Before any of the products can be used, you need to add your group, role or user to the list of users that are have access to the portfolio.

This is done under [ServiceCatalog -> Administration -> Portfolios](https://eu-west-1.console.aws.amazon.com/servicecatalog/home?region=eu-west-1#portfolios?activeTab=localAdminPortfolios). Select the portfolio and press "Add groups, roles, users".

It is possible to add this part of the portfolio configuration in `setup.yaml` but that's not the focus of this "minimal viable product".

# Another Product

To add "Another Product" to the portfolio

Upload a new CloudFormation template to the appropriate bucket

    aws s3 cp AnotherProduct.yaml s3://${S3Bucket}/AnotherProduct.yaml

Add the following to `setup.yaml`, adjusted to the situation at hand

    ProductAnotherPortfolio:
      Type: AWS::ServiceCatalog::PortfolioProductAssociation
      Properties:
        AcceptLanguage: en
        PortfolioId: !Ref Portfolio
        ProductId: !Ref ProductAnother
  
    ProductAnother:
      Type: "AWS::ServiceCatalog::CloudFormationProduct"
      Properties:
        Description: "Another Product description"
        Name: "another-product"
        Owner: "Conscia"
        ProvisioningArtifactParameters:
          - Description: "short-description-of-another-product"
            DisableTemplateValidation: false
            Name: "v1.0"
            Info:
              LoadTemplateFromURL: !Sub "https://s3-${AWS::Region}.amazonaws.com/${S3Bucket}/AnotherProduct.yaml"

Update the stack
    
     aws cloudformation update-stack --stack-name ServiceCatalogPortfolio --template-body file://setup.yaml

