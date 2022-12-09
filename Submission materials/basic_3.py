import sys
import time
import psutil


# Constants
delta = 30
alpha = [
    [  0, 110,  48,  94],
    [110,   0, 118,  48],
    [ 48, 118,   0, 110],
    [ 94,  48, 110,   0],
]
char_to_idx = { 'A': 0, 'C': 1, 'G': 2, 'T': 3 }

def get_space():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)

    return memory_consumed

def process_input(filename):
    with open(filename, 'r') as file:
        strings = ["", ""]
        orig_strings = ["", ""]
        steps = [0, 0]
        cur_str_idx = -1
        for line in file:
            line = line.strip()
            if line.isnumeric():
                s = strings[cur_str_idx]
                strings[cur_str_idx] = s[:int(line)+1] + s + s[int(line)+1:]
                steps[cur_str_idx] += 1
            else:
                cur_str_idx += 1
                strings[cur_str_idx] = line
                orig_strings[cur_str_idx] = line
        assert(len(strings[0]) == 2**steps[0] * len(orig_strings[0]))
        assert(len(strings[1]) == 2**steps[1] * len(orig_strings[1]))
    return strings



class BasicSolver:
    def __init__(self, delta, alpha, char_to_idx):
        self.delta = delta
        self.alpha = alpha
        self.char_to_idx = char_to_idx

    def _find_optimal_value(self, s1, s2):
        m, n = len(s1), len(s2)

        opt = [[0 for _ in range(n+1)] for _ in range(m+1)]

        # Initialize row 0
        for i in range(m+1):
            opt[i][0] = i * delta

        # Initialize col 0
        for j in range(n+1):
            opt[0][j] = j * delta

        # Fill OPT matrix using recurrence relation
        for i in range(1, m+1):
            for j in range(1, n+1):
                opt[i][j] = min([
                    alpha[char_to_idx[s1[i-1]]][char_to_idx[s2[j-1]]] + opt[i-1][j-1],
                    delta + opt[i-1][j],
                    delta + opt[i][j-1]
                ])
        
        return opt

    def _find_optimal_alignment(self, opt, s1, s2):
        m, n = len(s1), len(s2)
        a1, a2 = "", ""
        i, j = m, n

        while i > 0 and j > 0:
            min_opt_val, min_opt_choice = min([
                    (alpha[char_to_idx[s1[i-1]]][char_to_idx[s2[j-1]]] + opt[i-1][j-1], 0),
                    (delta + opt[i][j-1], 2),
                    (delta + opt[i-1][j], 1),
                ], key=lambda x: x[0])
            if min_opt_choice == 0:
                i -= 1
                j -= 1
                a1 += s1[i]
                a2 += s2[j]
            elif min_opt_choice == 1:
                i -= 1
                a1 += s1[i]
                a2 += '_'
            else:
                j -= 1
                a1 += '_'
                a2 += s2[j]
        
        while i > 0:
            i -= 1
            a1 += s1[i]
            a2 += '_'

        while j > 0:
            j -= 1
            a1 += '_'
            a2 += s2[j]

        return a1[::-1], a2[::-1]

    def solve(self, s1, s2):

        opt = self._find_optimal_value(s1, s2)
        a1, a2 = self._find_optimal_alignment(opt, s1, s2)

        return a1, a2, opt[len(s1)][len(s2)]

def main(input_fn, output_fn):

    # Inputs
    s1, s2 = process_input(input_fn)

    # Solver
    solver = BasicSolver(delta, alpha, char_to_idx)

    # Alignments
    startTime = time.time()
    #startSpace = get_space()
    basicA1, basicA2, basicOpt = solver.solve(s1, s2)
    endTime = (time.time() - startTime) * 1000
    #endSpace = get_space() - startSpace
    endSpace = get_space()

    f = open(output_fn, 'w')

    print(basicOpt, file=f)
    print(basicA1, file=f)
    print(basicA2, file=f)
    print(endTime, file = f)
    print(endSpace, file=f)

    f.close()

    return


if __name__ == '__main__':
    input_fn = sys.argv[1]
    output_fn = sys.argv[2]

    main(input_fn, output_fn)
