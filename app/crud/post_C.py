from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from ..database import get_database
from ..models.post_M import Blog, Category
from ..models.user_M import User
from ..routes.auth_R import get_current_user_email
from ..schemas.post_S import BlogCreateSchema, BlogResponseSchema

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=BlogResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_blog(
    db: Annotated[AsyncSession, Depends(get_database)],
    blog_data: BlogCreateSchema,
    email: Annotated[str, Depends(get_current_user_email)],
):
    user_query = select(User).where(User.email == email)
    user_result = await db.execute(user_query)
    current_user = user_result.scalar_one_or_none()

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    existing_blog_query = select(Blog).where(Blog.title == blog_data.title)
    existing_blog_result = await db.execute(existing_blog_query)
    existing_blog = existing_blog_result.scalar_one_or_none()

    if existing_blog:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A blog with this title already exists.",
        )

    category_query = select(Category).where(Category.id == blog_data.category_id)
    category_result = await db.execute(category_query)
    category = category_result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    new_blog = Blog(
        title=blog_data.title,
        content=blog_data.content,
        summary=blog_data.summary,
        category_id=blog_data.category_id,
        author_id=current_user.id,
    )
    new_blog.author = current_user

    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog


@router.get("/", response_model=list[BlogResponseSchema])
async def get_blogs(db: Annotated[AsyncSession, Depends(get_database)]):
    query = (
        select(Blog)
        .options(selectinload(Blog.author))
        .order_by(Blog.created_at.desc())
    )
    result = await db.execute(query)
    blogs = result.scalars().all()
    return blogs


@router.get("/{blog_id}", response_model=BlogResponseSchema)
async def get_blog(blog_id: int, db: Annotated[AsyncSession, Depends(get_database)]):
    query = select(Blog).options(selectinload(Blog.author)).where(Blog.id == blog_id)
    result = await db.execute(query)
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    return blog
