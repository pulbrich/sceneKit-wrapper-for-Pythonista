# sceneKit-wrapper-for-Pythonista
SceneKit module access from Pythonista, pure python package using objc_util

The package provides a rather comprehensive Python interface to the **SceneKit** module, in **Pythonista**. Unimplemented features are low level graphics and those, which are mostly unavailable at runtime.

The calling and parameter conventions are as close as possible to the documentation by [Apple in objC](https://developer.apple.com/documentation/scenekit?language=objc), so that the online version can be used with the exceptions described below.

# Installation


# Basics

The best way to get acquainted with the wrapper (or with SceneKit features) is going through the demo code set. These are numbered and sorted in increasing complexity. Most of them use no external assets, for those which do, the asset is included in the same directory.

A word of caution: just as with any code that extensively relies on the objC (objc_util and ctypes) runtime environment, it is rather easy to crash Pythonista with wrong SceneKit calls. Random crashes when exiting a script may also happen. Fear not, no harm is done. Eliminate any new code from your script until you find the offending line, and figure out what may have caused the problem. The usual culprit is wrong types for some arguments. E.g., if an attribute expects a Node instance and you supply instead a Geometry one, chances are that your code will fail with some kind of address fault.

# Conventions

Include the wrapper in your script as follows:

```
include sceneKit as scn
```

Afterwards names and identifiers in SceneKit can be used by putting scn. in front, after having omitted the SCN letters from the name found in the documentation. E. g. `scn.Node` stands for `SCNNode`.

Method names are formed by taking the documented selectors until the first `:`. E.g.:

```
hit_list = self.physics_world.rayTestWithSegmentFromPoint(p1i, p2i, scn.PhysicsTestSearchModeKey:scn.PhysicsTestSearchModeClosest})
```

calls `rayTestWithSegmentFromPoint:toPoint:options:`. `toPoint` and `options` can be used as keywords.

Some special considerations: if a property is named `type` it is sometimes represented as `...Type`, like `aPhisicsBody.bodyType` and not `aPhisicsBody.type`. Try `type` first and if no such attribute exists then `...Type`. 

Occasionally you might get an error of "None type has no attribute ID". This may happen if you want to supply `None` as a parameter to a method that usually expects a class instance. In such cases use `scn.Nil`.

Properties that have integer enumerations for their value are represented as Python `ENUM`s. E.g.: `SCNHitTestSearchModeClosest` is to be referred to as `scn.HitTestSearchMode.Closest`, though `scn.HitTestSearchMode.SCNHitTestSearchModeClosest` will also work for convenience.

String constants, however, are not represented by ENUMs so that their values can be provided or constructed as normal strings. The corresponding names and identifiers exist nonetheless. E.g., `aLight.type = scn.LightTypeAmbient` and `aLight.type = "ambient"` are both correct. It is however recommended to use the `scn.` names because more often than not the correct strings are difficult to guess.

Some classes outside of the SceneKit domain have been added to the wrapper because of their frequent use.

These are:

* CAMediaTimingFunction
* CAValueFunction
* CAAnimation
* CABasicAnimation,
* CAKeyframeAnimation
* CAAnimationGroup

* *CATransition is not implemented but SKTransition is, as scn.Transition, except transitionWithCIFilter:duration:

In the wrapper the corresponding classes are called `scn.Core...`, like `scn.CoreAnimation`, i.e., substitute CA for Core.

Several necessary constants are also available, like *kCAMediaTimingFunctionDefault, kCAMediaTimingFunctionEaseIn, kCAMediaTimingFunctionEaseInEaseOut, kCAMediaTimingFunctionEaseOut, kCAMediaTimingFunctionLinear, kCAValueFunctionRotateX, kCAValueFunctionRotateY, kCAValueFunctionRotateZ, kCAValueFunctionScale, kCAValueFunctionScaleX, kCAValueFunctionScaleY, kCAValueFunctionScaleZ, kCAValueFunctionTranslate, kCAValueFunctionTranslateX, kCAValueFunctionTranslateY, kCAValueFunctionTranslateZ, kCAAnimationCubic, kCAAnimationCubicPaced, kCAAnimationDiscrete, kCAAnimationLinear, kCAAnimationPaced, kCAAnimationRotateAuto, kCAAnimationRotateAutoReverse*.

You can omit the kCA prefix and use `scn.MediaTimingFunctionDefault`, for example.

# Getting started

A typical skeleton script would look like this:

```

from objc_util import *
import sceneKit as scn
import ui

class Demo:
  
  @classmethod
  def run(cls):
    cls().main()
    
  @on_main_thread
  def main(self):
    self.main_view = ui.View()
    w, h = ui.get_window_size()
    self.main_view.frame = (0, 0, w, h)
    self.main_view.name = 'demo'
    
    self.scene_view = scn.View((0, 0, w, h), superView=self.main_view)
    
    self.scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleWidth
    self.scene_view.allowsCameraControl = True
    
    self.scene_view.scene = scn.Scene()
    self.root_node = self.scene_view.scene.rootNode 
    
    self.scene_view.backgroundColor = (.77, .97, 1.0)
    self.scene_view.delegate = self
    
    # set up your scene here
    
    # add at least one light
    self.ambient_node = scn.Node()
    self.ambient = scn.Light()
    self.ambient.type = scn.LightTypeAmbient
    self.ambient.color = (.38, .42, .45, .1)
    self.ambient_node.light = self.ambient
    self.root_node.addChildNode(self.ambient_node)
    
    self.main_view.present(hide_title_bar=False)
    
  def update(self, view, atTime):
    # your program/game logic comes here
    pass
    
Demo.run()

```

Take note of the `superView=self.main_view` convenience argument on the line that creates the `sceneView`.

# Delegates

Several important features of SceneKit are implemented through delegates. In your script you have to designate a class instance with some of the prescribed methods to act as delegate. One class instance can serve as delegate for several things as long as the methods don't conflict. A convenient practice is to designate the view or game controller class instance as delegate (see the above skeleton code), so that you have easy access to the objects in the controller.

The various delegates expect the following bound methods and call them with the indicated arguments. Define only those methods, in which you do something; placeholders are unnecessary. 

[**SceneRendererDelegate**](https://developer.apple.com/documentation/scenekit/scnscenerendererdelegate?language=objc)

```
def update(self, aView, time):

def didApplyAnimations(self, aView, time):

def didSimulatePhysics(self, aView, time):

def didApplyConstraints(self, aView, time):

def willRenderScene(self, aView, aScene, time):

def didRenderScene(self, aView, aScene, time):
```

[**PhysicsContactDelegate**](https://developer.apple.com/documentation/scenekit/scnphysicscontactdelegate?language=objc)

```
def didBeginContact(self, aWorld, aContact):

def didUpdateContact(self, aWorld, aContact):

def didEndContact(self, aWorld, aContact):
```

The last argument is an instance of the scn.PhysicsContact Class.

[**CameraControllerDelegate**](https://developer.apple.com/documentation/scenekit/scncameracontrollerdelegate?language=objc)

```
def cameraInertiaWillStart(self, aCameraController):

def cameraInertiaDidEnd(self, aCameraController):
```

The last argument is an instance of the scn.CameraController Class.

[**CoreAnimationDelegate**](https://developer.apple.com/documentation/quartzcore/caanimationdelegate?language=objc)

```
def animationDidStart(self, anAnim):

def animationDidStop(self, anAnim, flag):
```

anAnim is an `scn.CoreAnimation` class instance, the flag  is a bool indicating whether the animation has completed by reaching the end of its duration.

[**AvoidOccluderConstraintDelegate**](https://developer.apple.com/documentation/scenekit/scnavoidoccluderconstraintdelegate?language=objc)

```
def didAvoidOccluder(self, constraint, occluder, node):

def shouldAvoidOccluder(self, constraint, occluder, node):
  return aBool
```
occluder, node are `scn.Node` instances. aBool instructs if the avoid constraint should fire for the given nodes.

[**SceneExportDelegate**](https://developer.apple.com/documentation/scenekit/scnsceneexportdelegate?language=objc)

```
def writeImage(self, ximage, xdocumentURL, xoriginalImageURL):
  return aString
```
See [this page](https://developer.apple.com/documentation/scenekit/scnsceneexportdelegate/1524221-writeimage?language=objc) for more explanation.

# Block technology

SceneKit offers additional functionality for several methods through code blocks/closures in objC. The wrapper package allows the usage of these by accepting a method (bound or unbound) or function object as the block, so long as these methods correspond to the following signatures and conventions. See the sample below and the respective block signature:

```
  self.trace.handleEvent(scn.ParticleEvent.Birth, [scn.ParticlePropertyPosition], self.traceParticleEventBlock)
    ...
  def traceParticleEventBlock(self, prop, aProperty, particleIndex):
    prop[1] = 0. #set the y coordinate of the position of the particle to 0.
```

In the specifications below `pCode` stands for your method.

### Blocks related to `scn.Node`

[childNodesPassingTest](https://developer.apple.com/documentation/scenekit/scnnode/1407982-childnodespassingtest?language=objc)

```
def pCode(node):
  return (bool1, bool2)
# OR
  return bool1
```
`bool1` denotes if the node passed your rest, the optional `bool2` should be set to `True` to stop the search process.

[enumerateChildNodesUsingBlock](https://developer.apple.com/documentation/scenekit/scnnode/1408032-enumeratechildnodesusingblock?language=objc)

```
def pCode(node):
  return bool
```
`bool` should be set to `True` to stop the search process.

[enumerateHierarchyUsingBlock](https://developer.apple.com/documentation/scenekit/scnnode/1642248-enumeratehierarchyusingblock?language=objc)

```
def pCode(node):
  return bool
```
`bool` should be set to `True` to stop the search process.

### Blocks related to modifying particles in response to particle system events

[handleEvent](https://developer.apple.com/documentation/scenekit/scnparticlesystem/1523251-handleevent?language=objc)

```
def pCode(prop, aProperty, particleIndex):
  prop[0] = newScalarForProperty
# OR
  prop[0] = prop[0] + 2.
# OR
  prop[0], prop[1], prop[2] = aNewVector3
```
`prop` is the current value of the `aProperty` property (given as a string constant, e.g., `scn.ParticlePropertyPosition`) as list. You change elements of this list, depending on the nature of the property being tinkered with.

[addModifierForProperties](https://developer.apple.com/documentation/scenekit/scnparticlesystem/1522635-addmodifierforproperties?language=objc)

```
def pCode(prop, aProperty, particleIndex, deltaTime):
```
Arguments and setting of new values as above, `deltaTime` is the elapsed time, in seconds, since the last frame of simulation. Use this block to change properties of individual particles on each frame of simulation.

### Blocks related to `scn.Action`

[runBlock](https://developer.apple.com/documentation/scenekit/scnaction/1523637-runblock?language=objc)

```
def pCode(node):
```

[customActionWithDuration](https://developer.apple.com/documentation/scenekit/scnaction/1523692-customactionwithduration?language=objc)

```
def pCode(node, elapsedTime):
```
`elapsedTime` is the amount of time that has passed since the action began executing.

[timingFunction](https://developer.apple.com/documentation/scenekit/scnaction/1524130-timingfunction?language=objc)

```
def pCode(time):
  return newTime
```
The block gets called only if meaningful, it must return a floating-point value between 0.0 and 1.0 and it must provide 1.0 at some point to let the action finish and signal completion.

### Blocks related to `scn.Animation`

[animationDidStart](https://developer.apple.com/documentation/scenekit/scnanimation/2866063-animationdidstart?language=objc)

```
def pCode(animation, receiver):
```
`receiver` is the animated object

[animationDidStop](https://developer.apple.com/documentation/scenekit/scnanimation/2866040-animationdidstop?language=objc)

```
def pCode(animation, receiver, completed):
```
Arguments as above; `completed` is `True` if the animation stopped because it is completed.

### Blocks related to `scn.SceneRenderer` (`scn.View`)

[prepareObject](https://developer.apple.com/documentation/scenekit/scnscenerenderer/1522798-prepareobject?language=objc)

```
def pCode():
  return aBool
```
The block gets called periodically and should return `False` to tell SceneKit to continue preparing the object, or `True` to cancel preparation.

[prepareObjects](https://developer.apple.com/documentation/scenekit/scnscenerenderer/1523375-prepareobjects?language=objc)

```
def pCode(success):
```
The block get called when object preparation fails or completes. `success` is `True` if all content was successfully prepared for rendering; otherwise `False`.

### Block related to `scn.Scene`

[writeToURL](https://developer.apple.com/documentation/scenekit/scnscene/1523577-writetourl?language=objc)

```
def pCode(totalProgress, xError):
  return aBool
```
`totalProgress` is a number between 0.0 and 1.0 that indicates the progress of the export operation, with 0.0 indicating that the operation has just begun and 1.0 indicating the operation has completed. `xError` is an error code or `None`. Return `True` to cancel export.

### Block related to `scn.PhysicsField`

[customFieldWithEvaluationBlock](https://developer.apple.com/documentation/scenekit/scnphysicsfield/1388140-customfieldwithevaluationblock?language=objc)

```
def pCode(position, velocity, mass, charge, time):
  return aVector3
```
Creates a field that runs the specified block to determine the force a field applies to each object in its area of effect. currently only the x component of the field can be set.

Technical note: The block should return a Structure by value, which is not supported by the currently included version of ctypes and objc_util. Now only the x component of the field force is applied.

# Using external assets

Scenekit is rather restrictive in using external assets in the runtime environment but a few ways are available. The built-in Pythonista resources (images via ui.image, fonts or sounds) are available in the usual manner. E.g.:

```
sound = scn.AudioSource('game:Pulley')
sound_player = scn.AudioPlayer.audioPlayerWithSource(sound)
node.addAudioPlayer(sound_player)
```

Genuinely external assets can be used as follows. However, file related constructor and init methods don’t work, use the versions with an `URL` argument.

[sceneWithURL](https://developer.apple.com/documentation/scenekit/scnscene/1522660-scenewithurl?language=objc)

This method works as long as the url points to a file, which is a SceneKit compressed scene (.dae or .abc) that you have generated by processing your asset file through Xcode.

Similarly, if in Xcode you convert your asset file into a SceneKit archive (.scn), it is readable.

You can also construct a scene programatically, export it through the `writeToURL` method and then use it in another script.


[sceneWithMDLAsset](https://developer.apple.com/documentation/scenekit/scnscene/1419833-scenewithmdlasset?language=objc)

[nodeWithMDLObject](https://developer.apple.com/documentation/scenekit/scnnode/1419841-nodewithmdlobject?language=objc)

[cameraWithMDLCamera](https://developer.apple.com/documentation/scenekit/scncamera/1419839-camerawithmdlcamera?language=objc)

[lightWithMDLLight](https://developer.apple.com/documentation/scenekit/scnlight/1419849-lightwithmdllight?language=objc)

[geometryWithMDLMesh](https://developer.apple.com/documentation/scenekit/scngeometry/1419845-geometrywithmdlmesh?language=objc)

[geometryElementWithMDLSubmesh](https://developer.apple.com/documentation/scenekit/scngeometryelement/1419843-geometryelementwithmdlsubmesh?language=objc)

[materialWithMDLMaterial](https://developer.apple.com/documentation/scenekit/scnmaterial/1419835-materialwithmdlmaterial?language=objc)

These work, however the MDL module is not part of this wrapper. Make sure not to supply `None` instead of a valid MDL asset for argument, you will get no error but no content either. MDL routines can easily import `.obj` models.

[Consult this page](https://developer.apple.com/documentation/modelio/mdlasset/1391813-canimportfileextension?language=objc) to see if a particular asset file could be used.

Here is a sample code:

```
from objc_util import *
import sceneKit as scn

MDLAsset, MDLMesh, MDLSubmesh = ObjCClass('MDLAsset'), ObjCClass('MDLMesh'), ObjCClass('MDLSubmesh')
...
asset = MDLAsset.alloc().initWithURL_(nsurl('_Lucy.obj'))
mesh = asset.objectAtIndex_(0)
lucy_geometry = scn.Geometry.geometryWithMDLMesh(mesh)

lucy_node_1 = scn.Node.nodeWithGeometry(lucy_geometry)

lucy_node_2 = scn.Node.nodeWithMDLObject(mesh)
```

# Convenience methods and properties unavailable in SceneKit proper

`View` instance method:

```
def addToSuperview(self, aUIView):
```

`GeometrySource` Class methods:

```
def geometrySourceWithVectors(source, semantic):

def interleavedGeometrySourceWithVectors(sourceList, semanticList):
```

`GeometrySource` read-only instance property:

```
vectors
```

# Unresolved issues

**Skinner** class - implemented but the init method always returns None. Needs futher investigation.

**light.sphericalHarmonicsCoefficients** - returns `None` also for probe light type.

**Node: SIMD type methods** - not implemented due to `objc_util` and `ctypes` limitations. Redirected to non-simd versions of properties.

**Hitresult: simdLocalCoordinates, simdLocalNormal, simdModelTransform, simdWorldCoordinates, simdWorldNormal** - not implemented, see above.

**SCNTransformConstraint** - currently cannot be implemented, block is supposed to return a structure, which is not supported by `ctypes` and `objc_util`.

**Scn.CoreAnimation defaultValueForKey method** - implemented but proper usage is unclear.

**SceneRenderer: overlaySKScene** - warning: overlay must be a genuine `SKScene` and not a `Scene` from the Pythonista scene module


# Unimplemented features

`scn.ViewOption` - Dictionary keys specifying initialization options, used when initializing a SceneKit view. (low level graphics)

`scn.Scene` - screenSpaceReflection properties (beta)

Customizing Node Rendering - `scn.Node` filters and rendererDelegate properties

`scn.Renderer` Class (don't mix it with `scn.SceneRenderer`). It is meant to add content rendered by SceneKit to an app that already renders other content by using Metal, OpenGL, or OpenGL ES directly. Out of scope.

Renderer Customization - low level graphics, out of scope

`scn.SceneRenderer` - Customizing Scene Rendering with Metal and Customizing Scene Rendering with OpenGL. Low level graphics, out of scope.

`scn.SceneRenderer` - currentViewport, temporalAntialiasingEnabled, usesReverseZ properties. (beta)

`scn.CoreKeyframeAnimation` (`CAKeyframeAnimation`) - path property

`scn.action` `runBlock:queue:` and `javaScriptActionWithScript:duration:`

`geometrySourceWithBuffer:vertexFormat:semantic:vertexCount:dataOffset:dataStride:` - Needs Metal and scene renderer delegate. low level graphics, out of scope.

`SCNSceneSource` - limited use in runtime environment; use scene with url or the MDL methods for external assets

`SCNExportJavaScriptModule` - out of scope

