This directory contains the code, dockerfile, and python notebooks used to run the modified OpenAddresses (https://github.com/openaddresses/openaddresses) pipeline on the source files in the source directory. This processing was done using Kubeflow pipelines.

The Open Addresses processing scripts were modified to include additional variables when they were available at the source, specifically the street name, street type, street direction, and full address. The directory of these scripts is https://github.com/CSBP-CPSE/OpenAddresses-batch-machine.

Because the pipeline saves all downloads to minio storage, it is useful to define a shortcut for the standard minimal tenant,


```
source  /vault/secrets/minio-standard-tenant-1

mc config host add standard $MINIO_URL $MINIO_ACCESS_KEY $MINIO_SECRET_KEY
```


