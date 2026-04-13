import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

SqlAlchemyBase = orm.declarative_base()

# Модель пользователя
class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, unique=True, index=True)
    hashed_password = sa.Column(sa.String, nullable=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

# Модель товара
class Product(SqlAlchemyBase):
    __tablename__ = 'products'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=True)
    price = sa.Column(sa.Integer, nullable=True)
    img_path = sa.Column(sa.String, nullable=True)

# Настройка подключения
__factory = None

def global_init(db_file):
    global __factory
    if __factory:
        return
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    SqlAlchemyBase.metadata.create_all(engine)

def create_session() -> Session:
    return __factory()