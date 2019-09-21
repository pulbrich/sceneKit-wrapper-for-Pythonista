'''
sceneKit Physics module for sceneKit
includes 
'''

from ctypes import *
from objc_util import *

import sceneKit
from .sceneKitEnv import *
from .sceneKitNode import *
from .sceneKitGeometry import *
from .sceneKitSceneRenderer import *

class PhysicsBodyType(Enum):
  Static = 0
  Dynamic = 1
  Kinematic = 2
  SCNPhysicsBodyTypeStatic = 0
  SCNPhysicsBodyTypeDynamic = 1
  SCNPhysicsBodyTypeKinematic = 2
  
_physicsShapeOptions = []
for anOption in ['SCNPhysicsShapeOptionCollisionMargin', 'SCNPhysicsShapeKeepAsCompoundKey', 'SCNPhysicsShapeScaleKey', 'SCNPhysicsShapeTypeKey', 'SCNPhysicsShapeTypeBoundingBox', 'SCNPhysicsShapeTypeConcavePolyhedron', 'SCNPhysicsShapeTypeConvexHull']:
  _physicsShapeOptions.append(str(ObjCInstance(c_void_p.in_dll(c, anOption))))
_physicsShapeOptions = tuple(_physicsShapeOptions)
  
SCNPhysicsShapeOptionCollisionMargin, SCNPhysicsShapeKeepAsCompoundKey, SCNPhysicsShapeScaleKey, SCNPhysicsShapeTypeKey, SCNPhysicsShapeTypeBoundingBox, SCNPhysicsShapeTypeConcavePolyhedron, SCNPhysicsShapeTypeConvexHull = _physicsShapeOptions
PhysicsShapeOptionCollisionMargin, PhysicsShapeKeepAsCompoundKey, PhysicsShapeScaleKey, PhysicsShapeTypeKey, PhysicsShapeTypeBoundingBox, PhysicsShapeTypeConcavePolyhedron, PhysicsShapeTypeConvexHull = _physicsShapeOptions

_physicsTestOptions = []
for anOption in ['SCNPhysicsTestBackfaceCullingKey', 'SCNPhysicsTestCollisionBitMaskKey', 'SCNPhysicsTestSearchModeKey', 'SCNPhysicsTestSearchModeAll', 'SCNPhysicsTestSearchModeAny', 'SCNPhysicsTestSearchModeClosest']:
  _physicsTestOptions.append(str(ObjCInstance(c_void_p.in_dll(c, anOption))))
_physicsTestOptions = tuple(_physicsTestOptions)

SCNPhysicsTestBackfaceCullingKey, SCNPhysicsTestCollisionBitMaskKey, SCNPhysicsTestSearchModeKey, SCNPhysicsTestSearchModeAll, SCNPhysicsTestSearchModeAny, SCNPhysicsTestSearchModeClosest = _physicsTestOptions
PhysicsTestBackfaceCullingKey, PhysicsTestCollisionBitMaskKey, PhysicsTestSearchModeKey, PhysicsTestSearchModeAll, PhysicsTestSearchModeAny, PhysicsTestSearchModeClosest = _physicsTestOptions

class PhysicsCollisionCategory(Enum):
  Default = (1 << 0)
  Static = (1 << 1)
  All = (~0)
  SCNPhysicsCollisionCategoryDefault = (1 << 0)
  SCNPhysicsCollisionCategoryStatic = (1 << 1)
  SCNPhysicsCollisionCategoryAll = (~0)
  
class PhysicsFieldScope(Enum):
  InsideExtent = 0
  OutsideExtent = 1
  SCNPhysicsFieldScopeInsideExtent = 0
  SCNPhysicsFieldScopeOutsideExtent = 1
  
class PhysicsWorld(CInst_NoCache):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      return None
      
  def setGravity(self, aVector3):
    self.ID.setGravity_(vector3Make(aVector3))
  def getGravity(self):
    grav = self.ID.gravity()
    return Vector3(grav.a, grav.b, grav.c)
  gravity = property(getGravity, setGravity)
  
  def setSpeed(self, aSpeed):
    self.ID.setSpeed_(aSpeed)    
  def getSpeed(self):
    return self.ID.speed()
  speed = property(getSpeed, setSpeed)
  
  def setTimeStep(self, aTimeStep):
    self.ID.setTimeStep_(aTimeStep)    
  def getTimeStep(self):
    return self.ID.timeStep()
  timeStep = property(getTimeStep, setTimeStep)
  
  def updateCollisionPairs(self):
    self.ID.updateCollisionPairs()
    
  def addBehavior(self, aBehavior):
    self.ID.addBehavior_(aBehavior.ID)
    
  def removeBehavior(self, aBehavior):
    self.ID.removeBehavior_(aBehavior.ID)
    
  def getAllBehaviors(self):
    return tuple([sceneKit.PhysicsBehavior.outof(aBehavior) for aBehavior in self.ID.allBehaviors()])
  allBehaviors = property(getAllBehaviors, None)
  
  def removeAllBehaviors(self):
    self.ID.removeAllBehaviors()
    
  def setContactDelegate(self, aDelegate):
    aPhysicsContactDelegate = PhysicsContactDelegate(aDelegate)
    self.ID.setContactDelegate_(aPhysicsContactDelegate.ID)
  def getContactDelegate(self):
    aPhysicsContactDelegate = sceneKit.PhysicsContactDelegate.outof(self.ID.contactDelegate())
    return aPhysicsContactDelegate.delegate
  contactDelegate = property(getContactDelegate, setContactDelegate)
  
  def contactTestBetween(self, bodyA=None, bodyB=None, options=None):
    contactList = self.ID.contactTestBetweenBody_andBody_options_(bodyA.ID, bodyB.ID, options)
    return tuple([sceneKit.PhysicsContact.outof(aCon) for aCon in contactList])
    
  def contactTest(self, body=None, options=None):
    contactList = self.ID.contactTestWithBody_options_(body.ID, options)
    return tuple([sceneKit.PhysicsContact.outof(aCon) for aCon in contactList])
    
  def rayTestWithSegment(self, origin=None, dest=None, options=None):
    hitList = self.ID.rayTestWithSegmentFromPoint_toPoint_options_(vector3Make(origin), vector3Make(dest), options)
    return tuple([sceneKit.HitTestResult.outof(aHit) for aHit in hitList])
    
  def rayTestWithSegmentFromPoint(self, origin=None, toPoint=None, options=None):
    return self.rayTestWithSegment(origin=origin, dest=toPoint, options=None)
    
  def convexSweepTest(self, shape=None, fromTransform=None, toTransform=None, options=None):
    contactList = self.id.convexSweepTestWithShape_fromTransform_toTransform_options_(shape.ID, matrix4Make(fromTransform), matrix4Make(toTransform), options)
    return tuple([sceneKit.PhysicsContact.outof(aCon) for aCon in contactList])
        
  def convexSweepTestWithShape(self, shape=None, fromTransform=None, toTransform=None, options=None):
    return self.convexSweepTest(shape=shape, fromTransform=fromTransform, toTransform=toTransform, options=options)
    
