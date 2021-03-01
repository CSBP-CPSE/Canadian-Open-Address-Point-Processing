# Summary

This repo builds and provides access to [this modification](https://github.com/JosephKuchar/batch-machine) of [OpenAddresses batch-machine](https://github.com/openaddresses/batch-machine).  The container is built is similar to that specified by the OpenAddresses repo, but is pinned to a specific commit from JosephKuchar/batch-machine and restricts the user to be non-ROOT.

# Usage:

See `../.github/workflows/build_openaddresses.yml` (or `publish_openaddresses.yml`) for CI/build details, which build `./container/Dockerfile`

See `./pipeline/get_openaddresses_data.ipynb` for example usage.  Typically, the easiest way to invoke this is through a Kubeflow Pipeline.
