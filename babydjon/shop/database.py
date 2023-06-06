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
    
    if password == user.Password:
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
	[BonusCard].[Bonus]
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

def deleteOneProductFromCart(productId : int, buyerId : int):
    sqlQuery = """delete [Cart] 
    where [Product] = {0} and
    [Buyer] = {1}"""
    deletedCount = connection.cursor().execute(sqlQuery.format(productId, buyerId)).rowcount
    return deletedCount

def deleteProductsFromCart(productsId, buyerId : int):
    sqlQuery = """delete [Cart] 
    where [Product] in ({0}) and
    [Buyer] = {1}"""
    productsId = str(productsId).split(",")
    productsId[0] = productsId[0].replace("[","")
    productsId[len(productsId) - 1] = productsId[len(productsId) - 1].replace("]","")
    deletedCount = connection.cursor().execute(sqlQuery.format(str(",".join(productsId)), buyerId)).rowcount
    return deletedCount

def getSumCostInCart(productsId : list, buyerId : int):
    sqlQuery = """select sum([Product].[Cost] * [Cart].[Count]) 
from [Product] 
join [Cart] 
    on ([Cart].[Product] = [Product].[Id] and 
        [Product].[Id] in ({0}) 
        and [Cart].[Buyer] = {1})"""
    sumCost = connection.cursor().execute(sqlQuery.format(str(",".join(map(str,productsId))), buyerId)).fetchone()[0]
    return sumCost

def getBonusCardBalance(buyerId : int):
    sqlQuery = """declare @BonusCardNumber int

set @BonusCardNumber = (select [Buyer].[BonusCardNumber] from [Buyer] where [Id] = {0})
if (@BonusCardNumber is not null)
begin
	select concat('-', (select [BonusCard].[Bonus] from [BonusCard] where [Number] = @BonusCardNumber))
end
else
begin
	select 'отсутстует карта'
end"""
    message = connection.cursor().execute(sqlQuery.format(buyerId)).fetchone()[0]
    return message

def updateCartCount(buyerId : int, productId : int, count : int):
    result = {"cost" : 0, 
              "updateCount" : 0}
    sqlUpdateQuery = """update [Cart] 
set [Count] = {0}
    where [Buyer] = {1} and 
        [Product] = {2}"""
    sqlGetCostQuery = """select [Product].[Cost] * [Cart].[Count] 
from [Cart]
join [Product] on (
	[Product].[Id] = [Cart].[Product] and
	[Cart].[Product] = {0} and
	[Cart].[Buyer] = {1})"""
    result["updateCount"] = connection.cursor().execute(sqlUpdateQuery.format(count, buyerId, productId)).rowcount
    result["cost"] = int(connection.cursor().execute(sqlGetCostQuery.format(productId, buyerId)).fetchone()[0])
    return result