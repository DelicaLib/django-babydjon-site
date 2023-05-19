# Generated by Django 4.1.9 on 2023-05-19 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BonusCard',
            fields=[
                ('Number', models.BigAutoField(auto_created=True, db_index=True, primary_key=True, serialize=False, verbose_name='Number')),
                ('Bonus', models.PositiveIntegerField(blank=True, default=0, verbose_name='Bonus')),
                ('Type', models.CharField(blank=True, default='Стандартная', max_length=20, verbose_name='Type')),
            ],
            options={
                'db_table': 'BonusCard',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=30)),
                ('Subcategory', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'Category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('Id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('FullName', models.CharField(max_length=100, verbose_name='FullName')),
                ('Salary', models.PositiveIntegerField(default=0, verbose_name='Salary')),
                ('PhoneNumber', models.CharField(max_length=12, verbose_name='PhoneNumber')),
            ],
            options={
                'db_table': 'Courier',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('Id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('Title', models.CharField(max_length=100, verbose_name='Title')),
                ('Responsibilities', models.TextField(verbose_name='Responsibilities')),
            ],
            options={
                'db_table': 'JobTitle',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OfflineStore',
            fields=[
                ('Id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('Address', models.CharField(blank=True, max_length=200, verbose_name='Address')),
                ('OpeningTime', models.TimeField(verbose_name='OpeningTime')),
                ('ClosingTime', models.TimeField(verbose_name='ClosingTime')),
            ],
            options={
                'db_table': 'OfflineStore',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Producer',
            fields=[
                ('Id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('CompanyName', models.CharField(blank=True, max_length=50, verbose_name='CompanyName')),
                ('Address', models.CharField(blank=True, max_length=200, verbose_name='Address')),
                ('Mail', models.CharField(max_length=100, verbose_name='Email')),
            ],
            options={
                'db_table': 'Producer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('Id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('Email', models.CharField(max_length=100, verbose_name='Email')),
                ('PhoneNumber', models.CharField(max_length=12, verbose_name='PhoneNumber')),
                ('FullName', models.CharField(max_length=100, verbose_name='FullName')),
                ('Login', models.CharField(max_length=50, verbose_name='Login')),
                ('Password', models.CharField(max_length=70, verbose_name='Password')),
                ('Address', models.CharField(blank=True, max_length=200, verbose_name='Address')),
                ('Balance', models.PositiveIntegerField(default=0, verbose_name='Balance')),
                ('BonusCardNumber', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.bonuscard')),
            ],
            options={
                'db_table': 'Buyer',
            },
        ),
        migrations.CreateModel(
            name='Support',
            fields=[
                ('Id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('FullName', models.CharField(max_length=100, verbose_name='FullName')),
                ('Email', models.CharField(max_length=100, verbose_name='Email')),
                ('PhoneNumber', models.CharField(max_length=12, verbose_name='PhoneNumber')),
                ('Salary', models.PositiveIntegerField(blank=True, default=0, verbose_name='Cost')),
                ('Login', models.CharField(max_length=50, verbose_name='Login')),
                ('Password', models.CharField(max_length=70, verbose_name='Password')),
            ],
            options={
                'db_table': 'Support',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('Id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('Title', models.CharField(blank=True, max_length=50, verbose_name='Title')),
                ('Cost', models.PositiveIntegerField(blank=True, default=0, verbose_name='Cost')),
                ('Count', models.PositiveIntegerField(blank=True, default=0, verbose_name='Count')),
                ('Size', models.PositiveIntegerField(blank=True, default=0, verbose_name='Size')),
                ('Color', models.CharField(blank=True, max_length=50, verbose_name='Color')),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.category', verbose_name='Category')),
                ('Producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.producer', verbose_name='Producer')),
            ],
            options={
                'db_table': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('Id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('FullName', models.CharField(max_length=100, verbose_name='FullName')),
                ('PhoneNumber', models.CharField(max_length=12, verbose_name='PhoneNumber')),
                ('Email', models.CharField(max_length=100, verbose_name='Email')),
                ('Salary', models.PositiveIntegerField(default=0, verbose_name='Salary')),
                ('JobTitle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.jobtitle')),
                ('OfflineStore', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.offlinestore')),
            ],
            options={
                'db_table': 'Personal',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('Id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('Count', models.PositiveIntegerField(default=0, verbose_name='Count')),
                ('CostDelivery', models.PositiveIntegerField(blank=True, default=0, verbose_name='CostDelivery')),
                ('Type', models.CharField(blank=True, max_length=20, verbose_name='Type')),
                ('DeliveryDate', models.DateField(blank=True, verbose_name='DeliveryDate')),
                ('Retrieved', models.BooleanField(blank=True, verbose_name='Retrieved')),
                ('CostProduct', models.PositiveIntegerField(blank=True, default=0, verbose_name='CostProduct')),
                ('Bonuses', models.PositiveIntegerField(blank=True, default=0, verbose_name='Bonuses')),
                ('Buyer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.buyer')),
                ('Courier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.courier')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.product')),
            ],
            options={
                'db_table': 'Order',
            },
        ),
        migrations.CreateModel(
            name='OnlineStore',
            fields=[
                ('Address', models.UUIDField(primary_key=True, serialize=False, verbose_name='Address')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.product')),
                ('Support', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.support')),
            ],
            options={
                'db_table': 'OnlineStore',
            },
        ),
        migrations.CreateModel(
            name='OfflineStoreProducts',
            fields=[
                ('Id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='Id')),
                ('OfflineStore', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.offlinestore')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.product')),
            ],
            options={
                'db_table': 'OfflineStoreProducts',
            },
        ),
    ]
