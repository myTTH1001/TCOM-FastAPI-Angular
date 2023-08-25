from sqlalchemy.orm import Session 
from schemas.blog import CreateBlog, UpdateBlog
from db.models.blog import Blog

# thêm 1 blog mới
def create_new_blog(blog: CreateBlog, db: Session, author_id:int = 1):
    blog = Blog(**blog.dict(),author_id=author_id)

    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

# lấy chi tiết blog có id=  id
def retreive_blog(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog

# Tìm blog có active = True và title chứa question
def list_blogs(db : Session, q: str):
    blogs = db.query(Blog).filter(Blog.is_active==True or Blog.title.ilike(f"%{q}%")).all()
    return blogs

# Cập nhật 1 bản ghi trong blog
def update_blog(id:int, blog: UpdateBlog, author_id: int, db: Session):
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return {"error":f"Blog with id {id} does not exist"}
    if not blog_in_db.author_id == author_id:
        return {"error":f"Only the author can modify the blog"}
    
    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    db.add(blog_in_db)
    db.commit()
    return blog_in_db

# Xóa 1 blog
def delete_blog(id:int, author_id:int,db:Session):
    blog_in_db = db.query(Blog).filter(Blog.id == id)
    if not blog_in_db.first():
        return {"error":f"Could not find blog with id {id}"}
    if not blog_in_db.first().author_id == author_id:
        return {"error":f"Only the author can delete a blog"}
    blog_in_db.delete()
    db.commit()
    return {"msg":f"deleted blog with id {id}"}