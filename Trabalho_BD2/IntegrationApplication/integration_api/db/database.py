from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Aqui usamos SQLite local, mas você pode trocar para PostgreSQL, etc.
SQLALCHEMY_DATABASE_URL = "sqlite:///./estoque.db"

# Conexão para SQLite (com multithreading)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Gerenciador de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base usada para os models
Base = declarative_base()
