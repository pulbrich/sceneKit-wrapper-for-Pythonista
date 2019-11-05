"""
MDL import demo
"""

from objc_util import *
import sceneKit as scn
import ui
import math

MDLAsset, MDLMesh, MDLSubmesh = ObjCClass('MDLAsset'), ObjCClass('MDLMesh'), ObjCClass('MDLSubmesh')



class Demo:
    
  @classmethod
  def run(cls):
    cls().main()
    
  @on_main_thread
  def main(self):
    main_view = ui.View()
    w, h = ui.get_screen_size()
    main_view.frame = (0,0,w,h)
    main_view.name = 'MDL import demo'
  
    scene_view = scn.View(main_view.frame, superView=main_view)
    scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleWidth
    scene_view.allowsCameraControl = True
    scene_view.backgroundColor = 'white'
    scene_view.rendersContinuously = True
    scene_view.scene = scn.Scene()
    
    root_node = scene_view.scene.rootNode

    floor_geometry = scn.Floor()
    floor_node = scn.Node.nodeWithGeometry(floor_geometry)
    root_node.addChildNode(floor_node)
    
    asset = MDLAsset.alloc().initWithURL_(nsurl('Lucy.obj'))
    mesh = asset.objectAtIndex_(0)
    lucy_geometry = scn.Geometry.geometryWithMDLMesh(mesh)
    
    lucy_node_1 = scn.Node.nodeWithGeometry(lucy_geometry)
    root_node.addChildNode(lucy_node_1)
    
    lucy_node_2 = scn.Node.nodeWithMDLObject(mesh)
    lucy_node_2.position = (10., 0., 0.)
    root_node.addChildNode(lucy_node_2)

    camera_node = scn.Node()
    camera_node.camera = scn.Camera()
    camera_node.position = (10., 10., 10.)
    camera_node.lookAt(root_node.position)
    root_node.addChildNode(camera_node)
    
    light_node = scn.Node()
    light_node.position = (-20., 20., 20)
    light = scn.Light()
    light.type = scn.LightTypeDirectional
    light.castsShadow = True
    light.shadowSampleCount = 32
    light.color = (.99, 1.0, .86)
    light_node.light = light
    light_node.lookAt(root_node.position)
    root_node.addChildNode(light_node)
    
    main_view.present(style='fullscreen', hide_title_bar=False)
    
Demo.run()
