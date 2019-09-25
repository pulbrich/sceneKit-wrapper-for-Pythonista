'''sceneRenderer modul, to be included in sceneKit'''

from collections import OrderedDict, Iterable
from ui import parse_color
import time

import sceneKit
from .sceneKitEnv import *
from .sceneKitNode import *

class TransitionDirection(Enum):
  Up =0
  Down = 1
  Right = 2
  Left = 3
  SKTransitionDirectionUp =0
  SKTransitionDirectionDown = 1
  SKTransitionDirectionRight = 2
  SKTransitionDirectionLeft = 3
  
SKTransitionDirection = TransitionDirection

class DebugOption(Flag):
  OptionNone = 0
  ShowBoundingBoxes = (1 << 1)
  ShowWireframe = (1 << 5)
  RenderAsWireframe = (1 << 6)
  ShowSkeletons = (1 << 7)
  ShowCreases = (1 << 8)
  ShowConstraints = (1 << 9)
  ShowCameras = (1 << 10)
  ShowLightInfluences = (1 << 2)
  ShowLightExtents = (1 << 3)
  ShowPhysicsShapes = (1 << 0)
  ShowPhysicsFields = (1 << 4)
  SCNDebugOptionNone = 0
  SCNDebugOptionShowBoundingBoxes = (1 << 1)
  SCNDebugOptionShowWireframe = (1 << 5)
  SCNDebugOptionRenderAsWireframe = (1 << 6)
  SCNDebugOptionShowSkeletons = (1 << 7)
  SCNDebugOptionShowCreases = (1 << 8)
  SCNDebugOptionShowConstraints = (1 << 9)
  SCNDebugOptionShowCameras = (1 << 10)
  SCNDebugOptionShowLightInfluences = (1 << 2)
  SCNDebugOptionShowLightExtents = (1 << 3)
  SCNDebugOptionShowPhysicsShapes = (1 << 0)
  SCNDebugOptionShowPhysicsFields = (1 << 4)

class RenderingAPI(Enum):
  Metal = 0
  OpenGLES2 = 1
  OpenGLLegacy = 2
  OpenGLCore32 = 3
  OpenGLCore41 = 4
  SCNRenderingAPIMetal = 0
  SCNRenderingAPIOpenGLES2 = 1
  SCNRenderingAPIOpenGLLegacy = 2
  SCNRenderingAPIOpenGLCore32 = 3
  SCNRenderingAPIOpenGLCore41 = 4
  

