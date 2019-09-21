'''camera modul, to be included in sceneKit'''

import sceneKit
from .sceneKitEnv import *
from .sceneKitNode import *
from .sceneKitAnimation import *

class CameraProjectionDirection(Enum):
  Vertical = 0
  Horizontal = 1
  CameraProjectionDirectionVertical = 0
  CameraProjectionDirectionHorizontal = 1

class InteractionMode(Enum):
  Fly = 0
  OrbitAngleMapping = 1
  OrbitArcball = 2
  OrbitCenteredArcball = 3
  OrbitTurntable = 4
  Pan = 5
  Truck = 6
  SCNInteractionModeFly = 0
  SCNInteractionModeOrbitAngleMapping = 1
  SCNInteractionModeOrbitArcball = 2
  SCNInteractionModeOrbitCenteredArcball = 3
  SCNInteractionModeOrbitTurntable = 4
  SCNInteractionModePan = 5
  SCNInteractionModeTruck = 6

  
class Camera(Animatable, CInst):
  def __init__(self, mdlCamera=None, ID=None):
    if ID is not None:
      self.ID = ID
    elif mdlCamera is not None:
      self.ID = SCNCamera.cameraWithMDLCamera_(mdlCamera)
      if self.ID is None:
        raise RuntimeError('cameraWithMDLCamera failed. Wrong MDL asset?')
    else:
      self.ID = SCNCamera.camera()
    
  @classmethod
  def camera(cls):
    return cls()
    
  @classmethod
  def cameraWithMDLCamera(cls, mdlCamera=None):
    return cls(mdlCamera=mdlCamera)

  def setName(self, aString):
    self.ID.setName(aString)    
  def getName(self):
    return str(self.ID.name())
  name = property(getName, setName)
  
  def setZNear(self, aDist):
    self.ID.setZNear(aDist)    
  def getZNear(self):
    return self.ID.zNear()
  zNear = property(getZNear, setZNear)
  
  def setZFar(self, aDist):
    self.ID.setZFar(aDist)    
  def getZFar(self):
    return self.ID.zFar()
  zFar = property(getZFar, setZFar)
  
  def setAutomaticallyAdjustsZRange(self, aBool):
    self.ID.setAutomaticallyAdjustsZRange(aBool)    
  def getAutomaticallyAdjustsZRange(self):
    return self.ID.automaticallyAdjustsZRange()
  automaticallyAdjustsZRange = property(getAutomaticallyAdjustsZRange, setAutomaticallyAdjustsZRange)
  
  def setFieldOfView(self, anAngle):
    self.ID.setFieldOfView(anAngle)    
  def getFieldOfView(self):
    return self.ID.fieldOfView()
  fieldOfView = property(getFieldOfView, setFieldOfView) 
  
  def setFocalLength(self, aDist):
    self.ID.setFocalLength(aDist)    
  def getFocalLength(self):
    return self.ID.focalLength()
  focalLength = property(getFocalLength, setFocalLength)
  
  def setSensorHeight(self, aDist):
    self.ID.setSensorHeight(aDist)    
  def getSensorHeight(self):
    return self.ID.sensorHeight()
  sensorHeight = property(getSensorHeight, setSensorHeight)
  
  def setProjectionDirection(self, aDirection):
    self.ID.setProjectionDirection(aDirection.value)    
  def getProjectionDirection(self):
    return CameraProjectionDirection(self.ID.projectionDirection())
  projectionDirection = property(getProjectionDirection, setProjectionDirection)
  
  def setProjectionTransform(self, aMatrix4):
    self.ID.setProjectionTransform(matrix4Make(aMatrix4))
  def getProjectionTransform(self):
    trans = self.ID.projectionTransform()
    return matrix4Make(getCStructValuesAsList(trans))
  projectionTransform = property(getProjectionTransform, setProjectionTransform)
  
  def setUsesOrthographicProjection(self, aBool):
    self.ID.setUsesOrthographicProjection(aBool)    
  def getUsesOrthographicProjection(self):
    return self.ID.usesOrthographicProjection()
  usesOrthographicProjection = property(getUsesOrthographicProjection, getUsesOrthographicProjection)
  
  def setOrthographicScale(self, aScale):
    self.ID.setOrthographicScale(aScale)    
  def getOrthographicScale(self):
    return self.ID.orthographicScale()
  orthographicScale = property(getOrthographicScale, setOrthographicScale)

  def setCategoryBitMask(self, aBitMask):
    self.ID.setCategoryBitMask(aBitMask)    
  def getCategoryBitMask(self):
    return self.ID.categoryBitMask()
  categoryBitMask = property(getCategoryBitMask, setCategoryBitMask)
  
  def setWantsDepthOfField(self, aBool):
    self.ID.setWantsDepthOfField(aBool)    
  def getWantsDepthOfField(self):
    return self.ID.wantsDepthOfField()
  wantsDepthOfField = property(getWantsDepthOfField, setWantsDepthOfField)

  def setFocusDistance(self, aDist):
    self.ID.setFocusDistance(aDist)    
  def getFocusDistance(self):
    return self.ID.focusDistance()
  focusDistance = property(getFocusDistance, setFocusDistance)
  
  def setFStop(self, aStop):
    self.ID.setFStop(aStop)    
  def getFStop(self):
    return self.ID.fStop()
  fStop = property(getFStop, setFStop)
  
  def setApertureBladeCount(self, aCount):
    self.ID.setApertureBladeCount(aCount)    
  def getApertureBladeCount(self):
    return self.ID.apertureBladeCount()
  apertureBladeCount = property(getApertureBladeCount, setApertureBladeCount)
  
  def setFocalBlurSampleCount(self, aCount):
    self.ID.setFocalBlurSampleCount(aCount)    
  def getFocalBlurSampleCount(self):
    return self.ID.focalBlurSampleCount()
  focalBlurSampleCount = property(getFocalBlurSampleCount, setFocalBlurSampleCount)
  
  def setMotionBlurIntensity(self, aBlur):
    self.ID.setMotionBlurIntensity(aBlur)    
  def getMotionBlurIntensity(self):
    return self.ID.motionBlurIntensity()
  motionBlurIntensity = property(getMotionBlurIntensity, setMotionBlurIntensity)
  
  def setWantsHDR(self, aBool):
    self.ID.setWantsHDR(aBool)    
  def getWantsHDR(self):
    return self.ID.wantsHDR()
  wantsHDR = property(getWantsHDR, setWantsHDR)
  
  def setExposureOffset(self, anOffset):
    self.ID.setExposureOffset(anOffset)    
  def getExposureOffset(self):
    return self.ID.exposureOffset()
  exposureOffset = property(getExposureOffset, setExposureOffset)
  
  def setAverageGray(self, aGray):
    self.ID.setAverageGray(aGray)    
  def getAverageGray(self):
    return self.ID.averageGray()
  averageGray = property(getAverageGray, setAverageGray)
  
  def setWhitePoint(self, aWhite):
    self.ID.setWhitePoint(aWhite)    
  def getWhitePoint(self):
    return self.ID.whitePoint()
  whitePoint = property(getWhitePoint, setWhitePoint)
  
  def setMinimumExposure(self, anExposure):
    self.ID.setMinimumExposure(anExposure)    
  def getMinimumExposure(self):
    return self.ID.minimumExposure()
  minimumExposure = property(getMinimumExposure, setMinimumExposure)
  
  def setMaximumExposure(self, anExposure):
    self.ID.setMaximumExposure(anExposure)    
  def getMaximumExposure(self):
    return self.ID.maximumExposure()
  maximumExposure = property(getMaximumExposure, setMaximumExposure)
  
  def setWantsExposureAdaptation(self, aBool):
    self.ID.setWantsExposureAdaptation(aBool)    
  def getWantsExposureAdaptation(self):
    return self.ID.wantsExposureAdaptation()
  wantsExposureAdaptation = property(getWantsExposureAdaptation, setWantsExposureAdaptation)
  
  def setExposureAdaptationBrighteningSpeedFactor(self, aFactor):
    self.ID.setExposureAdaptationBrighteningSpeedFactor(aFactor)    
  def getExposureAdaptationBrighteningSpeedFactor(self):
    return self.ID.exposureAdaptationBrighteningSpeedFactor()
  exposureAdaptationBrighteningSpeedFactor = property(getExposureAdaptationBrighteningSpeedFactor, setExposureAdaptationBrighteningSpeedFactor)
  
  def setExposureAdaptationDarkeningSpeedFactor(self, aFactor):
    self.ID.setExposureAdaptationDarkeningSpeedFactor(aFactor)    
  def getExposureAdaptationDarkeningSpeedFactor(self):
    return self.ID.exposureAdaptationDarkeningSpeedFactor()
  exposureAdaptationDarkeningSpeedFactor = property(getExposureAdaptationDarkeningSpeedFactor, setExposureAdaptationDarkeningSpeedFactor)
  
  def setContrast(self, aContrast):
    self.ID.setContrast(aContrast)    
  def getContrast(self):
    return self.ID.contrast()
  contrast = property(getContrast, setContrast)
  
  def setSaturation(self, aSaturation):
    self.ID.setSaturation(aSaturation)    
  def getSaturation(self):
    return self.ID.saturation()
  saturation = property(getSaturation, setSaturation)
  
  def setBloomIntensity(self, anIntensity):
    self.ID.setBloomIntensity(anIntensity)    
  def getBloomIntensity(self):
    return self.ID.bloomIntensity()
  bloomIntensity = property(getBloomIntensity, setBloomIntensity)
  
  def setBloomThreshold(self, aThreshold):
    self.ID.setBloomThreshold(aThreshold)    
  def getBloomThreshold(self):
    return self.ID.bloomThreshold()
  bloomThreshold = property(getBloomThreshold, setBloomThreshold)
  
  def setBloomBlurRadius(self, aRadius):
    self.ID.setBloomBlurRadius(aRadius)    
  def getBloomBlurRadius(self):
    return self.ID.bloomBlurRadius()
  bloomBlurRadius = property(getBloomBlurRadius, setBloomBlurRadius)
  
  def setColorFringeIntensity(self, anIntensity):
    self.ID.setColorFringeIntensity(anIntensity)    
  def getColorFringeIntensity(self):
    return self.ID.colorFringeIntensity()
  colorFringeIntensity = property(getColorFringeIntensity, setColorFringeIntensity)
  
  def setColorFringeStrength(self, aStrength):
    self.ID.setColorFringeStrength(aStrength)    
  def getColorFringeStrength(self):
    return self.ID.colorFringeStrength()
  colorFringeStrength = property(getColorFringeStrength, setColorFringeStrength)
  
  def setVignettingIntensity(self, anIntensity):
    self.ID.setVignettingIntensity(anIntensity)    
  def getVignettingIntensity(self):
    return self.ID.vignettingIntensity()
  vignettingIntensity = property(getVignettingIntensity, setVignettingIntensity)
  
  def setVignettingPower(self, aPower):
    self.ID.setVignettingPower(aPower)    
  def getVignettingPower(self):
    return self.ID.vignettingPower()
  vignettingPower = property(getVignettingPower, setVignettingPower)
  
  def setScreenSpaceAmbientOcclusionIntensity(self, anIntensity):
    self.ID.setScreenSpaceAmbientOcclusionIntensity(anIntensity)    
  def getScreenSpaceAmbientOcclusionIntensity(self):
    return self.ID.screenSpaceAmbientOcclusionIntensity()
  screenSpaceAmbientOcclusionIntensity = property(getScreenSpaceAmbientOcclusionIntensity, setScreenSpaceAmbientOcclusionIntensity)
  
  def setScreenSpaceAmbientOcclusionRadius(self, aRadius):
    self.ID.setScreenSpaceAmbientOcclusionRadius(aRadius)    
  def getScreenSpaceAmbientOcclusionRadius(self):
    return self.ID.screenSpaceAmbientOcclusionRadius()
  screenSpaceAmbientOcclusionRadius = property(getScreenSpaceAmbientOcclusionRadius, setScreenSpaceAmbientOcclusionRadius)
  
  def setScreenSpaceAmbientOcclusionBias(self, aBias):
    self.ID.setScreenSpaceAmbientOcclusionBias(aBias)    
  def getScreenSpaceAmbientOcclusionBias(self):
    return self.ID.screenSpaceAmbientOcclusionBias()
  screenSpaceAmbientOcclusionBias = property(getScreenSpaceAmbientOcclusionBias, setScreenSpaceAmbientOcclusionBias)
  
  def setScreenSpaceAmbientOcclusionDepthThreshold(self, aThreshold):
    self.ID.setScreenSpaceAmbientOcclusionDepthThreshold(aThreshold)    
  def getScreenSpaceAmbientOcclusionDepthThreshold(self):
    return self.ID.screenSpaceAmbientOcclusionDepthThreshold()
  screenSpaceAmbientOcclusionDepthThreshold = property(getScreenSpaceAmbientOcclusionDepthThreshold, setScreenSpaceAmbientOcclusionDepthThreshold)
  
  def setScreenSpaceAmbientOcclusionNormalThreshold(self, aThreshold):
    self.ID.setScreenSpaceAmbientOcclusionNormalThreshold(aThreshold)    
  def getScreenSpaceAmbientOcclusionNormalThreshold(self):
    return self.ID.screenSpaceAmbientOcclusionNormalThreshold()
  screenSpaceAmbientOcclusionNormalThreshold = property(getScreenSpaceAmbientOcclusionNormalThreshold, setScreenSpaceAmbientOcclusionNormalThreshold)
  
  def setColorGrading(self, aMaterialProperty):
    self.ID.setColorGrading(aMaterialProperty.ID)    
  def getColorGrading(self):
    return MaterialProperty.outof(self.ID.colorGrading())
  colorGrading = property(getColorGrading, setColorGrading)
  
