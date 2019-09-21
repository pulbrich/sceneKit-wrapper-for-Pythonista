'''geometry module for sceneKit'''

import ctypes
from objc_util import *

import sceneKit
from .sceneKitEnv import *
from .sceneKitAnimation import *
from .sceneKitMaterial import *
from .sceneKitGeometrySource import *

_CATextLayerAlignmentModes = []
for aMode in ['kCAAlignmentNatural', 'kCAAlignmentLeft', 'kCAAlignmentRight', 'kCAAlignmentCenter', 'kCAAlignmentJustified']:
  _CATextLayerAlignmentModes.append(str(ObjCInstance(c_void_p.in_dll(c, aMode))))
_CATextLayerAlignmentModes = tuple(_CATextLayerAlignmentModes)
  
kCAAlignmentNatural, kCAAlignmentLeft, kCAAlignmentRight, kCAAlignmentCenter, kCAAlignmentJustified = _CATextLayerAlignmentModes
AlignmentNatural, AlignmentLeft, AlignmentRight, AlignmentCenter, AlignmentJustified = _CATextLayerAlignmentModes

_CATextLayerTruncationModes = []
for aMode in ['kCATruncationNone', 'kCATruncationStart', 'kCATruncationEnd', 'kCATruncationMiddle']:
  _CATextLayerTruncationModes.append(str(ObjCInstance(c_void_p.in_dll(c, aMode))))
_CATextLayerTruncationModes = tuple(_CATextLayerTruncationModes)

kCATruncationNone, kCATruncationStart, kCATruncationEnd, kCATruncationMiddle = _CATextLayerTruncationModes
TruncationNone, TruncationStart, TruncationEnd, TruncationMiddle = _CATextLayerTruncationModes

class MorpherCalculationMode(Enum):
  Normalized = 0
  Additive = 1
  SCNMorpherCalculationModeNormalized = 0
  SCNMorpherCalculationModeAdditive = 1
  
class ChamferMode(Enum):
  Both = 0
  Front = 1
  Back = 2
  SCNChamferModeBoth = 0
  SCNChamferModeFront = 1
  SCNChamferModeBack = 2
  
class TessellationSmoothingMode(Enum):
  ModeNone = 0
  Triangles = 1
  Phong = 2
  SCNTessellationSmoothingModeNone = 0
  SCNTessellationSmoothingModePNTriangles = 1
  SCNTessellationSmoothingModePhong = 2
  
class TessellationPartitionMode(Enum):
  Pow2 = 0
  ModeInteger = 1
  FractionalOdd = 2
  FractionalEven = 3
  MTLTessellationPartitionModePow2 = 0
  MTLTessellationPartitionModeInteger = 1
  MTLTessellationPartitionModeFractionalOdd = 2
  MTLTessellationPartitionModeFractionalEven = 3

