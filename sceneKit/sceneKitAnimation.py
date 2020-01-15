'''animation modul, to be included in sceneKit'''

from random import random

import sceneKit

from .sceneKitEnv import *

class ActionTimingMode(Enum):
  Linear = 0
  EaseIn = 1
  EaseOut= 2
  EaseInEaseOut = 3
  SCNActionTimingModeLinear = 0
  SCNActionTimingModeEaseIn = 1
  SCNActionTimingModeEaseOut= 2
  SCNActionTimingModeEaseInEaseOut = 3
  
_CAMediaTimingFunctionNames = []
for aName in ['kCAMediaTimingFunctionDefault', 'kCAMediaTimingFunctionEaseIn', 'kCAMediaTimingFunctionEaseInEaseOut', 'kCAMediaTimingFunctionEaseOut', 'kCAMediaTimingFunctionLinear']:
  _CAMediaTimingFunctionNames.append(str(ObjCInstance(c_void_p.in_dll(c, aName))))
_CAMediaTimingFunctionNames = tuple(_CAMediaTimingFunctionNames)
kCAMediaTimingFunctionDefault, kCAMediaTimingFunctionEaseIn, kCAMediaTimingFunctionEaseInEaseOut, kCAMediaTimingFunctionEaseOut, \
kCAMediaTimingFunctionLinear = _CAMediaTimingFunctionNames
MediaTimingFunctionDefault, MediaTimingFunctionEaseIn, MediaTimingFunctionEaseInEaseOut, MediaTimingFunctionEaseOut, \
MediaTimingFunctionLinear = _CAMediaTimingFunctionNames

_CAValueFunctions = []
for aFunc in ['kCAValueFunctionRotateX', 'kCAValueFunctionRotateY', 'kCAValueFunctionRotateZ', 'kCAValueFunctionScale', 'kCAValueFunctionScaleX', 'kCAValueFunctionScaleY', 'kCAValueFunctionScaleZ', 'kCAValueFunctionTranslate', 'kCAValueFunctionTranslateX', 'kCAValueFunctionTranslateY', 'kCAValueFunctionTranslateZ']:
  _CAValueFunctions.append(str(ObjCInstance(c_void_p.in_dll(c, aFunc))))
_CAValueFunctions = tuple(_CAValueFunctions)
kCAValueFunctionRotateX, kCAValueFunctionRotateY, kCAValueFunctionRotateZ, kCAValueFunctionScale, kCAValueFunctionScaleX, \
kCAValueFunctionScaleY, kCAValueFunctionScaleZ, kCAValueFunctionTranslate, kCAValueFunctionTranslateX, kCAValueFunctionTranslateY, \
kCAValueFunctionTranslateZ = _CAValueFunctions
ValueFunctionRotateX, ValueFunctionRotateY, ValueFunctionRotateZ, ValueFunctionScale, ValueFunctionScaleX, \
ValueFunctionScaleY, ValueFunctionScaleZ, ValueFunctionTranslate, ValueFunctionTranslateX, ValueFunctionTranslateY, \
ValueFunctionTranslateZ = _CAValueFunctions

_CAAnimationCalculationModes = []
for aMode in ['kCAAnimationCubic', 'kCAAnimationCubicPaced', 'kCAAnimationDiscrete', 'kCAAnimationLinear', 'kCAAnimationPaced']:
  _CAAnimationCalculationModes.append(str(ObjCInstance(c_void_p.in_dll(c, aMode))))
_CAAnimationCalculationModes = tuple(_CAAnimationCalculationModes)
kCAAnimationCubic, kCAAnimationCubicPaced, kCAAnimationDiscrete, kCAAnimationLinear, kCAAnimationPaced = _CAAnimationCalculationModes
AnimationCubic, AnimationCubicPaced, AnimationDiscrete, AnimationLinear, AnimationPaced = _CAAnimationCalculationModes

_CAAnimationRotationModes = []
for aMode in ['kCAAnimationRotateAuto', 'kCAAnimationRotateAutoReverse']:
  _CAAnimationRotationModes.append(str(ObjCInstance(c_void_p.in_dll(c, aMode))))
_CAAnimationRotationModes = tuple(_CAAnimationRotationModes)
kCAAnimationRotateAuto, kCAAnimationRotateAutoReverse = _CAAnimationRotationModes
AnimationRotateAuto, AnimationRotateAutoReverse = _CAAnimationRotationModes

