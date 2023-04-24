#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_service_catalog.cdk_service_catalog_stack import CdkServiceCatalogStack
#from pipeline.pipeline import PipelineStack

app = cdk.App()
#PipelineStack(app, "PipelineStack")

CdkServiceCatalogStack(app, "CdkServiceCatalogStack")

app.synth()
