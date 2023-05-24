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
    return models.Buyer.objects.raw(f"select * from [Buyer] where [Id] = {userId}")[0]
    
    
def setUserSettings(userId: int, fullname: str, email: str, phoneNumber : str, address : str, password: str, newPassword: str, newPasswordRepeat: str):
    user = None
    for i in models.Buyer.objects.raw(f"select * from [Buyer] where [Id] = {userId}"):
        user = i
    
    if password == i.Password:
        if fullname != "":
            connection.cursor().execute(f"update [Buyer] set [FullName]='{ fullname }' where [Id] = {userId} ")
        if email != "":
            connection.cursor().execute(f"update [Buyer] set [Email]='{ email }' where [Id] = {userId} ")
        if phoneNumber != "":
            if len(phoneNumber) != 12 or phoneNumber[0] + phoneNumber[1] != "+7" or not phoneNumber[1:11].isdigit():
                return "Неправильный формат номера телефона. Формат должен быть (+7XXXXXXXXXX), где X - цифра"
            connection.cursor().execute(f"update [Buyer] set [PhoneNumber]='{ phoneNumber }' where [Id] = {userId} ")
        if address != "":
            connection.cursor().execute(f"update [Buyer] set [Address]='{ address }' where [Id] = {userId} ")
        if newPassword != "" and newPassword == newPasswordRepeat:
            connection.cursor().execute(f"update [Buyer] set [Password]='{ newPassword }' where [Id] = {userId} ")
    else:
        return "Неправильный пароль"
    
    return "0"


def createBonusCard(userId: int):
    newCardId = connection.cursor().execute("insert into [BonusCard] output Inserted.Number values(0, 'Стандартная')").fetchone()[0]
    connection.cursor().execute(f"update [Buyer] set [BonusCardNumber]='{ newCardId }' where [Id] = {userId} ")
    