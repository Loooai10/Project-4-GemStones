# Generated by Django 4.1.3 on 2022-12-06 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_uploadimage_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadimage',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.product'),
        ),
    ]