class SceneRenderer: 
  def setScene(self, scene):
    self.ID.setScene_(scene.ID)
  def getScene(self):
    return sceneKit.Scene.outof(self.ID.scene())
  scene = property(getScene, setScene)
  
  def presentScene(self, scene=None, withTransition=None, incomingPointOfView=None, completionHandler=None, transition=None):
    def _func(_cmd):
      completionHandler()
    if completionHandler is not None:
      block = ObjCBlock(_func)
    else: block = None
    if withTransition is None: withTransition = transition
    if withTransition is not None: withTransition = withTransition.ID
    if incomingPointOfView is not None: incomingPointOfView = incomingPointOfView.ID
    self.ID.presentScene_withTransition_incomingPointOfView_completionHandler_(scene.ID, withTransition, incomingPointOfView, block)
    
  def setPointOfView(self, aNode):
    self.ID.setPointOfView_(aNode.ID)    
  def getPointOfView(self):
    return sceneKit.Node.outof(self.ID.pointOfView())
  pointOfView = property(getPointOfView, setPointOfView)
  
  def setAutoenablesDefaultLighting(self, aBool):
    self.ID.setAutoenablesDefaultLighting_(aBool)    
  def getAutoenablesDefaultLighting(self):
    return self.ID.autoenablesDefaultLighting()
  autoenablesDefaultLighting = property(getAutoenablesDefaultLighting, setAutoenablesDefaultLighting)
  
  def setJitteringEnabled(self, aBool):
    self.ID.setJitteringEnabled_(aBool)    
  def getJitteringEnabled(self):
    return self.ID.jitteringEnabled()
  jitteringEnabled = property(getJitteringEnabled, setJitteringEnabled)
  
  def setShowsStatistics(self, aBool):
    self.ID.setShowsStatistics_(aBool)
  def getShowsStatistics(self):
    return self.ID.showsStatistics()
  showsStatistics = property(getShowsStatistics, setShowsStatistics)
  
  def setDebugOptions(self, flags):
    if not isinstance(flags, Iterable):
      flags = [flags]
    mask = 0
    for aFlag in flags:
      mask = mask | aFlag.value
    self.ID.setDebugOptions_(mask)
  def getDebugOptions(self):
    mask = self.ID.debugOptions()
    flags = []
    for aFlag in DebugOption:
      if (mask & aFlag.value) != 0: flags.append(aFlag)
    if len(flags) == 0: flags = [DebugOption.OptionNone]
    return tuple(flags)
  debugOptions = property(getDebugOptions, setDebugOptions)
    
  def getRenderingAPI(self):
    return RenderingAPI(self.ID.renderingAPI())
  renderingAPI = property(getRenderingAPI, None)
  
  def setSceneTime(self, aSceneTime):
    self.ID.setSceneTime_(aSceneTime)    
  def getSceneTime(self):
    return self.ID.sceneTime()
  sceneTime = property(getSceneTime, setSceneTime)
  
  def setPlaying(self, aBool):
    self.ID.setPlaying_(aBool)    
  def isPlaying(self):
    return self.ID.isPlaying()
  playing = property(isPlaying, setPlaying)
  
  def setLoops(self, aBool):
    self.ID.setLoops_(aBool)    
  def getLoops(self):
    return self.ID.loops()
  loops = property(getLoops, setLoops)
  
  def prepareObject(self, anObject, shouldAbortBlock=None, block=None):
    if shouldAbortBlock is None: shouldAbortBlock = block
    if shouldAbortBlock is not None:
      blockInstance = PrepareObjectShouldAbortBlockBlock(shouldAbortBlock)
      self.ID.prepareObject_shouldAbortBlock_(anObject.ID, blockInstance.blockCode)
    else:
      self.ID.prepareObject_shouldAbortBlock_(anObject.ID, None)
      
  def prepareObjects(self, objects=None, completionHandler=None, withCompletionHandler=None):
    if completionHandler is None: completionHandler = withCompletionHandler
    try:
      iterator = iter(objects)
    except TypeError:
      objects = [objects]
    objects = [anObject.ID for anObject in objects]
    blockInstance = PrepareObjectsWithCompletionHandlerBlock(completionHandler)
    self.ID.prepareObjects_withCompletionHandler_(objects, blockInstance.blockCode)
  
  def hitTest(self, aPoint, options):
    hitList = self.ID.hitTest_options_(CGPoint(aPoint), hitTestOptions(options))
    return tuple([sceneKit.HitTestResult.outof(aHit) for aHit in hitList])

  def isNodeInsideFrustum(self, node=None, withPointOfView=None):
    return self.ID.isNodeInsideFrustum_withPointOfView_(node.ID, withPointOfView.ID)  
  def isNode(self, node, insideFrustumOf=None):
    return self.isNodeInsideFrustum(node, insideFrustumOf)
    
  def nodesInsideFrustumWithPointOfView(self, pointOfView=None):
    nodeList = self.ID.nodesInsideFrustumWithPointOfView_(pointOfView.ID)
    return tuple([sceneKit.Node.outof(aNode) for aNode in nodeList])
  def nodesInsideFrustum(self, of=None):
    return self.nodesInsideFrustumWithPointOfView(pointOfView=of)
    
  def projectPoint(self, point=None):
    pointP = self.ID.projectPoint_(vector3Make(point))
    return Vector3(pointP.a, pointP.b, pointP.c)
    
  def unProjectPoint(self, point=None):
    pointP = self.ID.unProjectPoint_(vector3Make(point))
    return Vector3(pointP.a, pointP.b, pointP.c)
    
  def setDelegate(self, aDelegate):
    sceneRendererDelegate = SceneRendererDelegate(aDelegate)
    self.ID.setDelegate_(sceneRendererDelegate.ID)
  def getDelegate(self):
    aSceneRendererDelegate = sceneKit.SceneRendererDelegate.outof(self.ID.delegate())
    return aSceneRendererDelegate.delegate
  delegate = property(getDelegate, setDelegate)
  
  def setAudioListener(self, aNode):
    if aNode is None: aNode = sceneKit.Nil
    self.ID.setAudioListener_(aNode.ID)    
  def getAudioListener(self):
    return sceneKit.Node.outof(self.ID.audioListener())
  audioListener = property(getAudioListener, setAudioListener)
  
  def getAudioEnvironmentNode(self):
    return self.ID.audioEnvironmentNode()
  audioEnvironmentNode = property(getAudioEnvironmentNode, None)
  
  def getAudioEngine(self):
    return self.ID.audioEngine()
  audioEngine = property(getAudioEngine, None)
  
  def setOverlaySKScene(self, anSKScene):
    self.ID.setOverlaySKScene_(anSKScene)    
  def getOverlaySKScene(self):
    return self.ID.overlaySKScene()
  overlaySKScene = property(getOverlaySKScene, setOverlaySKScene)
  
