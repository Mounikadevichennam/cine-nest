from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, Profile, UserRole
from app.schemas.user import UserSignup, UserLogin
from app.auth.security import hash_password, verify_password, create_access_token

class AuthService:
    @staticmethod
    def register_user(db: Session, user_in: UserSignup) -> dict:
        existing_user = db.query(User).filter(User.email == user_in.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )
        
        # Check if first user in system -> grant ADMIN role, else default USER
        total_users = db.query(User).count()
        assigned_role = UserRole.ADMIN if total_users == 0 else UserRole.USER

        new_user = User(
            name=user_in.name,
            email=user_in.email,
            password_hash=hash_password(user_in.password),
            role=assigned_role,
            preferred_language=user_in.preferred_language or "Telugu"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Create default main profile for user
        default_profile = Profile(
            user_id=new_user.id,
            profile_name=new_user.name,
            avatar="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"
        )
        db.add(default_profile)
        db.commit()

        access_token = create_access_token(
            data={"sub": str(new_user.id), "email": new_user.email, "role": new_user.role.value}
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": new_user
        }

    @staticmethod
    def authenticate_user(db: Session, user_in: UserLogin) -> dict:
        user = db.query(User).filter(User.email == user_in.email).first()
        if not user or not verify_password(user_in.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )
        
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role.value}
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
