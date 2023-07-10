from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from perfil.models import Categoria
import json
from django.contrib.messages import constants
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt



def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})



def update_valor_planejamento_categoria(request, id):      
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.filter(id=id)
    try:
        categoria.update(valor_planejamento=novo_valor)
        print('Sucesso')
        return JsonResponse({'status':'sucesso'})

    except Exception as e:
        return JsonResponse({'status':'erro', 'message': str(e)})

   

def ver_planejamento(request):   
    categorias = Categoria.objects.all()
    return render(request, 'ver_planejamento.html', {'categorias': categorias} )