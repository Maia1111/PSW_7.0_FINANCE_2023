
def calcula_total(obj, campo):
    total = 0
    for item in obj:
        total += getattr(item, campo)
    return total



