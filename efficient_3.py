import sys
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


class EfficientSolver:
    def __init__(self, delta, alpha, char_to_idx):
        self.delta = delta
        self.alpha = alpha
        self.char_to_idx = char_to_idx

    def _find_optimal_value(self, s1, s2):
        m, n = len(s1), len(s2)

        opt = [[0 for _ in range(n+1)] for _ in range(2)]

        # Initialize col 0
        for j in range(n+1):
            opt[0][j] = j * delta

        # Fill OPT matrix using recurrence relation
        i = 0
        for i in range(1, m+1):
            r = i % 2
            opt[r][0] = i * delta
            for j in range(1, n+1):
                opt[r][j] = min([
                    alpha[char_to_idx[s1[i-1]]][char_to_idx[s2[j-1]]] + opt[1-r][j-1],
                    delta + opt[1-r][j],
                    delta + opt[r][j-1]
                ])

        if i % 2 == 0:
            return opt[::-1]
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
        
    def recursive(self, s1, s2):
        m, n = len(s1), len(s2)
        if m == 0 and n == 0:
            return "", "", 0
        if m == 0:
            return '_' * n, s2, delta * n
        if n == 0:
            return s1, '_' * m, delta * m
        

        if m == 1:
            opt = self._find_optimal_value(s1, s2)
            
            a1, a2 = self._find_optimal_alignment(opt, s1, s2)
            return a1, a2, opt[-1][-1]
            
        else:
            s1_mid = len(s1) // 2
            s1_l, s1_r = s1[:s1_mid], s1[s1_mid:]
            opt_l = self._find_optimal_value(s1_l, s2)
            opt_r = self._find_optimal_value(s1_r[::-1], s2[::-1])

            opt = [(opt_l[1][i] + opt_r[1][n-i], i) for i in range(len(opt_r[1]))]
            opt, s2_mid = min(opt, key=lambda x:x[0])

            s2_l, s2_r = s2[:s2_mid], s2[s2_mid:]

            a1_l, a2_l, opt_rec_l = self.recursive(s1_l, s2_l)
            a1_r, a2_r, opt_rec_r = self.recursive(s1_r, s2_r)

            return a1_l + a1_r, a2_l + a2_r, opt_rec_l + opt_rec_r

    def solve(self, s1, s2):
        a1, a2, opt = self.recursive(s1, s2)

        return a1, a2, opt


def main(input_fn, output_fn):
    # Inputs
    s1, s2 = process_input(input_fn)

    # Solver
    solver = EfficientSolver(delta, alpha, char_to_idx)

    # Alignments
    a1, a2, opt = solver.solve(s1, s2)

    return a1, a2, opt


if __name__ == '__main__':
    input_fn = sys.argv[1]
    output_fn = sys.argv[2]

    main(input_fn, output_fn)
