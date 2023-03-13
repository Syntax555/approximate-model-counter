import argparse
from approximate_model_counter import approximate_model_counter

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='input file in DIMACS CNF format')
    parser.add_argument('--algorithm', default='walk_sat', help='algorithm to use (walk_sat, gsat, or simulated_annealing)')
    parser.add_argument('--num_samples', default=100000, type=int, help='number of samples for counting the number of satisfying terms')
    args = parser.parse_args()
    approximate_model_counter(args.filename, args.algorithm, args.num_samples)

    