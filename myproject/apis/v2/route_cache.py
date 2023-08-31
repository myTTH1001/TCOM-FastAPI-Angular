from fastapi import APIRouter, status
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from db.models.blog import Blog
# from cachetools import TTLCache
import redis, json
from sqlalchemy.orm.attributes import instance_dict


router = APIRouter()

# dung lượng tối đa 100, thời gian sống Time to Live 60 giây
# cache = TTLCache(maxsize=100, ttl=60)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


@router.post("/cache/add")
async def add_to_cache(key: str, db: Session = Depends(get_db)):
    # Kiểm tra dữ liệu đã có trong cache chưa
    cached_data = redis_client.get(key)
    if cached_data:
        return {"message": "Dữ liệu đã tồn tại trong cache", "data": json.loads(cached_data)}

    # Truy vấn từ cơ sở dữ liệu
    blogs = db.query(Blog).filter(Blog.id >= int(key)).all()
    if blogs:
        blog_dicts = []
        for blog in blogs:
            # Chuyển đổi đối tượng SQLAlchemy thành từ điển
            blog_dict = instance_dict(blog)
            blog_dict.pop('_sa_instance_state', None)  # Loại bỏ thông tin phiên làm việc
            blog_dicts.append(blog_dict)
        blog_json = json.dumps(blog_dicts, default=str)  # Sử dụng default=str để xử lý datetime
        print(blog_dicts)
        # Lưu dữ liệu blog vào cache Redis
        redis_client.set(key, blog_json) 
        return {"message": "Dữ liệu đã được thêm vào cache", "data": json.loads(blog_json)}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy dữ liệu trong cơ sở dữ liệu")

@router.get("/cache/blog/{key}")
async def cache_get_blog(key: str, db: Session = Depends(get_db)):
    # Kiểm tra xem dữ liệu có tồn tại trong cache Redis không
    cached_result = redis_client.get(key)

    if cached_result is not None:
        return {"message": "Dữ liệu lấy từ cache", "data": json.loads(cached_result)}

    # Lấy dữ liệu từ cơ sở dữ liệu
    blogs = db.query(Blog).filter(Blog.id >= int(key)).all()
    if blogs is None:
        raise HTTPException(detail=f"Bài viết với ID {id} không tồn tại.", status_code=status.HTTP_404_NOT_FOUND)

    if blogs:
        blog_dicts = []
        for blog in blogs:
            # Chuyển đổi đối tượng SQLAlchemy thành từ điển
            blog_dict = instance_dict(blog)
            blog_dict.pop('_sa_instance_state', None)  # Loại bỏ thông tin phiên làm việc
            blog_dicts.append(blog_dict)
        blog_json = json.dumps(blog_dicts, default=str)  # Sử dụng default=str để xử lý datetime

        # Lưu dữ liệu blog vào cache Redis
        redis_client.set(key, blog_json) 
    return {"message": "Dữ liệu chưa có trong cache", "data in db": json.loads(blog_json)}

@router.delete("/cache/clear")
async def clear_cache():
    redis_client.flushdb()
    return {"message": "Cache cleared"}