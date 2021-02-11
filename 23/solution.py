from queue import Queue
from threading import Thread


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
        print("cmp input", self.input, i)
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


class Node:
  def __init__(self, data, address, network):
    self.cmp = Computer(data[:], [address]) # Set address as first command
    self.cmp.input_action = lambda: -1 # Default command
    self.address = address
    self.network = network


  def receive(self, package):
    if package is not None: # add package to queue
      print(f"Add message {package}")
      self.cmp.input.insert(0, package[0])
      self.cmp.input.insert(0, package[1])
    dest = self.cmp.run()
    print("get dest for", self.address, dest)
    if dest is not None:
      new_package = (self.cmp.run(), self.cmp.run())
      self.network.send(self.address, dest, new_package)
    else:
      print("none")


class Network:
  def __init__(self):
    self.queue = Queue()
    self._network = {}
  

  def add_node(self, data, address):
    node = Node(data, address, self)
    self._network[address] = node

  
  def start(self):
    for i in range(50): # Start all nodes
      self._network[i].receive(None)
    


  def send(self, frm, to, package):
    print(f"Send {package} from {frm} to {to}")
    # self._network[to].receive(package)


if __name__ == "__main__":
  data = list(map(int, my.split(",")))

  network = Network()
  for i in range(50):
    network.add_node(data, i)
  network.start()
  
