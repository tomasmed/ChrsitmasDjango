# Generated by Django 3.2.7 on 2021-12-01 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0001_initial'),
        ('ads', '0005_ad_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='gift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gifts.gift'),
        ),
        migrations.AddField(
            model_name='fav',
            name='gift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gifts.gift'),
        ),
    ]