"""
based on:
a tetrahedron by cvp at https://forum.omz-software.com/topic/3922/for-the-fun-a-photos-cube

"""

from objc_util import *
import ctypes
import sceneKit as scn
import ui
import math

@on_main_thread
def demo():
    main_view = ui.View()
    w, h = ui.get_screen_size()
    main_view.frame = (0,0,w,h)
    main_view.name = 'Tetrahedron'
  
    scene_view = scn.View(main_view.frame, superView=main_view)
    scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleRightMargin
    scene_view.allowsCameraControl = True
    
    scene_view.scene = scn.Scene()
    
    root_node = scene_view.scene.rootNode
    
    camera_node = scn.Node()
    camera_node.camera = scn.Camera()
    camera_node.position = (0,0,5)
    root_node.addChildNode(camera_node)    

    verts = [
    scn.Vector3(0, 1, 0),
    scn.Vector3(-0.5, 0, 0.5),
    scn.Vector3(0.5, 0, 0.5),
    scn.Vector3(0.5, 0, -0.5),
    scn.Vector3(-0.5, 0, -0.5),
    scn.Vector3(0, -1, 0)]

    source = scn.GeometrySource.geometrySourceWithVertices(verts)
 
    indexes = [3,3,3,3,3,3,3,3,
    0, 1, 2,
    2, 3, 0,
    3, 4, 0,
    4, 1, 0,
    1, 5, 2,
    2, 5, 3,
    3, 5, 4,
    4, 5, 1]

    elements = scn.GeometryElement.geometryElementWithData(indexes, scn.GeometryPrimitiveType.Polygon)
    
    geometry = scn.Geometry.geometryWithSources(source, elements)

    material = scn.Material()
    material.contents = scn.RGBA(1,0.9,0.9,1.0)
    geometry.materials = material
     
    geometry_node = scn.Node.nodeWithGeometry(geometry)
    root_node.addChildNode(geometry_node)
    
    elements2 = []
    materials = []
    colors = ['red','blue','green','yellow','orange','pink','cyan','orchid']
    for i in range(8):
      j = 8 + i*3
      indexes2 = [indexes[j],indexes[j+1],indexes[j+2]]
      element = scn.GeometryElement.geometryElementWithData(indexes2, scn.GeometryPrimitiveType.Triangles)
      elements2.append(element)
      material = scn.Material()
      material.contents= colors[i]
      materials.append(material)
    geometry2 = scn.Geometry.geometryWithSources(source, elements2)  
    geometry2.materials = materials
    geometry2_node = scn.Node.nodeWithGeometry(geometry2)
    tx,ty,tz = (-1.5,0,0)
    translation = (1,0,0,0, 0,1,0,0, 0,0,1,0, tx,ty,tz,1)
    geometry2_node.pivot = translation
    root_node.addChildNode(geometry2_node)

    constraint = scn.LookAtConstraint.lookAtConstraintWithTarget(geometry_node)
    constraint.gimbalLockEnabled = True
    camera_node.constraints = constraint
    
    light_node = scn.Node()
    light_node.position = (100, 0, -10)
    light = scn.Light()
    light.type = scn.LightTypeDirectional
    light.castsShadow = True
    light.color = 'white'
    light_node.light = light
    root_node.addChildNode(light_node)
    
    rotate_action = scn.Action.repeatActionForever(scn.Action.rotateBy(0, math.pi*2, 0, 10))
    geometry_node.runAction(rotate_action)
    geometry2_node.runAction(rotate_action)
    
    main_view.present(hide_title_bar=False)
  
  
demo()
