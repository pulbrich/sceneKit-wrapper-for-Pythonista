'''Cube puzzles - five typical 3x3x3 3D puzzles.

(c) Peter Ulbrich, 2019

a demo script for the sceneKit wrapper package for Pythonista

See the README.md for details.

'''

import math

import sceneKit as scn

from data import *
import main
import setup
from piece import *
import solver

class ManualStage:
  def __init__(self, puzzle_variant):
    self.piece_set = Piece_set(puzzle_variant)
    self.center_view = setup.setup_center_view(self.piece_set)
    setup.setup_drawer_views(self.piece_set)
    self.solver = solver.Solver(puzzle_variant)

    self.show_drawer_animation = setup.setup_show_drawer_animation()
    
    self.solved_tray_piece = None
    self.tray_piece_transforms = []
    self.tray_piece_transforms_index = -1
    
    data.hud_layer.set_title(str(puzzle_variant.name).replace('_', ' '))
    
  def restart(self):
    scn.Transaction.begin()
    scn.Transaction.animationDuration = 1.
    self.piece_set.reset_pieces()
    self.piece_set.previous_piece_in_tray = []
    scn.Transaction.commit()
    self.reset_show_next_tray_position()
    
  def scene_views(self):
    return [self.center_view] + [aPiece.drawer_view for aPiece in self.piece_set.pieces]
    
  def tap(self, location):
    for aPiece in self.piece_set.pieces:
      drawer_frame = aPiece.drawer_view.frame
      if drawer_frame[0] < location.x < drawer_frame[0] + drawer_frame[2] and drawer_frame[1] < location.y < drawer_frame[1] + drawer_frame[3]:
        self.drawer_tapped(aPiece)
        return
    if self.center_view.frame[0] < location.x < self.center_view.frame[0] + self.center_view.frame[2] and self.center_view.frame[1] < location.y < self.center_view.frame[1] + self.center_view.frame[3]:
      self.center_view_tapped(location)
      return
        
  def center_view_tapped(self, location):
    x = location.x - self.center_view.frame[0]
    y = location.y - self.center_view.frame[1]
    hit_list = self.center_view.hitTest((x, y), {scn.HitTestOptionSearchMode:scn.HitTestSearchMode.Closest, scn.HitTestOptionCategoryBitMask:2})
    if not hit_list: return
    
    hit_name = hit_list[0].node.name
    tray_piece = next((aCandidate for aCandidate in self.piece_set.pieces if aCandidate.location == Piece_location.Tray), None)
    scn.Transaction.begin()
    scn.Transaction.animationDuration = 1.
    try:
      if hit_name[0] == 'r':
        tray_piece.rotate(hit_name[1])
      elif hit_name[0] == 's':
        shift = 1 if hit_name[2] == '1' else -1
        tray_piece.shift(hit_name[1], shift)
    except (IndexError, AttributeError): pass
    scn.Transaction.commit()
    
    if hit_name == 'box':
      scn.Transaction.begin()
      scn.Transaction.animationDuration = 1.5
      if tray_piece is not None:
        tray_piece.drop()