class CameraControlConfiguration(CInst):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = None
    
  def setAllowsTranslation(self, aBool):
    self.ID.setAllowsTranslation(aBool)    
  def getAllowsTranslation(self):
    return self.ID.allowsTranslation()
  allowsTranslation = property(getAllowsTranslation, setAllowsTranslation)
  
  def setAutoSwitchToFreeCamera(self, aBool):
    self.ID.setAutoSwitchToFreeCamera(aBool)    
  def getAutoSwitchToFreeCamera(self):
    return self.ID.autoSwitchToFreeCamera()
  autoSwitchToFreeCamera = property(getAutoSwitchToFreeCamera, setAutoSwitchToFreeCamera)
  
  def setFlyModeVelocity(self, aFlyModeVelocity):
    self.ID.setFlyModeVelocity(aFlyModeVelocity)    
  def getFlyModeVelocity(self):
    return self.ID.flyModeVelocity()
  flyModeVelocity = property(getFlyModeVelocity, setFlyModeVelocity)
  
  def setPanSensitivity(self, aPanSensitivity):
    self.ID.setPanSensitivity(aPanSensitivity)    
  def getPanSensitivity(self):
    return self.ID.panSensitivity()
  panSensitivity = property(getPanSensitivity, setPanSensitivity)
  
  def setRotationSensitivity(self, aRotationSensitivity):
    self.ID.setRotationSensitivity(aRotationSensitivity)    
  def getRotationSensitivity(self):
    return self.ID.rotationSensitivity()
  rotationSensitivity = property(getRotationSensitivity, setRotationSensitivity)
  
  def setTruckSensitivity(self, aTruckSensitivity):
    self.ID.setTruckSensitivity(aTruckSensitivity)    
  def getTruckSensitivity(self):
    return self.ID.truckSensitivity()
  truckSensitivity = property(getTruckSensitivity, setTruckSensitivity)
  
