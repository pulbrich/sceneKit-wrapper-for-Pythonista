'''
geometrySource module for sceneKit
includes class GeometrySource and class GeometryElement 
'''

from ctypes import *
from objc_util import *
import sys

import sceneKit
from .sceneKitEnv import *

class GeometryPrimitiveType(Enum):
  Triangles = 0
  TriangleStrip = 1
  Line = 2
  Point = 3
  Polygon = 4
  SCNGeometryPrimitiveTypeTriangles = 0
  SCNGeometryPrimitiveTypeTriangleStrip = 1
  SCNGeometryPrimitiveTypeLine = 2
  SCNGeometryPrimitiveTypePoint = 3
  SCNGeometryPrimitiveTypePolygon = 4
  
_geometrySourceSemantics = []
for aSemantics in ['SCNGeometrySourceSemanticVertex', 'SCNGeometrySourceSemanticNormal', 'SCNGeometrySourceSemanticTexcoord', 'SCNGeometrySourceSemanticColor', 'SCNGeometrySourceSemanticTangent', 'SCNGeometrySourceSemanticEdgeCrease', 'SCNGeometrySourceSemanticVertexCrease', 'SCNGeometrySourceSemanticBoneIndices', 'SCNGeometrySourceSemanticBoneWeights']:
  _geometrySourceSemantics.append(str(ObjCInstance(c_void_p.in_dll(c, aSemantics))))
_geometrySourceSemantics = tuple(_geometrySourceSemantics)
  
SCNGeometrySourceSemanticVertex, SCNGeometrySourceSemanticNormal, SCNGeometrySourceSemanticTexcoord, SCNGeometrySourceSemanticColor, SCNGeometrySourceSemanticTangent, SCNGeometrySourceSemanticEdgeCrease, SCNGeometrySourceSemanticVertexCrease, SCNGeometrySourceSemanticBoneIndices, SCNGeometrySourceSemanticBoneWeights = _geometrySourceSemantics  
GeometrySourceSemanticVertex, GeometrySourceSemanticNormal, GeometrySourceSemanticTexcoord, GeometrySourceSemanticColor, GeometrySourceSemanticTangent, GeometrySourceSemanticEdgeCrease, GeometrySourceSemanticVertexCrease, GeometrySourceSemanticBoneIndices, GeometrySourceSemanticBoneWeights = _geometrySourceSemantics

