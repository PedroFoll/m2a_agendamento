from random import randint

def formatCpf(a):
    a=list(a)
    a.insert(3,'.')
    a.insert(7,'.')
    a.insert(11,'-')
    return "".join(a)

while True:
    cpf=str(randint(10000000000,99999999999))
    cpf_valido = cpf[:9]
    multiplicador = 10
    soma = 0
    c = 1

    while c <= 2:
        for i in cpf_valido:
            i = int(i)
            soma+= i*multiplicador
            multiplicador -= 1
        multiplicador = 11
        valor = 11 - (soma %11)
        soma = 0
        if valor > 9:
            cpf_valido += '0'
        else:
            cpf_valido += str(valor)
        c += 1

    if cpf == cpf_valido:
        break

cpf_validado = cpf