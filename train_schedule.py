import numpy as np


# Train Schedule
class TrainScheduleProblem:
    _n = 0
    _m = 0
    _route_train = []
    _cross_time_train = []
    _start_time_train = []
    _safety_time_train = []
    _cross_time = {}

    def __init__(self, filepath='instance_1.txt'):
        f = open(filepath, 'r')
        n = self._n = int(f.readline())
        self._m = int(f.readline())
        self._start_time_train = [int(a) for a in f.readline().split()]
        for i in range(n):
            self._route_train.append([int(a) for a in f.readline().split()])
            self._cross_time_train.append([int(a) for a in f.readline().split()])
            self._safety_time_train.append([int(a) for a in f.readline().split()])

        for i in range(n):
            for j in range(len(self._route_train[i])):
                self._cross_time[(i, self._route_train[i][j])] = self._cross_time_train[i][j]
        pass

    @property
    def n(self):
        return self._n

    @property
    def m(self):
        return self._m

    def routes(self, train):
        return self._route_train[train]

    def start_time(self, train):
        return self._start_time_train[train]

    def cross_time(self, train, route):
        return self._cross_time.setdefault((train, route), 0)

    def safety_time(self, t_i, t_j):
        return self._safety_time_train[t_i][t_j]


class Schedule:
    _departure_time_train = []

    def __init__(self, ts: TrainScheduleProblem):
        self._ts = ts
        for i in range(ts.n):
            self._departure_time_train.append(np.zeros(len(ts.routes(i)), dtype=int))
            self._departure_time_train[i][0] = ts.start_time(i)
            for j in range(1, len(self._departure_time_train[i])):
                self._departure_time_train[i][j] = self._departure_time_train[i][j - 1] + ts.cross_time(i,
                                                                                                        ts.routes(i)[
                                                                                                            j - 1])

    def check_collision(self):
        ts = self._ts
        for i in range(1, ts.n):
            r_i = ts.routes(i)
            dep_i = self._departure_time_train[i]
            for j in range(i):
                r_j = ts.routes(j)
                dep_j = self._departure_time_train[j]
                for a in range(len(r_i)):
                    for b in range(len(r_j)):
                        if r_i[a] == r_j[b]:
                            if np.abs(dep_i[a] - dep_j[b]) < ts.safety_time(i, j):
                                return False
                        elif r_i[a] == -r_j[b]:
                            if dep_i[a] < dep_j[b]:
                                if dep_i[a] + ts.cross_time(i, r_i[a]) >= dep_j[b]:
                                    return False
                            elif dep_j[b] + ts.cross_time(j, r_j[b]) >= dep_i[a]:
                                return False
        return True

    def check_time_table(self):
        ts = self._ts
        for t in range(ts.n):
            dep = self._departure_time_train[t]
            clock = ts.start_time(t)
            for i, r in enumerate(ts.routes(t)):
                if clock < dep[i]:
                    return False
                clock = dep[i] + ts.cross_time(t, r)
        return True
