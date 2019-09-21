'''node modul, to be included in sceneKit'''

from ctypes import *
from objc_util import *

import sceneKit

from .sceneKitEnv import *
from .sceneKitGeometry import *
from .sceneKitAnimation import *
from .sceneKitLight import *
from .sceneKitCamera import *
from .sceneKitPhysics import *
from .sceneKitAudio import *

class MovabilityHint(Enum):
  Fixed = 0
  Movable = 1
  SCNMovabilityHintFixed = 0
  SCNMovabilityHintMovable = 1  

class ReferenceLoadingPolicy(Enum):
  Immediate = 0
  OnDemand = 1
  SCNReferenceLoadingPolicyImmediate = 0
  SCNReferenceLoadingPolicyOnDemand = 1


class Node(Actionable, Animatable, BoundingVolume, CInst):
  def __init__(self, geometry=None, mdlObject=None, ID=None):
    if geometry is not None:
      self.ID = SCNNode.nodeWithGeometry_(geometry.ID)
    elif mdlObject is not None:
      self.ID = SCNNode.nodeWithMDLObject_(mdlObject)
      if self.ID is None:
        raise RuntimeError('nodeWithMDLObject failed. Wrong MDL asset?')
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = SCNNode.node()
      
  @classmethod
  def node(cls):
    return cls()
    
  @classmethod
  def nodeWithGeometry(cls, geometry=None):
    return cls(geometry=geometry)
    
  @classmethod
  def nodeWithMDLObject(cls, mdlObject=None):
    return cls(mdlObject=mdlObject)
      
  def setName(self, aString):
    self.ID.setName_(aString)    
  def getName(self):
    return str(self.ID.name())
  name = property(getName, setName)
   
  def setLight(self, aLight):
    self.ID.setLight_(aLight.ID)    
  def getLight(self):
    return sceneKit.Light.outof(self.ID.light())
  light = property(getLight, setLight)
      
  def setCamera(self, camera):
    self.ID.setCamera_(camera.ID)
  def getCamera(self):
    return sceneKit.Camera.outof(self.ID.camera())
  camera = property(getCamera, setCamera)
  
  def setGeometry(self, aGeometry):
    self._ID.setGeometry_(aGeometry.ID)    
  def getGeometry(self):
    return sceneKit.Geometry.outof(self.ID.geometry())
  geometry = property(getGeometry, setGeometry)
  
  def setMorpher(self, aMorpher):
    self.ID.setMorpher_(aMorpher.ID)    
  def getMorpher(self):
    return sceneKit.Morpher.outof(self.ID.morpher())
  morpher = property(getMorpher, setMorpher)
  
  def setSkinner(self, aSkinner):
    self.ID.setSkinner_(aSkinner.ID)    
  def getSkinner(self):
    return sceneKit.Skinner.outof(self.ID.skinner())
  skinner = property(getSkinner, setSkinner)
  
  def setCategoryBitMask(self, aBitMask):
    self.ID.setCategoryBitMask_(aBitMask)    
  def getCategoryBitMask(self):
    return self.ID.categoryBitMask()
  categoryBitMask = property(getCategoryBitMask, setCategoryBitMask)
  
  def setTransform(self, anM4):
    self.ID.setTransform_(matrix4Make(anM4))    
  def getTransform(self):
    return matrix4Make(getCStructValuesAsList(self.ID.transform()))
  transform = property(getTransform, setTransform)
    
  def setPosition(self, aVector3):
    self.ID.setPosition_(vector3Make(aVector3))
  def getPosition(self):
    pos = self.ID.position()
    return Vector3(pos.a, pos.b, pos.c)
  position = property(getPosition, setPosition)
    
  def setRotation(self, aVector4):
    self.ID.setRotation_(vector4Make(aVector4))
  def getRotation(self):
    rot = self.ID.rotation()
    return Vector4(rot.a, rot.b, rot.c, rot.d)
  rotation = property(getRotation, setRotation)
    
  def setEulerAngles(self, aVector3):
    self.ID.setEulerAngles_(vector3Make(aVector3))
  def getEulerAngles(self):
    angle = self.ID.eulerAngles()
    return Vector3(angle.a, angle.b, angle.c)
  eulerAngles = property(getEulerAngles, setEulerAngles)
    
  def setOrientation(self, aQuaternion):
    self.ID.setOrientation_(quaternionMake(aQuaternion))
  def getOrientation(self):
    ori = self.ID.orientation()
    return Quaternion(ori.a, ori.b, ori.c, ori.d)
  orientation = property(getOrientation, setOrientation)
    
  def setScale(self, aVector3):
    self.ID.setScale_(vector3Make(aVector3))
  def getScale(self):
    sca = self.ID.scale()
    return Vector3(sca.a, sca.b, sca.c)
  scale = property(getScale, setScale)
    
  def setPivot(self, aMatrix4):
    self.ID.setPivot_(matrix4Make(aMatrix4))
  def getPivot(self):
    piv = self.ID.pivot()
    return matrix4Make(getCStructValuesAsList(piv))
  pivot = property(getPivot, setPivot)
  
  
  simdTransform = property(getTransform, setTransform)
  simdPosition = property(getPosition, setPosition)
  simdRotation = property(getRotation, setRotation)
  simdEulerAngles = property(getEulerAngles, setEulerAngles)
  simdOrientation = property(getOrientation, setOrientation)
  simdScale = property(getScale, setScale)
  simdPivot = property(getPivot, setPivot)
  
  def setConstraints(self, listOfConstraints):
    try:
      iterator = iter(listOfConstraints)
    except TypeError:
      listOfConstraints = [listOfConstraints]
    self.ID.setConstraints_([lc.ID for lc in listOfConstraints])    
  def getConstraints(self):
    return tuple([sceneKit.Constraint.outof(lc) for lc in self.ID.constraints()])
  constraints = property(getConstraints, setConstraints)
      
  def getPresentationNode(self):
    return sceneKit.Node.outof(self.ID.presentationNode())
  presentationNode = property(getPresentationNode, None)
  
  def setPaused(self, aBool):
    self.ID.setPaused_(aBool)    
  def isPaused(self):
    return self.ID.isPaused()
  paused = property(isPaused, setPaused)
  
  def setHidden(self, aBool):
    self.ID.setHidden_(aBool)    
  def isHidden(self):
    return self.ID.isHidden()
  hidden = property(isHidden, setHidden)
  
  def setOpacity(self, anOpacity):
    self.ID.setOpacity_(anOpacity)    
  def getOpacity(self):
    return self.ID.opacity()
  opacity = property(getOpacity, setOpacity)
  
  def setRenderingOrder(self, anInt):
    self.ID.setRenderingOrder_(anInt)    
  def getRenderingOrder(self):
    return self.ID.renderingOrder()
  renderingOrder = property(getRenderingOrder, setRenderingOrder)
  
  def setCastsShadow(self, aBool):
    self.ID.setCastsShadow_(aBool)    
  def getCastsShadow(self):
    return self.ID.castsShadow()
  castsShadow = property(getCastsShadow, setCastsShadow)
  
  def setMovabilityHint(self, aHint):
    self.ID.setMovabilityHint_(aHint.value)
  def getMovabilityHint(self):
    return MovabilityHint(self.ID.movabilityHint())
  movabilityHint = property(getMovabilityHint, setMovabilityHint)
  
  def getParentNode(self):
    return sceneKit.Node.outof(self.ID.parentNode())
  parentNode = property(getParentNode, None)

  def getChildNodes(self):
    nodeList = self.ID.childNodes()
    return tuple([sceneKit.Node.outof(aNode) for aNode in nodeList])
  childNodes = property(getChildNodes, None)
  
  def addChildNode(self, child=None):
    self.ID.addChildNode_(child.ID)
    
  def insertChildNode(self, child=None, atIndex=0):
    self.ID.insertChildNode_atIndex_(child.ID, atIndex)
    
  def removeFromParentNode(self):
    self.ID.removeFromParentNode()
    
  def replaceChildNode(self, oldchild, newchild):
    self.ID.replaceChildNode_with_(oldchild.ID, newchild.ID)
    
  def childNodesPassingTest(self, predicate=None):
    blockInstance = ChildNodesPassingTestBlock(predicate)
    nodeList = self.ID.childNodesPassingTest_(blockInstance.blockCode)
    return tuple(sceneKit.Node.outof(aNode) for aNode in nodeList)
  
  def childNodeWithName(self, name, recursively=False):
    return sceneKit.Node.outof(self.ID.childNodeWithName_recursively_(name, recursively))
    
  def enumerateChildNodesUsingBlock(self, block=None):
    blockInstance = EnumerateChildNodesUsingBlockBlock(block)
    self.ID.enumerateChildNodesUsingBlock_(blockInstance.blockCode)
    
  def enumerateHierarchyUsingBlock(self, block=None):
    blockInstance = EnumerateChildNodesUsingBlockBlock(block)
    self.ID.enumerateHierarchyUsingBlock_(blockInstance.blockCode)
    
  def setFilters(self, filters):
    self.ID.setFilters_(filters)
  def getFilters(self):
    ret = self.ID.filters()
    return tuple(ret) if ret is not None else None
  filters = property(getFilters, setFilters)
    
  def setPhysicsBody(self, aPhysicsBody):
    self.ID.setPhysicsBody_(aPhysicsBody.ID)    
  def getPhysicsBody(self):
    return sceneKit.PhysicsBody.outof(self.ID.physicsBody())
  physicsBody = property(getPhysicsBody, setPhysicsBody)
  
  def setPhysicsField(self, aPhysicsField):
    self.ID.setPhysicsField_(aPhysicsField.ID)    
  def getPhysicsField(self):
    return sceneKit.PhysicsField.outof(self.ID.physicsField())
  physicsField = property(getPhysicsField, setPhysicsField)
  
  def addParticleSystem(self, system=None):
    self.ID.addParticleSystem_(system.ID)
    
  def getParticleSystems(self):
    return tuple([sceneKit.ParticleSystem.outof(aSystem) for aSystem in self.ID.particleSystems()])
  particleSystems = property(getParticleSystems, None)
  
  def removeParticleSystem(self, system=None):
    self.ID.removeParticleSystem_(system.ID)
    
  def removeAllParticleSystems(self):
    self.ID.removeAllParticleSystems()
    
  def addAudioPlayer(self, player=None):
    self.ID.addAudioPlayer_(player.ID)
    
  def getAudioPlayers(self):
    ret = self.ID.audioPlayers()
    if ret is None: ret = []
    return tuple(sceneKit.AudioPlayer.outof(aPlayer) for aPlayer in ret)
  audioPlayers = property(getAudioPlayers, None)
  
  def removeAudioPlayer(self, player=None):
    self.ID.removeAudioPlayer_(player.ID)
    
  def removeAllAudioPlayers(self):
    self.ID.removeAllAudioPlayers()
    
  def clone(self):
    return sceneKit.Node.outof(self.ID.clone())
    
  def flattenedClone(self):
    return sceneKit.Node.outof(self.ID.flattenedClone())
    
  def hitTestWithSegment(self, fromPoint=None, toPoint=None, options=None):
    fpv, tpv = SCNVector3(), SCNVector3()
    fpv.x, fpv.y, fpv.z = fromPoint[0], fromPoint[1], fromPoint[2]
    tpv.x, tpv.y, tpv.z = toPoint[0], toPoint[1], toPoint[2]
    hitList = self.ID.hitTestWithSegmentFromPoint_toPoint_options_(fpv, tpv, hitTestOptions(options))
    return tuple([sceneKit.HitTestResult.outof(aHit) for aHit in hitList])
    
  def rotateBy(self, worldRotation=None, worldTarget=None):
    self.ID.rotateBy_aroundTarget_(quaternionMake(worldRotation), vector3Make(worldTarget))
  def rotateByAroundTarget(self, rotateBy=None, aroundTarget=None):
    self.rotateBy(rotateBy, aroundTarget)
    
  def localTranslateBy(self, translation=None):
    self.ID.localTranslateBy_(vector3Make(translation))
    
  def localRotateBy(self, rotation=None):
    self.ID.localRotateBy_(quaternionMake(rotation))
    
  def lookAt(self, worldTarget=None):
    self.ID.lookAt_(vector3Make(worldTarget))
    
  def lookAtUpLocalFront(self, worldTarget=None, worldUp=None, localFront=None):
    self.ID.lookAt_up_localFront_(vector3Make(worldTarget), vector3Make(worldUp), vector3Make(localFront))
  def lookAtUp(self, lookAt=None, up=None, localFront=None):
    self.lookAtUpLocalFront(lookAt, up, localFront)
  
  localRight = Vector3(SCNNode.localRight().a, SCNNode.localRight().b, SCNNode.localRight().c)
  localUp = Vector3(SCNNode.localUp().a, SCNNode.localUp().b, SCNNode.localUp().c)
  localFront = Vector3(SCNNode.localFront().a, SCNNode.localFront().b, SCNNode.localFront().c)
  
  def getWorldRight(self):
    right = self.ID.worldRight()
    return Vector3(right.a, right.b, right.c)
  worldRight = property(getWorldRight, None)
  
  def getWorldUp(self):
    up = self.ID.worldUp()
    return Vector3(up.a, up.b, up.c)
  worldUp = property(getWorldUp, None)
  
  def getWorldFront(self):
    front = self.ID.worldFront()
    return Vector3(front.a, front.b, front.c)
  worldFront = property(getWorldFront, None)
  
  def setWorldTransform(self, aTransform):
    self.ID.setWorldTransform_(matrix4Make(aTransform))
  def getWorldTransform(self):
    aTransform = self.ID.worldTransform()
    return matrix4Make(getCStructValuesAsList(aTransform))
  worldTransform = property(getWorldTransform, setWorldTransform)
  
  def setWorldOrientation(self, anOrientation):
    self.ID.setWorldOrientation_(quaternionMake(anOrientation))
  def getWorldOrientation(self):
    anOrientation = self.ID.worldOrientation()
    return quaternionMake(getCStructValuesAsList(anOrientation))
  worldOrientation = property(getWorldOrientation, setWorldOrientation)
  
  def setWorldPosition(self, aPosition):
    self.ID.setWorldPosition_(vector3Make(aPosition))
  def getWorldPosition(self):
    aPosition = self.ID.worldPosition()
    return Vector3(aPosition.a, aPosition.b, aPosition.c)
  worldPosition = property(getWorldPosition, setWorldPosition)
  
  def convertPosition(self, position=None, fromNode=None, toNode=sceneKit.Nil):
    if fromNode is not None:
      return vector3Make(getCStructValuesAsList(self.ID.convertPosition_fromNode_(vector3Make(position), fromNode.ID)))
    else:
      return vector3Make(getCStructValuesAsList(self.ID.convertPosition_toNode_(vector3Make(position), toNode.ID)))
  def convertPositionFromNode(self, position=None, fromNode=None):
    return self.convertPosition(position, fromNode=fromNode)
  def convertPositionToNode(self, position=None, toNode=None):
    return self.convertPosition(position, toNode=toNode)
    
  def convertTransform(self, transform=None, fromNode=None, toNode=sceneKit.Nil):
    if fromNode is not None:
      return matrix4Make(getCStructValuesAsList(self.ID.convertTransform_fromNode_(matrix4Make(transform), fromNode.ID)))
    else:
      return matrix4Make(getCStructValuesAsList(self.ID.convertTransform_toNode_(matrix4Make(transform), toNode.ID)))
  def convertTransformFromNode(self, transform=None, fromNode=None):
    return self.convertTransform(transform, fromNode=fromNode)
  def convertTransformToNode(self, transform=None, toNode=None):
    return self.convertTransform(transform, toNode=fromNode)
    
  def convertVector(self, vector=None, fromNode=None, toNode=sceneKit.Nil):
    if fromNode is not None:
      return vector3Make(getCStructValuesAsList(self.ID.convertVector_fromNode_(vector3Make(vector), fromNode.ID)))
    else:
      return vector3Make(getCStructValuesAsList(self.ID.convertVector_toNode_(vector3Make(vector), toNode.ID)))
  def convertVectorFromNode(self, vector=None, fromNode=None):
    return self.convertVector(vector, fromNode=fromNode)
  def convertVectorToNode(self, vector=None, toNode=None):
    return self.convertVector(vector, toNode=fromNode)
    
  simdRotateBy = rotateBy
  simdRotateByAroundTarget = rotateByAroundTarget
  simdLocalTranslateBy = localTranslateBy
  simdLocalRotateBy = localRotateBy
  simdLookAt = lookAt
  simdLookAtUpLocalFront = lookAtUpLocalFront
  simdLookAtUp = lookAtUp
  
  simdLocalRight = localRight
  simdLocalUp = localUp
  simdLocalFront = localFront
  simdWorldRight = property(getWorldRight, None)
  simdWorldUp = property(getWorldUp, None)
  simdWorldFront = property(getWorldFront, None)
  simdWorldTransform = property(getWorldTransform, setWorldTransform)
  simdWorldOrientation = property(getWorldOrientation, setWorldOrientation)
  simdWorldPosition = property(getWorldPosition, setWorldPosition)
  
  smidConvertPosition = convertPosition
  smidConvertPositionFromNode = convertPositionFromNode
  smidConvertPositionToNode = convertPositionToNode
  
  smidConvertTransform = convertTransform
  smidConvertTransformFromNode = convertTransformFromNode
  smidConvertTransformToNode = convertTransformToNode
  
  smidConvertVector = convertVector
  smidConvertVectorFromNode = convertVectorFromNode
  smidConvertVectorToNode = convertVectorToNode
  
