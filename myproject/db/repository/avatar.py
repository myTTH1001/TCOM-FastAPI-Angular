from fastapi import UploadFile, File 
from secrets import token_hex


async def upload_avatar(file: UploadFile = File(...)):
    file_ext= file.filename.split(".")[-1]
    file_name = token_hex(10)
    image_extension = f"{file_name}.{file_ext}"
    image_path = f"static/{image_extension}"

    with open(image_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return file_name, image_path