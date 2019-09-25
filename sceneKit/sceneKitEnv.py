'''environment for sceneKit'''

from objc_util import *
from collections import namedtuple, Iterable
from ui import parse_color, Image
import ui
from types import MethodType
from enum import Enum, Flag
import weakref

import sceneKit

load_framework('SceneKit')
load_framework('SpriteKit')

NSValue = ObjCClass('NSValue')
NSError = ObjCClass('NSError')
UIImage = ObjCClass('UIImage')
UIFont = ObjCClass('UIFont')


CAMediaTimingFunction, CAValueFunction, CAAnimation, CABasicAnimation, CAKeyframeAnimation, CAAnimationGroup = map(ObjCClass, ['CAMediaTimingFunction', 'CAValueFunction', 'CAAnimation', 'CABasicAnimation', 'CAKeyframeAnimation', 'CAAnimationGroup'])

SCNView, SCNScene, SCNBox, SCNNode, SCNSceneSource, SCNMaterial, SCNCamera, SCNLight, \
  SCNGeometry, SCNFloor, SCNPlane, SCNBox, SCNCapsule, SCNCone, \
  SCNCylinder, SCNPyramid, SCNSphere, SCNTorus, SCNTube, SCNMaterialProperty, SCNConstraint, \
  SCNBillboardConstraint, SCNLookAtConstraint, SCNDistanceConstraint, SCNAvoidOccluderConstraint, \
  SCNAccelerationConstraint, SCNSliderConstraint, SCNReplicatorConstraint, SCNIKConstraint, \
  SCNAction, SCNTransaction, SCNAnimation, SCNAnimationPlayer, SCNAnimationEvent, \
  SCNTimingFunction, SKTransition, SCNMorpher, SCNReferenceNode, SCNGeometrySource, SCNGeometryElement, \
  SCNText, SCNShape, SCNLevelOfDetail, SCNGeometryTessellator, SCNSkinner, SCNPhysicsShape, \
  SCNPhysicsBody, SCNPhysicsContact, SCNPhysicsWorld, SCNPhysicsField, SCNPhysicsBehavior, SCNPhysicsHingeJoint, \
  SCNPhysicsSliderJoint, SCNPhysicsBallSocketJoint, SCNPhysicsConeTwistJoint, SCNPhysicsVehicle, SCNPhysicsVehicleWheel, \
  SCNParticleSystem, SCNParticlePropertyController, SCNAnimationPlayer, SCNAudioSource, SCNAudioPlayer, SCNSceneSource \
  = map(ObjCClass, ['SCNView', 'SCNScene', 'SCNBox', 'SCNNode', 'SCNSceneSource', 'SCNMaterial', 'SCNCamera', 'SCNLight', 'SCNGeometry', 'SCNFloor', 'SCNPlane', 'SCNBox', 'SCNCapsule', 'SCNCone', 'SCNCylinder', 'SCNPyramid', 'SCNSphere', 'SCNTorus', 'SCNTube', 'SCNMaterialProperty', 'SCNConstraint', 'SCNBillboardConstraint', 'SCNLookAtConstraint', 'SCNDistanceConstraint', 'SCNAvoidOccluderConstraint', 'SCNAccelerationConstraint', 'SCNSliderConstraint', 'SCNReplicatorConstraint', 'SCNIKConstraint', 'SCNAction', 'SCNTransaction', 'SCNAnimation', 'SCNAnimationPlayer', 'SCNAnimationEvent', 'SCNTimingFunction', 'SKTransition', 'SCNMorpher', 'SCNReferenceNode', 'SCNGeometrySource', 'SCNGeometryElement', 'SCNText', 'SCNShape', 'SCNLevelOfDetail', 'SCNGeometryTessellator', 'SCNSkinner', 'SCNPhysicsShape', 'SCNPhysicsBody', 'SCNPhysicsContact', 'SCNPhysicsWorld', 'SCNPhysicsField', 'SCNPhysicsBehavior', 'SCNPhysicsHingeJoint', 'SCNPhysicsSliderJoint', 'SCNPhysicsBallSocketJoint', 'SCNPhysicsConeTwistJoint', 'SCNPhysicsVehicle', 'SCNPhysicsVehicleWheel', 'SCNParticleSystem', 'SCNParticlePropertyController', 'SCNAnimationPlayer', 'SCNAudioSource', 'SCNAudioPlayer', 'SCNSceneSource'])
  
_hitTestOptions = []
for anOption in ['SCNHitTestBackFaceCullingKey', 'SCNHitTestBoundingBoxOnlyKey', 'SCNHitTestOptionCategoryBitMask', \
'SCNHitTestClipToZRangeKey', 'SCNHitTestIgnoreChildNodesKey', 'SCNHitTestIgnoreHiddenNodesKey', \
'SCNHitTestRootNodeKey', 'SCNHitTestOptionSearchMode']:
  _hitTestOptions.append(str(ObjCInstance(c_void_p.in_dll(c, anOption))))
