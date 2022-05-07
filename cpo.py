# Imports
from docplex.cp.model import *
from config import TIMELIMIT


def build_cpo_model(data):
    model = CpoModel()
    intervals = []
    for j in range(data['n']):
        intervals.append(interval_var(size=data['p'][j], name="job_" + str(j)))
        intervals[j].set_start_min(data['r'][j])
        intervals[j].set_end_max(data['deadline'][j])
    model.add(no_overlap(intervals))
    model.add(minimize(sum(max(end_of(intervals[j]) - data['d'][j], 0) * data['w'][j] for j in range(data['n']))))

    return model


def solve_cpo(model, model_name, n):
    solution = model.solve(TimeLimit=TIMELIMIT, LogVerbosity="Quiet")
    # Performance
    with open(f"output/log_{model_name}", 'a') as f:
        print(f"{n};{solution.get_solve_time()}", file=f)
    # Optimal
    if solution.is_solution_optimal():
        print("Optimal found CPO")
    # No solution
    if not solution.is_solution():
        print("Infeasible solution CPO")

    return solution.get_objective_value()
