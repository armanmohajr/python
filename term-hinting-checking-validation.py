from typing import NewType, TypedDict

RGB = NewType("RGB", tuple[int, int, int])
HSL = NewType("HSL", tuple[int, int, int])


class User(TypedDict):
    first_name: str
    last_name: str
    email: str
    age: int | None
    fav_color: RGB | None


def create_user(
    first_name: str,
    last_name: str,
    age: int | None = None,
    fav_color: RGB | None = None
) -> User:
    email = f"{first_name.lower()}_{last_name.lower()}@example.com"

    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "age": age,
        "fav_color": fav_color,
    }


user1 = create_user("John", "Doe", 20, fav_color=RGB((109, 123, 135)))
user2 = create_user("arman", "ahmed", fav_color=RGB((109, 123, 135)))
print(user1)
print(user2)
