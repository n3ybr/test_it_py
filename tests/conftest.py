import pytest
from sqlmodel.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient

from main import app
from database import get_session
from models.users import Users
from controllers.user_controller import get_password_hash

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()

@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_session_override():  
        return session

    app.dependency_overrides[get_session] = get_session_override  

    client = TestClient(app)  
    yield client  

@pytest.fixture(name="token")
def token_fixture(client: TestClient, session: Session):  
    username = "testuser"
    password = "testpassword"
    
    hashed_password = get_password_hash(password)
    session.add(Users(username=username, password=hashed_password))
    session.commit()

    response = client.post(
        "/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == 200, response.text
    return response.json()["access_token"]

@pytest.fixture(name="auth_client")  
def auth_client_fixture(client: TestClient, token: str):  
    client.headers = {"Authorization": f"Bearer {token}"}
    return client