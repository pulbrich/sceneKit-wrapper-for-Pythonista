'''Cube puzzles - five typical 3x3x3 3D puzzles.

(c) Peter Ulbrich, 2019

a demo script for the sceneKit wrapper package for Pythonista

See the README.md for details.

'''

from enum import Enum, auto
import math
import weakref

import sceneKit as scn

from data import *
import setup

class Piece_location(Enum):
  Drawer = auto()
  Tray = auto()
  Puzzle = auto()
  Solver = auto()
  
class Piece_set:
  def __init__(self, puzzle_variant):
    self.pieces = setup.setup_pieces(self, puzzle_variant)
    self.puzzle_variant = puzzle_variant
    self.previous_piece_in_tray = []
    
  def solved(self):
    unplaced_pieces = sum(1 for aPiece in self.pieces if aPiece.location != Piece_location.Puzzle)
    return unplaced_pieces == 0
    
  def reset_pieces(self):
    for aPiece in self.pieces:
      aPiece.reset()
    
class Piece:
  def __init__(self, piece_set, name=None, handle_node=None):
    self.piece_set = weakref.ref(piece_set)()
    self.name = name
    self.drawer_handle_node = handle_node
    self.location = Piece_location.Drawer
    self.piece_handle_node = handle_node.clone()

    self.tray_handle_node = scn.Node()
    self.tray_handle_node.addChildNode(self.piece_handle_node) 
    self.drawer_view = None   
    self.tray_handle_node.opacity = 0.
    
  def __str__(self):
    return 'piece ' + self.name + ' ' + str(self.location)
    
  def reset(self):
    self.location = Piece_location.Drawer
    self.tray_handle_node.opacity = 0.
    self.drawer_handle_node.opacity = 1.0
    self.piece_handle_node.eulerAngles = (0, 0, 0)
    self.piece_handle_node.position = (0, 0, 0)
    
  def from_drawer_to_tray(self):
    self.drawer_handle_node.opacity = 0.5
    self.tray_handle_node.opacity = 1.0
    self.piece_handle_node.eulerAngles = (0, 0, 0)
    self.piece_handle_node.position = (0, 0, 0)
    self.location = Piece_location.Tray
    
  def from_tray_to_drawer(self):
    self.drawer_handle_node.opacity = 1.0
    self.tray_handle_node.opacity = 0.0
    self.location = Piece_location.Drawer
    
  def rotate(self, axis, constraint=True, zero_align=False):
    thetaOver2 = math.pi / 4
    if axis == 'x' and data.horizontal or axis == 'y' and not data.horizontal:
      new_rotation = (math.sin(thetaOver2), 0, 0, math.cos(thetaOver2))
    elif axis == 'y' and data.horizontal or axis == 'x' and not data.horizontal:
      if not data.horizontal: thetaOver2 *= -1
      new_rotation = (0, math.sin(thetaOver2), 0, math.cos(thetaOver2))
    elif axis == 'z':
      new_rotation = (0, 0, math.sin(thetaOver2), math.cos(thetaOver2))
    self.piece_handle_node.rotateBy(new_rotation, self.piece_handle_node.worldPosition)
    if constraint:
      self.constraint(zero_align)
    
  def shift(self, axis, distance):
    pos = self.piece_handle_node.position
    if axis == 'x': new_shift = scn.Vector3(distance, 0, 0)
    elif axis == 'y': new_shift = scn.Vector3(0, distance, 0)
    elif axis == 'z': new_shift = scn.Vector3(0, 0, distance)     
    self.piece_handle_node.position = (pos.x + new_shift.x, pos.y + new_shift.y, pos.z + new_shift.z)
    self.constraint()
    
  def constraint(self, zero_align=False):
    pos = self.piece_handle_node.position
    min_box, max_box = self.tray_handle_node.boundingBox
    min_box = scn.Vector3(round(min_box.x + 0.5), round(min_box.y + 0.5), round(min_box.z + 0.5))
    max_box = scn.Vector3(round(max_box.x - 0.5), round(max_box.y - 0.5), round(max_box.z - 0.5))
    new_pos = [round(pos.x), round(pos.y), round(pos.z)]
    
    if not zero_align:
      if min_box.x < 0: new_pos[0] = pos.x - min_box.x
      if max_box.x > 2: new_pos[0] = pos.x - (max_box.x - 2)
      if min_box.y < -2: new_pos[1] = pos.y - (min_box.y + 2)
      if max_box.y > 0: new_pos[1] = pos.y - (max_box.y - 0)
      if min_box.z < -2: new_pos[2] = pos.z - (min_box.z + 2)
      if max_box.z > 0: new_pos[2] = pos.z - max_box.z
    else:
      new_pos[0] = pos.x - min_box.x
      new_pos[1] = pos.y - min_box.y
      new_pos[2] = pos.z - max_box.z
      
    self.piece_handle_node.position = new_pos
    
  def drop(self):
    tray_handle = self.tray_handle_node.parentNode
    starting_positions = [self.piece_handle_node.convertPosition(aNode.position, toNode=tray_handle) for aNode in self.piece_handle_node.childNodes]

    pieces_resting_set = set()
    for aPiece in (_ for _ in self.piece_set.pieces if _.location == Piece_location.Puzzle):
      for aNode in aPiece.piece_handle_node.childNodes:
        aPos = aPiece.piece_handle_node.convertPosition(aNode.position, toNode=tray_handle)
        pieces_resting_set.add(scn.Vector3(round(aPos.x), round(aPos.y), round(aPos.z)))
        
    for downShift in range(16):
      new_positions = {scn.Vector3(round(aStartPos.x), round(aStartPos.y - downShift), round(aStartPos.z)) for aStartPos in starting_positions}          
      break_value = min(aPos.y for aPos in new_positions)
          
      if break_value < -6: break
      if not new_positions.isdisjoint(pieces_resting_set): break
                   
    downShift -= 1
    current_position = self.piece_handle_node.position
        
    self.piece_handle_node.position = scn.Vector3(current_position.x, current_position.y - downShift, current_position.z)
        
    top_value = max(aPos.y for aPos in new_positions) + 1
    if top_value <= -4:
      self.location = Piece_location.Puzzle
      self.piece_set.previous_piece_in_tray.append(self)
      return True
    else: return False
    
  def lift(self):
    pos = self.piece_handle_node.position
    self.piece_handle_node.position = (pos.x, 0, pos.z)
    self.constraint()
    self.location = Piece_location.Tray


if __name__ == '__main__':
  import main
  main.MainViewController.run()
