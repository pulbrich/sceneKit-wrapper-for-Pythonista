'''Cube puzzles - five typical 3x3x3 3D puzzles.

(c) Peter Ulbrich, 2019

a demo script for the sceneKit wrapper package for Pythonista

See the README.md for details.

'''

import math
import sceneKit as scn

import main
from data import *
from piece import *

def setup_elementary_cube_geometry():
  geometry = scn.Box(1., 1., 1., 0.)
  material = scn.Material()
  material.diffuse.contents = 'resources/wood.png'
  geometry.firstMaterial = material
  return geometry
  
def setup_pieces(piece_set, puzzle_variant):
  pieces = []
  for name, cubes in data.reference_pieces[puzzle_variant.value].items():
    handle_node = scn.Node()
    handle_node.name = name
    nodes = []    
    for aCubePosition in cubes:
      nodes.append(scn.Node.nodeWithGeometry(setup_elementary_cube_geometry()))
      nodes[-1].position = aCubePosition  
    
    for aNode in nodes:
      aNode.geometry.firstMaterial.diffuse.intensity = (0.7 - len(pieces)/len(data.reference_pieces[puzzle_variant.value])) + 0.3
      handle_node.addChildNode(aNode)
      
    pieces.append(Piece(piece_set, name, handle_node))
  
  return pieces
  
rotate_action = scn.Action.repeatActionForever(scn.Action.rotateBy(0, math.pi*2, 0, 25.))

def setup_selector_views():
  selector_views = []
  for aVariant in Puzzle_variant:
    selector_view = scn.View(None, superView=data.main_view)
    selector_view.preferredFramesPerSecond = 30
    selector_view.rendersContinuously = False
    selector_view.autoenablesDefaultLighting = True
    selector_view.allowsCameraControl = False
    
    selector_view.scene = scn.Scene()
    selector_view.scene.background.contents = 'beige'
    
    title_geometry = scn.Text(str(aVariant.name).replace('_', ' '), 0.3)
    title_geometry.font = ('Chalkboard SE', 4.)
    title_geometry.firstMaterial.contents = (.48, .14, .14)
    title_geometry.flatness = 0.1
    title_geometry.chamferRadius = 0.08
    bbox_min, bbox_max = title_geometry.boundingBox
    title_size = bbox_max.x - bbox_min.x
    title_node = scn.Node.nodeWithGeometry(title_geometry)
    title_node.position = (-title_size/2, -1., -25.)
    selector_view.scene.rootNode.addChildNode(title_node)
    
    puzzle_node = scn.Node()
    
    table_geometry = scn.Cylinder(6., 0.5)
    table_geometry.firstMaterial.diffuse.contents = 'resources/marble.jpg'
    table_node = scn.Node.nodeWithGeometry(table_geometry)
    table_node.position = (0., -0.75, 0.)
    puzzle_node.addChildNode(table_node)
    
    puzzle_node.position = (0., -0.25, 0.)
    piece_set = Piece_set(aVariant)
    pieces = len(piece_set.pieces)
    for index, aPiece in enumerate(piece_set.pieces):
      show_piece = aPiece.drawer_handle_node
      show_piece.rotation = (0, 1, 0, index/pieces*2*math.pi - math.pi/4.)
      show_piece.position = scn.Vector3(4.*math.sin(index/pieces*2*math.pi), 0., 4.*math.cos(index/pieces*2*math.pi))
      puzzle_node.addChildNode(show_piece)
      
    puzzle_node.runAction(rotate_action)
    selector_view.scene.rootNode.addChildNode(puzzle_node)
    
    camera_node = scn.Node()
    camera_node.name = 'selector_camera'
    camera_node.position = (0., 7., 11.)
    camera_node.lookAt((0., 0., 0.))
    camera_node.camera = scn.Camera()
    selector_view.scene.rootNode.addChildNode(camera_node)
    
    selector_views.append(selector_view)
  return selector_views