class GeometrySource(CInst):
  def __init__(self, count=None, data=None, semantic=None, vectorCount=None, floatComponents=None, componentsPerVector=None, bytesPerComponent=None, dataOffset=None, dataStride=None, geometrySourceWithVertices=None, geometrySourceWithNormals=None, geometrySourceWithTextureCoordinates=None, geometrySourceWithData=None, geometrySourceWithCData=None, ID=None):
    if geometrySourceWithVertices is not None:
      try:
        iterator = iter(geometrySourceWithVertices)
      except TypeError:
        geometrySourceWithVertices = [geometrySourceWithVertices]
      SCNVector3ArrayN = SCNVector3 * len(geometrySourceWithVertices)
      verts = [SCNVector3(*aVertice) for aVertice in geometrySourceWithVertices]
      verts_array = SCNVector3ArrayN(*verts)
      self.ID = SCNGeometrySource.geometrySourceWithVertices_count_(byref(verts_array), len(verts), restype=c_void_p, argtypes=[POINTER(SCNVector3ArrayN), c_long])
    elif geometrySourceWithNormals is not None:
      try:
        iterator = iter(geometrySourceWithNormals)
      except TypeError:
        geometrySourceWithNormals = [geometrySourceWithNormals]
      SCNVector3ArrayN = SCNVector3 * len(geometrySourceWithNormals)
      norms = [SCNVector3(*aNorm) for aNorm in geometrySourceWithNormals]
      norms_array = SCNVector3ArrayN(*norms)
      self.ID = SCNGeometrySource.geometrySourceWithNormals_count_(byref(norms_array), len(norms), restype=c_void_p, argtypes=[POINTER(SCNVector3ArrayN), c_long])
    elif geometrySourceWithTextureCoordinates is not None:
      try:
        iterator = iter(geometrySourceWithTextureCoordinates)
      except TypeError:
        geometrySourceWithTextureCoordinates = [geometrySourceWithTextureCoordinates]
      CGPointArrayN = CGPoint * len(geometrySourceWithTextureCoordinates)
      coords = [CGPoint(*aCoord) for aCoord in geometrySourceWithTextureCoordinates]
      coords_array = CGPointArrayN(*coords)
      self.ID = SCNGeometrySource.geometrySourceWithTextureCoordinates_count_(byref(coords_array), len(coords), restype=c_void_p, argtypes=[POINTER(CGPointArrayN), c_long])
    elif geometrySourceWithData is not None:     
      dataC = ns(bytes(geometrySourceWithData))
      self.ID = SCNGeometrySource.geometrySourceWithData_semantic_vectorCount_floatComponents_componentsPerVector_bytesPerComponent_dataOffset_dataStride_(dataC, semantic, vectorCount, floatComponents, componentsPerVector, bytesPerComponent, dataOffset, dataStride)
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = None
      
  @classmethod
  def geometrySourceWithData(cls, data=None, semantic=None, vectorCount=None, floatComponents=None, componentsPerVector=None, bytesPerComponent=None, dataOffset=None, dataStride=None):
    return cls(geometrySourceWithData=data, semantic=semantic, vectorCount=vectorCount, floatComponents=floatComponents, componentsPerVector=componentsPerVector, bytesPerComponent=bytesPerComponent, dataOffset=dataOffset, dataStride=dataStride)
  
  @classmethod
  def geometrySourceWithVertices(cls, vertices=None, count=None):
    return cls(geometrySourceWithVertices=vertices, count=count)
    
  @classmethod
  def geometrySourceWithNormals(cls, normals=None, count=None):
    return cls(geometrySourceWithNormals=normals, count=count)
    
  @classmethod
  def geometrySourceWithTextureCoordinates(cls, textureCoordinates=None, count=None):
    return cls(geometrySourceWithTextureCoordinates=textureCoordinates, count=count)
    
  @classmethod
  def interleavedGeometrySourceWithVectors(cls, sourceList, semanticList):
    returnSources, sourceParams, vertexStructFields = [], [], []
    vectorCount = len(sourceList[0])
    dataOffset = 0
    for i in range(len(sourceList)):
      vectors = sourceList[i]
      floatComponents = isinstance(vectors[0][0], float)
      componentsPerVector = len(vectors[0])
      bytesPerComponent = sizeof(c_float) if floatComponents else sizeof(c_int)
      sourceParams.append((floatComponents, componentsPerVector, bytesPerComponent, dataOffset))
      for j in range(componentsPerVector):
        field = 'f'+str(i)+str(j)
        if floatComponents:
          vertexStructFields.append((field, c_float))
          dataOffset += sizeof(c_float)
        else:
          vertexStructFields.append((field, c_int))
          dataOffset += sizeof(c_int)
    dataStride = dataOffset    
    class vertexStruct(Structure):
      _fields_ = vertexStructFields      
    vertexStructArrayType = vertexStruct * vectorCount
    vertexStructArray = vertexStructArrayType()       
    for i in range(vectorCount):
      element = []
      for j in range(len(sourceList)):
        element += sourceList[j][i]
      vertexStructArray[i] = vertexStruct(*element)
    data = NSData.dataWithBytes_length_(byref(vertexStructArray), sizeof(vertexStructArray))
    for i in range(len(sourceList)): 
      returnSources.append( cls.outof( SCNGeometrySource.geometrySourceWithData_semantic_vectorCount_floatComponents_componentsPerVector_bytesPerComponent_dataOffset_dataStride_(data, semanticList[i], vectorCount, sourceParams[i][0], sourceParams[i][1], sourceParams[i][2], sourceParams[i][3], dataStride)))

    return tuple(returnSources)
    
  @classmethod
  def geometrySourceWithVectors(cls, source, semantic):
    return cls.interleavedGeometrySourceWithVectors([source], [semantic])[0]
    
  def getVectors(self):
    data = nsdata_to_bytes(self.ID.data())
    dataRet = []
    for i in range(self.vectorCount):
      components = []
      for j in range(self.componentsPerVector):
        if self.floatComponents:
          dataC = create_string_buffer(data[(i*self.dataStride+self.dataOffset)+j*self.bytesPerComponent : (i*self.dataStride+self.dataOffset)+j*self.bytesPerComponent+self.bytesPerComponent], size=self.bytesPerComponent)
          components.append(c_float.from_buffer(dataC).value)
        else:
          components.append(int.from_bytes(data[(i*self.dataStride+self.dataOffset)+j*self.bytesPerComponent : (i*self.dataStride+self.dataOffset)+j*self.bytesPerComponent+self.bytesPerComponent], sys.byteorder))
      if self.componentsPerVector == 2:
        dataRet.append(vector2Make(components))
      elif self.componentsPerVector == 3:
        dataRet.append(vector3Make(components))
      elif self.componentsPerVector == 4:
        dataRet.append(vector4Make(components))
      else:
        dataRet.append(tuple(components))
    return tuple(dataRet)
  vectors = property(getVectors, None)
  
  def getData(self):
    return nsdata_to_bytes(self.ID.data())
  data = property(getData, None)
    
  def getSemantic(self):
    return self.ID.semantic()
  semantic = property(getSemantic, None)
  
  def getVectorCount(self):
    return self.ID.vectorCount()
  vectorCount = property(getVectorCount, None)
  
  def getFloatComponents(self):
    return self.ID.floatComponents()
  floatComponents = property(getFloatComponents, None)
  
  def getComponentsPerVector(self):
    return self.ID.componentsPerVector()
  componentsPerVector = property(getComponentsPerVector, None)
  
  def getBytesPerComponent(self):
    return self.ID.bytesPerComponent()
  bytesPerComponent = property(getBytesPerComponent, None)
  
  def getDataOffset(self):
    return self.ID.dataOffset()
  dataOffset = property(getDataOffset, None)
  
  def getDataStride(self):
    return self.ID.dataStride()
  dataStride = property(getDataStride, None)


