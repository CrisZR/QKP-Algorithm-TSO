import os
import random 
import logging
import typing 
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def obtain_data(arr: str) -> typing.Optional[dict]:
    
    data_dicc = {
        'refrence': arr.pop(0).strip(),
        'NVariables': (arr.pop(0).strip()),
        'Coeficientes': arr.pop(0).strip(),
        'Contraint': arr.pop(-8).strip(),
        'Capacity': arr.pop(-7).strip(),
        'Weights': arr.pop(-6).strip(),
        "error":arr.pop(-2).strip(),
        "error1":arr.pop(-3).strip()
    }
    max_length = max(len(line.split()) for line in arr if line.strip())
    matrix = [list(map(int, line.split())) + [0] * (max_length - len(line.split())) for line in arr if line.strip()]
    np_matrix = np.array(matrix)
    print(np_matrix)


    
    return f'\n{data_dicc}' 

def Call_Instance(txt: str) -> tuple[bool, str]:

    try: 
        logger.info(f"Obteniendo instancia {txt}")
        with open(f'QKPGroupI/{txt}', 'r') as file:
            arr = file.readlines()
        data_array = obtain_data(arr)            
        
        return True, data_array

    except Exception as e:
        logger.error(f'Error al obtener la instancia: {str(e)}')
        return False, f'Error en la ejectución: {str(e)}'
    
cwd = os.listdir('QKPGroupI')


for index,file in enumerate(cwd, start=1):
    print(f'{index} - {file}')

try:
    tx = int(input('Escoge el indice de la instancia: '))
    if 1 <= tx <= len(cwd):  # Verifica si el índice está dentro del rango
        txt = cwd[tx - 1]

        print(Call_Instance(txt))  
    else:
        raise ValueError('Indice fuera del rango de instancias')
except ValueError as e:
    print(f'Error: {e}')

#Crear un dicc donde guardar datos importantes