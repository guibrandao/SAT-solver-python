import sys
import re
import CNF_Tseytin_Transformer as transform
from copy import deepcopy

true_vars = set() #Conjunto de variáveis verdadeiras
false_vars = set() #Conjunto de variáveis falsas
n_props, n_splits = 0, 0 #Contagem de propagaçoes unitárias no nosso problema, Contagem de pontos de decisão

def print_cnf(cnf): #Recebe uma lista de strings (cláusulas)
    s = ''
    for i in cnf:
        if len(i) > 0: #Verificamos se a cláusula não é vazia
            t = i.replace('  ', ' ') 
            s += '(' + t.replace(' ', '+') + ')' #Caso não seja vazia, substitui todos os ' ' por '+' e a colocamos a cláusula entre parênteses. Depois disso, concatena a cláusula recem formatada com as anteriores.
    if s == '': #Verificamos se a string continua vazia após o novo formato (isso significa que a entrada cnf era vazia, logicamente isso é verdadeiro).
        s = '()' #Definimos s como '()' para indicar que temos uma fórmula vazia
    print(s)

def isUnit(cnfLine):
    return ' ' not in cnfLine

def removeEmpty(cnfLine):
    if '  ' in cnfLine:
        return cnfLine.replace('  ', ' ') 
    return cnfLine

def isLiteral(word):
    return re.match(r"([a-zA-Z])(\d*)",word)

def extractLiterals(input_cnf):
    input = input_cnf.replace('\n',' ').replace('!','')
    return [i for i in set(input.split()) if isLiteral(i)]

def unit_propagation(cnf, new_true, new_false):
    global true_vars, false_vars, n_props, n_splits
    units = [i for i in cnf if isUnit(i)]  #Armazena em lista todas as cláusulas com um único literal
    units = list(set(units)) #Novamente removemos cláusulas duplicadas
    if len(units): #Verificamos se de fato existem cláusulas unitárias
        for unit in units:
            n_props += 1 #Incrementamos em 1 para cada cláusula unitária que encontrarmos
            if '!' in unit: 
                false_vars.add(unit[1:])
                new_false.append(unit[1:]) #Se houver um simbolo de negação, adicionamos a variável (chamemos de A, por exemplo) ao conjunto de variáveis falsas e a lista de atribuições falsas
                i = 0 #Começamos a percorrer a fórmula
                while True:
                    removeEmpty(cnf[i])
                    if unit in cnf[i].split(): #Aqui indica que o literal !A ocorre na iesima clausula
                        cnf.remove(cnf[i]) #Podemos remover essa clausula, ja que A é falso, i.e. !A é verdadeiro, logo a clausula toda é verdadeira
                        i -= 1
                    elif unit[1:] in cnf[i].split(): #Aqui indica que o literal A ocorre na iesima clausula
                        cnf[i] = cnf[i].replace(unit[1:], '').strip() #Removemos o literal A da clausula, ja que este é falso e nao pode mais contribuir pra satisfatibilidade
                    i += 1
                    if i >= len(cnf): 
                        break
            else: 
                true_vars.add(unit)
                new_true.append(unit) #Se nao houver um simbolo de negaçao, adicionamos a variavel ao conjunto de variaveis verdadeiras e a lista de atribuições verdadeiras
                i = 0 #Começamos a percorrer a fórmula
                while True:
                    removeEmpty(cnf[i])
                    if '!'+unit in cnf[i].split():
                        cnf[i] = cnf[i].replace('!'+unit, '').strip() #Se ocorrer o literal !A, este é falso, logo removemos da clausula
                        removeEmpty(cnf[i])
                    elif unit in cnf[i].split():
                        cnf.remove(cnf[i]) #Se ocorrer o literal A, podemos remover a clausula inteira
                        i -= 1
                    i += 1
                    if i >= len(cnf):
                        break
    print('Cláusulas unitárias =', units) #Imprimimos todas cláusulas unitárias
    print('FNC após propagação unitária = ', end = '')
    print_cnf(cnf) #Imprimimos a fórmula resultante após fazer a propagaçao unitária


def backtracking(new_true,new_false):
    global true_vars, false_vars
    for i in new_true:
            true_vars.remove(i)
    for i in new_false:
            false_vars.remove(i)

