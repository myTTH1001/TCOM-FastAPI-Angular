from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi import UploadFile, File
from sqlalchemy import desc, cast, String
from db.session import get_db
from sqlalchemy.orm import Session 
import psutil, GPUtil
from db.models.system import SystemInfo
from apis.v1.route_login import get_current_user
from db.models.user import User
from sqlalchemy import text
import pandas as pd
from datetime import datetime


router = APIRouter()


@router.post("/system_info")
async def add_system_info(db: Session= Depends(get_db)):
    # CPU and Memory Information
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    # GPU Information
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            "gpu_id": gpu.id,
            "gpu_name": gpu.name,
            "gpu_memory_total": gpu.memoryTotal,
            "gpu_memory_free": gpu.memoryFree,
            "gpu_memory_used": gpu.memoryUsed,
            "gpu_utilization": gpu.load,
        })
    system_info = SystemInfo(
        cpu_percent=cpu_percent,
        memory_total=memory_info.total,
        memory_available=memory_info.available,
        memory_percent=memory_info.percent,
        gpu_id = gpu_info[0]["gpu_id"],
        gpu_name= gpu_info[0]["gpu_name"],
        gpu_memory_total= gpu_info[0]["gpu_memory_total"],
        gpu_memory_free= gpu_info[0]["gpu_memory_free"],
        gpu_memory_used= gpu_info[0]["gpu_memory_used"],
        gpu_utilization= gpu_info[0]["gpu_utilization"],
    )
    db.add(system_info)
    db.commit()
    db.close()
    return {"message": "System info saved"}


@router.get("/system/getinfo")
async def get_system_info(db: Session= Depends(get_db), current_user: User=Depends(get_current_user)):
    if current_user is not None:
        getinfo = db.query(SystemInfo).order_by(desc(SystemInfo.id)).first()
        return {"msg": getinfo}
    else:
        return None
    

@router.get("/export/{format}")
async def export_data(format: str, db: Session= Depends(get_db), time_up:str=datetime.now(), time_down:str=None):
    if format not in ["csv", "txt", "xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid format")

    # Truy vấn cơ sở dữ liệu
    query = db.execute(text("SELECT * FROM systeminfo WHERE timestamp BETWEEN :time_down AND :time_up"), {"time_down": time_down, "time_up":time_up})
    
    # Chuyển dữ liệu thành DataFrame
    df = pd.DataFrame(query.fetchall(), columns=query.keys())
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime("%y-%m-%d %H:%M:%S.%f")

    # Xử lý và xuất dữ liệu thành các tệp tương ứng
    if format == "csv":
        csv_filename = "data.csv"
        df.to_csv(csv_filename, index=False)
    elif format == "txt":
        txt_filename = "data.txt"
        df.to_csv(txt_filename, sep="\t", index=False)
    else:
        xlsx_filename = "data.xlsx"
        df.to_excel(xlsx_filename, engine="openpyxl", index=False)
    return {"message": "export file DONE!"}




@router.put("/import/file_to_db")
async def import_data(db: Session = Depends(get_db), file: UploadFile = File(...)):
    # chỉ chấp nhận import file csv và xlsx
    ALLOWED_EXTENSIONS = ["xlsx", "csv"]
    def allowed_file(file):
        return "." in file and file.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file format")

    try:
        if file.filename.endswith("xlsx"):
            df = pd.read_excel(file.filename)
        else:
            df = pd.read_csv(file.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    for index, row in df.iterrows():
        row = row.drop("id")
        data = row.to_dict()
        record = SystemInfo(**data)

        record.timestamp = datetime.strptime(record.timestamp, "%y-%m-%d %H:%M:%S.%f")
       
        check_db = db.query(SystemInfo).filter(SystemInfo.timestamp == record.timestamp).first()
        if check_db:
            db.delete(check_db)
        db.add(record)
        db.commit()
    return {"message": "Data imported successfully"}
