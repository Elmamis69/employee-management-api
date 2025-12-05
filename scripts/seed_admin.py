#!/usr/bin/env python3
"""
Script para crear un usuario admin en la base de datos.
Uso: python scripts/seed_admin.py
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.core.config import settings


def seed_admin():
    """Crea un usuario admin en la base de datos si no existe"""
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = Session()
    
    try:
        # Verificar si el admin ya existe
        existing_admin = db.query(User).filter(
            User.email == "admin@example.com"
        ).first()
        
        if existing_admin:
            print("✓ Admin user already exists")
            return
        
        # Crear usuario admin
        admin_user = User(
            email="admin@example.com",
            full_name="Administrator",
            hashed_password=get_password_hash("hola123123"),
            role=UserRole.ADMIN,
            is_active=True,
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✓ Admin user created successfully")
        print("  Email: admin@example.com")
        print("  Password: hola123123")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error creating admin user: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()
