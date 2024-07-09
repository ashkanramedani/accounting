import hashlib
import json
import os
import time
import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from lib.json_handler import json_handler
from lib.minio import MinioClient

# from lib.oauth2 import oauth2_scheme, get_current_user, create_access_token, create_refresh_token
# expire_date, delete_date, can_deleted, deleted, update_date, can_update, visible, create_date, priority
#    DateTime,    DateTime,        True,   False,    DateTime,       True,    True,    DateTime,      Int

router = APIRouter(prefix='/api/v1/file', tags=['File'])

# to get the current working directory
directory = os.getcwd()
_obj_json_handler_config = json_handler(FilePath=directory + "/configs/config.json")
config = _obj_json_handler_config.Data


def removeChar(filename: str, ch: str):
    return filename.replace(ch, '')


@router.post('/files')
async def download_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}


@router.post('/downloadfile')
def download_files(bucket_name: str, file_path: str):
    _obClientMinio = MinioClient(endpoint=config['minio']['endpoint'], access_key=config['minio']['access_key'], secret_key=config['minio']['secret_key'], bucket_name=bucket_name)
    _obClientMinio.download_file(file=file_path, file_size=81921)


@router.post('/geturl')
def geturl(bucket_name: str, object_name: str, limit: int = 2):
    _obClientMinio = MinioClient(endpoint=config['minio']['endpoint'], access_key=config['minio']['access_key'], secret_key=config['minio']['secret_key'], bucket_name=bucket_name)
    url = _obClientMinio.get_url(bucket_name, object_name, limit)
    return {"url": url}


@router.post('/uploadfile_with_version')
async def uploadfile_with_version(bucket_name: str, file_size: int, gname: int = 0, user_id: int = 1, prefix_name: str = "", postfix_name: str = "", file: UploadFile = File(...)):
    filename = file.filename
    content_type = file.content_type

    if gname == 1:
        pre_name = ""

        prefix_name = removeChar(prefix_name, ' ')
        prefix_name = removeChar(prefix_name, '_')

        if prefix_name != "":
            pre_name += prefix_name + "_"

        pre_name += str(hashlib.md5(str(str(user_id) + str(filename)).encode('utf8')).hexdigest())

        postfix_name = removeChar(postfix_name, ' ')
        postfix_name = removeChar(postfix_name, '_')

        if postfix_name != "":
            pre_name += "_" + postfix_name

        filename = pre_name + '.' + filename.rsplit('.', 1)[1].lower()

        file.filename = filename

    _obClientMinio = MinioClient(endpoint=config['minio']['endpoint'], access_key=config['minio']['access_key'], secret_key=config['minio']['secret_key'], bucket_name=bucket_name)
    version_id = _obClientMinio.upload_file(file=file, file_size=file_size)

    return {'bucketname': bucket_name, 'filename': filename, 'file_size': file_size, 'type': content_type, 'version_id': version_id}


@router.post('/uploadfile')
async def uploadfile(bucket_name: str, file_size: int, gname: int = 0, file: UploadFile = File(...)):
    filename = file.filename
    content_type = file.content_type
    if gname == 1:
        pre_name = str((hashlib.md5(str(str(time.time()) + str(filename)).encode('utf8')).hexdigest()))
        filename = pre_name + '.' + filename.rsplit('.', 1)[1].lower()
        file.filename = filename

    _obClientMinio = MinioClient(endpoint=config['minio']['endpoint'], access_key=config['minio']['access_key'], secret_key=config['minio']['secret_key'], bucket_name=bucket_name)
    _obClientMinio.upload_file(file=file, file_size=file_size)

    return {'bucketname': bucket_name, 'filename': filename, 'file_size': file_size, 'type': content_type}


# Directory to save uploaded files
UPLOAD_DIR = "files"
FILE_INFO_PATH = "file_info.json"
DOWNLOAD_LOG_DIR = "download_logs"

# Create the file_info.json and download_logs directory if they don't exist
for path in [FILE_INFO_PATH, DOWNLOAD_LOG_DIR]:
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump([], f)


def update_file_info(filename):
    with open(FILE_INFO_PATH) as f:
        file_info = json.load(f)

    file_info.append({"filename": filename, "path": f"{UPLOAD_DIR}/{filename}"})

    with open(FILE_INFO_PATH, "w") as f:
        json.dump(file_info, f)


def log_download_info(filename, client_ip):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{DOWNLOAD_LOG_DIR}/download_log_{timestamp}.json"

    with open(log_filename, "w") as f:
        download_log = json.load(f)

        download_log.append({"filename": filename, "client_ip": client_ip})

        json.dump(download_log, f)


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    update_file_info(file.filename)

    return {"filename": file.filename}


@router.get("/downloadfile/{filename}")
async def read_item(filename: str):
    file_path = f"{UPLOAD_DIR}/{filename}"

    # Log download information
    # log_download_info(filename, client_ip)
    #
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)


@router.post("/savefile/")
async def save_file_content(file: UploadFile = File(...)):
    # Generate a UUID as the filename
    unique_filename = f"{str(uuid.uuid4())}{os.path.splitext(file.filename)[1]}"
    file_path = f"{UPLOAD_DIR}/{unique_filename}"

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    update_file_info(unique_filename)

    return {
        "file_name": f"{unique_filename}",
        "detail": f"File '{unique_filename}' saved successfully."
    }


@router.get("/testfile/{filename}")
async def test_file_info(filename: str):
    file_path = f"{UPLOAD_DIR}/{filename}"

    try:
        with open(file_path, "r") as f:
            content = f.read()
            # Calculate MD5 hash of file content
            file_hash = hashlib.md5(content.encode()).hexdigest()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")

    return {"filename": filename, "hash": file_hash}


@router.put("/changefilename/{filename}")
async def change_file_name(filename: str, new_filename: str):
    file_path = f"{UPLOAD_DIR}/{filename}"
    new_file_path = f"{UPLOAD_DIR}/{new_filename}"

    try:
        # Rename the file
        os.rename(file_path, new_file_path)
        # Update file information with the new filename
        update_file_info(new_filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")

    return {"message": f"File name changed from '{filename}' to '{new_filename}'."}

# async def download_file( user_id: PyObjectId, storage_id: PyObjectId, file_path: str ) -> str | None:
#     if storage := await get_storage(user_id=user_id, storage_id=storage_id):
#         client = MinioClient(
#             endpoint='apiminio.ieltsdaily.ir',
#             access_key="ugsEXJZpUfDHDRKd",
#             secret_key="zCo2bNwsIStIt4Os7l5aOiBzlrM8q9tj",
#             bucket_name="product",
#         )
#         destination_folder = f"{settings.TEMP_FOLDER}/{user_id}"
#         filename = file_path.split("/")[-1]
#         client.download_file(
#             source=file_path, destination=f"{destination_folder}/{filename}"
#         )
#         return f"{destination_folder}/{filename}"
