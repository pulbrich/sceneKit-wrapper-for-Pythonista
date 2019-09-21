'''constraints modul, to be included in sceneKit'''

from collections import OrderedDict, Iterable

import sceneKit
from .sceneKitEnv import *
from .sceneKitNode import *

class BillboardAxis(Flag):
  X = (0x1 << 0)
  Y = (0x1 << 1)
  Z = (0x1 << 2)
  All = X | Y | Z
  SCNBillboardAxisX = (0x1 << 0)
  SCNBillboardAxisY = (0x1 << 1)
  SCNBillboardAxisZ = (0x1 << 2)
  SCNBillboardAxisAll = X | Y | Z


class Constraint(CInst):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = None
      
  @classmethod
  def subclassOutof(cls, ID=None):
    desc = str(ID.description())
    kind = desc[4:desc.index(':')]
    if kind == 'BillboardConstraint':
      return BillboardConstraint(ID=ID)
    elif kind == 'LookAtConstraint':
      return LookAtConstraint(ID=ID)
    elif kind == 'DistanceConstraint':
      return DistanceConstraint(ID=ID)
    elif kind == 'AvoidOccluderConstraint':
      return AvoidOccluderConstraint(ID=ID)
    elif kind == 'AccelerationConstraint':
      return AccelerationConstraint(ID=ID)
    elif kind == 'IKConstraint':
      return IKConstraint(ID=ID)
    elif kind == 'ReplicatorConstraint':
      return ReplicatorConstraint(ID=ID)
    else:
      return cls(ID=ID)

  def setInfluenceFactor(self, anInfluenceFactor):
    self.ID.setInfluenceFactor(anInfluenceFactor)    
  def getInfluenceFactor(self):
    return self.ID.influenceFactor()
  influenceFactor = property(getInfluenceFactor, setInfluenceFactor)
  
  def setEnabled(self, aBool):
    self.ID.setEnabled(aBool)    
  def getEnabled(self):
    return self.ID.enabled()
  enabled = property(getEnabled, setEnabled)
  
  def setIncremental(self, aBool):
    self.ID.setIncremental(aBool)    
  def getIncremental(self):
    return self.ID.incremental()
  incremental = property(getIncremental, setIncremental)
  
class _Target:
  def setTarget(self, aTargetNode):
    self.ID.setTarget(aTargetNode.ID)
  def getTarget(self):
    return sceneKit.Node.outof(self.ID.target())
  target = property(getTarget, setTarget)
  
class BillboardConstraint(Constraint):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNBillboardConstraint.billboardConstraint()
      
  @classmethod
  def billboardConstraint(cls):
    return cls()
 
  def setFreeAxes(self, axes):
    if not isinstance(axes, Iterable):
      axes = [axes]
    mask = 0
    for anAxis in axes:
      mask = mask | anAxis.value
    self.ID.setFreeAxes(mask)
  def getFreeAxes(self):
    mask = self.ID.freeAxes()
    axes = []
    for anAxis in BillboardAxis:
      if (mask & anAxis.value) != 0: axes.append(anAxis)
    if len(axes) == 4: axes = [BillboardAxis.All]
    return tuple(axes)
  freeAxes = property(getFreeAxes, setFreeAxes)
    
