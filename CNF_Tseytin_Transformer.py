import re
from const import OPERACOES
import ajustar_formula as aj

formula = '((A&B)|(C&D)|(E&F)|(G&H))'
numero_variaveis_novas = 0

# CNF3 pega formulas do tipo A = B * C e coloca na CNF, onde * é |, &, <, > ou =. Pode transformar também A = !B.
def CNF3(formula):
    formula = formula.replace(" ","")
    delimitador = formula.find("=")
    p = formula[:delimitador]
    q = formula[delimitador+1:]
    if q[0] == '!':
        formulaNegativa = True
        for simbolo in q:
            if simbolo in OPERACOES:
                formulaNegativa = False
        if formulaNegativa:
            cnf = f'({q[1:]}|{p})&({q}|!{p})'
            return cnf.replace("!!","")
    x1,x2 = '', ''
    operador = ''
    cnf = formula
    for index,simbolo in enumerate(q):
        if simbolo not in OPERACOES:
            x1 += simbolo
        else:
            operador = simbolo
            x2 = q[index+1:]
            break
    if(operador == '&'):
        cnf = f"(!{x1}|!{x2}|{p})&({x1}|!{p})&({x2}|!{p})"
    elif(operador == '|'):
        cnf = f"({x1}|{x2}|!{p})&(!{x1}|{p})&(!{x2}|{p})"
    elif(operador == '>'):
        cnf = f"(!{x1}|{x2}|!{p})&({x1}|{p})&(!{x2}|{p})"
    elif(operador == '<'):
        cnf = f"(!{x2}|{x1}|!{p})&({x2}|{p})&(!{x1}|{p})"
    elif(operador == '='):
        cnf = f"(!{x1}|!{x2}|{p})&(!{x1}|{x2}|!{p})&({x1}|!{x2}|!{p})&({x1}|{x2}|{p})"
    return cnf.replace("!!","")

def listaSubformulas(formula,subformulas=['p0'],p='p0'):
    global numero_variaveis_novas
    contadorParenteses = 0
    if aj.verificarParentesesInicial(formula):
        if formula[0] == '!':
            numero_variaveis_novas += 1
            subformulas.append(f'p{numero_variaveis_novas-1}=!p{numero_variaveis_novas}')
            listaSubformulas(formula[2:-1],subformulas,f'p{numero_variaveis_novas}')
        else:
            formula = formula[1:-1]
    for index, simbolo in enumerate(formula):
        if(simbolo == '('):
            contadorParenteses += 1
        elif(simbolo == ')'):
            contadorParenteses -= 1
        if(contadorParenteses == 0 and simbolo in OPERACOES):
            operacao = simbolo
            esquerda_nomeada = formula[0:index]
            direita_nomeada = formula[index+1:]
            if (len(esquerda_nomeada)>2):
                esquerda = esquerda_nomeada
                numero_variaveis_novas += 1
                esquerda_nomeada = f'p{numero_variaveis_novas}'
                listaSubformulas(esquerda,subformulas,esquerda_nomeada)
            if (len(direita_nomeada)>2):
                direita = direita_nomeada
                numero_variaveis_novas += 1
                direita_nomeada = f'p{numero_variaveis_novas}'
                listaSubformulas(direita,subformulas,direita_nomeada)
            subformulas.append(f'{p}={esquerda_nomeada}{operacao}{direita_nomeada}')
    return subformulas
        

def transformacaoTseytin(formula,descritivo=False):
    # Se já tiver em CNF, não faz nada
    if re.match(r"(\(!?[a-zA-Z0-9]+(\|!?[a-zA-Z0-9]+)*?\)&?)+",formula):
        return formula
    if descritivo: print(f'A sua fórmula é: \n {formula}')
    formula = formula.replace('!!','')
    formula = formula.replace(' ','')
    formula = formula.replace('\n','')
    formula = aj.ajustarParenteses(formula)
    lista = listaSubformulas(formula)
    if descritivo: print(f'Depois de alguns ajustes ela fica: \n {formula}')
    if descritivo: print(f'As sub-fórmulas são: \n {lista}')
    cnfTseytin = ''
    for subFormula in lista:
        cnfTseytin += CNF3(subFormula)+'&'
    cnfTseytin = cnfTseytin[:-1]
    if descritivo:
        print(f'A transformação para CNF de Tseytin resultante é: \n {cnfTseytin}')
        print(f'A quantidade de clausulas foram: {cnfTseytin.count('&')+1}')
    return cnfTseytin

def mudarSintaxeCNF(formula):
    formula = formula.replace('|',' ')
    formula = formula.replace('&','\n')
    formula = formula.replace('(','')
    formula = formula.replace(')','')
    formula = formula.replace('!!','')
    return formula
