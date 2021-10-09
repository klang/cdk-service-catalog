from aws_cdk import core as cdk
from aws_cdk.aws_iam import PrincipalPolicyFragment
from aws_cdk.aws_s3_assets import Asset
from aws_cdk.aws_s3 import Bucket, CfnBucket
from aws_cdk.aws_servicecatalog import CloudFormationTemplate, Portfolio, CloudFormationProduct, CloudFormationProductVersion, CfnCloudFormationProduct
from aws_cdk.aws_servicecatalog import CfnCloudFormationProduct as cfnp
from aws_cdk.aws_servicecatalog import CfnPortfolioProductAssociation

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class CdkServiceCatalogStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    
        portfolio = Portfolio(self, "Portfolio", description="Nice Helpers", display_name="Nice Helpers", provider_name="Conscia")

        # we could create a function or a class that does this, but seriously .. we already have a class hieracy that's supposed to handle this
        v1 = [CloudFormationProductVersion(product_version_name="v1.0", 
                                           validate_template=False, 
                                           cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/UserSpecificTrustRole.yaml"))]
        p1 = CloudFormationProduct(self, "UserSpecificTrustRole", 
                                        owner="Conscia", 
                                        product_name="temporary-trusted-user", 
                                        description="TemporaryUserTrust to Conscia",
                                        product_versions=v1)
                                        
        portfolio.add_product(p1)

        #It's not yet possible to have two versions of a product
        # will result in 
        # jsii.errors.JSIIError: There is already a Construct with name 'Template' in CloudFormationProduct [AccountTrustRole]
        # also         
        #  the individual versions can not be assigned a description
        p2v1=CloudFormationProductVersion(product_version_name="v1.0", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/AccountSpecificTrustRole.yaml"))
        p2v2=CloudFormationProductVersion(product_version_name="v1.1", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/AccountSpecificTrustRoleReadOnlyAccess.yaml"))
       
        p2 = CloudFormationProduct(self, "AccountTrustRole", 
                                        owner="Conscia", 
                                        product_name="temporary-trusted-account", 
                                        description="v1.0 - TemporaryAccountTrust to Conscia",
                                        product_versions=[p2v1])
                                        # product_versions=[p2v1, p2v2] would have been nice
        p21 = CloudFormationProduct(self, "AccountSpecificTrustRoleReadOnlyAccess", 
                                        owner="Conscia", 
                                        product_name="temporary-trusted-account-read-only", 
                                        description="v1.1 - TemporaryAccountTrust to Conscia",
                                        product_versions=[p2v2])
                                        
        #portfolio.add_product(p2)
        #portfolio.add_product(p21)

        # it's not possible to make a product, with two versions in the way we would expect above, so we try it this way
        # the following lines and p21 can be replaced by `product_versions=[p2v1, p2v2]` in the definition of p2, when
        # CloudFormationProduct is adjusted to support more versions.
        a1 = Asset(self, "AccountSpecificTrustRoleAsset", path="./cdk_service_catalog/products/AccountSpecificTrustRole.yaml")
        a2 = Asset(self, "AccountSpecificTrustRoleReadOnlyAccessAsset", path="./cdk_service_catalog/products/AccountSpecificTrustRoleReadOnlyAccess.yaml")
        
        p3 = cdk.CfnResource(self, "p3", type="AWS::ServiceCatalog::CloudFormationProduct",
                properties={"Name": "temporary-trusted-account",
                            "Owner": "Conscia",
                            "Description": "TemporaryAccountTrust to Conscia",
                            "ProvisioningArtifactParameters": [
                                {
                                    "Description": "AdministratorAccess",
                                    "DisableTemplateValidation": False,
                                    "Name": "v1.0",
                                    "Info": {"LoadTemplateFromURL": a1.http_url}
                                },
                                {
                                    "Description": "ReadOnlyAccess",
                                    "DisableTemplateValidation": False,
                                    "Name": "v1.1",
                                    "Info": {"LoadTemplateFromURL": a2.http_url}
                                }
                                ],
                            }
                    )
        
        
        p3association = CfnPortfolioProductAssociation(self, "p3association", 
            portfolio_id=portfolio.portfolio_id, product_id=p3.ref)

        #portfolio.add_product(CloudFormationProduct.from_product_arn(self, "p3arn", p3.get_att("ProvisioningArtifactIds")))


        v4 = [CloudFormationProductVersion(product_version_name="v1.0", 
                                           validate_template=False, 
                                           cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/MultiAccountTrustRole.yaml"))]
        p4 = CloudFormationProduct(self, "MultiAccountTrustRole", 
                                        owner="Conscia", 
                                        product_name="temporary-trusted-accounts", 
                                        description="TemporaryAccountTrust to several accounts",
                                        product_versions=v4)
                                        
        portfolio.add_product(p4)

        asset1 = Asset(self, "vpc-and-linux", path="./cdk_service_catalog/products/simple-vpc-and-linux-instance.yaml")
        asset2 = Asset(self, "vpc-and-linux-ssm", path="./cdk_service_catalog/products/simple-vpc-and-linux-instance-with-ssm.yaml")
        asset3 = Asset(self, "vpc-and-linux-ssm-only", path="./cdk_service_catalog/products/simple-vpc-and-linux-instance-with-ssm-only.yaml")
        p5 = cdk.CfnResource(self, "p5", type="AWS::ServiceCatalog::CloudFormationProduct",
                properties={"Name": "vpc-and-linux",
                            "Owner": "Conscia",
                            "Description": "Simple VPC with Linux instance",
                            "ProvisioningArtifactParameters": [
                                {
                                    "Description": "VPC with Linux with public ssh access",
                                    "DisableTemplateValidation": False,
                                    "Name": "v1.0",
                                    "Info": {"LoadTemplateFromURL": asset1.http_url}
                                },
                                {
                                    "Description": "VPC with Linux with access through ssm",
                                    "DisableTemplateValidation": False,
                                    "Name": "v1.1",
                                    "Info": {"LoadTemplateFromURL": asset2.http_url}
                                },
                                {
                                    "Description": "VPC with Linux with access through ssm only",
                                    "DisableTemplateValidation": False,
                                    "Name": "v1.2",
                                    "Info": {"LoadTemplateFromURL": asset3.http_url}
                                }
                                ],
                            }
                    )
        
        
        p5association = CfnPortfolioProductAssociation(self, "p5association", 
            portfolio_id=portfolio.portfolio_id, product_id=p5.ref)
        