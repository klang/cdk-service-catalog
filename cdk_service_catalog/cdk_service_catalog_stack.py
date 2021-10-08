from aws_cdk import core as cdk
from aws_cdk.aws_s3_assets import Asset
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_servicecatalog import CloudFormationTemplate, Portfolio, CloudFormationProduct, CloudFormationProductVersion, CfnCloudFormationProduct

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class CdkServiceCatalogStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #bucket = Bucket(self, "ProductBucket", bucket_name="703965850448-cdk-service-catalog")
#       AccountSpecificTrustRole.yaml
#       AccountSpecificTrustRoleReadOnlyAccess.yaml
#       MultiAccountTrustRole.yaml
#       UserSpecificTrustRole.yaml
#       simple-vpc-and-linux-instance-with-ssm-only.yaml
#       simple-vpc-and-linux-instance-with-ssm.yaml
#       simple-vpc-and-linux-instance.yaml
# 
    # asset = Asset(self, "UserSpecificTrustRole", path="./cdk_service_catalog/products/UserSpecificTrustRole.yaml")
        portfolio = Portfolio(self, "Portfolio", description="Nice Helpers", display_name="Nice Helpers", provider_name="Conscia")

        v1 = [CloudFormationProductVersion(product_version_name="v1.0", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/UserSpecificTrustRole.yaml"))]
        p1 = CloudFormationProduct(self, "UserSpecificTrustRole", 
                                        owner="Conscia", 
                                        product_name="temporary-trusted-user", 
                                        description="TemporaryUserTrust to Conscia",
                                        product_versions=v1)
                                        
        portfolio.add_product(p1)

        # p2v1 = CfnCloudFormationProduct(self, "p2v1", 
        #                                         name="temporary-trusted-accoutn", 
        #                                         owner="Conscia", 
        #                                         description="TemporaryAccountTrust to Conscia",
        #                                         provisioning_artifact_parameters=[
        #                                             CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty(name="v1.0",description="AdministratorAccess",disable_template_validation=False, info= {})
        #                                         ])
        # CfnCloudFormationProduct.ProvisioningArtifactPropertiesProperty.description


        #It's not yet possible to have two versions of a product
        # will result in 
        # jsii.errors.JSIIError: There is already a Construct with name 'Template' in CloudFormationProduct [AccountTrustRole]
        # also         
        #  the individual versions can not be assigned a description
        #v2 = [CloudFormationProductVersion(product_version_name="v1.0", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/AccountSpecificTrustRole.yaml")),
        #      #CloudFormationProductVersion(product_version_name="v1.1", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/AccountSpecificTrustRoleReadOnlyAccess.yaml")),
        #]
        p2v1=CloudFormationProductVersion(product_version_name="v1.0", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/AccountSpecificTrustRole.yaml"))
        p2v2=CloudFormationProductVersion(product_version_name="v1.1", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/AccountSpecificTrustRoleReadOnlyAccess.yaml"))
       
        p2 = CloudFormationProduct(self, "AccountTrustRole", 
                                        owner="Conscia", 
                                        product_name="temporary-trusted-account", 
                                        description="TemporaryAccountTrust to Conscia",
                                        product_versions=[p2v1])
                                        # product_versions=[p2v1, p2v2] would have been nice
        p21 = CloudFormationProduct(self, "AccountSpecificTrustRoleReadOnlyAccess", 
                                        owner="Conscia", 
                                        product_name="temporary-trusted-account-read-only", 
                                        description="TemporaryAccountTrust to Conscia",
                                        product_versions=[p2v2])
                                        
        portfolio.add_product(p2)
        portfolio.add_product(p21)



