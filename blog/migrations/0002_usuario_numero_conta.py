# Generated by Django 2.2.12 on 2020-06-12 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='numero_conta',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]