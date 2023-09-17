import random
import copy
import math

def initial_state(n):
    return [[' ' for _ in range(n)] for _ in range(n)]

def objective_function(state, nonogramX, nonogramY):
    score = 0
    affected_rows = set()
    affected_columns = set()

    for i, row in enumerate(state):
        black_zones = ''.join(row).split(' ')
        black_sizes = [len(zone) for zone in black_zones if zone]
        if black_sizes == nonogramX[i]:
            score += 1
        affected_rows.add(i)

    for j in range(len(state)):
        column = [state[i][j] for i in range(len(state))]
        black_zones = ''.join(column).split(' ')
        black_sizes = [len(zone) for zone in black_zones if zone]
        if j < len(nonogramY) and black_sizes == nonogramY[j]:
            score += 1
        affected_columns.add(j)

    return score, affected_rows, affected_columns

def random_move(state, affected_rows, affected_columns):
    new_state = copy.deepcopy(state)
    while True:
        i, j = random.randint(0, len(state) - 1), random.randint(0, len(state) - 1)
        if i in affected_rows or j in affected_columns:
            new_state[i][j] = '#' if state[i][j] == ' ' else ' '
            return new_state
# initial_temperature:its for the probability of accepting a worse solution at the beginning of the search
# cooling_rate:its for the probability of accepting a worse solution at the end of the search 
def simulated_annealing(nonogramX, nonogramY, max_iterations=3000000, initial_temperature=5.0, cooling_rate=0.999):
    n = len(nonogramX)
    current_state = initial_state(n)
    current_score, affected_rows, affected_columns = objective_function(current_state, nonogramX, nonogramY)
    best_state = copy.deepcopy(current_state)
    best_score = current_score
    temperature = initial_temperature
    tabu_list = []

    for _ in range(max_iterations):
        new_state = random_move(current_state, affected_rows, affected_columns)
        new_score, new_affected_rows, new_affected_columns = objective_function(new_state, nonogramX, nonogramY)

        if new_state not in tabu_list and (new_score > current_score or random.random() < math.exp((new_score - current_score) / temperature)):
            current_state = new_state
            current_score = new_score
            affected_rows = new_affected_rows
            affected_columns = new_affected_columns
            tabu_list.append(new_state)
            if len(tabu_list) > 100: 
                tabu_list.pop(0)

            if current_score > best_score:
                best_state = copy.deepcopy(current_state)
                best_score = current_score

        temperature *= cooling_rate

    return best_state

def print_nonogram(nonogram):
    for row in nonogram:
        print(' '.join(row))

if __name__ == "__main__":
    nonogramY = [[1],[2],[3],[4],[5]]
    nonogramX = [[1],[2],[3],[4],[5]]
    nonogram = simulated_annealing(nonogramY, nonogramX)
    print("Nonogram generated:")
    print_nonogram(nonogram)
 