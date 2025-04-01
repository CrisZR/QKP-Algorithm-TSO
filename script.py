import os
import random 
import logging
import typing 
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def Call_Instance(tx: str) -> tuple[bool, str]:
    try: 
        logger.info("Obteniendo instancia de manera aleatoria")
        
        with open(f'QKPGroupI/{tx}') as file:
            txt = file.read()
        if txt:
            logging.info("Instancia exitosa")
            data_array = np.array(txt)
            return True, data_array
    
    except Exception as e:
        logger.error(f'Error al obtener la instancia: {str(e)}')
        return False, f'Error en la ejectución: {str(e)}'
     
cwd = os.listdir('QKPGroupI')
print("Instancias disponibles:")
for i, file_name in enumerate(cwd, start=1):
    print(f"{i}. {file_name}")

try:
    choice = int(input("Seleccione el número de la instancia que desea cargar: "))
    if 1 <= choice <= len(cwd):
        tx = cwd[choice - 1]
        print(Call_Instance(tx))
    else:
        print("Selección inválida. Por favor, elija un número válido.")
except ValueError:
    print("Entrada inválida. Por favor, ingrese un número.")