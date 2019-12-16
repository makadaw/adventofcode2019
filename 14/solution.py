import collections
import math


def slurp(file):
  import os
  result = ""
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file), "r") as f:
    result = f.read()
  return result.strip()
my = slurp("input")

e1 = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""


e2 = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""

e3 = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""


def parse_recieps(data):
  recieps = {"ORE": (1, [])}
  for l in data.split("\n"):
    ingridients, result = tuple(l.split("=>"))
    ingridients = [x.strip().split() for x in ingridients.split(",")]
    ingridients = [(int(x[0]), x[1]) for x in ingridients]

    result = result.strip().split()    
    if result[1] in recieps:
      raise Exception("Already exist in the list")
    recieps[result[1]] = (int(result[0]), ingridients)
  return recieps


def number_of_ore(recieps, amount = 1):
  to_create = [(amount*x[0], x[1]) for x in recieps["FUEL"][1]]
  balance = collections.defaultdict(lambda: 0)
  need_to_use = collections.defaultdict(lambda: 0)
  while len(to_create) > 0:
    ingridient = to_create[0]
    produce = recieps[ingridient[1]][0]
    ingridients = recieps[ingridient[1]][1]
    # print("Need", ingridient, "produce", produce, "from", ingridients)
    netto = ingridient[0]-balance[ingridient[1]]
    # We really need it
    if netto > 0:
      mult = math.ceil(netto/produce)
      balance[ingridient[1]] += mult*produce - ingridient[0] # But what is left to the balance
      need_to_use[ingridient[1]] += ingridient[0]
      # Add ingredients to the list multiplied
      to_create.extend([(x[0]*mult, x[1]) for x in ingridients])
    else:
      # We can reuse existed
      balance[ingridient[1]] -= ingridient[0]
    to_create = to_create[1:]
  return need_to_use["ORE"]


if __name__ == "__main__":
  data = my

  recieps = parse_recieps(data)
  print(f"For 1 FUEL we need {number_of_ore(recieps)} of ORE")
  
  ore =   1000000000000
  f = 0
  t = ore # If we have 1:1 ratio
  while t-f > 1:
    cur = math.floor(f+(t-f)/2)
    required = number_of_ore(recieps, cur)
    if required > ore:
      t = cur
    else:
      f = cur
  print(f"For {f} {number_of_ore(recieps, f)}")
  print(f"For {t} {number_of_ore(recieps, t)}")
  print(f"Posible amount from {ore} ore is {cur} use {required}")

  
    