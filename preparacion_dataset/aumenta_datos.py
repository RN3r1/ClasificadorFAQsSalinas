#Puedes probar con estso valores, y te debería de dar un vector de 24
# frase = "Quiero ACCION un SUJETO COLOR nuevo"
#
# acciones = ['comprar rapido', 'vender']
# sujetos = ['auto veloz', 'helicóptero blindado', 'monociclo']
# colores = ['azul', 'rojo', 'verde', 'morado']
#
# valores = [acciones, sujetos, colores]
# huecos = ['ACCION', 'SUJETO', 'COLOR']

def aumentar_data_set(frase, huecos, valores):
    list_frase = frase.split(' ')
    resultado = []
    list_aux = list(list_frase)
    for i in range(len(huecos)):
        if i == 0:
            try:
                index = list_aux.index(huecos[i])
                for valor in valores[i]:
                    if (' ' in valor) == True:
                        list_aux_original = list(list_aux)
                        del list_aux[index]
                        list_aux = list_aux[:index]+valor.split(' ')+list_aux[index:]
                        resultado.append(list(list_aux))
                        list_aux = list(list_aux_original)

                    else:
                        list_aux[index] = valor
                        resultado.append(list(list_aux))
            except:
                resultado.append(list(list_aux))
                continue
        else:
            list_aux = list(resultado)
            resultado.clear()
            for j in range(len(list_aux)):
                try:
                    index = list_aux[j].index(huecos[i])
                    for valor in valores[i]:
                        if (' ' in valor) == True:
                            list_aux_original = list(list_aux[j])
                            del list_aux[j][index]
                            list_aux[j] = list_aux[j][:index] + valor.split(' ') + list_aux[j][index:]
                            resultado.append(list(list_aux[j]))
                            list_aux[j] = list_aux_original
                        else:
                            list_aux[j][index] = valor
                            resultado.append(list(list_aux[j]))
                except:
                    resultado.extend(list(list_aux))
                    break
    return resultado

# print(aumentar_data_set(frase, huecos, valores))
# print(len(aumentar_data_set(frase, huecos, valores)))