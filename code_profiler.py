import datetime

RELEASE_MODE = False

def getTime():
    return datetime.datetime.now()

class CodeProfiler:
    def __init__(self):
        self.iterations_logged = 0
        self.task_durations = dict()
        self.task_starts = dict()
    def markTransitionFrom(self, taskName, toTaskName):
        if RELEASE_MODE:
            return
        time = getTime()
        dt = time - self.task_starts[taskName]
        if taskName in self.task_durations:
            self.task_durations[taskName] += dt
        else:
            self.task_durations[taskName] = dt
        self.task_starts[toTaskName] = time
    def markStartOf(self, taskName):
        if RELEASE_MODE:
            return
        time = getTime()
        self.task_starts[taskName] = time
    def markEndOf(self, taskName):
        if RELEASE_MODE:
            return
        time = getTime()
        dt = time - self.task_starts[taskName]
        if taskName in self.task_durations:
            self.task_durations[taskName] += dt
        else:
            self.task_durations[taskName] = dt
    def logTaskTimes(self, period):
        if RELEASE_MODE:
            return
        if (self.iterations_logged >= period):
            for key in self.task_durations:
                print(key, "took", self.task_durations[key])
                self.task_durations[key] = datetime.timedelta(0)
            self.iterations_logged = 0
            print()
        else:
            self.iterations_logged += 1