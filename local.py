# Imports
import localsolver
from config import TIMELIMIT


def build_localsolver_model(data):
    with localsolver.LocalSolver() as ls:
        model = ls.model
        ls.param.time_limit = TIMELIMIT
        ls.param.verbosity = False

        job_order = model.list(data['n'])
        model.constraint(model.count(job_order) == data['n'])

        release_dates = model.array(data['r'])
        deadlines = model.array(data["deadline"])
        due_dates = model.array(data['d'])
        processing_times = model.array(data['p'])
        weights = model.array(data['w'])

        job_time_selector = model.lambda_function(lambda j, prev:
                                                  model.iif(j > 0,
                                                            model.max(prev, release_dates[job_order[j]])
                                                            + processing_times[job_order[j]],
                                                            release_dates[job_order[j]] + processing_times[job_order[j]]
                                                            ))
        C = model.array(model.range(0, data['n']), job_time_selector)

        objective = model.sum()
        for i in range(data['n']):
            j = job_order[i]
            model.constraint(C[i] <= deadlines[j])
            model.constraint(C[i] >= release_dates[j] + processing_times[j])
            Tj = model.iif(C[i] > due_dates[j], C[i] - due_dates[j], 0)
            objective.add_operand(Tj * weights[j])

        model.minimize(objective)
        model.close()
        ls.solve()

        return objective.value
