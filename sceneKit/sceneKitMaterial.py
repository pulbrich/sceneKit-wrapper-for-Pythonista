'''material modul, to be included in sceneKit'''

from ui import parse_color, Image
from collections import OrderedDict, Iterable

import sceneKit
from .sceneKitEnv import *
from .sceneKitAnimation import *

_lightingModels = []
for aModel in ['SCNLightingModelBlinn', 'SCNLightingModelConstant', 'SCNLightingModelLambert', 'SCNLightingModelPhong', 'SCNLightingModelPhysicallyBased']:
  _lightingModels.append(str(ObjCInstance(c_void_p.in_dll(c, aModel))))

SCNLightingModelBlinn, SCNLightingModelConstant, SCNLightingModelLambert, SCNLightingModelPhong, SCNLightingModelPhysicallyBased = _lightingModels
LightingModelBlinn, LightingModelConstant, LightingModelLambert, LightingModelPhong, \
LightingModelPhysicallyBased = _lightingModels

class WrapMode(Enum):
  Clamp = 1
  Repeat = 2
  ClampToBorder = 3
  Mirror = 4
  SCNWrapModeClamp = 1
  SCNWrapModeRepeat = 2
  SCNWrapModeClampToBorder = 3
  SCNWrapModeMirror = 4
  
Clamp = WrapMode.Clamp
Repeat = WrapMode.Repeat
ClampToBorder = WrapMode.ClampToBorder
Mirror = WrapMode.Mirror

class FilterMode(Enum):
  ModeNone = 0
  Nearest = 1
  Linear = 2
  SCNFilterModeNone = 0
  SCNFilterModeNearest = 1
  SCNFilterModeLinear = 2
  
class ColorMask(Flag):
  MaskNone = 0
  Alpha = (0x1 << 0)
  Blue = (0x1 << 1)
  Green = (0x1 << 2)
  Red = (0x1 << 3)
  All = Alpha | Blue | Green | Red
  SCNColorMaskNone = 0
  SCNColorMaskAlpha = (0x1 << 0)
  SCNColorMaskBlue = (0x1 << 1)
  SCNColorMaskGreen = (0x1 << 2)
  SCNColorMaskRed = (0x1 << 3)
  SCNColorMaskAll = Alpha | Blue | Green | Red
  
class TransparencyMode(Enum):
  AOne = 0
  Default = 0
  RGBZero = 1
  SingleLayer = 2
  DualLayer = 3
  SCNTransparencyModeAOne = 0
  SCNTransparencyModeDefault = 0
  SCNTransparencyModeRGBZero = 1
  SCNTransparencyModeSingleLayer = 2
  SCNTransparencyModeDualLayer = 3
  
class BlendMode(Enum):
  Alpha = 0
  Add = 1
  Subtract = 2
  Multiply = 3
  Screen = 4
  Replace = 5
  Max = 6
  SCNBlendModeAlpha = 0
  SCNBlendModeAdd = 1
  SCNBlendModeSubtract = 2
  SCNBlendModeMultiply = 3
  SCNBlendModeScreen = 4
  SCNBlendModeReplace = 5
  SCNBlendModeMax = 6

class CullMode(Enum):
  Back = 0
  Front = 1
  SCNCullModeBack = 0
  SCNCullModeFront = 1
  
CullBack = CullMode.Back
CullFront = CullMode.Front

class FillMode(Enum):
  Fill = 0
  Lines = 1
  SCNFillModeFill = 0
  SCNFillModeLines = 1
  