class PhysicsField(CInst):
  def __init__(self, dragField=None, vortexField=None, radialGravityField=None, linearGravityField=None, noiseField=None, turbulenceField=None, springField=None, electricField=None, magneticField=None, smoothness=None, speed=None, block=None, ID=None):
    if ID is not None:
      self.ID = ID
    elif dragField is not None:
      self.ID = SCNPhysicsField.dragField()
    elif vortexField is not None:
      self.ID = SCNPhysicsField.vortexField()
    elif radialGravityField is not None:
      self.ID = SCNPhysicsField.radialGravityField()
      self.ID.setFalloffExponent_(2.0)
    elif linearGravityField is not None:
      self.ID = SCNPhysicsField.linearGravityField()
    elif noiseField is not None:
      self.ID = SCNPhysicsField.noiseFieldWithSmoothness_animationSpeed_(smoothness, speed)
    elif turbulenceField is not None:
      self.ID = SCNPhysicsField.turbulenceFieldWithSmoothness_animationSpeed_(smoothness, speed)
    elif springField is not None:
      self.ID = SCNPhysicsField.springField()
      self.ID.setFalloffExponent_(1.0)
    elif electricField is not None:
      self.ID = SCNPhysicsField.electricField()
      self.ID.setFalloffExponent_(2.0)
    elif magneticField is not None:
      self.ID = SCNPhysicsField.magneticField()
      self.ID.setFalloffExponent_(2.0)
    elif block is not None:
      self.fieldForceEvaluatorBlock = FieldForceEvaluatorBlock(block)
      self.ID = SCNPhysicsField.customFieldWithEvaluationBlock_(self.fieldForceEvaluatorBlock.blockCode)
    else:
      self.ID = SCNPhysicsField.field()
      
  @classmethod
  def dragField(cls):
    return cls(dragField=True)
    
  @classmethod
  def vortexField(cls):
    return cls(vortexField=True)
    
  @classmethod
  def radialGravityField(cls):
    return cls(radialGravityField=True)
    
  @classmethod
  def linearGravityField(cls):
    return cls(linearGravityField=True)
    
  @classmethod
  def noiseField(cls, smoothness=1.0, speed=0.0):
    return cls(noiseField=True, smoothness=smoothness, speed=speed)
    
  @classmethod
  def noiseFieldWithSmoothness(cls, smoothness=1.0, animationSpeed=0.0):
    return cls(noiseField=True, smoothness=smoothness, speed=animationSpeed)
    
  @classmethod
  def turbulenceField(cls, smoothness=1.0, speed=0.0):
    return cls(turbulenceField=True, smoothness=smoothness, speed=speed)
    
  @classmethod
  def turbulenceFieldWithSmoothness(cls, smoothness=1.0, animationSpeed=0.0):
    return cls(turbulenceField=True, smoothness=smoothness, speed=animationSpeed)
    
  @classmethod
  def springField(cls):
    return cls(springField=True)
    
  @classmethod
  def electricField(cls):
    return cls(electricField=True)
    
  @classmethod
  def magneticField(cls):
    return cls(magneticField=True)
    
  @classmethod
  def customFieldWithEvaluationBlock(cls, block=None):
    return cls(block=block)
    
  def setHalfExtent(self, aVector3):
    self.ID.setHalfExtent_(vector3Make(aVector3))
  def getHalfExtent(self):
    ext = self.ID.halfExtent()
    return Vector3(ext.a, ext.b, ext.c)
  halfExtent = property(getHalfExtent, setHalfExtent)
  
  def setScope(self, aScope):
    self.ID.setScope_(aScope.value)    
  def getScope(self):
    return PhysicsFieldScope(self.ID.scope())
  scope = property(getScope, setScope)
  
  def setUsesEllipsoidalExtent(self, aBool):
    self.ID.setUsesEllipsoidalExtent_(aBool)    
  def getUsesEllipsoidalExtent(self):
    return self.ID.usesEllipsoidalExtent()
  usesEllipsoidalExtent = property(getUsesEllipsoidalExtent, setUsesEllipsoidalExtent)
  
  def setOffset(self, anOffset):
    self.ID.setOffset_(vector3Make(anOffset))
  def getOffset(self):
    off = self.ID.offset()
    return Vector3(off.a, off.b, off.c)
  offset = property(getOffset, setOffset)

  def setDirection(self, aDirection):
    self.ID.setDirection_(vector3Make(aDirection))
  def getDirection(self):
    dire = self.ID.direction()
    return Vector3(dire.a, dire.b, dire.c)
  direction = property(getDirection, setDirection)
  
  def setStrength(self, aStrength):
    self.ID.setStrength_(aStrength)    
  def getStrength(self):
    return self.ID.strength()
  strength = property(getStrength, setStrength)
  
  def setFalloffExponent(self, aFalloffExponent):
    self.ID.setFalloffExponent_(aFalloffExponent)    
  def getFalloffExponent(self):
    return self.ID.falloffExponent()
  falloffExponent = property(getFalloffExponent, setFalloffExponent)
  
  def setMinimumDistance(self, aMinimumDistance):
    self.ID.setMinimumDistance_(aMinimumDistance)    
  def getMinimumDistance(self):
    return self.ID.minimumDistance()
  minimumDistance = property(getMinimumDistance, setMinimumDistance)
  
  def setActive(self, aBool):
    self.ID.setActive_(aBool)    
  def isActive(self):
    return self.ID.active()
  active = property(isActive, setActive)
  
  def setExclusive(self, aBool):
    self.ID.setExclusive_(aBool)    
  def isExclusive(self):
    return self.ID.exclusive()
  exclusive = property(isExclusive, setExclusive)
  
