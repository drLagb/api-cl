import os
#esta es la url del directorio del archivo
BASEPATH = os.path.dirname(os.path.abspath(__file__))

#bibliotecas 
Velocidad_corte_segundoxmetro = {
    "CR18": 10 , #tiempo: 6 segundos por metro (EJEMPLO 5000mm (5 metros) tendría una demora de 30 segundos)
    "CR16": 12,
    "CR14": 14,
    "HR14": 14,
    "HR12": 17,
    "HR1/8": 20,
    "HR3/16": 25,
    "HR1/4": 30,
    "HR5/16": 35,
    "HR3/8": 40,
    "HR1/2": 45,
    "INOX20": 10,
    "INOX18": 12,
    "INOX16": 14,
    "INOX14": 16,
    "INOX12": 18,
    "INOX1/8": 22,
    "INOX3/16": 29,
    "ALUM1": 10,
    "ALUM1,5": 12,
    "ALUM2,5": 14,
    "ALUM3": 16,
    "ALUM4": 18,
    "ALUM5": 21,
    "ALUM6": 24,
}


Valor_lamina_m2 = {  #este diccionario debe de cambiar con administración por fronetnd de un administrador con derechos
    "CR18":  120000,  #Costo lamina: área_de_la_figura * clave_del_diccionario (EJEMPLO: 0.032 m2 serían 3200 COP adicionales)
    "CR16": 180000,
    "CR14": 230000,
    "HR14": 210000,
    "HR12": 230000,
    "HR1/8": 260000,
    "HR3/16": 300000,
    "HR1/4": 345000,
    "HR5/16": 460000,
    "HR3/8": 520000,
    "HR1/2": 730000,
    "INOX20": 300000,
    "INOX18": 390000,
    "INOX16": 470000,
    "INOX14": 540000,
    "INOX12": 620000,
    "INOX1/8": 700000,
    "INOX3/16": 850000,
    "ALUM1": 150000,
    "ALUM1,5": 220000,
    "ALUM2,5": 300000,
    "ALUM3": 400000,
    "ALUM4": 480000,
    "ALUM5": 550000,
    "ALUM6": 650000,
}

#porcentaje_descuento




    # Crear un diccionario vacío
biblioteca = {}
# Leer los valores desde un archivo o desde la entrada estándar
# Aquí asumo que los valores están en un archivo llamado "valores.txt"
with open(os.path.join(BASEPATH, "descuentos.txt")) as archivo:
    # Iterar sobre cada línea del archivo
    for linea in archivo:
        # Separar la línea por el espacio y convertir los valores a enteros
        clave, valor = map(int, linea.split())
        # Asignar el valor a la clave en el diccionario
        biblioteca[clave] = valor

   
# Crear listas para cada material con sus calibres disponibles
calibres_CR = [calibre[2:] for calibre in Velocidad_corte_segundoxmetro.keys() if calibre.startswith("CR")]
calibres_HR = [calibre[2:] for calibre in Velocidad_corte_segundoxmetro.keys() if calibre.startswith("HR")]
calibres_INOX = [calibre[4:] for calibre in Velocidad_corte_segundoxmetro.keys() if calibre.startswith("INOX")]
calibres_ALUM = [calibre[4:] for calibre in Velocidad_corte_segundoxmetro.keys() if calibre.startswith("ALUM")]

# Imprimir las listas resultantes
# print("Calibres disponibles para CR:", calibres_CR)
# print("Calibres disponibles para HR:", calibres_HR)
# print("Calibres disponibles para INOX:", calibres_INOX)
# print("Calibres disponibles para ALUM:", calibres_ALUM)

