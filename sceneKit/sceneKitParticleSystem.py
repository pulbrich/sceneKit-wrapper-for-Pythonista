'''particle system modul, to be included in sceneKit'''

from ctypes import *

from ui import parse_color

import sceneKit
from .sceneKitEnv import *
from .sceneKitAnimation import *

class ParticleBirthLocation(Enum):
  Surface = 0
  Volume = 1
  Vertex = 2
  SCNParticleBirthLocationSurface = 0
  SCNParticleBirthLocationVolume = 1
  SCNParticleBirthLocationVertex = 2
  
class ParticleBirthDirection(Enum):
  Constant = 0
  SurfaceNormal = 1
  Random = 2
  SCNParticleBirthDirectionConstant = 0
  SCNParticleBirthDirectionSurfaceNormal = 1
  SCNParticleBirthDirectionRandom = 2
  
class ParticleImageSequenceAnimationMode(Enum):
  Repeat = 0
  Clamp = 1
  AutoReverse = 2
  SCNParticleImageSequenceAnimationModeRepeat = 0
  SCNParticleImageSequenceAnimationModeClamp = 1
  SCNParticleImageSequenceAnimationModeAutoReverse = 2
  
class ParticleBlendMode(Enum):
  Additive = 0
  Subtract = 1
  Multiply = 2
  Screen = 3
  Alpha = 4
  Replace = 5
  SCNParticleBlendModeAdditive = 0
  SCNParticleBlendModeSubtract = 1
  SCNParticleBlendModeMultiply = 2
  SCNParticleBlendModeScreen = 3
  SCNParticleBlendModeAlpha = 4
  SCNParticleBlendModeReplace = 5
  
class ParticleOrientationMode(Enum):
  BillboardScreenAligned = 0
  BillboardViewAligned = 1
  Free = 2
  BillboardYAligned = 3
  SCNParticleOrientationModeBillboardScreenAligned = 0
  SCNParticleOrientationModeBillboardViewAligned = 1
  SCNParticleOrientationModeFree = 2
  SCNParticleOrientationModeBillboardYAligned = 3
  
class ParticleSortingMode(Enum):
  ModeNone = 0
  ProjectedDepth = 1
  Distance = 2
  OldestFirst = 3
  YoungestFirst = 4
  SCNParticleSortingModeNone = 0
  SCNParticleSortingModeProjectedDepth = 1
  SCNParticleSortingModeDistance = 2
  SCNParticleSortingModeOldestFirst = 3
  SCNParticleSortingModeYoungestFirst = 4
  
_particleProperties = []
for aProperty in ['SCNParticlePropertyAngle', 'SCNParticlePropertyAngularVelocity', 'SCNParticlePropertyBounce', 'SCNParticlePropertyCharge', 'SCNParticlePropertyColor', 'SCNParticlePropertyContactNormal', 'SCNParticlePropertyContactPoint', 'SCNParticlePropertyFrame', 'SCNParticlePropertyFrameRate', 'SCNParticlePropertyFriction', 'SCNParticlePropertyLife', 'SCNParticlePropertyOpacity', 'SCNParticlePropertyPosition', 'SCNParticlePropertyRotationAxis', 'SCNParticlePropertySize', 'SCNParticlePropertyVelocity']:
  _particleProperties.append(str(ObjCInstance(c_void_p.in_dll(c, aProperty))))
_particleProperties = tuple(_particleProperties)
SCNParticlePropertyAngle, SCNParticlePropertyAngularVelocity, SCNParticlePropertyBounce, SCNParticlePropertyCharge, \
SCNParticlePropertyColor, SCNParticlePropertyContactNormal, SCNParticlePropertyContactPoint, SCNParticlePropertyFrame, \
SCNParticlePropertyFrameRate, SCNParticlePropertyFriction, SCNParticlePropertyLife, SCNParticlePropertyOpacity, \
SCNParticlePropertyPosition, SCNParticlePropertyRotationAxis, SCNParticlePropertySize, SCNParticlePropertyVelocity = _particleProperties
ParticlePropertyAngle, ParticlePropertyAngularVelocity, ParticlePropertyBounce, ParticlePropertyCharge, \
ParticlePropertyColor, ParticlePropertyContactNormal, ParticlePropertyContactPoint, ParticlePropertyFrame, \
ParticlePropertyFrameRate, ParticlePropertyFriction, ParticlePropertyLife, ParticlePropertyOpacity, \
ParticlePropertyPosition, ParticlePropertyRotationAxis, ParticlePropertySize, ParticlePropertyVelocity = _particleProperties

