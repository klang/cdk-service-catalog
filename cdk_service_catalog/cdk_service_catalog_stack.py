import aws_cdk as cdk
from aws_cdk.aws_servicecatalog import CloudFormationTemplate, Portfolio, CloudFormationProduct, CloudFormationProductVersion

from constructs import Construct
from .products.s3_bucket_product import S3BucketProduct

class CdkServiceCatalogStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
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

        p2v1=CloudFormationProductVersion(product_version_name="v1.0", description="AdministratorAccess", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/AccountSpecificTrustRole.yaml"))
        p2v2=CloudFormationProductVersion(product_version_name="v1.1", description="ReadOnlyAccess", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/AccountSpecificTrustRoleReadOnlyAccess.yaml"))

        p2 = CloudFormationProduct(self, "AccountTrustRole", 
                                        owner="Conscia", 
                                        product_name="temporary-trusted-account", 
                                        description="TemporaryAccountTrust to Conscia - either ReadOnlyAccess or AdministratorAccess",
                                        product_versions=[p2v1, p2v2])
                                        
        portfolio.add_product(p2)

        v4 = [CloudFormationProductVersion(product_version_name="v1.0", 
                                           validate_template=False, 
                                           cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/MultiAccountTrustRole.yaml"))]
        p4 = CloudFormationProduct(self, "MultiAccountTrustRole", 
                                        owner="Conscia", 
                                        product_name="temporary-trusted-accounts", 
                                        description="TemporaryAccountTrust to several accounts",
                                        product_versions=v4)
                                        
        portfolio.add_product(p4)

        p5v1=CloudFormationProductVersion(product_version_name="v1.0", description="VPC with Linux with public ssh access", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/simple-vpc-and-linux-instance.yaml"))
        p5v2=CloudFormationProductVersion(product_version_name="v1.1", description="VPC with Linux with access through ssm", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/simple-vpc-and-linux-instance-with-ssm.yaml"))
        p5v3=CloudFormationProductVersion(product_version_name="v1.2", description="VPC with Linux with access through ssm only", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/simple-vpc-and-linux-instance-with-ssm-only.yaml"))

        p5 = CloudFormationProduct(self, "VPCandLinux",
                                owner="Conscia",
                                product_name="simple-vpc-and-linux",
                                description="Simple VPC with Linux instance",
                                product_versions=[p5v1, p5v2, p5v3])
        portfolio.add_product(p5)

        # https://cloudpartners.atlassian.net/wiki/spaces/DEV/pages/1964572677/billing+alarm
        p6v1=CloudFormationProductVersion(product_version_name="v1.0", description="Training Budget", validate_template=False, cloud_formation_template=CloudFormationTemplate.from_asset(path="./cdk_service_catalog/products/TrainingCostBudget.yaml"))
        p6 = CloudFormationProduct(self, "TrainingBudget",
                                owner="Conscia",
                                product_name="training-budget",
                                description="Training Budget with notifications at $5,$10,$25 and $45 for individual developer accounts.",
                                product_versions=[p6v1])
        portfolio.add_product(p6)

        p7v1=CloudFormationProductVersion(product_version_name="v1.0", description="S3 Budget", validate_template=False, 
            cloud_formation_template=CloudFormationTemplate.from_product_stack(S3BucketProduct(self, "S3BucketProduct")))

        p7 = CloudFormationProduct(self, "Product",owner="Conscia", product_name="S3 Bucket", product_versions=[p7v1])
        portfolio.add_product(p7)