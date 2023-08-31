from datetime import datetime
from sqlalchemy import Float,Column, Integer, DateTime, String, JSON
import datetime
from db.base import Base


class SystemInfo(Base):
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    cpu_percent = Column(Float)
    memory_total = Column(Float)
    memory_available = Column(Float)
    memory_percent = Column(Float)
    # gpu_info = Column(JSON)  # Store GPU information as JSON
    gpu_id = Column(Float)
    gpu_name= Column(String)
    gpu_memory_total = Column(Float)
    gpu_memory_free = Column(Float)
    gpu_memory_used = Column(Float)
    gpu_utilization = Column(Float)