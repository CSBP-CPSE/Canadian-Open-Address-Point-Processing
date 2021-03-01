"""
This is a .py version of the .ipy file prepared by Andrew
The idea is to have the input json file as a system argument, so it can be run with a shell script

Summary
Uses the OpenAddresses tooling to

download data based on a user-defined JSON source specification
save the data in a user-defined location in MinIO

"""

import json
import sys
import kfp
from kfp.components import load_component_from_file
from kfp import dsl

"""
Define input and output parameters
"""
minio_bucket_name = 'deil-lode'
json_source_file = "/home/jovyan/Processing/ODA/Source_Files/nl/happy-valley-goose-bay.json"
minio_tenant = 'minimal'
openaddresses_args = "--layer addresses --layersource city"
minio_output_uri = f'{minio_bucket_name}/ODA/OA_Processing/Output/nl'

"""Component/Pipeline definitions"""

openaddresses_get_op = load_component_from_file(
    "./components/openaddresses_get_data.yaml"
)
copy_to_minio_op = load_component_from_file(
    "./components/copy_to_minio.yaml"
)

@dsl.pipeline(
    name="Download OpenAddresses Data to Minio"
)
def pipeline(
    source_json,
    minio_output_uri: str,
    # TODO: Handle these automatically once multitenancy is available
    minio_url,
    minio_access_key: str,
    minio_secret_key: str,
    openaddresses_args: str = "",
):
    operations = {}

    operations['Get Data'] = openaddresses_get_op(
        source_json=source_json,
        args=openaddresses_args,
    ).set_image_pull_policy("Always")

    operations['Store Data'] = copy_to_minio_op(
        local_source=operations['Get Data'].outputs['data'],
        minio_destination=minio_output_uri,
        minio_url=minio_url,
        minio_access_key=minio_access_key,
        minio_secret_key=minio_secret_key,
        flags="--recursive",  # Because outputs['data'] is a directory
    )
    # Set all operations display names to their key in the operations dict
    for name, op in operations.items():
        op.set_display_name(name)
        
"""Load JSON source file"""

with open(json_source_file, 'r') as fin:
    source_json = json.load(fin)
    
"""Get MinIO credentials from the Notebook Server (could also specify these things manually)"""
# Get minio credentials using a helper
from utilities import get_minio_credentials

minio_settings = get_minio_credentials(minio_tenant, strip_http=False)
minio_url = minio_settings["url"]
minio_access_key = minio_settings["access_key"]
minio_secret_key = minio_settings["secret_key"]

arguments = dict(
    source_json=json.dumps(source_json),
    openaddresses_args=openaddresses_args,
    minio_output_uri=minio_output_uri,
    minio_url=minio_url,
    minio_access_key=minio_access_key,
    minio_secret_key=minio_secret_key,
)
# Get minio credentials using a helper
from utilities import get_minio_credentials

minio_settings = get_minio_credentials(minio_tenant, strip_http=False)
minio_url = minio_settings["url"]
minio_access_key = minio_settings["access_key"]
minio_secret_key = minio_settings["secret_key"]

arguments = dict(
    source_json=json.dumps(source_json),
    openaddresses_args=openaddresses_args,
    minio_output_uri=minio_output_uri,
    minio_url=minio_url,
    minio_access_key=minio_access_key,
    minio_secret_key=minio_secret_key,
)

"""Run Pipeline"""

pipeline_run = kfp.Client().create_run_from_pipeline_func(
    pipeline,
    arguments=arguments,
    run_name="openaddresses-get-store-data"
)