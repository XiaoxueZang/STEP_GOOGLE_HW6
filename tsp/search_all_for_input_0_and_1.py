import sys
import math
import copy
global solution
global dist
solution = []


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def read_input(filename):
    with open(filename) as f:
        cities = []
        for (i,line) in enumerate(f.readlines()[1:]):  # Ignore the first line.
            xy = line.split(',')
            cities.append((float(xy[0]), float(xy[1])))
        return cities


def format_solution(solution):
    return 'index\n' + '\n'.join(map(str, solution))


def print_solution(solution):
    print(format_solution(solution))


def perm(finish, explore):
    if len(explore) == 0:
        global solution
        solution.append(copy.deepcopy(finish))
    for x in explore:
        finish.append(x)
        refresh_explore = explore.copy()
        refresh_explore.remove(x)
        perm(finish, refresh_explore)
        finish.pop()


def solve(cities):
    N = len(cities)
    global dist
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    start = [0]
    explore = list(range(1, N))
    perm(start, explore)
    global solution
    MIN = float('inf')

    for route in solution:
        SUM = 0
        for(i, x) in enumerate(route):
            if i == (len(route)-1):
                SUM += dist[0][x]
            else:
                SUM += dist[x][route[i+1]]
        if SUM < MIN:
            MIN = SUM
            shortest = route
    return shortest, MIN

if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution, length = solve(read_input(sys.argv[1]))
    #solution, length = solve(read_input("/Users/zangxiaoxue/step_google/google-step-tsp/input_2.csv"))
    print_solution(solution)
    print(length)