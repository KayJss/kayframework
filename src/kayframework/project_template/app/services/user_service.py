from sqlalchemy.orm import Session
from app.auth import models

class UserService:
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        """ID üzerinden kullanıcı bulur."""
        return db.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100):
        """Tüm kullanıcıları listeler (Sayfalamalı)."""
        return db.query(models.User).offset(skip).limit(limit).all()

    @staticmethod
    def deactivate_user(db: Session, user_id: int):
        """Kullanıcıyı pasif hale getirir (Silmek yerine güvenli yöntem)."""
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            user.is_active = False
            db.commit()
        return user