class ParticleEvent(Enum):
  Birth = 0
  Death = 1
  Collision = 2
  SCNParticleEventBirth = 0
  SCNParticleEventDeath = 1
  SCNParticleEventCollision = 2

class ParticleModifierStage(Enum):
  PreDynamics = 0
  PostDynamics = 1
  PreCollision = 2
  PostCollision = 3
  SCNParticleModifierStagePreDynamics = 0
  SCNParticleModifierStagePostDynamics = 1
  SCNParticleModifierStagePreCollision = 2
  SCNParticleModifierStagePostCollision = 3

class ParticleInputMode(Enum):
  OverLife = 0
  OverDistance = 1
  OverOtherProperty = 2
  SCNParticleInputModeOverLife = 0
  SCNParticleInputModeOverDistance = 1
  SCNParticleInputModeOverOtherProperty = 2

class ParticleSystem(Animatable, CInst):
  def __init__(self, name=None, directory=None, ID=None):
    self.particleEventBlocks = []
    self.particleModifierBlocks = []
    if ID is not None:
      self.ID = ID
    elif name is not None:
      self.ID = SCNParticleSystem.particleSystemNamed_inDirectory_(name, directory)
    else:
      self.ID = SCNParticleSystem.particleSystem()
      
  @classmethod
  def particleSystem(cls):
    return cls()
    
  @classmethod
  def particleSystemNamed(cls, name=None, directory=None, inDirectory=None):
    directory = inDirectory if directory is None else directory
    return cls(name=name, directory=inDirectory)
    
  def setEmissionDuration(self, aDuration):
    self.ID.setEmissionDuration_(aDuration)    
  def getEmissionDuration(self):
    return self.ID.emissionDuration()
  emissionDuration = property(getEmissionDuration, setEmissionDuration)
  
  def setEmissionDurationVariation(self, aVariation):
    self.ID.setEmissionDurationVariation_(aVariation)    
  def getEmissionDurationVariation(self):
    return self.ID.emissionDurationVariation()
  emissionDurationVariation = property(getEmissionDurationVariation, setEmissionDurationVariation)
  
  def setIdleDuration(self, aDuration):
    self.ID.setIdleDuration_(aDuration)    
  def getIdleDuration(self):
    return self.ID.idleDuration()
  idleDuration = property(getIdleDuration, setIdleDuration)
  
  def setIdleDurationVariation(self, aVariation):
    self.ID.setIdleDurationVariation_(aVariation)    
  def getIdleDurationVariation(self):
    return self.ID.idleDurationVariation()
  idleDurationVariation = property(getIdleDurationVariation, setIdleDurationVariation)

  def setLoops(self, aBool):
    self.ID.setLoops_(aBool)    
  def getLoops(self):
    return self.ID.loops()
  loops = property(getLoops, setLoops)
  
  def setWarmupDuration(self, aDuration):
    self.ID.setWarmupDuration_(aDuration)    
  def getWarmupDuration(self):
    return self.ID.warmupDuration()
  warmupDuration = property(getWarmupDuration, setWarmupDuration)
  
  def setBirthRate(self, aRate):
    self.ID.setBirthRate_(aRate)    
  def getBirthRate(self):
    return self.ID.birthRate()
  birthRate = property(getBirthRate, setBirthRate)
  
  def setBirthRateVariation(self, aVariation):
    self.ID.setBirthRateVariation_(aVariation)    
  def getBirthRateVariation(self):
    return self.ID.birthRateVariation()
  birthRateVariation = property(getBirthRateVariation, setBirthRateVariation)
  
  def setEmitterShape(self, aGeometry):
    self.ID.setEmitterShape_(aGeometry.ID)    
  def getEmitterShape(self):
    return sceneKit.Geometry.outof(self.ID.emitterShape())
  emitterShape = property(getEmitterShape, setEmitterShape)
  
  def setBirthLocation(self, aLocation):
    self.ID.setBirthLocation_(aLocation.value)    
  def getBirthLocation(self):
    return ParticleBirthLocation(self.ID.birthLocation())
  birthLocation = property(getBirthLocation, setBirthLocation)
  
  def setBirthDirection(self, aDirection):
    self.ID.setBirthDirection_(aDirection.value)    
  def getBirthDirection(self):
    return ParticleBirthDirection(self.ID.birthDirection())
  birthDirection = property(getBirthDirection, setBirthDirection)
  
  def setEmittingDirection(self, aDirection):
    self.ID.setEmittingDirection_(vector3Make(aDirection))
  def getEmittingDirection(self):
    dire = self.ID.emittingDirection()
    return Vector3(dire.a, dire.b, dire.c)
  emittingDirection = property(getEmittingDirection, setEmittingDirection)
  
  def setSpreadingAngle(self, anAngle):
    self.ID.setSpreadingAngle_(anAngle)    
  def getSpreadingAngle(self):
    return self.ID.spreadingAngle()
  spreadingAngle = property(getSpreadingAngle, setSpreadingAngle)
  
  def setParticleAngle(self, anAngle):
    self.ID.setParticleAngle_(anAngle)    
  def getParticleAngle(self):
    return self.ID.particleAngle()
  particleAngle = property(getParticleAngle, setParticleAngle)
  
  def setParticleAngleVariation(self, aVariation):
    self.ID.setParticleAngleVariation_(aVariation)    
  def getParticleAngleVariation(self):
    return self.ID.particleAngleVariation()
  particleAngleVariation = property(getParticleAngleVariation, setParticleAngleVariation)
  
  def setParticleVelocity(self, aVelocity):
    self.ID.setParticleVelocity_(aVelocity)    
  def getParticleVelocity(self):
    return self.ID.particleVelocity()
  particleVelocity = property(getParticleVelocity, setParticleVelocity)
  
  def setParticleVelocityVariation(self, aVariation):
    self.ID.setParticleVelocityVariation_(aVariation)    
  def getParticleVelocityVariation(self):
    return self.ID.particleVelocityVariation()
  particleVelocityVariation = property(getParticleVelocityVariation, setParticleVelocityVariation)
  
  def setParticleAngularVelocity(self, aVelocity):
    self.ID.setParticleAngularVelocity_(aVelocity)    
  def getParticleAngularVelocity(self):
    return self.ID.particleAngularVelocity()
  particleAngularVelocity = property(getParticleAngularVelocity, setParticleAngularVelocity)
  
  def setParticleAngularVelocityVariation(self, aVariation):
    self.ID.setParticleAngularVelocityVariation_(aVariation)    
  def getParticleAngularVelocityVariation(self):
    return self.ID.particleAngularVelocityVariation()
  particleAngularVelocityVariation = property(getParticleAngularVelocityVariation, setParticleAngularVelocityVariation)
  
  def setParticleLifeSpan(self, aSpan):
    self.ID.setParticleLifeSpan_(aSpan)    
  def getParticleLifeSpan(self):
    return self.ID.particleLifeSpan()
  particleLifeSpan = property(getParticleLifeSpan, setParticleLifeSpan)
  
  def setParticleLifeSpanVariation(self, aVariation):
    self.ID.setParticleLifeSpanVariation_(aVariation)    
  def getParticleLifeSpanVariation(self):
    return self.ID.particleLifeSpanVariation()
  particleLifeSpanVariation = property(getParticleLifeSpanVariation, setParticleLifeSpanVariation)
  
  def setParticleSize(self, aSize):
    self.ID.setParticleSize_(aSize)    
  def getParticleSize(self):
    return self.ID.particleSize()
  particleSize = property(getParticleSize, setParticleSize)
  
  def setParticleSizeVariation(self, aVariation):
    self.ID.setParticleSizeVariation_(aVariation)    
  def getParticleSizeVariation(self):
    return self.ID.particleSizeVariation()
  particleSizeVariation = property(getParticleSizeVariation, setParticleSizeVariation)
  
  def setParticleColor(self, aColor):
    r, g, b, a = parse_color(aColor)
    self.ID.setParticleColor_(UIColor.color(red=r, green=g, blue=b, alpha=a)) 
  def getParticleColor(self):
    color = self.ID.particleColor()
    return RGBA(color.red(), color.green(), color.blue(), color.alpha())
  particleColor = property(getParticleColor, setParticleColor)
  
  def setParticleColorVariation(self, aVector4):
    self.ID.setParticleColorVariation_(vector4Make(aVector4))    
  def getParticleColorVariation(self):
    var = self.ID.particleColorVariation()
    return Vector4(var.a, var.b, var.c, var.d)
  particleColorVariation = property(getParticleColorVariation, setParticleColorVariation)
  
  def setParticleImage(self, aContent):
    self.ID.setParticleImage_(sceneKit.contentFromPy(aContent))
  def getParticleImage(self):
    contents = self.ID.particleImage()
    return sceneKit.contentFromC(contents)
  particleImage = property(getParticleImage, setParticleImage)
  
  def setFresnelExponent(self, anExp):
    self.ID.setFresnelExponent_(anExp)    
  def getFresnelExponent(self):
    return self.ID.fresnelExponent()
  fresnelExponent = property(getFresnelExponent, setFresnelExponent)
  
  def setStretchFactor(self, aFactor):
    self.ID.setStretchFactor_(aFactor)    
  def getStretchFactor(self):
    return self.ID.stretchFactor()
  stretchFactor = property(getStretchFactor, setStretchFactor)
  
  def setImageSequenceRowCount(self, aCount):
    self.ID.setImageSequenceRowCount_(aCount)    
  def getImageSequenceRowCount(self):
    return self.ID.imageSequenceRowCount()
  imageSequenceRowCount = property(getImageSequenceRowCount, setImageSequenceRowCount)
  
  def setImageSequenceColumnCount(self, aCount):
    self.ID.setImageSequenceColumnCount_(aCount)    
  def getImageSequenceColumnCount(self):
    return self.ID.imageSequenceColumnCount()
  imageSequenceColumnCount = property(getImageSequenceColumnCount, setImageSequenceColumnCount)
  
  def setImageSequenceInitialFrame(self, aFrame):
    self.ID.setImageSequenceInitialFrame_(aFrame)    
  def getImageSequenceInitialFrame(self):
    return self.ID.imageSequenceInitialFrame()
  imageSequenceInitialFrame = property(getImageSequenceInitialFrame, setImageSequenceInitialFrame)
  
  def setImageSequenceInitialFrameVariation(self, aVariation):
    self.ID.setImageSequenceInitialFrameVariation_(aVariation)    
  def getImageSequenceInitialFrameVariation(self):
    return self.ID.imageSequenceInitialFrameVariation()
  imageSequenceInitialFrameVariation = property(getImageSequenceInitialFrameVariation, setImageSequenceInitialFrameVariation)
  
  def setImageSequenceFrameRate(self, aRate):
    self.ID.setImageSequenceFrameRate_(aRate)    
  def getImageSequenceFrameRate(self):
    return self.ID.imageSequenceFrameRate()
  imageSequenceFrameRate = property(getImageSequenceFrameRate, setImageSequenceFrameRate)
  
  def setImageSequenceFrameRateVariation(self, aVariation):
    self.ID.setImageSequenceFrameRateVariation_(aVariation)    
  def getImageSequenceFrameRateVariation(self):
    return self.ID.imageSequenceFrameRateVariation()
  imageSequenceFrameRateVariation = property(getImageSequenceFrameRateVariation, setImageSequenceFrameRateVariation)
  
  def setImageSequenceAnimationMode(self, aMode):
    self.ID.setImageSequenceAnimationMode_(aMode.value)    
  def getImageSequenceAnimationMode(self):
    return ParticleImageSequenceAnimationMode(self.ID.imageSequenceAnimationMode())
  imageSequenceAnimationMode = property(getImageSequenceAnimationMode, setImageSequenceAnimationMode)
  
  def setAffectedByGravity(self, aBool):
    self.ID.setAffectedByGravity_(aBool)    
  def getAffectedByGravity(self):
    return self.ID.affectedByGravity()
  affectedByGravity = property(getAffectedByGravity, setAffectedByGravity)
  
  def setAffectedByPhysicsFields(self, aBool):
    self.ID.setAffectedByPhysicsFields_(aBool)    
  def getAffectedByPhysicsFields(self):
    return self.ID.affectedByPhysicsFields()
  affectedByPhysicsFields = property(getAffectedByPhysicsFields, setAffectedByPhysicsFields)
  
  def setColliderNodes(self, aNodeList):
    try:
      iterator = iter(aNodeList)
    except TypeError:
      aNodeList = [aNodeList]
    self.ID.setColliderNodes_([aNode.ID for aNode in aNodeList])
  def getColliderNodes(self):
    return tuple([sceneKit.Node.outof(cNode) for cNode in self.ID.colliderNodes()])
  colliderNodes = property(getColliderNodes, setColliderNodes)
  
  def setParticleDiesOnCollision(self, aBool):
    self.ID.setParticleDiesOnCollision_(aBool)    
  def getParticleDiesOnCollision(self):
    return self.ID.particleDiesOnCollision()
  particleDiesOnCollision = property(getParticleDiesOnCollision, setParticleDiesOnCollision)
  
  def setAcceleration(self, aVector3):
    self.ID.setAcceleration_(vector3Make(aVector3))
  def getAcceleration(self):
    acc = self.ID.acceleration()
    return vector3(acc.a, acc.b, acc.c)
  acceleration = property(getAcceleration, setAcceleration)
  
  def setDampingFactor(self, aFactor):
    self.ID.setDampingFactor_(aFactor)    
  def getDampingFactor(self):
    return self.ID.dampingFactor()
  dampingFactor = property(getDampingFactor, setDampingFactor)
  
  def setParticleMass(self, aMass):
    self.ID.setParticleMass_(aMass)    
  def getParticleMass(self):
    return self.ID.particleMass()
  particleMass = property(getParticleMass, setParticleMass)
  
  def setParticleMassVariation(self, aVariation):
    self.ID.setParticleMassVariation_(aVariation)    
  def getParticleMassVariation(self):
    return self.ID.particleMassVariation()
  particleMassVariation = property(getParticleMassVariation, setParticleMassVariation)
  
  def setParticleCharge(self, aCharge):
    self.ID.setParticleCharge_(aCharge)    
  def getParticleCharge(self):
    return self.ID.particleCharge()
  particleCharge = property(getParticleCharge, setParticleCharge)
  
  def setParticleChargeVariation(self, aVariation):
    self.ID.setParticleChargeVariation_(aVariation)    
  def getParticleChargeVariation(self):
    return self.ID.particleChargeVariation()
  particleChargeVariation = property(getParticleChargeVariation, setParticleChargeVariation)
  
  def setParticleBounce(self, aBounce):
    self.ID.setParticleBounce_(aBounce)    
  def getParticleBounce(self):
    return self.ID.particleBounce()
  particleBounce = property(getParticleBounce, setParticleBounce)
  
  def setParticleBounceVariation(self, aVariation):
    self.ID.setParticleBounceVariation_(aVariation)    
  def getParticleBounceVariation(self):
    return self.ID.particleBounceVariation()
  particleBounceVariation = property(getParticleBounceVariation, setParticleBounceVariation)
  
  def setParticleFriction(self, aFriction):
    self.ID.setParticleFriction_(aFriction)    
  def getParticleFriction(self):
    return self.ID.particleFriction()
  particleFriction = property(getParticleFriction, setParticleFriction)
  
  def setParticleFrictionVariation(self, aVariation):
    self.ID.setParticleFrictionVariation_(aVariation)    
  def getParticleFrictionVariation(self):
    return self.ID.particleFrictionVariation()
  particleFrictionVariation = property(getParticleFrictionVariation, setParticleFrictionVariation)
  
  def setSystemSpawnedOnCollision(self, aSystem):
    self.ID.setSystemSpawnedOnCollision_(aSystem.ID)    
  def getSystemSpawnedOnCollision(self):
    return sceneKit.ParticleSystem.outof(self.ID.systemSpawnedOnCollision())
  systemSpawnedOnCollision = property(getSystemSpawnedOnCollision, setSystemSpawnedOnCollision)
  
  def setSystemSpawnedOnDying(self, aSystem):
    self.ID.setSystemSpawnedOnDying_(aSystem.ID)
  def getSystemSpawnedOnDying(self):
    return sceneKit.ParticleSystem.outof(self.ID.systemSpawnedOnDying())
  systemSpawnedOnDying = property(getSystemSpawnedOnDying, setSystemSpawnedOnDying)
  
  def setSystemSpawnedOnLiving(self, aSystem):
    self.ID.setSystemSpawnedOnLiving_(aSystem.ID)    
  def getSystemSpawnedOnLiving(self):
    return sceneKit.ParticleSystem.outof(self.ID.systemSpawnedOnLiving())
  systemSpawnedOnLiving = property(getSystemSpawnedOnLiving, setSystemSpawnedOnLiving)
  
  def setBlendMode(self, aMode):
    self.ID.setBlendMode_(aMode.value)    
  def getBlendMode(self):
    return ParticleBlendMode(self.ID.blendMode())
  blendMode = property(getBlendMode, setBlendMode)
  
  def setOrientationMode(self, aMode):
    self.ID.setOrientationMode_(aMode.value)    
  def getOrientationMode(self):
    return ParticleOrientationMode(self.ID.orientationMode())
  orientationMode = property(getOrientationMode, setOrientationMode)
  
  def setSortingMode(self, aMode):
    self.ID.setSortingMode_(aMode.value)    
  def getSortingMode(self):
    return ParticleSortingMode(self.ID.sortingMode())
  sortingMode = property(getSortingMode, setSortingMode)
  
  def setLightingEnabled(self, aBool):
    self.ID.setLightingEnabled_(aBool)    
  def isLightingEnabled(self):
    return self.ID.lightingEnabled()
  lightingEnabled = property(isLightingEnabled, setLightingEnabled)
  
  def setBlackPassEnabled(self, aBool):
    self.ID.setBlackPassEnabled_(aBool)    
  def isBlackPassEnabled(self):
    return self.ID.blackPassEnabled()
  blackPassEnabled = property(isBlackPassEnabled, setBlackPassEnabled)
  
  def setLocal(self, a):
    self.ID.setLocal_(a)    
  def isLocal(self):
    return self.ID.local()
  local = property(isLocal, setLocal)
  
  def reset(self):
    self.ID.reset()
    
  def setSpeedFactor(self, aFactor):
    self.ID.setSpeedFactor_(aFactor)    
  def getSpeedFactor(self):
    return self.ID.speedFactor()
  speedFactor = property(getSpeedFactor, setSpeedFactor)
  
  def setPropertyControllers(self, aDict):
    cDict = dict()
    for (prop, contr) in aDict.items():
      i = _particleProperties.index(prop)
      cDict[prop] = contr.ID
    self.ID.setPropertyControllers_(cDict)    
  def getPropertyControllers(self):
    cDict = self.ID.propertyControllers()
    aDict = dict()
    for (prop, contr) in cDict.items():
      aDict[str(prop)] = sceneKit.ParticlePropertyController.outof(contr)
    return aDict
  propertyControllers = property(getPropertyControllers, setPropertyControllers)
  
  def setOrientationDirection(self, aDirection):
    self.ID.setOrientationDirection_(vector3Make(aDirection))
  def getOrientationDirection(self):
    dire = self.ID.orientationDirection()
    return vector3(dire.a, dire.b, dire.c)
  orientationDirection = property(getOrientationDirection, setOrientationDirection)
  
  def setParticleIntensity(self, aParticleIntensity):
    self.ID.setParticleIntensity_(aParticleIntensity)    
  def getParticleIntensity(self):
    return self.ID.particleIntensity()
  particleIntensity = property(getParticleIntensity, setParticleIntensity)
  
  def setParticleIntensityVariation(self, aVariation):
    self.ID.setParticleIntensityVariation_(aVariation)    
  def getParticleIntensityVariation(self):
    return self.ID.particleIntensityVariation()
  particleIntensityVariation = property(getParticleIntensityVariation, setParticleIntensityVariation)
  
  def blockEnabler(self, prop):
  ##for blocks to work corresponding variation property must be non-default (apple bug)
  ##remove if Apple corrects sceneKit
    small = 0.0000001
    if prop == ParticlePropertyAngle and abs(self.particleAngleVariation) < small: self.particleAngleVariation = small
    elif prop == ParticlePropertyAngularVelocity and abs(self.particleAngularVelocityVariation) < small:
      self.particleAngularVelocityVariation = small
    elif prop == ParticlePropertyBounce and abs(self.particleBounceVariation) < small: self.particleBounceVariation = small
    elif prop == ParticlePropertyCharge and abs(self.particleChargeVariation) < small: self.particleChargeVariation = small
    elif prop == ParticlePropertyColor and (self.particleColorVariation[0]**2 + self.particleColorVariation[1]**2 + self.particleColorVariation[2]**2 + self.particleColorVariation[3]**2) < small:
      self.particleColorVariation = Vector4(0., 0., 0., small)
    elif prop == ParticlePropertyFrame and abs(self.imageSequenceInitialFrameVariation) < small:
      self.imageSequenceInitialFrameVariation = small
    elif prop == ParticlePropertyFrameRate and abs(self.imageSequenceFrameRateVariation < small):
      self.imageSequenceFrameRateVariation = small
    elif prop == ParticlePropertyFriction and abs(self.particleFrictionVariation < small):
      self.particleFrictionVariation = small
    elif prop == ParticlePropertyLife and abs(self.particleLifeSpanVariation) < small: self.particleLifeSpanVariation = small
    elif prop == ParticlePropertySize and abs(self.particleSizeVariation) < small: self.particleSizeVariation = small
    elif prop == ParticlePropertyVelocity and abs(self.particleVelocityVariation) < small: self.particleVelocityVariation = small
  
  def handleEvent(self, event=None, properties=None, block=None, forProperties=None, withBlock=None):
  ## for this to work you have to set the corresponding property variation value to anything but the default! Apple bug:
  ## done via self.blockEnabler(aProperty)
    if properties is None: properties = forProperties
    if block is None and withBlock is not None: block = withBlock
    try:
      iterator = iter(properties)
    except TypeError:
      properties = [properties]
    for aProperty in properties:
      self.blockEnabler(aProperty)
    blockInstance = ParticleEventBlock(event, properties, block)
    self.particleEventBlocks.append(blockInstance)
    self.ID.handleEvent_forProperties_withBlock_(event.value, properties, blockInstance.blockCode)    
  handle = handleEvent
    
  def addModifierForProperties(self, properties=None, stage=None, block=None, forProperties=None, atStage=None, withBlock=None):
    if properties is None: properties = forProperties
    if stage is None: stage = atStage
    if block is None and withBlock is not None: block = withBlock
    try:
      iterator = iter(properties)
    except TypeError:
      properties = [properties]
    for aProperty in properties:
      self.blockEnabler(aProperty)
    blockInstance = ParticleModifierBlock(properties, stage, block)
    self.particleModifierBlocks.append(blockInstance)
    self.ID.addModifierForProperties_atStage_withBlock_(properties, stage.value, blockInstance.blockCode)            
  addModifier = addModifierForProperties
  
  def removeModifiersOfStage(self, stage=None, ofStage=None):
    if stage is None: stage = ofStage
    self.particleModifierBlocks = [aBlock for aBlock in self.particleModifierBlocks if aBlock.stage != stage]
    self.ID.removeModifiersOfStage_(stage.value)    
  removeModifiers = removeModifiersOfStage
  
  def removeAllModifiers(self):
    self.particleModifierBlocks = []
    self.ID.removeAllModifiers()
  
  
