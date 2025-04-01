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
            logging.info("Intancia exitosa")
            data_array = np.array(txt)
            return True, data_array
    
    except Exception as e:
        logger.error(f'Error al obtener la instancia: {str(e)}')
        return False, f'Error en la ejectución: {str(e)}'
     
cwd = os.listdir('QKPGroupI')
tx =  random.choice(cwd)
print(Call_Instance(tx))