class CameraController(CInst):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = None
    
  def setDelegate(self, aDelegate):
    aCameraControllerDelegate = CameraControllerDelegate(aDelegate)
    self.ID.setDelegate(aCameraControllerDelegate.ID)    
  def getDelegate(self):
    aCameraControllerDelegate = sceneKit.CameraControllerDelegate.outof(self.ID.delegate())
    return aCameraControllerDelegate.delegate
  delegate = property(getDelegate, setDelegate)
  
  def setAutomaticTarget(self, aBool):
    self.ID.setAutomaticTarget(aBool)    
  def getAutomaticTarget(self):
    return self.ID.automaticTarget()
  automaticTarget = property(getAutomaticTarget, setAutomaticTarget)
  
  def setInertiaEnabled(self, aBool):
    self.ID.setInertiaEnabled(aBool)    
  def getInertiaEnabled(self):
    return self.ID.inertiaEnabled()
  inertiaEnabled = property(getInertiaEnabled, setInertiaEnabled)
  
  def setInertiaFriction(self, anInertiaFriction):
    self.ID.setInertiaFriction(anInertiaFriction)    
  def getInertiaFriction(self):
    return self.ID.inertiaFriction()
  inertiaFriction = property(getInertiaFriction, setInertiaFriction)
  
  def setInteractionMode(self, anInteractionMode):
    self.ID.setInteractionMode(anInteractionMode.value)
  def getInteractionMode(self):
    return InteractionMode(self.ID.interactionMode())
  interactionMode = property(getInteractionMode, setInteractionMode)
    
  def isInertiaRunning(self):
    return self.ID.isInertiaRunning()
  inertiaRunning = property(isInertiaRunning, None)
  
  def setMaximumHorizontalAngle(self, anAngle):
    self.ID.setMaximumHorizontalAngle(anAngle)    
  def getMaximumHorizontalAngle(self):
    return self.ID.maximumHorizontalAngle()
  maximumHorizontalAngle = property(getMaximumHorizontalAngle, setMaximumHorizontalAngle)
  
  def setMaximumVerticalAngle(self, anAngle):
    self.ID.setMaximumVerticalAngle(anAngle)    
  def getMaximumVerticalAngle(self):
    return self.ID.maximumVerticalAngle()
  maximumVerticalAngle = property(getMaximumVerticalAngle, setMaximumVerticalAngle)
  
  def setMinimumHorizontalAngle(self, anAngle):
    self.ID.setMinimumHorizontalAngle(anAngle)    
  def getMinimumHorizontalAngle(self):
    return self.ID.minimumHorizontalAngle()
  minimumHorizontalAngle = property(getMinimumHorizontalAngle, setMinimumHorizontalAngle)
  
  def setMinimumVerticalAngle(self, anAngle):
    self.ID.setMinimumVerticalAngle(anAngle)    
  def getMinimumVerticalAngle(self):
    return self.ID.minimumVerticalAngle()
  minimumVerticalAngle = property(getMinimumVerticalAngle, setMinimumVerticalAngle)
  
  def setPointOfView(self, aNode):
    self.ID.setPointOfView(aNode.ID)    
  def getPointOfView(self):
    return Node.outof(self.ID.pointOfView())
  pointOfView = property(getPointOfView, setPointOfView)
  
  def setTarget(self, aTarget):
    self.ID.setTarget(vector3Make(aTarget))
  def getTarget(self):
    aTarget = self.ID.target()
    return Vector3(aTarget.a, aTarget.b, aTarget.c)
  target = property(getTarget, setTarget)
  
  def setWorldUp(self, up):
    self.ID.setWorldUp(vector3Make(up))
  def getWorldUp(self):
    up = self.ID.worldUp()
    return Vector3(up.a, up.b, up.c)
  worldUp = property(getWorldUp, setWorldUp)
  
  def beginInteraction(self, location=None, withViewport=None):
    self.ID.beginInteraction_withViewport_(location, withViewport)
  beginInteractionWith = beginInteraction
    
  def clearRoll(self):
    self.ID.clearRoll()
    
  def continueInteraction(self, location=None, withViewport=None, sensitivity=None):
    self.ID.continueInteraction_withViewport_sensitivity_(location, withViewport, sensitivity)
  continueInteractionWith = continueInteraction
    
  def dollyBy(self, delta, onScreenPoint=None, viewPort=None):
    self.ID.dollyBy_onScreenPoint_viewport_(delta, onScreenPoint, viewPort)
    
  def dollyToTarget(self, delta):
    self.ID.dollyToTarget_(delta)
    
  def endInteraction(self, location=None, withViewport=None, velocity=None):
    self.ID.endInteraction_withViewport_velocity_(location, withViewport, velocity)
  endInteractionWith = endInteraction
    
  def frameNodes(self, nodeList=None):
    nList = [aNode.ID for aNode in nodeList]
    self.ID.frameNodes_(nList)
    
  def rollBy(self, delta, aroundScreenPoint=None, viewport=None):
    self.ID.rollBy_aroundScreenPoint_viewport_(delta, aroundScreenPoint, viewport)
    
  def rollAroundTarget(self, delta=None):
    self.ID.rollAroundTarget_(delta)
    
  def rotateBy(self, X=None, Y=None):
    self.ID.rotateByX_Y_(X, Y)   
  rotateByX = rotateBy 
    
  def stopInertia(self):
    self.ID.stopInertia()
    
  def translateInCameraSpaceBy(self, X=None, Y=None, Z=None):
    self.ID.translateInCameraSpaceByX_Y_Z_(X, Y, Z)
  translateInCameraSpaceByX = translateInCameraSpaceBy
  
