import random

def gsat(clauses, num_vars, max_flips, p):
    current_solution = [random.choice([True, False]) for _ in range(num_vars)]
    best_solution = current_solution
    best_cost = cost(current_solution, clauses)

    for i in range(max_flips):
        next_solution = generate_neighbor(current_solution)
        next_cost = cost(next_solution, clauses)

        if next_cost > best_cost:
            best_solution = next_solution
            best_cost = next_cost
        elif random.uniform(0, 1) < p:
            current_solution = next_solution

    return best_solution

def cost(solution, clauses):
    cost = 0
    for clause in clauses:
        clause_satisfied = False
        for literal in clause:
            var = abs(literal) - 1
            if literal > 0 and solution[var]:
                clause_satisfied = True
                break
            elif literal < 0 and not solution[var]:
                clause_satisfied = True
                break
        if not clause_satisfied:
            cost += 1
    return cost

def generate_neighbor(solution):
    var = random.choice(range(len(solution)))
    neighbor = solution[:]
    neighbor[var] = not neighbor[var]
    return neighbor