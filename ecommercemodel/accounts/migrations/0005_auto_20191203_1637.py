# Generated by Django 2.2.5 on 2019-12-03 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20191203_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(blank=True, default=False, verbose_name='Membro da equipe'),
        ),
    ]
