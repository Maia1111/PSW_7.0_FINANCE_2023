from django.shortcuts import render, redirect
from perfil.models import Categoria, Conta
from .models import Valores
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants

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
