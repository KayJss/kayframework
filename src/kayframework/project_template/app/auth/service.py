from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from app.auth import models, schema
from app.core.security import Security


def create_user(db: Session, user_data: schema.UserCreate) -> models.User:
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu email adresi zaten kayıtlı!")

    hashed_pwd = Security.hash_password(user_data.password)

    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_pwd,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, credentials: schema.UserLogin) -> models.User:
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not Security.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email veya şifre hatalı.")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Kullanıcı pasif.")
    return user


def update_profile(db: Session, user: models.User, user_data: schema.UserUpdate) -> models.User:
    if user_data.email and user_data.email != user.email:
        existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bu email adresi zaten kayıtlı!")
        user.email = user_data.email

    if user_data.username and user_data.username != user.username:
        user.username = user_data.username

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def change_password(db: Session, user: models.User, data: schema.PasswordChange):
    if not Security.verify_password(data.current_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mevcut şifre hatalı.")

    user.password = Security.hash_password(data.new_password)
    db.add(user)
    db.commit()
    return {"message": "Şifre güncellendi."}


def logout(response: Response):
    Security.clear_auth_cookies(response)
    return {"message": "Çıkış yapıldı."}
