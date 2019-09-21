"""
based on:
For the fun, a Photos cube by cvp at https://forum.omz-software.com/topic/3922/for-the-fun-a-photos-cube

includes a renderer delegate demo
"""
import random
import math
from objc_util import *
import sceneKit as scn
import ui

cube_image_names = ['emj:Airplane', 'emj:Cat_Face', 'emj:Anchor', 'emj:Basketball', 'emj:Aubergine', 'emj:Baby_Chick_1', 'emj:Alarm_Clock', 'emj:Ambulance', 'emj:American_Football', 'emj:Artist_Palette', 'emj:Athletic_Shoe', 'emj:Baby_Chick_2', 'emj:Baby_Chick_3', 'emj:Bactrian_Camel', 'emj:Balloon', 'emj:Banana', 'emj:Baseball', 'emj:Bird', 'emj:Blue_Book']

cube_images_orig = [ui.Image.named(cube_image_names[i]) for i in range(len(cube_image_names))]

(image_width_orig, image_height_orig) = cube_images_orig[0].size
(image_width, image_height) = (image_width_orig * 1.5, image_height_orig * 1.5)
i_x = (image_width - image_width_orig)/2
i_y = (image_height - image_height_orig)/2

cube_images = []
for i in range(len(cube_image_names)):
  with ui.ImageContext(image_width, image_height) as ctx:
    cube_images_orig[i].draw(i_x, i_y, image_width_orig, image_height_orig)
    cube_images.append(ctx.get_image())

with ui.ImageContext(image_width, image_height) as ctx:
  rrect = ui.Path.rounded_rect(0, 0, image_width, image_height, 2)
  rrect.line_width = 4
  ui.set_color((.91, .91, .91))
  rrect.fill()
  ui.set_color('black')
  rrect.stroke()
  d = 2
  rrect = ui.Path.rounded_rect(0+d, 0+d, image_width-2*d, image_height-2*d, 2)
  rrect.line_width = 2
  ui.set_color((.6, .6, .6))
  rrect.stroke()
  inside_image = ctx.get_image()

tile_image = ui.Image.named('plf:Tile_Water')
tile_number = 15
tile_factor = scn.Matrix4(tile_number, 0.0, 0.0, 0.0, 0.0, tile_number, 0.0, 0.0, 0.0, 0.0, tile_number, 0.0, 0.0, 0.0, 0.0, 1.0)

class RendererDelegateForMyScene:
# delete unnecessary methods for performance improvement
  def update(self, view, atTime):
    tick = int(atTime*10) % 50
    if tick == 0:
      cube_node = view.scene.rootNode.childNodeWithName('cube node')
      cube_geometry_materials = cube_node.geometry.materials
      for i in range(6):
        cube_geometry_materials[i].diffuse.contents = cube_images[random.randrange(len(cube_image_names))]
      cube_node.geometry.materials = cube_geometry_materials
    else:
      pass
    
  def didApplyAnimations(self, view, atTime):
    pass
    
  def didSimulatePhysics(self, view, atTime):
    pass
    
  def didApplyConstraints(self, view, atTime):
    pass
    
  def willRenderScene(self, view, scene, atTime):
    pass
    
  def didRenderScene(self, view, scene, atTime):
    pass
    
@on_main_thread
def main():
  main_view = ui.View()
  w, h = ui.get_screen_size()
  main_view.frame = (0,0,w,h)
  main_view.name = 'Photos cube'
  
  scene_view = scn.View(main_view.frame, superView=main_view)
  scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleRightMargin  
  scene_view.antialiasingMode = scn.AntialiasingMode.Multisampling16X

  
  scene_view.allowsCameraControl = True
  
  scene_view.backgroundColor = 'white'
  
  scene_view.delegate = RendererDelegateForMyScene()
  
  scene = scn.Scene()
  scene_view.scene = scene
  
  scn.Transaction.disableActions = True
  
  scene.background.contents = tile_image
  scene.background.contentsTransform = tile_factor
  scene.background.wrapS, scene.background.wrapT = scn.WrapMode.Repeat, scn.WrapMode.Repeat
    
  root_node = scene.rootNode

  cube_geometry = scn.Box(width=1, height=1, length=1, chamferRadius=0.05)
  cube_geometry_inside = scn.Box(width=1-0.001, height=1-0.001, length=1-0.001, chamferRadius=0.04)
  
  material_inside = scn.Material()
  material_inside.diffuse.contents = inside_image
  
  cube_geometry_inside.materials =[material_inside for i in range(6)]
  
  cube_geometry_materials = [scn.Material() for i in range(6)]
  for i in range(6):
    cube_geometry_materials[i].diffuse.contents = cube_images[random.randrange(len(cube_image_names))]
  cube_geometry.materials = cube_geometry_materials
   
  cube_node = scn.Node.nodeWithGeometry(cube_geometry)
  cube_node.name = 'cube node'
  cube_node_inside = scn.Node.nodeWithGeometry(cube_geometry_inside)
  cube_node.addChildNode(cube_node_inside)
  
  cube_node.position = (0., 0., -5.)
  
  cube_action = scn.Action.scaleTo(1.5, 3.0)
  cube_reversed_action = scn.Action.scaleTo(1.0, 1.0)
  cube_wait_action = scn.Action.waitForDuration(0.8)
  cube_y_rot_action1 = scn.Action.rotateBy(0, 0.2, 0, 0.3)
  cube_y_rot_action2 = scn.Action.rotateBy(0, -0.4, 0, 0.3)
  cube_y_rot_action3 = scn.Action.rotateBy(0, 0.2, 0, 0.3)
  
  cube_sequence = scn.Action.sequence([cube_action, cube_reversed_action, cube_wait_action, cube_y_rot_action1, cube_y_rot_action2, cube_y_rot_action3, cube_wait_action])
  cube_forever = scn.Action.repeatActionForever(cube_sequence)
  
  cube_node.runAction(cube_forever)
  
  
  constraint = scn.LookAtConstraint.lookAtConstraintWithTarget(cube_node)
  constraint.gimbalLockEnabled = True
  
  camera = scn.Camera()
  camera_node = scn.Node()
  camera_node.name = 'camera!'
  camera_node.camera = camera
  camera_node.position = (-3.0,3.0,3.0)
  camera_node.constraints = [constraint]
  
  lights_node = scn.Node()
  
  ambient_light = scn.Light() 
  ambient_light.type = scn.LightTypeAmbient
  ambient_light.name = 'ambient light'
  ambient_light.color = (.99, 1.0, .86)
  ambient_node = scn.Node()
  ambient_node.light = ambient_light
  lights_node.addChildNode(ambient_node)
  
  directional_light = scn.Light() 
  directional_light.type = scn.LightTypeDirectional
  directional_light.name = 'directional light'
  directional_light.color = 'white'
  directional_node = scn.Node()
  directional_node.light = directional_light
  directional_node.position = camera_node.position
  directional_node.constraints = [constraint]
  
  lights_node.addChildNode(directional_node)
  
  root_node.addChildNode(camera_node)
  root_node.addChildNode(lights_node)
  root_node.addChildNode(cube_node)
  scene_view.pointOfView = camera_node
  

  scn.Transaction.begin()
  scn.Transaction.disableActions = False
  scn.Transaction.animationDuration = 10.0
  directional_light.color = 'yellow'
  scn.Transaction.commit()

  
  scene_view.playing = True
  
  main_view.present(hide_title_bar=False)
  
if __name__ == '__main__':
  main()