def setup_center_view(piece_set):
  center_view = scn.View(None, superView=data.main_view)
  center_view.preferredFramesPerSecond = 30
  center_view.rendersContinuously = False
  center_view.autoenablesDefaultLighting = True    
  center_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleWidth
  center_view.allowsCameraControl = True
  center_view.jitteringEnabled = True
  
  center_view.backgroundColor = 'beige'
  
  box_size = 3.0
  box = scn.Box(box_size, box_size, box_size, 0.0)
  box.firstMaterial.diffuse.contents = (.86, .86, .86)
  box.firstMaterial.transparency = 0.15
  box.firstMaterial.cullMode = scn.CullMode.Front
  box_node = scn.Node.nodeWithGeometry(box)
  box_node.name = 'box'
  box_node.categoryBitMask = 2
  
  tray_handle = setup_tray(piece_set)
  axis_handle = setup_axes()
  tray_handle.addChildNode(axis_handle)
  box_node.addChildNode(tray_handle)
  
  scene = scn.Scene()
  scene.rootNode.addChildNode(box_node)
    
  camera_node = scn.Node()
  camera_node.name = 'center_camera'
  camera_node.position = (8., 10., 12)
  camera_node.lookAt((1., 3., -1.5))
  camera_node.camera = scn.Camera()    
  camera_node.camera.fieldOfView = 50    
  scene.rootNode.addChildNode(camera_node)

  center_view.scene = scene    
  return center_view
  
def setup_drawer_views(piece_set):
  for aPiece in piece_set.pieces:        
    drawer_view = scn.View(None, superView=data.main_view)
    drawer_view.preferredFramesPerSecond = 30
    drawer_view.rendersContinuously = False
    drawer_view.autoenablesDefaultLighting = True
    drawer_view.allowsCameraControl = True
    
    drawer_view.scene = scn.Scene()
    drawer_view.scene.background.contents = 'beige'
    show_piece = aPiece.drawer_handle_node
    show_piece.rotation = (0, 1, 0, math.pi/2.5)
    drawer_view.scene.rootNode.addChildNode(show_piece)
    
    min, max = drawer_view.scene.rootNode.boundingBox
    
    camera_node = scn.Node()
    camera_node.position = (2.5, 3., 2.5)
    camera_node.lookAt(((min.x+max.x)/2+1., (min.y+max.y)/2+0.5, 0.))
    camera_node.camera = scn.Camera()
    drawer_view.scene.rootNode.addChildNode(camera_node)
    
    aPiece.drawer_view = drawer_view
    
def setup_show_drawer_animation():
  core_animation = scn.CoreBasicAnimation('contents')
  core_animation.toValue = (.4, 1.0, .0, 0.9)
  core_animation.removedOnCompletion = False

  animation = scn.Animation.animationWithCAAnimation(core_animation)
  animation.removedOnCompletion = False
  animation.autoreverses = True
  animation.duration = 1.
  animation.repeatCount = 3

  return animation
  
def setup_tray(piece_set):
  tray_handle = scn.Node()
  tray_handle.position = (-1, 5, 1)
  tray_handle.name = 'tray'
  
  for aPiece in piece_set.pieces:
    tray_handle.addChildNode(aPiece.tray_handle_node)
    
  return tray_handle
  