class PrepareObjectShouldAbortBlockBlock:
  def __init__(self, block):    
    self.blockCode = ObjCBlock(self.blockInterface, restype=c_bool, argtypes=[c_void_p])
    self.pCode = block
      
  def blockInterface(self, _cmd):
    ret = self.pCode()
    if ret is None: return False
    return ret
    
class PrepareObjectsWithCompletionHandlerBlock:
  def __init__(self, block):    
    self.blockCode = ObjCBlock(self.blockInterface, restype=None, argtypes=[c_void_p, c_bool])
    self.pCode = block
      
  def blockInterface(self, _cmd, success):
    self.pCode(success)


class Transition(CInst):
  def __init__(self, duration=None, crossFadeWithDuration=None, doorsCloseHorizontalWithDuration=None, doorsCloseVerticalWithDuration=None, doorsOpenHorizontalWithDuration=None, doorsOpenVerticalWithDuration=None, doorwayWithDuration=None, fadeWithColor=None, fadeWithDuration=None, flipHorizontalWithDuration=None, flipVerticalWithDuration=None, moveInWithDirection= None, pushWithDirection=None, revealWithDirection=None, ID=None):
    if crossFadeWithDuration is not None:
      self.ID = SKTransition.crossFadeWithDuration_(crossFadeWithDuration)
    elif doorsCloseHorizontalWithDuration is not None:
      self.ID = SKTransition.doorsCloseHorizontalWithDuration_(doorsCloseHorizontalWithDuration)
    elif doorsCloseVerticalWithDuration is not None:
      self.ID = SKTransition.doorsCloseVerticalWithDuration_(doorsCloseVerticalWithDuration)
    elif doorsOpenHorizontalWithDuration is not None:
      self.ID = SKTransition.doorsOpenHorizontalWithDuration_(doorsOpenHorizontalWithDuration)
    elif doorsOpenVerticalWithDuration is not None:
      self.ID = SKTransition.doorsOpenVerticalWithDuration_(doorsOpenVerticalWithDuration)
    elif doorwayWithDuration is not None:
      self.ID = SKTransition.doorwayWithDuration_(doorwayWithDuration)
    elif fadeWithColor is not None:
      r, g, b, a = parse_color(fadeWithColor)
      self.ID = SKTransition.fadeWithColor_duration_(ObjCClass('UIColor').color(red=r, green=g, blue=b, alpha=a), duration)
    elif fadeWithDuration is not None:
      self.ID = SKTransition.fadeWithDuration_(FadeWithDuration)
    elif flipHorizontalWithDuration is not None:
      self.ID = SKTransition.flipHorizontalWithDuration_(flipHorizontalWithDuration)
    elif flipVerticalWithDuration is not None: 
      self.ID = SKTransition.flipVerticalWithDuration_(flipVerticalWithDuration)
    elif moveInWithDirection is not None:
      self.ID = SKTransition.moveInWithDirection_duration_(moveInWithDirection, duration)
    elif pushWithDirection is not None:
      self.ID = SKTransition.pushWithDirection_duration_(pushWithDirection, duration)
    elif revealWithDirection is not None:
      self.ID = SKTransition.revealWithDirection_duration_(revealWithDirection, duration)
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = None
    
  @classmethod
  def crossFadeWithDuration(cls, duration=0):
    return cls(crossFadeWithDuration=duration)
  @classmethod
  def crossFade(cls, duration=0):
    return cls.crossFadeWithDuration(cls, duration)
  
  @classmethod
  def doorsCloseHorizontalWithDuration(cls, duration=0):
    return cls(doorsCloseHorizontalWithDuration=duration)
  @classmethod
  def doorsCloseHorizontal(cls, duration=0):
    return cls.doorsCloseHorizontalWithDuration(cls, duration)
    
  @classmethod
  def doorsCloseVerticalWithDuration(cls, duration=0):
    return cls(doorsCloseVerticalWithDuration=duration)
  @classmethod
  def doorsCloseVertical(cls, duration=0):
    return cls.doorsCloseVerticalWithDuration(cls, duration)
    
  @classmethod
  def doorsOpenHorizontalWithDuration(cls, duration=0):
    return cls(doorsOpenHorizontalWithDuration=duration)
  @classmethod
  def doorsOpenHorizontal(cls, duration=0):
    return cls.doorsOpenHorizontalWithDuration(cls, duration)
    
  @classmethod
  def doorsOpenVerticalWithDuration(cls, duration=0):
    return cls(doorsOpenVerticalWithDuration=duration)
  @classmethod
  def doorsOpenVertical(cls, duration=0):
    return cls.doorsOpenVerticalWithDuration(cls, duration)
    
  @classmethod
  def doorwayWithDuration(cls, duration=0):
    return cls(doorwayWithDuration=duration)
  @classmethod
  def doorway(cls, duration=0):
    return cls.doorwayWithDuration(cls, duration)
    
  @classmethod
  def fadeWithColorWithDuration(cls, color=RGBA(0, 0, 0, 0), duration=0):
    return cls(fadeWithColor=color, duration=duration)
  @classmethod
  def fadeWithColor(cls, color=RGBA(0, 0, 0, 0), duration=0):
    return cls.fadeWithColorWithDuration(cls, color, duration)
    
  @classmethod
  def fadeWithDuration(cls, duration=0):
    return cls(fadeWithDuration=duration)
  @classmethod
  def fade(cls, duration=0):
    return cls.fadeWithDuration(cls, duration)
    
  @classmethod
  def flipHorizontalWithDuration(cls, duration=0):
    return cls(flipHorizontalWithDuration=duration)
  @classmethod
  def flipHorizontal(cls, duration=0):
    return cls.flipHorizontalWithDuration(cls, duration)
    
  @classmethod
  def flipVerticalWithDuration(cls, duration=0):
    return cls(flipVerticalWithDuration=duration)
  @classmethod
  def flipVertical(cls, duration=0):
    return cls.flipVerticalWithDuration(cls, duration) 
  
  @classmethod
  def moveInWithDirection(cls, direction=None, duration=0):
    return cls(moveInWithDirection=direction, duration=duration)
  @classmethod
  def moveIn(cls, direction=None, duration=0):
    return cls.moveInWithDirection(cls, direction, duration)
    
  @classmethod
  def pushWithDirection(cls, direction=None, duration=0):
    return cls(pushWithDirection=direction, duration=duration)
  @classmethod
  def push(cls, direction=None, duration=0):
    return cls.pushWithDirection(cls, direction, duration)
    
  @classmethod
  def revealWithDirection(cls, direction=None, duration=0):
    return cls(revealWithDirection=direction, duration=duration)
  @classmethod
  def reveal(cls, direction=None, duration=0):
    return cls.revealWithDirection(cls, direction, duration)
    
  def setPausesIncomingScene(self, aBool):
    self.ID.setPausesIncomingScene_(aBool)    
  def getPausesIncomingScene(self):
    return self.ID.pausesIncomingScene()
  pausesIncomingScene = property(getPausesIncomingScene, setPausesIncomingScene)
  
  def setPausesOutgoingScene(self, aBool):
    self.ID.setPausesOutgoingScene_(aBool)    
  def getPausesOutgoingScene(self):
    return self.ID.pausesOutgoingScene()
  pausesOutgoingScene = property(getPausesOutgoingScene, setPausesOutgoingScene)
  
