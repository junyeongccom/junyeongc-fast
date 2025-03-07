# ✅ 1. DatabaseBuilder: SQLAlchemy 엔진 및 세션 빌더
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class DatabaseConfigBuilder:
    def __init__(self):
        self._database_url = None
        self._echo = False
        self._future = True
        self._autocommit = False
        self._autoflush = False
        self._engine = None
        self._session_local = None
        self._base = declarative_base()
    
    def set_database_url(self, url: str):
        self._database_url = url
        return self
    
    def set_echo(self, echo: bool):
        self._echo = echo
        return self
    
    def set_future(self, future: bool):
        self._future = future
        return self
    
    def set_autocommit(self, autocommit: bool):
        self._autocommit = autocommit
        return self
    
    def set_autoflush(self, autoflush: bool):
        self._autoflush = autoflush
        return self
    
    def build(self):
        if not self._database_url:
            raise ValueError("Database URL must be provided")
        
        self._engine = create_async_engine(self._database_url, echo=self._echo, future=self._future)
        self._session_local = sessionmaker(bind=self._engine, class_=AsyncSession, expire_on_commit=False, autocommit=self._autocommit, autoflush=self._autoflush)
        
        return DatabaseConfig(
            database_url=self._database_url,
            echo=self._echo,
            future=self._future,
            autocommit=self._autocommit,
            autoflush=self._autoflush,
            engine=self._engine,
            session_local=self._session_local,
            base=self._base
        )

class DatabaseConfig:
    def __init__(self, database_url, echo, future, autocommit, autoflush, engine, session_local, base):
        self.database_url = database_url
        self.echo = echo
        self.future = future
        self.autocommit = autocommit
        self.autoflush = autoflush
        self.engine = engine
        self.session_local = session_local
        self.base = base

# Example Usage:
db_config = (
    DatabaseConfigBuilder()
    .set_database_url("postgresql+asyncpg://postgres:mypassword@database:5432/my_database")
    .set_echo(True)
    .set_autocommit(False)
    .set_autoflush(False)
    .build()
)

async def get_db():
    async with db_config.session_local() as session:
        yield session
