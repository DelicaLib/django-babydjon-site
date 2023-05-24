import shop.models as models
from django.db import connection

def login(login="", password=""):
    user = connection.cursor().execute(f"select [Id] from [Buyer] where [Login]= '{login}' and [Password]='{password}'")
    if user.rowcount == 0:
        return -1
    else:
        return user.fetchall()[0][0]
    
def register(firstname: str, secondname : str, email : str, phone : str, login : str, password : str):
    fullname = firstname + " " + secondname
    connection.cursor().execute(f"insert into [Buyer] values('{email}', '{phone}', '{fullname}', '{login}', '{password}', null, 0, null)")


def getUserData(userId: int):
    for i in models.Buyer.objects.raw(f"select * from [Buyer] where [Id] = {userId}"):
        context = {"Id" : i.Id,
                   "Email" : i.Email,
                   "PhoneNumber" : i.PhoneNumber,
                   "FullName" : i.FullName,
                   "Address" : i.Address,
                   "Balance" : i.Balance}
        return i