from django.shortcuts import render, redirect
from .models import Clientes 
from django.db import models
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.

def inicio(request):
    return render(request, 'blog/inicio.html', {})

def erro(request):
    return render(request, 'blog/erro.html', {})

@login_required(login_url='/login')
def clientes(request):
    clientes = Clientes.objects.filter(user=request.user).order_by('numero_conta')
    return render(request, 'blog/clientes.html', {'clientes': clientes})


def logout_user(request):
    logout(request)
    return redirect('/')


def login_user(request):
    return render(request, 'blog/login.html')


@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou senha inválido')
    return redirect('/login/')


@login_required(login_url='/login')
def depositar(request):
    return render(request, 'blog/deposito.html')


@login_required(login_url='/login')
def sacar(request):
    numero_conta = request.GET.get('id')
    return render(request, 'blog/saque.html', {'numero_conta': numero_conta})


@login_required(login_url='/login')
def deposito(request):
    try:
        if request.POST:
            conta = request.POST.get('conta')
            agencia = request.POST.get('agencia')
            deposito = request.POST.get('deposito')
            if deposito == '':
                messages.error(request, 'ERRO! Valor inválido')
            else:
                deposito = int(deposito)
                if conta == '' or agencia == '':
                    messages.error(request, 'ERRO! Conta não encontrada!')
                else:
                    if Clientes.objects.filter(user=request.user, cod_agencia=agencia, numero_conta=conta):
                        cli = Clientes.objects.get(user=request.user, cod_agencia=agencia, numero_conta=conta)
                        cli.saldo = deposito + cli.saldo
                        cli.save()
                        messages.success(request, f'Realizado deposito de {deposito:.2f} reais. Saldo atual: {cli.saldo}')
                    else:
                        messages.error(request, 'ERRO! Conta não encontrada!')
        return redirect('/clientes')
    except:
        return redirect('/erro')


@login_required(login_url='/login')
def saque(request):
    if request.POST:
        try:
            saque = request.POST.get('saque')
            conta = request.POST.get('conta')
            if saque == '':
                messages.error(request, 'ERRO! Valor inválido')
            else:
                saque = int(saque)
                if Clientes.objects.filter(user=request.user, numero_conta=conta):
                    cli = Clientes.objects.get(user=request.user, numero_conta=conta)
                    if saque <= cli.saldo:
                        cli.saldo = cli.saldo - saque
                        cli.save()
                        messages.success(request, f'Realizado saque de {saque:.2f} reais. Saldo atual: {cli.saldo}')
                    else:
                        messages.error(request, 'ERRO! Saldo insuficiente')
                else:
                    messages.error(request, 'ERRO! Conta não encontrada!')
        except Exception as erro:
            messages.error(request, f'ERRO! {erro}')
        finally:
            return redirect('/clientes')


def dolar(request):
    conta = request.POST.get('conta')
    r = requests.get('https://economia.awesomeapi.com.br/json/all/USD-BRL')
    d = r.json()
    dolar = d['USD']
    dolar['high'] = float(dolar['high'])
    c = round(dolar['high'], 2)
    cli = Clientes.objects.get(user=request.user)
    conv = float(cli.saldo) / c
    conv = int(conv)
    result = {'vdh': c, 'conv': conv}
    return render(request, 'blog/dolar.html', {'result': result})
