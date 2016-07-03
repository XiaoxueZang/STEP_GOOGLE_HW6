import sys
import math
global dist
import random

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
            both_near = set(near_i).intersection(near_i1)
            for city in both_near:
                if city==i or city==i1:
                    continue
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


def opt_3(size, path):
    global dist
    total = 0
    if size > 1000:
        top_nearest = 100
    else:
        top_nearest = int(size/2)
    while True:
        count = 0
        for i in range(size - 2):
            i1 = i + 1
            near_i = sorted(list(range(size)), key=lambda x: dist[path[i]][x])[1:top_nearest]
            near_i1 = sorted(list(range(size)), key=lambda x: dist[path[i1]][x])[1:top_nearest]
            both_near = set(near_i).intersection(near_i1)

            for city in both_near:
                if path.index(city) in list([i-1, i, i1, i1+1]):
                    continue
                j1 = path.index(city)
                if j1 == size-1:
                    j2 = 0
                else: j2 = j1+1
                if path[j2] in both_near:
                    j0 = j1 - 1
                    if j2 >= size-1:
                        j3 = 0
                    else:
                        j3 = j2 + 1
                    l1 = dist[path[i]][path[i1]]
                    l2 = dist[path[j0]][path[j1]]
                    l3 = dist[path[j2]][path[j3]]
                    l4 = dist[path[j0]][path[j3]]
                    if dist[path[i]][path[j2]] > dist[path[i]][path[j1]]:
                        connect_i = j1
                        connect_i1 = j2
                    else:
                        connect_i = j2
                        connect_i1 = j1
                    l5 = dist[path[i]][path[connect_i]]
                    l6 = dist[path[i1]][path[connect_i1]]
                    if l1 + l2 + l3 > l4 + l5 + l6:
                        new_path = path[:(i+1)] + [path[connect_i], path[connect_i1]] + path[i1:]
                        real_j1 = path[connect_i]
                        real_j2 = path[connect_i1]
                        if new_path.index(path[j0]) == len(new_path)-1:
                            # for debugging
                            if new_path[0] != real_j1 and new_path[0]!=real_j2:
                                print(real_j1, real_j2, new_path[0], new_path[1], new_path[-1])
                                sys.exit(1)
                            # debugging finish
                            new_path.pop(0)
                        else:
                            new_path.pop(new_path.index(path[j0]) + 1)
                        new_path.pop(new_path.index(path[j3]) - 1)
                        if len(set(new_path)) != size:
                            print(len(new_path))
                        assert len(set(new_path)) == size
                        path = new_path
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
    solution1, count = opt_2(len(solution0), solution0)
    solution2, total = opt_3(len(solution1), solution1)
    solution3, total1 = opt_1(len(solution2), solution2)
    print_solution(solution3)