class FieldForceEvaluatorBlock:
  def __init__(self, block):
    try:
      self.blockCode = ObjCBlock(self.blockInterface, restype=SCNVector3, argtypes=[c_void_p, SCNVector3, SCNVector3, c_float, c_float, c_double])
    except TypeError:
      self.blockCode = ObjCBlock(self.blockInterfaceLimited, restype=c_float, argtypes=[c_void_p, SCNVector3, SCNVector3, c_float, c_float, c_double])
    self.pCode = block
      
  def blockInterface(self, _cmd, SCNPosition, SCNVelocity, mass, charge, time):
    position = vector3Make(getCStructValuesAsList(SCNPosition))
    velocity = vector3Make(getCStructValuesAsList(SCNVelocity))
    ret = self.pCode(position, velocity, mass, charge, time)
    return SCNVector3(ret.x, ret.y, ret.z)
    
  def blockInterfaceLimited(self, _cmd, SCNPosition, SCNVelocity, mass, charge, time):
    position = vector3Make(getCStructValuesAsList(SCNPosition))
    velocity = vector3Make(getCStructValuesAsList(SCNVelocity))
    ret = self.pCode(position, velocity, mass, charge, time)
    return ret.x


class PhysicsBody(CInst):
  def __init__(self, bodyType=None, shape=None, ID=None):
    if ID is not None:
      self.ID = ID
    elif bodyType is not None:
      if shape is not None:
        shape = shape.ID
      self.ID = SCNPhysicsBody.bodyWithType_shape_(bodyType.value, shape)
    
  @classmethod
  def bodyWithType(cls, bodyType=None, shape=None):
    return cls(bodyType=bodyType, shape=shape)
    
  @classmethod
  def staticBody(cls):
    return cls(PhysicsBodyType.Static, None)
    
  @classmethod
  def dynamicBody(cls):
    return cls(PhysicsBodyType.Dynamic, None)
    
  @classmethod
  def kinematicBody(cls):
    return cls(PhysicsBodyType.Kinematic, None)
    
  def setPhysicsShape(self, aPhysicsShape):
    self.ID.setPhysicsShape_(aPhysicsShape.ID)    
  def getPhysicsShape(self):
    return sceneKit.PhysicsShape.outof(self.ID.physicsShape())
  physicsShape = property(getPhysicsShape, setPhysicsShape)
  
  def setBodyType(self, aBodyType):
    self.ID.setType_(aBodyType.value)    
  def getBodyType(self):
    return PhysicsBodyType(self.ID.type())
  bodyType = property(getBodyType, setBodyType)
  
  def setVelocityFactor(self, aFactor):
    self.ID.setVelocityFactor_(vector3Make(aFactor))
  def getVelocityFactor(self):
    vel = self.ID.velocityFactor()
    return Vector3(vel.a, vel.b, vel.c)
  velocityFactor = property(getVelocityFactor, setVelocityFactor)
  
  def setAngularVelocityFactor(self, aFactor):
    self.ID.setAngularVelocityFactor_(vector3Make(aFactor))
  def getAngularVelocityFactor(self):
    vel = self.ID.angularVelocityFactor()
    return Vector3(vel.a, vel.b, vel.c)
  angularVelocityFactor = property(getAngularVelocityFactor, setAngularVelocityFactor)
  
  def setAffectedByGravity(self, aBool):
    self.ID.setAffectedByGravity_(aBool)    
  def isAffectedByGravity(self):
    return self.ID.affectedByGravity()
  affectedByGravity = property(isAffectedByGravity, setAffectedByGravity)
  
  def setMass(self, aMass):
    self.ID.setMass_(aMass)    
  def getMass(self):
    return self.ID.mass()
  mass = property(getMass, setMass)
  
  def setCharge(self, aCharge):
    self.ID.setCharge_(aCharge)    
  def getCharge(self):
    return self.ID.charge()
  charge = property(getCharge, setCharge)
  
  def setFriction(self, aFriction):
    self.ID.setFriction_(aFriction)    
  def getFriction(self):
    return self.ID.friction()
  friction = property(getFriction, setFriction)

  def setRollingFriction(self, aRollingFriction):
    self.ID.setRollingFriction_(aRollingFriction)    
  def getRollingFriction(self):
    return self.ID.rollingFriction()
  rollingFriction = property(getRollingFriction, setRollingFriction)
  
  def setRestitution(self, aRestitution):
    self.ID.setRestitution_(aRestitution)    
  def getRestitution(self):
    return self.ID.restitution()
  restitution = property(getRestitution, setRestitution)
  
  def setDamping(self, aDamping):
    self.ID.setDamping_(aDamping)    
  def getDamping(self):
    return self.ID.damping()
  damping = property(getDamping, setDamping)
  
  def setAngularDamping(self, aDamping):
    self.ID.setAngularDamping_(aDamping)    
  def getAngularDamping(self):
    return self.ID.angularDamping()
  angularDamping = property(getAngularDamping, setAngularDamping)
  
  def setMomentOfInertia(self, aVector3):
    self.ID.setMomentOfInertia_(vector3Make(aVector3))
  def getMomentOfInertia(self):
    mom = self.ID.momentOfInertia()
    return Vector3(mom.a, mom.b, mom.c)
  momentOfInertia = property(getMomentOfInertia, setMomentOfInertia)
  
  def setUsesDefaultMomentOfInertia(self, aBool):
    self.ID.setUsesDefaultMomentOfInertia_(aBool)    
  def getUsesDefaultMomentOfInertia(self):
    return self.ID.usesDefaultMomentOfInertia()
  usesDefaultMomentOfInertia = property(getUsesDefaultMomentOfInertia, setUsesDefaultMomentOfInertia)
  
  def setCenterOfMassOffset(self, anOffset):
    self.ID.setCenterOfMassOffset_(vector3Make(anOffset))
  def getCenterOfMassOffset(self):
    cen = self.ID.centerOfMassOffset()
    return Vector3(cen.a, cen.b, cen.c)
  centerOfMassOffset = property(getCenterOfMassOffset, setCenterOfMassOffset)
  
  def setCategoryBitMask(self, aMask):
    if isinstance(aMask, PhysicsCollisionCategory):
      aMask = aMask.value
    self.ID.setCategoryBitMask_(aMask)    
  def getCategoryBitMask(self):
    return self.ID.categoryBitMask()
  categoryBitMask = property(getCategoryBitMask, setCategoryBitMask)
  
  def setContactTestBitMask(self, aMask):
    self.ID.setContactTestBitMask_(aMask)    
  def getContactTestBitMask(self):
    return self.ID.contactTestBitMask()
  contactTestBitMask = property(getContactTestBitMask, setContactTestBitMask)
  
  def setCollisionBitMask(self, aMask):
    if isinstance(aMask, PhysicsCollisionCategory):
      aMask = aMask.value
    self.ID.setCollisionBitMask_(aMask)    
  def getCollisionBitMask(self):
    return self.ID.collisionBitMask()
  collisionBitMask = property(getCollisionBitMask, setCollisionBitMask)
  
  def setContinuousCollisionDetectionThreshold(self, aHold):
    self.ID.setContinuousCollisionDetectionThreshold_(aHold)    
  def getContinuousCollisionDetectionThreshold(self):
    return self.ID.continuousCollisionDetectionThreshold()
  continuousCollisionDetectionThreshold = property(getContinuousCollisionDetectionThreshold, setContinuousCollisionDetectionThreshold)

  def applyForce(self, direction=None, position=None, impulse=False, atPosition=None):
    if atPosition is not None: position = atPosition
    if position is True or position is False:
      impulse = position
      position = None
    if position is None:
      self.ID.applyForce_impulse_(vector3Make(direction), impulse)
    else:
      self.ID.applyForce_atPosition_impulse_(vector3Make(direction), vector3Make(position), impulse)
  def applyForceAtPosition(self, direction=None, position=None, impulse=False, atPosition=None):
    self.applyForce(direction=direction, position=position, impulse=impulse, atPosition=atPosition)
    
  def applyTorque(self, torque=None, impulse=False):
    self.ID.applyTorque_impulse_(vector4Make(torque), impulse)
    
  def clearAllForces(self):
    self.ID.clearAllForces()
    
  def setVelocity(self, aVelocity):
    self.ID.setVelocity_(vector3Make(aVelocity))
  def getVelocity(self):
    vel = self.ID.velocity()
    return Vector3(vel.a, vel.b, vel.c)
  velocity = property(getVelocity, setVelocity)
  
  def setAngularVelocity(self, aVelocity):
    self.ID.setAngularVelocity_(vector4Make(aVelocity))
  def getAngularVelocity(self):
    vel = self.ID.angularVelocity()
    return Vector4(vel.a, vel.b, vel.c, vel.d)
  angularVelocity = property(getAngularVelocity, setAngularVelocity)
    
  def getIsResting(self):
    return self.ID.isResting()
  isResting = property(getIsResting, None)
  
  def setResting(self, aBool):
    self.ID.setResting_(aBool)    
  def getResting(self):
    return self.ID.isResting()
  resting = property(getResting, setResting)
  
  def setAllowsResting(self, aBool):
    self.ID.setAllowsResting_(aBool)    
  def getAllowsResting(self):
    return self.ID.allowsResting()
  allowsResting = property(getAllowsResting, setAllowsResting)
  
  def resetTransform(self):
    self.ID.resetTransform()
    
  def setAngularRestingThreshold(self, aHold):
    self.ID.setAngularRestingThreshold_(aHold)    
  def getAngularRestingThreshold(self):
    return self.ID.angularRestingThreshold()
  angularRestingThreshold = property(getAngularRestingThreshold, setAngularRestingThreshold)
  
  def setLinearRestingThreshold(self, aHold):
    self.ID.setLinearRestingThreshold_(aHold)    
  def getLinearRestingThreshold(self):
    return self.ID.linearRestingThreshold()
  linearRestingThreshold = property(getLinearRestingThreshold, setLinearRestingThreshold)
  
