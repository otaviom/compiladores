import util

file = open('fonte.txt', 'r')
fonte = file.readlines()
n_linha = 0
n_coluna = 0

def token(lexema, estado):

    token = util.tokens[estado]
    obj = {'lexema':lexema,'token':token,'tipo':'-'}

    if token == 'id':
        if lexema not in util.t_simbolos.keys():
            util.t_simbolos[lexema] = {'lexema':lexema,'token':token,'tipo':'-'}
        else:
            obj = util.t_simbolos[lexema]

    return obj

def proximo(estado_atual, simbolo):

    global n_linha
    global n_coluna

    if (estado_atual == 1 or estado_atual == 3) and simbolo == 'E':
        return util.t_transicoes[estado_atual][util.dic['E']]
    elif estado_atual == 7 and (not simbolo == '"') and (not simbolo == '\n'):
        return util.t_transicoes[estado_atual][util.dic['C']]
    elif estado_atual == 10 and (not simbolo == '}') and (not simbolo == '\n'):
        return util.t_transicoes[estado_atual][util.dic['C']]
    elif simbolo in util.digitos:
        return util.t_transicoes[estado_atual][util.dic['D']]
    elif simbolo in util.letras:
        return util.t_transicoes[estado_atual][util.dic['L']]
    elif simbolo not in util.dic.keys():
        return util.t_transicoes[estado_atual][util.dic['&']]
    else:
        return util.t_transicoes[estado_atual][util.dic[simbolo]]

def error(estado, n_linha, n_coluna):
    print('\nErro (' + str(n_linha+1) + ',' + str(n_coluna+1) +
            '): ' + util.erros[estado])

    return False

def lexema():

    global n_linha
    global n_coluna

    lex = ''
    linha = fonte[n_linha]

    estado_atual = 0
    estado_prox = 0

    while(True):

        simbolo = linha[n_coluna]
        estado_prox = proximo(estado_atual, simbolo)

        #print("\nEstado: " + str(estado_atual))
        #print("Simbolo: " + simbolo)
        #print("Lexema: " + lex)
        #print("Prox estado: " + str(estado_prox))

        if estado_prox == -1:
            if estado_atual in util.estados_final:
                return token(lex, estado_atual)
            else:
                return error(estado_atual, n_linha, n_coluna)
        elif estado_prox == 0:
            lex = ''
            if simbolo == '\n':
                n_linha = n_linha + 1
                try:
                    linha = fonte[n_linha]
                except:
                    return token(lex, 22)
                n_coluna = 0
            else:
                n_coluna = n_coluna + 1
        else:
            lex = lex + simbolo
            n_coluna = n_coluna + 1
            estado_atual = estado_prox


def main():

    while True:
        token = lexema()
        if token == False:
            break
        print(token)
        if token['token'] == 'EOF':
            break

    print('\nTabela de símbolos:')
    for i in util.t_simbolos:
        print(str(i) + ' : ' + str(util.t_simbolos[i]))

main()
