"""
based on:
a tetrahedron by cvp at https://forum.omz-software.com/topic/3922/for-the-fun-a-photos-cube

"""

from objc_util import *
import ctypes
import sceneKit as scn
import ui
import math


class Demo:
  def __init__(self):
    self.name = 'my name is Demo'
    pass
    
  @classmethod
  def run(cls):
    cls().main()
    
  @on_main_thread
  def main(self):
# actually you need only to preserve those properties that are needed after the main_view.present call, 
# in this case the self.morpher. All the other self. prefixes are not needed for the same functionality
    self.main_view = ui.View()
    w, h = ui.get_screen_size()
    self.main_view.frame = (0,0,w,h)
    self.main_view.name = 'Morpher demo'
  
    self.scene_view = scn.View(self.main_view.frame, superView=self.main_view)
    self.scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleRightMargin
    self.scene_view.allowsCameraControl = True
    
    self.scene_view.scene = scn.Scene()
    
    self.scene_view.delegate = self
    
    self.root_node = self.scene_view.scene.rootNode
    
    self.camera_node = scn.Node()
    self.camera_node.camera = scn.Camera()
    self.camera_node.position = (0,0,5)
    self.root_node.addChildNode(self.camera_node)    

    verts = [
    scn.Vector3(0, 1, 0),
    scn.Vector3(-0.5, 0, 0.5),
    scn.Vector3(0.5, 0, 0.5),
    scn.Vector3(0.5, 0, -0.5),
    scn.Vector3(-0.5, 0, -0.5),
    scn.Vector3(0, -1, 0)]
    
    verts_2 = [
    scn.Vector3(0, 2.5, 0),
    scn.Vector3(-0.4, 0, 0.4),
    scn.Vector3(0.4, 0, 0.4),
    scn.Vector3(0.4, 0, -0.4),
    scn.Vector3(-0.4, 0, -0.4),
    scn.Vector3(0, -1.5, 0)]

    self.source = scn.GeometrySource.geometrySourceWithVertices(verts)
    self.source_2 = scn.GeometrySource.geometrySourceWithVertices(verts_2)
 
    indexes = [
    0, 1, 2,
    2, 3, 0,
    3, 4, 0,
    4, 1, 0,
    1, 5, 2,
    2, 5, 3,
    3, 5, 4,
    4, 5, 1]

    self.elements = scn.GeometryElement.geometryElementWithData(indexes, scn.GeometryPrimitiveType.Triangles)
    
    self.geometry = scn.Geometry.geometryWithSources(self.source, self.elements)
    self.geometry_2 = scn.Geometry.geometryWithSources(self.source_2, self.elements)

    self.material = scn.Material()
    self.material.contents = scn.RGBA(1, 0.9, 0.9, 1.0)
    self.geometry.materials = self.material
    
    self.morpher = scn.Morpher()
    self.morpher.targets = [self.geometry_2]
    self.morpher.setWeightForTargetAtIndex(0.0, 0)
     
    self.geometry_node = scn.Node.nodeWithGeometry(self.geometry)
    self.geometry_node.name = 'hero'
    self.geometry_node.morpher = self.morpher
    self.root_node.addChildNode(self.geometry_node)

    # Add a constraint to the camera to keep it pointing to the target geometry
    constraint = scn.LookAtConstraint.lookAtConstraintWithTarget(self.geometry_node)
    constraint.gimbalLockEnabled = True
    self.camera_node.constraints = constraint
    
    self.light_node = scn.Node()
    self.light_node.position = (100, 0, -10)
    self.light = scn.Light()
    self.light.type = scn.LightTypeDirectional
    self.light.castsShadow = True
    self.light.color = 'white'
    self.light_node.light = self.light
    self.root_node.addChildNode(self.light_node)
    
    self.rotate_action = scn.Action.repeatActionForever(scn.Action.rotateBy(0, math.pi*2, 0, 10))
    self.geometry_node.runAction(self.rotate_action)
  
    self.main_view.present(hide_title_bar=False)

  def update(self, view, atTime):
    tick = (int(atTime*1000) % 314)/100.
    weight = math.sin(tick)
    self.morpher.setWeightForTargetAtIndex(weight, 0)
    
# also correct:    
#    hero_node = view.scene.rootNode.childNodeWithName('hero')
#    morpher = hero_node.morpher
#    morpher.setWeightForTargetAtIndex(weight, 0)



Demo.run()