class Geometry(Animatable, Actionable, BoundingVolume, CInst):
  def __init__(self, geometryWithSources=None, elements=None, mdlMesh=None, ID=None):
    if geometryWithSources is not None:
      try:
        iterator = iter(geometryWithSources)
      except TypeError:
        geometryWithSources = [geometryWithSources]
      try:
        iterator = iter(elements)
      except TypeError:
        elements = [elements]
      geometryWithSources = [aSource.ID for aSource in geometryWithSources]
      elements = [anElement.ID for anElement in elements]
      self.ID = SCNGeometry.geometryWithSources_elements_(geometryWithSources, elements)
    elif mdlMesh is not None:
      self.ID = SCNGeometry.geometryWithMDLMesh_(mdlMesh)
      if self.ID is None:
        raise RuntimeError('geometryWithMDLMesh failed. Wrong MDL asset?')
    elif ID is not None:
      self.ID = ID      
    else:
      self.ID = SCNGeometry.geometry()
      
  @classmethod
  def subclassOutof(cls, ID=None):
    desc = str(ID.description())
    kind = desc[4:desc.index(':')]
    if kind == 'Text':
      return Text(ID=ID)
    elif kind == 'Shape':
      return Shape(ID=ID)
    elif kind == 'Floor':
      return Floor(ID=ID)
    elif kind == 'Box':
      return Box(ID=ID)
    elif kind == 'Capsule':
      return Capsule(ID=ID)
    elif kind == 'Cone':
      return Cone(ID=ID)
    elif kind == 'Cylinder':
      return Cylinder(ID=ID)
    elif kind == 'Plane':
      return Plane(ID=ID)
    elif kind == 'Pyramid':
      return Pyramid(ID=ID)
    elif kind == 'Sphere':
      return Sphere(ID=ID)
    elif kind == 'Torus':
      return Torus(ID=ID)
    elif kind == 'Tube':
      return Tube(ID=ID)
    else:
      return cls(ID=ID)
    
  @classmethod
  def geometry(cls):
    return cls()
    
  @classmethod
  def geometryWithSources(cls, sources=None, elements=None):
    return cls(geometryWithSources=sources, elements=elements)
    
  @classmethod
  def geometryWithMDLMesh(cls, mdlMesh=None):
    return cls(mdlMesh=mdlMesh)
    
  def setName(self, aString):
    self.ID.setName_(aString)    
  def getName(self):
    return str(self.ID.name())
  name = property(getName, setName)
  
  def setMaterials(self, materialList):
    try:
      iterator = iter(materialList)
    except TypeError:
      materialList = [materialList]
    self.ID.setMaterials_([ml.ID for ml in materialList])    
  def getMaterials(self):
    return tuple([sceneKit.Material.outof(ml) for ml in self.ID.materials()])
  materials = property(getMaterials, setMaterials)
  
  def setFirstMaterial(self, aMaterial):
    self.ID.setFirstMaterial_(aMaterial.ID)    
  def getFirstMaterial(self):
    return sceneKit.Material.outof(self.ID.firstMaterial())
  firstMaterial = property(getFirstMaterial, setFirstMaterial)
  
  def getGeometryElements(self):
    elements = self.ID.geometryElements()
    if elements is None: return None
    return tuple([sceneKit.GeometryElement.outof(anElement) for anElement in elements])
  geometryElements = property(getGeometryElements, None)
  
  def getGeometrySources(self):
    sources = self.ID.geometrySources()
    if sources is None: return None
    return tuple([sceneKit.GeometrySource.outof(aSource) for aSource in sources])
  geometrySources = property(getGeometrySources, None)
  
  def getGeometryElementCount(self):
    return self.ID.geometryElementCount()
  geometryElementCount = property(getGeometryElementCount, None)
  
  def geometryElementAtIndex(self, index=0):
    return sceneKit.GeometryElement.outof(self.ID.geometryElementAtIndex_(index))
  geometryElementAt = geometryElementAtIndex
  
  def geometrySourcesForSemantic(self, semantic=None):
    return tuple([scenekit.GeometrySource.outof(aSource) for aSource in self.ID.geometrySourcesForSemantic_(semantic)])
  geometrySourcesFor = geometrySourcesForSemantic
  
  def setLevelsOfDetail(self, levels):
    self.ID.setLevelsOfDetail_([aLevel.ID for aLevel in levels])    
  def getLevelsOfDetail(self):
    return tuple([sceneKit.LevelOfDetail.outof(aLevel) for aLevel in self.ID.levelsOfDetail()])
  levelsOfDetail = property(getLevelsOfDetail, setLevelsOfDetail)
  
  def setSubdivisionLevel(self, aLevel):
    self.ID.setSubdivisionLevel_(aLevel)    
  def getSubdivisionLevel(self):
    return self.ID.subdivisionLevel()
  subdivisionLevel = property(getSubdivisionLevel, setSubdivisionLevel)
  
  def setEdgeCreasesElement(self, anElement):
    self.ID.setEdgeCreasesElement_(anElement.ID)    
  def getEdgeCreasesElement(self):
    return sceneKit.GeometryElement.outof(self.ID.edgeCreasesElement())
  edgeCreasesElement = property(getEdgeCreasesElement, setEdgeCreasesElement)
  
  def setEdgeCreasesSource(self, aSource):
    self.ID.setEdgeCreasesSource_(aSource.ID)    
  def getEdgeCreasesSource(self):
    return sceneKit.GeometrySource.outof(self.ID.edgeCreasesSource())
  edgeCreasesSource = property(getEdgeCreasesSource, setEdgeCreasesSource)
  
  def setWantsAdaptiveSubdivision(self, aBool):
    self.ID.setWantsAdaptiveSubdivision_(aBool)    
  def getWantsAdaptiveSubdivision(self):
    return self.ID.wantsAdaptiveSubdivision()
  wantsAdaptiveSubdivision = property(getWantsAdaptiveSubdivision, setWantsAdaptiveSubdivision)

  
