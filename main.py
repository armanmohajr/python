from datetime import datetime, UTC
from functools import partial
from typing import Literal, Annotated
from uuid import UUID, uuid4
import json

from pydantic import BaseModel, ValidationError, Field, EmailStr, HttpUrl, SecretStr, ValidationError, ValidationInfo, field_validator, model_validator, computed_field, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True,
                              strict=True,
                              extra="allow",
                              #   validate_assignment=True,
                              frozen=True
                              )

    uid: UUID = Field(default_factory=uuid4)
    username: Annotated[str, Field(min_length=3, max_length=20)]
    email: EmailStr
    password: SecretStr
    website: HttpUrl | None = None
    age: Annotated[int, Field(ge=13, le=120)]
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True

    first_name: str = ""
    last_name: str = ""
    follower_count: int = 0

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError(
                "Username must be alphanumeric (underscore allowed)")
        return v.lower()

    @field_validator("website", mode="before")
    @classmethod
    def add_http(cls, v: str | None) -> str | None:
        if v and not v.startswith(("http://", "https://")):
            return f"http://{v}"
        return v

    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @computed_field
    @property
    def is_influencer(self) -> bool:
        return self.follower_count >= 10000


class Comment(BaseModel):
    content: str
    author_email: EmailStr
    likes: int = 0


class BlogPost(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=10)]
    author: User
    view_count: int = 0
    is_published: bool = False
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    # created_at: datetime = Field(default_factory=partial(datetime.now, tz=UTC))
    status: Literal["draft", "published", "archived"] = "draft"
    slug: Annotated[str, Field(pattern=r"^[a-z0-9-]+$")]

    comments: list[Comment] = Field(default_factory=list)


class UserRegisteration(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def password_match(self) -> "UserRegisteration":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


user_data = {
    "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
    "username": "Arman_Ahmed",
    "email": "ArmnaAhmed@gmail.com",
    "age": 24,
    "password": "secret123",
    "notes": "Hello World",
}

user = User.model_validate_json(json.dumps(user_data))

user.email = "ArmanAhmed3@gmail.com"

print(user.model_dump_json(
    indent=2, by_alias=True))


# try:s
#     registration = UserRegisteration(
#         email="ArmanAhmed@gmail.com",
#         password="secret123",
#         confirm_password="secret456",
#     )
# except ValidationError as e:
#     print(e)

# post_data = {
#     "title": "Understanding Pydantic Models",
#     "content": "Pydantic makes data validation easy and intuitive...",
#     "slug": "understanding-pydantic",
#     "author": {
#         "username": "Arman_Ahmed",
#         "email": "ArmnaAhmed@gmail.com",
#         "age": 24,
#         "password": "secret123",
#     },
#     "comments": [
#         {
#             "content": "I think i understand nested models now",
#             "author_email": "student@gmail.com",
#             "likes": 10,
#         },
#         {
#             "content": "Can you explain how to use computed fields?",
#             "author_email": "viewer@gmail.com",
#             "likes": 15,
#         }
#     ]
# }

# post = BlogPost.model_validate(post_data)

# print(post.model_dump_json(indent=2))


# user = User(
#     username="Arman_Ahmed",
#     email="ArmnaAhmed@gmail.com",
#     age=24,
#     password="secret123",
#     website="armanahmed.com",
#     first_name="Arman",
#     last_name="Ahmed",
# )

# print(user.model_dump_json(indent=2))


# try:
#     user = User(
#         uid=0,
#         username="aa",
#         email="Armanahmed@gmail.com",
#         age=12,
#     )
# except ValidationError as e:
#     print(e)

# post = BlogPost(
#     title="Getting Started with Python",
#     content="Here's how to begin...",
#     author_id="12345"
# )

# print(post)
