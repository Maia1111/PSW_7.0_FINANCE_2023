from django.shortcuts import render, redirect
from perfil.models import Categoria, Conta
from .models import Valores
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta

def novo_valor(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        contas = Conta.objects.all()
        return render(request, 'novo_valor.html', {'categorias': categorias, 'contas': contas})
    
    elif request.method == 'POST':
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        conta = request.POST.get('conta')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')        
        tipo = request.POST.get('tipo')

    if  not valor:                                                                    
        messages.add_message(request, constants.ERROR, 'Campo valor não pode ser vazio')
        return redirect('/extrato/novo_valor')  
     
   
    if  not data:
        messages.add_message(request, constants.ERROR, 'Campo data não pode ser vazio')
        return redirect('/extrato/novo_valor')
    

    if len(descricao.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Campo descrição não pode ser vazio')
        return redirect('/extrato/novo_valor')
    
    
    if not tipo:
        messages.add_message(request, constants.ERROR, 'Campo tipo não pode ser vazio')
        return redirect('/extrato/novo_valor')       
    
    
    valores = Valores(valor=valor, 
                      categoria_id=categoria, 
                      conta_id=conta, 
                      data=data, 
                      descricao=descricao, 
                      tipo=tipo)
    valores.save()
    conta = Conta.objects.get(id=conta)
    
    if tipo == 'E':
        conta.valor += float(valor)
        conta.save()
        messages.add_message(request, constants.SUCCESS, 'Entrada cadastrada com sucesso')
    else:
        conta.valor -= float(valor)
        conta.save()
        messages.add_message(request, constants.SUCCESS, 'Saída cadastrada com sucesso')
    return redirect('/extrato/novo_valor')


def view_extrato(request):
    categorias = Categoria.objects.all()
    contas = Conta.objects.all()

    opcao_padrao = 0

    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')
    data_get = request.GET.get('periodo')    
    valores = Valores.objects.all()

    if conta_get:
        valores = valores.filter(conta_id=conta_get)
    
    if categoria_get:
        valores = valores.filter(categoria_id=categoria_get)
    
    if data_get:
        data_atual = datetime.now().date()
        dias = int(data_get)        
        data_filtro = data_atual - timedelta(days=dias)
        valores = valores.filter(data__gte=data_filtro, data__lte=data_atual)

    return render(request, 'view_extrato.html', {'valores': valores, 'categorias': categorias, 'contas': contas, 'opcao_padrao': opcao_padrao})



def zerar_filtro(request):
    return redirect('/extrato/view_extrato')