class GeometryElement(CInst):
  def __init__(self, geometryElementWithData=None, primitiveType=None, mdlSubMesh=None, ID=None):
    if geometryElementWithData is not None:
      if primitiveType == GeometryPrimitiveType.Triangles:
        count = len(geometryElementWithData) // 3
      elif primitiveType == GeometryPrimitiveType.TriangleStrip:
        count = len(geometryElementWithData) - 2
      elif primitiveType == GeometryPrimitiveType.Line:
        count = len(geometryElementWithData) // 2
      elif primitiveType == GeometryPrimitiveType.Point:
        count = len(geometryElementWithData)
      elif primitiveType == GeometryPrimitiveType.Polygon:
        count, remainder = 0, len(geometryElementWithData)
        for i in range(len(geometryElementWithData)):
          if remainder > 0:
            count += 1
            remainder -= (geometryElementWithData[i]+1)
          else:
            break
      else: count = 0      
      bytesPerIndex = (max(geometryElementWithData).bit_length() // 8) + 1
      indexes_array = bytearray(len(geometryElementWithData) * bytesPerIndex)
      for i in range(len(geometryElementWithData)):
        indexes_array[i*bytesPerIndex : (i+1)*bytesPerIndex] = geometryElementWithData[i].to_bytes(bytesPerIndex, sys.byteorder)
      datIndexes = ns(bytes(indexes_array))          
      self.ID = SCNGeometryElement.geometryElementWithData_primitiveType_primitiveCount_bytesPerIndex_(datIndexes, primitiveType.value, count, bytesPerIndex)
    elif mdlSubMesh is not None:
      self.ID = SCNGeometryElement.geometryElementWithMDLSubmesh_(mdlSubMesh)
      if self.ID is None:
        raise RuntimeError('geometryElementWithMDLSubmesh failed. Wrong MDL asset?')
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = None
  
  @classmethod
  def geometryElementWithData(cls, data=None, primitiveType=None, primitiveCount=None, bytesPerIndex=None):
    return cls(geometryElementWithData=data, primitiveType=primitiveType)
    
  @classmethod
  def geometryElementWithMDLSubmesh(cls, mdlSubMesh=None):
    return cls(mdlSubMesh=mdlSubMesh)
    
  def getData(self):
    data = nsdata_to_bytes(self.ID.data())
    bytesPerIndex = self.bytesPerIndex
    dataRet = []
    for i in range(0, len(data)//bytesPerIndex):
      dataRet.append(int.from_bytes(data[i*bytesPerIndex : (i+1)*bytesPerIndex], sys.byteorder))
    return tuple(dataRet)
  data = property(getData, None)
  
  def getBytesPerIndex(self):
    return self.ID.bytesPerIndex()
  bytesPerIndex = property(getBytesPerIndex, None)
  
  def getPrimitiveType(self):
    return GeometryPrimitiveType(self.ID.primitiveType())
  primitiveType = property(getPrimitiveType, None)
  
  def getPrimitiveCount(self):
    return self.ID.primitiveCount()
  primitiveCount = property(getPrimitiveCount, None)
  
  def setPrimitiveRange(self, aRange):
    anNSRange = NSRange(aRange[0], aRange[1])
    self.ID.setPrimitiveRange_(anNSRange)    
  def getPrimitiveRange(self):
    aRange = self.ID.primitiveRange()
    location, length = aRange.location, aRange.length
    if location > self.primitiveCount:
      location, length = 0, self.primitiveCount
    return (location, length)
  primitiveRange = property(getPrimitiveRange, setPrimitiveRange)
  
  def setPointSize(self, aSize):
    self.ID.setPointSize_(aSize)    
  def getPointSize(self):
    return self.ID.pointSize()
  pointSize = property(getPointSize, setPointSize)
  
  def setMinimumPointScreenSpaceRadius(self, aRadius):
    self.ID.setMinimumPointScreenSpaceRadius_(aRadius)    
  def getMinimumPointScreenSpaceRadius(self):
    return self.ID.minimumPointScreenSpaceRadius()
  minimumPointScreenSpaceRadius = property(getMinimumPointScreenSpaceRadius, setMinimumPointScreenSpaceRadius)
  
  def setMaximumPointScreenSpaceRadius(self, aRadius):
    self.ID.setMaximumPointScreenSpaceRadius_(aRadius)    
  def getMaximumPointScreenSpaceRadius(self):
    return self.ID.maximumPointScreenSpaceRadius()
  maximumPointScreenSpaceRadius = property(getMaximumPointScreenSpaceRadius, setMaximumPointScreenSpaceRadius)
