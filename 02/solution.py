example = [1,9,10,3, 2,3,11,0, 99, 30,40,50]
task_1 = [1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,10,19,23,1,23,9,27,1,5,27,31,2,31,13,35,1,35,5,39,1,39,5,43,2,13,43,47,2,47,10,51,1,51,6,55,2,55,9,59,1,59,5,63,1,63,13,67,2,67,6,71,1,71,5,75,1,75,5,79,1,79,9,83,1,10,83,87,1,87,10,91,1,91,9,95,1,10,95,99,1,10,99,103,2,103,10,107,1,107,9,111,2,6,111,115,1,5,115,119,2,119,13,123,1,6,123,127,2,9,127,131,1,131,5,135,1,135,13,139,1,139,10,143,1,2,143,147,1,147,10,0,99,2,0,14,0]


def calculate_sequance(s):
  idx = 0
  while True:
    op_code = s[idx]
    if op_code in [1, 2]:
      a, b = (s[s[idx+1]], s[s[idx+2]]) 
      s[s[idx+3]] = a + b if op_code is 1 else a * b
      idx = idx + 4
    else:
      if op_code is not 99:
        print(f"Unsupported op code {op_code}")
      break
  return s


task_2 = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,10,19,23,1,23,9,27,1,5,27,31,2,31,13,35,1,35,5,39,1,39,5,43,2,13,43,47,2,47,10,51,1,51,6,55,2,55,9,59,1,59,5,63,1,63,13,67,2,67,6,71,1,71,5,75,1,75,5,79,1,79,9,83,1,10,83,87,1,87,10,91,1,91,9,95,1,10,95,99,1,10,99,103,2,103,10,107,1,107,9,111,2,6,111,115,1,5,115,119,2,119,13,123,1,6,123,127,2,9,127,131,1,131,5,135,1,135,13,139,1,139,10,143,1,2,143,147,1,147,10,0,99,2,0,14,0]
def find_arguments(s=task_2, value=19690720):
  for x1 in range(100):
    for x2 in range(100):
        P = s[:]
        P[1] = x1
        P[2] = x2
        result = calculate_sequance(P)
        if P[0] == value:
          return (x1,x2)


if __name__ == "__main__":
    print(f"Answer on part 1: {calculate_sequance(task_1)[0]}")
    x1, x2 = find_arguments()
    print(f"Verb and noun are {x1} {x2}. What is 100 * noun + verb is {100*x1+x2}")
