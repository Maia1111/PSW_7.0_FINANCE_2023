from django.shortcuts import render, redirect
from django.http import HttpResponse
from perfil.models import Categoria



def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})

