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
    connection.cursor().execute(f"insert into [Buyer] values('{email}', '{phone}', '{fullname}', 't{login}', '{password}', null, 0, null)")