class ParticleEventBlock:
  ## for this to work you have to set the corresponding property variation value to anything but the default! Apple bug:
  ## done via self.blockEnabler(aProperty)
  def __init__(self, event, properties, block):
    self.blockCode = ObjCBlock(self.blockInterface, restype=None, argtypes=[c_void_p, POINTER(c_void_p), POINTER(c_size_t), POINTER(c_uint32), NSInteger])
    self.event = event
    if event == ParticleEvent.Birth:
      self.pInd = lambda ind, partInd: partInd
    else:
      self.pInd = lambda ind, partInd: ind[partInd]
    self.properties = properties
    self.propertyNumber = len(properties)
    self.pCode = block
    
  def blockInterface(self, _cmd, xData, dataStride, indicies, count):
    for particleIndex in range(count):
      pInd = self.pInd(indicies, particleIndex)
      for aPropertyIndex in range(self.propertyNumber):
        offset = dataStride[aPropertyIndex] * pInd
        propAddr = xData[aPropertyIndex] + offset
        prop = cast(propAddr, POINTER(c_float))
        self.pCode(prop, self.properties[aPropertyIndex], particleIndex)
        
class ParticleModifierBlock:
  ## for this to work you have to set the corresponding property variation value to anything but the default! Apple bug:
  ## done via self.blockEnabler(aProperty)
  def __init__(self, properties, stage, block):
    self.blockCode = ObjCBlock(self.blockInterface, restype=None, argtypes=[c_void_p, POINTER(c_void_p), POINTER(c_size_t), NSInteger, NSInteger, c_float])
    self.properties = properties
    self.propertyNumber = len(properties)
    self.stage = stage
    self.pCode = block
    
  def blockInterface(self, _cmd, xData, dataStride, start, end, deltaTime):
    for particleIndex in range(start, end):
      for aPropertyIndex in range(self.propertyNumber):
        offset = dataStride[aPropertyIndex] * particleIndex
        propAddr = xData[aPropertyIndex] + offset
        prop = cast(propAddr, POINTER(c_float))
        self.pCode(prop, self.properties[aPropertyIndex], particleIndex, deltaTime)
      

