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


e0 = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
e1 = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
e2 = "1102,34915192,34915192,7,4,7,99,0"
e3 = "104,1125899906842624,99"


if __name__ == "__main__":
  print(Computer(list(map(int, my.split(","))),[1]).run())
  print(Computer(list(map(int, my.split(","))),[2]).run())