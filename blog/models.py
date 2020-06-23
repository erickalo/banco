from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Clientes(models.Model):
    nome = models.CharField(max_length=50)
    cod_agencia = models.IntegerField()
    numero_conta = models.AutoField(primary_key=True)
    saldo = models.DecimalField(max_digits=9, decimal_places=2)
    data_criacao = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
