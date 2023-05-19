
import shop.models as models
from django.db import connection

def menuContext():
    return [{"name": "Главная", "url" : "/"}, 
        {"name": "Ассортимент", "url" : "https://vk.com/zheleznyakov03"}, 
        {"name": "Сообщения", "url" : "https://vk.com/zheleznyakov03"}, 
        {"name": "Друзья", "url" : "https://vk.com/zheleznyakov03"}, 
        {"name": "Форум", "url" : "https://vk.com/zheleznyakov03"}, 
        {"name": "Контакты", "url" : ""}, 
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
            "imgUrl" : "images/1-1.jpg",
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


def indexContext():
    context = {
            "menu" : menuContext(),
            "currPage" : "Главная",
            "sales" : generateSaleSlider(),
            "randomSliders" : generateRandomSliders()
            }
    return context
