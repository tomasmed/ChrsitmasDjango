# Generated by Django 3.2.7 on 2021-12-02 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0004_gift_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='purchased',
            field=models.IntegerField(null=True),
        ),
    ]
