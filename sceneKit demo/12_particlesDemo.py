'''
based on the code in the thread https://forum.omz-software.com/topic/1686/3d-in-pythonista by omz
'''
from objc_util import *
import sceneKit as scn
import ui
import math

@on_main_thread
def demo():
  main_view = ui.View()
  w, h = ui.get_screen_size()
  main_view.frame = (0,0,w,h)
  main_view.name = 'particles demo'
  
  scene_view = scn.View(main_view.frame, superView=main_view)
  scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleWidth
  scene_view.antialiasingMode = scn.AntialiasingMode.Multisampling16X

  scene_view.allowsCameraControl = True
  
  scene_view.backgroundColor = 'black'
  
  scene_view.scene = scn.Scene()

  root_node = scene_view.scene.rootNode
  text_mesh = scn.Text.textWithString('Pythonista', 6.0)
  text_mesh.flatness = 0.2
  text_mesh.chamferRadius = 0.4
  text_mesh.font = ('HelveticaNeue-Bold', 18)
  bbox_min, bbox_max = text_mesh.boundingBox
  text_width = bbox_max.x - bbox_min.x
  text_node = scn.Node.nodeWithGeometry(text_mesh)
  text_node.castsShadow = False
  text_container = scn.Node.node()
  text_container.addChildNode(text_node)
  text_container.position = (0, 40, 0)
  text_node.position = (-text_width/2, 0, 0)
  
  fire = scn.ParticleSystem()
  fire.birthRate = 300000
  fire.loops = True
  fire.emissionDuration = 8
  fire.emissionDurationVariation = 4
  fire.idleDuration = 2
  fire.idleDurationVariation = 0.5
  fire.emittingDirection = (0, 1, 0)
  fire.spreadingAngle = 15
  fire.particleDiesOnCollision = False
  fire.particleLifeSpan = 0.4
  fire.particleLifeSpanVariation = 0.5
  fire.particleVelocity = 20
  fire.particleVelocityVariation = 30
  fire.particleImage = ui.Image.named('shp:WhitePuff05')
  fire.particleSize = 0.4
  fire.particleSizeVariation = 0.2
  fire.particleIntensity = 1.5
  fire.particleIntensityVariation = 2
  fire.stretchFactor = 0.02
  colorAnim = scn.CoreKeyframeAnimation()
  colorAnim.values = [(.99, 1.0, .71, 0.8), (1.0, .52, .0, 0.8), (1., .0, .1, 1.), (.78, .0, .0, 0.3)]
  colorAnim.keyTimes = (0., 0.1, 0.8, 1.)
  fire.timingFunctions = [scn.CoreMediaTimingFunction.functionWithName(aFunc) for aFunc in [scn.MediaTimingFunctionEaseOut, scn.MediaTimingFunctionEaseInEaseOut, scn.MediaTimingFunctionEaseIn]]
  prop_con = scn.ParticlePropertyController.controllerWithAnimation(colorAnim)
  fire.propertyControllers = {scn.SCNParticlePropertyColor:prop_con}
  fire.emitterShape = text_mesh
  fire.birthLocation = scn.ParticleBirthLocation.SCNParticleBirthLocationSurface
  text_node.addParticleSystem(fire)

  root_node.addChildNode(text_container)
  
  light_node = scn.Node.node()
  light_node.position = (0, 105, 5)
  light_node.rotation = (1, 0, 0, -math.pi/2)
  light = scn.Light.light()
  light.type = 'spot'
  light.spotOuterAngle = 90
  light.castsShadow = True
  light.shadowSampleCount = 16
  light.color = 'white'
  light_node.light = light
  root_node.addChildNode(light_node)

  main_view.present(hide_title_bar=False)

demo()