class ChildNodesPassingTestBlock:
  def __init__(self, block):    
    self.blockCode = ObjCBlock(self.blockInterface, restype=c_bool, argtypes=[c_void_p, c_void_p, POINTER(c_bool)])
    self.pCode = block
      
  def blockInterface(self, _cmd, xnode, xstop):
    node = sceneKit.Node.outof(ObjCInstance(xnode))
    res = self.pCode(node)
    try:
      ret, stop = res
    except TypeError:
      ret, stop = res, False
    xstop[0] = stop
    return ret
    
class EnumerateChildNodesUsingBlockBlock:
  def __init__(self, block):    
    self.blockCode = ObjCBlock(self.blockInterface, restype=None, argtypes=[c_void_p, c_void_p, POINTER(c_bool)])
    self.pCode = block
      
  def blockInterface(self, _cmd, xnode, xstop):
    node = sceneKit.Node.outof(ObjCInstance(xnode))
    stop = self.pCode(node)
    xstop[0] = stop
  
class ReferenceNode(Node):
  def __init__(self, referenceURL=None, ID=None):
    if referenceURL is not None:
      self.ID = SCNReferenceNode.alloc().initWithURL_(nsurl(referenceURL))
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = SCNReferenceNode.alloc().init()
  
  @classmethod
  def referenceNodeWithURL(cls, referenceURL=None):
    return cls(referenceURL=referenceURL)
    
  def initWithURL(self, referenceURL=None):
    self.ID = self.ID.initWithURL_(nsurl(referenceURL))
    return self
    
  def initWithCoder(self, aDecoder=None):
    self.ID = self.ID.initWithCoder_(aDecoder)
    return self
    
  def setReferenceURL(self, anURL):
    self.ID.setReferenceURL_(nsurl(anURL))
  def getReferenceURL(self):
    return str(self.ID.referenceURL().absoluteString())
  referenceURL = property(getReferenceURL, setReferenceURL)
  
  def setLoadingPolicy(self, aPolicy):
    self.ID.setLoadingPolicy_(aPolicy.value)
  def getLoadingPolicy(self):
    return ReferenceLoadingPolicy(self.ID.loadingPolicy())
  loadingPolicy = property(getLoadingPolicy, setLoadingPolicy)
  
  def load(self):
    self.ID.load()
    
  def getLoaded(self):
    return self.ID.loaded()
  loaded = property(getLoaded, None)
  
  def unload(self):
    self.ID.unload()
