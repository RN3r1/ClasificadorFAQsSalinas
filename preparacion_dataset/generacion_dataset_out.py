"""Clase que te ayuda a 'inflar' tu dataset"""
import unicodedata
import pandas as pd
from preparacion_dataset.aumenta_datos import aumentar_data_set
from preparacion_dataset.aumentar_datos_tags import aumentar_data_set_tags


def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

#Declaración de los parámetros para inflar nuestro dataset
#Frase: Es la frase base donde los campos que queremos sustituir están en mayúsculas
#Hueco: Es el campo que queremos sustituir, recuerda que debe de ir en mayúscula
#Valores: Son los valores con los que quieres sustituir los huecos
#IMPORTANTE: el orden de arreglo de valores, y de huecos deben de coincidir.
#IMPORTANTE: el tamaño de tags, de huecos y de la primera dimensión de valores debe de ser igual

# topicos = ['dinero', 'dinero sucio', 'recibo', 'deposito', 'beneficiario', 'cuenta', 'cuenta compartida']
# acciones = ['enviar', 'recibir', 'obtener exitosamente', 'cancelar', 'pagar']
# unes = ['un', 'una', 'uno']
# valores = [topicos, acciones, unes]
#
# huecos = ['TOPICO', 'ACCION', 'UN']
#
# title_tags = ['tpc', 'acc', 'uns']


nombres_bot = ['este bot', 'aquí', 'esta plataforma', 'esto', 'bot', 'bto', 'bot de Dinero Expres', 'bot de Dinero Express', 'bot de Dinero Expres por messenger', 'bot de Dinero Express por Messenger', 'dexbot']
usar = ['usar', 'poder usar', 'utilizar', 'poder utilizar', 'manejar', 'poder manejar']
dispositivos = ['dispositivos', 'plataformas', 'celulares', 'sistemas operativos', 'dispositivo']
montos = ['monto', 'monto máximo', 'cantidad', 'cantidad máxima', 'dinero', 'dinero máximo']
haceres = ['cancelar', 'rechazar', 'invalidar', 'validar','hacer', 'realizar', 'completar', 'enviar', 'cobrar', 'obtener']
fondear = ['fondear', 'pagar']
envios = ['envio', 'operacion', 'transaccion']
presentares = ['debe presentarse', 'debo llevar', 'necesito presentar', 'debe llevarse']
presentares_b = ['debe presentar', 'debe llevar', 'necesita llevar','necesita presentar']
corregires = ['cambiar', 'corregir', 'editar', 'modificar', 'alterar']
corrijores = ['cambio', 'corrijo', 'corrigo', 'edito', 'altero', 'modifico']
ayudas = ['ayuda', 'asistencia', 'apoyo']
preenvios = ['un', 'una', 'el', 'la', 'mi']
premontos = ['el', 'la']
prebeneficiario = ['un', 'el', 'mi', 'una']
beneficiarios = ['beneficiario', 'amigo', 'beneficiaria', 'amiga']
fondeo = ['fondeo', 'pago']
datos = ['nombre', 'apellido', 'info', 'informacion', 'direccion', 'monto']
quereres = ['quiero', 'necesito', 'requiero', 'ocupo', 'busco']

valores = [nombres_bot, usar, dispositivos, montos, haceres, fondear, envios, presentares, presentares_b, corregires, corrijores, ayudas, preenvios, premontos, prebeneficiario, beneficiarios, fondeo, datos, quereres]

huecos = ['BOT', 'USAR', 'DISP', 'MONTO', 'HACER', 'FONDEAR', 'ENVIOS', 'PRESENTAR', 'PRESENTARB', 'CORREGIR', 'CORRIJO', 'AYUDA', 'UNS', 'PREMONTO', 'UNSB', 'BENEF', 'FONDEO', 'DATO', 'QUIERO']

title_tags = ['bot', 'usa', 'dsp', 'mnt', 'hcr', 'fnd', 'env', 'pnt', 'pnb', 'crg', 'crj', 'ayd', 'uns', 'pmt', 'unb', 'bnf', 'fdo', 'dat', 'qro']

# autores = ['Manuel', 'jose jose','lupita dalessio', 'chaplin', 'roman', 'christina', 'gerardo', 'linkin park', "jose jose","green day","muse","queen","eric clapton","maluma","tame impala","vicente fernandez","joan sebastian"]
# valores = [autores]
# huecos = ['AUTOR']
#
# title_tags = ['ar']

frases = []
numeros_intencion = []

res_frases = []
res_tags = []
#En este caso las frases a inflar las sacamos de un archivo txt
#Las frases infladas se guardan en 'frases' y sus número de intencion en 'numeros_intencion'
file = open("../trainingFAQs.txt", 'r')
for linea in file.readlines():
    frase = linea
    frase = frase.replace('?', '').replace('¿', '').replace('\n', '')
    frase = elimina_tildes(frase)
    numero_intencion = frase[0]#Se extrae el número de intención
    frase_sin_numero = frase[2:]#Se quita el número de intención
    frases.append(list(aumentar_data_set(frase_sin_numero, huecos, valores)))
    numeros_intencion.append(numero_intencion*len(aumentar_data_set(frase_sin_numero, huecos, valores)))

    frasesTags, tags = aumentar_data_set_tags(frase_sin_numero, huecos, valores, title_tags)
    res_frases.append(frasesTags)
    res_tags.append(tags)
file.close()

##########----INTENCIONES----##########
#Se ingresa el numero de intencion con la frase inflada correspondiente, y se escribe a otro txt
numeros_intencion = ''.join(numeros_intencion)
file = open("./data_final_inflado_intencion.txt", 'w')
index_numeros_intencion=0
for oraciones in frases:
    for palabra in oraciones:
        oracion = " ".join(str(x) for x in palabra)
        file.write(numeros_intencion[index_numeros_intencion]+' '+oracion)
        file.write('\n')
        index_numeros_intencion+=1
file.close()

#########----TAGS----###########
#Se ponen los tags y las frases dentro de sus listas correspondientes, para bajarlas a una sola dimensión
lista_frases_unida = []
lista_tags_unida = []

for frase_base in res_frases:
    for oraciones in frase_base:
        lista_frases_unida.extend(['-', '-', '-']+oraciones+['-', '-', '-'])

for frase_base in res_tags:
    for oraciones in frase_base:
        lista_tags_unida.extend(['-', '-', '-']+oraciones+['-', '-', '-'])

labels=["tags","words"]
df=pd.DataFrame.from_records(zip(lista_tags_unida,lista_frases_unida),columns=labels)
df.to_csv("data_final_inflado_tag.csv", sep=',')