import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    Integer,
    String,
)

class Base(DeclarativeBase):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    major = Column(String(100), nullable=False)

# 載入環境變數
load_dotenv()
DATABASE_HOST=os.getenv('DATABASE_HOST', 'postgres')
DATABASE_PORT=os.getenv('DATABASE_PORT', '5432')
DATABASE_PASS=os.getenv('DATABASE_PASS', 'postgres')
DATABASE_USER=os.getenv('DATABASE_USER', 'postgres')
DATABASE_NAME=os.getenv('DATABASE_NAME', 'postgres')

# 建立連線 URL
DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

# 創建資料庫引擎
engine = create_engine(DATABASE_URL)

# 創建 session
Session = sessionmaker(bind=engine)
session = Session()

# 插入四個學生資料
def insert_students():
    try:
        # 創建四個學生實例
        student1 = Student(name="Alice", age=20, major="Computer Science")
        student2 = Student(name="Bob", age=22, major="Mathematics")
        student3 = Student(name="Charlie", age=21, major="Physics")
        student4 = Student(name="David", age=23, major="Engineering")

        # 將學生物件加入 session
        session.add_all([student1, student2, student3, student4])

        # 提交事務到資料庫
        session.commit()

        print("Students inserted successfully!")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    insert_students()