import os
import logging
import typing
import numpy as np
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def obtain_data(arr: str) -> typing.Optional[dict]:
    data_dict = {
        'reference': arr.pop(0).strip(),
        'NVariables': arr.pop(0).strip(),
        'Coefficients': arr.pop(0).strip(),
        'Constraint': arr.pop(-8).strip(),
        'Capacity': arr.pop(-7).strip(),
        'Weights': arr.pop(-6).strip(),
        "error": arr.pop(-2).strip(),
        "error1": arr.pop(-3).strip()
    }
    max_length = max(len(line.split()) for line in arr if line.strip())
    matrix = [list(map(int, line.split())) + [0] * (max_length - len(line.split())) for line in arr if line.strip()]
    np_matrix = np.array(matrix)

    return data_dict

def call_instance(txt: str) -> None:
    try:
        logger.info(f"Loading instance {txt}")
        with open(f'QKPGroupI/{txt}', 'r') as file:
            arr = file.readlines()
        data_array = obtain_data(arr)

        # Initialize knapsack
        S = []
        wa = 0
        total_profit = 0

        # Step 1: Individual profitability pi/wi
        profit = list(map(int, data_array['Coefficients'].split()))
        wi = list(map(int, data_array['Weights'].split()))
        C = int(data_array['Capacity'])

        R = {i: profit[i] / wi[i] for i in range(len(profit)) if wi[i] > 0}
        sorted_items = sorted(R.items(), key=lambda x: x[1], reverse=True)


        # Read matrix Q
        Q_matrix = []
        with open(f'QKPGroupI/{txt}', 'r') as file:
            lines = file.readlines()
            matrix_lines = lines[3:-8]
            for line in matrix_lines:
                Q_matrix.append(list(map(int, line.strip().split())))

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

        print("\n--- RESULTS ---")
        print("Selected items (indexes):", [i + 1 for i in S])
        print("Total profit obtained:", total_profit)
        print("Total weight in knapsack:", wa)
        print(f"Computation time: {elapsed_time:.6f} seconds")

        # Feasibility checker
        print("\n--- FEASIBILITY CHECKER ---")
        # Check for repeated items
        if len(S) == len(set(S)):
            print("Are there repeated items?: No")
        else:
            print("Are there repeated items?: Yes")

        # Check if knapsack capacity is exceeded
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

