import multiprocessing
def _run_code(python_code, return_dict):
    global_var = {}
    exec(python_code, global_var)
    return_dict['answer'] = global_var['answer']

def execute(python_code, timeout=5):
    """
    Returns the path to the python interpreter. with 5s timeout
    """
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    process = multiprocessing.Process(target=_run_code, args=(python_code, return_dict))
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        return f"Execution timed out (possible infinite loop)."
    return str(return_dict['answer'])

def execute_original(python_code):
    """
    Returns the path to the python interpreter.
    """
    global_var = {}
    exec(python_code, global_var)
    # print(str(global_var))
    return str(global_var['answer'])

if __name__ == "__main__":
    python_code = "import geopy\nimport geopy.distance\nlatitude = 40.05555\nlongitude = -75.090723\n_, lo_max, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=90)\n_, lo_min, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=270)\nla_max, _, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=0)\nla_min, _, _ = geopy.distance.distance(kilometers=5).destination(point=(latitude, longitude), bearing=180)\nanswer = (la_max, la_min, lo_max, lo_min)"
    global_var = {"answer": 0}
    answer = execute(python_code)
    print(answer)