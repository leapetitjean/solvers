# Imports
from random import randint
from random import shuffle
from ast import literal_eval
from config import UP


def generate_instance(instance_size, nb_iter=1):
    # Initialize lists
    release_dates = []
    deadlines = []
    processing_times = []
    due_dates = []
    weights = []

    # Lower and upper bound
    lb = 0
    ub = UP

    # Generate instance_size jobs
    for i in range(instance_size):
        processing_time = randint(1, ub)
        deadline = randint(lb + processing_time, lb + ub)
        time = deadline - processing_time
        release_date = randint(0, time)
        due_date = randint(0, deadline)
        weight = randint(1, 100)
        lb = deadline
        # Add in lists
        deadlines.append(deadline)
        processing_times.append(processing_time)
        due_dates.append(due_date)
        release_dates.append(release_date)
        weights.append(weight)

    jobs_to_shuffle = list(zip(release_dates, deadlines, processing_times, due_dates, weights))
    shuffle(jobs_to_shuffle)
    release_dates, deadlines, processing_times, due_dates, weights = zip(*jobs_to_shuffle)

    # Write in .dat file
    file_name = f"data/example_{instance_size}_{nb_iter}.dat"
    with open(file_name, 'w') as f:
        print(f"n = {instance_size};\n"
              f"r = {list(release_dates)};\n"
              f"deadline = {list(deadlines)};\n"
              f"p = {list(processing_times)};\n"
              f"d = {list(due_dates)};\n"
              f"w = {list(weights)};", file=f)

    return file_name


def import_data(file_name):
    with open(file_name, 'r') as f:
        n = f.readline().split("= ")[1].split(';')[0]
        r = f.readline().split("= ")[1].split(';')[0]
        deadline = f.readline().split("= ")[1].split(';')[0]
        p = f.readline().split("= ")[1].split(';')[0]
        d = f.readline().split("= ")[1].split(';')[0]
        w = f.readline().split("= ")[1].split(';')[0]
    n = int(n)
    deadline = literal_eval(deadline)
    return {'n': n,
            'r': literal_eval(r),
            "deadline": deadline,
            'p': literal_eval(p),
            'd': literal_eval(d),
            'w': literal_eval(w)}
