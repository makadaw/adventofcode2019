import math
import sys

def fuel(mass):
  """ Take its mass, divide by three, round down, and subtract 2 """
  return max(math.floor(mass/3)-2, 0)

def total_fuel(mass):
  """ Calculate total fuel required by a ship including it own mass and mass of fuel """
  total = 0
  additinal = fuel(mass)
  while additinal > 0:
    total = total + additinal
    additinal = fuel(additinal)
  return total

def total_fule_for_modules(file, fuel):
  total = 0
  with open(file, "r") as f:
    per_module = [fuel(int(x[:-1])) for x in f if x != "\n"]
    for module in per_module:
      total = total + module
  return total

if __name__ == "__main__":
  file = sys.argv[1]
  task_1 = total_fule_for_modules(file, fuel)
  print(f"First task answer is {task_1}")
  task_2 = total_fule_for_modules(file, total_fuel)
  print(f"Second task answer is {task_2}")
