# Generated by Django 3.2.14 on 2022-08-14 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0006_auto_20220813_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Seguro',
        ),
    ]