class PhysicsBehavior(CInst):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNPhysicsBehavior.alloc().init()
      
  @classmethod
  def subclassOutof(cls, ID=None):
    desc = str(ID.description())
    kind = desc[4:desc.index(':')]
    if kind == 'PhysicsHingeJoint':
      return PhysicsHingeJoint(ID=ID)
    elif kind == 'PhysicsBallSocketJoint':
      return PhysicsBallSocketJoint(ID=ID)
    elif kind == 'PhysicsSliderJoint':
      return PhysicsSliderJoint(ID=ID)
    elif kind == 'PhysicsVehicle':
      return PhysicsVehicle(ID=ID)
    else:
      return cls(ID=ID)
    
class PhysicsHingeJoint(CInst):
  def __init__(self, bodyA=None, axisA=None, anchorA=None, bodyB=None, axisB=None, anchorB=None, ID=None):
    if ID is not None:
      self.ID = ID
    elif bodyB is None:
      self.ID = SCNPhysicsHingeJoint.jointWithBody_axis_anchor_(bodyA.ID, vector3Make(axisA), vector3Make(anchorA))
    else:
      self.ID = SCNPhysicsHingeJoint.jointWithBodyA_axisA_anchorA_bodyB_axisB_anchorB_(bodyA.ID, vector3Make(axisA), vector3Make(anchorA), bodyB.ID, vector3Make(axisB), vector3Make(anchorB))
    
  @classmethod
  def jointWithBody(cls, body=None, axis=None, anchor=None):
    return cls(bodyA=body, axisA=axis, anchorA=anchor)
    
  @classmethod
  def jointWithBodyA(cls, bodyA=None, axisA=None, anchorA=None, bodyB=None, axisB=None, anchorB=None):
    return cls(bodyA=bodyA, axisA=axisA, anchorA=anchorA, bodyB=bodyB, axisB=axisB, anchorB=anchorB)
    
  @classmethod
  def joint(cls, body=None, axis=None, anchor=None, bodyA=None, axisA=None, anchorA=None, bodyB=None, axisB=None, anchorB=None):
    if bodyB is None:
      if bodyA is None:
        return cls(bodyA=body, axisA=axis, anchorA=anchor)
      elif body is None:
        return cls(bodyA=bodyA, axisA=axisA, anchorA=anchorA)
      else:
        return cls(bodyA=body, axisA=axis, anchorA=anchor, bodyB=bodyA, axisB=axisA, anchorB=anchorA)
    elif body is None:
      return cls(bodyA=bodyA, axisA=axisA, anchorA=anchorA, bodyB=bodyB, axisB=axisB, anchorB=anchorB)
    else:
      return cls(bodyA=body, axisA=axis, anchorA=anchor, bodyB=bodyA, axisB=axisA, anchorB=anchorA)
      
  def getBodyA(self):
    return sceneKit.PhysicsBody.outof(self.ID.bodyA())
  bodyA = property(getBodyA, None)
  
  def getAxisA(self):
    ax = self.ID.axisA()
    return Vector3(ax.a, ax.b, ax.c)
  axisA = property(getAxisA, None)
  
  def getAnchorA(self):
    an = self.ID.anchorA()
    return Vector3(an.a, an.b, an.c)
  anchorA = property(getAnchorA, None)
  
  def getBodyB(self):
    return sceneKit.PhysicsBody.outof(self.ID.bodyB())
  bodyB = property(getBodyB, None)
  
  def getAxisB(self):
    ax = self.ID.axisB()
    return Vector3(ax.a, ax.b, ax.c)
  axisB = property(getAxisB, None)
  
  def getAnchorB(self):
    an = self.ID.anchorB()
    return Vector3(an.a, an.b, an.c)
  anchorB = property(getAnchorB, None)
  