def solve(cnf,literals):
    print('\nFNC = ', end='') 
    print_cnf(cnf) #Imprimimos a fórmula.
    new_true = []
    new_false = [] #Criamos essas listas para armazenarmos as atribuições feitas em cada nível. Será necessário para fazer o backtracking caso precise.
    global true_vars, false_vars, n_props, n_splits #Usaremos as versões globais das variáveis definidas no começo
    true_vars = set(true_vars)
    false_vars = set(false_vars)
    n_splits += 1 #Incrementa o número de decisões
    cnf = list(set(cnf)) #Ao transformar em conjunto e depois voltar para lista, removemos as possíveis cláusulas duplicadas
    unit_propagation(cnf, new_true, new_false)

    if len(cnf) == 0:
        return True #Se chegarmos na fórmula vazia, retornamos verdadeiro
    
    if sum(len(clause)==0 for clause in cnf): #Se encontramos uma cláusula vazia...
        backtracking(new_true,new_false)
        print('Cláusula vazia encontrada, voltando...')
        return False #Indicamos que esse ramo nao levou a uma solução

    #O proximo passo é olhar as clausulas não unitárias
    literals = extractLiterals(' '.join(cnf)) #Extraimos todas os literais que nao tem negação
    x = literals[0] #Escolhe a primeira variável nao atribuída da lista
    if solve(deepcopy(cnf)+[x], deepcopy(literals)): #Chamamos recursivamente nossa função solve considerando x como literal verdadeiro, se for verdadeiro, retornamos verdade
        return True
    elif solve(deepcopy(cnf)+['!'+x], deepcopy(literals)): #Se nao for verdadeiro, testamos o caso que x é falso, se for verdadeiro, achamos uma solução
        return True
    else: #Se nao encontrarmos uma solução em nenhum dos casos, então nao é possivel e fazemos backtracking
        backtracking(new_true,new_false)
        return False 

def verificaSintaxeETransforma(cnf):
    for simbolo in cnf:
        if simbolo in transform.OPERACOES:
            cnf = transform.transformacaoTseytinDescritiva(cnf)
            return transform.mudarSintaxeCNF(cnf)
    return transform.mudarSintaxeCNF(cnf)

def dpll(): #Aqui é onde a execução ocorre
    global true_vars, false_vars, n_props, n_splits #Usamos as variáveis globais
    if len(sys.argv)<2:
        print('Nenhum arquivo selecionado. Digite uma fórmula ou um caminho válido:')
        print('Escreva a sua fórmula usando os seguintes simbolos: ')
        print('> := ->; \n < := <-; \n = := <->; \n & := ∧; \n | := v; \n ! := ¬')
        input_cnf = input('Fórmula ou caminho: ')
        if '/' in input_cnf:
            input_cnf = open(input_cnf,'r').read()
    else:
        input_cnf = open(sys.argv[1], 'r').read() #Damos como entrada um arquivo cujo nome damos
    input_cnf = verificaSintaxeETransforma(input_cnf)
    literals = extractLiterals(input_cnf)
    cnf = input_cnf.splitlines() #Definimos nossa formula em FNC onde cada clausula está separada em cada linha no arquivo de entrada
    if solve(cnf, literals): #Chamamos nosa funçao que resolve a fórmula dada
        print('\nNúmero de Decisões =', n_splits)
        print('Propagaões Unitárias =', n_props)
        print('\nResultado: SATISFATÍVEL')
        print('Solução:')
        for i in true_vars:
            print('\t\t'+i, '= Verdadeiro')
        for i in false_vars:
            print('\t\t'+i, '= Falso') #Se a formula é satisfatível ela imprime 'SATISFATÍVEL' e mostra qual atribuição foi feita, numero de decisões que foram tomadas e quantas propagações unitárias foram feitas
    else:
        print('\nAlcançamos o nó inicial!') #Aqui diz que fizemos todas as decisões possiveis até o ponto inicial sem encontrar solução
        print('Número de Decisões =', n_splits)
        print('Propagações Unitárias =', n_props)
        print('\nResultado: INSATISFATÍVEL') #Se a formula não é satisfatível ela imprime 'INSATISFATÍVEL' e imprime numero de decisões que foram tomadas e quantas propagações unitárias foram feitas
    print()

if __name__=='__main__':
    dpll()
