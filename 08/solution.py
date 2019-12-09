def slurp(file):
  import os
  result = ""
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file), "r") as f:
    result = f.read()
  return result.strip()


def checksum(data, cols, rows):
  layer_len = cols*rows
  layers = [data[i*layer_len:(i+1)*layer_len] for i in range(0, int(len(data)/layer_len))]
  zeros = [l.count("0") for l in layers]
  layer = layers[zeros.index(min(zeros))]
  result = layer.count("1") * layer.count("2")
  return result


def decode(data, cols, rows):
  from functools import reduce
  TRANSPERENT = "2"
  layer_len = cols*rows
  layers = [data[i*layer_len:(i+1)*layer_len] for i in range(0, int(len(data)/layer_len))]
  layers.insert(0, "".join([str(s) for s in [TRANSPERENT] * layer_len]))
  def accum(a, l):
    result = a[:]
    for i in range(len(a)):
      result = result[:i] + (a[i] if a[i] != TRANSPERENT else l[i]) + result[i + 1:]
    return result
  return reduce(accum, layers)


def print_image(layer, cols, rows):
  print("\n".join([layer[i*cols:(i+1)*cols].replace("0", " ") for i in range(0, rows)]))


e1 = ("123456789012", 3, 2)
e2 = ("0222112222120000", 2, 2)
my = (slurp("./input"), 25, 6)


if __name__ == "__main__":
  f = my
  print(f"Checksum question {checksum(f[0], f[1], f[2])}")
  print("Decoded image:")
  print_image(decode(f[0], f[1], f[2]), f[1], f[2])