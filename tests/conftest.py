import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from compound.db.models import Compound


@pytest.fixture(scope='function')
def db():
    db_url = os.getenv('DB_URL')
    if not db_url:
        raise ValueError('Missing DB_URL environment variable')
    engine = create_engine(db_url)
    session_class = sessionmaker(bind=engine)
    session = session_class(autocommit=True, autoflush=True)
    session.query(Compound).delete()
    yield session
    session.query(Compound).delete()
