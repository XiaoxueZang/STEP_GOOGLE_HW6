import sys
import math
global dist
import random


def read_input(filename):
    with open(filename) as f:
        cities = []
        for (i, line) in enumerate(f.readlines()[1:]):  # Ignore the first line.
            xy = line.split(',')
            cities.append((float(xy[0]), float(xy[1]), i))
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
                if path.index(city)==i or path.index(city)==i1:
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


def divide(cities, to_how_many_parts=4):
    N = len(cities)

    cities.sort(key=lambda x: x[0]) #sort along x axis
    left = cities[:int(N/2+1)]
    middle = cities[int(N/2)]
    right = cities[int(N/2):]
    left.sort(key=lambda x: x[1]) #sort along y axis
    right.sort(key=lambda x: x[1])
    cities1 = left[:int(len(left)/2+1)]
    left_middle = left[int(len(left)/2)]
    cities2 = left[int(len(left)/2):]
    cities3 = right[:int(len(right)/2+1)]
    right_middle = right[int(len(right)/2)]
    cities4 = right[int(len(right)/2):]
    return [cities1, cities2, cities3, cities4], [middle, left_middle, right_middle]


def differ(p, c, q):
    global dist
    return dist[p][c] + dist[c][q] - dist[p][q]


def make_new_path(buff, c, succ):
    path = []
    i = c + succ
    while True:
        if i < 0: i = len(buff) - 1
        elif i >= len(buff): i = 0
        if i == c: break
        path.append(buff[i])
        i += succ
    return path


def merge(solution1, solution2, connect):
    size1 = len(solution1)
    size2 = len(solution2)
    i1 = solution1.index(connect)
    j1 = solution2.index(connect)
    if i1 ==size1-1:
        i2 = 0
    else:
        i2 = i1+1
    if j1 == size2-1:
        j2 = 0
    else:
        j2 = j1+1
    j0 = j1-1
    i0 = i1-1

    d1 = differ(solution1[i0], connect, solution2[j2])
    d2 = differ(solution1[i0], connect, solution2[j0])
    d3 = differ(solution1[i2], connect, solution2[j2])
    d4 = differ(solution1[i2], connect, solution2[j0])
    # 差分が一番大きいものを選択
    d = max(d1, d2, d3, d4)
    if d1 == d:
        solution1[i1:i1] = make_new_path(solution2, j1, 1)
    elif d2 == d:
        # (2)
        solution1[i1:i1] = make_new_path(solution2, j1, -1)
    elif d3 == d:
        # (3)
        solution1[i2:i2] = make_new_path(solution2, j1, 1)
    else:
        # (4)
        solution1[i2:i2] = make_new_path(solution2, j1, -1)
    solution1, total = opt_2(len(solution1), solution1)
    return solution1

def solve(cities):
    N = len(cities)
    global dist
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    def distance_from_current_city(to):
        return dist[current_city][to]
    solutions = []
    cities_group, connections = divide(cities)
    for cities_part in cities_group:
        current_city = cities_part[0][2]
        unvisited_cities = set([x[2] for x in cities_part[1:]])
        solution = [current_city]

        while unvisited_cities:
            next_city = min(unvisited_cities, key=distance_from_current_city)
            unvisited_cities.remove(next_city)
            solution.append(next_city)
            current_city = next_city
        solutions.append(solution)
    solution_left = merge(solutions[0], solutions[1], connections[1][2])
    solution_right = merge(solutions[2], solutions[3], connections[2][2])
    solution_all = merge(solution_left, solution_right, connections[0][2])
    assert len(set(solution_all))==N
    return solution_all



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
    solution1 = solve(read_input(sys.argv[1]))

    #solution1 = solve(read_input("/Users/zangxiaoxue/step_google/google-step-tsp/input_3.csv"))
    solution2, total = opt_2(len(solution1), solution1)
    print_solution(solution2)

