from fastapi import APIRouter, UploadFile
from fastapi import HTTPException, status
import json, os
from datetime import datetime
from fastapi.responses import FileResponse


router = APIRouter()


# uploadfile
@router.post("/upload/files")
async def upload_file(file: UploadFile):
    if file.content_type != "application/json":
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="JSON file is allowed")
    
    else:
        data = json.loads(file.file.read())
    return {"content": data , "filename": file.filename}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


# upload and download file
@router.post("/uploadndownload/")
async def upload_download_file(file: UploadFile):
    if file.content_type != "application/json":
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="JSON file is allowed")
    
    else:
        json_data = json.loads(file.file.read())
        new_filename = "{}_{}.txt".format(os.path.splitext(file.filename)[0], datetime.now().strftime('%Y%m%d%H%M%S'))
        SAVE_FILE_PATH = os.path.join(UPLOAD_DIR, new_filename)
        with open(SAVE_FILE_PATH, "w", encoding='utf-8') as f:
            f.write(str(json_data))
        return FileResponse(path= SAVE_FILE_PATH, filename= new_filename)