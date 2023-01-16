from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = relationship("Blog", back_populates="creator")
    #blogs = relationship("Blog", cascade="all,delete", backref='creator')

    def __repr__(self):
        return f"User(id:{self.id},name:{self.name},email:{self.email},password:{self.password})"


class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creator = relationship("User", back_populates="blogs")
    # creator = relationship(User, backref=backref("blogs", cascade='all,delete'))

    def __repr__(self):
        return f"Blog(id:{self.id},title:{self.title},body:{self.body})"
