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
    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte=DIA_ATUAL+5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
    outras_contas_pagar = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_proximas_vencimento).exclude(id__in=contas_pagas)

    total_vencidas = len(contas_vencidas)
    total_proximas_vencimento = len(contas_proximas_vencimento)
    total_outras_contas_pagar = len(outras_contas_pagar)
    total_contas_pagas = len(contas_pagas)
    print(total_outras_contas_pagar)

    print(contas_vencidas)
    print(outras_contas_pagar)
    

    
   
   
    return render(request, 'ver_contas.html', {'contas': contas, 
                                               'contas_vencidas': contas_vencidas, 
                                               'contas_proximas_vencimento': contas_proximas_vencimento,
                                               'outras_contas_pagar':outras_contas_pagar,
                                               'total_vencidas': total_vencidas,
                                               'total_proximas_vencimento': total_proximas_vencimento,
                                               'total_outras_contas_pagar': total_outras_contas_pagar,
                                               'total_contas_pagas': total_contas_pagas,})



    
   