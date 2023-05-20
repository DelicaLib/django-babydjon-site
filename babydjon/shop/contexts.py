
import shop.models as models
from django.db import connection
from numpy import array

def menuContext():
    return [{"name": "Главная", "url" : "/"}, 
        {"name": "Каталог", "url" : "https://vk.com/zheleznyakov03"}, 
        {"name": "Адреса", "url" : "https://vk.com/zheleznyakov03"}, 
        {"name": "Контакты", "url" : ""},
        {"name": "Заказы", "url" : "https://vk.com/zheleznyakov03"}, 
        {"name": "Корзина", "url" : "https://vk.com/zheleznyakov03"},
        {"name": "Профиль", "url" : "https://vk.com/zheleznyakov03"}]
    
def generateSaleSlider():
    return [{"source" : "images/sale1.jpg",
        "url" : "https://delicalib.github.io/Lagem/",
        "id" : 0},
        {"source" : "images/sale2.jpg",
        "url" : "https://delicalib.github.io/Lagem/",
        "id" : 1},
        {"source" : "images/sale3.jpg",
        "url" : "https://delicalib.github.io/Lagem/",
        "id" : 2}]

def getCategories():
    return models.Category.objects.raw("select top 4 ROW_NUMBER() OVER(ORDER BY NEWID() ASC) - 1 as id ,[Title] from [Category] group by [Title]")

def getRandomSlideData(category):
    slides = []
    for item in connection.cursor().execute(f"select top 12 ROW_NUMBER() OVER(ORDER BY NEWID() ASC) - 1 as id , * from [Product] where [Product].[Category] in (select [Id] from [Category] where [Category].[Title] = \'{category}\')"):
        slides.append({
            "id" : item.id,
            "cost" : int(item.Cost),
            "imgUrl" : item.ImageUrl,
            "productUrl" : "https://www.youtube.com/watch?v=xfJC8WH7C5I",
            "name" : item.Title}
        )
    return slides

def generateRandomSliders():
    randomSliders = []
    randomSlidersFromSql = getCategories()
    for item in randomSlidersFromSql:
        randomSliders.append({
            "id" : item.id,
            "header" : item.Title,
            "slides" : getRandomSlideData(item.Title)
        })
    return randomSliders


def getCategoriesAndSubcategories():
    categoriesAndSubcategories = {}
    categories = connection.cursor().execute("select [Title] from [Category] group by [Title] order by [Title] asc")
    for item in categories:
        categoriesAndSubcategories[item.Title] = list(connection.cursor().execute(f"select [Subcategory] from [Category] where [Title] = '{item.Title}' group by [Subcategory] order by [Subcategory] asc"))
    return categoriesAndSubcategories

def indexContext():
    context = {
            "menu" : menuContext(),
            "currPage" : "Главная",
            "sales" : generateSaleSlider(),
            "randomSliders" : generateRandomSliders(),
            "categoriesAndSubcategories" : getCategoriesAndSubcategories()
            }
    return context
