import re


def parse_env_var_def(s):
    """
    Parse string defining a shell environment variable, returning name and val

    Returns (varname, value) if matching pattern, else None
    """
    match = re.search(r"\s*(?<=export)\s+([^=]+)=(.*)", s)
    if match:
        lhs, rhs = match.groups()

        # Remove whitespace and any quoted strings' quotes
        lhs = lhs.strip().strip('\'').strip('"')
        rhs = rhs.strip().strip('\'').strip('"')
        # If both sides exist, return them
        if lhs and rhs:
            return lhs, rhs
    return None


def get_env_variables_from_file(filepath):
    """
    Returns a dictionary of the environment variables defined in a file
    """
    with open(filepath, 'r') as fin:
        lines = fin.readlines()
    lines = [parse_env_var_def(line) for line in lines]

    # Return a dict of lhs:rhs, skipping any lines that are blank
    return {line[0]: line[1] for line in lines if line}


def get_minio_credentials(tenant, strip_http=True, verbose=True):
    """
    Retrieve minio credentials from the vault (available from notebook server)

    Args:
        strip_http (bool): If True, strips http:// from the start of the minio
                           URL
        tenant (str): Minio tenant name, such as "minimal" or "premium"

    Returns:
        (dict): Dict with keys:
            url
            access_key
            secret_key
    """
    vault = f"/vault/secrets/minio-{tenant}-tenant-1"
    if verbose:
        print("Trying to access minio credentials from:")
        print(vault)
    d = get_env_variables_from_file(vault)

    # Select only the keys that we want, also checking that they exist at all
    key_map = {
        "MINIO_URL": "url",
        "MINIO_ACCESS_KEY": "access_key",
        "MINIO_SECRET_KEY": "secret_key",
    }
    minio_credentials = {}
    for k in key_map:
        try:
            minio_credentials[key_map[k]] = d[k]
        except KeyError:
            raise KeyError(f"Cannot find minio credential {k} in vault file")

    if strip_http:
        # Get rid of http:// in minio URL
        minio_credentials["url"] = re.sub(r'^https?://',
                                          "",
                                          minio_credentials["url"],
                                          )

    return minio_credentials


def create_bucket_if_missing(minio_obj, bucket):
    if not minio_obj.bucket_exists(bucket):
        minio_obj.make_bucket(bucket)
        print(f"Created bucket {bucket}")


def copy_to_minio(minio_url, bucket, access_key, secret_key, sourcefile,
                  destination):
    from minio import Minio

    # Store results to minio
    s3 = Minio(
        minio_url,
        access_key=access_key,
        secret_key=secret_key,
        secure=False,
        region="us-west-1",
    )

    # Create bucket if needed
    create_bucket_if_missing(s3, bucket)

    # Put file into bucket
    s3.fput_object(bucket, destination, sourcefile)


def minio_find_files_matching_pattern(minio_url, bucket, access_key,
                                      secret_key, pattern, prefix='',
                                      recursive=True):
    """
    Returns all files in a minio location that match the given pattern

    This function is glob-like in idea, but uses regex patterns instead
    of glob patterns.
    """
    import re
    from minio import Minio
    pattern = re.compile(pattern)

    s3 = Minio(
        minio_url,
        access_key=access_key,
        secret_key=secret_key,
        secure=False,
        region="us-west-1",
    )

    # Get everything in bucket/prefix
    objs = s3.list_objects(bucket, prefix=prefix, recursive=True)

    # Discard directories
    filepaths = [obj.object_name for obj in objs if not obj.is_dir]

    # Select only those that fit the pattern
    matching = [filepath for filepath in filepaths if pattern.match(filepath)]

    return matching
