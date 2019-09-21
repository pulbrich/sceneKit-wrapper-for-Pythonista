"""
physics experiments Nr. 1
"""

from objc_util import *
import ctypes
import sceneKit as scn
import ui
import math


class Demo:
    
  @classmethod
  def run(cls):
    cls().main()
    
  @on_main_thread
  def main(self):
    main_view = ui.View()
    w, h = ui.get_screen_size()
    main_view.frame = (0,0,w,h)
    main_view.name = 'physics experiment demo - 1'
  
    scene_view = scn.View(main_view.frame, superView=main_view)
    scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleRightMargin
    scene_view.allowsCameraControl = True
    
    scene_view.backgroundColor = 'white'    
    scene_view.scene = scn.Scene()
    
    physics_world = scene_view.scene.physicsWorld
    
    root_node = scene_view.scene.rootNode

    floor_geometry = scn.Floor()
    floor_geometry.reflectivity = 0.1
    floor_node = scn.Node.nodeWithGeometry(floor_geometry)
    root_node.addChildNode(floor_node)

    ball_radius = 0.2
    ball_geometry = scn.Sphere(radius=ball_radius)
    ball_geometry.firstMaterial.diffuse.contents = (.48, .48, .48)
    ball_geometry.firstMaterial.specular.contents = (.88, .88, .88)
    ball_node = scn.Node.nodeWithGeometry(ball_geometry)
    
    rope_seg_nr = 45
    rope_length = 5.0
    rope_radius = 0.025
    rope_seg_length = rope_length/rope_seg_nr
    
    rope_element_geometry = scn.Capsule(rope_radius, rope_seg_length)
    rope_element_geometry.firstMaterial.diffuse.content = (.77, .67, .09)
    
    rope_nodes = []
    for i in range(rope_seg_nr):
      rope_nodes.append(scn.Node.nodeWithGeometry(rope_element_geometry))
      if i > 0:
        rope_nodes[-1].position = (0., -rope_seg_length, 0.)
        rope_nodes[-2].addChildNode(rope_nodes[-1])
        aConstraint = scn.DistanceConstraint.distanceConstraintWithTarget(rope_nodes[-2])
        aConstraint.maximumDistance = rope_seg_length
        aConstraint.minimumDistance = rope_seg_length
        rope_nodes[-1].constraints = aConstraint
      else:
        rope_nodes[0].position = (0, rope_length+1.0-rope_seg_length/2, 0)
        aConstraint = scn.DistanceConstraint.distanceConstraintWithTarget(root_node)
        aConstraint.maximumDistance = rope_length+1.0-rope_seg_length/2
        aConstraint.minimumDistance = rope_length+1.0-rope_seg_length/2
        rope_nodes[0].constraints = aConstraint
        
    ball_node.position = (0, -rope_seg_length/2-rope_radius-ball_radius, 0)
    aConstraint = scn.DistanceConstraint.distanceConstraintWithTarget(rope_nodes[-1])
    aConstraint.maximumDistance = rope_seg_length/2 + rope_radius + ball_radius
    aConstraint.minimumDistance = rope_seg_length/2 + rope_radius + ball_radius
    ball_node.constraints = aConstraint
    
    rope_nodes[-1].addChildNode(ball_node)
    root_node.addChildNode(rope_nodes[0])
    
    ball_physicsBody = scn.PhysicsBody.dynamicBody()
    ball_physicsBody.physicsShape = scn.PhysicsShape.shapeWithGeometry(ball_geometry)
    ball_physicsBody.mass = 5.0
    ball_physicsBody.damping = 0.005
    ball_physicsBody.angularDamping = 0.00
    ball_node.physicsBody = ball_physicsBody
    
    rope_element_physicsShape = scn.PhysicsShape.shapeWithGeometry(rope_element_geometry)
    
    for i in range(rope_seg_nr):
      rope_nodes[i].physicsBody = scn.PhysicsBody.dynamicBody()
      rope_nodes[i].physicsBody.physicsShape = rope_element_physicsShape
      rope_nodes[i].physicsBody.mass = 1.1
      rope_nodes[i].physicsBody.damping = 0.00
      rope_nodes[i].physicsBody.angularDamping = 0.00
      if i > 0:
        physics_world.addBehavior(scn.PhysicsBallSocketJoint.joint(rope_nodes[i-1].physicsBody, (0, -rope_seg_length/2, 0), rope_nodes[i].physicsBody, (0, rope_seg_length/2, 0)))
    
    physics_world.addBehavior(scn.PhysicsBallSocketJoint.joint(rope_nodes[0].physicsBody, (0, rope_seg_length/2, 0)))    
    physics_world.addBehavior(scn.PhysicsBallSocketJoint.joint(rope_nodes[-1].physicsBody, (0, -rope_seg_length/2, 0), ball_node.physicsBody, (0, ball_radius, 0)))

    ball_node.physicsBody.applyForce((45.0, 0.0, 0.0), True)

    camera_node = scn.Node()
    camera_node.camera = scn.Camera()
    camera_node.position = (0 , rope_length+1.0 ,rope_length)
    camera_node.lookAt((0, rope_length/2+1.0, 0))
    root_node.addChildNode(camera_node)
    
    light_node = scn.Node()
    light_node.position = (rope_length, rope_length, rope_length)

    light = scn.Light()
    light.type = scn.LightTypeDirectional
    light.castsShadow = True
    light.shadowSampleCount = 32
    light.color = (.99, 1.0, .86)
    light_node.light = light
    light_node.lookAt((0, rope_length/2+1.0, 0))
    root_node.addChildNode(light_node)
    
    main_view.present(hide_title_bar=False)

Demo.run()
