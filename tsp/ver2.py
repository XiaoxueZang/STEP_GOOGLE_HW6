import sys
import math
global dist


def read_input(filename):
    with open(filename) as f:
        cities = []
        for (i, line) in enumerate(f.readlines()[1:]):  # Ignore the first line.
            xy = line.split(',')
            cities.append((float(xy[0]), float(xy[1])))
        return cities


def format_solution(solution):
    return 'index\n' + '\n'.join(map(str, solution))


def print_solution(solution):
    print(format_solution(solution))


def opt_1(size, path):
    global dist
    total = 0
    top_nearest = int(size)
    while True:
        count = 0
        for i in range(size-1):
            i1 = i + 1
            near_i = sorted(list(range(size)), key=lambda x: dist[path[i]][x])[1:top_nearest]
            near_i1 = sorted(list(range(size)), key=lambda x: dist[path[i1]][x])[1:top_nearest]

            for city in near_i:
                if city == path[i1]:
                    continue
                if city in near_i1:
                    j = path.index(city)
                    j0 = j-1
                    j1 = j+1
                    if j1 >= size:
                        j1 = 0
                    l1 = dist[path[i]][path[i1]]
                    l2 = dist[path[j0]][path[j]]
                    l3 = dist[path[j]][path[j1]]
                    l4 = dist[path[i]][path[j]]
                    l5 = dist[path[i1]][path[j]]
                    l6 = dist[path[j0]][path[j1]]
                    if l1 + l2 + l3 > l4 + l5 + l6:
                        #print(path)
                        new_path = path[:(i+1)] + [path[j]] + path[i1:]
                        new_path.pop(new_path.index(path[j0])+1)
                        path = new_path
                        #print(path)
                        assert len(path) == size
                        count += 1
        total += count
        if count == 0:
            break
    return path, total


def opt_2(size, path):
    global dist
    total = 0
    while True:
        count = 0
        for i in range(size - 2):
            i1 = i + 1
            for j in range(i + 2, size):
                if j == size - 1:
                    j1 = 0
                else:
                    j1 = j + 1
                if i != 0 or j1 != 0:
                    l1 = dist[path[i]][path[i1]]
                    l2 = dist[path[j]][path[j1]]
                    l3 = dist[path[i]][path[j]]
                    l4 = dist[path[i1]][path[j1]]
                    if l1 + l2 > l3 + l4:
                        new_path = path[i1:j + 1]
                        path[i1:j + 1] = new_path[::-1]
                        count += 1
        total += count
        if count == 0: break
    return path, total


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    N = len(cities)
    global dist
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    solution = [current_city]

    def distance_from_current_city(to):
        return dist[current_city][to]

    while unvisited_cities:
        next_city = min(unvisited_cities, key=distance_from_current_city)
        unvisited_cities.remove(next_city)
        solution.append(next_city)
        current_city = next_city
    #return opt_2(N, solution)
    return solution


def print_sum(solution):
    global dist
    SUM = 0
    for (i, pos) in enumerate(solution):
        if i != (len(solution) - 1):
            SUM += dist[pos][solution[i + 1]]
        else:
            SUM += dist[pos][0]
    print(SUM)

if __name__ == '__main__':
    assert len(sys.argv) > 1
    solution0 = solve(read_input(sys.argv[1]))
    #solution0 = solve(read_input("/Users/zangxiaoxue/step_google/google-step-tsp/input_2.csv"))
    solution1, count = opt_2(len(solution0), solution0)
    solution2, total = opt_1(len(solution1), solution1)
    print_solution(solution2)