class LookAtConstraint(Constraint, _Target):
  def __init__(self, target=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNLookAtConstraint.lookAtConstraintWithTarget_(target.ID)
    
  @classmethod
  def lookAtConstraintWithTarget(cls, target=None):
    return cls(target=target)
    
  def setGimbalLockEnabled(self, aBool):
    self.ID.setGimbalLockEnabled(aBool)    
  def getGimbalLockEnabled(self):
    return self.ID.gimbalLockEnabled()
  gimbalLockEnabled = property(getGimbalLockEnabled, setGimbalLockEnabled)
  
  def setLocalFront(self, aLocalFront):
    self.ID.setLocalFront(vector3Make(aLocalFront))
  def getLocalFront(self):
    front = self.ID.localFront()
    return Vector3(front.a, front.b, front.c)
  localFront = property(getLocalFront, setLocalFront)
  
  def setTargetOffset(self, aTargetOffset):
    self.ID.setTargetOffset(vector3Make(aTargetOffset))
  def getTargetOffset(self):
    offset = self.ID.targetOffset()
    return Vector3(offset.a, offset.b, offset.c)
  targetOffset = property(getTargetOffset, setTargetOffset)
  
  def setWorldUp(self, aWorldUp):
    self.ID.setWorldUp(vector3Make(aWorldUp))
  def getWorldUp(self):
    up = self.ID.worldUp()
    return Vector3(up.a, up.b, up.c)
  worldUp = property(getWorldUp, setWorldUp)
  
class DistanceConstraint(Constraint, _Target):
  def __init__(self, target=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNDistanceConstraint.distanceConstraintWithTarget_(target.ID)
      
  @classmethod
  def distanceConstraintWithTarget(cls, target=None):
    return cls(target=target)
    
  def setMaximumDistance(self, aMaximumDistance):
    self.ID.setMaximumDistance(aMaximumDistance)    
  def getMaximumDistance(self):
    return self.ID.maximumDistance()
  maximumDistance = property(getMaximumDistance, setMaximumDistance)
  
  def setMinimumDistance(self, aMinimumDistance):
    self.ID.setMinimumDistance(aMinimumDistance)    
  def getMinimumDistance(self):
    return self.ID.minimumDistance()
  minimumDistance = property(getMinimumDistance, setMinimumDistance)
  
class AvoidOccluderConstraint(Constraint, _Target):
  def __init__(self, target=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNAvoidOccluderConstraint.avoidOccluderConstraintWithTarget_(target.ID)
      
  @classmethod
  def avoidOccluderConstraintWithTarget(cls, target=None):
    return cls(target=target)
    
  def setBias(self, aBias):
    self.ID.setBias(aBias)    
  def getBias(self):
    return self.ID.bias()
  bias = property(getBias, setBias)
  
  def setOccluderCategoryBitMask(self, aBitMask):
    self.ID.setOccluderCategoryBitMask(aBitMask)    
  def getOccluderCategoryBitMask(self):
    return self.ID.occluderCategoryBitMask()
  occluderCategoryBitMask = property(getOccluderCategoryBitMask, setOccluderCategoryBitMask)
  
  def setDelegate(self, aDelegate):
    anAvoidOccluderConstraintDelegate = AvoidOccluderConstraintDelegate(aDelegate)
    self.ID.setDelegate_(anAvoidOccluderConstraintDelegate.ID)
  def getDelegate(self):
    anAvoidOccluderConstraintDelegate = sceneKit.AvoidOccluderConstraintDelegate.outof(self.ID.delegate())
    return anAvoidOccluderConstraintDelegate.delegate if anAvoidOccluderConstraintDelegate is not None else None
  delegate = property(getDelegate, setDelegate)
  
class AccelerationConstraint(Constraint):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNAccelerationConstraint.accelerationConstraint()
      
  @classmethod
  def accelerationConstraint(cls):
    return cls()
    
  def setDamping(self, aDamping):
    self.ID.setDamping(aDamping)    
  def getDamping(self):
    return self.ID.damping()
  damping = property(getDamping, setDamping)
  
  def setDecelerationDistance(self, aDist):
    self.ID.setDecelerationDistance(aDist)    
  def getDecelerationDistance(self):
    return self.ID.decelerationDistance()
  decelerationDistance = property(getDecelerationDistance, setDecelerationDistance)
  
  def setMaximumLinearAcceleration(self, aMaximumLinearAcceleration):
    self.ID.setMaximumLinearAcceleration(aMaximumLinearAcceleration)    
  def getMaximumLinearAcceleration(self):
    return self.ID.maximumLinearAcceleration()
  maximumLinearAcceleration = property(getMaximumLinearAcceleration, setMaximumLinearAcceleration)
  
  def setMaximumLinearVelocity(self, aMaximumLinearVelocity):
    self.ID.setMaximumLinearVelocity(aMaximumLinearVelocity)    
  def getMaximumLinearVelocity(self):
    return self.ID.maximumLinearVelocity()
  maximumLinearVelocity = property(getMaximumLinearVelocity, setMaximumLinearVelocity)
  
class SliderConstraint(Constraint):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNSliderConstraint.sliderConstraint()
      
  @classmethod
  def sliderConstraint(cls):
    return cls()
    
  def setCollisionCategoryBitMask(self, aMask):
    self.ID.setCollisionCategoryBitMask(aMask)    
  def getCollisionCategoryBitMask(self):
    return self.ID.collisionCategoryBitMask()
  collisionCategoryBitMask = property(getCollisionCategoryBitMask, setCollisionCategoryBitMask)
  
  def setOffset(self, anOffset):
    self.ID.setOffset(vector3Make(anOffset))
  def getOffset(self):
    offset = self.ID.offset()
    return Vector3(offset.a, offset.b, offset.c)
  offset = property(getOffset, setOffset)
  
  def setRadius(self, aRadius):
    self.ID.setRadius(aRadius)    
  def getRadius(self):
    return self.ID.radius()
  radius = property(getRadius, setRadius)
  
class ReplicatorConstraint(Constraint, _Target):
  def __init__(self, target=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNReplicatorConstraint.replicatorConstraintWithTarget_(target.ID)
      
  @classmethod
  def replicatorConstraintWithTarget(cls, target=None):
    return cls(target=target)
    
  def setOrientationOffset(self, anOrientationOffset):
    self.ID.setOrientationOffset(quaternionMake(anOrientationOffset))
  def getOrientationOffset(self):
    anOffset = self.ID.orientationOffset()
    return Quaternion(anOffset.a, anOffset.b, anOffset.c, anOffset.d)
  orientationOffset = property(getOrientationOffset, setOrientationOffset)
  
  def setPositionOffset(self, anOffset):
    self.ID.setPositionOffset(vector3Make(anOffset))
  def getPositionOffset(self):
    offset = self.ID.positionOffset()
    return Vector3(offset.a, offset.b, offset.c)
  positionOffset = property(getPositionOffset, setPositionOffset)
  
  def setReplicatesOrientation(self, aBool):
    self.ID.setReplicatesOrientation(aBool)    
  def getReplicatesOrientation(self):
    return self.ID.replicatesOrientation()
  replicatesOrientation = property(getReplicatesOrientation, setReplicatesOrientation)
  
  def setReplicatesPosition(self, aBool):
    self.ID.setReplicatesPosition(aBool)    
  def getReplicatesPosition(self):
    return self.ID.replicatesPosition()
  replicatesPosition = property(getReplicatesPosition, setReplicatesPosition)
  
  def setReplicatesScale(self, aBool):
    self.ID.setReplicatesScale(aBool)    
  def getReplicatesScale(self):
    return self.ID.replicatesScale()
  replicatesScale = property(getReplicatesScale, setReplicatesScale)
  
  def setScaleOffset(self, aScaleOffset):
    self.ID.setScaleOffset(vector3Make(aScaleOffset))
  def getScaleOffset(self):
    anOffset = self.ID.scaleOffset()
    return Vector3(offset.a, offset.b, offset.c)
  scaleOffset = property(getScaleOffset, setScaleOffset)
  
class IKConstraint(Constraint):
  def __init__(self, chainRootNode=None, ID=None):
    if ID is not None:
      self.ID = ID
    elif chainRootNode is not None:
      self.ID = SCNIKConstraint.inverseKinematicsConstraintWithChainRootNode_(chainRootNode.ID)
    else:
      self.ID = SCNIKConstraint.alloc()
      
  @classmethod
  def inverseKinematicsConstraintWithChainRootNode(cls, chainRootNode=None):
    return cls(chainRootNode=chainRootNode)
    
  def initWithChainRootNode(self, chainRootNode=None):
    self.ID.initWithChainRootNode_(chainRootNode.ID)
    
  def setChainRootNode(self, aChainRootNode):
    self.ID.setChainRootNode(aChainRootNode.ID)
  def getChainRootNode(self):
    return sceneKit.Node.outof(self.ID.chainRootNode())
  chainRootNode = property(getChainRootNode, setChainRootNode)

  def setMaxAllowedRotationAngleForJoint(self, aNode):
    self.ID.setMaxAllowedRotationAngleForJoint(aNode.ID)    
  def getMaxAllowedRotationAngleForJoint(self):
    return self.ID.maxAllowedRotationAngleForJoint()
  maxAllowedRotationAngleForJoint = property(getMaxAllowedRotationAngleForJoint, setMaxAllowedRotationAngleForJoint)
  
  def setTargetPosition(self, aTargetPosition):
    self.ID.setTargetPosition(vector3Make(aTargetPosition))
  def getTargetPosition(self):
    aPos = self.ID.targetPosition()
    return Vector3(aPos.a, aPos.b, aPos.c)
  targetPosition = property(getTargetPosition, setTargetPosition)
  
def avoidOccluderConstraint_didAvoidOccluder_forNode_(_self, _cmd, constraint, occluder, node):
  anAvoidOccluderConstraintDelegate = sceneKit.AvoidOccluderConstraintDelegate.outof(ObjCInstance(_self))
  if anAvoidOccluderConstraintDelegate.methods[0]:
    constraint = sceneKit.AvoidOccluderConstraint.outof(ObjCInstance(constraint))
    occluder = sceneKit.Node.outof(ObjCInstance(occluder))
    node = sceneKit.Node.outof(ObjCInstance(node))
    anAvoidOccluderConstraintDelegate.delegate.didAvoidOccluder(constraint, occluder, node)
    
def avoidOccluderConstraint_shouldAvoidOccluder_forNode_(_self, _cmd, constraint, occluder, node):
  anAvoidOccluderConstraintDelegate = sceneKit.AvoidOccluderConstraintDelegate.outof(ObjCInstance(_self))
  if anAvoidOccluderConstraintDelegate.methods[1]:
    constraint = sceneKit.AvoidOccluderConstraint.outof(ObjCInstance(constraint))
    occluder = sceneKit.Node.outof(ObjCInstance(occluder))
    node = sceneKit.Node.outof(ObjCInstance(node))
    ret = anAvoidOccluderConstraintDelegate.delegate.shouldAvoidOccluder(constraint, occluder, node)
    return ret if ret is not None else False

class AvoidOccluderConstraintDelegate(CInst):
  _actions = ('didAvoidOccluder', 'shouldAvoidOccluder')
  _newCClassName = 'SCNPYAvoidOccluderConstraintDelegateClass'
  _cMethodList = [avoidOccluderConstraint_didAvoidOccluder_forNode_, avoidOccluderConstraint_shouldAvoidOccluder_forNode_]
  avoidOccluderConstraint_didAvoidOccluder_forNode_.restype = None
  avoidOccluderConstraint_didAvoidOccluder_forNode_.argtypes = [c_void_p, c_void_p, c_void_p]
  avoidOccluderConstraint_shouldAvoidOccluder_forNode_.restype = c_bool
  avoidOccluderConstraint_shouldAvoidOccluder_forNode_.argtypes = [c_void_p, c_void_p, c_void_p]
  _protocols =['SCNAvoidOccluderConstraintDelegate']
  DelegateCClass = create_objc_class(_newCClassName, NSObject, methods=_cMethodList, protocols=_protocols)
  
  def __init__(self, aDelegate=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.delegate = aDelegate
      self.methods = [callable(_a) for _a in [getattr(aDelegate, anAction, False) for anAction in AvoidOccluderConstraintDelegate._actions]]
      self.ID = AvoidOccluderConstraintDelegate.DelegateCClass.alloc().init().autorelease()
  
