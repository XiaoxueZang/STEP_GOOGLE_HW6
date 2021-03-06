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
def opt2: diminish the crosses
def opt3

I think the sequence and times of conducting those 3 optimization trials affect the final result, which leaves space for further experiments.

Reference:
I got hint form this website: http://www.geocities.jp/m_hiroi/light/pyalgo62.html

I hope this website could be helpful to you as well:)

#7/4 追加:
ver4_give_best_anser_to_input_3.py gives best answer for input_3(just like its name)
I initially wanted to combine opt1 and opt3 into one function to save calculation time(which is how def opt1 works in this code). I coincidently found that this code gives best answer for input_3.csv and input_6.csv.
The score for input_6.csv is 40939.337940293706
and the calculated path is saved in solution_yours_6_best_by_ver4.csv
However, the execution time for input_6.csv is like:

real	46m30.051s
user	45m13.075s
sys	0m18.036s

It is so costly:(

#7/5:
Add BoltzmanSA.cpp
I tried Boltzmann Machine with Simulated Annealing. I copied the code from internet and added several changes.
I found finding the proper parameter is hard and SA is a slow method for it includes several redundant calculations.
The related files could be seen in directory SA
The code file is BoltzmanSA.cpp. It gives solutions for input_0.csv and input_1.csv. Its solutions do not surpass former solutions. I found it hard to choose proper parameters for the code. Thus, I abandon this method.

#7/7:
Add ver5_for_input_6.py in directory tsp
I tried to divide the graph into 4 parts and merge them together. Its performance did not surpass former ones, but it is a little bit quicker than greedy_op2_ver1.py for input_6.csv 
The execution time is 0m13.620s.
If graph is divided into more parts, better performance is expected.

One idea about input_7.csv
I think it might be feasible to divide the nodes into many parts and merge them together to give one solution.

