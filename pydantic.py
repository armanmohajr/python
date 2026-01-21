from pydantic import BaseModel, Field, EmailStr, SecretStr, HttpUrl, field_validator, computed_field
from uuid import UUID, uuid4


class User(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    username: str = Field(min_length=3)
    email: EmailStr
    password: SecretStr
    website: HttpUrl | None = None
    age: int = Field(ge=13, le=120)
    first_name: str = ""
    last_name: str = ""
    follower_count: int = 0

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric or underscore")
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
