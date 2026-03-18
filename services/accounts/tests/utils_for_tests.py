from app.schemas.pydantic_schemas import User


test_users = (
    User(email="user1@gmail.com", password="MyStrongPassword"),
    User(email="user2@gmail.com", password="strongpassword123"),
    User(email="user2@gmail.com", password="somestring4567890")
    )
