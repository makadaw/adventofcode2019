my = """<x=-5, y=6, z=-11>
<x=-8, y=-4, z=-2>
<x=1, y=16, z=4>
<x=11, y=11, z=-4>"""

e1 = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

e2 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""

def parse(str):
  return [list(map(int, [i.strip()[2:] for i in x[1:-1].split(",")])) for x in str.split("\n")]


def compare(a, b):
    if a == b: return 0
    return -1 if a > b else 1


def system_energy(m, steps=10):  
  num = len(m)
  velocity = [[0, 0, 0] for x in range(num)]
  for i in range(steps):
    for p1 in range(num):
      for p2 in range(num):
        if p1 != p2:
          velocity[p1][0] += compare(m[p1][0], m[p2][0])
          velocity[p1][1] += compare(m[p1][1], m[p2][1])
          velocity[p1][2] += compare(m[p1][2], m[p2][2])
    # Apply velocity
    for k, v in enumerate(velocity):
      m[k][0] += v[0]
      m[k][1] += v[1]
      m[k][2] += v[2]
  total = sum(sum(abs(x) for x in m[i]) * sum(abs(x) for x in velocity[i]) for i in range(num))
  return total


def find_repeated_position(m):  
  num = len(m)
  velocity = [[0, 0, 0] for x in range(num)]
  positions = set()
  i = 0
  all_zero = True
  while True:
    state = "|".join([",".join(str(x)) for x in m])
    if state in positions:
      break
    positions.add(state)
    for p1 in range(num):
      for p2 in range(num):
        if p1 != p2:
          velocity[p1][0] += compare(m[p1][0], m[p2][0])
          velocity[p1][1] += compare(m[p1][1], m[p2][1])
          velocity[p1][2] += compare(m[p1][2], m[p2][2])
    # Apply velocity
    for k, v in enumerate(velocity):
      m[k][0] += v[0]
      m[k][1] += v[1]
      m[k][2] += v[2]
    print("Step", i)
    i+=1
  return i


if __name__ == "__main__":
  m = parse(e2)
  # print(f"System total energy on 1000 step {system_energy(m, steps=1000)}")
  print(find_repeated_position(m))
