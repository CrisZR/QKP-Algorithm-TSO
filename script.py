import os
import random 
import logging
import typing 
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def Call_Instance(tx: str) -> tuple[bool, dict]:
    try:
        logger.info("Obteniendo instancia...")

        with open(f'QKPGroupI/{tx}', 'r') as file:
            lines = file.readlines()

        # Interpreta la primera línea como referencia de la instancia
        instance_reference = lines[0].strip()

        # Interpreta la segunda línea como el número de variables (n)
        n = int(lines[1].strip())

        # Interpretar la tercera línea como los coeficientes lineales (c_i)
        c_i = list(map(int, lines[2].strip().split()))

        # Verifica que el número de coeficientes lineales coincida con n (Numero de variables)
        if len(c_i) != n:
            raise ValueError(f"El número de coeficientes lineales ({len(c_i)}) no coincide con n ({n}).")
        
        #Interpreta las lineas que abarcan la matriz con los coeficientes cuadráticos (q_ij)


        # Interpreta la linea de la constante si es del tipo <=
        constraint_type_line = 2 + n + 1
        if constraint_type_line < len(lines):
            constraint_type = int(lines[constraint_type_line].strip())
        else:
            raise ValueError("No se encontró la línea que indica el tipo de restricción.")

        # Interpreta la linea (2 + n + 2) como la capacidad de la mochila (K)
        knapsack_type_line = 2 + n + 2
        if knapsack_type_line < len(lines):
            knapsack_type_line = int(lines[knapsack_type_line].strip())
        else:
            raise ValueError("No se encontró la línea que indica el valor de la mochila.")
        
        #Interpreta la linea de los coeficientes de capacidad de cada variable (K_i)
        weights_line = 2 + n + 3
        if weights_line < len(lines):
            weights = list(map(int, lines[weights_line].strip().split()))
            if len(weights) != n:
                raise ValueError(f"El número de pesos ({len(weights)}) no coincide con n ({n}).")
        else:
            raise ValueError("No se encontró la línea que indica los coeficientes de las restricciones de capacidad.")

        data = {
            "reference": instance_reference,
            "n": n,
            "c_i": c_i,	
            "constraint_type": constraint_type,
            "K": knapsack_type_line,
            "weights": weights,
            
        }

        logger.info(f"Instancia '{instance_reference}' cargada exitosamente con {n} variables.")
        return True, data

    except Exception as e:
        logger.error(f"Error al obtener la instancia: {str(e)}")
        return False, {"error": f"Error en la ejecución: {str(e)}"}



# Muestra las instancias dentro de la carpeta QKPGroupI
cwd = os.listdir('QKPGroupI')
print("Instancias disponibles:")
for i, file_name in enumerate(cwd, start=1):
    print(f"{i}. {file_name}")

# Solicita una instancia de la carpeta
try:
    choice = int(input("Seleccione el número de la instancia que desea cargar: "))
    if 1 <= choice <= len(cwd):
        tx = cwd[choice - 1]
        success, instance_data = Call_Instance(tx)
        if success:
            print("Datos de la instancia:")
            print(f"Referencia: {instance_data['reference']}") #Nombre de la instancia
            print(f"Número de variables (n): {instance_data['n']}") #Número de variables
            print(f"Coeficientes lineales (c_i): {instance_data['c_i']}") #Coeficientes lineales
            print(f"Tipo de restricción: {instance_data['constraint_type']}")
            print(f"Capacidad de la mochila (K): {instance_data['K']}")
            print(f"Coeficientes de capacidad (K_i): {instance_data['weights']}")
            
        else:
            print(f"Error: {instance_data['error']}")
    else:
        print("Selección inválida. Por favor, elija un número válido.")
except ValueError:
    print("Entrada inválida. Por favor, ingrese un número.")