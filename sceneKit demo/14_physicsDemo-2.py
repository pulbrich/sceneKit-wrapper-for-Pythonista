"""
physics experiments Nr. 2
"""

from objc_util import *
import ctypes
import sceneKit as scn
import ui
import math
import random
from scene import *

class Counter(Scene):
  def setup(self):
    self.background_color = 'midnightblue'
    self.counter = -1
    self.counter_node = LabelNode(str(self.counter))
    self.counter_node.position = (self.size.w/2, self.size.h/2)
    self.add_child(self.counter_node)
    
  def update(self):
    self.counter_node.text = str(self.counter)

class Demo:
    
  @classmethod
  def run(cls):
    cls().main()
    
  @on_main_thread
  def main(self):
    main_view = ui.View()
    w, h = ui.get_screen_size()
    main_view.frame = (0,0,w,h)
    main_view.name = 'physics experiment demo - 2'
  
    scene_view = scn.View(main_view.frame, superView=main_view)
    scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleRightMargin
    scene_view.allowsCameraControl = True
    
    self.counter_scene = Counter()
    counter_view = SceneView()
    counter_view.frame = (0., 0., 100., 50.)
    counter_view.scene = self.counter_scene    
    main_view.add_subview(counter_view)
    
#    scene_view.debugOptions = scn.DebugOption.ShowBoundingBoxes | scn.DebugOption.ShowCameras | scn.DebugOption.ShowLightInfluences
    
#    scene_view.debugOptions = scn.DebugOption.ShowPhysicsShapes
    
    scene_view.backgroundColor = 'white'
    scene_view.scene = scn.Scene()
    
    physics_world = scene_view.scene.physicsWorld
    physics_world.contactDelegate = self
    
    root_node = scene_view.scene.rootNode
    
    box_size = 10
    box = scn.Box(box_size, box_size, box_size, 0.0)
    box.firstMaterial.diffuse.contents = (.86, .86, .86)
    box.firstMaterial.transparency = 0.15
    box.firstMaterial.cullMode = scn.CullMode.Front
    box_node = scn.Node.nodeWithGeometry(box)
    root_node.addChildNode(box_node)
    
    self.particle_number = 25
    particle_max_r = box_size/20
    particle_colors = ['black', 'blue', 'green', 'pink', 'yellow', 'red', 'cyan', 'gray', 'magenta', 'brown', 'crimson', 'gold', 'indigo', 'olive']
    particles_node = scn.Node()
    particles_node.physicsField = scn.PhysicsField.electricField()
    particles_node.physicsField.strength = 5.0

    root_node.addChildNode(particles_node)
    for i in range(self.particle_number):
      r = random.uniform(0.35*particle_max_r, particle_max_r)
      particle = scn.Sphere(r)
      particle.firstMaterial.diffuse.contents = random.choice(particle_colors)
      particle.firstMaterial.specular.contents = (.86, .94, 1.0, 0.8)
      particle_node = scn.Node.nodeWithGeometry(particle)
      particle_node.position = (random.uniform(-(box_size/2-particle_max_r)*0.95, (box_size/2-particle_max_r)*0.95), random.uniform(-(box_size/2-particle_max_r)*0.95, (box_size/2-particle_max_r)*0.95), random.uniform(-(box_size/2-particle_max_r)*0.95, (box_size/2-particle_max_r)*0.95))
      particle_node.physicsBody = scn.PhysicsBody.dynamicBody()
      particle_node.physicsBody.mass = 1.2*r
      particle_node.physicsBody.charge = random.uniform(-10*r, +0*r)
      particle_node.physicsBody.restitution = 1.0
      particle_node.physicsBody.damping = 0.0
      particle_node.physicsBody.angularDamping = 0.0
      particle_node.physicsBody.continuousCollisionDetectionThreshold = 1*r
      particle_node.physicsBody.affectedByGravity = False
      particle_node.physicsBody.contactTestBitMask = scn.PhysicsCollisionCategory.Default.value
      particle_node.physicsBody.velocity = (random.uniform(-box_size, box_size), random.uniform(-box_size, box_size), random.uniform(-box_size, box_size))
      particles_node.addChildNode(particle_node)
    
    box_nodes = scn.Node()
    d = box_size/2
    for pos in [(d,0,0), (-d,0,0), (0,d,0), (0,-d,0), (0,0,d), (0,0,-d)]:
      aNode = scn.Node()
      aNode.position = pos
      aNode.lookAt((0,0,0))
      aNode.physicsBody = scn.PhysicsBody.staticBody()
      aNode.physicsBody.physicsShape = scn.PhysicsShape.shapeWithGeometry(scn.Plane(box_size, box_size))
      box_nodes.addChildNode(aNode)
    root_node.addChildNode(box_nodes)
    
    constraint = scn.LookAtConstraint.lookAtConstraintWithTarget(root_node)
    constraint.gimbalLockEnabled = True
    
    camera_node = scn.Node()
    camera_node.camera = scn.Camera()
    camera_node.position = (-2.5*box_size, 1.5*box_size, 2*box_size)
    camera_node.constraints = constraint
    root_node.addChildNode(camera_node)
    
    light_node = scn.Node()
    light_node.position = (box_size, box_size, box_size)
    light = scn.Light()
    light.type = scn.LightTypeDirectional
    light.castsShadow = True
    light.shadowSampleCount = 32
    light.color = (.95, 1.0, .98)
    light_node.light = light
    light_node.constraints = constraint
    root_node.addChildNode(light_node)
    
    main_view.present(style='fullscreen', hide_title_bar=False)
    
  def didEndContact(self, aWorld, aContact):
    big, small = (aContact.nodeA, aContact.nodeB) if aContact.nodeA.physicsBody.mass > aContact.nodeB.physicsBody.mass else (aContact.nodeB, aContact.nodeA)
    m1, m2 = big.physicsBody.mass, small.physicsBody.mass
    v1, v2 = big.physicsBody.velocity, small.physicsBody.velocity
    m = m1 + m2
    big.physicsBody.mass = m
    big.physicsBody.charge += small.physicsBody.charge
    big.geometry.radius += 0.4*math.log1p(small.geometry.radius)
    big.physicsBody.physicsShape = scn.PhysicsShape.shapeWithGeometry(big.geometry)
    big.physicsBody.continuousCollisionDetectionThreshold = 1*big.geometry.radius
    big.physicsBody.velocity = ((m1*v1.x+m2*v2.x)/(m), (m1*v1.y+m2*v2.y)/(m), (m1*v1.z+m2*v2.z)/(m))
    small.removeFromParentNode()
    self.particle_number -= 1
    self.counter_scene.counter = self.particle_number

Demo.run()
