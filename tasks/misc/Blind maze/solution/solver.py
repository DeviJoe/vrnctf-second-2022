#!/usr/bin/env python3
import os
from pwnlib.tubes import process
import sys

visited_nodes = set()

opposite_nodes = {'a': 'd', 'w': 's', 'd': 'a', 's': 'w'}


class MazeProcess:
  def __init__(self, arg_list):
    self.proc = process.process(arg_list, cwd=os.path.dirname(__file__))

  def sendString(self,string: str):
    self.proc.sendline(string.encode())


  def read(self, timeout=0.01):
    result = self.proc.recv(timeout=timeout).decode()
    return result

  def close(self):
    self.proc.kill()


def visit_node(i, j):
  visited_nodes.add((i, j))


def check_is_visited(i, j):
  return (i, j) in visited_nodes


def check_pos_is_valid(proc: MazeProcess, direction: str):
  ret = 0
  proc.sendString(direction)

  recv_line = proc.read()

  if "vrnctf" in recv_line:
    ret = 2

  elif "Going" in recv_line:
    ret = 1

    proc.sendString(opposite_nodes[direction])
    proc.read()

  return ret, recv_line


def solve(proc: MazeProcess, direction: str = ""):
  solved = False

  for char in ['w', 'a', 's', 'd']:
    if char == opposite_nodes.get(direction, 0):
      continue

    ret, resp = check_pos_is_valid(proc, char)

    if ret == 1:
      proc.sendString(char)
      print(f">> { proc.read() }")

      solved = solve(proc, char)

      if not solved:
        proc.sendString(opposite_nodes[char])
        print(f"<< { proc.read() }")
      else:
        break

    if ret == 2:
      solved = True
      print(resp)
      break

  return solved


if __name__ == "__main__":
  proc = MazeProcess(["./maze", "-vvvv"])
  sys.setrecursionlimit(150000)


  print(proc.read())

  solve(proc)

  proc.close()