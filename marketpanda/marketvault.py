import gdown

def download_db():
    """
    Download database from google drive
    :return: database binary file
    """
    url = 'https://drive.google.com/uc?id=1HiBvyOnzTi0kXY7GBSZ2RcwsdxJI90yr'
    output = "marketvault.db"

    # create google drive downloader object
    gdown.download(url, output, quiet=False)
    return output