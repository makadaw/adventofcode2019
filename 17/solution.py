from itertools import cycle


def slurp(file):
  import os
  result = ""
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file), "r") as f:
    result = f.read()
  return result.strip()
my = slurp("input")


class Computer:
  def __init__(self, program, init_input, init_ip=0, input_action=None ):
    self.mem = dict(enumerate(program))
    self.input = init_input
    self.output = None # output
    self.index = init_ip # ip
    self.input_action = input_action
    self.base = 0 # base for mode 2 addressing

  def write(self, addr, value):
    self.mem[addr] = value

  def read(self, addr): 
    return self.mem[addr] if addr in self.mem else 0

  def address(self, addr, mode): # get address for 3rd operand
    if mode==1:   return addr
    elif mode==2: return self.base + self.read(addr)
    else:         return self.read(addr)

  def value(self, addr, mode): 
    return self.read(self.address(addr, mode))

  def run(self):
    self.halted = False
    while self.read(self.index)%100 != 99: # run till halt
      ip = self.index; 
      oop = self.read(ip); 
      op = oop%100
      self.index += (0,4,4,2,2,3,3,4,4,2)[op] # default increments for operations
      if op in (1,2,4,5,6,7,8,9): v = self.value(ip+1,(oop//100)%10)
      if op in (1,2,  5,6,7,8):   w = self.value(ip+2,(oop//1000)%10)
      if op in (1,2,7,8):    dest = self.address(ip+3,(oop//10000)%10)
      if op == 1:
        self.write( dest, v + w ) # add
      elif op == 2: 
        self.write( dest, v * w )# mul
      elif op == 7: 
        self.write( dest, int(v < w) ) # setl
      elif op == 8: 
        self.write( dest, int(v ==w) ) # sete
      elif op == 9: 
        self.base += v # rebase
      elif op == 4: 
        self.output = v
        return v # O: yielded output
      elif op==3: # in
        if len(self.input) == 0:
          if self.input_action is None:
            raise Exception("Please provide input function input_action")
          i = self.input_action()
        else:
          i = self.input.pop()
        self.write(self.address(ip+1,(oop//100)%10), i)
      elif op==5: # jmpt
        if v != 0: 
          self.index = w
      elif op==6: # jmpf
        if v == 0: 
          self.index = w
      else: 
        raise Exception(f"wrong opcode {op}, original {oop} at index {ip}")
    self.halted = True


def surround(p):
  return [tuple(map(sum, zip(x[0], x[1]))) for x in zip(cycle([p]), [(0,1), (0,-1), (1,0), (-1,0)])]


def sum_of_alignments(frame):
  total = 0
  for k, v in frame.items():
    if v == "#":
      check = surround(k)
      if sum(1 if frame[x] == "#" else 0 for x in check if x in frame) == 4:
        total += k[0]*k[1]
  return total


def print_frame(frame):
  for y in range(43):
    row = []
    for x in range(40):
      p = (x, y)
      if p in frame:
        row.append(frame[p])
    print("".join(row))


def build_frame(cmp):
  frame = {}
  cursor = (0, 0)
  while True:
    output = cmp.run()
    if cmp.halted:
      break
    if output == 10:
      cursor = (0, cursor[1]+1)
    else:
      frame[cursor] = {35: "#", 46: ".", 94: "?"}[output]
      cursor = (cursor[0]+1, cursor[1])
  return frame


def next_point(p, direction):
  add = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}[direction]
  return tuple(map(sum, zip(p, add)))


def build_path(frame):
  curr = [p for p, v in frame.items() if v == "?"][0]
  # vectorized path
  direction = "^"
  movements = []
  while True:
    # [tuple(map(sum, zip(x[0], x[1]))) for x in zip(cycle([p]), [(0,1), (0,-1), (1,0), (-1,0)])]
    if direction in ("^", "v"):
      rotate = [">", "<"]
    else:
      rotate = ["^", "v"]
    check = [next_point(curr, x) for x in rotate]
    if check[0] in frame and frame[check[0]] == "#":
      new_direction = rotate[0]
    elif check[1] in frame and frame[check[1]] == "#":
      new_direction = rotate[1]
    else:
      break
    # Move forward
    rotate_to = "R" if direction+new_direction in ("^>", ">v", "v<", "<^") else "L"
    direction = new_direction
    move = 0
    forward = curr
    while True:
      forward = next_point(forward, direction)
      if forward in frame and frame[forward] == "#":
        move += 1
        curr = forward
      else:
        break
    movements.extend([rotate_to, move])
  return movements


def count_subseq(seq, sub):
    m, n = len(seq), len(sub)
    limit = m-n
    i = 0
    count = 0
    while True:
      if i > limit:
        break
      if seq[i] == sub[0]:
        if sum(1 if seq[i+s] == sub[s] else 0 for s in range(n)) == n:
          i += n-1
          count += 1
      i += 1
    return count


if __name__ == "__main__":
  data = list(map(int, my.split(",")))
  
  cmp = Computer(data, [])
  frame = build_frame(cmp)
  print_frame(frame)
  print("Sum of alignments", sum_of_alignments(frame))
  
  movements = build_path(frame)
  # some manual work :(
  move_input = list(map(ord, """A,B,A,B,A,C,B,C,A,C
R,4,L,10,L,10
L,8,R,12,R,10,R,4
L,8,L,8,R,10,R,4
n
"""))
  
  # Run program
  data[0] = 2
  move_input.reverse()
  C = Computer(data, move_input)
  last = 0
  while True:
    a = C.run()
    if a is None:
      break
    last = a
  print(f"Collected {last}")