class PhysicsSliderJoint(PhysicsHingeJoint):
  def setMinimumLinearLimit(self, aLimit):
    self.ID.setMinimumLinearLimit_(aLimit)    
  def getMinimumLinearLimit(self):
    return self.ID.minimumLinearLimit()
  minimumLinearLimit = property(getMinimumLinearLimit, setMinimumLinearLimit)
  
  def setMaximumLinearLimit(self, aLimit):
    self.ID.setMaximumLinearLimit_(aLimit)    
  def getMaximumLinearLimit(self):
    return self.ID.maximumLinearLimit()
  maximumLinearLimit = property(getMaximumLinearLimit, setMaximumLinearLimit)
  
  def setMinimumAngularLimit(self, aLimit):
    self.ID.setMinimumAngularLimit_(aLimit)    
  def getMinimumAngularLimit(self):
    return self.ID.minimumAngularLimit()
  minimumAngularLimit = property(getMinimumAngularLimit, setMinimumAngularLimit)
  
  def setMaximumAngularLimit(self, aLimit):
    self.ID.setMaximumAngularLimit_(aLimit)    
  def getMaximumAngularLimit(self):
    return self.ID.maximumAngularLimit()
  maximumAngularLimit = property(getMaximumAngularLimit, setMaximumAngularLimit)
  
  def setMotorTargetLinearVelocity(self, aTarget):
    self.ID.setMotorTargetLinearVelocity_(aTarget)    
  def getMotorTargetLinearVelocity(self):
    return self.ID.motorTargetLinearVelocity()
  motorTargetLinearVelocity = property(getMotorTargetLinearVelocity, setMotorTargetLinearVelocity)
  
  def setMotorMaximumForce(self, aForce):
    self.ID.setMotorMaximumForce_(aForce)    
  def getMotorMaximumForce(self):
    return self.ID.motorMaximumForce()
  motorMaximumForce = property(getMotorMaximumForce, setMotorMaximumForce)
  
  def setMotorTargetAngularVelocity(self, aTarget):
    self.ID.setMotorTargetAngularVelocity_(aTarget)    
  def getMotorTargetAngularVelocity(self):
    return self.ID.motorTargetAngularVelocity()
  motorTargetAngularVelocity = property(getMotorTargetAngularVelocity, setMotorTargetAngularVelocity)
  
  def setMotorMaximumTorque(self, aMax):
    self.ID.setMotorMaximumTorque_(aMax)    
  def getMotorMaximumTorque(self):
    return self.ID.motorMaximumTorque()
  motorMaximumTorque = property(getMotorMaximumTorque, setMotorMaximumTorque)
  
