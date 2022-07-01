#! /usr/bin/env python3

import random
import argparse
import logging

def start_the_games(boxes, bruteforce):
    logging.debug('Running a {} test on {}'.format('brute force' if bruteforce else 'loop', boxes))
    for pris in boxes:
        res = check_inmate_random(boxes, pris) if bruteforce else check_inmate_loop(boxes, pris)
        if not res:
            return False
    return True

def check_inmate_loop(boxes, inmate_num):
    cur_box = inmate_num
    for i in range(1, int(len(boxes) / 2) + 1):
        if boxes[cur_box] == inmate_num:
            logging.debug('Inmate {} found their number in box {} on attempt '
                          '{}'.format(inmate_num, cur_box, i))
            return True
        else:
            logging.debug('Inmate {} found {} in box {} on attempt '
                          '{}'.format(inmate_num, boxes[cur_box], cur_box, i))
        cur_box = boxes[cur_box]
    logging.debug('Inmate {} did not find their number in time. Bummer'.format(inmate_num))
    return False

def check_inmate_random(boxes, inmate_num):
    choices = list(range(1, len(boxes) + 1))
    random.shuffle(choices)
    choices = choices[:int(len(choices) / 2)]

    logging.debug('Inmate {} is going to randomly try boxes {}'.format(inmate_num, choices))
    for i in range(0, len(choices)):
        guess = choices[i]
        if boxes[guess] == inmate_num:
            logging.debug('Inmate {} found their number in box {} on attempt '
                          '{}'.format(inmate_num, guess, i + 1))
            return True
        else:
            logging.debug('Inmate {} found {} in box {} on attempt '
                          '{}'.format(inmate_num, boxes[guess], guess, i + 1))

    logging.debug('Inmate {} did not find their number in time. Bummer'.format(inmate_num))
    return False

def fill_boxes(num_of_boxes):
    pris_nums = list(range(1, num_of_boxes + 1))
    random.shuffle(pris_nums)
    boxes = {}    
    for pris in range(1, num_of_boxes + 1):
        boxes[pris] = pris_nums[pris - 1]

    return boxes

def parse_args():
    parser = argparse.ArgumentParser(description='A number of prisoners must try to escape by '
                                                 'all of them finding their number in random '
                                                 'boxes, when each can only search half. '
                                                 'Will they succeed?')
    parser.add_argument('--debug', '-d', action='store_true', help='Verbose debugging')
    parser.add_argument('num_prisoners', type=int, help='How many prisoners?')
    parser.add_argument('iterations', type=int, help='How many times to run the test')
    parser.add_argument('--bruteforce', '-b', action='store_true', 
                        help='No strategy, just brute force it')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    successes = 0
    failures = 0
    for i in range(0, args.iterations):
        boxes = fill_boxes(args.num_prisoners)
        if start_the_games(boxes, args.bruteforce):
            successes += 1
        else:
            failures += 1
    logging.info('After {} runs with {} prisoners (using {}), there were {} successes and {} '
                 ' failures ({} percent '
                 'success)'.format(successes + failures, args.num_prisoners, 
                                   'no strategy' if args.bruteforce else 'loop strategy',
                                   successes, 
                                   failures, successes / (successes + failures)))

if __name__ == '__main__':
    main()    
