search_all_for_input_0_and_1.py: 全探索です
ver3_best_temp.py: returns the best result for now(07/03)
The problem is that for input_6.csv, the speed is quite slow.
You could try greedy_op2_ver1.py to have a relatively good result(42712.37) in shorter time:
real	0m19.151s
user	0m18.477s
sys	0m0.204s

My idea is mainly to improve greedy search algorithm.
I search and change time-consuming routes into shorter routes.
They could be read in 3 functions:
def opt1
def opt2
def opt3

I think the sequence and times of conducting those 3 optimization trials affect the final result, which leaves space for further experiments.