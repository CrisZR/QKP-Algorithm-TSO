import os
import logging
import typing
import numpy as np
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to obtain data from the file
def obtain_data(arr: list) -> typing.Optional[dict]:
    reference = arr.pop(0).strip()
    N = int(arr.pop(0).strip())
    coefficients = arr.pop(0).strip()

    # Read matrix Q (tamaño NxN)
    Q_matrix = []
    for _ in range(N):
        line = arr.pop(0).strip()
        row = list(map(int, line.split()))
        Q_matrix.append(row)

    # Get Constraint, Capacity, Weights...
    constraint = arr.pop(0).strip()
    capacity = arr.pop(0).strip()
    weights = arr.pop(0).strip()

    error1 = arr.pop(-2).strip()
    error2 = arr.pop(-1).strip()

    data_dict = {
        'reference': reference,
        'NVariables': N,
        'Coefficients': coefficients,
        'Constraint': constraint,
        'Capacity': capacity,
        'Weights': weights,
        "error": error1,
        "error1": error2,
        'Q_matrix': Q_matrix
    }

    return data_dict

def swap_1_1(S, wa, total_profit, profit, wi, C, Q):
    improved = True
    while improved:
        improved = False
        for i in S:  
            for j in range(len(profit)):  
                if j not in S and wa - wi[i] + wi[j] <= C:  
                    new_profit = total_profit - profit[i] + profit[j]
                    interaction_loss = sum(Q[i][k] for k in S if k != i)
                    interaction_gain = sum(Q[j][k] for k in S if k != i)
                    new_profit += interaction_gain - interaction_loss

                    if new_profit > total_profit:
                        S.remove(i)
                        S.append(j)
                        wa = wa - wi[i] + wi[j]
                        total_profit = new_profit
                        improved = True
                        break
            if improved:
                break
    return S, wa, total_profit


def local_search_10_percent(S, wa, total_profit, profit, wi, C, Q):
    improved = True
    while improved:
        improved = False
        num_swaps = max(1, int(0.1 * len(S)))
        # Seleccionar aleatoriamente el %10 de los elementos de la solución actual.
        candidates = random.sample(S, num_swaps) if len(S) >= num_swaps else S.copy()
        for i in candidates:
            for j in range(len(profit)):
                if j not in S:
                    new_weight = wa - wi[i] + wi[j]
                    if new_weight <= C:
                        lost_interactions = sum(Q[i][k] for k in S if k != i)
                        gain_interactions = sum(Q[j][k] for k in S if k != i)
                        new_profit = total_profit - profit[i] + profit[j] - lost_interactions + gain_interactions
                        if new_profit > total_profit:
                            S.remove(i)
                            S.append(j)
                            wa = new_weight
                            total_profit = new_profit
                            improved = True
                            break
            if improved:
                break
    return S, wa, total_profit

# Function to call the instance and process the data
def call_instance(txt: str) -> None:
    try:
        logger.info(f"Loading instance {txt}")
        with open(f'QKPGroupI/{txt}', 'r') as file:
            arr = file.readlines()
        data_array = obtain_data(arr)

        # Initialize knapsack and profit
        S = []
        wa = 0
        total_profit = 0

        # Step 1: Individual profitability pi/wi
        profit = list(map(int, data_array['Coefficients'].split()))
        wi = list(map(int, data_array['Weights'].split()))
        C = int(data_array['Capacity'])

        R = {i: profit[i] / wi[i] for i in range(len(profit)) if wi[i] > 0}
        sorted_items = sorted(R.items(), key=lambda x: x[1], reverse=True)

        Q_matrix = data_array['Q_matrix']

        Q = np.zeros((len(profit), len(profit)), dtype=int)
        for i in range(len(Q_matrix)):
            for j in range(len(Q_matrix[i])):
                Q[i][j] = Q_matrix[i][j]
                Q[j][i] = Q_matrix[i][j]  # Make it symmetric

        start_time = time.time()

        # Select the first item
        for idx, _ in sorted_items:
            if wi[idx] + wa <= C:
                S.append(idx)
                wa += wi[idx]
                total_profit += profit[idx]
                break

        # Step 2: iterative selection based on interactions
        while True:
            available = [i for i in range(len(profit)) if i not in S and wi[i] + wa <= C]
            if not available:
                break

            scores = {}
            for i in available:
                interaction_sum = sum(Q[i][j] for j in S)
                if wi[i] > 0:
                    scores[i] = interaction_sum / wi[i]

            if not scores:
                break

            selected = max(scores.items(), key=lambda x: x[1])[0]
            S.append(selected)
            wa += wi[selected]
            total_profit += profit[selected] + sum(Q[selected][j] for j in S if j != selected)

        end_time = time.time()
        elapsed_time = end_time - start_time
        S, wa, total_profit = swap_1_1(S, wa, total_profit, profit, wi, C, Q)
        S, wa, total_profit = local_search_10_percent(S, wa, total_profit, profit, wi, C, Q)


        print("\n--- RESULTS ---")
        print("Selected items (indexes):", [i + 1 for i in S])
        print("Total profit obtained:", total_profit)
        print("Total weight in knapsack:", wa)
        print(f"Computation time: {elapsed_time:.6f} seconds")

        # Feasibility checker
        print("\n--- FEASIBILITY CHECKER ---")
        if len(S) == len(set(S)):
            print("Are there repeated items?: No")
        else:
            print("Are there repeated items?: Yes")

        if wa > C:
            print("Is knapsack capacity exceeded?: Yes")
        else:
            print("Is knapsack capacity exceeded?: No")

    except Exception as e:
        logger.error(f'Error while loading instance: {str(e)}')
        print(f'Execution error: {str(e)}')

cwd = os.listdir('QKPGroupI')
for index, file in enumerate(cwd, start=1):
    print(f'{index} - {file}')

try:
    tx = int(input('Choose the instance index: '))
    if 1 <= tx <= len(cwd):
        txt = cwd[tx - 1]
        call_instance(txt)
    else:
        raise ValueError('Index out of range')
except ValueError as e:
    print(f'Error: {e}')
