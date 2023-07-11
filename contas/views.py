from django.shortcuts import render, redirect
from django.http import HttpResponse
from perfil.models import Categoria
from .models import ContaPagar, ContaPaga
from django.contrib.messages import constants
from django.contrib import messages
from datetime import datetime



def definir_contas(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html', {'categorias': categorias})
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')        

        if  not titulo.strip():
            messages.add_message(request, messages.ERROR, 'Título é obrigatório!')
            return redirect('/contas/definir_contas')
        
        if not descricao.strip():
            messages.add_message(request, messages.ERROR, 'Descrição é obrigatório!')
            return redirect('/contas/definir_contas')
        
        if not valor:
            messages.add_message(request, messages.ERROR, 'Valor é obrigatório!')
            return redirect('/contas/definir_contas')

        conta = ContaPagar(titulo=titulo, 
                           categoria_id=categoria, 
                           descricao=descricao, 
                           valor=valor,
                            dia_pagamento=dia_pagamento)
        conta.save()
        messages.add_message(request, messages.SUCCESS, 'Conta cadastrada com sucesso!')
        return redirect('/contas/definir_contas')


def ver_contas(request):

    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    contas = ContaPagar.objects.all()
    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
    contas_vencidas = ContaPagar.objects.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    print(contas_vencidas)
    

    
   
   
    return render(request, 'ver_contas.html', {'contas': contas})



    
   