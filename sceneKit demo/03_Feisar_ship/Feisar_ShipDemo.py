"""
using the Feisar_Ship.scn file
"""

from objc_util import *
import ctypes
import sceneKit as scn
import ui
import math


class Demo:
  def __init__(self):
    self.name = 'Feisar_Ship'
    pass
    
  @classmethod
  def run(cls):
    cls().main()
    
  @on_main_thread
  def main(self):
    main_view = ui.View()
    w, h = ui.get_screen_size()
    main_view.frame = (0,0,w,h)
    main_view.name = 'Feisar_Ship demo'
  
    scene_view = scn.View(main_view.frame, superView=main_view)
    scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleWidth
    scene_view.allowsCameraControl = True
    
    scene_view.backgroundColor = 'black'
    
    scene_view.scene = scn.Scene.sceneWithURL(url='Feisar_Ship.scn')
    
    root_node = scene_view.scene.rootNode

    feisar_node = root_node.childNodes[0]
    
    feisar_node.light = scn.nil
    root_node.light = scn.nil

    feisar_geometry = feisar_node.geometry
    geometry_sources = feisar_geometry.geometrySources
    
    feisar_material = feisar_geometry.firstMaterial
    feisar_material.emission.intensity = 0.05
    feisar_material.roughness.contents = (.79, .79, .79)
    feisar_material.metalness.contents = (.11, .11, .11)

    pulse_action = scn.Action.repeatActionForever(scn.Action.sequence([scn.Action.fadeInWithDuration(1.2), scn.Action.fadeOutWithDuration(0.5)]))
    
    blue_emitter = scn.Material()
    blue_emitter.diffuse.contents = 'black'
    blue_emitter.emission.contents = (.0, .35, 1.0)
    white_emitter = scn.Material()
    white_emitter.diffuse.contents = 'black'
    white_emitter.emission.contents = (.86, .98, 1.0)
    
    nose_geometry = scn.Sphere(radius=1.5)
    nose_geometry.firstMaterial = blue_emitter
    nose_node = scn.Node.nodeWithGeometry(nose_geometry)
    nose_node.position = (0., 4.35, 161.)
    nose_node.castsShadow = False
    nose_node.runAction(pulse_action)    
    feisar_node.addChildNode(nose_node)
    
    front_grille_p0 = scn.vector3Make((0., 10., 137.6))
    front_grille_p1 = scn.vector3Make((0., 20., 153.5))
    front_grille_ds1 = scn.vector3Make((-0.25, 0.7, -0.25))    
    grille_nr = 15
    dt = 0.8/grille_nr
    front_grille_node = scn.Node()
    feisar_node.addChildNode(front_grille_node)
    
    front_grille_geometry = scn.Cylinder(0.45, 13.7)
    front_grille_geometry.firstMaterial = white_emitter
    
    for i in range(grille_nr):
      aNode = scn.Node.nodeWithGeometry(front_grille_geometry)
      aNode.position = (0., front_grille_p0.y+(front_grille_p1.y-front_grille_p0.y)*i/grille_nr, front_grille_p0.z+(front_grille_p1.z-front_grille_p0.z)*i/grille_nr)
      aNode.scale = (1.+front_grille_ds1.x*i/grille_nr, 1.+front_grille_ds1.y*i/grille_nr, 1.+front_grille_ds1.z*i/grille_nr)
      aNode.rotation = (0., 0., 1., math.pi/2)
      grille_action = scn.Action.sequence([scn.Action.waitForDuration(i*dt), scn.Action.fadeOutWithDuration(0.7*dt), scn.Action.waitForDuration(dt), scn.Action.fadeInWithDuration(0.3*dt), scn.Action.waitForDuration((grille_nr-2-i)*dt)])
      aNode.runAction(scn.Action.repeatActionForever(scn.Action.sequence([grille_action, grille_action.reversedAction()])))
      front_grille_node.addChildNode(aNode)

    constraint = scn.LookAtConstraint.lookAtConstraintWithTarget(feisar_node)
    constraint.gimbalLockEnabled = True

    
    light_node = scn.Node()
    light_node.position = (150, 60, -20)

    light = scn.Light()
    light.type = scn.LightTypeDirectional
    light.castsShadow = True
    light.color = (.99, 1.0, .86)
    light_node.light = light
    light_node.constraints = constraint
    root_node.addChildNode(light_node)
    
    main_view.present(style='fullscreen', hide_title_bar=False)
    
Demo.run()