def setup_axes():    
  axis_rode = scn.Cylinder(0.015, 7.5)
  axis_rode.firstMaterial.contents = 'blue'

  vertical_axis_rode = scn.Cylinder(0.015, 11.)
  vertical_axis_rode.firstMaterial.contents = 'blue'
  
  rotate_control_geometry = scn.Sphere(0.35)
  rotate_control_geometry.firstMaterial.contents = 'red'
  
  cube_rotate_control_geometry = scn.Sphere(0.35)
  cube_rotate_control_geometry.firstMaterial.contents = 'green'
  
  shift_control_geometry = scn.Cone(0, 0.38, 0.7)
  shift_control_geometry.firstMaterial.contents = 'orange'
  
  axis_handle = scn.Node()
  axis_handle.name = 'origo'
  axis_handle.position = (-0.5, -0.5, 0.5)
  
  x_axis_node = scn.Node.nodeWithGeometry(axis_rode)
  x_axis_node.rotation = (0, 0, 1, math.pi/2)
  x_axis_node.position = (1.5, 0, 0)
  
  x_axis_rotate_control_node_1 = scn.Node.nodeWithGeometry(rotate_control_geometry)
  x_axis_rotate_control_node_1.position = (0., -axis_rode.height / 2 + 1, 0.)
  x_axis_rotate_control_node_1.name = 'rx1'
  x_axis_rotate_control_node_1.categoryBitMask = 2
  x_axis_node.addChildNode(x_axis_rotate_control_node_1)
  x_axis_rotate_control_node_2 = scn.Node.nodeWithGeometry(rotate_control_geometry)
  x_axis_rotate_control_node_2.position = (0., axis_rode.height / 2 - 1, 0.)
  x_axis_rotate_control_node_2.name = 'rx2'
  x_axis_rotate_control_node_2.categoryBitMask = 2
  x_axis_node.addChildNode(x_axis_rotate_control_node_2)
  
  x_axis_shift_control_node_1 = scn.Node.nodeWithGeometry(shift_control_geometry)
  x_axis_shift_control_node_1.position = (0., -axis_rode.height / 2, 0.)
  x_axis_shift_control_node_1.rotation = (0., 0., 1., -math.pi)
  x_axis_shift_control_node_1.name = 'sx1'
  x_axis_shift_control_node_1.categoryBitMask = 2
  x_axis_node.addChildNode(x_axis_shift_control_node_1)
  x_axis_shift_control_node_2 = scn.Node.nodeWithGeometry(shift_control_geometry)
  x_axis_shift_control_node_2.position = (0., axis_rode.height / 2, 0.)
  x_axis_shift_control_node_2.name = 'sx2'
  x_axis_shift_control_node_2.categoryBitMask = 2
  x_axis_node.addChildNode(x_axis_shift_control_node_2)
  
  axis_handle.addChildNode(x_axis_node)
  
  y_axis_node = scn.Node.nodeWithGeometry(vertical_axis_rode)
  y_axis_node.rotation = (1, 0, 0, -math.pi)
  y_axis_node.position = (0, -3, 0)
  y_axis_rotate_control_node_1 = scn.Node.nodeWithGeometry(rotate_control_geometry)
  y_axis_rotate_control_node_1.position = (0., -vertical_axis_rode.height / 2, 0.)
  y_axis_rotate_control_node_1.name = 'ry1'
  y_axis_rotate_control_node_1.categoryBitMask = 2
  y_axis_node.addChildNode(y_axis_rotate_control_node_1)
  y_axis_rotate_control_node_2 = scn.Node.nodeWithGeometry(rotate_control_geometry)
  y_axis_rotate_control_node_2.position = (0., vertical_axis_rode.height / 2, 0.)
  y_axis_rotate_control_node_2.name = 'ry2'
  y_axis_rotate_control_node_2.categoryBitMask = 2
  y_axis_node.addChildNode(y_axis_rotate_control_node_2)

  axis_handle.addChildNode(y_axis_node)
  
  z_axis_node = scn.Node.nodeWithGeometry(axis_rode)
  z_axis_node.rotation = (1, 0, 0, -math.pi/2)
  z_axis_node.position = (0, 0, -1.5)
  z_axis_rotate_control_node_1 = scn.Node.nodeWithGeometry(rotate_control_geometry)
  z_axis_rotate_control_node_1.position = (0., -axis_rode.height / 2 + 1, 0.)
  z_axis_rotate_control_node_1.name = 'rz1'
  z_axis_rotate_control_node_1.categoryBitMask = 2
  z_axis_node.addChildNode(z_axis_rotate_control_node_1)
  z_axis_rotate_control_node_2 = scn.Node.nodeWithGeometry(rotate_control_geometry)
  z_axis_rotate_control_node_2.position = (0., axis_rode.height / 2 - 1, 0.)
  z_axis_rotate_control_node_2.name = 'rz2'
  z_axis_rotate_control_node_2.categoryBitMask = 2
  z_axis_node.addChildNode(z_axis_rotate_control_node_2)
  
  z_axis_shift_control_node_1 = scn.Node.nodeWithGeometry(shift_control_geometry)
  z_axis_shift_control_node_1.position = (0., -axis_rode.height / 2, 0.)
  z_axis_shift_control_node_1.rotation = (0., 0., 1., math.pi)
  z_axis_shift_control_node_1.name = 'sz1'
  z_axis_shift_control_node_1.categoryBitMask = 2
  z_axis_node.addChildNode(z_axis_shift_control_node_1)
  z_axis_shift_control_node_2 = scn.Node.nodeWithGeometry(shift_control_geometry)
  z_axis_shift_control_node_2.position = (0., axis_rode.height / 2, 0.)
  z_axis_shift_control_node_2.name = 'sz2'
  z_axis_shift_control_node_2.categoryBitMask = 2
  z_axis_node.addChildNode(z_axis_shift_control_node_2)
  
  axis_handle.addChildNode(z_axis_node)

  return axis_handle

if __name__ == '__main__':
  main.MainViewController.run()
