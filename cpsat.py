# Imports
from ortools.sat.python import cp_model
from config import TIMELIMIT


def build_cpsat_model(data):
    model = cp_model.CpModel()
    intervals = []
    tardiness = []
    for j in range(data['n']):
        start = model.NewIntVar(data['r'][j], data["deadline"][j], name=f"start_job{j}")
        end = model.NewIntVar(data['r'][j], data["deadline"][j], name=f"end_job_{j}")
        intervals.append(model.NewIntervalVar(start, data['p'][j], end, name=f"job_{j}"))
        t = model.NewIntVar(0, data["deadline"][j], name=f"tardiness_{j}")
        model.AddMaxEquality(t, [end - data['d'][j], 0])
        tardiness.append(t)
    model.AddNoOverlap(intervals)
    model.Minimize(cp_model.LinearExpr.WeightedSum(tardiness, data['w']))
    return model


def solve_cpsat(model, model_name, n):
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = TIMELIMIT
    solution = solver.Solve(model)
    # No solution
    if solution == cp_model.INFEASIBLE:
        return -1
    if solution == cp_model.OPTIMAL:
        print("Optimal found CPSAT")
    else:
        print("Non optimal solution CPSAT")
    # Bound
    print(solver.BestObjectiveBound())
    # Performance
    with open(f"output/log_{model_name}", 'a') as f:
        print(f"{n};{solver.WallTime()}", file=f)

    return round(solver.ObjectiveValue())
