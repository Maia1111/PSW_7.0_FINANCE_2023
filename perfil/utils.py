from extrato.models import Valores
from datetime import datetime
from .models import Conta


def calcula_total(obj, campo):
    total = 0
    for item in obj:
        total += getattr(item, campo)
    return total



def calcula_equilibrio_financeiro():
    gastos_essenciasis = Valores.objects.filter(data__month=datetime.now().month).filter(tipo="S").filter(categoria__essencial=True)
    gastos_nao_essenciais = Valores.objects.filter(data__month=datetime.now().month).filter(tipo="S").filter(categoria__essencial=False)
    entradas_mensal = Valores.objects.filter(data__month=datetime.now().now().month).filter(tipo="E")
    try:    

        total_gastos_essencias = calcula_total(gastos_essenciasis, 'valor')
        total_gastos_nao_essenciais = calcula_total(gastos_nao_essenciais, 'valor') 
        total_entradas_mensal = calcula_total(entradas_mensal, 'valor')   
        total_gastos = total_gastos_essencias + total_gastos_nao_essenciais
        percentual_gastos_essencias = porcentagem_gastos_essenciais = (total_gastos_essencias * 100) / total_gastos
        percentual_gastos_nao_essenciais =porcentagem_gastos_nao_essenciais = (total_gastos_nao_essenciais * 100) / total_gastos
        total_gastos_mensal = total_gastos_essencias + total_gastos_nao_essenciais 
    except Exception as e:
        total_gastos_essencias = 0
        total_gastos_nao_essenciais = 0
        total_entradas_mensal = 0
        total_gastos = 0
        percentual_gastos_essencias = 0
        percentual_gastos_nao_essenciais = 0
        total_gastos_mensal = 0
        porcentagem_gastos_essenciais = 0
        porcentagem_gastos_nao_essenciais = 0
        entradas_mensal = 0
        saldo = 0
        print(e)


    
    
  
    saldo = total_entradas_mensal - total_gastos_mensal


    try:
        return  int(porcentagem_gastos_essenciais), int(porcentagem_gastos_nao_essenciais),  total_gastos_mensal, entradas_mensal, saldo
        
    except:
        porcentagem_gastos_essenciais = 0
        porcentagem_gastos_nao_essenciais = 0

        return  porcentagem_gastos_essenciais, porcentagem_gastos_nao_essenciais
    

def calcular_total_banco():
    contas = Conta.objects.all()
    total_bancos = 0
    for conta in contas:
        total_bancos += conta.valor
    return total_bancos
    



   
   
   

         
         