_hitTestOptions = tuple(_hitTestOptions)

SCNHitTestBackFaceCullingKey, SCNHitTestBoundingBoxOnlyKey, SCNHitTestOptionCategoryBitMask, \
SCNHitTestClipToZRangeKey, SCNHitTestIgnoreChildNodesKey, SCNHitTestIgnoreHiddenNodesKey, \
SCNHitTestRootNodeKey, SCNHitTestOptionSearchMode = _hitTestOptions
HitTestBackFaceCulling, HitTestBoundingBoxOnly, HitTestCategoryBitMask, HitTestClipToZRange, \
HitTestIgnoreChildNodes, HitTestIgnoreHiddenNodes, HitTestRootNode, HitTestSearchMode = _hitTestOptions

class HitTestSearchMode(Enum):
  Closest = 0
  All = 1
  Any = 2
  SCNHitTestSearchModeClosest = 0
  SCNHitTestSearchModeAll = 1
  SCNHitTestSearchModeAny =2

def hitTestOptions(inDict):
  outDict = {}
  for k, v in inDict.items():
    if k == HitTestBackFaceCulling:
      outDict[k] = bool(v)
    elif k == HitTestBoundingBoxOnly:
      outDict[k] = bool(v)
    elif k == HitTestCategoryBitMask:
      outDict[k] = int(v)
    elif k == HitTestClipToZRange:
      outDict[k] = bool(v)
    elif k == HitTestIgnoreChildNodes:
      outDict[k] = bool(v)
    elif k == HitTestIgnoreHiddenNodes:
      outDict[k] = bool(v)
    elif k == HitTestRootNode:
      outDict[k] = v.ID
    elif k == HitTestSearchMode:
      outDict[k] = v.value
  return outDict

Point = namedtuple('Point', 'x y')
Vector2 = namedtuple('Vector2', 'x y')
Vector3 = namedtuple('Vector3', 'x y z')
class SCNVector3(Structure):
  _fields_ = [("x", c_float), ("y", c_float), ("z", c_float)]

Vector4 = namedtuple('Vector4', 'x y z w')
Quaternion = namedtuple('Quaternion', 'x y z w')
class SCNVector4(Structure):
  _fields_ = [("x", c_float), ("y", c_float), ("z", c_float), ("w", c_float)]

Matrix4 = namedtuple('Matrix4', 'm11 m12 m13 m14 m21 m22 m23 m24 m31 m32 m33 m34 m41 m42 m43 m44')
Matrix4Identity = Matrix4(1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0)

class SCNMatrix4(Structure):
  _fields_ = [('m11', c_float), ('m12', c_float), ('m13', c_float), ('m14', c_float), ('m21', c_float), ('m22', c_float), ('m23', c_float), ('m24', c_float), ('m31', c_float), ('m32', c_float), ('m33', c_float), ('m34', c_float), ('m41', c_float), ('m42', c_float), ('m43', c_float), ('m44', c_float)]


RGBA = namedtuple('RGBA', 'red green blue alpha')

Size = namedtuple('Size', 'width height')

def getCStructValuesAsList(aCStruct): 
    fieldList = [aField[0] for aField in aCStruct._fields_]
    return [getattr(aCStruct, aField) for aField in fieldList]
    
def vector2Make(iter):
  return Vector2._make(iter)

def vector3Make(iter):
  return Vector3._make(iter)
  
def quaternionMake(iter):
  return Quaternion._make(iter)
  
def vector4Make(iter):
  return Vector4._make(iter)
  
def matrix4Make(iter):
  return Matrix4._make(iter)
  
def RGBAMake(color):
  r, g, b, a = parse_color(color)
  return RGBA(r, g, b, a)
  
class BoundingVolume:
  def setBoundingBox(self, minMax):
    (minV, maxV) = minMax
    bbox_min, bbox_max = SCNVector3(), SCNVector3()
    bbox_min.x, bbox_min.y, bbox_min.z = minV[0], minV[1], minV[2]
    bbox_max.x, bbox_max.y, bbox_max.z = maxV[0], maxV[1], maxV[2]   
    self.ID.setBoundingBoxMin_max_(byref(bbox_min), byref(bbox_max), restype=None, argtypes=[POINTER(SCNVector3), POINTER(SCNVector3)])   
  def getBoundingBox(self):
    bbox_min, bbox_max = SCNVector3(), SCNVector3()
    retFlag = self.ID.getBoundingBoxMin_max_(byref(bbox_min), byref(bbox_max), restype=c_bool, argtypes=[POINTER(SCNVector3), POINTER(SCNVector3)])  
    if retFlag:
      return (vector3Make(getCStructValuesAsList(bbox_min)), vector3Make(getCStructValuesAsList(bbox_max)))
    else:
      return None
  def getBoundingBoxMin(self):
    return self.getBoundingBox(self)
  boundingBox = property(getBoundingBox, setBoundingBox)
  
  def getBoundingSphere(self):
    center = SCNVector3()
    radius = c_double(0.0)
    retFlag = self.ID.getBoundingSphereCenter_radius_(byref(center), byref(radius), restype=c_bool, argtypes=[POINTER(SCNVector3), POINTER(c_double)])  
    if retFlag:
      return (vector3Make(getCStructValuesAsList(center)), float(radius.value))
    else:
      return None
  boundingSphere = property(getBoundingSphere, None)
  
