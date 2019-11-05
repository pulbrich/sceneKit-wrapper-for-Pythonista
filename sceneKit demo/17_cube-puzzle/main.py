'''Cube puzzles - five typical 3x3x3 3D puzzles.

(c) Peter Ulbrich, 2019

a demo script for the sceneKit wrapper package for Pythonista

See the README.md for details.

'''

import sceneKit as scn
import ui
import Gestures

from data import *
from hud import *
import manual
import selector
import setup

class MainViewController:
    
  class MainView(ui.View):
    def will_close(self):
      data.gestures_instance.remove_all_gestures(data.main_view)
      for aSceneView in data.active_stage.scene_views():
        aSceneView.scene.paused = True
        aSceneView.removeFromSuperview()
      for aView in data.main_view.subviews:
        data.main_view.remove_subview(aView)
    
    def layout(self):
      _, _, w, h = data.main_view.frame
      data.horizontal = w > h
      data.hud_layer.layout()
      data.active_stage.layout()
      
    
  @classmethod
  def run(cls):
    scn.clearCache()
    cls().main()
  
  @on_main_thread
  def main(self):
    data.main_view = self.MainView()
    w, h = ui.get_window_size()
    data.main_view.frame = (0, 0, w, h)
    
    data.gestures_instance = Gestures.Gestures()
    data.gestures_instance.add_tap(data.main_view, self.simple_tap)

    data.hud_layer = Hud()
    self.next_stage(selector.SelectorStage())

    data.main_view.present(style='fullscreen', hide_title_bar=True)
   
  @classmethod 
  def next_stage(cls, stage_instance):
    if data.active_stage is not None:
      for aSceneView in data.active_stage.scene_views():
        aSceneView.scene.paused = True
        aSceneView.removeFromSuperview()
    data.active_stage = stage_instance
    data.hud_layer.bring_to_front()
    
  def simple_tap(self, tap_data):
    data.active_stage.tap(tap_data.location)
    

if __name__ == '__main__':
  MainViewController.run()
