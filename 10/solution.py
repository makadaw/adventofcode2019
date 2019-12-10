def slurp(file):
  import os
  result = ""
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file), "r") as f:
    result = f.read()
  return result.strip()
my = slurp("input")

e1 = """
.#..#
.....
#####
....#
...##
"""

e2 = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
import math


def map_map(str):
  return [(x, y) for y, line in enumerate(str.strip().split("\n")) for x, c in enumerate(line)
            if c == '#']


def visiable_asteroids(points, p):
  def reducer(a, p):
    dx, dy = a[0]-p[0], a[1]-p[1]
    g = abs(math.gcd(dx, dy))
    return (dx//g, dy//g)
  return set([reducer(a, p) for a in points if a != p])


def best_point(points):
  best = max([(i, len(visiable_asteroids(points, p))) for i,p in enumerate(points)], key=lambda t: t[1])
  return (points[best[0]], best[1])


def vaporized(points, station, number=199):
  result = sorted([(math.atan2(dx, dy), (dx, dy)) for dx, dy in visiable_asteroids(points, station)], reverse=True)
  dx, dy = result[199][1]
  start = (station[0]+dx, station[1]+dy)
  while start not in points:
    start = (start[0]+dx, start[1]+dy)
  return start


if __name__ == "__main__":
  map = map_map(my)
  best = best_point(map)
  print(f"Best point at {best[0]} with {best[1]} asteroids")
  point200 = vaporized(map, best[0], 2)
  print(f"200th point {point200[0] * 100 + point200[1]}")