class Material(Animatable, CInst):
  def __init__(self, mdlMaterial=None, ID=None):
    if ID is not None:
      self.ID = ID
    elif mdlMaterial is not None:
      self.ID = SCNMaterial.materialWithMDLMaterial_(mdlMaterial)
      if self.ID is None:
        raise RuntimeError('materialWithMDLMaterial failed. Wrong MDL asset?')
    else:
      self.ID = SCNMaterial.material()
    
  @classmethod
  def material(cls):
    return cls()
    
  @classmethod
  def materialWithMDLMaterial(cls, mdlMaterial=None):
    return cls(mdlMaterial=mdlMaterial)
    
  def setName(self, aString):
    self.ID.setName_(aString)    
  def getName(self):
    return str(self.ID.name())
  name = property(getName, setName)
  
  def setContents(self, aContent):
    self.diffuse.contents = aContent
  def getContents(self):
    return self.diffuse.contents
  contents = property(getContents, setContents)
  
  def setLightingModelName(self, aName):
    if aName[:3] != 'SCN': aName = 'SCN'+aName
    self.ID.setLightingModelName_(aName)    
  def getLightingModelName(self):
    return str(self.ID.lightingModelName())[3:]
  lightingModelName = property(getLightingModelName, setLightingModelName)
   
  def getDiffuse(self):
    return sceneKit.MaterialProperty.outof(self.ID.diffuse())
  diffuse = property(getDiffuse, None)
  
  def getMetalness(self):
    return sceneKit.MaterialProperty.outof(self.ID.metalness())
  metalness = property(getMetalness, None)
  
  def getRoughness(self):
    return sceneKit.MaterialProperty.outof(self.ID.roughness())
  roughness = property(getRoughness, None)
    
  def getNormal(self):
    return sceneKit.MaterialProperty.outof(self.ID.normal())
  normal = property(getNormal, None)
  
  def getDisplacement(self):
    return sceneKit.MaterialProperty.outof(self.ID.displacement())
  displacement = property(getDisplacement, None)
  
  def getEmission(self):
    return sceneKit.MaterialProperty.outof(self.ID.emission())
  emission = property(getEmission, None)
  
  def getSelfIllumination(self):
    return sceneKit.MaterialProperty.outof(self.ID.selfIllumination())
  selfIllumination = property(getSelfIllumination, None)
  
  def getAmbientOcclusion(self):
    return sceneKit.MaterialProperty.outof(self.ID.ambientOcclusion())
  ambientOcclusion = property(getAmbientOcclusion, None)
  
  def getDiffuse(self):
    return sceneKit.MaterialProperty.outof(self.ID.diffuse())
  diffuse = property(getDiffuse, None)
   
  def getAmbient(self):
    return sceneKit.MaterialProperty.outof(self.ID.ambient())
  ambient = property(getAmbient, None)
     
  def getSpecular(self):
    return sceneKit.MaterialProperty.outof(self.ID.specular())
  specular = property(getSpecular, None)

  def getReflective(self):
    return scenekit.MaterialProperty.outof(self.ID.reflective())
  reflective = property(getReflective, None)
  
  def getMultiply(self):
    return sceneKit.MaterialProperty.outof(self.ID.multiply())
  multiply = property(getMultiply, None)
  
  def getTransparent(self):
    return sceneKit.MaterialProperty.outof(self.ID.transparent())
  transparent = property(getTransparent, None)
  
  def setShininess(self, aShineniness):
    self.ID.setShininess_(aShineniness)    
  def getShininess(self):
    return self.ID.shininess()
  shininess = property(getShininess, setShininess)
  
  def setFresnelExponent(self, anExponent):
    self.ID.setFresnelExponent_(anExponent)    
  def getFresnelExponent(self):
    return self.ID.fresnelExponent()
  fresnelExponent = property(getFresnelExponent, setFresnelExponent)
  
  def setLocksAmbientWithDiffuse(self, aBool):
    self.ID.setLocksAmbientWithDiffuse_(aBool)    
  def getLocksAmbientWithDiffuse(self):
    return self.ID.locksAmbientWithDiffuse()
  locksAmbientWithDiffuse = property(getLocksAmbientWithDiffuse, setLocksAmbientWithDiffuse)
  
  def setTransparency(self, aTransparency):
    self.ID.setTransparency_(aTransparency)    
  def getTransparency(self):
    return self.ID.transparency()
  transparency = property(getTransparency, setTransparency)
  
  def setTransparencyMode(self, aTransparencyMode):
    self.ID.setTransparencyMode_(aTransparencyMode.value)
  def getTransparencyMode(self):
    return TransparencyMode(self.ID.transparencyMode())
  transparencyMode = property(getTransparencyMode, setTransparencyMode)
  
  def setBlendMode(self, aBlendMode):
    self.ID.setBlendMode_(aBlendMode.value)
  def getBlendMode(self):
    return BlendMode(self.ID.blendMode())
  blendMode = property(getBlendMode, setBlendMode)
  
  def setLitPerPixel(self, aBool):
    self.ID.setLitPerPixel_(aBool)    
  def getLitPerPixel(self):
    return self.ID.litPerPixel()
  litPerPixel = property(getLitPerPixel, setLitPerPixel)
  
  def setDoubleSided(self, aBool):
    self.ID.setDoubleSided_(aBool)    
  def isDoubleSided(self):
    return self.ID.doubleSided()
  doubleSided = property(isDoubleSided, setDoubleSided)
  
  def setCullMode(self, aCullMode):
    self.ID.setCullMode_(aCullMode.value)
  def getCullMode(self):
    return CullMode(self.ID.cullMode())
  cullMode = property(getCullMode, setCullMode)
  
  def setFillMode(self, aFillMode):
    self.ID.setFillMode_(aFillMode.value)
  def getFillMode(self):
    return FillMode(self.ID.fillMode())
  fillMode = property(getFillMode, setFillMode)
  
  def setWritesToDepthBuffer(self, aBool):
    self.ID.setWritesToDepthBuffer_(aBool)    
  def getWritesToDepthBuffer(self):
    return self.ID.writesToDepthBuffer()
  writesToDepthBuffer = property(getWritesToDepthBuffer, setWritesToDepthBuffer)
  
  def setReadsFromDepthBuffer(self, aBool):
    self.ID.setReadsFromDepthBuffer_(aBool)    
  def getReadsFromDepthBuffer(self):
    return self.ID.readsFromDepthBuffer()
  readsFromDepthBuffer = property(getReadsFromDepthBuffer, setReadsFromDepthBuffer)
  
  def setColorBufferWriteMask(self, aColorBufferWriteMask):
    self.ID.setColorBufferWriteMask_(_colorMasks.index(aColorBufferWriteMask))
  def getColorBufferWriteMask(self):
    return _colorMasks[self.ID.colorBufferWriteMask()]
  colorBufferWriteMask = property(getColorBufferWriteMask, setColorBufferWriteMask)
  
