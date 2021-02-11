def slurp(file):
  import os
  result = ""
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file), "r") as f:
    result = f.read()
  return result.strip()
my = slurp("input")

if __name__ == "__main__":
  m = {(x,y): v for y, l in enumerate(my.split("\n")) for x, v in enumerate(l)}
  print(m)