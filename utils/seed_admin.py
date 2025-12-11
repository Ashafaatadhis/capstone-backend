from sqlmodel import Session, select
from models.user import User, UserRole
from utils.password import hash_password


def seed_admin(session: Session):
    # cek apakah sudah ada user
    stmt = select(User)
    existing_user = session.exec(stmt).first()

    if existing_user:
        return  # sudah ada user → tidak perlu buat admin default

    # kalau belum ada, buat admin default
    admin = User(
        username="admin",
        password_hash=hash_password("admin123"),
        role=UserRole.admin
    )

    session.add(admin)
    session.commit()
    session.refresh(admin)

    print("🌱 Default admin created:")
    print("   username: admin")
    print("   password: admin123")