class Action(CInst):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = None

  def setDuration(self, aDurarion):
    self.ID.setDuration(aDurarion)    
  def getDuration(self):
    return self.ID.duration()
  duration = property(getDuration, setDuration)
  
  def setSpeed(self, aspeed):
    self.ID.setSpeed(aspeed)    
  def getSpeed(self):
    return self.ID.speed()
  speed = property(getSpeed, setSpeed)
  
  def setTimingMode(self, aTimingMode):
    self.ID.setTimingMode(aTimingMode.value)
  def getTimingMode(self):
    return ActionTimingMode(self.ID.timingMode())
  timingMode = property(getTimingMode, setTimingMode)
  
  @classmethod
  def moveBy(cls, *args):
    if len(args) == 2 and len(args[0]) == 3:
      return MoveBy(args[0][0], args[0][1], args[0][2], args[1])
    else:
      return MoveBy(*args)
      
  @classmethod
  def moveTo(cls, *args):
    return MoveTo(*args)
    
  @classmethod
  def rotateBy(cls, *args):
    if len(args) == 2 and len(args[0]) == 3:
      return RotateBy(args[0][0], args[0][1], args[0][2], args[1])
    elif len(args) == 3:
      return rotateByAroundAxis(*args)
    elif len(args) == 5:
      return rotateByAroundAxis(args[0], Vector3(args[1], args[2], args[3]), args[4])
    else:
      return RotateBy(*args)
      
  @classmethod
  def rotateByAroundAxis(cls, *args):
    return RotateByAroundAxis(*args)
    
  @classmethod
  def rotateByAngleAroundAxis(cls, *args):
    return RotateByAngleAroundAxis(*args)
      
  @classmethod
  def rotateTo(cls, *args, shortestUnitArc=None):
    if len(args) == 2 and len(args[0]) == 3:
      return RotateTo(args[0][0], args[0][1], args[0][2], args[1], shortestUnitArc=shortestUnitArc)
    else:
      return RotateTo(*args, shortestUnitArc=shortestUnitArc)
      
  @classmethod
  def rotateToAxisAngle(cls, *args):
    return RotateToAxisAngle(*args)
      
  @classmethod
  def scaleBy(cls, *args):
    return ScaleBy(*args)
      
  @classmethod
  def scaleTo(cls, *args):
    return ScaleTo(*args)
      
  @classmethod
  def fadeInWithDuration(cls, *args):
    return FadeInWithDuration(*args)
      
  @classmethod
  def fadeOutWithDuration(cls, *args):
    return FadeOutWithDuration(*args)
    
  @classmethod
  def fadeOpacityBy(cls, *args):
    return FadeOpacityBy(*args)
    
  @classmethod
  def fadeOpacityTo(cls, *args):
    return FadeOpacityTo(*args)
    
  @classmethod
  def hide(cls, *args):
    return Hide(*args)
    
  @classmethod
  def unhide(cls, *args):
    return Unhide(*args)
    
  @classmethod
  def playAudioSource(cls, *args):
    return PlayAudioSource(*args)
    
  @classmethod
  def removeFromParentNode(cls, *args):
    return RemoveFromParentNode(*args)
    
  @classmethod
  def group(cls, *args):
    return Group(*args)
    
  @classmethod
  def sequence(cls, *args):
    return Sequence(*args)
    
  @classmethod
  def repeatAction(cls, *args):
    return RepeatAction(*args)
    
  @classmethod
  def repeatActionForever(cls, *args):
    return RepeatActionForever(*args)
    
  @classmethod
  def waitForDuration(cls, duration=0.0, withRange=None):
    return WaitForDuration(duration, withRange)
    
  @classmethod
  def runBlock(cls, *args):
    return RunBlock(*args)
   
  @classmethod
  def customActionWithDuration(cls, *args):
    return CustomActionWithDuration(*args)
       
  def reversedAction(self):
    return Action.outof(self.ID.reversedAction())
    
  def setTimingFunction(self, aTimingFunc=lambda x:x):
    blockInstance = ActionTimingFunctionBlock(aTimingFunc)
    self.ID.setTimingFunction_(blockInstance.ID)
  def getTimingFunction(self):
    aTimingFunc = sceneKit.ActionTimingFunctionBlock.outof(self.ID.timingFunction())
    return aTimingFunc.pCode    
  timingFunction = property(getTimingFunction, setTimingFunction)
  
