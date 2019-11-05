"""
using the ship.scn file from XCode
"""

from objc_util import *
import ctypes
import sceneKit as scn
import ui
import math


class Demo:
  def __init__(self):
    self.name = 'ship!'
    pass
    
  @classmethod
  def run(cls):
    cls().main()
    
  @on_main_thread
  def main(self):
    main_view = ui.View()
    w, h = ui.get_screen_size()
    main_view.frame = (0,0,w,h)
    main_view.name = 'ship demo'
  
    scene_view = scn.View(main_view.frame, superView=main_view)
    scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleWidth
    scene_view.allowsCameraControl = True
    
    scene_view.scene = scn.Scene.sceneWithURL(url='ship.scn')
    
    root_node = scene_view.scene.rootNode
    
    ship_node = root_node.childNodes[0]
    ship_mesh = ship_node.childNodes[0]
    ship_emitter = ship_mesh.childNodes[0]
    ship_emitter_light = ship_emitter.light
    ship_camera = ship_mesh.camera
    scrap_meshShape = ship_mesh.geometry
    lambert1 = scrap_meshShape.materials[0]

    camera_node = scn.Node()
    camera_node.camera = scn.Camera()
    camera_node.position = (0,0,5)
    root_node.addChildNode(camera_node)    

    # Add a constraint to the camera to keep it pointing to the target geometry
    constraint = scn.LookAtConstraint.lookAtConstraintWithTarget(root_node)
    constraint.gimbalLockEnabled = True
    camera_node.constraints = constraint
    
    light_node = scn.Node()
    light_node.position = (100, 50, 100)
    light = scn.Light()
    light.type = scn.LightTypeDirectional
    light.castsShadow = True
    light.color = 'white'
    light_node.light = light
    light_node.constraints = constraint
    root_node.addChildNode(light_node)
    
    ambient_light = scn.Light() 
    ambient_light.type = scn.LightTypeAmbient
    ambient_light.name = 'ambient light'
    ambient_light.color = (.99, 1.0, .86)
    ambient_light.intensity = 100
    ambient_node = scn.Node()
    ambient_node.light = ambient_light
    root_node.addChildNode(ambient_node)
  
    main_view.present(style='fullscreen', hide_title_bar=False)

Demo.run()
