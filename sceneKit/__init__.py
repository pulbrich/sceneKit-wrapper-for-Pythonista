'''
sceneKit top module for the sceneKit wrapper under Pythonista

(c) Peter Ulbrich, 2019, peter.ulbrich@gmail.com

Use of this source code is governed by the MIT license:
  
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

from objc_util import *
import ctypes
import ui
from collections import namedtuple, OrderedDict
import os

from .sceneKitEnv import *
from .sceneKitNode import *
from .sceneKitMaterial import *
from .sceneKitCamera import *
from .sceneKitGeometry import *
from .sceneKitLight import *
from .sceneKitConstraints import *
from .sceneKitAnimation import *
from .sceneKitSceneRenderer import *
from .sceneKitGeometrySource import *
from .sceneKitPhysics import *
from .sceneKitParticleSystem import *
from .sceneKitAudio import *
# from .sceneKitSceneSource import *  #not implemented due to limited use under runtime environment


class ViewAutoresizing(Flag):
  AutoresizingNone = 0
  FlexibleLeftMargin = (1 << 0)
  FlexibleWidth = (1 << 1)
  FlexibleRightMargin = (1 << 2)
  FlexibleTopMargin = (1 << 3)
  FlexibleHeight = (1 << 4)
  FlexibleBottomMargin = (1 << 5)
  
  UIViewAutoresizingNone = 0
  UIViewAutoresizingFlexibleLeftMargin = (1 << 0)
  UIViewAutoresizingFlexibleWidth = (1 << 1)
  UIViewAutoresizingFlexibleRightMargin = (1 << 2)
  UIViewAutoresizingFlexibleTopMargin = (1 << 3)
  UIViewAutoresizingFlexibleHeight = (1 << 4)
  UIViewAutoresizingFlexibleBottomMargin = (1 << 5)

_sceneAttributes = []
for anAttribute in ['SCNSceneEndTimeAttributeKey', 'SCNSceneFrameRateAttributeKey', 'SCNSceneStartTimeAttributeKey', 'SCNSceneUpAxisAttributeKey']:
  _sceneAttributes.append(str(ObjCInstance(c_void_p.in_dll(c, anAttribute))))
_sceneAttributes = tuple(_sceneAttributes)

SCNSceneEndTimeAttributeKey, SCNSceneFrameRateAttributeKey, SCNSceneStartTimeAttributeKey, \
SCNSceneUpAxisAttributeKey = _sceneAttributes
SceneEndTimeAttributeKey, SceneFrameRateAttributeKey, SceneStartTimeAttributeKey, \
SceneUpAxisAttributeKey = _sceneAttributes

class AntialiasingMode(Enum):
  ModeNone = 0
  Multisampling2X = 1
  Multisampling4X = 2
  Multisampling8X = 3
  Multisampling16X = 4
  SCNAntialiasingModeNone = 0
  SCNAntialiasingModeMultisampling2X = 1
  SCNAntialiasingModeMultisampling4X = 2
  SCNAntialiasingModeMultisampling8X = 3
  SCNAntialiasingModeMultisampling16X = 4
  
                       
class View(SceneRenderer, CInst):
  def __init__(self, frame=None, superView=None, ID=None):
    if frame is not None:
      try:
        if len(frame) == 4:
          x, y, w, h = frame
        elif len(frame) == 2:
          (x, y), (w, h) = frame
        frame = CGRect((x, y),(w, h))
      except TypeError:
        pass       
      self.ID = SCNView.alloc().initWithFrame_options_(frame, None).autorelease()
      if superView is not None:
        self.addToSuperview(superView)
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = SCNView.alloc().init()
      if superView is not None:
        self.addToSuperview(superView)
    
  def addToSuperview(self, aUIView):
    aUIView.objc_instance.addSubview_(self.ID)
    
  def removeFromSuperview(self):
    self.ID.removeFromSuperview()
    
  def initWithFrame(self, frame=None):
    if frame is not None:
      try:
        if len(frame) == 4:
          x, y, w, h = frame
        elif len(frame) == 2:
          (x, y), (w, h) = frame
        frame = CGRect((x, y),(w, h))
      except TypeError:
        pass       
    self.ID.initWithFrame_options_(frame, None)

  def setBackgroundColor(self, color):
    r, g, b, a = parse_color(color)
    self.ID.setBackgroundColor_(UIColor.color(red=r, green=g, blue=b, alpha=a))
  def getBackgroundColor(self):
    backgroundColor = self.ID.backgroundColor()
    return RGBA(backgroundColor.red(), backgroundColor.green(), backgroundColor.blue(), backgroundColor.alpha())    
  backgroundColor = property(getBackgroundColor, setBackgroundColor)
  background_color = property(getBackgroundColor, setBackgroundColor)
  
  def setPreferredFramesPerSecond(self, aRate):
    self.ID.setPreferredFramesPerSecond(aRate)    
  def getPreferredFramesPerSecond(self):
    return self.ID.preferredFramesPerSecond()
  preferredFramesPerSecond = property(getPreferredFramesPerSecond, setPreferredFramesPerSecond)
  
  def setRendersContinuously(self, aBool):
    self.ID.setRendersContinuously(aBool)    
  def getRendersContinuously(self):
    return self.ID.rendersContinuously()
  rendersContinuously = property(getRendersContinuously, setRendersContinuously)
  
  def setAntialiasingMode(self, anAntialiasingMode):
    self.ID.setAntialiasingMode(anAntialiasingMode.value)
  def getAntialiasingMode(self):
    return AntialiasingMode(self.ID.antialiasingMode())
  antialiasingMode = property(getAntialiasingMode, setAntialiasingMode)
  
  def setAllowsCameraControl(self, control=True):
    self.ID.setAllowsCameraControl_(control)    
  def getAllowsCameraControl(self):
    return self.ID.allowsCameraControl()    
  allowsCameraControl = property(getAllowsCameraControl, setAllowsCameraControl)
    
  def getCameraControlConfiguration(self):
    return sceneKit.CameraControlConfiguration.outof(self.ID.cameraControlConfiguration())
  cameraControlConfiguration = property(getCameraControlConfiguration, None)
  
  def getDefaultCameraController(self):
    return sceneKit.CameraController.outof(self.ID.defaultCameraController())
  defaultCameraController = property(getDefaultCameraController, None)

  def pause(self, sender=None):
    self.ID.pause_(sender)
    
  def play(self, sender=None):
    self.ID.play_(sender)
    
  def stop(self, sender=None):
    self.ID.stop_(sender)
    
  def snapshot(self):
    uiImage = self.ID.snapshot()
    c.UIImagePNGRepresentation.argtypes = [c_void_p]
    c.UIImagePNGRepresentation.restype = c_void_p
    data = ObjCInstance(c.UIImagePNGRepresentation(uiImage.ptr))
    return Image.from_data(nsdata_to_bytes(data),2.0)

  def setAutoresizingMask(self, flags):
    try:
      iterator = iter(flags)
    except TypeError:
      flags = [flags]
    mask = 0
    for aFlag in flags:
      mask = mask | aFlag.value
    self.ID.setAutoresizingMask_(mask)
  def getAutoresizingMask(self):
    mask = self.ID.autoresizingMask()
    flags = []
    for aFlag in ViewAutoresizing:
      if (mask & aFlag.value) != 0: flags.append(aFlag)
    return tuple(flags)
  autoresizingMask = property(getAutoresizingMask, setAutoresizingMask)
  
  def setDrawableResizesAsynchronously(self, aBool):
    self.ID.setDrawableResizesAsynchronously_(aBool)    
  def getDrawableResizesAsynchronously(self):
    return self.ID.drawableResizesAsynchronously()
  drawableResizesAsynchronously = property(getDrawableResizesAsynchronously, setDrawableResizesAsynchronously)
  
    
class Scene(Animatable, CInst):
  def __init__(self, name=None, inDirectory= None, options=None, url=None, mdlAsset=None, ID=None):
    if name is not None and inDirectory is None:
      self.ID = SCNScene.sceneNamed_(name)
    elif name is not None and inDirectory is not None:
      self.ID = SCNScene.sceneNamed_inDirectory_options_(name, inDirectory, options)
    elif url is not None:
      error = c_void_p(0)
      ret = SCNScene.sceneWithURL_options_error_(nsurl(url), self.convertOptions(options), byref(error), restype=c_void_p, argtypes=[c_void_p, c_void_p, c_void_p])
      if ret is None:
        self.ID = None
        try:
          error = ObjCInstance(error)
          message = "sceneWithURL failed. Error: " + str(int(error.code())) + ' ' + str(error.localizedDescription())
        except AttributeError:
          message = "sceneWithURL failed. Wrong URL?"
        raise RuntimeError(message)
      else:
        self.ID = ret
    elif mdlAsset is not None:
      self.ID = SCNScene.sceneWithMDLAsset_(mdlAsset)
      if self.ID is None:
        raise RuntimeError('sceneWithMDLAsset failed. Wrong asset?')
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = SCNScene.scene()
      
  @classmethod
  def scene(cls):
    return cls()
    
  @classmethod
  def sceneNamed(cls, name=None, inDiectory=None, options=None):
    return cls(name=name, inDiectory=inDiectory, options=options)
    
  @classmethod
  def sceneWithURL(cls, url=None, options=None):
    return cls(url=url, options=options)
    
  @classmethod
  def sceneWithMDLAsset(cls, mdlAsset=None):
    return cls(mdlAsset=mdlAsset)
    
  def convertOptions(self, options):
    if options is None: return None
    retOptions = {}
    for key, value in options.items():
      i = _sceneSourceLoadingOptions.index(key)
      if key == SceneSourceAnimationImportPolicyKey:
        i = _sceneSourceAnimationImportPolicies.index(value)
      elif key == SCNSceneSourceAssetDirectoryURLsKey:
        value = [nsurl(aValue) for aValue in value]
      retOptions[key] = value
    return retOptions
    
  def setPaused(self, aBool):
    self.ID.setPaused(aBool)    
  def getPaused(self):
    return self.ID.paused()
  paused = property(getPaused, setPaused)
  
  def getRootNode(self):
    return Node.outof(self.ID.rootNode())    
  rootNode = property(getRootNode, None)
  
  def getBackground(self):
    return MaterialProperty.outof(self.ID.background())
  background = property(getBackground, None)
   
  def getLightingEnvironment(self):
    return MaterialProperty.outof(self.ID.lightingEnvironment())
  lightingEnvironment = property(getLightingEnvironment, None)
  
  def attributeForKey(self, key):
    attribute = self.ID.attributeForKey_(key)
    if key == SCNSceneUpAxisAttributeKey and attribute is not None:
      attribute = attribute.SCNVector3Value()
      return Vector3(attribute.a, attribute.b, attribute.c)
    else:
      return attribute
      
  def setAttribute(self, attribute, key):
    if key == SCNSceneUpAxisAttributeKey:
      attribute = vector3Make(attribute)
      attribute = NSValue.valueWithSCNVector3_(attribute)
    self.ID.setAttribute_forKey_(attribute, key)
  def setAttributeForKey(self, attribute, key):
    self.setAttribute(attribute, key)
      
  def writeToURL(self, url=None, options=None, delegate=None, progressHandler=None):
    if delegate is not None:
      sceneWriteToUrlDelegate = SceneWriteToUrlDelegate(delegate)
      delegate = sceneWriteToUrlDelegate.ID
    if progressHandler is not None:
      self.sceneWriteToUrlProgressHandler = sceneWriteToUrlProgressHandlerBlock(progressHandler)
      progressHandler = self.sceneWriteToUrlProgressHandler.blockCode
    return self.ID.writeToURL_options_delegate_progressHandler_(nsurl(url), self.convertOptions(options), delegate, progressHandler)
    
  def setFogStartDistance(self, aFogStartDistance):
    self.ID.setFogStartDistance(aFogStartDistance)    
  def getFogStartDistance(self):
    return self.ID.fogStartDistance()
  fogStartDistance = property(getFogStartDistance, setFogStartDistance)
  
  def setFogEndDistance(self, aFogEndDistance):
    self.ID.setFogEndDistance(aFogEndDistance)    
  def getFogEndDistance(self):
    return self.ID.fogEndDistance()
  fogEndDistance = property(getFogEndDistance, setFogEndDistance)
  
  def setFogDensityExponent(self, aFogDensityExponent):
    self.ID.setFogDensityExponent(aFogDensityExponent)    
  def getFogDensityExponent(self):
    return self.ID.fogDensityExponent()
  fogDensityExponent = property(getFogDensityExponent, setFogDensityExponent)
  
  def setFogColor(self, aFogColor):
    r, g, b, a = parse_color(aFogColor)
    self.ID.setFogColor_(ObjCClass('UIColor').color(red=r, green=g, blue=b, alpha=a))    
  def getFogColor(self):
    aFogColor = self.ID.fogColor()
    return RGBA(aFogColor.red(), aFogColor.green(), aFogColor.blue(), aFogColor.alpha())
  fogColor = property(getFogColor, setFogColor)
  
  def getPhysicsWorld(self):
    return PhysicsWorld.outof(self.ID.physicsWorld())
  physicsWorld = property(getPhysicsWorld, None)
  
  def addParticleSystem(self, system=None, transform=Matrix4Identity, withTransform=None):
    if withTransform is not None: transform = withTransform
    self.ID.addParticleSystem_withTransform_(system.ID, matrix4Make(transform))
    
  def getParticleSystems(self):
    return tuple([sceneKit.ParticleSystem.outof(aSystem) for aSystem in self.ID.particleSystems()])
  particleSystems = property(getParticleSystems, None)
  
  def removeParticleSystem(self, system=None):
    self.ID.removeParticleSystem_(system.ID)
    
  def removeAllParticleSystems(self):
    self.ID.removeAllParticleSystems()
    
def writeImage_withSceneDocumentURL_originalImageURL_(_self, _cmd, ximage, xdocumentURL, xoriginalImageURL):
  aWriteToUrlDelegate = sceneKit.SceneWriteToUrlDelegate.outof(ObjCInstance(_self))
  if aWriteToUrlDelegate.methods[0]:
    if ximage is not None:
      ximage = ObjCInstance(ximage)
      ximage = contentFromC(ximage)
    if xdocumentURL is not None:
      xdocumentURL = ObjCInstance(xdocumentURL)
      xdocumentURL = contentFromC(xdocumentURL)
    if xoriginalImageURL is not None:
      xoriginalImageURL = ObjCInstance(xoriginalImageURL)
      xoriginalImageURL = contentFromC(xoriginalImageURL)      
    ret =aWriteToUrlDelegate.delegate.writeImage(ximage, xdocumentURL, xoriginalImageURL)
    return nsurl(ret) if ret is not None else None
    
class SceneWriteToUrlDelegate(CInst):
  _actions = ('writeImage',)
  _newCClassName = 'SCNPYWriteToUrlDelegateClass'
  _cMethodList = [writeImage_withSceneDocumentURL_originalImageURL_]
  writeImage_withSceneDocumentURL_originalImageURL_.restype = c_void_p
  writeImage_withSceneDocumentURL_originalImageURL_.argtypes = [c_void_p, c_void_p, c_void_p]
  _protocols = ['SCNSceneExportDelegate']
  DelegateCClass = create_objc_class(_newCClassName, NSObject, methods=_cMethodList, protocols=_protocols)
  
  def __init__(self, aDelegate=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.delegate = aDelegate
      self.methods = [callable(_a) for _a in [getattr(aDelegate, anAction, False) for anAction in WriteToUrlDelegate._actions]]
      self.ID = WriteToUrlDelegate.DelegateCClass.alloc().init()
    
class sceneWriteToUrlProgressHandlerBlock:
  def __init__(self, block):    
    self.blockCode = ObjCBlock(self.blockInterface, restype=None, argtypes=[c_void_p, c_float, c_void_p, POINTER(c_bool)])
    self.pCode = block
      
  def blockInterface(self, _cmd, totalProgress, xError, xStop):
    totalProgress = float(totalProgress)
    try:
      xError = ObjCInstance(xError)
      code = xError.code()
    except AttributeError:
      xError = None
    stop = self.pCode(totalProgress, xError)
    if stop is None: stop = False
    xStop[0] = stop
