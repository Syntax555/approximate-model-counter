import random

def walk_sat(clauses, num_vars, max_flips, p):
    current_solution = [random.choice([True, False]) for _ in range(num_vars)]
    best_solution = current_solution
    best_cost = calculate_cost(current_solution, clauses)

    for i in range(max_flips):
        current_cost = calculate_cost(current_solution, clauses)
        if current_cost == 0:
            return current_solution

        if random.uniform(0, 1) < p:
            next_solution = generate_random_neighbor(current_solution)
        else:
            next_solution = generate_best_neighbor(current_solution, clauses)

        next_cost = calculate_cost(next_solution, clauses)
        if next_cost < best_cost:
            best_solution = next_solution
            best_cost = next_cost
        elif next_cost < current_cost:
            current_solution = next_solution

    return best_solution


def calculate_cost(solution, clauses):
    cost = 0
    for clause in clauses:
        clause_satisfied = False
        for literal in clause:
            if literal > 0 and solution[literal-1]:
                clause_satisfied = True
                break
            elif literal < 0 and not solution[abs(literal)-1]:
                clause_satisfied = True
                break
        if not clause_satisfied:
            cost += 1
    return cost

def generate_random_neighbor(solution):
    index = random.randint(0, len(solution) - 1)
    neighbor = solution.copy()
    neighbor[index] = not neighbor[index]
    return neighbor

def generate_best_neighbor(solution, clauses):
    best_neighbor = None
    best_cost = float('inf')
    for i in range(len(solution)):
        neighbor = solution.copy()
        neighbor[i] = not neighbor[i]
        cost = calculate_cost(neighbor, clauses)
        if cost < best_cost:
            best_neighbor = neighbor
            best_cost = cost
    return best_neighbor
