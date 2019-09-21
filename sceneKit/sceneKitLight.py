'''light modul, to be included in sceneKit'''

from ui import parse_color

import sceneKit
from .sceneKitEnv import *
from .sceneKitMaterial import *
from .sceneKitAnimation import *

_lightTypes = []
for aLightType in ['SCNLightTypeIES', 'SCNLightTypeAmbient', 'SCNLightTypeDirectional', 'SCNLightTypeOmni', 'SCNLightTypeProbe', 'SCNLightTypeSpot']:
  _lightTypes.append(str(ObjCInstance(c_void_p.in_dll(c, aLightType))))
_lightTypes = tuple(_lightTypes)

SCNLightTypeIES, SCNLightTypeAmbient, SCNLightTypeDirectional, \
SCNLightTypeOmni, SCNLightTypeProbe, SCNLightTypeSpot = _lightTypes
LightTypeIES, LightTypeAmbient, LightTypeDirectional, \
LightTypeOmni, LightTypeProbe, LightTypeSpot = _lightTypes

class ShadowMode(Enum):
  Forward = 0
  Deferred = 1
  Modulated = 2
  SCNShadowModeForward = 0
  SCNShadowModeDeferred = 1
  SCNShadowModeModulated = 2


class Light(Animatable, CInst):
  def __init__(self, mdlLight=None, ID=None):
    if ID is not None:
      self.ID = ID
    elif mdlLight is not None:
      self.ID = SCNLight.lightWithMDLLight_(mdlLight)
      if self.ID is None:
        raise RuntimeError('lightWithMDLLight failed. Wrong MDL asset?')   
    else:
      self.ID = SCNLight.light()
    
  @classmethod
  def light(cls):
    return cls()
    
  @classmethod
  def lightWithMDLLight(cls, mdlLight=None):
    return cls(mdlLight=mdlLight)

  def setName(self, aString):
    self.ID.setName_(aString)    
  def getName(self):
    return str(self.ID.name())
  name = property(getName, setName)
  
  def setType(self, aLightType):
    self.ID.setType_(aLightType)    
  def getType(self):
    return self.ID.type()
  type = property(getType, setType)
  
  def setColor(self, aColor):
    r, g, b, a = parse_color(aColor)
    self.ID.setColor_(UIColor.color(red=r, green=g, blue=b, alpha=a)) 
  def getColor(self):
    color = self.ID.color()
    return RGBA(color.red(), color.green(), color.blue(), color.alpha())
  color = property(getColor, setColor)

  def setTemperature(self, aTemp):
    self.ID.setTemperature_(aTemp)    
  def getTemperature(self):
    return self.ID.temperature()
  temperature = property(getTemperature, setTemperature)
  
  def setIntensity(self, anIntensity):
    self.ID.setIntensity_(anIntensity)    
  def getIntensity(self):
    return self.ID.intensity()
  intensity = property(getIntensity, setIntensity)
   
  def getSphericalHarmonicsCoefficients(self):
    return self.ID.sphericalHarmonicsCoefficients()
  sphericalHarmonicsCoefficients = property(getSphericalHarmonicsCoefficients, None)

  def setAttenuationStartDistance(self, aDistance):
    self.ID.setAttenuationStartDistance_(aDistance)    
  def getAttenuationStartDistance(self):
    return self.ID.attenuationStartDistance()
  attenuationStartDistance = property(getAttenuationStartDistance, setAttenuationStartDistance)
  
  def setAttenuationEndDistance(self, aDistance):
    self.ID.setAttenuationEndDistance_(aDistance)    
  def getAttenuationEndDistance(self):
    return self.ID.attenuationEndDistance()
  attenuationEndDistance = property(getAttenuationEndDistance, setAttenuationEndDistance)
  
  def setAttenuationFalloffExponent(self, aFallOff):
    self.ID.setAttenuationFalloffExponent_(aFallOff)    
  def getAttenuationFalloffExponent(self):
    return self.ID.attenuationFalloffExponent()
  attenuationFalloffExponent = property(getAttenuationFalloffExponent, setAttenuationFalloffExponent)
  
  def setSpotInnerAngle(self, anAngle):
    self.ID.setSpotInnerAngle_(anAngle)    
  def getSpotInnerAngle(self):
    return self.ID.spotInnerAngle()
  spotInnerAngle = property(getSpotInnerAngle, setSpotInnerAngle)
  
  def setSpotOuterAngle(self, anAngle):
    self.ID.setSpotOuterAngle_(anAngle)    
  def getSpotOuterAngle(self):
    return self.ID.spotOuterAngle()
  spotOuterAngle = property(getSpotOuterAngle, setSpotOuterAngle)
  
  def setCastsShadow(self, aBool):
    self.ID.setCastsShadow_(aBool)    
  def getCastsShadow(self):
    return self.ID.castsShadow()
  castsShadow = property(getCastsShadow, setCastsShadow)
  
  def setShadowRadius(self, aRadius):
    self.ID.setShadowRadius_(aRadius)    
  def getShadowRadius(self):
    return self.ID.shadowRadius()
  shadowRadius = property(getShadowRadius, setShadowRadius)
  
  def setShadowColor(self, aColor):
    r, g, b, a = parse_color(aColor)
    self.ID.setShadowColor_(ObjCClass('UIColor').color(red=r, green=g, blue=b, alpha=a)) 
  def getShadowColor(self):
    color = self.ID.shadowColor()
    return RGBA(color.red(), color.green(), color.blue(), color.alpha())
  shadowColor = property(getShadowColor, setShadowColor)
  
  def setShadowMapSize(self, aGCSize):
    self.ID.setShadowMapSize_(aGCSize)    
  def getShadowMapSize(self):
    map = self.ID.shadowMapSize()
    return Size(map.width, map.height)
  shadowMapSize = property(getShadowMapSize, setShadowMapSize)

  def setShadowSampleCount(self, aCount):
    self.ID.setShadowSampleCount_(aCount)    
  def getShadowSampleCount(self):
    return self.ID.shadowSampleCount()
  shadowSampleCount = property(getShadowSampleCount, setShadowSampleCount)
  
  def setShadowMode(self, aMode):
    self.ID.setShadowMode_(aMode.value)
  def getShadowMode(self):
    return ShadowMode(self.ID.shadowMode())
  shadowMode = property(getShadowMode, setShadowMode)

  def setShadowBias(self, aBias):
    self.ID.setShadowBias_(aBias)    
  def getShadowBias(self):
    return self.ID.shadowBias()
  shadowBias = property(getShadowBias, setShadowBias)
  
  def setOrthographicScale(self, aScale):
    self.ID.setOrthographicScale_(aScale)    
  def getOrthographicScale(self):
    return self.ID.orthographicScale()
  orthographicScale = property(getOrthographicScale, setOrthographicScale)
  
  def setZFar(self, aDistance):
    self.ID.setZFar_(aDistance)    
  def getZFar(self):
    return self.ID.zFar()
  zFar = property(getZFar, setZFar)
  
  def setZNear(self, aDistance):
    self.ID.setZNear_(aDistance)    
  def getZNear(self):
    return self.ID.zNear()
  zNear = property(getZNear, setZNear)
  
  def setCategoryBitMask(self, aBitMask):
    self.ID.setCategoryBitMask_(aBitMask)    
  def getCategoryBitMask(self):
    return self.ID.categoryBitMask()
  categoryBitMask = property(getCategoryBitMask, setCategoryBitMask)
  
  def setIESProfileURL(self, anURL):
    self.ID.setIESProfileURL_(nsurl(anURL))
  def getIESProfileURL(self):
    return str(self.ID.IESProfileURL().absoluteString())
  IESProfileURL = property(getIESProfileURL, setIESProfileURL)
  
  def setAutomaticallyAdjustsShadowProjection(self, aBool):
    self.ID.setAutomaticallyAdjustsShadowProjection_(aBool)    
  def getAutomaticallyAdjustsShadowProjection(self):
    return self.ID.automaticallyAdjustsShadowProjection()
  automaticallyAdjustsShadowProjection = property(getAutomaticallyAdjustsShadowProjection, setAutomaticallyAdjustsShadowProjection)
  
  def setForcesBackFaceCasters(self, aBool):
    self.ID.setForcesBackFaceCasters_(aBool)    
  def getForcesBackFaceCasters(self):
    return self.ID.forcesBackFaceCasters()
  forcesBackFaceCasters = property(getForcesBackFaceCasters, setForcesBackFaceCasters)

  def setMaximumShadowDistance(self, aDistance):
    self.ID.setMaximumShadowDistance_(aDistance)    
  def getMaximumShadowDistance(self):
    return self.ID.maximumShadowDistance()
  maximumShadowDistance = property(getMaximumShadowDistance, setMaximumShadowDistance)
  
  def setSampleDistributedShadowMaps(self, aBool):
    self.ID.setSampleDistributedShadowMaps_(aBool)    
  def getSampleDistributedShadowMaps(self):
    return self.ID.sampleDistributedShadowMaps()
  sampleDistributedShadowMaps = property(getSampleDistributedShadowMaps, setSampleDistributedShadowMaps)
  
  def setShadowCascadeCount(self, aCount):
    self.ID.setShadowCascadeCount_(aCount)    
  def getShadowCascadeCount(self):
    return self.ID.shadowCascadeCount()
  shadowCascadeCount = property(getShadowCascadeCount, setShadowCascadeCount)
  
  def setShadowCascadeSplittingFactor(self, aFactor):
    self.ID.setShadowCascadeSplittingFactor_(aFactor)    
  def getShadowCascadeSplittingFactor(self):
    return self.ID.shadowCascadeSplittingFactor()
  shadowCascadeSplittingFactor = property(getShadowCascadeSplittingFactor, setShadowCascadeSplittingFactor)
  
  def setGobo(self, aMaterialProperty):
    self.ID.setGobo_(aMaterialProperty._materialProperty)    
  def getGobo(self):
    return sceneKit.MaterialProperty.outof(self.ID.gobo())
  gobo = property(getGobo, setGobo)