class PhysicsBallSocketJoint(CInst):
  def __init__(self, bodyA=None, anchorA=None, bodyB=None, anchorB=None, ID=None):
    if ID is not None:
      self.ID = ID
    elif bodyB is None:
      self.ID = SCNPhysicsBallSocketJoint.jointWithBody_anchor_(bodyA.ID, vector3Make(anchorA))
    else:
      self.ID = SCNPhysicsBallSocketJoint.jointWithBodyA_anchorA_bodyB_anchorB_(bodyA.ID, vector3Make(anchorA), bodyB.ID, vector3Make(anchorB))
    
  @classmethod
  def jointWithBody(cls, body=None, anchor=None):
    return cls(bodyA=body, anchorA=anchor)
    
  @classmethod
  def jointWithBodyA(cls, bodyA=None, anchorA=None, bodyB=None, anchorB=None):
    return cls(bodyA=bodyA, anchorA=anchorA, bodyB=bodyB, anchorB=anchorB)
    
  @classmethod
  def joint(cls, body=None, anchor=None, bodyA=None, anchorA=None, bodyB=None, anchorB=None):
    if bodyB is None:
      if bodyA is None:
        return cls(bodyA=body, anchorA=anchor)
      elif body is None:
        return cls(bodyA=bodyA, anchorA=anchorA)
      else:
        return cls(bodyA=body, anchorA=anchor, bodyB=bodyA, anchorB=anchorA)
    elif body is None:
      return cls(bodyA=bodyA, anchorA=anchorA, bodyB=bodyB, anchorB=anchorB)
    else:
      return cls(bodyA=body, anchorA=anchor, bodyB=bodyA, anchorB=anchorA)
      
  def getBodyA(self):
    return sceneKit.PhysicsBody.outof(self.ID.bodyA())
  bodyA = property(getBodyA, None)
  
  def getAnchorA(self):
    an = self.ID.anchorA()
    return Vector3(an.a, an.b, an.c)
  anchorA = property(getAnchorA, None)
  
  def getBodyB(self):
    return sceneKit.PhysicsBody.outof(self.ID.bodyB())
  bodyB = property(getBodyB, None)
  
  def getAnchorB(self):
    an = self.ID.anchorB()
    return Vector3(an.a, an.b, an.c)
  anchorB = property(getAnchorB, None)

class PhysicsConeTwistJoint(CInst):
  def __init__(self, bodyA=None, frameA=None, bodyB=None, frameB=None, ID=None):
    if ID is not None:
      self.ID = ID
    elif bodyB is None:
      self.ID = SCNPhysicsConeTwistJoint.jointWithBody_frame_(bodyA.ID, matrix4Make(frameA))
    else:
      self.ID = SCNPhysicsConeTwistJoint.jointWithBodyA_frameA_bodyB_frameB_(bodyA.ID, matrix4Make(frameA), bodyB.ID, matrix4Make(frameB))
    
  @classmethod
  def jointWithBody(cls, body=None, frame=None):
    return cls(bodyA=body, frameA=frame)
    
  @classmethod
  def jointWithBodyA(cls, bodyA=None, frameA=None, bodyB=None, frameB=None):
    return cls(bodyA=bodyA, frameA=frameA, bodyB=bodyB, frameB=frameB)
    
  @classmethod
  def joint(cls, body=None, frame=None, bodyA=None, frameA=None, bodyB=None, frameB=None):
    if bodyB is None:
      if bodyA is None:
        return cls(bodyA=body, frameA=frame)
      elif body is None:
        return cls(bodyA=bodyA, frameA=frameA)
      else:
        return cls(bodyA=body, frameA=frame, bodyB=bodyA, frameB=frameA)
    elif body is None:
      return cls(bodyA=bodyA, frameA=frameA, bodyB=bodyB, frameB=frameB)
    else:
      return cls(bodyA=body, frameA=frame, bodyB=bodyA, frameB=frameA)
      
  def getBodyA(self):
    return sceneKit.PhysicsBody.outof(self.ID.bodyA())
  bodyA = property(getBodyA, None)
  
  def getFrameA(self):
    fr = self.ID.frameA()
    return Vector3(fr.a, fr.b, fr.c)
  frameA = property(getFrameA, None)
  
  def getBodyB(self):
    return sceneKit.PhysicsBody.outof(self.ID.bodyB())
  bodyB = property(getBodyB, None)
  
  def getFrameB(self):
    fr = self.ID.frameB()
    return Vector3(fr.a, fr.b, fr.c)
  frameB = property(getFrameB, None)

  def setMaximumAngularLimit1(self, aLimit):
    self.ID.setMaximumAngularLimit1_(aLimit)    
  def getMaximumAngularLimit1(self):
    return self.ID.maximumAngularLimit1()
  maximumAngularLimit1 = property(getMaximumAngularLimit1, setMaximumAngularLimit1)
  
  def setMaximumAngularLimit2(self, aLimit):
    self.ID.setMaximumAngularLimit2_(aLimit)    
  def getMaximumAngularLimit2(self):
    return self.ID.maximumAngularLimit2()
  maximumAngularLimit2 = property(getMaximumAngularLimit2, setMaximumAngularLimit2)

  def setMaximumTwistAngle(self, aMax):
    self.ID.setMaximumTwistAngle_(aMax)    
  def getMaximumTwistAngle(self):
    return self.ID.maximumTwistAngle()
  maximumTwistAngle = property(getMaximumTwistAngle, setMaximumTwistAngle)

