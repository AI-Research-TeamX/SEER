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


def test_classifier(args):
    print_args(args)
    datasets = ['flight', 'coffee', 'yelp', 'airbnb', 'dblp', 'scirex', 'agenda', 'gsm8k']
    hardnesses = ['easy', 'hard']

    logs_list = []
    total_sum = [0, 0, 0, 0]
    classifier = TaskClassifier(args)
    print(f"Prompt of classifier: {classifier.prompt}")
    print(f"Information: {classifier.databases_info}")
    print(f"Examples: {classifier.examples}")
    
    for hardness in hardnesses:
        for dataset in datasets:
            # no gsm8k-hard
            if dataset == 'gsm8k' and hardness == 'hard': continue

            args.dataset = dataset
            args.hardness = hardness

            print("=" * 10 + f"Classifier Start: {args.dataset}-{args.hardness}" + "=" * 10)
            
            file_path = f"data/questions/{args.hardness}/{args.dataset}-{args.hardness}.jsonl"
            with open(file_path, 'r') as f:
                contents = []
                for item in jsonlines.Reader(f):
                    contents.append(item)

            trial = 0
            correct_questions = []
            incorrect_questions = []
            error_questions = []

            for i in range(len(contents)):
                print(f"Question {contents[i]['qid']}: {contents[i]['question']}")
                try:
                    response = classifier.run(contents[i]['question'])
                    result = parse_classification(response)
                    if result:
                        if result.lower() == args.dataset:
                            correct_questions.append(contents[i]['qid'])
                            print(f"Classif_is_correct: GT={args.dataset} Answer={result}")
                        else:
                            incorrect_questions.append(f"{contents[i]['qid']}: {response}")
                            print(f"Classif_is_incorrect: GT={args.dataset} Response={response}")
                    else:
                        error_questions.append(f"{contents[i]['qid']}: parse_error={response}")
                        print(f"Error parse_error: qid={contents[i]['qid']} parse_error={response}")
                except Exception as e:
                    error_questions.append(f"{contents[i]['qid']}: run_error={e}")
                    print(f"Error run_error: qid={contents[i]['qid']} run_error={e}")

                trial += 1
            
            correct_logs = f'Correct/All: {len(correct_questions)}/{trial}'
            incorrect_logs = f'Incorrect/All: {len(incorrect_questions)}/{trial}, {incorrect_questions}'
            error_logs = f'Error/All: {len(error_questions)}/{trial}, {error_questions}'
            print(correct_logs)
            print(incorrect_logs)
            print(error_logs)
            print("=" * 10 + f"Classifier End: {args.dataset}-{args.hardness}" + "=" * 10)

            logs_list.append(correct_logs)
            logs_list.append(incorrect_logs)
            logs_list.append(error_logs)
            total_sum[0] += len(correct_questions)
            total_sum[1] += len(incorrect_questions)
            total_sum[2] += len(error_questions)
            total_sum[3] += trial

    print("=" * 10 + f"Total Summary" + "=" * 10)
    for _log in logs_list:
        print(_log)
    print(f"Total correct: {total_sum[0]}/{total_sum[3]}")
    print(f"Total incorrect: {total_sum[1]}/{total_sum[3]}")
    print(f"Total error: {total_sum[2]}/{total_sum[3]}")
    print("=" * 10 + f"Total Summary" + "=" * 10)


def test_classifier_all():
    __console__=sys.stdout

    args = load_args_from_config()

    sys.stdout = open(f'{args.classifier_engine}_classification_v6.log', mode = 'w')
    args.classifier_prompt = 'classifier'
    test_classifier(args)
    sys.stdout = __console__

    sys.stdout = open(f'{args.classifier_engine}_classification_v6_no_info.log', mode = 'w')
    args.classifier_prompt = 'classifier_no_info'
    test_classifier(args)
    sys.stdout = __console__

    sys.stdout = open(f'{args.classifier_engine}_classification_v6_zero_shot.log', mode = 'w')
    args.classifier_prompt = 'classifier_zero_shot'
    test_classifier(args)
    sys.stdout = __console__