#        if len([_ for _ in self.piece_set.pieces if _.location != Piece_location.Puzzle]) == 0:
        if self.piece_set.solved():
          self.show_finished()
      else:
        try:
          tray_piece = self.piece_set.previous_piece_in_tray.pop()
          tray_piece.lift()
          tray_piece.constraint()
        except IndexError: pass        
      scn.Transaction.commit()
    self.reset_show_next_tray_position()
    
  def drawer_tapped(self, aPiece):
    self.reset_show_next_tray_position()
    scn.Transaction.begin()
    scn.Transaction.animationDuration = 0.3
    onTray = next((aCandidate for aCandidate in self.piece_set.pieces if aCandidate.location == Piece_location.Tray), None)
    if onTray is not None:
      onTray.from_tray_to_drawer()
    if aPiece.location == Piece_location.Drawer and aPiece != onTray:
      aPiece.from_drawer_to_tray()             
    scn.Transaction.commit()
    
  def hint(self):
    if self.piece_set.solved():
      self.show_finished()
      return
      
    tray_pieces = [aPiece for aPiece in self.piece_set.pieces if aPiece.location == Piece_location.Tray]
    if tray_pieces and tray_pieces[0] == self.solved_tray_piece:
      self.show_next_tray_position()
      return
    
    solver_input = {}
    for aPiece in self.piece_set.pieces:
      if aPiece.location == Piece_location.Puzzle:
        tray_handle = aPiece.tray_handle_node.parentNode
        positions = []
        for aNode in aPiece.piece_handle_node.childNodes:
          aPos = aPiece.piece_handle_node.convertPosition(aNode.position, toNode=tray_handle)
          positions.append(aPos)
          
        solver_input[aPiece.name] = tuple(positions)

    solution = self.solver.solve_it(solver_input)
      
    if not solution:
      self.show_dead_end()
      return
      
    candidate_names = set()
    for aSolution in solution:
      for anOption in aSolution[0]:
        candidate_names.add(anOption[0])
            
    candidate_pieces = [aPiece for aPiece in self.piece_set.pieces if aPiece.name in candidate_names]

    
    if not tray_pieces or tray_pieces[0] not in candidate_pieces:
      self.show_candidates(candidate_pieces)
      return
      
    if tray_pieces and tray_pieces[0] in candidate_pieces:
      tray_piece = tray_pieces[0]
      tray_piece_transforms = set()
      for aSolution in self.solver.solution:
        for aStepItem in aSolution[0]:
          if aStepItem[0] == tray_piece.name:
            tray_piece_transforms.add(aStepItem[1])
      self.setup_show_next_tray_position(tray_piece, list(tray_piece_transforms))
      self.show_next_tray_position()
      return

      
  def show_dead_end(self):
    message_symbol = '🤷🏻‍♀️'
    data.hud_layer.show_alert(message_symbol)
    
  def show_finished(self):
    message_symbol = '👍'
    data.hud_layer.show_alert(message_symbol)


  def show_candidates(self, candidate_pieces):
    for aPiece in candidate_pieces:
      aPiece.drawer_view.scene.background.removeAllAnimations()
      aPiece.drawer_view.scene.background.addAnimation(self.show_drawer_animation)
      
  def setup_show_next_tray_position(self, tray_piece, tray_piece_transforms):
    self.solved_tray_piece = tray_piece
    self.tray_piece_transforms = tray_piece_transforms
    self.tray_piece_transforms_index = -1
    data.hud_layer.set_status('')
    
  def reset_show_next_tray_position(self):
    self.solved_tray_piece = None
    self.tray_piece_transforms = []
    self.tray_piece_transforms_index = -1
    data.hud_layer.set_status('')
    
  def show_next_tray_position(self):
    self.tray_piece_transforms_index += 1
    if self.tray_piece_transforms_index == len(self.tray_piece_transforms):
      self.tray_piece_transforms_index = 0
    
    tray_piece = self.solved_tray_piece
    transform = self.tray_piece_transforms[self.tray_piece_transforms_index]
    
    original_transform = tray_piece.piece_handle_node.transform
    
    tray_piece.from_drawer_to_tray()    
    for ind, axis in enumerate(['x', 'y', 'z']):
      for _ in range(transform[ind]):
        tray_piece.rotate(axis, constraint=False)
    tray_piece.constraint(zero_align=True)
    tray_piece.shift('x', transform[3])
    tray_piece.shift('y', transform[4])
    tray_piece.shift('z', transform[5])
    
    new_transform = tray_piece.piece_handle_node.transform    
    tray_piece.piece_handle_node.transform = original_transform
    
    scn.Transaction.begin()
    scn.Transaction.animationDuration = 1.    
    tray_piece.piece_handle_node.transform = new_transform
    scn.Transaction.commit()
    
    lead = "".join('⚫️' for i in range(self.tray_piece_transforms_index))
    tail = "".join('⚫️' for i in range(len(self.tray_piece_transforms) - self.tray_piece_transforms_index - 1))
    data.hud_layer.set_status(lead + '🔵' + tail)

  def layout(self):
    _, _, w, h = data.main_view.frame
    half = (len(self.piece_set.pieces) + 1) // 2
    odd = 2 * half - len(self.piece_set.pieces)
    side_with_gap = min(int(min(w, h) / (half+0.2)), int(min(w, h) / 3.5))
    side = int(0.8 * side_with_gap)
    gap = side_with_gap - side
    for i in range(len(self.piece_set.pieces)):
      tile = i % half
      left_side = top_side = i < half
      if data.horizontal:
        x = int(2 * gap) if left_side else w - int(2*gap) - side
        y = h - (odd * side_with_gap if not left_side else 0)//2 - (h - half*side - (half-1) * gap)//2 - side - tile*side_with_gap
      else:
        x = (odd * side_with_gap if not top_side else 0)//2 + (w - half*side - (half-1) * gap)//2 + tile*side_with_gap
        y = 20 + side//2 if top_side else h - 20 - side//2 - side
        
      self.piece_set.pieces[i].drawer_view.frame = (x, y, (side), (side))
      
    x = 2*gap + side_with_gap if data.horizontal else gap
    y = (h - half*side - (half-1)*gap)//2 + 10 if data.horizontal else 20 + side//2 + side + gap
    
    self.center_view.frame = (x, y, w - 2*x, h - 2*y) if data.horizontal else (x, y, w - 2*x, h - 2*y)
    
    box_node = self.center_view.scene.rootNode.childNodeWithName('box')
    box_node.rotation = (0, 0, 1, 0) if data.horizontal else (0, 0, 1, -math.pi/2)
    box_node.position = (1., 1., -1.) if data.horizontal else (-0.5, 3, -1)
    box_node.scale = (1., 1., 1.) if data.horizontal else (1.3, 1.3, 1.3)
    
    camera_node = self.center_view.scene.rootNode.childNodeWithName('center_camera')
    camera_node.position = (6., 8.5, 9.5) if data.horizontal else (9.2, 10., 13.)
    
if __name__ == '__main__':
  main.MainViewController.run()
