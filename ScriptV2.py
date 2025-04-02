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

        """# Matriz de interacciones (q_ij) - Construcción completa -  matriz simetrica
        q_ij = [[0] * n for _ in range(n)]  # Matriz vacía
        row_idx = 3  # Primera línea de la matriz en el archivo

        for i in range(n):
            values = list(map(int, lines[row_idx].strip().split()))
    
            # Rellenar solo la parte correcta de la matriz
            for j in range(len(values)):
                q_ij[i][j] = values[j]  # Asignamos directamente desde el archivo
    
            row_idx += 1  # Avanzamos a la siguiente fila"""
        
        # Matriz de interacciones (q_ij) - Construcción como triangular inferior
        q_ij = []  # Inicializa la matriz como una lista vacía
        row_idx = 3  # Primera línea de la matriz en el archivo, empieza en la linea 4

        for i in range(n):
            values = list(map(int, lines[row_idx].strip().split()))
            q_ij.append(values)  # Agrega la fila con su tamaño exacto
            row_idx += 1  # Avanza a la siguiente línea


        # Tipo de restricción
        constraint_type_line = row_idx  # Siguiente línea
        if constraint_type_line < len(lines):
            constraint_type = int(lines[constraint_type_line].strip())
        else:
            raise ValueError("No se encontró la línea que indica el tipo de restricción.")

        # Capacidad de la mochila (K)
        knapsack_line = constraint_type_line + 1
        if knapsack_line < len(lines):
            knapsack_capacity = int(lines[knapsack_line].strip())
        else:
            raise ValueError("No se encontró la línea que indica el valor de la mochila.")

        # Pesos de los objetos
        weights_line = knapsack_line + 1
        if weights_line < len(lines):
            weights = list(map(int, lines[weights_line].strip().split()))
            if len(weights) != n:
                raise ValueError(f"El número de pesos ({len(weights)}) no coincide con n ({n}).")
        else:
            raise ValueError("No se encontró la línea de los coeficientes de capacidad.")


        data = {
            "reference": instance_reference,
            "n": n,
            "c_i": c_i,
            "q_ij": q_ij,
            "constraint_type": constraint_type,
            "K": knapsack_capacity,
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
            print("Matriz de interacciones (q_ij):")
            for row in instance_data["q_ij"][:100]:  # Mostrar solo las primeras 12 filas
                print(row[:100])  # Mostrar solo las primeras 12 columnas
            #print("Matriz de interacciones (q_ij):")
            #for row in instance_data["q_ij"]:
                #print(" ".join(map(str, row)))  # Imprime solo los valores sin ceros extra
            print(f"Tipo de restricción: {instance_data['constraint_type']}")
            print(f"Capacidad de la mochila (K): {instance_data['K']}")
            print(f"Coeficientes de capacidad (K_i): {instance_data['weights']}")
            
        else:
            print(f"Error: {instance_data['error']}")
    else:
        print("Selección inválida. Por favor, elija un número válido.")
except ValueError:
    print("Entrada inválida. Por favor, ingrese un número.")
