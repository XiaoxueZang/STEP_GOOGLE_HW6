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
            both_near = set(near_i).intersection(near_i1)
            if i == 0:
                i0 = size - 1
            else:
                i0 = i - 1
            if i1 == size - 1:
                i2 = 0
            else:
                i2 = i1 + 1
            for city in both_near:
                if path.index(city) in list([i0, i, i1, i2]):
                    continue
                j1 = path.index(city)
                j0 = j1-1
                if j1 == size-1:
                    j2 = 0
                else:
                    j2 = j1+1
                if j2 == size-1:
                    j3 = 0
                else:
                    j3 = j2+1
                l1 = dist[path[i]][path[i1]]
                l2 = dist[path[j0]][path[j1]]
                l3 = dist[path[j1]][path[j2]]
                l4 = dist[path[i]][path[j1]]
                l5 = dist[path[i1]][path[j1]]
                l6 = dist[path[j0]][path[j2]]
                change = False
                if l1 + l2 + l3 > l4 + l5 + l6:
                    change = True
                    new_path = path[:(i + 1)] + [path[j1]] + path[i1:]
                    if new_path.index(path[j0]) == len(new_path) - 1:
                        new_path.pop(0)
                    else:
                        new_path.pop(new_path.index(path[j0]) + 1)

                    path = new_path

                    assert len(set(path)) == size # make sure all the cities are included in new path
                    count += 1
                if change:
                    continue
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
                    new_path = path[:(i + 1)] + [path[connect_i], path[connect_i1]] + path[i1:]
                    if new_path.index(path[j0]) == len(new_path) - 1:
                        new_path.pop(0)
                    else:
                        new_path.pop(new_path.index(path[j0]) + 1)
                    new_path.pop(new_path.index(path[j3]) - 1)

                    assert len(set(new_path)) == size # make sure all the cities are included in new path
                    path = new_path
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
    unvisited_cities = set(range(0, N))
    unvisited_cities.remove(current_city)
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
    solution1, to = opt_1(len(solution0), solution0)
    solution2, total = opt_2(len(solution1), solution1)
    solution3, total1 = opt_1(len(solution2), solution2)
    solution4, total2 = opt_2(len(solution3), solution3)
    solution5, total1 = opt_1(len(solution4), solution4)
    print_sum(solution5)


