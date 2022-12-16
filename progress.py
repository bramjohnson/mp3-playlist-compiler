import math
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

class ProgressBar:
    def __init__(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r") -> None:
        self.iteration = int(iteration)
        self.total = int(total)
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.printEnd = printEnd

        self.increment(iteration)

    def increment(self, amount):
        self.iteration += int(amount)
        self.iteration = min(self.iteration, self.total)
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (self.iteration / float(self.total)))
        filledLength = int(math.ceil(self.length * (self.iteration / self.total)))
        # print("Length:", self.length, "Iteration:", self.iteration, "Total:", self.total, "FilledLength:", filledLength)
        dash_number = max(0, min(self.length, self.length - filledLength)) # Ensure no wonky
        bar = self.fill * filledLength + '-' * dash_number
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end = self.printEnd)
    
    def finish(self):
        # Print New Line on Complete
        filledLength = int(math.ceil(self.length * (self.iteration / self.total)))
        bar = self.fill * filledLength
        print(f'\r{self.prefix} |{bar}| {100}% {self.suffix}', end = self.printEnd)
        print()