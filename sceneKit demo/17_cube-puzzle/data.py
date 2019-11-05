'''Cube puzzles - five typical 3x3x3 3D puzzles.

(c) Peter Ulbrich, 2019

a demo script for the sceneKit wrapper package for Pythonista

See the README.md for details.

'''

from collections import namedtuple
from enum import Enum
import ui

@ui.in_background
def print_in_background(*text):
  print(*text)

Cube = namedtuple('Cube', 'x y z')

class Puzzle_variant(Enum):
  Half_Hour = 0
  Soma_Cube = 1
  Diabolical_Cube = 2
  Mikusinskis_Cube = 3
  Five_Piece = 4

class Data:
  __slots__ = ('main_view', 'horizontal', 'gestures_instance', 'hud_layer', 'active_stage', 'reference_pieces')
  
  def __init__(self):
    self.reference_pieces = self.create_reference_pieces()
    self.active_stage = None
    
  def create_reference_pieces(self):
    piece_definitions = [
      [
      [((2., 0., 0.), (1., 1., 0.), (1., 1., -1.)), '1'],
      [((2., 0., 0.), (2., 0., -1.)), '2'],
      [((2., 0., 0.), (0., 0., -1.), (1., 1., 0.)), '3'],
      [((1., 1., 0.), (2., 1., 0.), (1., 0., -1.)), '4'],
      [((2., 0., 0.), (1., 0., -1.)), '5'],
      [((0., 0., -1.), (0., 1., -1.)), '6']
      ], [
      [((0., 0., -1.), (0., 1., -1.)), '1'],
      [((0., 1., 0.), (0., 0., -1.)), '2'],
      [((1., 1., 0.), (0., 0., -1.)), '3'],
      [((2., 0., 0.), (2., 0., -1.)), '4'],
      [((2., 0., 0.), (1., 0., -1.)), '5'],
      [((1., 0., -1.),), '6'],
      [((1., 0., -1.), (2., 0., -1.)), '7']
      ], [
      [tuple(), '1'],
      [((0., 0., -1.), (1., 0., -1.)), '2'],
      [((2., 0., 0.,), (0., 0., -1.), (1., 0., -1.), (0., 0., -2.)), '3'],
      [((0., 0., -1),), '4'],
      [((2., 0., 0.), (0., 0., -1.), (2., 0., -1.)), '5'],
      [((2., 0., 0.), (0., 0., -1.), (1., 0., -1.), (2., 0., -1.), (0., 0., -2.)), '6']
      ], [
      [((2., 0., 0.), (0., 0., -1.)), '1'],
      [((2., 0., 0.), (0., 0., -1.), (0., 1., -1.)), '2'],
      [((0., 0., -1.), (0., 1., -1.)), '3'],
      [((1., 0., -1.), (1., 1., -1.)), '4'],
      [((2., 0., 0.), (2., 1., 0.), (1., 0., -1.)), '5'],
      [((1., 0., -1.), (1., 1., -1.), (2., 1., -1.)), '6']
      ], [
      [((1., 0., -1.), (2., 0., 0.), (2., 1., 0.)), '1'],
      [((2., 0., 0.), (2., 1., 0.), (2., 1., -1.)), '2'],
      [((2., 0., 0.), (2., 0., -1.), (1., 1., 0.)), '3'],
      [((0., 1., 0.), (2., 0., 0.), (2., 0., -1.), (2., 1., -1.)), '4'],
      [((0., 1., 0.), (2., 0., 0.), (2., 1., 0.), (2., 1., -1.)), '5']
      ]
      ]
    
    reference_pieces = []
    for aDefinition in piece_definitions:
      pieces = {}
      for aPiece in aDefinition:
        name = aPiece[1]
        nodes = [Cube(0., 0., 0.)]
        
        nodes.append(Cube(1., 0., 0.))
        
        for aCubePosition in aPiece[0]:
          nodes.append(Cube._make(aCubePosition))
          
        pieces[name] = nodes  
      reference_pieces.append(pieces)
    return reference_pieces
    
data = Data()

if __name__ == '__main__':
  import main
  main.MainViewController.run() 
