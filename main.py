#!/usr/bin/python3

# Imports
from sys import argv
from pathlib import Path
from os import remove
from os.path import exists
import matplotlib.pyplot as plt
from pandas import read_csv
from mip import *
from cpo import *
from cpsat import *
from local import *
from data_tools import *


MODELS = ["first", "rank", "cpo", "cpsat", "localsolver"]


def run_instance(file_name, model_name):
    data = import_data(file_name)
    n = data['n']
    if model_name == "first":
        model = build_first_model(data)
        return solve_mip(model, model_name, n)
    elif model_name == "rank":
        model = build_rank_model(data)
        return solve_mip(model, model_name, n)
    elif model_name == "cpo":
        model = build_cpo_model(data)
        return solve_cpo(model, model_name, n)
    elif model_name == "cpsat":
        model = build_cpsat_model(data)
        return solve_cpsat(model, model_name, n)
    elif model_name == "localsolver":
        return build_localsolver_model(data)
    else:
        print_model_error(model_name)


def print_gaps(solutions):
    while solutions[0][0] == -1:
        solutions.remove(solutions[0])
    for i in range(1, len(solutions)):
        print(f"Gap between best solution {solutions[0][1]} and {solutions[i][1]}: "
              f"{(solutions[i][0] - solutions[0][0]) / solutions[0][0]}")


def show_perf(models_name):
    plt.title("Performances")
    plt.xlabel("Nombre de tâches")
    plt.ylabel("Temps de résolution")
    for model_name in models_name:
        file_name = f"output/log_{model_name}"
        if exists(file_name):
            data = read_csv(file_name, sep=";")
            data = data.sort_values(by=["nb"])
            # median can be change by mean or quantile(value)
            data = data.groupby(["nb"])["time"].median().reset_index()
            plt.plot(data["nb"], data["time"], label=f"Modèle : {french_name(model_name)}")
        else:
            print(f"\033[31mError: \033[0mNon-existent file {file_name}")
            exit(1)
    plt.legend()
    plt.show()


def french_name(model_name):
    if model_name == "first":
        return "MIP Premier"
    if model_name == "rank":
        return "MIP Rang"
    if model_name == "cpo":
        return "CPO"
    if model_name == "cpsat":
        return "CPSAT"


def init_log(models_name):
    for model_name in models_name:
        with open(f"output/log_{model_name}", "w") as f:
            print("nb;time", file=f)


def print_model_error(model_name):
    print(f"\033[31mError: \033[0mUnknown model {model_name}\n"
          f"    Expected one of: {MODELS}")
    exit(1)


def print_usage():
    print(f"\033[34mUsage:\n"
          f"    \033[35mInitialize log file: \033[0m./main.py -i <{MODELS}> ...\n"
          f"    \033[35mShow performance model: \033[0m./main.py -p <{MODELS}> ...\n"
          f"    \033[35mGenerate instance: \033[0m./main.py -g <instance_size> ...\n"
          f"    \033[35mRun instance: \033[0m./main.py -r <{MODELS}> <instance_name> ...\n"
          f"    \033[35mShow results and gap between all models: \033[0m./main.py -a <lower_bound> "
          f"<upper_bound> <nb_iter>\n"
          f"    \033[35mShow performance of a specific model: \033[0m./main.py -am "
          f"<model_name> <lower_bound> <upper_bound> <nb_iter>\n"
          f"    \033[34mClean repertory: \033[0m./main.py --clean\n"
          f"    \033[34mHelp (see more details): \033[0m./main.py --help")


def option_error():
    print("\033[31mError: \033[0mNot enough arguments")
    print_usage()
    exit(1)


