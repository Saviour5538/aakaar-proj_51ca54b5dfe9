import uuid
from sqlalchemy.exc import SQLAlchemyError
from database.models import (
    engine, SessionLocal, User, Session, UploadedFile, DataChunk, KnowledgeGraphEdge, QueryHistory
)

def seed_database():
    session = SessionLocal()
    try:
        # Create sample users
        user1 = User(
            id=uuid.uuid4(),
            email="user1@example.com",
            password_hash="hashed_password_1",
            created_at=None
        )
        user2 = User(
            id=uuid.uuid4(),
            email="user2@example.com",
            password_hash="hashed_password_2",
            created_at=None
        )
        user3 = User(
            id=uuid.uuid4(),
            email="user3@example.com",
            password_hash="hashed_password_3",
            created_at=None
        )
        session.add_all([user1, user2, user3])
        session.commit()

        # Create sample sessions
        session1 = Session(
            id=uuid.uuid4(),
            user_id=user1.id,
            token="token1",
            created_at=None,
            expires_at=None
        )
        session2 = Session(
            id=uuid.uuid4(),
            user_id=user2.id,
            token="token2",
            created_at=None,
            expires_at=None
        )
        session.add_all([session1, session2])
        session.commit()

        # Create sample uploaded files
        file1 = UploadedFile(
            id=uuid.uuid4(),
            user_id=user1.id,
            session_id=session1.id,
            filename="file1.xlsx",
            original_filename="original_file1.xlsx",
            file_size=1024,
            status="uploaded",
            uploaded_at=None,
            processed_at=None
        )
        file2 = UploadedFile(
            id=uuid.uuid4(),
            user_id=user2.id,
            session_id=session2.id,
            filename="file2.xlsx",
            original_filename="original_file2.xlsx",
            file_size=2048,
            status="processed",
            uploaded_at=None,
            processed_at=None
        )
        session.add_all([file1, file2])
        session.commit()

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()