class HitTestResult(CInst_NoCache):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = None
     
  def getNode(self):
    return sceneKit.Node.outof(self.ID.node())
  node = property(getNode, None)
  
  def getGeometryIndex(self):
    return self.ID.geometryIndex()
  geometryIndex = property(getGeometryIndex, None)
  
  def getFaceIndex(self):
    return self.ID.faceIndex()
  faceIndex = property(getFaceIndex, None)
  
  def getLocalCoordinates(self):
    coo = self.ID.localCoordinates()
    return Vector3(coo.a, coo.b, coo.c)
  localCoordinates = property(getLocalCoordinates, None)
  
  def getWorldCoordinates(self):
    coo = self.ID.worldCoordinates()
    return Vector3(coo.a, coo.b, coo.c)
  worldCoordinates = property(getWorldCoordinates, None)

  def getLocalNormal(self):
    normal = self.ID.localNormal()
    return Vector3(normal.a, normal.b, normal.c)
  localNormal = property(getLocalNormal, None)
  
  def getWorldNormal(self):
    normal = self.ID.worldNormal()
    return Vector3(normal.a, normal.b, normal.c)
  worldNormal = property(getWorldNormal, None)
  
  def getModelTransform(self):
    trans = self.ID.modelTransform()
    return matrix4Make(getCStructValuesAsList(trans))  
  modelTransform = property(getModelTransform, None)
  
  def textureCoordinatesWithMappingChannel(self, channel):
    coord = self.ID.textureCoordinatesWithMappingChannel_(channel)
    return Point(coord.x, coord.y)   
  def textureCoordinates(self, withMappingChannel=0):
    return textureCoordinatesWithMappingChannel(self, withMappingChannel)
    
  def getBoneNode(self):
    return scenekit.Node.outof(self.ID.boneNode())
  boneNode = property(getBoneNode, None)