class LevelOfDetail(CInst):
  def __init__(self, geometry=None, screenSpaceRadius= None, ID=None):
    if screenSpaceRadius is not None:
      self.ID = SCNLevelOfDetail.levelOfDetailWithGeometry_screenSpaceRadius_(geometry.ID, screenSpaceRadius)
    elif worldSpaceDistance is not None:
      self.ID = SCNLevelOfDetail.levelOfDetailWithGeometry_worldSpaceDistance_(geometry.ID, worldSpaceDistance) 
    elif ID is not None:
      self.ID = ID      
    else:
      self.ID = SCNLevelOfDetail.levelOfDetail()
      
  @classmethod
  def levelOfDetailWithGeometry(cls, geometry=None, screenSpaceRadius=None, worldSpaceDistance=None):
    return cls(geometry=geometry, screenSpaceRadius=screenSpaceRadius, worldSpaceDistance=worldSpaceDistance)
    
  def getGeometry(self):
    return sceneKit.Geometry.outof(self.ID.geometry())
  geometry = property(getGeometry, None)
  
  def getScreenSpaceRadius(self):
    return self.ID.screenSpaceRadius()
  screenSpaceRadius = property(getScreenSpaceRadius, None)
  
  def getWorldSpaceDistance(self):
    return self.ID.worldSpaceDistance()
  worldSpaceDistance = property(getWorldSpaceDistance, None)
  
  def setTessellator(self, aTessellator):
    self.ID.setTessellator_(aTessellator.ID)    
  def getTessellator(self):
    return sceneKit.GeometryTessellator.outof(self.ID.tessellator())
  tessellator = property(getTessellator, setTessellator)


class GeometryTessellator(CInst):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNGeometryTessellator.alloc().init()
      
  def setSmoothingMode(self, aMode):
    self.ID.setSmoothingMode_(aMode.value)    
  def getSmoothingMode(self):
    return TessellationSmoothingMode(self.ID.smoothingMode())
  smoothingMode = property(getSmoothingMode, setSmoothingMode)
  
  def setEdgeTessellationFactor(self, aFactor):
    self.ID.setEdgeTessellationFactor_(aFactor)    
  def getEdgeTessellationFactor(self):
    return self.ID.edgeTessellationFactor()
  edgeTessellationFactor = property(getEdgeTessellationFactor, setEdgeTessellationFactor)
  
  def setInsideTessellationFactor(self, aFactor):
    self.ID.setInsideTessellationFactor_(aFactor)    
  def getInsideTessellationFactor(self):
    return self.ID.insideTessellationFactor()
  insideTessellationFactor = property(getInsideTessellationFactor, setInsideTessellationFactor)
  
  def setAdaptive(self, aBool):
    self.ID.setAdaptive_(aBool)    
  def isAdaptive(self):
    return self.ID.adaptive()
  adaptive = property(isAdaptive, setAdaptive)
  
  def setScreenSpace(self, aBool):
    self.ID.setScreenSpace_(aBool)    
  def isScreenSpace(self):
    return self.ID.screenSpace()
  screenSpace = property(isScreenSpace, setScreenSpace)
  
  def setMaximumEdgeLength(self, aFloat):
    self.ID.setMaximumEdgeLength_(aFloat)    
  def getMaximumEdgeLength(self):
    return self.ID.maximumEdgeLength()
  maximumEdgeLength = property(getMaximumEdgeLength, setMaximumEdgeLength)
  
  def setTessellationFactorScale(self, aFloat):
    self.ID.setTessellationFactorScale_(aFloat)    
  def getTessellationFactorScale(self):
    return self.ID.tessellationFactorScale()
  tessellationFactorScale = property(getTessellationFactorScale, setTessellationFactorScale)
  
  def setTessellationPartitionMode(self, aMode):
    self.ID.setTessellationPartitionMode_(aMode.value)    
  def getTessellationPartitionMode(self):
    return TessellationPartitionMode(self.ID.tessellationPartitionMode())
  tessellationPartitionMode = property(getTessellationPartitionMode, setTessellationPartitionMode)
  
      
class _GeoWidth:
  def setWidth(self, aWidth):
    self.ID.setWidth_(aWidth)    
  def getWidth(self):
    return self.ID.width()
  width = property(getWidth, setWidth)
  
  def setWidthSegmentCount(self, aCount):
    self.ID.setWidthSegmentCount_(aCount)    
  def getWidthSegmentCount(self):
    return self.ID.widthSegmentCount()
  widthSegmentCount = property(getWidthSegmentCount, setWidthSegmentCount)
  
