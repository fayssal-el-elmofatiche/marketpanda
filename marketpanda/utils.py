# © Copyright 2023 dnbf.tech GmbH
# Created by fayssalelmofatiche at 10.10.23
# Description: different functions for helping with data retrieval from sqlite database and transformations

import os

def get_file_metadata(file_path: str) -> dict:
    """
    Get the metadata of a file
    :param file_path: path to the file
    :return: dictionary containing the metadata
    """
    # Retrieve the metadata of the file
    file_metadata = os.stat(file_path)

    # Construct the metadata dictionary
    metadata = {
        "file_name": os.path.basename(file_path),
        "file_size in MB": file_metadata.st_size,
        "file_creation_time": file_metadata.st_ctime / ((1024 * 1024)),
        "file_modification_time": file_metadata.st_mtime
    }

    return metadata