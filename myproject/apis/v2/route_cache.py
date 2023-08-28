from fastapi import APIRouter, status
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.blog import ShowBlog
from db.session import get_db
from db.repository.blog import retreive_blog
from sqlalchemy.orm import Session 
from db.models.blog import Blog
# from cachetools import TTLCache
import redis, json


router = APIRouter()

# dung lượng tối đa 100, thời gian sống Time to Live 60 giây
# cache = TTLCache(maxsize=100, ttl=60)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# @router.post("/cache/add")
# async def add_to_cache(key: str, db: Session= Depends(get_db)):
#     value = 1 # db.query(Blog).filter(Blog.id == id).all()
#     redis_client.set(key =1, value =1)
#     return {"message": redis_client}


# @router.get("/cache/blog/{id}", response_model=ShowBlog)
# async def cache_get_blog(key: str, db: Session= Depends(get_db)):
#     cached_result = redis_client.get(key)
#     print (cached_result)
#     if cached_result is not None:
#         print("Cache hit!")
#         return {"result": "ok"}
#     else:
#         cached_result = "not ok"
#     if not cached_result:
#         raise HTTPException(detail=f"Blog with ID does not exist.", status_code=status.HTTP_404_NOT_FOUND)
#     return {"message":"out"}
  
 
# @router.delete("/cache/clear")
# async def clear_cache():
#     redis_client.flushdb()
#     return {"message": "Cache cleared"}


@router.post("/cache/add")
async def add_to_cache(key: str, db: Session = Depends(get_db)):
    # Thay bằng logic truy vấn thực tế của bạn
    blog = db.query(Blog).filter(Blog.id == 1).first()
    blog_json = json.dumps(blog, default=lambda o: o.__dict__)
    # Lưu dữ liệu blog vào cache Redis
    redis_client.set(key, blog_json)  # Giả sử `key` là một chuỗi và `blog` là một đối tượng
    
    return {"message": "Dữ liệu được thêm vào cache"}

@router.get("/cache/blog/{id}", response_model=ShowBlog)
async def cache_get_blog(id: int, db: Session = Depends(get_db)):
    # Kiểm tra xem dữ liệu có tồn tại trong cache Redis không
    cached_result = redis_client.get(str(id))

    if cached_result is not None:
        print("Dữ liệu từ cache!")
        # Bạn có thể trả về kết quả từ cache tại đây
        return {"result": cached_result}
    else:
        print("Dữ liệu không có trong cache!")

    # Lấy dữ liệu từ cơ sở dữ liệu
    blog = db.query(Blog).filter(Blog.id == id).first()

    if blog is None:
        raise HTTPException(detail=f"Bài viết với ID {id} không tồn tại.", status_code=status.HTTP_404_NOT_FOUND)

    # Lưu dữ liệu blog từ cơ sở dữ liệu vào cache Redis
    redis_client.set(str(id), blog)  # Giả sử `id` là một số nguyên và `blog` là một đối tượng

    return blog