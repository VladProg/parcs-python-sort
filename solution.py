from Pyro4 import expose
import heapq


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        k = len(self.workers)
        print("Workers %d" % k)

        # input
        arr = self.read_input()
        n = len(arr)

        # map
        mapped = []
        for i in xrange(0, k):
            print("map %d" % i)
            mapped.append(self.workers[i].mymap(arr[n * i // k: n * (i + 1) // k]))

        # reduce
        result = self.myreduce(mapped)

        # output
        self.write_output(result)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(arr):
        arr.sort()
        return arr

    @staticmethod
    @expose
    def myreduce(mapped):
        return list(heapq.merge(part.value for part in mapped))

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            return list(map(int, f.readlines()))

    def write_output(self, output):
        with open(self.output_file_name, 'w') as f:
            f.writelines([str(item) + '\n' for item in output])
        print("output done")
