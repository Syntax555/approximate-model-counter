import random
import math

def simulated_annealing(clauses, num_vars, max_iterations, temperature, cooling_rate):
    current_solution = [random.choice([True, False]) for _ in range(num_vars)]
    current_cost = cost(current_solution, clauses)
    best_solution = current_solution
    best_cost = current_cost

    for i in range(max_iterations):
        next_solution = generate_neighbor(current_solution)
        next_cost = cost(next_solution, clauses)

        delta_cost = next_cost - current_cost
        acceptance_probability = math.exp(-delta_cost / temperature)
        if acceptance_probability > random.uniform(0, 1):
            current_solution = next_solution
            current_cost = next_cost

        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost

        temperature *= cooling_rate

    return best_solution
        
def cost(solution, clauses):
    cost = 0
    for clause in clauses:
        for literal in clause:
            if literal > 0:
                if solution[literal - 1]:
                    cost -= 1
                    break
            else:
                if not solution[-literal - 1]:
                    cost -= 1
                    break
    return cost

def generate_neighbor(solution):
    index = random.randint(0, len(solution) - 1)
    neighbor_solution = solution[:]
    neighbor_solution[index] = not neighbor_solution[index]
    return neighbor_solution