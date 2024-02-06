import os
from azure.storage.blob import BlobServiceClient
from const import PATH_TO_RESOURCES
from pymongo import MongoClient


def get_blob_service_client():
    """Retrieve the Azure Blob Service Client
    
    Alternative way to authenticate: use Microsoft Entra ID instead of connection strings

    Returns:
        BlobServiceClient: the BlobServiceClient returned based on the Blob Connection String save in local env variable
    """
    try:
        BLOB_CONN_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        return BlobServiceClient.from_connection_string(BLOB_CONN_STRING)
    except Exception as e:
        print(f"An error has occurred: {e}")


def get_image_from_blob():
    """Download birthday meme image from the "images" container from "demofunc0001" storage account

    Returns:
        str: the path to the image downloaded.
    """
    # local_file_name = str(uuid.uuid4()) + ".jpg"
    local_file_name = "bday_meme.jpg"
    blob_service_client = get_blob_service_client()
    container_name = "images"
    # blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    blob_name = "bday1.jpg"
    download_file_path = os.path.join(PATH_TO_RESOURCES, str.replace(local_file_name ,'.jpg', 'DOWNLOAD.jpg'))
    
    download(blob_service_client=blob_service_client, container_name=container_name, download_file_path=download_file_path, blob_name=blob_name)
    
    return download_file_path


def get_text_from_blob():
    """Download birthday message from the "text" container from "demofunc0001" storage account

    Returns:
        str: the birthday message
    """
    # local_file_name = str(uuid.uuid4()) + ".txt"
    local_file_name = "msg.txt"
    blob_service_client = get_blob_service_client()
    container_name = "text"
    # blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    blob_name = "msg.txt"
    download_file_path = os.path.join(PATH_TO_RESOURCES, str.replace(local_file_name ,'.txt', 'DOWNLOAD.txt'))
    
    download(blob_service_client=blob_service_client, container_name=container_name, download_file_path=download_file_path, blob_name=blob_name)
    
    with open(download_file_path, "r") as f:
        msg = f.read()
        return msg


def get_doc_from_blob():
    """Download a document from the "docs" container from "demofunc0001" storage account
    
    Returns:
        str: the path to the document downloaded.
    """
    local_file_name = "notice.pdf"
    blob_service_client = get_blob_service_client()
    container_name = "docs"
    # blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    blob_name = "rent_notice.pdf"
    download_file_path = os.path.join(PATH_TO_RESOURCES, str.replace(local_file_name ,'.txt', 'DOWNLOAD.txt'))
    
    download(blob_service_client=blob_service_client, container_name=container_name, download_file_path=download_file_path, blob_name=blob_name)
    
    return download_file_path


def download(blob_service_client, container_name: str, download_file_path: str, blob_name: str):
    """The actual process of downloading from Azure Blob

    Args:
        blob_service_client (_type_): The Blob service client.
        container_name (str): Name of the Blob container.
        download_file_path (str): Path to download.
        blob_name (str): Name of the blob.
    """
    container_client = blob_service_client.get_container_client(container_name) 
    print("\nDownloading blob to \n\t" + download_file_path)
    
    with open(file=download_file_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob_name).readall())


def get_collection():
    """To return a collection (of contacts) from the local MongoDB database

    Returns:
        pymongo.collection.Collection: the collection of a MongoDB database.
    """
    variable = "AzureMongoDBConnectionStr"
    CONNECTION_STRING = os.getenv(variable)
    client = MongoClient(CONNECTION_STRING)
    database = client[os.getenv("AZURE_MONGODB_DB")]
    return database[os.getenv("AZURE_MONGODB_COLLECTION")]


# -----testing-----
# print(get_image_from_blob())
# print(download_from_text_container())
# print(get_doc_from_blob())