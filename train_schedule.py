import numpy as np


# Train Schedule
class TrainScheduleProblem:
    _n: int = 0
    "number of trains"
    _m: int = 0
    "number of stretches"
    stretches = []
    "stretches sequence for each train"
    crossing_time = []
    "crossing time of stretches sequence for each train"
    start_time = []
    "start time for each train"
    safety_time = []
    "minimum safety departure time distance for each train pair"
    _cross_time = {}
    "_cross_time[(t,s)] = crossing time of train 't' on stretch 's'"

    def __init__(self, filepath: str = 'instance_1.txt'):
        """

        :param filepath: instance file path
        """
        f = open(filepath, 'r')
        n = self._n = int(f.readline())
        self._m = int(f.readline())
        self.start_time = [int(a) for a in f.readline().split()]
        for i in range(n):
            self.stretches.append([int(a) for a in f.readline().split()])
            self.crossing_time.append([int(a) for a in f.readline().split()])
            self.safety_time.append([int(a) for a in f.readline().split()])

        for i in range(n):
            for j in range(len(self.stretches[i])):
                self._cross_time[(i, self.stretches[i][j])] = self.crossing_time[i][j]
        pass

    @property
    def n(self):
        return self._n

    @property
    def m(self):
        return self._m

    def cross_time(self, train: int, route: int) -> int:
        return self._cross_time.setdefault((train, route), 0)


class Schedule:
    dep_time = []

    def __init__(self, ts: TrainScheduleProblem):
        self.ts = ts
        for i in range(ts.n):
            self.dep_time.append(np.zeros(len(ts.stretches[i]), dtype=int))
            self.dep_time[i][0] = ts.start_time[i]
            for j in range(1, len(self.dep_time[i])):
                self.dep_time[i][j] = self.dep_time[i][j - 1] + ts.cross_time(i, ts.stretches[i][j - 1])

    def check_collision(self):
        ts = self.ts
        for i in range(1, ts.n):
            r_i = ts.stretches[i]
            dep_i = self.dep_time[i]
            for j in range(i):
                r_j = ts.stretches[j]
                dep_j = self.dep_time[j]
                for a in range(len(r_i)):
                    for b in range(len(r_j)):
                        if r_i[a] == r_j[b]:
                            if np.abs(dep_i[a] - dep_j[b]) < ts.safety_time[i][j]:
                                return False
                        elif r_i[a] == -r_j[b]:
                            if dep_i[a] < dep_j[b]:
                                if dep_i[a] + ts.cross_time(i, r_i[a]) >= dep_j[b]:
                                    return False
                            elif dep_j[b] + ts.cross_time(j, r_j[b]) >= dep_i[a]:
                                return False
        return True

    def check_time_table(self):
        ts = self.ts
        for t in range(ts.n):
            dep = self.dep_time[t]
            clock = ts.start_time[t]
            for i, r in enumerate(ts.stretches[t]):
                if clock < dep[i]:
                    return False
                clock = dep[i] + ts.cross_time(t, r)
        return True
