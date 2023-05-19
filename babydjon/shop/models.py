from django.db import models

class Category(models.Model):
    Title = models.CharField(max_length=30)
    Subcategory = models.CharField(max_length=30)
    
    def __str__(self):
        return self.Title
    class Meta:
        db_table = 'Category'
        managed = False


class BonusCard(models.Model):
    Number = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Number', db_index=True)
    Bonus = models.PositiveIntegerField(default=0, blank=True, verbose_name='Bonus')
    Type = models.CharField(max_length=20, blank=True, verbose_name='Type', default="Стандартная")
    
    def __str__(self):
        return self.Number
    class Meta:
        db_table = 'BonusCard'
        managed = False


class Buyer(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')
    Email = models.CharField(max_length=100, blank=False, verbose_name='Email')
    PhoneNumber = models.CharField(max_length=12, blank=False, verbose_name='PhoneNumber')
    FullName = models.CharField(max_length=100, blank=False, verbose_name='FullName')
    Login = models.CharField(max_length=50, blank=False, verbose_name='Login')
    Password = models.CharField(max_length=70, blank=False, verbose_name='Password')
    Address = models.CharField(max_length=200, blank=True, verbose_name='Address')
    Balance = models.PositiveIntegerField(default=0, blank=False, verbose_name='Balance')
    BonusCardNumber = models.ForeignKey("BonusCard", on_delete=models.PROTECT, name="BonusCardNumber", null=True)
    
    def __str__(self):
        return self.FullName
    class Meta:
        db_table = 'Buyer'
     
        
class Courier(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')
    FullName = models.CharField(max_length=100, blank=False, verbose_name='FullName')
    Salary = models.PositiveIntegerField(default=0, blank=False, verbose_name='Salary')
    PhoneNumber = models.CharField(max_length=12, blank=False, verbose_name='PhoneNumber')
    
    def __str__(self):
        return self.FullName
    class Meta:
        db_table = 'Courier'
        managed = False


class JobTitle(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')
    Title = models.CharField(max_length=100, blank=False, verbose_name='Title')
    Responsibilities = models.TextField(verbose_name='Responsibilities')

    def __str__(self):
        return self.Title
    class Meta:
        db_table = 'JobTitle'
        managed = False


class OfflineStore(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')
    Address = models.CharField(max_length=200, blank=True, verbose_name='Address')
    OpeningTime = models.TimeField(verbose_name='OpeningTime')
    ClosingTime = models.TimeField(verbose_name='ClosingTime')
    
    def __str__(self):
        return self.Address
    class Meta:
        db_table = 'OfflineStore'
        managed = False


class OfflineStoreProducts(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')
    Product = models.ForeignKey("Product", on_delete=models.PROTECT, name="Product", null=False)
    OfflineStore = models.ForeignKey("OfflineStore", on_delete=models.PROTECT, name="OfflineStore", null=False)
    
    def __str__(self):
        return self.Id
    class Meta:
        db_table = 'OfflineStoreProducts'
        

class OnlineStore(models.Model):
    Address = models.UUIDField(primary_key=True, name="Address", verbose_name='Address')
    Product = models.ForeignKey("Product", on_delete=models.PROTECT, name="Product", null=False)
    Support = models.ForeignKey("Support", on_delete=models.PROTECT, name="Support", null=False)
    
    def __str__(self):
        return self.Address
    class Meta:
        db_table = 'OnlineStore'
        
        
class Order(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')
    Count = models.PositiveIntegerField(default=0, blank=False, verbose_name='Count')
    Product = models.ForeignKey("Product", on_delete=models.PROTECT, name="Product", null=False)
    Buyer = models.ForeignKey("Buyer", on_delete=models.PROTECT, name="Buyer", null=False)
    CostDelivery = models.PositiveIntegerField(default=0, blank=True, verbose_name="CostDelivery")
    Type = models.CharField(max_length=20, blank=True, verbose_name="Type")
    Courier = models.ForeignKey("Courier", on_delete=models.PROTECT, name="Courier", null=True)
    DeliveryDate = models.DateField(blank=True, verbose_name="DeliveryDate")
    Retrieved = models.BooleanField(blank=True, verbose_name="Retrieved")
    CostProduct = models.PositiveIntegerField(default=0, blank=True, verbose_name="CostProduct")
    Bonuses = models.PositiveIntegerField(default=0, blank=True, verbose_name="Bonuses")
    
    def __str__(self):
        return self.Id
    class Meta:
        db_table = 'Order'
        
        
class Personal(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')
    FullName = models.CharField(max_length=100, blank=False, verbose_name='FullName')
    PhoneNumber = models.CharField(max_length=12, blank=False, verbose_name='PhoneNumber')
    Email = models.CharField(max_length=100, blank=False, verbose_name='Email')
    Salary = models.PositiveIntegerField(default=0, blank=False, verbose_name='Salary')
    OfflineStore = models.ForeignKey("OfflineStore", on_delete=models.PROTECT, name="OfflineStore", null=False)
    JobTitle = models.ForeignKey("JobTitle", on_delete=models.PROTECT, name="JobTitle", null=False)
        
    def __str__(self):
        return self.FullName
    class Meta:
        db_table = 'Personal'
        
class Producer(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')
    CompanyName = models.CharField(max_length=50, blank=True, verbose_name='CompanyName')
    Address = models.CharField(max_length=200, blank=True, verbose_name='Address')
    Mail = models.CharField(max_length=100, blank=False, verbose_name='Email')
        
    def __str__(self):
        return self.CompanyName
    class Meta:
        db_table = 'Producer'
        managed = False
        
class Product(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')
    Title = models.CharField(max_length=50, blank=True, verbose_name="Title")
    Cost = models.PositiveIntegerField(default=0, blank=True, verbose_name="Cost")
    Count = models.PositiveIntegerField(default=0, blank=True, verbose_name="Count")
    Size = models.PositiveIntegerField(default=0, blank=True, verbose_name="Size")
    Color = models.CharField(max_length=50, blank=True, verbose_name="Color")
    Category = models.ForeignKey("Category", on_delete=models.PROTECT, name="Category", verbose_name="Category")
    Producer = models.ForeignKey("Producer", on_delete=models.PROTECT, name="Producer", verbose_name="Producer")
        
    def __str__(self):
        return self.Title
    class Meta:
        db_table = 'Product'
        

class Support(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')
    FullName = models.CharField(max_length=100, blank=False, verbose_name='FullName')
    Email = models.CharField(max_length=100, blank=False, verbose_name='Email')
    PhoneNumber = models.CharField(max_length=12, blank=False, verbose_name='PhoneNumber')
    Salary = models.PositiveIntegerField(default=0, blank=True, verbose_name="Cost")
    Login = models.CharField(max_length=50, blank=False, verbose_name='Login')
    Password = models.CharField(max_length=70, blank=False, verbose_name='Password')
    
    def __str__(self):
        return self.FullName
    class Meta:
        db_table = 'Support'