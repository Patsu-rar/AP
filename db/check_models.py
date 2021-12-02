# from datetime import date
#
# from db.models import Session, User, Region, Category, Advertisement
# from main import bc
#
#
# def fill_db():
#     session = Session()
#     region = Region(id=1, name="Test Region")
#     region_2 = Region(id=2, name="Test Region2")
#     category = Category(id=1, name="Category")
#     category_2 = Category(id=2, name="Category2")
#     user = User(id=1, username="user1", email="user1@mail.com", first_name="User1FirstName", last_name="User1LastName",
#                 password=bc.generate_password_hash("user1", rounds=4).decode('UTF-8'), region=region)
#     advertisement = Advertisement(id=1, text="Test Text", date_of_publishing=date.today(), status='open',
#                                   region=region, category=category, user=user)
#     session.add(region)
#     session.add(region_2)
#     session.add(category_2)
#     session.add(category)
#     session.add(user)
#     session.add(advertisement)
#     session.commit()