def cameraInertiaDidEndForController_(_self, _cmd, cameraController):
  aCameraControllerDelegate = sceneKit.CameraControllerDelegate.outof(ObjCInstance(_self))
  if aCameraControllerDelegate.methods[0]:
    aCameraController = sceneKit.CameraController.outof(ObjCInstance(cameraController))
    aCameraControllerDelegate.delegate.cameraInertiaDidEnd(aCameraController)

def cameraInertiaWillStartForController_(_self, _cmd, cameraController):
  aCameraControllerDelegate = sceneKit.CameraControllerDelegate.outof(ObjCInstance(_self))
  if aCameraControllerDelegate.methods[1]:
    aCameraController = sceneKit.CameraController.outof(ObjCInstance(cameraController))
    aCameraControllerDelegate.delegate.cameraInertiaWillStart(aCameraController)
  
class CameraControllerDelegate(CInst):
  _actions = ('cameraInertiaDidEnd', 'cameraInertiaWillStart')
  _newCClassName = 'SCNPYCameraControllerDelegateClass'
  _cMethodList = [cameraInertiaDidEndForController_, cameraInertiaWillStartForController_]
  _protocols =['SCNCameraControllerDelegate']
  DelegateCClass = create_objc_class(_newCClassName, NSObject, methods=_cMethodList, protocols=_protocols)
  
  def __init__(self, aDelegate, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.delegate = aDelegate
      self.methods = [callable(_a) for _a in [getattr(aDelegate, anAction, False) for anAction in CameraControllerDelegate._actions]]
      self.ID = CameraControllerDelegate.DelegateCClass.alloc().init().autorelease()
