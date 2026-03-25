from app.schemas.pydantic_schemas import User


test_users = (
    User(email="user1@gmail.com", password="MyStrongPassword"),
    User(email="user2@gmail.com", password="strongpassword123"),
    User(email="user2@gmail.com", password="somestring4567890")
    )


class TestPassword:
    password='MyStrongPassword'
    hashed_password='$argon2id$v=19$m=65536,t=3,p=4$Rm81aqXN6zHvrSasfb346A$Vjzf0rczccXVvwiZJnuPxxp+L0uCA1c8Cs3s7sRA5KI'
