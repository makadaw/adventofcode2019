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


def print_number_of_blocks(data):
  cp = Computer(data, [])
  field = {}
  while True:
    point = (cp.run(), cp.run())
    action = cp.run()
    if cp.halted:
      break
    field[point] = action
  print(f"Block tiles: {sum(1 for k in field if field[k] == 2)}")


def print_field(field):
  width = height = 0
  for x, y in field:
    if x is not None:
      width = max(width, x)
      height = max(height, y)    
  for y in range(height):
    line = [str(field[(x, y)]) if field[(x, y)] != 0 else " " for x in range(width)]
    print("".join(line))


def win_the_game(data):
  field = {}
  def automatic_input():
    ball = [k for k in field if field[k] == 4][0]
    paddle = [k for k in field if field[k] == 3][0]
    if ball[0] == paddle[0]: return 0
    return -1 if ball[0] < paddle[0] else 1
  cp = Computer(data, [], input_action=automatic_input)
  while True:
    point = (cp.run(), cp.run())
    action = cp.run()
    if cp.halted:
      break
    field[point] = action
    if point[0] == -1:
      print_field(field)
  print(f"Score {field[(-1, 0)]}")


if __name__ == "__main__":
  data = list(map(int, my.split(",")))
  print_number_of_blocks(data)
  data[0] = 2
  win_the_game(data)
