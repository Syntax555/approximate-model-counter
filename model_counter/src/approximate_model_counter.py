import numpy as np

from cnf_parser import read_cnf_file
from walk_sat import walk_sat
from gsat import gsat
from simulated_annealing import simulated_annealing


def approximate_model_counter(filename, algorithm, num_samples):
    num_vars, num_clauses, clauses = read_cnf_file(filename)
    count = count_satisfying_terms(num_vars, clauses, algorithm, num_samples)
    print('Approximate number of satisfying terms: {}'.format(count))


def count_satisfying_terms(num_vars, clauses, algorithm, num_samples, num_bootstraps=1000):
    unique_solutions = set()
    num_solutions = 0

    while num_solutions < num_samples:
        if algorithm == 'walk_sat':
            solution = walk_sat(clauses, num_vars, max_flips=1000, p=0.5)
        elif algorithm == 'gsat':
            solution = gsat(clauses, num_vars, max_flips=1000, p=0.5)
        elif algorithm == 'simulated_annealing':
            solution = simulated_annealing(clauses, num_vars, max_iterations=1000, temperature=0.5, cooling_rate=0.99)
        else:
            raise ValueError('Invalid algorithm: {}'.format(algorithm))

        if is_unique(solution, clauses):
            unique_solutions.add(tuple(solution))
        num_solutions += 1

    # Bootstrap resampling to estimate the count
    bootstrap_counts = []
    for _ in range(num_bootstraps):
        resampled_solutions = np.random.choice(list(unique_solutions), size=num_samples, replace=True)
        unique_resampled_solutions = set(resampled_solutions)
        count = len(unique_resampled_solutions)
        bootstrap_counts.append(count)

    estimated_count = np.mean(bootstrap_counts)
    return estimated_count

def is_unique(solution, clauses):
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
            return False
    return True