class MaterialProperty(Animatable, CInst):
  def __init__(self, contents=None, ID=None):
    if contents is not None:
      self.ID = SCNMaterialProperty.materialPropertyWithContents_(contents)
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = None
      
  @classmethod    
  def materialPropertyWithContents(cls, contents=None):
    return cls(contents=contents)
  
  def setContents(self, aContent):
    self.ID.setContents_(contentFromPy(aContent))
  def getContents(self):
    contents = self.ID.contents()
    return contentFromC(contents)
  contents = property(getContents, setContents)

  def setIntensity(self, anIntensity):
    self.ID.setIntensity_(anIntensity)    
  def getIntensity(self):
    return self.ID.intensity()
  intensity = property(getIntensity, setIntensity)
  
  def setContentsTransform(self, aTransform):
    self.ID.setContentsTransform_(matrix4Make(aTransform))
  def getContentsTransform(self):
    trans = self.ID.contentsTransform()
    return matrix4Make(getCStructValuesAsList(trans))
  contentsTransform = property(getContentsTransform, setContentsTransform)
  
  def setWrapS(self, aWrapMode):
    self.ID.setWrapS_(aWrapMode.value)
  def getWrapS(self):
    return WrapMode(self.ID.wrapS())
  wrapS = property(getWrapS, setWrapS)
  
  def setWrapT(self, aWrapMode):
    self.ID.setWrapT_(aWrapMode.value)
  def getWrapT(self):
    return WrapMode(self.ID.wrapT())
  wrapT = property(getWrapT, setWrapT)
  
  def setMinificationFilter(self, aFilter):
    self.ID.setMinificationFilter_(aFilter.value)
  def getMinificationFilter(self):
    return FilterMode(self.ID.minificationFilter())
  minificationFilter = property(getMinificationFilter, setMinificationFilter)

  def setMagnificationFilter(self, aFilter):
    self.ID.setMagnificationFilter_(aFilter.value)
  def getMagnificationFilter(self):
    return FilterMode(self.ID.magnificationFilter())
  magnificationFilter = property(getMagnificationFilter, setMagnificationFilter)
  
  def setMipFilter(self, aFilter):
    self.ID.setMipFilter_(aFilter.value)
  def getMipFilter(self):
    return FilterMode(self.ID.mipFilter())
  mipFilter = property(getMipFilter, setMipFilter)
  
  def setMaxAnisotropy(self, anAnisotropy):
    self.ID.setMaxAnisotropy_(anAnisotropy)    
  def getMaxAnisotropy(self):
    return self.ID.maxAnisotropy()
  maxAnisotropy = property(getMaxAnisotropy, setMaxAnisotropy)
  
  def setMappingChannel(self, aChannel):
    self.ID.setMappingChannel_(aChannel)    
  def getMappingChannel(self):
    return self.ID.mappingChannel()
  mappingChannel = property(getMappingChannel, setMappingChannel)
  
  def setTextureComponents(self, flags):
    if not isinstance(flags, Iterable):
      flags = [flags]
    mask = 0
    for aFlag in flags:
      mask = mask | aFlag.value
    self.ID.setTextureComponents_(mask)
  def getTextureComponents(self):
    mask = self.ID.textureComponents()
    flags = []
    for aFlag in ColorMask:
      if (mask & aFlag.value) != 0: flags.append(aFlag)
    if len(flags) == 5: flags = [ColorMask.All]
    elif len(flags) == 0: flags = [ColorMask.MaskNone]
    return tuple(flags)
  textureComponents = property(getTextureComponents, setTextureComponents)
