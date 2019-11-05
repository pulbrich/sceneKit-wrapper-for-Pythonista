"""
based on:
photoCube at https://forum.omz-software.com/topic/3922/for-the-fun-a-photos-cube
For the fun, a Photos cube by cvp at https://forum.omz-software.com/topic/3922/for-the-fun-a-photos-cube
"""

from objc_util import *
import sceneKit as scn
import ui

cube_image_names = ['emj:Airplane', 'emj:Cat_Face', 'emj:Anchor', 'emj:Basketball', 'emj:Aubergine', 'emj:Baby_Chick_1']
cube_images_orig = [ui.Image.named(cube_image_names[i]) for i in range(6)]

(image_width_orig, image_height_orig) = cube_images_orig[0].size
(image_width, image_height) = (image_width_orig * 1.5, image_height_orig * 1.5)
i_x = (image_width - image_width_orig)/2
i_y = (image_height - image_height_orig)/2

cube_images = []
for i in range(6):
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

@on_main_thread
def main():
  main_view = ui.View()
  w, h = ui.get_screen_size()
  main_view.frame = (0,0,w,h)
  main_view.name = 'Photos cube'
  
  scene_view = scn.View(main_view.frame)
  scene_view.autoresizingMask = (scn.ViewAutoresizing.FlexibleHeight, scn.ViewAutoresizing.FlexibleRightMargin)
  
  scene_view.allowsCameraControl = True
  
  scene_view.backgroundColor = 'white'
  
  scene_view.addToSuperview(main_view)
  
  scene = scn.Scene()
  scene_view.scene = scene
    
  root_node = scene.rootNode

  cube_geometry = scn.Box(width=1, height=1, length=1, chamferRadius=0.05)
  cube_geometry_inside = scn.Box(width=1-0.001, height=1-0.001, length=1-0.001, chamferRadius=0.04)
  
  Material_inside = scn.Material()
  Material_inside.diffuse.contents = inside_image
  
  cube_geometry_inside.materials =[Material_inside for i in range(6)]
  
  cube_geometry_materials = [scn.Material() for i in range(6)]
  for i in range(6):
    cube_geometry_materials[i].diffuse.contents = cube_images[i]

 
  cube_geometry.materials = cube_geometry_materials
     
  cube_node = scn.Node.nodeWithGeometry(cube_geometry)
  cube_node_inside = scn.Node.nodeWithGeometry(cube_geometry_inside)
  cube_node.addChildNode(cube_node_inside)
  
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
  
  
  scn.Transaction.setAnimationDuration(10.0)
  directional_light.color = 'yellow'
  
  
  main_view.present(style='fullscreen', hide_title_bar=False)
  
if __name__ == '__main__':
  main()
