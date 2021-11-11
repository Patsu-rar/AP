import datetime
from validators import email


def check_json(function):
    def wrapper(*args, **kwargs):
        table_model, request = args
        correct = list(filter(lambda key: key not in table_model.__table__.columns.keys()[1:], request.json.keys())) == []
        return function(*args, **kwargs) and correct
    return wrapper


@check_json
def check_user(user_model, request):
    valid = True
    if request.json.get("email"):
        valid = valid and email(request.json.get("email"))
    region_id = request.json.get("region_id", None)
    if region_id:
        valid = valid and (region_id in range(1, 11))
    return valid


@check_json
def check_advertisement(advertisement_model, request):
    valid = []
    date = request.json.get("date_of_publishing", None)
    region_id = request.json.get("region_id", None)
    category_id = request.json.get("category_id", None)
    if region_id:
        valid.append(region_id in range(1, 11))
    if category_id:
        valid.append(category_id in range(1, 7))
    if date:
        valid.append(False)
    return all(valid)
