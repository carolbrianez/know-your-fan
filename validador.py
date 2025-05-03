import re

def validar_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * ((i+1) - j) for j in range(i))
        digito = (soma * 10 % 11) % 10
        if int(cpf[i]) != digito:
            return False
    return True

def validar_link_social(link: str) -> bool:
    padrao = r'https:\/\/(www\.)?(instagram\.com|twitter\.com|tiktok\.com|x\.com)\/[a-zA-Z0-9_.]+\/?'
    return re.match(padrao, link.strip()) is not None
