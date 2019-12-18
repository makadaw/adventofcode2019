import math


def slurp(file):
  import os
  result = ""
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file), "r") as f:
    result = f.read()
  return result.strip()
my = slurp("input")

e1 = "12345678"
e2 = "80871224585914546619083218645595"
e3 = "03036732577212944063491565474664"


def process(data, ticks=100):
  base = [0, 1, 0, -1]
  output = data[:]
  output_len = len(output)
  ticks_bases = {}
  for tick in range(ticks):
    tmp = []
    for i in range(output_len):
      if i not in ticks_bases:
        tick_base = [val for val in base for _ in range(i+1)] # Build base pattern
        pattern = [tick_base[i%len(tick_base)] for i in range(1, output_len+1)] # Build pattern for a row
        ticks_bases[i] = pattern
      pattern = ticks_bases[i]
      tmp.append(abs(sum([x[0] * x[1] for x in zip(output, pattern)]))%10)
      print(f"Calculate tick {tick} row {i}")
    output = tmp
  return output


if __name__ == "__main__":  
  data = [int(x) for x in my]
  
  # output = process(data)
  # first8 = "".join(map(str, output[:8]))
  # print(f"First 8 numbers after 100 ticks {first8}")

  offset = int("".join(map(str, data[:7])))
  repeated = data[:]
  data_length = len(repeated) * 10000
  necessary_length = data_length - offset
  num_copies = math.ceil(necessary_length / len(repeated))
  repeated = repeated * num_copies
  repeated = repeated[-necessary_length:]

  def calculate(data, num_phases=100):
    for i in range(0, num_phases):
        sum = 0
        for j in range(len(data) - 1, -1, -1):
            sum += data[j]
            data[j] = sum % 10
    return data

  output = calculate(repeated)
  print("".join(map(str, output[:8])))
