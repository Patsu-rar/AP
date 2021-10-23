from models import Session, User, Region, Category, Advertisement
from datetime import date

session = Session()

region = Region(id=1, name="Test Region")

category = Category(id=1, name="Category")

user = User(id=1, username="user1", email="user1@mail.com", first_name="User1FirstName", last_name="User1LastName",
            password="user1password", region=region)
advertisement = Advertisement(id=1, text="Test Text", date_of_publishing=date.today(), status='open',
                              region=region,
                              category=category, user=user)
session.add(region)
session.add(category)
session.add(advertisement)
session.add(user)
session.commit()

print(session.query(Advertisement).all()[0])
print(session.query(Region).all()[0])
print(session.query(Category).all()[0])
print(session.query(User).all()[0])
