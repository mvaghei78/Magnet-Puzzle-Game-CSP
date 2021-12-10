from pathlib import Path
import numpy as np

class MapReader:
    def __init__(self, filepath):
        self.filepath = filepath

    def read_map(self):
        path = Path(self.filepath)
        if not path.is_file():
            print(f'The file {self.filepath} does not exist')
        else:
            reader = open(self.filepath, "r")
            self.pairs = []
            try:
                line_index = 1
                for line in reader.readlines():
                    line = line.rstrip("\n")
                    if line_index == 1:
                        self.NumberOfRows = int(line.split(" ")[0])
                        self.NumberOfColumns = int(line.split(" ")[1])
                    elif line_index == 2:
                        self.PositivePoleEachRow = [int(x) for x in line.split(" ") if x != ""]
                    elif line_index == 3:
                        self.NegativePoleEachRow = [int(x) for x in line.split(" ") if x != ""]
                    elif line_index == 4:
                        self.PositivePoleEachColumn = [int(x) for x in line.split(" ") if x != ""]
                    elif line_index == 5:
                        self.NegativePoleEachColumn = [int(x) for x in line.split(" ") if x != ""]
                    else:
                        self.pairs.append([int(x) for x in line.split(" ") if x != ""])
                    line_index += 1
            finally:
                # print(self.NumberOfRows, self.NumberOfColumns)
                # print(self.PositivePoleEachRow)
                # print(self.NegativePoleEachRow)
                # print(self.PositivePoleEachColumn)
                # print(self.NegativePoleEachColumn)
                # print(self.pairs)
                reader.close()
        self.PositivePoleEachRow = np.array(self.PositivePoleEachRow)
        self.NegativePoleEachRow = np.array(self.NegativePoleEachRow)
        self.PositivePoleEachColumn = np.array(self.PositivePoleEachColumn)
        self.NegativePoleEachColumn = np.array(self.NegativePoleEachColumn)
        self.pairs = np.array(self.pairs)

        return self.NumberOfRows, self.NumberOfColumns, self.PositivePoleEachRow, \
               self.NegativePoleEachRow, self.PositivePoleEachColumn, self.NegativePoleEachColumn, \
               self.pairs


if __name__ == "__main__":
    MapReader("D:/Dars/term9/AI/project/PROJECT3/Magnet-Puzzle-Game-CSP/InputFiles/input1_method2.txt").read_map()
