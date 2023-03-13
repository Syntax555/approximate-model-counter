def read_cnf_file(filename):
    with open(filename, 'r') as f:
        num_vars = None
        num_clauses = None
        clauses = []
        for line in f:
            line = line.strip()
            if line.startswith('c'):
                continue
            elif line.startswith('p'):
                _, _, num_vars, num_clauses = line.split()
                num_vars = int(num_vars)
                num_clauses = int(num_clauses)
            else:
                clause = [int(literal) for literal in line.split()[:-1]]
                clauses.append(clause)
        return num_vars, num_clauses, clauses