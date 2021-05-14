from contourpy import FillType, LineType, max_threads


def corner_masks():
    return ['no mask', False, True]
    
def fill_types():
    return list(FillType.__members__.values())

def line_types():
    return list(LineType.__members__.values())

def problem_sizes():
    return [10, 30, 100, 300, 1000]

def thread_counts():
    thread_counts = [1, 2, 4, 6, 8]
    return list(filter(lambda n: n <= max(max_threads(), 1), thread_counts))