class _NoneClass:
  ID = None
nil = _NoneClass()
null = nil
Nil = nil
Null = nil

_CInstCache = dict()

def printCache():
  print('_CInstCache')
  for anItem in list(_CInstCache.items()):
    print('-----', '\n', anItem)
  print('&&&&&&&&&END')
  
def cacheSize():
  return len(_CInstCache)
  
def clearCache():
  _CInstCache.clear()
  
class CInst:
  def setID(self, aCInst):
    self._ID = aCInst
    _CInstCache[aCInst] = self
  def getID(self):
    return self._ID
  ID = property(getID, setID)
  
  @classmethod
  def outof(cls, fromC):
    if fromC is None:
      return nil
    elif fromC in _CInstCache:
      return _CInstCache[fromC]
    else:
      try:
        return cls.subclassOutof(ID=fromC)
      except AttributeError:
        return cls(ID=fromC)
    
  def __str__(self):
    return 'CInst instance with ' + str(self.ID)
    
    
class CInst_NoCache:
  def setID(self, aCInst):
    self._ID = aCInst
  def getID(self):
    return self._ID
  ID = property(getID, setID)
  
  @classmethod
  def outof(cls, fromC):
    if fromC is None:
      return nil
    else:
      try:
        return cls.subclassOutof(ID=fromC)
      except AttributeError:
        return cls(ID=fromC)
    
  def __str__(self):
    return 'CInst_NoCache instance with ' + str(self.ID)
    

def contentFromPy(aPContent):
  def isImage(aPContent):
    return isinstance(aPContent, Image)
  def isImageArray(aPContent):
    if isinstance(aPContent, Iterable):
      for aPContentElement in aPContent:
        if not isImage(aPContentElement): return False
      return True
    return False
  def isNumber(aPContent):
    return isinstance(aPContent, float) or isinstance(aPContent, int)
  def isURL(aPContent):
    if isinstance(aPContent, str):
      if ' ' in aPContent: return False
      if len(aPContent) > 8 or ':' in aPContent or '/' in aPContent or '.' in aPContent: return True
    return False
  def isColor(aPContent):
    try:
      r, g, b, a = parse_color(aPContent)
      return True
    except:
      return False
       
  if isImage(aPContent):
    aPng = aPContent.to_png()
    return ObjCClass('UIImage').imageWithData_(aPng)
  elif isImageArray(aPContent):
    imageList = []
    for anImage in aPContent:
      aPng = anImage.to_png()
      imageList.append(ObjCClass('UIImage').imageWithData_(aPng))
    return imageList
  elif isNumber(aPContent):
    return ns(aPContent)
  elif isURL(aPContent):
    return nsurl(aPContent)
  elif isColor(aPContent):
    r, g, b, a = parse_color(aPContent) #parse_color accepts anything, might result in random colors
    return UIColor.color(red=r, green=g, blue=b, alpha=a)
  else:
    return aPContent

def contentFromC(aCContent):
  if aCContent is None: return None
  elif aCContent.isKindOfClass(UIColor):
    return RGBA(aCContent.red(), aCContent.green(), aCContent.blue(), aCContent.alpha())
  elif aCContent.isKindOfClass(ObjCClass('UIImage')):
    c.UIImagePNGRepresentation.argtypes = [c_void_p]
    c.UIImagePNGRepresentation.restype = c_void_p
    data = ObjCInstance(c.UIImagePNGRepresentation(aCContent.ptr))
    return Image.from_data(nsdata_to_bytes(data),2.0)
  elif aCContent.isKindOfClass(NSArray):
    if aCContent.objectAtIndex(0).isKindOfClass(ObjCClass('UIImage')):
      imageArray = []
      c.UIImagePNGRepresentation.argtypes = [c_void_p]
      c.UIImagePNGRepresentation.restype = c_void_p
      for i in range(aCContent.count()):
        aCImg = aCContent.objectAtIndex(i)
        if aCImg.isKindOfClass(ObjCClass('UIImage')):
          data = ObjCInstance(c.UIImagePNGRepresentation(aCImg.ptr))
          imageArray.append(Image.from_data(nsdata_to_bytes(data),2.0))
      return imageArray
    elif aCContent.isKindOfClass(NSURL): return str(aCContent.absoluteString())
    else: pass
  return aCContent
