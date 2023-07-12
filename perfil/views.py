from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Categoria, Conta
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total, calcula_equilibrio_financeiro, calcular_total_banco
from extrato.models import Valores
from datetime import datetime
from contas.models import ContaPaga, ContaPagar
from .import models




def home(request):
   valores = Valores.objects.filter(data__month=datetime.now().month)
   entradas = valores.filter(tipo='E')
   saidas = valores.filter(tipo='S')
   total_entradas = calcula_total(entradas, 'valor')
   total_saidas = calcula_total(saidas, 'valor')
   saldo = total_entradas - total_saidas

   MES_ATUAL = datetime.now().month
   DIA_ATUAL = datetime.now().day
   contas = ContaPagar.objects.all()
   banco = Conta.objects.all()
   contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
   contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
   contas_proximas_vencimento = contas.filter(dia_pagamento__lte=DIA_ATUAL+5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
   print(banco)
   total_vencidas = len(contas_vencidas)
   print(total_vencidas)
   total_proximas_vencimento = len(contas_proximas_vencimento) 
   print(total_proximas_vencimento) 
   total_contas_pagas = len(contas_pagas)
   print(total_contas_pagas) 

   porcentagem_gastos_essenciais, porcentagem_gastos_nao_essenciais, total_gastos_mensal, entradas_mensal, saldo  = calcula_equilibrio_financeiro()

   total_bancos = calcular_total_banco()
   
   print(porcentagem_gastos_essenciais)
   print(porcentagem_gastos_nao_essenciais)

   return render(request, 'home.html', {'total_entradas': total_entradas, 
                                        'total_saidas':total_saidas, 'saldo':saldo,
                                        'total_vencidas': total_vencidas, 
                                        'total_proximas_vencimento': total_proximas_vencimento, 
                                        'banco': banco,
                                        'porcentagem_gastos_essenciais': porcentagem_gastos_essenciais,
                                        'porcentagem_gastos_nao_essenciais': porcentagem_gastos_nao_essenciais,
                                        'total_bancos': total_bancos,
                                        })


def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    total_contas = 0
    for conta in contas:
        total_contas += conta.valor        
    return render(request, 'gerenciar.html',{'contas': contas, 'total_contas': total_contas, 'categorias': categorias})


def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or valor == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar')
        

    conta = Conta(apelido=apelido,
                   banco=banco, 
                   tipo=tipo, 
                   valor=valor,
                   icone=icone)
    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
    return redirect('/perfil/gerenciar')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso')
    return redirect('/perfil/gerenciar')


def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))
    cat = Categoria.objects.filter(categoria=nome).all()
    if len(cat) > 0:
        messages.add_message(request, constants.ERROR, 'Categoria já cadastrada')
        return redirect('/perfil/gerenciar')
    
    if len(nome.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Campo categoria não pode ser vazio')
        return redirect('/perfil/gerenciar')
   
    categoria = Categoria(categoria=nome, essencial=essencial)
    categoria.save()
    
    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar')

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial    
    categoria.save()
    return redirect('/perfil/gerenciar')

def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()
    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria=categoria)
        for valor in valores:
            total += valor.valor

        dados [categoria.categoria] = total
    print(dados.keys())
    print(dados.values())

  


    return render(request, 'dashboard.html', {'label': list(dados.keys()), 'dados': list(dados.values())})

    