'''
Created on Apr 6, 2019

@author: S528358
'''
from sqlalchemy import ForeignKey
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker, relationship
from pickle import INST
Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id'), primary_key = True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    
    def __repr__(self):
        return "<User(first_name = %s, last_name = %s)>"%(self.first_name,self.last_name) 
# print(User.__table__)
class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key = True)
    email_address = Column(String, nullable = False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship("User", back_populates="addresses")
    
    def __repr__(self):
        return "<Address(email_address = %s>"%self.email_address
User.addresses = relationship("Address", order_by=Address.id, back_populates="user")
Base.metadata.create_all(engine)
obj1 = User(first_name="kelsey", last_name ="means")
Session = sessionmaker(bind=engine)
session = Session()
session.add(obj1)   
our_user = session.query(User).filter_by(first_name='kelsey').first()
print(our_user)
print(obj1)
print(obj1 is our_user)
session.add_all([
    User(first_name = 'name1', last_name='last_name1'),
    User(first_name = 'name2', last_name ='last_name2'),
    User(first_name = 'name3', last_name = 'last_name3')])
session.new
session.commit()
for instance in session.query(User).order_by(User.id):
    print(instance.first_name, instance.last_name)
obj1.last_name = 'lolwa'
print(session.dirty)
# print(session.new)
fake_user = User(first_name = 'fuck', last_name = 'you')
session.add(fake_user)
print(fake_user in session)
session.rollback()
print(fake_user in session)

for first_name, last_name in session.query(User.first_name, User.last_name):
    print(first_name, last_name)
    
for instance in session.query(User, User.first_name).all():
    print(instance.User, instance.first_name)
    
for instance in session.query(User).order_by(User.id)[1:3]:
    print(instance.id, instance.first_name, instance.last_name)
print('+++++++++++++++++')
for instance in session.query(User).filter(~User.first_name.in_(['kelsey'])):
    print(instance.first_name, instance.last_name)

print("testing == method")
for instance in session.query(User).filter(User.first_name == "kelsey"):
    print(instance.first_name, instance.last_name)
print("testing != method")
for instance in session.query(User).filter(User.first_name != 'kelsey'):
    print(instance.first_name, instance.last_name)

print("testing LIKE case sensitive")
for instance in session.query(User).filter(User.first_name.like("%NAMEd%")):
    print(instance.first_name, instance.last_name)
    
print("testing ILIKE case in - sensitive")
for instance in session.query(User).filter(User.first_name.ilike("%NAMEd%")):
    print(instance.first_name, instance.last_name)
    
print("testing IS NOT None")
for instance in session.query(User).filter(User.first_name.isnot(None)):
    print(instance.first_name, instance.last_name)
    
print("testing AND")
for instance in session.query(User).filter(and_(User.first_name=='kelsey'), User.last_name=='means'):
    print(instance.first_name, instance.last_name)
    
# print('testing match')
# for instance in session.query(User).filter(User.first_name.match("kelsey")):
#     print(instance.first_name, instance.last_name)

print("testing all method")
for instance in session.query(User).all():
    print(instance.first_name, instance.last_name)
    
print("testing first")
result = session.query(User).first()
print(result.first_name, result.last_name)

print("fetch all rows using one")
# result = session.query(User).one()
# print(result)
# for instance in session.query(User).one():
#     print(instance.first_name, instance.last_name)
jack = User(first_name = "jack", last_name = "dickinson")
print(jack.addresses)
jack.addresses = [Address(email_address = "jack@gmail.com")]
print(jack.addresses[0].user)
session.add(jack)
session.commit()
for instance in session.query(User).filter(User.first_name == "jck"):
    print(instance.first_name, instance.last_name)