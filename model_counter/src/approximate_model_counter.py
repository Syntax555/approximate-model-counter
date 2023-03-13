import math
import random
from cnf_parser import read_cnf_file
from walk_sat import walk_sat
from gsat import gsat
from simulated_annealing import simulated_annealing


def approximate_model_counter(filename, algorithm, num_samples):
    num_vars, num_clauses, clauses = read_cnf_file(filename)
    count = count_satisfying_terms(num_vars, clauses, algorithm, num_samples)
    print('Approximate number of satisfying terms: {}'.format(count))


def count_satisfying_terms(num_vars, clauses, algorithm, num_samples):
    count = 0
    num_solutions = 0
    
    # Iterate until we have collected the desired number of samples
    while num_solutions < num_samples:
        if algorithm == 'walk_sat':
            solution = walk_sat(clauses, num_vars, max_flips=1000, p=0.5)
        elif algorithm == 'gsat':
            solution = gsat(clauses, num_vars, max_flips=1000, p=0.5)
        elif algorithm == 'simulated_annealing':
            solution = simulated_annealing(clauses, num_vars, max_iterations=1000, temperature=0.5, cooling_rate=0.99)
        else:
            raise ValueError('Invalid algorithm: {}'.format(algorithm))
        
        # If the solution is a satisfying assignment, increment the count
        if is_satisfying(solution, clauses):
            count += 1
        num_solutions += 1

        estimated_count = count / num_solutions * num_samples
        margin_of_error = 1.96 * math.sqrt(estimated_count * (1 - estimated_count / num_samples)) / math.sqrt(num_samples)
        lower_bound = estimated_count - margin_of_error
        upper_bound = estimated_count + margin_of_error
        if lower_bound <= num_samples <= upper_bound:
            break
    
    return count

def is_satisfying(solution, clauses):
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