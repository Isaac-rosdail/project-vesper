# Holds fixtures & test config, automatically loaded by pytest (import not req'd)

import pytest
from app import create_app
from app.core.database import get_engine, db_session
from app.core.db_base import Base
from sqlalchemy import text
import time
import subprocess

#session = db_session()

print("conftest loaded!")

############### Ensure Docker PostgreSQL container is running before tests start
@pytest.fixture(scope="session", autouse=True)
def ensure_docker_postgres():
    print("Ensuring vesper-db is running...")

    # Check if already running
    result = subprocess.run(
        ["docker", "ps", "-q", "-f", "name=vesper-db"],
        capture_output=True, text=True
    )

    if not result.stdout.strip():
        print("Starting vesper-db container...")
        subprocess.run(["docker", "start", "vesper-db"])
        time.sleep(3) # Let it initialize

# Create app once and use it for all tests
@pytest.fixture(scope="session")
def app():
    app = create_app("testing")  # Create with 'testing' config
    yield app

# Fixture to reset the database before each test (optional, for clean slate)
@pytest.fixture(scope="session", autouse=True)
def reset_db(app):
    engine = get_engine(app.config)
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT") # Study this later!!
        conn.execute(text("DROP SCHEMA IF EXISTS public CASCADE;"))
        conn.execute(text("CREATE SCHEMA public;"))

    # Import DB stuff
    from app.modules.groceries import models as grocery_models
    from app.modules.tasks import models as tasks_models
    Base.metadata.create_all(engine)

# Fixture to clear all table data between tests
# Necessary now that tests and app share the same session via monkeypatching
@pytest.fixture(autouse=True)
def clear_tables(app):
    sess = db_session()
    try:
        for table in reversed(Base.metadata.sorted_tables):
            sess.execute(table.delete())
        sess.flush()
        yield
    finally:
        sess.rollback()
        sess.close() # Optional with scoped_session but safe here
        db_session.remove()

## TRY THIS OUT
@pytest.fixture(scope="session")
def engine(app):
    return get_engine(app.config)

# Fixture to cleanup session (replaces db_session we had before)
@pytest.fixture(autouse=True)
def cleanup_session():
    yield
    db_session.remove()

# monkeypatches get_db_session() to use our test session
@pytest.fixture(autouse=True)
def patch_db_session(monkeypatch):
    from app.core.database import db_session as global_session
    monkeypatch.setattr("app.core.database.get_db_session", lambda *_: global_session())

# Fake browser to test routes (lets us send requests from a fake browser/client)
@pytest.fixture
def client(app):
    return app.test_client()

# Basic sanity test
def test_postgresql_connection(db_session):
    result = db_session.execute(text("SELECT 1")).scalar()
    assert result == 1