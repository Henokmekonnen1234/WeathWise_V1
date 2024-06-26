#!/usr/bin/env python3

from models import storage
from models.user import User
from models.transaction import Transaction

user = User()
user.first_name = "Henok"
user.last_name = "Mekonnen"
user.email = "someone@gmail.com"
user.username = "Henokmac"
user.password = "@Enok123"
user.save()
ts = Transaction()
ts.user_id = user._id
ts.amount = 40.40
ts.type = "expense"
ts.catagory = "food"
ts.description = "for coffee"
ts.save()
print(storage.all())
print("=============")
print(storage.get(User, "bf822464-3c3c-4eff-a33f-3b780abd4f96"))