class _GeoHeight:  
  def setHeight(self, aHeight):
    self.ID.setHeight_(aHeight)    
  def getHeight(self):
    return self.ID.height()
  height = property(getHeight, setHeight)
  
  def setHeightSegmentCount(self, aCount):
    self.ID.setHeightSegmentCount_(aCount)    
  def getHeightSegmentCount(self):
    return self.ID.heightSegmentCount()
  heightSegmentCount = property(getHeightSegmentCount, setHeightSegmentCount)
  
class _GeoLength:
  def setLength(self, aLength):
    self.ID.setLength_(aLength)    
  def getLength(self):
    return self.ID.length()
  length = property(getLength, setLength)
  
  def setLenghtSegmentCount(self, aCount):
    self.ID.setLenghtSegmentCount_(aCount)    
  def getLenghtSegmentCount(self):
    return self.ID.lenghtSegmentCount()
  lenghtSegmentCount = property(getLenghtSegmentCount, setLenghtSegmentCount)
  
class _GeoRadius:
  def setRadius(self, aRadius):
    self.ID.setRadius_(aRadius)    
  def getRadius(self):
    return self.ID.radius()
  radius = property(getRadius, setRadius)
  
class _GeoRadialSegmentCount:
  def setRadialSegmentCount(self, aCount):
    self.ID.setRadialSegmentCount_(aCount)    
  def getRadialSegmentCount(self):
    return self.ID.radialSegmentCount()
  radialSegmentCount = property(getRadialSegmentCount, setRadialSegmentCount)
  
class Floor(Geometry):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNFloor.floor()
      
  @classmethod
  def floor(cls):
    return cls()
  
  def setWidth(self, aWidth):
    self.ID.setWidth_(aWidth)    
  def getWidth(self):
    return self.ID.width()
  width = property(getWidth, setWidth)
  
  def setLength(self, aLength):
    self.ID.setLength_(aLength)    
  def getLength(self):
    return self.ID.length()
  length = property(getLength, setLength)  
  
  def setReflectivity(self, aReflectivity):
    self.ID.setReflectivity_(aReflectivity)    
  def getReflectivity(self):
    return self.ID.reflectivity()
  reflectivity = property(getReflectivity, setReflectivity)
  
  def setReflectionFalloffEnd(self, aFallOff):
    self.ID.setReflectionFalloffEnd_(aFallOff)    
  def getReflectionFalloffEnd(self):
    return self.ID.reflectionFalloffEnd()
  reflectionFalloffEnd = property(getReflectionFalloffEnd, setReflectionFalloffEnd)
  
  def setReflectionFalloffStart(self, aFallOff):
    self.ID.setReflectionFalloffStart_(aFallOff)    
  def getReflectionFalloffStart(self):
    return self.ID.reflectionFalloffStart()
  reflectionFalloffStart = property(getReflectionFalloffStart, setReflectionFalloffStart)
  
  def setReflectionResolutionScaleFactor(self, aFactor):
    self.ID.setReflectionResolutionScaleFactor_(aFactor)    
  def getReflectionResolutionScaleFactor(self):
    return self.ID.reflectionResolutionScaleFactor()
  reflectionResolutionScaleFactor = property(getReflectionResolutionScaleFactor, setReflectionResolutionScaleFactor)

  def setReflectionCategoryBitMask(self, aBitMask):
    self.ID.setReflectionCategoryBitMask_(aBitMask)    
  def getReflectionCategoryBitMask(self):
    return self.ID.reflectionCategoryBitMask()
  reflectionCategoryBitMask = property(getReflectionCategoryBitMask, setReflectionCategoryBitMask)
        