def renderer_updateAtTime_(_self, _cmd, renderer, time):
  aSceneRendererDelegate = sceneKit.SceneRendererDelegate.outof(ObjCInstance(_self))
  if aSceneRendererDelegate.methods[0]:
    aView = sceneKit.View.outof(ObjCInstance(renderer))
    aSceneRendererDelegate.delegate.update(aView, time)

def renderer_didApplyAnimationsAtTime_(_self, _cmd, renderer, time):
  aSceneRendererDelegate = sceneKit.SceneRendererDelegate.outof(ObjCInstance(_self))
  if aSceneRendererDelegate.methods[1]:
    aView = sceneKit.View.outof(ObjCInstance(renderer))
    aSceneRendererDelegate.delegate.didApplyAnimations(aView, time)

def renderer_didSimulatePhysicsAtTime_(_self, _cmd, renderer, time):
  aSceneRendererDelegate = sceneKit.SceneRendererDelegate.outof(ObjCInstance(_self))
  if aSceneRendererDelegate.methods[2]:
    aView = sceneKit.View.outof(ObjCInstance(renderer))
    aSceneRendererDelegate.delegate.didSimulatePhysics(aView, time)

def renderer_willRenderScene_atTime_(_self, _cmd, renderer, scene, time):
  aSceneRendererDelegate = sceneKit.SceneRendererDelegate.outof(ObjCInstance(_self))
  if aSceneRendererDelegate.methods[3]:
    aView = sceneKit.View.outof(ObjCInstance(renderer))
    aScene = sceneKit.Scene.outof(ObjCInstance(scene))
    aSceneRendererDelegate.delegate.willRenderScene(aView, aScene, time)

def renderer_didRenderScene_atTime_(_self, _cmd, renderer, scene, time):
  aSceneRendererDelegate = sceneKit.SceneRendererDelegate.outof(ObjCInstance(_self))
  if aSceneRendererDelegate.methods[4]:
    aView = sceneKit.View.outof(ObjCInstance(renderer))
    aScene = sceneKit.Scene.outof(ObjCInstance(scene))
    aSceneRendererDelegate.delegate.didRenderScene(aView, aScene, time)

def renderer_didApplyConstraintsAtTime_(_self, _cmd, renderer, time):
  aSceneRendererDelegate = sceneKit.SceneRendererDelegate.outof(ObjCInstance(_self))
  if aSceneRendererDelegate.methods[5]:
    aView = sceneKit.View.outof(ObjCInstance(renderer))
    aSceneRendererDelegate.delegate.didApplyConstraints(aView, time)

class SceneRendererDelegate(CInst):
  _actions = ('update', 'didApplyAnimations', 'didSimulatePhysics', 'willRenderScene', 'didRenderScene', 'didApplyConstraints')
  _newCClassName = 'SCNPYSceneRendererDelegateClass'
  _cMethodList = [renderer_updateAtTime_, renderer_didApplyAnimationsAtTime_, renderer_didSimulatePhysicsAtTime_, renderer_willRenderScene_atTime_, renderer_didRenderScene_atTime_, renderer_didApplyConstraintsAtTime_]
  renderer_updateAtTime_.restype = None
  renderer_updateAtTime_.argtypes = [c_void_p, c_double]
  renderer_didApplyAnimationsAtTime_.restype = None
  renderer_didApplyAnimationsAtTime_.argtypes = [c_void_p, c_double]
  renderer_didSimulatePhysicsAtTime_.restype = None
  renderer_didSimulatePhysicsAtTime_.argtypes = [c_void_p, c_double]
  renderer_willRenderScene_atTime_.restype = None
  renderer_willRenderScene_atTime_.argtypes = [c_void_p, c_void_p, c_double]
  renderer_didRenderScene_atTime_.restype = None
  renderer_didRenderScene_atTime_.argtypes = [c_void_p, c_void_p, c_double]
  renderer_didApplyConstraintsAtTime_.restype = None
  renderer_didApplyConstraintsAtTime_.argtypes = [c_void_p, c_double]
  _protocols =['SCNSceneRendererDelegate']
  DelegateCClass = create_objc_class(_newCClassName, NSObject, methods=_cMethodList, protocols=_protocols)

  def __init__(self, aDelegate=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.delegate = aDelegate
      self.methods = [callable(_a) for _a in [getattr(aDelegate, anAction, False) for anAction in SceneRendererDelegate._actions]]
      self.ID = SceneRendererDelegate.DelegateCClass.alloc().init()
