from aws_cdk import (aws_s3 as s3)
from aws_cdk.aws_servicecatalog import (ProductStack)
from constructs import Construct

class S3BucketProduct(ProductStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        s3.Bucket(self, "BucketProduct")