def test_decomposer_handler_all(fpath):
    # __console__=sys.stdout
    modes_list = {
        'origin': [True, False],
        'noclass': [False, None],
        'preference': [True, True]
    }

    temps = {'t1':0, 't2':0.2, 't3':0.5, 't4':0.7, 't5':1.0}
    for tag in ['t1']:
        # v5: origin
        mode = 'origin'
        args = load_args_from_config(temp=temps[tag])
        vfile = f"{fpath}/tap_{mode}_{tag}"
        test_decomposer_handler(args, fpath, vfile, classifier_tag=modes_list[mode][0], preference_tag=modes_list[mode][1])

        # # v5: noclass
        # mode = 'noclass'
        # args = load_args_from_config(temp=temps[tag])
        # vfile = f"{fpath}/tap_{mode}_{tag}"
        # test_decomposer_handler(args, fpath, vfile, classifier_tag=modes_list[mode][0], preference_tag=modes_list[mode][1])
    
    print("RUNNING TASK DONE")
    # sys.stdout = __console__


def test_decomposer_handler(args, fpath, vflie, classifier_tag, preference_tag):
    __console__ = sys.stdout
    print_args(args)
    # datasets = ['flight', 'coffee'√, 'yelp'√, 'airbnb', 'dblp'√, 'scirex'√, 'agenda'√, 'gsm8k'√]
    # hardnesses = ['easy', 'hard']
    datasets = ['flight', 'coffee', 'yelp', 'airbnb', 'dblp', 'scirex', 'agenda', 'gsm8k'] if not args.dataset else list(args.dataset.split(' '))
    hardnesses = ['easy', 'hard']

    library_init_path = "seer/prompt_library/library.json"
    library_save_path = f"{fpath}/library.tmp.json"
    if os.path.exists(library_save_path):
        selector = ExampleSelection(init_path=library_save_path)
    else:
        selector = ExampleSelection(init_path=library_init_path)
    controller = Controller(args, selector=selector)
    
    for dataset in datasets:
        for hardness in hardnesses:
            # no gsm8k-hard
            if dataset == 'gsm8k' and hardness == 'hard': continue

            sleep_when_working = False
            if sleep_when_working:
                while datetime.now().day <= 5 and datetime.now().hour >= 8 and datetime.now().hour < 20:
                    time.sleep(1*60*60)
            # log file exists or not
            if os.path.exists(f'{vflie}_{dataset}_{hardness}.log'):
                # open and check finished or not
                with open(f'{vflie}_{dataset}_{hardness}.log', 'r') as f:
                    lines = f.readlines()
                    if ''.join(lines).count(f"{'='*20} SUMMARY {'='*20}") == 2:
                        continue

            sys.stdout = open(f'{vflie}_{dataset}_{hardness}.log', mode = 'w')

            args.dataset = dataset
            args.hardness = hardness

            print_args(args)
            sum_results = []
            print("=" * 10 + f"Start: {args.dataset}-{args.hardness}" + "=" * 10)
            
            file_path = f"data/questions/{args.hardness}/{args.dataset}-{args.hardness}.jsonl"
            with open(file_path, 'r') as f:
                contents = []
                for item in jsonlines.Reader(f):
                    contents.append(item)

            evaluate_correct = 0
            for i in range(0, len(contents)):
                tmp = controller.run_tap(contents[i]['question'], contents[i]['answer'], classifier_tag=classifier_tag, preference_tag=preference_tag)
                sum_results.append(tmp)

                # tmp data structure
                if llm_evaluate(tmp['question'], tmp['key'], tmp['answer']):
                    print(f"{'='*10}LLM_Evaluate_Correct{'='*10}")
                    evaluate_correct += 1
                    if controller.solver.prompt_tag == "solver_adaptive":
                        selector.add_example(tmp)
                else:
                    print(f"{'='*10}LLM_Evaluate_Incorrect{'='*10}")
                # break

            print("=" * 10 + f"End: {args.dataset}-{args.hardness}" + "=" * 10)
            
            # save selector
            selector.save_library(library_save_path)

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


if __name__ == "__main__":
    print(f"START:{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    # test_classifier_all()
    fpath = load_args_from_config().fpath
    if not os.path.exists(fpath):
        try:
            os.makedirs(fpath)
            print(f"Path '{fpath}' did not exist, but it has been created.")
        except Exception as e:
            raise ValueError(f"Error: Unable to create path '{fpath}'. {e}")

    test_decomposer_handler_all(fpath)
    print(f"DONE:{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    pass
