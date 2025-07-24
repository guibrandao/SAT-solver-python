from const import OPERACOES

def adicionaString(palavra,modificacao,index):
	return palavra[:index] + modificacao + palavra[index:]

def ajustaListaOperacao(listaOperacao,index):
    for pos,item in enumerate(listaOperacao):
        if item > index:
            listaOperacao[pos] += 2
    return listaOperacao

#Função que verifica se a fórmula começa com parenteses. 
def verificarParentesesInicial(formula):
    contadorParenteses = 0
    if formula[:2] == '!(':
        formula = formula[1:]
    if formula[0] == '(':
        for index, simbolo in enumerate(formula):
            if(simbolo == '('):
                contadorParenteses += 1
            elif(simbolo == ')'):
                contadorParenteses -= 1
            if (contadorParenteses == 0 and index != len(formula)-1):
                return False
        return True
    else:
        return False

def ajustarParenteses(formula):
    ini,fim = '',''
    if verificarParentesesInicial(formula):
        if formula[0] != '!':
            formula = formula[1:-1]
            ini,fim = '(',')'
        else:
            formula = formula[2:-1]
            ini,fim = '!(',')'
    formulaAjustada = ''
    listaOrdemOperacoes = [[],[],[],[],[]]
    contadorParenteses = 0
    for index, simbolo in enumerate(formula):
        if simbolo == '(':
            contadorParenteses += 1
        elif simbolo == ')':
            contadorParenteses -= 1
        if simbolo in OPERACOES and contadorParenteses == 0:
            mappedOperations = {'&':4,'|':3,'<':2,'>':1,'=':0}
            listaOrdemOperacoes[mappedOperations[simbolo]].append(index)
    listaOperacoesPrimarias = [item for sublist in listaOrdemOperacoes for item in sublist]
    if len(listaOperacoesPrimarias) == 0:
        return ini+formula+fim
    while len(listaOperacoesPrimarias) > 1 :
        indexOp = listaOperacoesPrimarias.pop()
        listaOperacoesPrimarias = ajustaListaOperacao(listaOperacoesPrimarias,indexOp)
        # Procuramos onde botar parenteses na esquerda
        if formula[indexOp-1] != ')':
            if indexOp-2 >= 0:
                if formula[indexOp-2] == '!':
                    formula = adicionaString(formula,'(',indexOp-2)
                else:
                    formula = adicionaString(formula,'(',indexOp-1)
            else:
                formula = adicionaString(formula,'(',indexOp-1)
        else:
            for i in range(indexOp-1,-1,-1):
                if formula[i] == ')':
                    contadorParenteses += 1
                if formula[i] == '(':
                    contadorParenteses -= 1
                if contadorParenteses == 0:
                    if formula[i] == '!':
                        formula = adicionaString(formula,'(',i-1)
                    else:
                        formula = adicionaString(formula,'(',i)
                    break
        # Agora procuramos para a direitra
        if indexOp+3 <= len(formula):
            if formula[indexOp+2] != '(' and formula[indexOp+2:indexOp+4] != '!(':
                if formula[indexOp+2] == '!':
                    formula = adicionaString(formula,')',indexOp+4)
                else:
                    formula = adicionaString(formula,')',indexOp+3)
            else:
                if  formula[indexOp+2:indexOp+4] == '!(':
                    indexOp += 1
                for i in range(indexOp+2,len(formula)):
                    if formula[i] == ')':
                        contadorParenteses += 1
                    if formula[i] == '(':
                        contadorParenteses -= 1
                    if contadorParenteses == 0:
                        formula = adicionaString(formula,')',i+1)
                        break
        else:
            formula = adicionaString(formula,')',indexOp+3)
    indexOp = listaOperacoesPrimarias.pop()
    formulaAjustada = ini+ajustarParenteses(formula[:indexOp]) + formula[indexOp] + ajustarParenteses(formula[indexOp+1:])+fim
    return formulaAjustada