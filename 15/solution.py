import collections


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


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
LEFT = {NORTH: WEST, SOUTH: EAST, WEST: SOUTH, EAST: NORTH}
RIGHT = {NORTH: EAST, SOUTH: WEST, WEST: NORTH, EAST: SOUTH}
BACK = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}

R_WALL = 0
R_MOVED = 1
R_IS_OXY = 2

M_SPACE = "."
M_WALL = "#"
M_UNIT = "*"

  
def build_map(data):
  C = Computer(data, [])
  width = [0, 0]
  height = [0, 0]
  pos = (0, 0)
  ship = collections.defaultdict(lambda: M_WALL)

  moves = []
  unexplored = {}

  while True:
    if pos not in unexplored:
      unexplored[pos] = [NORTH,SOUTH,WEST,EAST]
    
    if unexplored[pos]:
      # We didn't check all positions
      back_tracing = False
      move = unexplored[pos].pop()
    else:
      # For this point we done
      back_tracing = True

      if not moves:
        break # Get everything
      move = BACK[moves.pop()]
    C.input.append(move)
    output = C.run()
    if output in (R_MOVED, R_IS_OXY):
      pos = next_position(pos, move)
      ship[pos] = M_SPACE if output == R_MOVED else M_UNIT
      width[0] = min(width[0], pos[0])
      width[1] = max(width[1], pos[0])
      height[0] = min(height[0], pos[1])
      height[1] = max(height[1], pos[1])

      if not back_tracing:
        moves.append(move)
  return (ship, (width[0]-1, width[1]+1), (height[0]-1, height[1]+1))
    

def next_position(fromp, direction):
  if direction == NORTH:
    return (fromp[0], fromp[1]+1)
  elif direction == EAST:
    return (fromp[0]+1, fromp[1])
  elif direction == SOUTH:
    return (fromp[0], fromp[1]-1)
  elif direction == WEST:
    return (fromp[0]-1, fromp[1])


def draw_map(ship, width, height):
  for y in range(height[1], height[0]-1, -1):
    row = []
    for x in range(width[0], width[1]+1):
      if x == 0 and y == 0:
        row.append("0")
      else:
        row.append(str(ship[(x, y)]))
    print("".join(row))



class Solver:
  def __init__(self, ship_map, start, finish):
    self.ship_map = ship_map[0]
    self.start = start
    self.finish = finish


  def getAdjacentSpaces(self, space, visited):
    spaces = list()
    spaces.append((space[0]-1, space[1]))  # NORTH
    spaces.append((space[0]+1, space[1]))  # SOUTH
    spaces.append((space[0], space[1]-1))  # WEST
    spaces.append((space[0], space[1]+1))  # EAST

    final = list()
    for i in spaces:
        if self.ship_map[i] != M_WALL and i not in visited:
            final.append(i)
    return final


  def bfs(self):
    self.basic_operations = 0
    queue = [self.start]
    visited = set()

    while len(queue) != 0:
      if queue[0] == self.start:
        path = [queue.pop(0)]
      else:
        path = queue.pop()
      front = path[-1]
      if front == self.finish:
          return path
      elif front not in visited:
          for adjacentSpace in self.getAdjacentSpaces(front, visited):
              newPath = list(path)
              newPath.append(adjacentSpace)
              queue.append(newPath)
              # global basic_operations
              self.basic_operations += 1
          visited.add(front)
    return None


  def find(self):
    return self.bfs()


def fill_all_empty_space(ship_map):
  filled = ship_map[0]
  total = sum([1 for k, v in ship_map[0].items() if v == M_SPACE])
  tick = 0
  while True:
    already = [k for k, v in filled.items() if v == M_UNIT]
    for p in already:
      check = [
        (p[0], p[1]+1),
        (p[0], p[1]-1),
        (p[0]+1, p[1]),
        (p[0]-1, p[1])
      ]
      for c in check:
        if filled[c] == M_SPACE:
          filled[c] = M_UNIT
    tick += 1
    if len(already) == total:
      # We are done
      break
  draw_map(filled, ship_map[1], ship_map[2])
  return tick

if __name__ == "__main__":
  data = map(int, my.split(","))

  ship_map = build_map(data)
  draw_map(ship_map[0], ship_map[1], ship_map[2])
  unit = list(filter(lambda x: x[1] == M_UNIT, ship_map[0].items()))[0][0]
  path = Solver(ship_map, (0, 0), unit).find()
  print(f"Shortst route is {len(path)-1} steps")
  minutes = fill_all_empty_space(ship_map)
  print(f"It will take {minutes} minutes to fill")
  