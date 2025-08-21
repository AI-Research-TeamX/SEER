import os
import sys
import random
from datetime import datetime
import time

# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from llm_agents import Controller, TaskClassifier
from llm_evaluator import llm_evaluate
from utils import load_args_from_config, parse_classification, print_args

from prompt_library.selection import ExampleSelection

import jsonlines

current_datetime = datetime.now()
datetime_string = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")

CORRECT = 'correct'
INCORRECT = 'incorrect'
HALTED = 'halted'

def run_all_random(args, fpath, classifier_tag, preference_tag):
    __console__ = sys.stdout
    print_args(args)
    datasets = ['flight', 'coffee', 'yelp', 'airbnb', 'dblp', 'scirex', 'agenda', 'gsm8k'] if not args.dataset else list(args.dataset.split(' '))
    hardnesses = ['easy', 'hard']

    contents = []
    for dataset in datasets:
        for hardness in hardnesses:
            # no gsm8k-hard
            if dataset == 'gsm8k' and hardness == 'hard': continue
            file_path = f"data/questions/{hardness}/{dataset}-{hardness}.jsonl"
            with open(file_path, 'r') as f:
                for item in jsonlines.Reader(f):
                    contents.append(item)

    random.seed(int(args.seed))
    random.shuffle(contents)
    # contents = contents[:]
    window_len = 153
    window_results = []
    assert len(contents) % window_len == 0
    
    library_init_path = "seer/prompt_library/library.json"

    for window_index in range(len(contents) // window_len):
        wind_start = window_index * window_len
        wind_end = (window_index + 1) * window_len

        vfile = f"{fpath}/tap_{wind_start}_{wind_end}.log"
        # log file exists or not
        if os.path.exists(vfile):
            # open and check finished or not
            with open(vfile, 'r') as f:
                lines = f.readlines()
                if ''.join(lines).count(f"{'='*20} SUMMARY {'='*20}") == 2:
                    continue

        if window_index == 0:
            selector = ExampleSelection(init_path=library_init_path)
        else:
            library_load_path = f"{fpath}/library-{wind_start}.json"
            assert os.path.exists(library_load_path)
            selector = ExampleSelection(init_path=library_load_path)
        controller = Controller(args, selector=selector)
    
        sys.stdout = open(vfile, mode = 'w')

        args.dataset = f"random_{wind_start}_{wind_end}"
        args.hardness = "random"

        print_args(args)
        sum_results = []
        tmp_example = []

        print("=" * 10 + f"Start: {wind_start}-{wind_end}" + "=" * 10)
        
        evaluate_correct = 0
        for _ in range(window_len):
            i = window_index * window_len + _

            tmp = controller.run_tap(contents[i]['question'], contents[i]['answer'], classifier_tag=classifier_tag, preference_tag=preference_tag)
            sum_results.append(tmp)

            # tmp data structure
            if llm_evaluate(tmp['question'], tmp['key'], tmp['answer']):
                print(f"{'='*10}LLM_Evaluate_Correct{'='*10}")
                evaluate_correct += 1
                if controller.solver.prompt_tag == "solver_adaptive":
                    tmp_example.append(tmp)
            else:
                print(f"{'='*10}LLM_Evaluate_Incorrect{'='*10}")

        for tmp in tmp_example:
            selector.add_example(tmp)

        print("=" * 10 + f"End: {wind_start}-{wind_end}" + "=" * 10)
        
        selector.save_library(f"{fpath}/library-{wind_end}.json")

        # print all result
        print(f"{'='*20} SUMMARY {'='*20}")
        for result in sum_results:
            print(f"Question:{result['question']}")
            print(f"Classifier:{result['class']}")
            print(f"Decomposer:{result['tools']}")
            print(f"Handler:{result['paras']}")
            print(f"Results:{result['results']}")
            print(f"GT vs Answer:{{{result['key']}}}-{{{result['answer']}}}")
        print(f"{'='*20} SUMMARY {'='*20}")
        """
        {
            'question':str
            'key':str
            'class':str
            'tools':[]
            'paras':[]
            'results':[]
            'answer':str
            'scratchpad':str
        }
        """

        # LLM evaluator
        print(f"{'='*20} LLM-EVALUATION {'='*20}")
        print(f"LLM evaluator: {evaluate_correct}/{len(sum_results)}={evaluate_correct/len(sum_results)*100}%")
        print(f"{'='*20} LLM-EVALUATION {'='*20}")
        print(flush=True)
        sys.stdout = __console__

        window_results.append(f"{evaluate_correct}/{len(sum_results)}")
    return window_results


if __name__ == "__main__":
    print(f"START:{datetime.now().strftime('%Y%m%d_%H%M%S')}")    
    fpath = load_args_from_config().fpath
    if not os.path.exists(fpath):
        try:
            os.makedirs(fpath)
            print(f"Path '{fpath}' did not exist, but it has been created.")
        except Exception as e:
            raise ValueError(f"Error: Unable to create path '{fpath}'. {e}")

    res = run_all_random(
        args=load_args_from_config(temp=0),
        fpath=fpath,
        classifier_tag=True,
        preference_tag=False
    )

    with open(f"{fpath}/done.log", 'w') as f:
        f.write(f"ok\n{res}")

    print(f"DONE:{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    pass