class ActionTimingFunctionBlock(CInst):
  def __init__(self, block, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = ObjCBlock(self.blockInterface, restype=c_float, argtypes=[c_void_p, c_float])
      self.pCode = block
    
  def blockInterface(self, _cmd, time):
    return self.pCode(time)
  
class MoveBy(Action):
  def __init__(self, x=0.0, y=0.0, z=0.0, duration=0.0):
    self.ID = SCNAction.moveByX_y_z_duration_(x, y, z, duration)
    
class MoveTo(Action):
  def __init__(self, aVector3, duration=0.0):
    self.ID = SCNAction.moveTo_duration_(vector3Make(aVector3), duration)
    
class RotateBy(Action):
  def __init__(self, x=0.0, y=0.0, z=0.0, duration=0.0):
    self.ID = SCNAction.rotateByX_y_z_duration_(x, y, z, duration)
    
class RotateByAroundAxis(Action):
  def __init__(self, angle=0.0, axis=Vector3(0,0,0), duration=0.0):
    self.ID = SCNAction.rotateByAngle_aroundAxis_duration_(angle, vector3Make(axis), duration)
    
RotateByAngleAroundAxis = RotateByAroundAxis

class RotateTo(Action):
  def __init__(self, x=0.0, y=0.0, z=0.0, duration=0.0, shortestUnitArc=None):
    if shortestUnitArc is None:
      self.ID = SCNAction.rotateToX_y_z_duration_(x, y, z, duration)
    else:
      self.ID = SCNAction.rotateToX_y_z_duration_shortestUnitArc_(x, y, z, duration, shortestUnitArc)
      
class RotateToAxisAngle(Action):
  def __init__(self, axisAngle=Vector4(0,0,0,0), duration=0.0):
    self.ID = SCNAction.rotateToAxisAngle_duration_(vector4Make(axisAngle), duration)
    
class ScaleBy(Action):
  def __init__(self, scale=1.0, duration=0.0):
    self.ID = SCNAction.scaleBy_duration_(scale, duration)
    
class ScaleTo(Action):
  def __init__(self, scale=1.0, duration=0.0):
    self.ID = SCNAction.scaleTo_duration_(scale, duration)
    
class FadeInWithDuration(Action):
  def __init__(self, duration=0.0):
    self.ID = SCNAction.fadeInWithDuration_(duration) 

class FadeOutWithDuration(Action):
  def __init__(self, duration=0.0):
    self.ID = SCNAction.fadeOutWithDuration_(duration)
    
class FadeOpacityBy(Action):
  def __init__(self, opacity=0.0, duration=0.0):
    self.ID = SCNAction.fadeOpacityBy_duration_(opacity, duration)
    
class FadeOpacityTo(Action):
  def __init__(self, opacity=0.0, duration=0.0):
    self.ID = SCNAction.fadeOpacityTo_duration_(opacity, duration)
    
class Hide(Action):
  def __init__(self):
    self.ID = SCNAction.hide()
    
class Unhide(Action):
  def __init__(self):
    self.ID = SCNAction.unhide()
    
class RemoveFromParentNode(Action):
  def __init__(self):
    self.ID = SCNAction.removeFromParentNode()
    
class PlayAudioSource(Action):
  def __init__(self, source=None, wait=None, waitForCompletion=None):
    if waitForCompletion is not None: wait = waitForCompletion
    self.ID = SCNAction.playAudioSource_waitForCompletion_(source.ID, wait)
    
class Group(Action):
  def __init__(self, actions):
    actionList = [anAction.ID for anAction in actions]
    self.ID = SCNAction.group_(actionList)
     
class Sequence(Action):
  def __init__(self, actions):
    actionList = [anAction.ID for anAction in actions]
    self.ID = SCNAction.sequence_(actionList)
    
class RepeatAction(Action):
  def __init__(self, action, count=1):
    self.ID = SCNAction.repeatAction_count_(action.ID, count)
    
class RepeatActionForever(Action):
  def __init__(self, action):
    self.ID = SCNAction.repeatActionForever_(action.ID)
    
class WaitForDuration(Action):
  def __init__(self, duration=0.0, withRange=None):
    if withRange is None:
      self.ID = SCNAction.waitForDuration_(duration)
    else:
      self.ID = SCNAction.waitForDuration_withRange_(duration, withRange)
      
class RunBlock(Action):
  def __init__(self, block):
    self.blockCode = ObjCBlock(self.blockInterface, restype=None, argtypes=[c_void_p, c_void_p])
    self.pCode = block
    self.ID = SCNAction.runBlock_(self.blockCode)
    
  def blockInterface(self, _cmd, node):
    node = sceneKit.Node.outof(ObjCInstance(node))
    self.pCode(node)
    
class CustomActionWithDuration(Action):
  def __init__(self, duration=None, block=None, seconds=None, action=None):
    if duration is None: duration = seconds
    if block is None: block = action
    self.blockCode = ObjCBlock(self.blockInterface, restype=None, argtypes=[c_void_p, c_void_p, c_double])
    self.pCode = block
    self.ID = SCNAction.customActionWithDuration_actionBlock_(duration, self.blockCode)
    
  def blockInterface(self, _cmd, node, elapsedTime):
    node = sceneKit.Node.outof(ObjCInstance(node))
    self.pCode(node, elapsedTime)
    
    
class Actionable: 
  def runAction(self, action, forKey=None, completionHandler=None, key=None, block=None):
    if block is not None: completionHandler = block
    if key is not None: forKey = key
    if ~isinstance(forKey, str) and completionHandler is None: completionHandler = forKey
    if forKey is None and completionHandler is None:
      self.ID.runAction_(action.ID)
    elif forKey is None and completionHandler is not None:
      self.ID.runAction_completionHandler_(action.ID, completionHandler)
    elif forKey is not None and completionHandler is None:
      self.ID.runAction_forKey_(action.ID, forKey)
    else:
      self.ID.runAction_forKey_completionHandler_(action.ID, forKey, completionHandler)
      
  def actionForKey(self, key):
    return Action.outof(self.ID.actionForKey_(key))

  def setHasActions(self, aBool):
    self.ID.setHasActions(aBool)    
  def getHasActions(self):
    return self.ID.hasActions()
  hasActions = property(getHasActions, setHasActions)
  
  def getActionKeys(self):
    keys = self.ID.actionKeys()
    return tuple(keys)
  actionKeys = property(getActionKeys, None)
  
  def removeActionForKey(self, key):
    self.ID.removeActionForKey_(key)
    
  def removeAllActions(self):
    self.ID.removeAllActions()
    
class TransactionClass:
  def __init__(self):
    self.pCode = None
    
  @classmethod
  def begin(cls):
    SCNTransaction.begin()
    
  @classmethod 
  def commit(cls):
    SCNTransaction.commit()
    
  @classmethod 
  def flush(cls):
    SCNTransaction.flush()

  def setAnimationDuration(self, anAnimationDuration):
    SCNTransaction.setAnimationDuration(anAnimationDuration)    
  def getAnimationDuration(self):
    return SCNTransaction.animationDuration()
  animationDuration = property(getAnimationDuration, setAnimationDuration)
  
  def setDisableActions(self, aBool):
    SCNTransaction.setDisableActions(aBool)    
  def getDisableActions(self):
    return SCNTransaction.disableActions()
  disableActions = property(getDisableActions, setDisableActions)
  
  @classmethod
  def lock(cls):
    SCNTransaction.lock()
    
  @classmethod  
  def unlock(cls):
    SCNTransaction.unlock()
    
  @classmethod
  def setValueForKey(cls, value, key):
    SCNTransaction.setValue_forKey_(value, key)
    
  @classmethod
  def valueForKey(cls, key):
    return SCNTransaction.valueForKey_(key)
    
  def setAnimationTimingFunction(self, aFunc):
    SCNTransaction.setAnimationTimingFunction_(aFunc.ID)    
  def getAnimationTimingFunction(self):
    return sceneKit.TimingFunction.outof(SCNTransaction.animationTimingFunction())
  animationTimingFunction = property(getAnimationTimingFunction, setAnimationTimingFunction)
  
  def setCompletionBlock(self, aBlock):
    self.pCode = aBlock
    SCNTransaction.setCompletionBlock_(aBlock)
  def getCompletionBlock(self):
    return self.pCode
  completionBlock = property(getCompletionBlock, setCompletionBlock)
    
Transaction = TransactionClass()

class Animatable:
  def addAnimation(self, animation, key=None):
    if key is not None: key = str(key)
    self.ID.addAnimation_forKey_(animation.ID, key)
    
  def getAnimationKeys(self):
    keys = self.ID.animationKeys()
    return tuple(str(aKey) for aKey in keys)
  animationKeys = property(getAnimationKeys, None)
  
  def removeAllAnimations(self):
    self.ID.removeAllAnimations()
    
  def removeAnimation(self, key):
    self.ID.removeAnimationForKey_(key)
    
  def addAnimationPlayer(self, player, key=None):
    if key is not None: key = str(key)
    self.ID.addAnimationPlayer_forKey_(player.ID, key)
    
  def animationPlayerForKey(self, key):
    return sceneKit.AnimationPlayer.outof(self.ID.animationPlayerForKey_(key))
    
  def removeAnimationForKey(self, key, duration=0., blendOutDuration=None):
    if blendOutDuration is not None:
      duration = blendOutDuration
    if duration > 0.:
      self.ID.removeAnimationForKey_blendOutDuration_(key, duration)
    else:
      self.ID.removeAnimationForKey_(key)
    
class AnimationPlayer(CInst, Animatable):
  def __init__(self, animation=None, ID=None):
    if animation is not None:
      self.ID = SCNAnimationPlayer.animationPlayerWithAnimation_(animation.ID)
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = None
      
  @classmethod
  def animationPlayerWithAnimation(cls, animation=None):
    return cls(animation=animation)
    
  def setAnimation(self, anAnimation):
    self.ID.setAnimation(anAnimation.ID)    
  def getAnimation(self):
    return Animation.outof(self.ID.animation())
  animation = property(getAnimation, setAnimation)
      
  def setBlendFactor(self, aBlendFactor):
    self.ID.setBlendFactor(aBlendFactor)    
  def getBlendFactor(self):
    return self.ID.blendFactor()
  blendFactor = property(getBlendFactor, setBlendFactor)
  
  def setPaused(self, aBool):
    self.ID.setPaused(aBool)    
  def getPaused(self):
    return self.ID.paused()
  paused = property(getPaused, setPaused)
  
  def setSpeed(self, aSpeed):
    self.ID.setSpeed(aSpeed)    
  def getSpeed(self):
    return self.ID.speed()
  speed = property(getSpeed, setSpeed)
  
  def play(self):
    self.ID.play()
    
  def stop(self):
    self.ID.stop()
    
  def stopWithBlendOutDuration(self, duration=0.0):
    self.ID.stopWithBlendOutDuration_(duration)
  
class Animation(CInst):
  def __init__(self, name=None, URL=None, caAnimation=None, ID=None):
    if name is not None:
      self.ID = SCNAnimation.animationNamed_(name)
    elif URL is not None:
      self.ID = SCNAnimation.animationWithContentsOfURL_(nsurl(URL))
    elif caAnimation is not None:
      if isinstance(caAnimation, sceneKit.CoreAnimation): caAnimation = caAnimation.ID
      self.ID = SCNAnimation.animationWithCAAnimation_(caAnimation)
    elif ID is not None:
      self.ID = ID      
    else:
      self.ID = None
      
  @classmethod
  def animationWithCAAnimation(cls, caAnimation=None):
    return cls(caAnimation=caAnimation)
      
  @classmethod
  def animationNamed(cls, name=None):
    return cls(name=name)
  
  @classmethod
  def animationWithContentsOfURL(cls, URL=None):
    return cls(URL=URL)
    
  def setAnimationDidStart(self, aBlock):
    self.animationDidStartBlock = AnimationDidStartBlock(aBlock)
    self.ID.setAnimationDidStart_(self.animationDidStartBlock.blockCode)
  def getAnimationDidStart(self):
    return self.animationDidStartBlock.pCode
  animationDidStart = property(getAnimationDidStart, setAnimationDidStart)
  
  def setAnimationDidStop(self, aBlock):
    self.animationDidStopBlock = AnimationDidStopBlock(aBlock)
    self.ID.setAnimationDidStop_(self.animationDidStopBlock.blockCode)    
  def getAnimationDidStop(self):
    return self.animationDidStopBlock.pCode
  animationDidStop = property(getAnimationDidStop, setAnimationDidStop)
    
  def setAnimationEvents(self, animationEvents):
    try:
      iterator = iter(animationEvents)
    except TypeError:
      animationEvents = [animationEvents]
    self.ID.setAnimationEvents([anEvent.ID for anEvent in animationEvents])
  def getAnimationEvents(self):
    animationEventsList = self.ID.animationEvents()
    animationEvents = [sceneKit.AnimationEvent.outof(anEvent) for anEvent in animationEventsList]
    return tuple(animationEvents)
  animationEvents = property(getAnimationEvents, setAnimationEvents)
  
  def setAutoreverses(self, aBool):
    self.ID.setAutoreverses(aBool)    
  def getAutoreverses(self):
    return self.ID.autoreverses()
  autoreverses = property(getAutoreverses, setAutoreverses)
  
  def setBlendInDuration(self, aBlendInDuration):
    self.ID.setBlendInDuration(aBlendInDuration)    
  def getBlendInDuration(self):
    return self.ID.blendInDuration()
  blendInDuration = property(getBlendInDuration, setBlendInDuration)
  
  def setBlendOutDuration(self, aBlendOutDuration):
    self.ID.setBlendOutDuration(aBlendOutDuration)    
  def getBlendOutDuration(self):
    return self.ID.blendOutDuration()
  blendOutDuration = property(getBlendOutDuration, setBlendOutDuration)
  
  def setDuration(self, aDuration):
    self.ID.setDuration(aDuration)    
  def getDuration(self):
    return self.ID.duration()
  duration = property(getDuration, setDuration)
  
  def setFillsBackward(self, aBool):
    self.ID.setFillsBackward(aBool)    
  def getFillsBackward(self):
    return self.ID.fillsBackward()
  fillsBackward = property(getFillsBackward, setFillsBackward)
  
  def setFillsForward(self, aBool):
    self.ID.setFillsForward(aBool)    
  def getFillsForward(self):
    return self.ID.fillsForward()
  fillsForward = property(getFillsForward, setFillsForward)
  
  def setAdditive(self, aBool):
    self.ID.setAdditive(aBool)    
  def isAdditive(self):
    return self.ID.isAdditive()
  additive = property(isAdditive, setAdditive)
  
  def setAppliedOnCompletion(self, aBool):
    self.ID.setAppliedOnCompletion(aBool)    
  def isAppliedOnCompletion(self):
    return self.ID.isAppliedOnCompletion()
  appliedOnCompletion = property(isAppliedOnCompletion, setAppliedOnCompletion)
  
  def setCumulative(self, aBool):
    self.ID.setCumulative(aBool)    
  def isCumulative(self):
    return self.ID.isCumulative()
  cumulative = property(isCumulative, setCumulative)
  
  def setRemovedOnCompletion(self, aBool):
    self.ID.setRemovedOnCompletion(aBool)    
  def isRemovedOnCompletion(self):
    return self.ID.isRemovedOnCompletion()
  removedOnCompletion = property(isRemovedOnCompletion, setRemovedOnCompletion)
  
  def setKeyPath(self, aKeyPath):
    self.ID.setKeyPath(str(aKeyPath))
  def getKeyPath(self):
    keyPath = self.ID.keyPath()
    return str(keyPath) if keyPath is not None else None
  keyPath = property(getKeyPath, setKeyPath)
  
  def setRepeatCount(self, aRepeatCount):
    self.ID.setRepeatCount(aRepeatCount)    
  def getRepeatCount(self):
    return self.ID.repeatCount()
  repeatCount = property(getRepeatCount, setRepeatCount)
  
  def setStartDelay(self, aStartDelay):
    self.ID.setStartDelay(aStartDelay)    
  def getStartDelay(self):
    return self.ID.startDelay()
  startDelay = property(getStartDelay, setStartDelay)
  
  def setTimeOffset(self, aTimeOffset):
    self.ID.setTimeOffset(aTimeOffset)    
  def getTimeOffset(self):
    return self.ID.timeOffset()
  timeOffset = property(getTimeOffset, setTimeOffset)
  
  def setTimingFunction(self, aTimingFunction):
    self.ID.setTimingFunction(aTimingFunction.ID)    
  def getTimingFunction(self):
    return TimingFunction.outof(self.ID.timingFunction())
  timingFunction = property(getTimingFunction, setTimingFunction)
  
  def setUsesSceneTimeBase(self, aBool):
    self.ID.setUsesSceneTimeBase(aBool)    
  def getUsesSceneTimeBase(self):
    return self.ID.usesSceneTimeBase()
  usesSceneTimeBase = property(getUsesSceneTimeBase, setUsesSceneTimeBase)
  
class AnimationDidStartBlock:
  def __init__(self, block):    
    self.blockCode = ObjCBlock(self.blockInterface, restype=None, argtypes=[c_void_p, c_void_p, c_void_p])
    self.pCode = block
      
  def blockInterface(self, _cmd, xAnimation, xReceiver):
    animation = sceneKit.Animation.outof(ObjCInstance(xAnimation))
    receiver = sceneKit.CInst.outof(ObjCInstance(xReceiver)) if xReceiver is not None else None
    self.pCode(animation, receiver)
    
class AnimationDidStopBlock:
  def __init__(self, block):    
    self.blockCode = ObjCBlock(self.blockInterface, restype=None, argtypes=[c_void_p, c_void_p, c_void_p, c_bool])
    self.pCode = block
      
  def blockInterface(self, _cmd, xAnimation, xReceiver, completed):
    animation = sceneKit.Animation.outof(ObjCInstance(xAnimation))
    receiver = sceneKit.CInst.outof(ObjCInstance(xReceiver)) if xReceiver is not None else None
    self.pCode(animation, receiver, completed)
    
class AnimationEvent(CInst):
  def __init__(self, time=0, block=None, eventBlock=None, ID=None):
    if eventBlock is not None: block = eventBlock
    if block is not None:
      self.blockCode = ObjCBlock(self.blockInterface, restype=None, argtypes=[c_void_p, c_void_p, c_void_p, c_bool])
      self.ID = SCNAnimationEvent.animationEventWithKeyTime_block_(time, self.blockCode)
      self.pCode = block
    elif ID is not None:
      self.ID = ID      
    else:
      self.ID = None
      
  def blockInterface(self, _cmd, xAnimation, xAnimatedObject, playingBackward):
    animation = sceneKit.Animation.outof(ObjCInstance(xAnimation))
    animatedObject = sceneKit.CInst.outof(ObjCInstance(xAnimatedObject))
    self.pCode(animation, animatedObject, playingBackward)
    
  @classmethod
  def animationEventWithKeyTime(cls, time=0., block=None, eventBlock=None):
    return cls(time=time, block=block, eventBlock=eventBlock)
    

class TimingFunction(CInst):
  def __init__(self, timingMode=None, aCoreMediaTimingFunction=None, ID=None):
    if timingMode is not None:
      self.ID = SCNTimingFunction.functionWithTimingMode_(timingMode.value)
    elif aCoreMediaTimingFunction is not None:
      if isinstance(aCoreMediaTimingFunction, sceneKit.CoreMediaTimingFunction):
        aCoreMediaTimingFunction = aCoreMediaTimingFunction.ID
      self.ID = SCNTimingFunction.functionWithCAMediaTimingFunction_(aCoreMediaTimingFunction)
    elif ID is not None:
      self.ID = ID      
    else:
      self.ID = None
    
  @classmethod
  def functionWithTimingMode(cls, timingMode):
    return cls(timingMode=timingMode)
    
  @classmethod
  def functionWithCAMediaTimingFunction(cls, aCoreMediaTimingFunction=None):
    return cls(aCoreMediaTimingFunction=aCoreMediaTimingFunction)
  
    
class CoreMediaTimingFunction(CInst):
  def __init__(self, name=None, c1x=0., c1y=0., c2x=0., c2y=0., ID=None):
    if ID is not None:
      self.ID = ID
    elif name is not None:
      self.ID = CAMediaTimingFunction.functionWithName_(name)
    else:
      self.ID = CAMediaTimingFunction.functionWithControlPoints____(c1x, c1y, c2x, c2y)
      
  @classmethod
  def functionWithName(cls, name=None):
    return cls(name=name)
    
  @classmethod
  def functionWithControlPoints(cls, c1x=0., c1y=0., c2x=0., c2y=0.):
    return cls(c1x, c1y, c2x, c2y)
    
  def initWithControlPoints(self, c1x=0., c1y=0., c2x=0., c2y=0.):
    self.ID.initWithControlPoints____(c1x, c1y, c2x, c2y)
    
  def getControlPointAtIndex(self, idx=0):
    cidx = c_int(idx) if idx in [0, 1, 2, 3] else 0
    res_type = c_float * 2
    res = res_type()
    self.ID.getControlPointAtIndex_values_(cidx, byref(res), restype=None, argtypes=[c_int, POINTER(res_type)])
    return tuple(res)
    
class CoreValueFunction(CInst):
  def __init__(self, name=None, ID=None):
    if ID is not None:
      self.ID = ID
    elif name is not None:
      self.ID = CAValueFunction.functionWithName_(name)
    else:
      self.ID = None
      
  @classmethod
  def functionWithName(cls, name=None):
    return cls(name=name)
    
  def getName(self):
    return self.ID.name()
  name = property(getName, None)
  
class CorePropertyAnimation:
  @classmethod
  def animationWithKeyPath(cls, aPath):
    return cls(aPath)
    
  vector3Indicator = 1000000 + 10000000*random()

  def setKeyPath(self, aPath):
    self.ID.setKeyPath_(str(aPath))
  def getKeyPath(self):
    return str(self.ID.keyPath())
  keyPath = property(getKeyPath, setKeyPath)
  
  def setCumulative(self, aBool):
    self.ID.setCumulative_(aBool)    
  def isCumulative(self):
    return self.ID.cumulative()
  cumulative = property(isCumulative, setCumulative)
  
  def setAdditive(self, aBool):
    self.ID.setAdditive_(aBool)    
  def isAdditive(self):
    return self.ID.additive()
  additive = property(isAdditive, setAdditive)
  
  def setValueFunction(self, aFunc):
    if isinstance(aFunc, sceneKit.CoreValueFunction): aFunc = aFunc.ID
    self.ID.setValueFunction_(aFunc)    
  def getValueFunction(self):
    return sceneKit.CoreValueFunction.outof(self.ID.valueFunction())
  valueFunction = property(getValueFunction, setValueFunction)
  
  def valueFromP(self, aValue):
    if isinstance(aValue, (int, float)):
      return ns(aValue)
    elif isinstance(aValue, (Vector3, SCNVector3)):
      return NSValue.valueWithSCNVector4_(SCNVector4(aValue[0], aValue[1], aValue[2], self.vector3Indicator), restype=c_void_p, argtypes=[SCNVector4])
    elif isinstance(aValue, (Vector4, Quaternion, SCNVector4)):
      return NSValue.valueWithSCNVector4_(SCNVector4(aValue[0], aValue[1], aValue[2], aValue[3]), restype=c_void_p, argtypes=[SCNVector4])
    else:   
      r, g, b, a = parse_color(aValue)
      return UIColor.color(red=r, green=g, blue=b, alpha=a)
      
  def valueFromC(self, aValue):
    try:
      return aValue.floatValue()
    except AttributeError:
      pass
    try:
      return RGBA(aValue.red(), aValue.green(), aValue.blue(), aValue.alpha())
    except AttributeError:
      pass
    try:
      aValue = getCStructValuesAsList(aValue.SCNVector4Value())
      if abs(aValue[3]-self.vector3Indicator) < 10.0 :
        return vector3Make(aValue[0:3])
      else:
        return vector4Make(aValue)
    except AttributeError:
      return None
    
class CoreAnimation(CInst, CorePropertyAnimation):
  def __init__(self, animation=None, ID=None):
    if ID is not None:
      self.ID = ID
    elif animation is not None:
      self.ID = CAAnimation.animationWithSCNAnimation_(animation.ID)
    else:
      self.ID = CAAnimation.animation()
      
  @classmethod
  def animation(cls):
    return cls()
    
  @classmethod
  def animationWithSCNAnimation(cls, anSCNAnimation=None):
    return cls(animation=anSCNAnimation)

  def setRemovedOnCompletion(self, aBool):
    self.ID.setRemovedOnCompletion_(aBool)    
  def isRemovedOnCompletion(self):
    return self.ID.removedOnCompletion()
  removedOnCompletion = property(isRemovedOnCompletion, setRemovedOnCompletion)
  
  def setTimingFunction(self, aTimingFunction):
    if isinstance(aTimingFunction, CoreMediaTimingFunction):
      aTimingFunction = aTimingFunction.ID
    self.ID.setTimingFunction_(aTimingFunction)    
  def getTimingFunction(self):
    return sceneKit.CoreMediaTimingFunction.outof(self.ID.timingFunction())
  timingFunction = property(getTimingFunction, setTimingFunction)
  
  def setDelegate(self, aDelegate):
    aCoreAnimationDelegate = CoreAnimationDelegate(aDelegate)
    self.ID.setDelegate_(aCoreAnimationDelegate.ID)
  def getDelegate(self):
    aCoreAnimationDelegate = sceneKit.CoreAnimationDelegate.outof(self.ID.delegate())
    return aCoreAnimationDelegate.delegate
  delegate = property(getDelegate, setDelegate)
  
  @classmethod
  def defaultValueForKey(cls, key=None):
    ret = CAAnimation.defaultValueForKey_(key)
    return ret #override this method in subclasses and return the default value as desired
    
  def shouldArchiveValueForKey(self, key):
    return self.ID.shouldArchiveValueForKey_(key)
    
  def setUsesSceneTimeBase(self, aBool):
    self.ID.setUsesSceneTimeBase_(aBool)    
  def getUsesSceneTimeBase(self):
    return self.ID.usesSceneTimeBase()
  usesSceneTimeBase = property(getUsesSceneTimeBase, setUsesSceneTimeBase)
  
  def setFadeInDuration(self, aFadeInDuration):
    self.ID.setFadeInDuration_(aFadeInDuration)    
  def getFadeInDuration(self):
    return self.ID.fadeInDuration()
  fadeInDuration = property(getFadeInDuration, setFadeInDuration)
  
  def setFadeOutDuration(self, aFadeOutDuration):
    self.ID.setFadeOutDuration_(aFadeOutDuration)    
  def getFadeOutDuration(self):
    return self.ID.fadeOutDuration()
  fadeOutDuration = property(getFadeOutDuration, setFadeOutDuration)
  
  def setAnimationEvents(self, animationEvents):
    try:
      iterator = iter(animationEvents)
    except TypeError:
      animationEvents = [animationEvents]
    self.ID.setAnimationEvents([anEvent.ID for anEvent in animationEvents])   
  def getAnimationEvents(self):
    animationEventsList = self.ID.animationEvents()
    animationEvents = [sceneKit.AnimatioEvent.outof(anEvent) for anEvent in animationEventsList]
    return tuple(animationEvents)
  animationEvents = property(getAnimationEvents, setAnimationEvents)
  
def animationDidStart_(_self, _cmd, anim):
  aCoreAnimationDelegate = sceneKit.CoreAnimationDelegate.outof(ObjCInstance(_self))
  if aCoreAnimationDelegate.methods[0]:
    anAnim = sceneKit.CoreAnimation.outof(ObjCInstance(anim))
    aCoreAnimationDelegate.delegate.animationDidStart(anAnim)
    
def animationDidStop_finished_(_self, _cmd, anim, flag):
  aCoreAnimationDelegate = sceneKit.CoreAnimationDelegate.outof(ObjCInstance(_self))
  if aCoreAnimationDelegate.methods[1]:
    anAnim = sceneKit.CoreAnimation.outof(ObjCInstance(anim))
    aCoreAnimationDelegate.delegate.animationDidStop(anAnim, flag)
  
class CoreAnimationDelegate(CInst):
  _actions = ('animationDidStart', 'animationDidStop')
  _newCClassName = 'SCNPYCoreAnimationDelegateClass'
  _cMethodList = [animationDidStart_, animationDidStop_finished_]
  _protocols =['CAAnimationDelegate']
  DelegateCClass = create_objc_class(_newCClassName, NSObject, methods=_cMethodList, protocols=_protocols)
  
  def __init__(self, aDelegate, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.delegate = aDelegate
      self.methods = [callable(_a) for _a in [getattr(aDelegate, anAction, False) for anAction in CoreAnimationDelegate._actions]]
      self.ID = CoreAnimationDelegate.DelegateCClass.alloc().init()
          
class CoreBasicAnimation(CoreAnimation):
  def __init__(self, keyPath=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = CABasicAnimation.animation()
      if keyPath is not None:
        self.keyPath = keyPath
      
  def setFromValue(self, aValue):
    self.ID.setFromValue_(self.valueFromP(aValue))
  def getFromValue(self):
    return self.valueFromC(self.ID.fromValue())
  fromValue = property(getFromValue, setFromValue)
  
  def setToValue(self, aValue):
    aValue = self.valueFromP(aValue)
    self.ID.setToValue_(aValue)
  def getToValue(self):
    return self.valueFromC(self.ID.toValue())
  toValue = property(getToValue, setToValue)
  
  def setByValue(self, aValue):
    self.ID.setByValue_(self.valueFromP(aValue))    
  def getByValue(self):
    return self.valueFromC(self.ID.byValue())
  byValue = property(getByValue, setByValue)
  
  
class CoreKeyframeAnimation(CoreAnimation):
  def __init__(self, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = CAKeyframeAnimation.animation()
      
  def setValues(self, aList):
    aList = [self.valueFromP(aValue) for aValue in aList]
    self.ID.setValues_(aList)    
  def getValues(self):
    ret = self.ID.values()
    if ret is None: return None
    return tuple(self.valueFromC(aValue) for aValue in ret)
  values = property(getValues, setValues)
  
  def setKeyTimes(self, aList):
    self.ID.setKeyTimes_([ns(aValue) for aValue in aList])
  def getKeyTimes(self):
    ret = self.ID.keyTimes()
    if ret is None: return None
    return tuple(aRet.floatValue() for aRet in ret)
  keyTimes = property(getKeyTimes, setKeyTimes)
  
  def setTimingFunctions(self, aList):
    cList = []
    for aFunc in aList:
      if isinstance(aFunc, CoreMediaTimingFunction):
        cList.append(aFunc.ID)
      else:
        cList.append(aFunc)      
    self.ID.setTimingFunctions_(cList)    
  def getTimingFunctions(self):
    ret = self.ID.timingFunctions()
    if ret is None: return None
    return tuple([sceneKit.CoreMediaTimingFunction.outof(aFunc) for aFunc in ret])
  timingFunctions = property(getTimingFunctions, setTimingFunctions)
  
  def setCalculationMode(self, aMode):
    self.ID.setCalculationMode_(aMode)    
  def getCalculationMode(self):
    return str(self.ID.calculationMode())
  calculationMode = property(getCalculationMode, setCalculationMode)
  
  def setRotationMode(self, aMode):
    self.ID.setRotationMode_(aMode)    
  def getRotationMode(self):
    return str(self.ID.rotationMode())
  rotationMode = property(getRotationMode, setRotationMode)
  
  def setTensionValues(self, aList):
    self.ID.setTensionValues_([ns(aValue) for aValue in aList])    
  def getTensionValues(self):
    ret = self.ID.tensionValues()
    if ret is None: return None
    return tuple(aRet.floatValue() for aRet in ret)
  tensionValues = property(getTensionValues, setTensionValues)
  
  def setContinuityValues(self, aList):
    self.ID.setContinuityValues_([ns(aValue) for aValue in aList])    
  def getContinuityValues(self):
    ret = self.ID.continuityValues()
    if ret is None: return None
    return tuple(ret.floatValue() for aRet in ret)
  continuityValues = property(getContinuityValues, setContinuityValues)
  
  def setBiasValues(self, aList):
    self.ID.setBiasValues_([ns(aValue) for aValue in aList])    
  def getBiasValues(self):
    ret = self.ID.biasValues()
    if ret is None: return None
    return tuple(ret.floatValue() for aRet in ret)
  biasValues = property(getBiasValues, setBiasValues)
  
class CoreAnimationGroup(CoreAnimation):
  def __init__(self, animations=None, ID=None):
    if ID is not None:
      self.ID = ID
    else:
      self.ID = CAAnimationGroup.alloc().init()
      if animations is not None:
        self.setAnimations(animations)
      
  def setAnimations(self, animList):
    try:
      iterator = iter(animList)
    except TypeError:
      animList = [animList]
    animListC = [anAnim.ID if isinstance(anAnim, CoreAnimation) else anAnim for anAnim in animList]
    self.ID.setAnimations_(animListC)
  def getAnimations(self):
    ret = self.ID.animations()
    return tuple(sceneKit.CoreAnimation.outof(anAnim) for anAnim in ret)
  animations = property(getAnimations, setAnimations)