class PhysicsVehicle(CInst):
  def __init__(self, chassisBody=None, wheels=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      try:
        iterator = iter(wheels)
      except TypeError:
        wheels = [wheels]
      wheels = [aWheel.ID for aWheel in wheels]
      desc = str(chassisBody.ID.description())
      kind = desc[4:desc.index(':')]
      if kind == 'PhysicsBody':
        self.ID = SCNPhysicsVehicle.vehicleWithChassisBody_wheels_(chassisBody.ID, wheels)
      else:
        raise TypeError('PhysicsBody instance is expected for chassisBody')
  
  @classmethod
  def vehicleWithChassisBody(cls, chassisBody=None, wheels=None):
    return cls(chassisBody=chassisBody, wheels=wheels)
    
  @classmethod
  def vehicle(cls, chassisBody=None, wheels=None):
    return cls(chassisBody=chassisBody, wheels=wheels)
    
  def getChassisBody(self):
    return sceneKit.PhysicsBody.outof(self.ID.chassisBody())
  chassisBody = property(getChassisBody, None)
  
  def getWheels(self):
    return tuple([sceneKit.PhysicsVehicleWheel.outof(aWheel) for aWheel in self.ID.wheels()])
  wheels = property(getWheels, None)
  
  def applyEngineForce(self, engineForce=None, forWheelAtIndex=None, value=0.0, index=0):
    if engineForce is None: engineForce = value
    if forWheelAtIndex is None: forWheelAtIndex = index
    self.ID.applyEngineForce_forWheelAtIndex_(engineForce, forWheelAtIndex)
    
  def applyBrakingForce(self, brakingForce=None, forWheelAtIndex=None, value=0.0, index=0):
    if brakingForce is None: brakingForce = value
    if forWheelAtIndex is None: forWheelAtIndex = index
    self.ID.applyBrakingForce_forWheelAtIndex_(brakingForce, forWheelAtIndex)
    
  def setSteeringAngle(self, steeringAngle=None, forWheelAtIndex=None, value=0.0, index=0):
    if steeringAngle is None: steeringAngle = value
    if forWheelAtIndex is None: forWheelAtIndex = index
    self.ID.setSteeringAngle_forWheelAtIndex_(steeringAngle, forWheelAtIndex)

  def getSpeedInKilometersPerHour(self):
    return self.ID.speedInKilometersPerHour()
  speedInKilometersPerHour = property(getSpeedInKilometersPerHour, None)
  
  
class PhysicsVehicleWheel(CInst):
  def __init__(self, node=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNPhysicsVehicleWheel.wheelWithNode_(node.ID)
  
  @classmethod
  def wheelWithNode(cls, node=None):
    return cls(node=node)

  def setConnectionPosition(self, aVector3):
    self.ID.setConnectionPosition_(vector3Make(aVector3))
  def getConnectionPosition(self):
    pos = self.ID.connectionPosition()
    return Vector3(pos.a, pos.b, pos.c)
  connectionPosition = property(getConnectionPosition, setConnectionPosition)
  
  def setAxle(self, aVector3):
    self.ID.setAxle_(vector3Make(aVector3))
  def getAxle(self):
    ax = self.ID.axle()
    return Vector3(ax.a, ax.b, ax.c)
  axle = property(getAxle, setAxle)
  
  def setSteeringAxis(self, aVector3):
    self.ID.setSteeringAxis_(vector3Make(aVector3))
  def getSteeringAxis(self):
    ax = self.ID.steeringAxis()
    return Vector3(ax.a, ax.b, ax.c)
  steeringAxis = property(getSteeringAxis, setSteeringAxis)
  
  def setRadius(self, aRadius):
    self.ID.setRadius_(aRadius)    
  def getRadius(self):
    return self.ID.radius()
  radius = property(getRadius, setRadius)
  
  def setFrictionSlip(self, aSlip):
    self.ID.setFrictionSlip_(aSlip)    
  def getFrictionSlip(self):
    return self.ID.frictionSlip()
  frictionSlip = property(getFrictionSlip, setFrictionSlip)
  
  def setSuspensionStiffness(self, aStiff):
    self.ID.setSuspensionStiffness_(aStiff)    
  def getSuspensionStiffness(self):
    return self.ID.suspensionStiffness()
  suspensionStiffness = property(getSuspensionStiffness, setSuspensionStiffness)
  
  def setSuspensionCompression(self, aComp):
    self.ID.setSuspensionCompression_(aComp)    
  def getSuspensionCompression(self):
    return self.ID.suspensionCompression()
  suspensionCompression = property(getSuspensionCompression, setSuspensionCompression)
  
  def setSuspensionDamping(self, aSuspensionDamping):
    self.ID.setSuspensionDamping_(aSuspensionDamping)    
  def getSuspensionDamping(self):
    return self.ID.suspensionDamping()
  suspensionDamping = property(getSuspensionDamping, setSuspensionDamping)
  
  def setMaximumSuspensionTravel(self, aTravel):
    self.ID.setMaximumSuspensionTravel_(aTravel)    
  def getMaximumSuspensionTravel(self):
    return self.ID.maximumSuspensionTravel()
  maximumSuspensionTravel = property(getMaximumSuspensionTravel, setMaximumSuspensionTravel)
  
  def setSuspensionRestLength(self, aLength):
    self.ID.setSuspensionRestLength_(aLength)    
  def getSuspensionRestLength(self):
    return self.ID.suspensionRestLength()
  suspensionRestLength = property(getSuspensionRestLength, setSuspensionRestLength)
  
  def getNode(self):
    return sceneKit.Node.outof(self.ID.node())
  node = property(getNode, None)


class PhysicsShape(CInst):
  def __init__(self, geometry=None, node= None, shapes=None, transforms=None, options=None, ID=None):
    if options is not None:
      options = dict(options)
      if SCNPhysicsShapeScaleKey in options:
        scale = vector3Make(options[SCNPhysicsShapeScaleKey])
        scaleC = SCNVector3(scale.x, scale.y, scale.z)
        options[SCNPhysicsShapeScaleKey] = NSValue.valueWithSCNVector3_(scaleC)
        
    if ID is not None:
      self.ID = ID
    elif geometry is not None:
      self.ID = SCNPhysicsShape.shapeWithGeometry_options_(geometry.ID, options)
    elif node is not None:
      self.ID = SCNPhysicsShape.shapeWithNode_options_(node.ID, options)
    elif shapes is not None:
      try:
        iterator = iter(shapes)
      except TypeError:
        shapes = [shapes]
      shapes = [aShape.ID for aShape in shapes]
      if transforms is not None:
        try:
          iterator = iter(transforms)
        except TypeError:
          transforms = [transforms]
        length = len(transforms)
        transforms = [SCNMatrix4(*m) for m in transforms]
        transforms = [NSValue.valueWithSCNMatrix4_(s, restype=c_void_p, argtypes=[SCNMatrix4]) for s in transforms]
        bArray = NSMutableArray.array()
        for i in range(length):
          bArray.addObject_(transforms[i])
        transforms = NSArray.arrayWithArray_(bArray)        
      self.ID = SCNPhysicsShape.shapeWithShapes_transforms_(shapes, transforms)    
    else:
      return None
    
  @classmethod
  def shapeWithGeometry(cls, geometry=None, options=None):
    return cls(geometry=geometry, options=options)
    
  @classmethod
  def shapeWithNode(cls, node=None, options=None):
    return cls(node=node, options=options)
    
  @classmethod
  def shapeWithShapes(cls, shapes=None, transforms=None):
    return cls(shapes=shapes, transforms=transforms)

  def getSourceObject(self):
    anObject = self.ID.sourceObject()
    try:
      anObject.parentNode()
      return sceneKit.Node.outof(anObject)
    except AttributeError: pass
    try:
      anObject.firstMaterial()
      return sceneKit.Geometry.outof(anObject)
    except AttributeError: pass
    try:
      iterator = iter(anObject)
      return tuple([sceneKit.PhysicsShape.outof(aShape) for aShape in anObject])      
    except TypeError:
      return None     
  sourceObject = property(getSourceObject, None)
  
  def getOptions(self):
    options = self.ID.options()
    if options is not None:
      if SCNPhysicsShapeScaleKey in options:
        scaleC = options[SCNPhysicsShapeScaleKey].SCNVector3Value()
        scale = Vector3(scale.x, scale.y, scale.z)
        options[SCNPhysicsShapeScaleKey] = scale
    return options
  options = property(getOptions, None)
  
  def getTransforms(self):
    return tuple([matrix4Make(getCStructValuesAsList(aTrans.SCNMatrix4Value())) for aTrans in self.ID.transforms()])
  transforms = property(getTransforms, None)
  
class PhysicsContact(CInst_NoCache):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      return None
      
  def getNodeA(self):
    return sceneKit.Node.outof(self.ID.nodeA())
  nodeA = property(getNodeA, None)
  
  def getNodeB(self):
    return sceneKit.Node.outof(self.ID.nodeB())
  nodeB = property(getNodeB, None)
  
  def getContactPoint(self):
    point = self.ID.contactPoint()
    return Vector3(point.a, point.b, point.c)
  contactPoint = property(getContactPoint, None)
  
  def getContactNormal(self):
    normal = self.ID.contactNormal()
    return Vector3(normal.a, normal.b, normal.c)
  contactNormal = property(getContactNormal, None)
  
  def getCollisionImpulse(self):
    return self.ID.collisionImpulse()
  collisionImpulse = property(getCollisionImpulse, None)
  
  def getPenetrationDistance(self):
    return self.ID.penetrationDistance()
  penetrationDistance = property(getPenetrationDistance, None)
  
  def getSweepTestFraction(self):
    return self.ID.sweepTestFraction()
  sweepTestFraction = property(getSweepTestFraction, None)
  
def physicsWorld_didBeginContact_(_self, _cmd, world, contact):
  aPhysicsContactDelegate = sceneKit.PhysicsContactDelegate.outof(ObjCInstance(_self))
  if aPhysicsContactDelegate.methods[0]:
    aWorld = sceneKit.PhysicsWorld.outof(ObjCInstance(world))
    aContact = sceneKit.PhysicsContact.outof(ObjCInstance(contact))
    aPhysicsContactDelegate.delegate.didBeginContact(aWorld, aContact)
    
def physicsWorld_didUpdateContact_(_self, _cmd, world, contact):
  aPhysicsContactDelegate = sceneKit.PhysicsContactDelegate.outof(ObjCInstance(_self))
  if aPhysicsContactDelegate.methods[1]:
    aWorld = sceneKit.PhysicsWorld.outof(ObjCInstance(world))
    aContact = sceneKit.PhysicsContact.outof(ObjCInstance(contact))
    aPhysicsContactDelegate.delegate.didUpdateContact(aWorld, aContact)
    
def physicsWorld_didEndContact_(_self, _cmd, world, contact):
  aPhysicsContactDelegate = sceneKit.PhysicsContactDelegate.outof(ObjCInstance(_self))
  if aPhysicsContactDelegate.methods[2]:
    aWorld = sceneKit.PhysicsWorld.outof(ObjCInstance(world))
    aContact = sceneKit.PhysicsContact.outof(ObjCInstance(contact))
    aPhysicsContactDelegate.delegate.didEndContact(aWorld, aContact)
  
class PhysicsContactDelegate(CInst):
  _actions = ('didBeginContact', 'didUpdateContact', 'didEndContact')
  _newCClassName = 'SCNPYPhysicsContactDelegateClass'
  _cMethodList = [physicsWorld_didBeginContact_, physicsWorld_didUpdateContact_, physicsWorld_didEndContact_]
  _protocols =['SCNPhysicsContactDelegate']
  DelegateCClass = create_objc_class(_newCClassName, NSObject, methods=_cMethodList, protocols=_protocols)

  def __init__(self, aDelegate, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.delegate = aDelegate
      self.methods = [callable(_a) for _a in [getattr(aDelegate, anAction, False) for anAction in PhysicsContactDelegate._actions]]
      self.ID = PhysicsContactDelegate.DelegateCClass.alloc().init()
