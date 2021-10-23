from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.schema import ForeignKey

engine = create_engine('mysql+pymysql://root:password@localhost:3306/ap_lab6')
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(45), nullable=False)
    first_name = Column(String(45))
    last_name = Column(String(45))
    email = Column(String(45))
    password = Column(String(45))
    region_id = Column(Integer, ForeignKey('region.id'))
    advertisements = relationship("Advertisement", backref="user")

    def __str__(self):
        return f"User: {self.username} first name: {self.first_name}, last name: {self.last_name}, email: {self.email}, password: {self.password}, region: {self.region_id}"


class Category(BaseModel):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    advertisements = relationship("Advertisement", backref="category")

    def __str__(self):
        return f"Category: {self.name}"


class Region(BaseModel):
    __tablename__ = "region"
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    advertisements = relationship("Advertisement", backref="region")
    users = relationship("User", backref="region")

    def __str__(self):
        return f"Region: {self.name}"


class Advertisement(BaseModel):
    __tablename__ = "Advertisement"
    id = Column(Integer, primary_key=True)
    text = Column(String(45), nullable=False)
    date_of_publishing = Column(DATETIME)
    status = Column(Enum('open', 'close'), default='open')
    region_id = Column(Integer, ForeignKey('region.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    def __str__(self):
        return f"Advertisement: {self.text} date of publishing: {self.date_of_publishing}, status: {self.status}, region: {self.region_id}, category: {self.category_id}, user: {self.user_id} "
