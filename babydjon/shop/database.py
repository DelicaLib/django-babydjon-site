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
    

def getProductData(productId: int):
    productData = models.Product.objects.raw(f"select * from [Product] where [Id] = {productId}")[0]
    productData.Cost = int(productData.Cost)
    return productData

def getSizes(product):
    sizes = list(connection.cursor().execute(f"select [Size] from [Product] where [Title] = '{product.Title}' and [Producer] = {product.Producer.Id} and [Count] > 0 group by [Size] order by [Size]").fetchall())
    for i in range(len(sizes)):
        sizes[i] = sizes[i][0]
    return sizes

def getCartData(buyerId: int):
    sqlCart = """select
		[Product].[Id],
		[Product].[Title], 
        [Product].[ImageUrl],
		[Cart].[Count], 
		[Cart].[Count] * [Product].[Cost]
		from [Cart]
		join [Product] 
		on (
			[Cart].[Buyer] = {0}
			and [Cart].[Product] = [Product].[Id]) 
		order by [Product].[Title]"""
    sqlMoney = """
    select
	[Buyer].[Balance],
	[BonusCard].[Number]
	from [Buyer]
	left join [BonusCard] on (
		([BonusCard].[Number] = [Buyer].[BonusCardNumber]))
	where [Buyer].[Id] = {0}"""
    
    rawDataCart = connection.cursor().execute(sqlCart.format(buyerId)).fetchall()
    data = dict()
    data["data"] = []
    for i in rawDataCart:
        data["data"].append({"ProductId" : i[0],
                     "ProductTitle" : i[1],
                     "ProductImg" : i[2],
                     "Count" : i[3],
                     "Cost" : int(i[4])})
    rawDataMoney = connection.cursor().execute(sqlMoney.format(buyerId)).fetchone()
    data["addresses"] = getOfflineAddresses()
    data["user"] = dict()
    data["user"]["balance"] = int(rawDataMoney[0])
    data["user"]["bonus"] = rawDataMoney[1]
    return data

def getOfflineAddresses():
    addresses = []
    sqlAddresses = """select top 10
    [Address]
    from [OfflineStore]
    """
    rawAddresses = connection.cursor().execute(sqlAddresses).fetchall()
    for i in rawAddresses:
        addresses.append(i[0])
    return addresses