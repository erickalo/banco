# Generated by Django 2.2.12 on 2020-06-15 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_clientes_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes',
            name='saldo',
        ),
    ]
