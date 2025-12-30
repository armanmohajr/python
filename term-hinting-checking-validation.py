import random
from typing import NewType
from dataclasses import dataclass

import requests

resp = requests.get("https://coreyms.com", timeout=5)
status = resp.status_code

RGB = NewType("RGB", tuple[int, int, int])
HSL = NewType("HSL", tuple[int, int, int])


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    age: int | None = None
    fav_color: RGB | None = None


def create_user(
    first_name: str,
    last_name: str,
    age: int | None = None,
    fav_color: RGB | None = None
) -> User:
    email = f"{first_name.lower()}_{last_name.lower()}@example.com"

    return User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        age=age,
        fav_color=fav_color
    )


def random_choice[T](items: list[T]) -> T:
    return random_choice(items)


user1 = create_user("John", "Doe", 20, fav_color=RGB((109, 123, 135)))
user2 = create_user("arman", "ahmed", fav_color=RGB((109, 123, 135)))
print(user1)
print(user2)


users = [user1, user2]
random_user = random_choice(users)
print(random_user)

emails = [user.email for user in users]
rando_email = random_choice(emails)
print(rando_email)

# def create_user(
#     first_name: str,
#     last_name: str,
#     age: int | None = None,
#     fav_color: RGB | None = None
# ) -> User:
#     email = f"{first_name.lower()}_{last_name.lower()}@example.com"

#     return {
#         "first_name": first_name,
#         "last_name": last_name,
#         "email": email,
#         "age": age,
#         "fav_color": fav_color,
#     }
