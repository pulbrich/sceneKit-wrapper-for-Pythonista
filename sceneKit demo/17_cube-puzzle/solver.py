'''Cube puzzles - five typical 3x3x3 3D puzzles.

(c) Peter Ulbrich, 2019

a demo script for the sceneKit wrapper package for Pythonista

See the README.md for details.

'''

import math
import pickle

try:
  from pyrr import Vector3, Quaternion
except ImportError:
  Vector3 = Quaternion = None

from data import *

class Piece:
  def __init__(self, name, shapes):
    self.name = name
    self.puzzle_shape = None
    self.shapes = shapes

class Solver:
  def __init__(self, puzzle_variant):
    self.puzzle_cubes = sum(len(nodes) for nodes in data.reference_pieces[puzzle_variant.value].values())
    
    try:
      with open('resources/'+puzzle_variant.name+'-shapes.P', 'rb') as fp:
        self.shapes_dict = pickle.load(fp)
        for name, nodes in data.reference_pieces[puzzle_variant.value].items():
          if len(list(self.shapes_dict[name].keys())[0]) != len(nodes):
            raise pickle.UnpicklingError        
    except (FileNotFoundError, pickle.UnpicklingError, KeyError):
      if Vector3 is None:
        raise ImportError('Module Pyrr is needed to recreate the shapes.P file. Ether re-download the shapes.P file or run "pip install pyrr".')
      self.shapes_dict = {}
      for name, nodes in data.reference_pieces[puzzle_variant.value].items():
        self.shapes_dict[name] = self.generate_shapes(nodes)
      with open('resources/'+puzzle_variant.name+'-shapes.P', 'wb') as fp:
        pickle.dump(self.shapes_dict, fp)
      
    self.pieces = [Piece(name, self.shapes_dict[name]) for name in data.reference_pieces[puzzle_variant.value].keys()]
    
    try:
      with open('resources/'+puzzle_variant.name+'-solution.P', 'rb') as fs:
        self.empty_solutions = pickle.load(fs)
        if self.empty_solutions:
          if len(data.reference_pieces[puzzle_variant.value][self.empty_solutions[0][0][0][0]]) != len(self.empty_solutions[0][0][0][1]):
            raise pickle.UnpicklingError
    except (FileNotFoundError, pickle.UnpicklingError, KeyError):
      self.generate_solutions()
      self.empty_solutions = self.path
      with open('resources/'+puzzle_variant.name+'-solution.P', 'wb') as fs:
        pickle.dump(self.empty_solutions, fs)
    self.path = []
    self.solution = []
        
  def solve_it(self, input):
    for aPiece in self.pieces:
      aPiece.puzzle_shape = None
      aPiece.shapes = self.shapes_dict[aPiece.name]

    for aPiece_name in input:
      aPiece = [_ for _ in self.pieces if _.name == aPiece_name][0]
      shape = input[aPiece_name]
      aPiece.puzzle_shape = frozenset([Cube(int(round(aNode.x)), int(round(aNode.y)), int(round(aNode.z))) for aNode in shape])
      aPiece.shapes = {aPiece.puzzle_shape:self.shapes_dict[aPiece.name][aPiece.puzzle_shape]}
      
    self.solution = []
    for aPath in self.empty_solutions:
      aSolution = []
      valid_path = True
      distance = 0
      for aStep in aPath:
        next_step_items = []
        for aPiece_name, aShape in aStep:
          aPiece = [_ for _ in self.pieces if _.name == aPiece_name][0]
          if aPiece_name in input and aShape != aPiece.puzzle_shape:
            valid_path = False
            break
          if aPiece_name not in input:
            next_step_items.append((aPiece_name, aPiece.shapes[aShape]))
          elif distance < len(input):
            pass
          else:
            valid_path = False
            break
        else:
          distance += len(aStep)
        if not valid_path:
          break
        elif next_step_items:
          aSolution.append(next_step_items)
      if aSolution and valid_path:
        self.solution.append(aSolution)

    return self.solution
    
  def generate_solutions(self):
    for aPiece in self.pieces:
      aPiece.puzzle_shape = None
      aPiece.shapes = self.shapes_dict[aPiece.name]
    self.path = []
    self.solve(set(), len(self.pieces) - 1)
    
  def solve(self, cubes_used, piece_ind):
    if piece_ind < 0:
      if len(cubes_used) != self.puzzle_cubes:
        return
      else:
        new_path = []
        solver_pieces = self.pieces[:]
        while solver_pieces:
          next_removals = []
          for aPiece in solver_pieces:
            larger_shape = set()
            for aNode in aPiece.puzzle_shape:
              larger_shape.add(Cube(aNode.x, aNode.y + 1, aNode.z))
              larger_shape.add(Cube(aNode.x, aNode.y + 2, aNode.z))
        
            remainder_cubes = set()
            for aRemainder_piece in (_ for _ in solver_pieces if _ != aPiece):
              remainder_cubes.update(aRemainder_piece.puzzle_shape)
        
            if remainder_cubes.isdisjoint(larger_shape):
              next_removals.append(aPiece)
          
          if next_removals:
            path_entry = []
            for aPiece in next_removals:
              path_entry.append((aPiece.name, aPiece.puzzle_shape))
              solver_pieces.remove(aPiece)
            new_path.append(path_entry)
            
          else:
            new_path = []
            break
      
        if not solver_pieces:
          new_path.reverse()
          self.path.append(new_path)
        return        
        
    for next_shape in self.pieces[piece_ind].shapes:
      if cubes_used.isdisjoint(next_shape):
        self.pieces[piece_ind].puzzle_shape = next_shape
        solved = self.solve(cubes_used | next_shape, piece_ind - 1)
        self.pieces[piece_ind].puzzle_shape = None
            
    return
    
  def generate_shapes(self, nodes):
    nodes = [Vector3(aNode) for aNode in nodes]
    theta = math.pi / 2
    quaternions = {}
    for i in range(4):
      quaternions[(i, 0, 0)] = Quaternion.from_x_rotation(i * theta)
      quaternions[(0, i, 0)] = Quaternion.from_y_rotation(i * theta)
      quaternions[(0, 0, i)] = Quaternion.from_z_rotation(i * theta)
    shapes = {}
    for x_rot in (3, 2, 1, 0):
      new_rotation = quaternions[(x_rot, 0, 0)]
      rotated_nodes_x = self.shape_constrained([new_rotation * aNode for aNode in nodes], zero_align=True)
      for y_rot in (3, 2, 1, 0):
        new_rotation = quaternions[(0, y_rot, 0)]
        rotated_nodes_y = self.shape_constrained([new_rotation * aNode for aNode in rotated_nodes_x], zero_align=True)
        for z_rot in (3, 2, 1, 0):
          new_rotation = quaternions[(0, 0, z_rot)]
          rotated_nodes = self.shape_constrained([new_rotation * aNode for aNode in rotated_nodes_y], zero_align=True)
          for x_shift in (2, 1, 0):
            for y_shift in (2, 1, 0):
              for z_shift in (-2, -1, 0):
                new_shift = Vector3([float(x_shift), float(y_shift), float(z_shift)])
                shifted_nodes = [new_shift + aNode for aNode in rotated_nodes]
                shape = self.shape_constrained(shifted_nodes)
                shape = frozenset([Cube(int(round(aNode.x)), int(round(aNode.y)), int(round(aNode.z))) for aNode in shape])
                shapes[shape] = (x_rot, y_rot, z_rot, x_shift, y_shift, z_shift)
    return shapes
              
  def shape_constrained(self, shape_nodes, zero_align=False):
    min_box = Vector3([100., 100., 100.])
    max_box = Vector3([-100., -100., -100.])
    for aNode in shape_nodes:
      min_box.x = round(min(min_box.x, aNode.x))
      min_box.y = round(min(min_box.y, aNode.y))
      min_box.z = round(min(min_box.z, aNode.z))
      max_box.x = round(max(max_box.x, aNode.x))
      max_box.y = round(max(max_box.y, aNode.y))
      max_box.z = round(max(max_box.z, aNode.z))
    
    offset = Vector3()
    if not zero_align:
      if min_box.x < 0: offset.x = float(min_box.x)
      elif max_box.x > 2: offset.x = float(max_box.x - 2.)
      if min_box.y < -6: offset.y = float(min_box.y + 6.)
      elif max_box.y > -4: offset.y = float(max_box.y + 4.)
      if min_box.z < -2: offset.z = float(min_box.z + 2.)
      elif max_box.z > 0: offset.z = float(max_box.z)
    else:
      offset.x = float(min_box.x)
      offset.y = float(min_box.y + 6.)
      offset.z = float(max_box.z)
      
    return [aNode - offset for aNode in shape_nodes]
    
if __name__ == '__main__':
  import main
  main.MainViewController.run()

