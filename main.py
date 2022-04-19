from train_schedule import TrainScheduleProblem,Schedule

ts = TrainScheduleProblem()
s = Schedule(ts)

s.check_time_table()
s.check_collision()