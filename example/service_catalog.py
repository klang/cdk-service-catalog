from aws_cdk import core as cdk
from aws_cdk.aws_servicecatalog import CloudFormationTemplate, Portfolio, CloudFormationProduct, CloudFormationProductVersion

from aws_cdk import core


class ServiceCatalogStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        portfolio = Portfolio(self, "ExamplePortfolio", description="Example", display_name="Example", provider_name="LocalAdmin")
                             
        version1=CloudFormationProductVersion(product_version_name="v1.0", description="ReadOnlyAccess", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./example/products/AccountSpecificTrustRoleReadOnlyAccess.yaml"))
        version2=CloudFormationProductVersion(product_version_name="v1.1", description="AdministratorAccess", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./example/products/AccountSpecificTrustRole.yaml"))

        product = CloudFormationProduct(self, "IamRoles", 
                                        owner="LocalAdmin", 
                                        product_name="TemporaryRole", 
                                        product_versions=[version1]) #version2 can not be inserted here, without getting an error
                                        
        portfolio.add_product(product)