class ParticlePropertyController(CInst):
  def __init__(self, animation=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      if isinstance(animation, sceneKit.CoreAnimation):
        animation = animation.ID
      self.ID = SCNParticlePropertyController.controllerWithAnimation_(animation)
      
  @classmethod
  def controllerWithAnimation(cls, animation=None):
    return cls(animation=animation)
    
  def setAnimation(self, anAnimation):
    if isinstance(anAnimation, sceneKit.CoreAnimation):
      anAnimation = anAnimation.ID
    self.ID.setAnimation_(anAnimation)    
  def getAnimation(self):
    return sceneKit.CoreAnimation.outof(self.ID.animation())
  animation = property(getAnimation, setAnimation)
  
  def setInputMode(self, aMode):
    self.ID.setInputMode_(aMode.value)    
  def getInputMode(self):
    return ParticleInputMode(self.ID.inputMode())
  inputMode = property(getInputMode, setInputMode)
  
  def setInputBias(self, aBias):
    self.ID.setInputBias_(aBias)    
  def getInputBias(self):
    return self.ID.inputBias()
  inputBias = property(getInputBias, setInputBias)
  
  def setInputScale(self, aScale):
    self.ID.setInputScale_(aScale)    
  def getInputScale(self):
    return self.ID.inputScale()
  inputScale = property(getInputScale, setInputScale)
  
  def setInputOrigin(self, aNode):
    self.ID.setInputOrigin_(aNode.ID)    
  def getInputOrigin(self):
    return sceneKit.Node.outof(self.ID.inputOrigin())
  inputOrigin = property(getInputOrigin, setInputOrigin)
  
  def setInputProperty(self, aProperty):
    i = _particleProperties.index(aProperty)
    self.ID.setInputProperty_(aProperty)    
  def getInputProperty(self):
    return str(self.ID.inputProperty())
  inputProperty = property(getInputProperty, setInputProperty)
  
  
