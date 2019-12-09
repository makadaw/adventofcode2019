my = "3,8,1001,8,10,8,105,1,0,0,21,42,55,64,85,98,179,260,341,422,99999,3,9,101,2,9,9,102,5,9,9,1001,9,2,9,1002,9,5,9,4,9,99,3,9,1001,9,5,9,1002,9,4,9,4,9,99,3,9,101,3,9,9,4,9,99,3,9,1002,9,4,9,101,3,9,9,102,5,9,9,101,4,9,9,4,9,99,3,9,1002,9,3,9,1001,9,3,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99"


def process(commands, input):
  mem = [int(x) for x in commands.split(",")]
  i = 0
  output=None
  def arguments_position(p):
    m = (int(mem[p]%1000/100), int(mem[p]%10000/1000), int(mem[p]%100000/10000))
    return (mem[mem[p+1]] if m[0] == 0 else mem[p+1], mem[mem[p+2]] if m[1] == 0 else mem[p+2])
  while i < len(mem) and mem[i] != 99:
    op = mem[i]%100
    d = 2
    if op in [1,2]:
      a, b = arguments_position(i)
      mem[mem[i+3]] = a + b if op == 1 else a * b
      d = 4
    elif op == 3:
      print(input)
      mem[mem[i+1]] = input.pop() if len(input) > 0 else 0
    elif op == 4:
      output = mem[mem[i+1]]
    elif op in [5,6]:
      d = 3
      a, b = arguments_position(i)
      if (op == 5 and a != 0) or (op == 6 and a == 0):
        i = b
        d = 0
    elif op == 7:
      a, b = arguments_position(i)
      mem[mem[i+3]] = int(a < b)
      d = 4
    elif op == 8:
      a, b = arguments_position(i)
      mem[mem[i+3]] = int(a == b)
      d = 4
    elif op == 99:
      print("stop!!!")
    i = i + d
  return (mem, output)


def run_amplifiers(input, signal):
  output = 0
  for i in range(5):
    o = process(input, [output, signal[i]])
    output = o[1]
  return output


def find_max(input):
  signals = [[a, b, c, d, e] if len(set([a,b,c,d,e])) == 5 else None \
    for a in range(5) for b in range(5) for c in range(5) for d in range(5) for e in range(5)]
  signals = filter(lambda x: x is not None, signals)
  results = [ run_amplifiers(input, signal) for signal in signals]
  return max(results)


def run_amplifiers_in_feedbacks(input, signal):
  output = 0
  i = 0
  while True:
    o = process(input, [output, signal[i%5]])
    output = o[1]
    print(f"Output {output}")
    i = i + 1
  return output


def loop_max(input):
  signals = [[a, b, c, d, e] \
    for a in range(5, 10) for b in range(5, 10) \
    for c in range(5, 10) for d in range(5, 10) for e in range(5, 10) \
    if len(set([a,b,c,d,e])) == 5]
  return run_amplifiers_in_feedbacks(input, signals[0])

  
e1 = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
e2 = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
e3 = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"

if __name__ == "__main__":
  # print(f"Max signal is {find_max(my)}")
  print(f"Feedback loop signal is {loop_max(e3)}")