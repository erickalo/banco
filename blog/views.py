from django.shortcuts import render, redirect
from .models import Clientes 
from django.db import models
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def inicio(request):
    return render(request, 'blog/inicio.html', {})

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
    return render(request, 'blog/saque.html')


@login_required(login_url='/login')
def deposito(request):
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
                    messages.success(request, f'Deposito realizado. Saldo atual: {cli.saldo}')
                else:
                    messages.error(request, 'ERRO! Conta não encontrada!')
    return redirect('/depositar')


@login_required(login_url='/login')
def saque(request):
    if request.POST:
        conta = request.POST.get('conta')
        saque = request.POST.get('saque')
        if saque == '':
            messages.error(request, 'ERRO! Valor inválido')
        else:
            saque = int(saque)
            if Clientes.objects.filter(user=request.user, numero_conta=conta):
                cli = Clientes.objects.get(user=request.user, numero_conta=conta)
                if saque <= cli.saldo:
                    cli.saldo = cli.saldo - saque
                    cli.save()
                    messages.success(request, f'Saque realizado. Saldo atual: {cli.saldo}')
                else:
                    messages.error(request, 'ERRO! Saldo insuficiente')
            else:
                messages.error(request, 'ERRO! Conta não encontrada!')
    return redirect('/sacar')