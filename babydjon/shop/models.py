from django.db import models

class Category(models.Model):
    Title = models.CharField(max_length=30, db_column="Title")
    Subcategory = models.CharField(max_length=30, db_column="Subcategory")
    
    def __str__(self):
        return self.Title
    class Meta:
        db_table = 'Category'


class BonusCard(models.Model):
    Number = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Number', db_index=True, db_column="Number")
    Bonus = models.PositiveIntegerField(default=0, null=True, verbose_name='Bonus', db_column="Bonus")
    Type = models.CharField(max_length=20, null=True, verbose_name='Type', default="Стандартная", db_column="Type")
    
    def __str__(self):
        return self.Number
    class Meta:
        db_table = 'BonusCard'


class Buyer(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id', db_column="Id")
    Email = models.CharField(max_length=100, blank=False, verbose_name='Email', db_column="Email")
    PhoneNumber = models.CharField(max_length=12, blank=False, verbose_name='PhoneNumber', db_column="PhoneNumber")
    FullName = models.CharField(max_length=100, blank=False, verbose_name='FullName', db_column="FullName")
    Login = models.CharField(max_length=50, blank=False, verbose_name='Login', db_column="Login")
    Password = models.CharField(max_length=70, blank=False, verbose_name='Password', db_column="Password")
    Address = models.CharField(max_length=200, null=True, verbose_name='Address', db_column="Address")
    Balance = models.PositiveIntegerField(default=0, blank=False, verbose_name='Balance', db_column="Balance")
    BonusCardNumber = models.ForeignKey("BonusCard", on_delete=models.PROTECT, name="BonusCardNumber", null=True, db_column="BonusCardNumber")
    
    def __str__(self):
        return self.FullName
    class Meta:
        db_table = 'Buyer'
     
        
class Courier(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id', db_column="Id")
    FullName = models.CharField(max_length=100, blank=False, verbose_name='FullName', db_column="FullName")
    Salary = models.PositiveIntegerField(default=0, blank=False, verbose_name='Salary', db_column="Salary")
    PhoneNumber = models.CharField(max_length=12, blank=False, verbose_name='PhoneNumber', db_column="PhoneNumber")
    
    def __str__(self):
        return self.FullName
    class Meta:
        db_table = 'Courier'


class JobTitle(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id', db_column="Id")
    Title = models.CharField(max_length=100, blank=False, verbose_name='Title', db_column="Title")
    Responsibilities = models.TextField(verbose_name='Responsibilities', db_column="Responsibilities")

    def __str__(self):
        return self.Title
    class Meta:
        db_table = 'JobTitle'


class OfflineStore(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id', db_column="Id")
    Address = models.CharField(max_length=200, null=True, verbose_name='Address', db_column="Address")
    OpeningTime = models.TimeField(verbose_name='OpeningTime', db_column="OpeningTime")
    ClosingTime = models.TimeField(verbose_name='ClosingTime', db_column="ClosingTime")
    
    def __str__(self):
        return self.Address
    class Meta:
        db_table = 'OfflineStore'


class OfflineStoreProducts(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id', db_column="Id")
    Product = models.ForeignKey("Product", on_delete=models.PROTECT, name="Product", null=False, db_column="Product")
    OfflineStore = models.ForeignKey("OfflineStore", on_delete=models.PROTECT, name="OfflineStore", null=False, db_column="OfflineStore")
    
    def __str__(self):
        return self.Id
    class Meta:
        db_table = 'OfflineStoreProducts'
        

class OnlineStore(models.Model):
    Address = models.UUIDField(primary_key=True, name="Address", verbose_name='Address', db_column="Address")
    Product = models.ForeignKey("Product", on_delete=models.PROTECT, name="Product", null=False, db_column="Product")
    Support = models.ForeignKey("Support", on_delete=models.PROTECT, name="Support", null=False, db_column="Support")
    
    def __str__(self):
        return self.Address
    class Meta:
        db_table = 'OnlineStore'
        
        
class Order(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id', db_column="Id")
    Count = models.PositiveIntegerField(default=0, blank=False, verbose_name='Count', db_column="Count")
    Product = models.ForeignKey("Product", on_delete=models.PROTECT, name="Product", null=False, db_column="Product")
    Buyer = models.ForeignKey("Buyer", on_delete=models.PROTECT, name="Buyer", null=False, db_column="Buyer")
    CostDelivery = models.PositiveIntegerField(default=0, null=True, verbose_name="CostDelivery", db_column="CostDelivery")
    Type = models.CharField(max_length=20, null=True, verbose_name="Type", db_column="Type")
    Courier = models.ForeignKey("Courier", on_delete=models.PROTECT, name="Courier", null=True, db_column="Courier")
    DeliveryDate = models.DateField(null=True, verbose_name="DeliveryDate", db_column="DeliveryDate")
    Retrieved = models.BooleanField(null=True, verbose_name="Retrieved", db_column="Retrieved")
    CostProduct = models.PositiveIntegerField(default=0, null=True, verbose_name="CostProduct", db_column="CostProduct")
    Bonuses = models.PositiveIntegerField(default=0, null=True, verbose_name="Bonuses", db_column="Bonuses")
    
    def __str__(self):
        return self.Id
    class Meta:
        db_table = 'Order'
        
        
class Personal(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id', db_column="Id")
    FullName = models.CharField(max_length=100, blank=False, verbose_name='FullName', db_column="FullName")
    PhoneNumber = models.CharField(max_length=12, blank=False, verbose_name='PhoneNumber', db_column="PhoneNumber")
    Email = models.CharField(max_length=100, blank=False, verbose_name='Email', db_column="Email")
    Salary = models.PositiveIntegerField(default=0, blank=False, verbose_name='Salary', db_column="Salary")
    OfflineStore = models.ForeignKey("OfflineStore", on_delete=models.PROTECT, name="OfflineStore", null=False, db_column="OfflineStore")
    JobTitle = models.ForeignKey("JobTitle", on_delete=models.PROTECT, name="JobTitle", null=False, db_column="JobTitle")
        
    def __str__(self):
        return self.FullName
    class Meta:
        db_table = 'Personal'
        
class Producer(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id', db_column="Id")
    CompanyName = models.CharField(max_length=50, null=True, verbose_name='CompanyName', db_column="CompanyName")
    Address = models.CharField(max_length=200, null=True, verbose_name='Address', db_column="Address")
    Mail = models.CharField(max_length=100, blank=False, verbose_name='Email', db_column="Mail")
        
    def __str__(self):
        return self.CompanyName
    class Meta:
        db_table = 'Producer'
        
class Product(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id', db_column="Id")
    Title = models.CharField(max_length=50, null=True, verbose_name="Title", db_column="Title")
    Cost = models.PositiveIntegerField(default=0, null=True, verbose_name="Cost", db_column="Cost")
    Count = models.PositiveIntegerField(default=0, null=True, verbose_name="Count", db_column="Count")
    Size = models.PositiveIntegerField(default=0, null=True, verbose_name="Size", db_column="Size")
    Color = models.CharField(max_length=50, null=True, verbose_name="Color", db_column="Color")
    Category = models.ForeignKey("Category", on_delete=models.PROTECT, name="Category", verbose_name="Category", db_column="Category")
    Producer = models.ForeignKey("Producer", on_delete=models.PROTECT, name="Producer", verbose_name="Producer", db_column="Producer")
    ImageUrl = models.ImageField(upload_to="img/%Y-%m-%d/", name="ImageUrl", verbose_name="ImageUrl", null=True, db_column="ImageUrl")
        
    def __str__(self):
        return self.Title
    class Meta:
        db_table = 'Product'
        

class Support(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id', db_column="Id")
    FullName = models.CharField(max_length=100, blank=False, verbose_name='FullName', db_column="FullName")
    Email = models.CharField(max_length=100, blank=False, verbose_name='Email', db_column="Email")
    PhoneNumber = models.CharField(max_length=12, blank=False, verbose_name='PhoneNumber', db_column="PhoneNumber")
    Salary = models.PositiveIntegerField(default=0, null=True, verbose_name="Cost", db_column="Salary")
    Login = models.CharField(max_length=50, blank=False, verbose_name='Login', db_column="Login")
    Password = models.CharField(max_length=70, blank=False, verbose_name='Password', db_column="Password")
    
    def __str__(self):
        return self.FullName
    class Meta:
        db_table = 'Support'
        
        
class Cart(models.Model):
    Id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id', db_column="Id")
    Buyer = models.ForeignKey("Buyer", on_delete=models.PROTECT, name="Buyer", null=False, db_column="Buyer")
    Product = models.ForeignKey("Product", on_delete=models.PROTECT, name="Product", null=False, db_column="Product")
    Count = models.PositiveIntegerField(default=0, null=True, verbose_name="Count", db_column="Count")
    
    def __str__(self):
        return self.Id
    class Meta:
        db_table = 'Cart'