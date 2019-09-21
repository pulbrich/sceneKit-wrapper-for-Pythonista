"""
avoid occluder demo
"""

from objc_util import *
import sceneKit as scn
import ui
import math
  
def dot(v1, v2):
  return sum(x*y for x,y in zip(list(v1),list(v2)))
  
def det2(v1, v2):
  return v1[0]*v2[1] - v1[1]*v2[0]

class Demo:
    
  @classmethod
  def run(cls):
    cls().main()
    
  @on_main_thread
  def main(self):
    main_view = ui.View()
    w, h = ui.get_screen_size()
    main_view.frame = (0,0,w,h)
    main_view.name = 'avoid occluder demo'
  
    scene_view = scn.View(main_view.frame, superView=main_view)
    scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleWidth
    scene_view.allowsCameraControl = True
    scene_view.delegate = self
    scene_view.backgroundColor = 'white'
    scene_view.rendersContinuously = True
    scene_view.scene = scn.Scene()
    
    root_node = scene_view.scene.rootNode

    floor_geometry = scn.Floor()
    floor_node = scn.Node.nodeWithGeometry(floor_geometry)
    root_node.addChildNode(floor_node)

    ball_radius = 0.2
    ball_geometry = scn.Sphere(radius=ball_radius)
    ball_geometry.firstMaterial.diffuse.contents = (.48, .48, .48)
    ball_geometry.firstMaterial.specular.contents = (.88, .88, .88)
    self.ball_node_1 = scn.Node.nodeWithGeometry(ball_geometry)
    self.ball_node_2 = scn.Node.nodeWithGeometry(ball_geometry)
   
    root_node.addChildNode(self.ball_node_1)
    root_node.addChildNode(self.ball_node_2)
    
    occluder_geometry = scn.Box(0.3, 2., 15., 0.2)
    occluder_geometry.firstMaterial.diffuse.contents = (.91, .91, .91)
    occluder_node = scn.Node.nodeWithGeometry(occluder_geometry)
    occluder_node.position = (0., 0.8, 0.)
    root_node.addChildNode(occluder_node)
    
    self.orbit_r = 10
    self.omega_speed_1 = math.pi/1500
    self.omega_speed_2 = 1.5*self.omega_speed_1
    self.ball_node_1.position = (self.orbit_r, 0.5, 0.)
    self.ball_node_2.position = (0., 0.5, self.orbit_r)
    
    constraint = scn.AvoidOccluderConstraint.avoidOccluderConstraintWithTarget(self.ball_node_1)
    self.ball_node_2.constraints = [constraint]

    camera_node = scn.Node()
    camera_node.camera = scn.Camera()
    camera_node.position = (0.5*self.orbit_r , 0.5*self.orbit_r, 1.5*self.orbit_r)
    camera_node.lookAt(root_node.position)
    root_node.addChildNode(camera_node)
    
    light_node = scn.Node()
    light_node.position = (self.orbit_r, self.orbit_r, self.orbit_r)
    light = scn.Light()
    light.type = scn.LightTypeDirectional
    light.castsShadow = True
    light.shadowSampleCount = 32
    light.color = (.99, 1.0, .86)
    light_node.light = light
    light_node.lookAt(root_node.position)
    root_node.addChildNode(light_node)
    
    main_view.present(hide_title_bar=False)
    
  def update(self, view, atTime):
    pos_1 = self.ball_node_1.presentationNode.position
    pos_2 = self.ball_node_2.presentationNode.position
    self.omega_1 = -math.atan2(det2((pos_1.x, pos_1.z), (1., 0.)), dot((pos_1.x, pos_1.z), (1., 0.)))
    self.omega_2 = -math.atan2(det2((pos_2.x, pos_2.z), (1., 0.)), dot((pos_2.x, pos_2.z), (1., 0.)))
    self.omega_1 += self.omega_speed_1
    self.omega_2 += self.omega_speed_2
    self.ball_node_1.position = (self.orbit_r*math.cos(self.omega_1), 0.5, self.orbit_r*math.sin(self.omega_1))
    self.ball_node_2.position = (self.orbit_r*math.cos(self.omega_2), 0.5, self.orbit_r*math.sin(self.omega_2))

Demo.run()
