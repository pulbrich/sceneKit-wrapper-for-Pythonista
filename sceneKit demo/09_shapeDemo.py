'''
shape: A geometry based on a two-dimensional path, optionally extruded to create a three-dimensional object
'''
from objc_util import *
import sceneKit as scn
import ui
from math import *

w, h = ui.get_screen_size()
title_bar = 88+44 # you should get these programatically in a real app
if w > h:
  image_frame = (0, 0, w/2, h-title_bar)
  scene_frame = (w/2, 0, w/2, h)
  box_bubble = 1.4
else:
  image_frame = (0, 0, w, (h-title_bar)/2)
  scene_frame = (0, (h-title_bar)/2, w, (h+title_bar)/2)
  box_bubble = 1.0
    
image_size = CGSize(image_frame[2], image_frame[3])
image_center = CGPoint(image_size.width/2, image_size.height/2)
leaves = 20
r0 = min(image_size.width, image_size.height)/2*0.1
r1 = min(image_size.width, image_size.height)/2*0.8
c1 = r0+(r1-r0)*0.5
c2 = r0+(r1-r0)*0.95
dalpha = 2*pi/leaves/2

path = ui.Path()
for i in range(leaves):
  alpha = i*2*pi/leaves
  x0, y0 = image_center.x+r0*cos(alpha), image_center.y+r0*sin(alpha)
  x1, y1 = image_center.x+r1*cos(alpha), image_center.y+r1*sin(alpha)
  cx11, cy11 = image_center.x+c2*cos(alpha+dalpha), image_center.y+c2*sin(alpha+dalpha)
  cx21, cy21 = image_center.x+c1*cos(alpha+dalpha), image_center.y+c1*sin(alpha+dalpha)
  cx12, cy12 = image_center.x+c1*cos(alpha+dalpha), image_center.y+c1*sin(alpha+dalpha)
  cx22, cy22 = image_center.x+c2*cos(alpha-dalpha), image_center.y+c2*sin(alpha-dalpha)
  path.move_to(x0, y0)
  path.add_curve(x1, y1, cx11, cy11, cx21, cy21)
  path.add_curve(x0, y0, cx12, cy12, cx22, cy22)
  
x0, y0 = image_center.x+r0*cos(0), image_center.y+r0*sin(0)
path.move_to(x0, y0)
path.add_arc(image_center.x, image_center.y, r0, 0, 2*pi)  
path.close()

with ui.ImageContext(image_size.width, image_size.height) as ctx:
  ui.set_color('red')
  path.stroke()
  img = ctx.get_image()

@on_main_thread
def demo():
  main_view = ui.View()
  main_view.frame = (0,0,w,h)
  main_view.name = 'shapeDemo'
  main_view.background_color = 'white'
  
  image_view = ui.ImageView()
  image_view.frame = image_frame
  image_view.background_color = 'white'
  image_view.content_mode = ui.CONTENT_CENTER
  image_view.image = img
  
  main_view.add_subview(image_view)
  
  scene_view = scn.View(scene_frame, superView=main_view)
  scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleRightMargin  
  scene_view.antialiasingMode = scn.AntialiasingMode.Multisampling16X
  scene_view.allowsCameraControl = True 
  scene_view.backgroundColor = 'white' 
  scene_view.scene = scn.Scene()

  root_node = scene_view.scene.rootNode

  shape = scn.Shape.shapeWithPath(path, 40)
  shape.chamferRadius = 8
  shape.firstMaterial.contents = 'yellow'
  
  shape_node = scn.Node.nodeWithGeometry(shape)
  shape_node.castsShadow = True
  bbox_min, bbox_max = shape.boundingBox
  shape_width = bbox_max.x - bbox_min.x
  shape_height = bbox_max.y - bbox_min.y
  shape_tr = list(scn.Matrix4Identity)
  shape_tr[13] = bbox_min.y+0.5*shape_height
  shape_node.pivot = shape_tr
  shape_node.position = (-bbox_min.x-0.5*shape_width, 0, 0)

  shape_container = scn.Node()
  shape_container.addChildNode(shape_node)

  scale = image_size.width/shape_width
  shape_container.scale = (scale, scale, 1)
  shape_width *= scale
  shape_height *= scale
  
  shape_container.position = (0, 0.2*shape_height, 0.5*shape_height)
  shape_container.rotation = (0, 1, 0, pi) # compensates for the differen coordinate systems of drawing vs. scene
  
  rotate_action = scn.Action.rotateBy(0, 0, 2*pi, 10)
  rotate_action.timingMode = scn.ActionTimingMode.EaseInEaseOut
  invers_action = rotate_action.reversedAction()  
  combined_action = scn.Action.sequence([rotate_action, invers_action])  
  shape_container.runAction(scn.Action.repeatActionForever(combined_action))
  
  box = scn.Box(width=2*shape_width, height=4, length=1.6*shape_width, chamferRadius=1)
  box.firstMaterial.contents = (.76, .91, 1.0)
  
  boxBoxMin, boxBoxMax = box.boundingBox
  box.boundingBox = ((box_bubble*boxBoxMin.x, boxBoxMin.y, boxBoxMin.z), (box_bubble*boxBoxMax.x, boxBoxMax.y, boxBoxMax.z))
  box_node = scn.Node.nodeWithGeometry(box)
  box_node.rotation = (1, 0, 0, pi/4)

  root_node.addChildNode(box_node)
  root_node.addChildNode(shape_container)
  
  constraint = scn.LookAtConstraint.lookAtConstraintWithTarget(shape_container)
  constraint.gimbalLockEnabled = True
  
  light_node = scn.Node()
  light_z = boxBoxMax.z + 0.0*boxBoxMax.z
  light_y = (shape_container.position.y+0.5*shape_height/2)/shape_container.position.z*light_z
  light_node.position = (20, light_y, light_z)
  light_node.constraints = [constraint]
  light = scn.Light()
  light.type = 'spot'
  light.spotOuterAngle = 90
  light.castsShadow = True
  light.zFar = 1500
  light.shadowSampleCount = 16
  light.color = 'white'
  light_node.light = light
  root_node.addChildNode(light_node)
  
  ambient_light = scn.Light() 
  ambient_light.type = scn.LightTypeAmbient
  ambient_light.color = (.41, .32, .0)
  ambient_node = scn.Node()
  ambient_node.light = ambient_light
  root_node.addChildNode(ambient_node)
    
  main_view.present(hide_title_bar=False)

demo()
