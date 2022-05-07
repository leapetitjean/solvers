# Imports
from docplex.mp.model import Model
from config import TIMELIMIT


def build_first_model(data):
    model = Model('First model')
    model.set_time_limit(TIMELIMIT)
    # Data
    jobs = range(data["n"])
    # Preprocessing
    M = max(data["deadline"])
    # Variables
    C = model.continuous_var_list(keys=jobs, name="C")
    T = model.continuous_var_list(keys=jobs, name="T")
    y = model.binary_var_matrix(keys1=jobs, keys2=jobs, name="y")
    # Constraints
    model.add_constraints(C[j] <= data["deadline"][j] for j in jobs)
    model.add_constraints(C[j] >= data["r"][j] + data["p"][j] for j in jobs)
    model.add_constraints(T[j] >= 0 for j in jobs)
    model.add_constraints(T[j] >= C[j] - data["d"][j] for j in jobs)
    model.add_constraints(C[j] <= C[i] - data["p"][i] + M * y[i, j]
                          if j < i else C[j] >= 0 for i in jobs for j in jobs)
    model.add_constraints(C[i] <= C[j] - data["p"][j] + M * (1 - y[i, j])
                          if j < i else C[i] >= 0 for i in jobs for j in jobs)
    # Objective
    model.minimize(model.sum(T[j] * data["w"][j] for j in jobs))

    return model


def build_rank_model(data):
    model = Model('Rank model')
    model.set_time_limit(TIMELIMIT)
    # Data
    jobs = range(data["n"])
    # Preprocessing
    M = max(data["deadline"])
    # Variables
    C = model.continuous_var_list(keys=jobs, name="C")
    T = model.continuous_var_list(keys=jobs, name="T")
    Tp = model.continuous_var_list(keys=jobs, name="Tp")
    a = model.binary_var_matrix(keys1=jobs, keys2=jobs, name="a")
    # Constraints
    model.add_constraints(model.sum(a[k, j] for j in jobs) == 1 for k in jobs)
    model.add_constraints(model.sum(a[j, k] for j in jobs) == 1 for k in jobs)
    model.add_constraints(C[k] <= model.sum(data["deadline"][j] * a[k, j]
                                            for j in jobs) for k in jobs)
    model.add_constraints(C[k] >= model.sum((data["r"][j] + data["p"][j]) * a[k, j]
                                            for j in jobs) for k in jobs)
    model.add_constraints(T[k] >= 0 for k in jobs)
    model.add_constraints(T[k] >= C[k] - model.sum(data["d"][j] * a[k, j]
                                                   for j in jobs) for k in jobs)
    model.add_constraints(C[k-1] <= C[k] - model.sum(data["p"][j] * a[k, j]
                                                     for j in jobs) for k in range(1, data["n"]))
    model.add_constraints(M * (1 - a[k, j]) + Tp[j] >= T[k] for j in jobs for k in jobs)
    # Objective
    model.minimize(model.sum(Tp[j] * data["w"][j] for j in jobs))

    return model


def solve_mip(model, model_name, n):
    solution = model.solve()
    if solution is None:
        return -1
    # Performance
    with open(f"output/log_{model_name}", 'a') as f:
        print(f"{n};{solution.solve_details.time}", file=f)
    # Bound
    print("MIP best bound :")
    print(solution.solve_details.best_bound)

    return round(solution.get_objective_value())
