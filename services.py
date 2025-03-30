from config.db import Base, engine

def create_database():
    return Base.metadata.create_all(bind=engine)
