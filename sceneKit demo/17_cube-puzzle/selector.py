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
import manual

class SelectorStage:
  def __init__(self):
    self.selector_views = setup.setup_selector_views()
    self.animation = setup.setup_show_drawer_animation()
    self.animation.repeatCount = 1
    self.animation.animationDidStop = self.next_selector_animation
    self.animation_player = scn.AnimationPlayer(self.animation)

    self.selector_views[0].scene.background.addAnimationPlayer(self.animation_player, 'highlight')
    self.animation_player.play()
      
    self.animation_index = 0
    
    data.hud_layer.back_button.hidden = True
    data.hud_layer.restart_button.hidden = True
    data.hud_layer.set_title('Cube puzzles')
    
  def next_selector_animation(self, animation, receiver, completed):
    if completed:
      self.selector_views[self.animation_index].scene.background.removeAllAnimations()
      self.animation_index += 1
      if self.animation_index == len(self.selector_views):
        self.animation_index = 0
      self.selector_views[self.animation_index].scene.background.addAnimationPlayer(self.animation_player, 'highlight')
    
  def scene_views(self):
    return self.selector_views
    
  def tap(self, location):
    for index, aView in enumerate(self.selector_views):
      aFrame = aView.frame
      if aFrame[0] < location.x < aFrame[0] + aFrame[2] and aFrame[1] < location.y < aFrame[1] + aFrame[3]:
        data.hud_layer.back_button.hidden = False
        data.hud_layer.restart_button.hidden = False
        main.MainViewController.next_stage(manual.ManualStage(Puzzle_variant(index)))
    
  def hint(self):
    data.hud_layer.show_generic_help()
    
  def layout(self):
    _, _, w, h = data.main_view.frame
    rows = int(math.sqrt(len(self.selector_views)))
    columns = (len(self.selector_views)-1)//rows + 1
    missing = rows*columns - len(self.selector_views)
    if not data.horizontal:
      rows, columns = columns, rows
    width = int(w / (columns + 0.8 + 0.3*(columns-1)))
    height = int(h / (rows + 0.8 + 0.3*(rows-1)))
    for i in range(len(self.selector_views)):
      row = i // columns
      column = i % columns
      if row != rows - 1:
        self.selector_views[i].frame = (int(0.4*width + 1.3*column*width), int(0.4*height + 1.3*row*height), width, height)
      else:
        self.selector_views[i].frame = (int(0.4*width + missing/2*1.3*width + 1.3*column*width), int(0.4*height + 1.3*row*height), width, height)
      camera_node = self.selector_views[i].scene.rootNode.childNodeWithName('selector_camera')
      camera_node.position = (0., 7., 11.) if width/height > 0.8 else (0., 9.5, 14.5)

    
if __name__ == '__main__':
  main.MainViewController.run()
