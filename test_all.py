import pytest

def similarity_score(a1, a2, delta, alpha, char_to_idx):
    assert(len(a1) == len(a2))
    score = 0
    for i in range(len(a1)):
        if a1[i] == '_' or a2[i] == '_':
            score += delta
        else:
            score += alpha[char_to_idx[a1[i]]][char_to_idx[a2[i]]]
    return score

class InputOutputPair:
    def __init__(self, input_fn, output_fn):
        self.input_fn = input_fn
        self.output_fn = output_fn

        with open(output_fn, 'r') as f:
            self.similarity = int(f.readline().strip())
            self.aligned_1 = f.readline().strip()
            self.aligned_2 = f.readline().strip()
            self.string_1 = self.aligned_1.replace('_', '')
            self.string_2 = self.aligned_2.replace('_', '')

@pytest.fixture(
    params=[
        ('tests/input1.txt', 'tests/test_output1.txt'),
        ('tests/input2.txt', 'tests/test_output2.txt'),
        ('tests/input3.txt', 'tests/test_output3.txt'),
        ('tests/input4.txt', 'tests/test_output4.txt'),
        ('tests/input5.txt', 'tests/test_output5.txt'),
    ]
)
def input_output_pair(request):
    input_fn, output_fn = request.param
    return InputOutputPair(input_fn, output_fn)

def test_basic_solver(input_output_pair):
    from basic_3 import process_input, BasicSolver, delta, alpha, char_to_idx
    solver = BasicSolver(delta, alpha, char_to_idx)

    s1, s2 = process_input(input_output_pair.input_fn)

    assert(s1 == input_output_pair.string_1)
    assert(s2 == input_output_pair.string_2)

    a1, a2, opt = solver.solve(s1, s2)

    score = similarity_score(a1, a2, delta, alpha, char_to_idx)
    assert(opt == input_output_pair.similarity)
    assert(score == input_output_pair.similarity)

    assert(a1.replace('_', '') == s1)
    assert(a2.replace('_', '') == s2)

    assert(a1 == input_output_pair.aligned_1)
    assert(a2 == input_output_pair.aligned_2)

def test_efficient_solver(input_output_pair):
    from efficient_3 import process_input, EfficientSolver, delta, alpha, char_to_idx
    solver = EfficientSolver(delta, alpha, char_to_idx)

    s1, s2 = process_input(input_output_pair.input_fn)

    assert(s1 == input_output_pair.string_1)
    assert(s2 == input_output_pair.string_2)

    a1, a2, opt = solver.solve(s1, s2)

    score = similarity_score(a1, a2, delta, alpha, char_to_idx)
    assert(opt == input_output_pair.similarity)
    assert(score == input_output_pair.similarity)

    assert(a1.replace('_', '') == s1)
    assert(a2.replace('_', '') == s2)

    # assert(a1 == input_output_pair.aligned_1)
    # assert(a2 == input_output_pair.aligned_2)