class Plane(Geometry, _GeoHeight, _GeoWidth):
  def __init__(self, width=0.0, height=0.0, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNPlane.planeWithWidth_height_(width, height)
      
  @classmethod
  def planeWithWidth(cls, width=0.0, height=0.0):
    return cls(width=width, height=height)
  
  def setCornerRadius(self, aRadius):
    self.ID.setCornerRadius_(aRadius)    
  def getCornerRadius(self):
    return self.ID.cornerRadius()
  cornerRadius = property(getCornerRadius, setCornerRadius)
  
  def setCornerRadiusSegmentCount(self, aCount):
    self.ID.setCornerRadiusSegmentCount_(aCount)    
  def getCornerRadiusSegmentCount(self):
    return self.ID.cornerRadiusSegmentCount()
  cornerRadiusSegmentCount = property(getCornerRadiusSegmentCount, setCornerRadiusSegmentCount)
  
class Box(Geometry, _GeoHeight, _GeoWidth, _GeoLength):
  def __init__(self, width=0.0, height=0.0, length=0.0, chamferRadius=0.0, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNBox.boxWithWidth_height_length_chamferRadius_(width, height, length, chamferRadius)
      
  @classmethod
  def boxWithWidth(cls, width=0.0, height=0.0, length=0.0, chamferRadius=0.0):
    return cls(width=width, height=height, length=length, chamferRadius=chamferRadius)
  
  def setChamferRadius(self, aRadius):
    self.ID.setChamferRadius_(aRadius)    
  def getChamferRadius(self):
    return self.ID.chamferRadius()
  chamferRadius = property(getChamferRadius, setChamferRadius)
  
  def setChamferRadiusSegmentCount(self, aCount):
    self.ID.setChamferRadiusSegmentCount_(aCount)    
  def getChamferRadiusSegmentCount(self):
    return self.ID.chamferRadiusSegmentCount()
  chamferRadiusSegmentCount = property(getChamferRadiusSegmentCount, setChamferRadiusSegmentCount)
  
class Capsule(Geometry, _GeoHeight, _GeoRadialSegmentCount):
  def __init__(self, capRadius=0.0, height=0.0, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNCapsule.capsuleWithCapRadius_height_(capRadius, height)
      
  @classmethod
  def capsuleWithCapRadius(cls, capRadius=0.0, height=0.0):
    return cls(capRadius=capRadius, height=height)
  
  def setCapRadius(self, aRadius):
    self.ID.setCapRadius_(aRadius)    
  def getCapRadius(self):
    return self.ID.capRadius()
  capRadius = property(getCapRadius, setCapRadius)
  
  def setCapSegmentCount(self, aCount):
    self.ID.setCapSegmentCount_(aCount)    
  def getCapSegmentCount(self):
    return self.ID.capSegmentCount()
  capSegmentCount = property(getCapSegmentCount, setCapSegmentCount)
  
class Cone(Geometry, _GeoHeight, _GeoRadialSegmentCount):
  def __init__(self, topRadius=0.0, bottomRadius=0.0, height=0.0, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNCone.coneWithTopRadius_bottomRadius_height_(topRadius, bottomRadius, height)
      
  @classmethod
  def coneWithTopRadius(cls, topRadius=0.0, bottomRadius=0.0, height=0.0):
    return cls(topRadius=topRadius, bottomRadius=bottomRadius, height=height)
    
  def setTopRadius(self, aRadius):
    self.ID.setTopRadius_(aRadius)    
  def getTopRadius(self):
    return self.ID.topRadius()
  topRadius = property(getTopRadius, setTopRadius)
  
  def setBottomRadius(self, aRadius):
    self.ID.setBottomRadius_(aRadius)    
  def getBottomRadius(self):
    return self.ID.bottomRadius()
  bottomRadius = property(getBottomRadius, setBottomRadius)
  
class Cylinder(Geometry, _GeoRadius, _GeoHeight, _GeoRadialSegmentCount):
  def __init__(self, radius=0.0, height=0.0, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNCylinder.cylinderWithRadius_height_(radius, height)
      
  @classmethod
  def cylinderWithRadius(cls, radius=0.0, height=0.0):
    return cls(radius=radius, height=height)
  
class Pyramid(Geometry, _GeoHeight, _GeoWidth, _GeoLength):
  def __init__(self, width=0.0, height=0.0, length=0.0, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNPyramid.pyramidWithWidth_height_length_(width, height, length)
      
  @classmethod
  def pyramidWithWidth(cls, width=0.0, height=0.0, length=0.0):
    return cls(width=width, height=height, length=length)
    
class Sphere(Geometry, _GeoRadius):
  def __init__(self, radius=0.0, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNSphere.sphereWithRadius_(radius)
      
  @classmethod
  def sphereWithRadius(cls, radius=0.0):
    return cls(radius=radius)
    
  def setGeodesic(self, aBool):
    self.ID.setGeodesic_(aBool)    
  def getGeodesic(self):
    return self.ID.geodesic()
  geodesic = property(getGeodesic, setGeodesic)
  
  def setSegmentCount(self, aCount):
    self.ID.setSegmentCount_(aCount)    
  def getSegmentCount(self):
    return self.ID.segmentCount()
  segmentCount = property(getSegmentCount, setSegmentCount)
  
class Torus(Geometry):
  def __init__(self, ringRadius=0.0, pipeRadius=0.0, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNTorus.torusWithRingRadius_pipeRadius_(ringRadius, pipeRadius)
      
  @classmethod
  def torusWithRingRadius(cls, ringRadius=0.0, pipeRadius=0.0):
    return cls(ringRadius=ringRadius, pipeRadius=pipeRadius)
  
  def setRingRadius(self, aRadius):
    self.ID.setRingRadius_(aRadius)    
  def getRingRadius(self):
    return self.ID.ringRadius()
  ringRadius = property(getRingRadius, setRingRadius)
  
  def setRingSegmentCount(self, aCount):
    self.ID.setRingSegmentCount_(aCount)    
  def getRingSegmentCount(self):
    return self.ID.ringSegmentCount()
  ringSegmentCount = property(getRingSegmentCount, setRingSegmentCount)
  
  def setPipeRadius(self, aRadius):
    self.ID.setPipeRadius_(aRadius)   
  def getPipeRadius(self):
    return self.ID.pipeRadius()
  pipeRadius = property(getPipeRadius, setPipeRadius)
  
  def setPipeSegmentCount(self, aCount):
    self.ID.setPipeSegmentCount_(aCount)    
  def getPipeSegmentCount(self):
    return self.ID.pipeSegmentCount()
  pipeSegmentCount = property(getPipeSegmentCount, setPipeSegmentCount)
  
class Tube(Geometry, _GeoHeight, _GeoRadialSegmentCount):
  def __init__(self, innerRadius=0.0, outerRadius=0.0, height=0.0, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNTube.tubeWithInnerRadius_outerRadius_height_(innerRadius, outerRadius, height)
      
  @classmethod
  def tubeWithInnerRadius(cls, innerRadius=0.0, outerRadius=0.0, height=0.0):
    return cls(innerRadius=innerRadius, outerRadius=outerRadius, height=height)
    
  def setInnerRadius(self, aRadius):
    self.ID.setInnerRadius_(aRadius)    
  def getInnerRadius(self):
    return self.ID.innerRadius()
  innerRadius = property(getInnerRadius, setInnerRadius)
  
  def setOuterRadius(self, aRadius):
    self.ID.setOuterRadius_(aRadius)    
  def getOuterRadius(self):
    return self.ID.outerRadius()
  outerRadius = property(getOuterRadius, setOuterRadius)
  
class Text(Geometry):
  def __init__(self, string=None, extrusionDepth=0.0, ID=None):
    if string is not None:
      self.ID = SCNText.textWithString_extrusionDepth_(string, extrusionDepth)
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = SCNText.text()
  
  @classmethod
  def textWithString(cls, string=None, extrusionDepth=0.0):
    return cls(string=string, extrusionDepth=extrusionDepth)
    
  def setString(self, aString):
    self.ID.setString_(aString)    
  def getString(self):
    return self.ID.string()
  string = property(getString, setString)
  
  def setFont(self, aFont):
    fontName, pointSize = aFont
    if fontName == '<system>':
      aFont = UIFont.systemFontOfSize_(pointSize)
    elif fontName == '<system-bold>':
      aFont = UIFont.boldSystemFontOfSize_(pointSize)
    else:
      aFont = UIFont.fontWithName_size_(fontName, pointSize)
    self.ID.setFont_(aFont)    
  def getFont(self):
    aFont = self.ID.font()
    return (aFont.fontName(), aFont.pointSize())
  font = property(getFont, setFont)
  
  def setContainerFrame(self, aRect):
    try:
      if len(aRect) == 4: aRect = CGRect((aRect[0], aRect[1]), (aRect[2], aRect[3]))
      elif len(aRect) == 2: aRect = CGRect(aRect[0], aRect[1])
    except TypeError:
      pass
    self.ID.setContainerFrame_(aRect)
  def getContainerFrame(self):
    return self.ID.containerFrame()
  containerFrame = property(getContainerFrame, setContainerFrame)
  
  def setWrapped(self, aBool):
    self.ID.setWrapped_(aBool)    
  def isWrapped(self):
    return self.ID.wrapped()
  wrapped = property(isWrapped, setWrapped)
  
  def setAlignmentMode(self, aMode):
    self.ID.setAlignmentMode_(aMode)    
  def getAlignmentMode(self):
    return self.ID.alignmentMode()
  alignmentMode = property(getAlignmentMode, setAlignmentMode)
  
  def setTruncationMode(self, aMode):
    self.ID.setTruncationMode_(aMode)    
  def getTruncationMode(self):
    return self.ID.truncationMode()
  truncationMode = property(getTruncationMode, setTruncationMode)
  
  def getTextSize(self):
    return self.ID.textSize()
  textSize = property(getTextSize, None)
  
  def setFlatness(self, aFloat):
    self.ID.setFlatness_(aFloat)    
  def getFlatness(self):
    return self.ID.flatness()
  flatness = property(getFlatness, setFlatness)
  
  def setExtrusionDepth(self, aFloat):
    self.ID.setExtrusionDepth_(aFloat)    
  def getExtrusionDepth(self):
    return self.ID.extrusionDepth()
  extrusionDepth = property(getExtrusionDepth, setExtrusionDepth)

  def setChamferRadius(self, aFloat):
    self.ID.setChamferRadius_(aFloat)    
  def getChamferRadius(self):
    return self.ID.chamferRadius()
  chamferRadius = property(getChamferRadius, setChamferRadius)
  
  def setChamferProfile(self, aPath):
    self.ID.setChamferProfile_(ObjCInstance(aPath))
  def getChamferProfile(self):
    profile = self.ID.chamferProfile()
    uipath=ui.Path()
    ObjCInstance(uipath).appendBezierPath_(profile)
    return uipath
  chamferProfile = property(getChamferProfile, setChamferProfile)
  
class Shape(Geometry):
  def __init__(self, extrusionDepth=None, shapeWithPath=None, ID=None):
    if extrusionDepth is not None:
      self.ID = SCNShape.shapeWithPath_extrusionDepth_(ObjCInstance(shapeWithPath), extrusionDepth)
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = SCNShape.shape()
  
  @classmethod
  def shapeWithPath(cls, path=None, extrusionDepth=0.0):
    return cls(shapeWithPath=path, extrusionDepth=extrusionDepth)
    
  def setExtrusionDepth(self, aFloat):
    self.ID.setExtrusionDepth_(aFloat)    
  def getExtrusionDepth(self):
    return self.ID.extrusionDepth()
  extrusionDepth = property(getExtrusionDepth, setExtrusionDepth)
  
  def setPath(self, aPath):
    self.ID.setPath_(ObjCInstance(aPath))    
  def getPath(self):
    aPath = self.ID.path()
    uipath=ui.Path()
    ObjCInstance(uipath).appendBezierPath_(aPath)
    return uipath
  path = property(getPath, setPath)
  
  def setChamferMode(self, aMode):
    self.ID.setChamferMode_(aMode.value)    
  def getChamferMode(self):
    return ChamferMode(self.ID.chamferMode())
  chamferMode = property(getChamferMode, setChamferMode)
  
  def setChamferProfile(self, aPath):
    self.ID.setChamferProfile_(ObjCInstance(aPath))
  def getChamferProfile(self):
    profile = self.ID.chamferProfile()
    uipath=ui.Path()
    ObjCInstance(uipath).appendBezierPath_(profile)
    return uipath
  chamferProfile = property(getChamferProfile, setChamferProfile)
  
  def setChamferRadius(self, aFloat):
    self.ID.setChamferRadius_(aFloat)    
  def getChamferRadius(self):
    return self.ID.chamferRadius()
  chamferRadius = property(getChamferRadius, setChamferRadius)
  

class Morpher(CInst):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = SCNMorpher.morpher()
    
  def setTargets(self, targetList):
    try:
      iterator = iter(targetList)
    except TypeError:
      targetList = [targetList]
    self.ID.setTargets_([aTarget.ID for aTarget in targetList])
  def getTargets(self):
    return tuple([sceneKit.Geometry.outof(aTarget) for aTarget in self.ID.targets()])
  targets = property(getTargets, setTargets)
  
  def weightForTargetAtIndex(self, index=0):
    return self.ID.weightForTargetAtIndex_(index)
 
  def setWeightForTargetAtIndex(self, weight=0.0, index=0):
    self.ID.setWeight_forTargetAtIndex_(weight, index)
  
  def setCalculationMode(self, aMode):
    self.ID.setCalculationMode_(aMode.value)
  def getCalculationMode(self):
    return MorpherCalculationMode(self.ID.calculationMode())
  calculationMode = property(getCalculationMode, setCalculationMode)
  
  def setUnifiesNormals(self, aBool):
    self.ID.setUnifiesNormals_(aBool)    
  def getUnifiesNormals(self):
    return self.ID.unifiesNormals()
  unifiesNormals = property(getUnifiesNormals, setUnifiesNormals)
  
  def setWeights(self, weightList):
    try:
      iterator = iter(weightList)
    except TypeError:
      weightList = [weightList]
    self.ID.setWeights_(weightList)    
  def getWeights(self):
    return tuple(self.ID.weights())
  weights = property(getWeights, setWeights)
  
  def setWeightForTargetNamed(self, weight=0.0, name=None):
    self.ID.setWeight_forTargetNamed_(weight, name)
    
  def setWeightForTarget(self, weight = 0.0, name=None, index=None):
    if index is not None:
      self.setWeightForTargetAtIndex(weight, index)
    else:
      self.setWeightForTargetNamed(weight, name)
      
  def weightForTargetNamed(self, name=None):
    return self.ID.weightForTargetNamed_(name)
    
  def weightForTarget(self, index=None, name=None):
    if index is not None:
      return self.weightForTargetAtIndex(index)
    else:
      return self.weightForTargetNamed(name)
      
class Skinner(CInst):
  def __init__(self, baseGeometry=None, bones=None, boneInverseBindTransforms=None, boneWeights=None, boneIndices=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      if baseGeometry is not None:
        baseGeometry = baseGeometry.ID
      if bones is not None:
        bonesArray = NSMutableArray.array()
        for i in range(len(bones)):
          bonesArray.addObject_(bones[i].ID)
        bones = NSArray.arrayWithArray_(bonesArray)
      if boneInverseBindTransforms is not None:
        length = len(boneInverseBindTransforms)
        boneInverseBindTransforms = [SCNMatrix4(*m) for m in boneInverseBindTransforms]
        boneInverseBindTransforms = [NSValue.valueWithSCNMatrix4_(s, restype=c_void_p, argtypes=[SCNMatrix4]) for s in boneInverseBindTransforms]

        bArray = NSMutableArray.array()
        for i in range(length):
          bArray.addObject_(boneInverseBindTransforms[i])
        boneInverseBindTransforms = NSArray.arrayWithArray_(bArray)

      if boneWeights is not None:
        boneWeights = boneWeights.ID
      if boneIndices is not None:
        boneIndices = boneIndices.ID

      self.ID = SCNSkinner.skinnerWithBaseGeometry_bones_boneInverseBindTransforms_boneWeights_boneIndices_(baseGeometry, bones, boneInverseBindTransforms, boneWeights, boneIndices, restype=c_void_p, argtypes=[c_void_p, c_void_p, c_void_p, c_void_p, c_void_p])
    
  @classmethod
  def skinnerWithBaseGeometry(cls, baseGeometry=None, bones=None, boneInverseBindTransforms=None, boneWeights=None, boneIndices=None):
    return cls(baseGeometry=baseGeometry, bones=bones, boneInverseBindTransforms=boneInverseBindTransforms, boneWeights=boneWeights, boneIndices=boneIndices)
    
  def setBaseGeometry(self, aBaseGeometry):
    self.ID.setBaseGeometry_(aBaseGeometry.ID)    
  def getBaseGeometry(self):
    return sceneKit.Geometry.outof(self.ID.baseGeometry())
  baseGeometry = property(getBaseGeometry, setBaseGeometry)
  
  def setBaseGeometryBindTransform(self, aBaseGeometryBindTransform):
    self.ID.setBaseGeometryBindTransform_(SCNMatrix4(*aBaseGeometryBindTransform))
  def getBaseGeometryBindTransform(self):
#    print(self.ID.baseGeometryBindTransform(restype=SCNMatrix4, argtypes=[]))
    return matrix4Make(getCStructValuesAsList(self.ID.baseGeometryBindTransform())) #??? to be tested if a Skinner can finally be programmed...
  baseGeometryBindTransform = property(getBaseGeometryBindTransform, setBaseGeometryBindTransform)
  
  def setSkeleton(self, aSkeleton):
    self.ID.setSkeleton_(aSkeleton.ID)    
  def getSkeleton(self):
    return sceneKit.Node.outof(self.ID.skeleton())
  skeleton = property(getSkeleton, setSkeleton)
  
  def getBones(self):
    return tuple([sceneKit.Node.outof(aBone) for aBone in self.ID.bones()])
  bones = property(getBones, None)
  
  def getBoneInverseBindTransforms(self):
    ret = self.ID.boneInverseBindTransforms()
    retM = []
    for aValue in ret:
      scnM4 = aValue.SCNMatrix4Value()  #??? to be tested if a Skinner can finally be programmed...
      retM.append(matrix4Make(getCStructValuesAsList(scnM4)))
    return tuple(retM)
  boneInverseBindTransforms = property(getBoneInverseBindTransforms, None)
  
  def getBoneWeights(self):
    return sceneKit.GeometrySource.outof(self.ID.boneWeights())
  boneWeights = property(getBoneWeights, None)
  
  def getBoneIndices(self):
    return sceneKit.GeometrySource.outof(self.ID.boneIndices())
  boneIndices = property(getBoneIndices, None)
