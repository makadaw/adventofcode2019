import collections
import math


def slurp(file):
  import os
  result = ""
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file), "r") as f:
    result = f.read()
  return result.strip()
my = slurp("input")


class Computer:
  def __init__(self, program, init_input, init_ip=0 ):
    self.mem = dict(enumerate(program))
    self.input = init_input
    self.output = None # output
    self.index = init_ip # ip
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
          self.index -= 2; 
          return # No inputs?
        self.write(self.address(ip+1,(oop//100)%10), self.input.pop())
      elif op==5: # jmpt
        if v != 0: 
          self.index = w
      elif op==6: # jmpf
        if v == 0: 
          self.index = w
      else: 
        raise Exception(f"wrong opcode {op}, original {oop} at index {ip}")
    self.halted = True


TRANSITIONS = {
  # 0 left, 1 right
  (0, 1): [(-1, 0), (1,0)], # From UP
  (1, 0): [(0, 1), (0, -1)], # From RIGHT
  (0, -1): [(1, 0), (-1, 0)], # From DOWN
  (-1, 0): [(0, -1), (0, 1)] # From LEFT
}


def number_of_painted_panels(parsed):
  grid = collections.defaultdict(lambda: 0)
  point = (0,0)
  direction = (0, 1)
  painted = []
  cmp = Computer(parsed, [])
  while True:
    cmp.input = [grid[point]]
    color = cmp.run()
    if cmp.halted:
      break
    if color != grid[point]:
      painted.append(point)
    grid[point] = color
    move = cmp.run()
    # Rotate robot
    direction = TRANSITIONS[direction][move]
    point = (point[0] + direction[0], point[1] + direction[1])
  return len(set(painted))


def print_id(parsed):
  grid = collections.defaultdict(lambda: 0)
  point = (0,0)
  grid[point] = 1
  direction = (0, 1)
  sides = (0, 0)
  cmp = Computer(parsed, [])
  while True:
    cmp.input = [grid[point]]
    color = cmp.run()
    if cmp.halted:
      break
    grid[point] = color
    move = cmp.run()
    # Rotate robot
    direction = TRANSITIONS[direction][move]
    point = (point[0] + direction[0], point[1] + direction[1])
    sides = (max(sides[0], abs(point[0])), max(sides[1], abs(point[1])))
  for y in range(sides[1], -sides[1]-1, -1):
    layer = []
    for x in range(-sides[0], sides[0]+1):
      layer.append(" " if grid[x, y] == 0 else "*")
    print("".join(layer))
  # return grid

if __name__ == "__main__":
  parsed = list(map(int, my.split(",")))
  print(f"Painted panels: {number_of_painted_panels(parsed)}")
  print_id(parsed)