def show_help():
    print(f"\033[34mOptions:\n"
          f"    \033[35m-i: \033[0mInitialize the file log_<model_name> with the two columns nb;time "
          f"for each models passed as arguments, you can pass several models at once.\n"
          f"    \033[32mExample: \033[35m./main.py -i first rank\033[0m will initialize both log_first and log_rank\n"
          f"    \033[35m-p: \033[0mDisplay the performance graph on the log_<model_names> data "
          f"for <model_names> passed as arguments\n"
          f"    \033[32mExample: \033[35m./main.py -p first rank\033[0m will display a graph with "
          f"log_first and log_rank data\n"
          f"    \033[35m-g: \033[0mGenerate instances of the size passed in arguments\n"
          f"    \033[32mExample: \033[35m./main.py -g 5 10\033[0m will generate an instance of size 5 and 10 "
          f"in example_5.dat and example_10.dat\n"
          f"    \033[35m-r: \033[0mRun <model_name> on the instances passed as arguments, "
          f"you can pass several .dat files\n"
          f"    \033[32mExample: \033[35m./main.py -r example_5.dat example_10.dat\033[0m will run the model "
          f"on both example_5.dat and example_10.dat instances\n"
          f"    \033[35m-a: \033[0mGenerate instances from size <lower_bound> to size <upper_bound>, "
          f"run it <nb_iter> times on all models and print results and gap between all models"
          f"    \033[32mExample: \033[35m./mip -a 1 12\033[0m generates instances from 1 to 12 (excluded), "
          f"run it on all {MODELS} and show performance of all models\n"
          f"    \033[35m-am: \033[0mGenerate instances from size <lower_bound> to size <upper_bound>, " 
          f"run it <nb_iter> times on the specified model and show the performance of the model with "
          f"the initialized log file\n"
          f"    \033[32mExample: \033[35m./mip -am {MODELS} 1 12\033[0m generates instances from 1 to 12 (excludes), "
          f"run it on <model_name> and shows the performance graph")


def main(args):
    # Control options
    if len(args) < 2:
        option_error()
    option = args[1]
    if option == "--help":
        show_help()
    elif option == "--clean":
        for p in Path(".").glob("data/example_*"):
            remove(p)
        for p in Path(".").glob("output/log_*"):
            remove(p)
        print("\033[32mSuccessfully cleaned\033[0m")
    elif len(args) < 3:
        option_error()
    # 2-arguments options
    elif option == "-p":
        model_names = args[2:]
        for model_name in model_names:
            if model_name not in MODELS:
                print_model_error(model_name)
        show_perf(model_names)
    elif option == "-i":
        model_names = args[2:]
        for model_name in model_names:
            if model_name not in MODELS:
                print_model_error(model_name)
        init_log(model_names)
    elif option == "-g":
        for size in args[2:]:
            size = int(size)
            generate_instance(size)
    # 3-arguments options
    elif len(args) < 4:
        option_error()
    elif option == "-r":
        model_name = args[2]
        if model_name not in MODELS:
            print_model_error(model_name)
        for file_name in args[3:]:
            run_instance(file_name, model_name)
    elif len(args) < 5:
        option_error()
    elif option == "-a":
        lb = int(args[2])
        ub = int(args[3])
        nb_iter = int(args[4])
        init_log(MODELS)
        for size in range(lb, ub):
            for i in range(nb_iter):
                file_name = generate_instance(size, i+1)
                solutions = []
                for model_name in MODELS:
                    solutions.append(run_instance(file_name, model_name))
                solutions = sorted(zip(solutions, MODELS))
                print(file_name)
                print(*solutions)
                print_gaps(solutions)
    elif len(args) < 6:
        option_error()
    elif option == "-am":
        model_name = args[2]
        lb = int(args[3])
        ub = int(args[4])
        nb_iter = int(args[5])
        if model_name not in MODELS:
            print_model_error(model_name)
        init_log([model_name])
        for size in range(lb, ub):
            file_name = generate_instance(size)
            for _ in range(nb_iter):
                run_instance(file_name, model_name)
        show_perf([model_name])
    else:
        print(f"\033[31mError: \033[0mUnknown option {option}")
        print_usage()


if __name__ == '__main__':
    main(argv)
