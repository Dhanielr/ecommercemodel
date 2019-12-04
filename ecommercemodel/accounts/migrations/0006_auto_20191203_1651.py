# Generated by Django 2.2.5 on 2019-12-03 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20191203_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, help_text='Indica que este usuário está ativo para logar.', verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(blank=True, default=False, help_text='Indica que este usuário é membro da equipe de administradores.', verbose_name='Membro da equipe'),
        ),
    ]
