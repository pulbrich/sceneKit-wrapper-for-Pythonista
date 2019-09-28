'''
A python implementation of the SceneKit Vehicle Demo presented by Apple in 2014

https://developer.apple.com/library/archive/samplecode/SceneKitVehicle/History/History.html

This script needs the Gestures module from

https://github.com/mikaelho/pythonista-gestures
'''
from objc_util import *
import sceneKit as scn
import ui
import motion
import Gestures
import math
import random

from OverlayScene import *

M_PI = math.pi
M_PI_2 = math.pi/2
M_PI_4 = math.pi/4

scn.clearCache()

class GameViewController:
  
  @classmethod
  def run(cls):
    cls().main()
    
  @on_main_thread
  def main(self):

    self.main_view = ui.View()
    w, h = ui.get_window_size()
    self.main_view.frame = (0, 0, w, h)
    self.main_view.name = 'Apple SceneKit demo'
    
    self.scnView = scn.View((0, 0, w, h), superView=self.main_view)
    self.scnView.preferredFramesPerSecond = 30
    self.scnView.rendersContinuously = True
    
    #set the background to back
    self.scnView.backgroundColor = 'black'
    
    #setup the scene
    scene = self.setupScene()
        
    #present it
    self.scnView.scene = scene
        
    #tweak physics
    self.scnView.scene.physicsWorld.speed = 4.0
        
    #initial point of view
    self.scnView.pointOfView = self.myCameraNode

    
    #plug game logic
    self.scnView.delegate = self
    
    #setup overlays
    self.overlayScene = OverlayScene(self.main_view)
    self.camera_button = False


    #setup accelerometer
    self.setupAccelerometer()
    
    self.g = Gestures.Gestures()
    self.g.add_long_press(self.main_view, self.touch_1, number_of_taps_required=None, number_of_touches_required=1, minimum_press_duration = 0.2)
    self.g.add_long_press(self.main_view, self.touch_2, number_of_taps_required=None, number_of_touches_required=2, minimum_press_duration = 0.2)
    self.g.add_long_press(self.main_view, self.touch_3, number_of_taps_required=None, number_of_touches_required=3, minimum_press_duration = 0.2)
    
    self.g.add_doubletap(self.main_view, self.touch_dt, number_of_touches_required = 2)

    self.defaultEngineForce = 300.0
    self.defaultBrakingForce = 3.0
    self.steeringClamp = 0.6
    self.cameraDamping = 0.3
    
    self.maxSpeed = 200.
    
    self.touchCount = 0
    self.doubleTap = False
    self.inCarView = False
    
    self.ticks = 0
    self.check = 0
    self.tryVar = 0
    
    self.main_view.present(hide_title_bar=True)


  def setupScene(self):
    #create a new scene
    scene = scn.Scene()
    
    #global environment
    self.setupEnvironment(scene)
        
    #add elements
    self.setupSceneElements(scene)
        
    #setup vehicle
    self.myVehicleNode = self.setupVehicle(scene)
        
    #create a main camera
    self.myCameraNode = scn.Node()
    self.myCameraNode.camera = scn.Camera()
    self.myCameraNode.camera.xFov = 75
    self.myCameraNode.camera.zFar = 500
    self.myCameraNode.position = scn.Vector3(0, 60, 50)
    self.myCameraNode.rotation  = scn.Vector4(1, 0, 0, -M_PI_4*0.75)
    scene.rootNode.addChildNode(self.myCameraNode)
        
    #add a secondary camera to the car
    frontCameraNode = scn.Node()
    frontCameraNode.position = scn.Vector3(0, 3.5, 2.5)
    frontCameraNode.rotation = scn.Vector4(0, 1, 0, M_PI)
    frontCameraNode.camera = scn.Camera()
    frontCameraNode.camera.xFov = 75
    frontCameraNode.camera.zFar = 500
        
    self.myVehicleNode.addChildNode(frontCameraNode)
    
    self.pointOfViews = [self.myCameraNode, frontCameraNode]
    
    return scene
    
  def setupEnvironment(self, scene):
    #add an ambient light
    ambientLight = scn.Node()
    ambientLight.light = scn.Light()
    ambientLight.light.type = scn.LightTypeAmbient
    ambientLight.light.color = (0.3, 0.3, 0.3, 1.0)
    scene.rootNode.addChildNode(ambientLight)
        
    #add a key light to the scene
    #keep an ivar for later manipulation
    self.mySpotLightNode = scn.Node()
    self.mySpotLightNode.light = scn.Light()
    self.mySpotLightNode.light.type = scn.LightTypeSpot        
    self.mySpotLightNode.light.castsShadow = True    
    self.mySpotLightNode.light.color = (0.8, 0.8, 0.8, 1.0)
    self.mySpotLightNode.position = scn.Vector3(0, 80, 30)
    self.mySpotLightNode.rotation = scn.Vector4(1, 0, 0, -M_PI/2.8)
    self.mySpotLightNode.light.spotInnerAngle = 0
    self.mySpotLightNode.light.spotOuterAngle = 50
    self.mySpotLightNode.light.shadowColor = 'black'
    self.mySpotLightNode.light.zFar = 40
    self.mySpotLightNode.light.zNear = 5
    self.mySpotLightNode.shadowSampleCount = 16
    scene.rootNode.addChildNode(self.mySpotLightNode)

    floor = scn.Node()
    floor.geometry = scn.Floor()
    floor.geometry.firstMaterial.diffuse.contents = "resources/wood.png"
    scale = list(scn.Matrix4Identity)
    scale[0], scale[5], scale[10] = 2., 2., 1.
    floor.geometry.firstMaterial.diffuse.contentsTransform = scale
    floor.geometry.firstMaterial.locksAmbientWithDiffuse = True
    floor.geometry.reflectionFalloffEnd = 10
        
    staticBody = scn.PhysicsBody.staticBody()
    floor.physicsBody = staticBody
    scene.rootNode.addChildNode(floor)
    
  def setupSceneElements(self, scene):
    #add walls
    wall = scn.Node(geometry=scn.Box(width=400, height=100, length=4, chamferRadius=0))
    wall.geometry.firstMaterial.diffuse.contents = "resources/wall.jpg"
    scale = list(scn.Matrix4Identity)
    scale[0], scale[5], scale[13], scale[10] = 24., 2., 1., 1.
    
    wall.geometry.firstMaterial.diffuse.contentsTransform = scale
    wall.geometry.firstMaterial.diffuse.wrapS = scn.WrapMode.Repeat
    wall.geometry.firstMaterial.diffuse.wrapT = scn.WrapMode.Mirror
    wall.geometry.firstMaterial.doubleSided = False
    wall.castsShadow = False
    wall.geometry.firstMaterial.locksAmbientWithDiffuse = False
        
    wall.position = scn.Vector3(0, 50, -92)
    wall.physicsBody = scn.PhysicsBody.staticBody()
    scene.rootNode.addChildNode(wall)

    wall = wall.clone()
    wall.position = scn.Vector3(-202, 50, 0)
    wall.rotation = scn.Vector4(0, 1, 0, M_PI_2)
    scene.rootNode.addChildNode(wall)
        
    wall = wall.clone()
    wall.position = scn.Vector3(202, 50, 0)
    wall.rotation = scn.Vector4(0, 1, 0, -M_PI_2)
    scene.rootNode.addChildNode(wall)
        
    backWall = scn.Node(geometry=scn.Plane(width=400, height=100))
    backWall.geometry.firstMaterial = wall.geometry.firstMaterial
    backWall.position = scn.Vector3(0, 50, 200)
    backWall.rotation = scn.Vector4(0, 1, 0, M_PI)
    backWall.castsShadow = False
    backWall.physicsBody = scn.PhysicsBody.staticBody()
    scene.rootNode.addChildNode(backWall)
        
    #add ceil
    ceilNode = scn.Node(geometry=scn.Plane(width=400, height=400))
    ceilNode.position = scn.Vector3(0, 100, 0)
    ceilNode.rotation = scn.Vector4(1, 0, 0, M_PI_2)
    ceilNode.geometry.firstMaterial.doubleSided = False
    ceilNode.castsShadow = False
    ceilNode.geometry.firstMaterial.locksAmbientWithDiffuse = False
    scene.rootNode.addChildNode(ceilNode)
   
    #add a train
    self.addTrainToScene(scene, pos=scn.Vector3(-5, 20, -40))
        
    #add wooden blocks
    self.addWoodenBlockToScene(scene, imageName="resources/WoodCubeA.jpg", position=scn.Vector3(-10, 15, 10))
    self.addWoodenBlockToScene(scene, imageName="resources/WoodCubeB.jpg", position=scn.Vector3(-9, 10, 10))
    self.addWoodenBlockToScene(scene, imageName="resources/WoodCubeC.jpg", position=scn.Vector3(20, 15, -11))
    self.addWoodenBlockToScene(scene, imageName="resources/WoodCubeA.jpg", position=scn.Vector3(25, 5, -20))

    #add more block
    for _ in range(4):
      self.addWoodenBlockToScene(scene, imageName="resources/WoodCubeA.jpg", position=scn.Vector3(random.randint(-30, 30), 20, random.randint(-20, 20)))
      self.addWoodenBlockToScene(scene, imageName="resources/WoodCubeB.jpg", position=scn.Vector3(random.randint(-30, 30), 20, random.randint(-20, 20)))
      self.addWoodenBlockToScene(scene, imageName="resources/WoodCubeC.jpg", position=scn.Vector3(random.randint(-30, 30), 20, random.randint(-20, 20)))
        
    #add cartoon book
    block = scn.Node()
    block.position = scn.Vector3(20, 10, -16)
    block.rotation = scn.Vector4(0, 1, 0, -M_PI_4)
    block.geometry = scn.Box(width=22, height=2., length=34, chamferRadius=0)
    frontMat = scn.Material()
    frontMat.locksAmbientWithDiffuse = True
    frontMat.diffuse.contents = "resources/book_front.jpg"
    frontMat.diffuse.mipFilter = scn.FilterMode.Linear
    backMat = scn.Material()
    backMat.locksAmbientWithDiffuse = True
    backMat.diffuse.contents = "resources/book_back.jpg"
    backMat.diffuse.mipFilter = scn.FilterMode.Linear
    edgeMat = scn.Material()
    edgeMat.locksAmbientWithDiffuse = True
    edgeMat.diffuse.contents = "resources/book_side_title.jpg"
    edgeMat.diffuse.mipFilter = scn.FilterMode.Linear
    edgeMatSide = scn.Material()
    edgeMatSide.locksAmbientWithDiffuse = True
    edgeMatSide.diffuse.contents = "resources/book_side.jpg"
    edgeMatSide.diffuse.mipFilter = scn.FilterMode.Linear
  
    block.geometry.materials = [edgeMatSide, edgeMatSide, edgeMatSide, edgeMat, frontMat, backMat]
    block.physicsBody = scn.PhysicsBody.dynamicBody()
    scene.rootNode.addChildNode(block)
        
    #add carpet
    path = ui.Path.rounded_rect(-50, -30, 100, 50, 2.5)
    rug_geometry = scn.Shape.shapeWithPath(path, extrusionDepth=0.05)
    rug = scn.Node.nodeWithGeometry(rug_geometry)
    rug.geometry.firstMaterial.locksAmbientWithDiffuse = True
    rug.geometry.firstMaterial.diffuse.contents = "resources/carpet.jpg"
    rug.position = scn.Vector3(0, 0.01, 0)
    rug.rotation = scn.Vector4(1, 0, 0, M_PI_2)
    scene.rootNode.addChildNode(rug)
        
    #add ball
    ball = scn.Node()
    ball.position = scn.Vector3(-5, 5, -18)
    ball.geometry = scn.Sphere(radius=5)
    ball.geometry.firstMaterial.locksAmbientWithDiffuse = True
    ball.geometry.firstMaterial.diffuse.contents = "resources/ball.jpg"
    scale = list(scn.Matrix4Identity)
    scale[0], scale[5], scale[10] = 2., 1., 1.
    ball.geometry.firstMaterial.diffuse.contentsTransform = scale
    ball.geometry.firstMaterial.diffuse.wrapS = scn.WrapMode.Mirror
    ball.physicsBody = scn.PhysicsBody.dynamicBody()
    ball.physicsBody.restitution = 0.9
    scene.rootNode.addChildNode(ball)

  def addWoodenBlockToScene(self, scene, imageName=None, position=None):
    #create a new node
    block = scn.Node()
        
    #place it
    block.position = position
        
    #attach a box of 5x5x5
    block.geometry = scn.Box(width=5, height=5, length=5, chamferRadius=0)
        
    #use the specified images named as the texture
    block.geometry.firstMaterial.diffuse.contents = imageName
        
    #turn on mipmapping
    block.geometry.firstMaterial.diffuse.mipFilter = scn.FilterMode.Linear
        
    #make it physically based
    block.physicsBody = scn.PhysicsBody.dynamicBody()
        
    #add to the scene
    scene.rootNode.addChildNode(block)
        
  def addTrainToScene(self, scene=None, pos=None):    
    def addTrainToSceneBlock(child):
      if child.geometry is not None and child.geometry != scn.nil:
        node = child.clone()
        node.position = scn.Vector3(node.position.x + pos.x, node.position.y + pos.y, node.position.z + pos.z)
        min, max = node.getBoundingBox()
                
        body = scn.PhysicsBody.dynamicBody()
        boxShape = scn.Box(width=(max.x - min.x), height=(max.y - min.y), length=(max.z - min.z), chamferRadius=0.0)
                
        body.physicsShape = scn.PhysicsShape(geometry=boxShape, options=None)
        
        trans = list(scn.Matrix4Identity)
        trans[13] = -min.y
        node.pivot = trans
        node.physicsBody = body
        scene.rootNode.addChildNode(node)
        return False
    
    trainScene = scn.Scene(url="resources/train_flat_PY.scn")
        
    #physicalize the train with simple boxes
    trainScene.rootNode.enumerateChildNodesUsingBlock(addTrainToSceneBlock)
        
    #add smoke
    self.smokeHandle = scene.rootNode.childNodeWithName("Smoke", recursively=True)
    self.smoke = scn.ParticleSystem()
    
    self.smoke.birthRate = 30
    self.smoke.birthLocation = scn.ParticleBirthLocation.SCNParticleBirthLocationSurface
    self.smoke.loops = True
    self.smoke.emissionDuration = 1
    self.smoke.emissionDurationVariation = 0
    self.smoke.idleDuration = 0
    self.smoke.idleDurationVariation = 0.
    self.smoke.emittingDirection = (0, 1, 0)
    self.smoke.spreadingAngle = 10
    self.smoke.particleAngleVariation = 180
    self.smoke.particleDiesOnCollision = False
    self.smoke.particleLifeSpan = 5.
    self.smoke.particleLifeSpanVariation = 0.
    self.smoke.particleVelocity = 6.
    self.smoke.particleVelocityVariation = 1
    self.smoke.particleImage = ui.Image.named('resources/tex_smoke.png')
    self.smoke.particleSize = 3.
    self.smoke.particleSizeVariation = 0.5
    self.smoke.particleIntensity = 1.
    self.smoke.particleIntensityVariation = 0.
    self.smoke.stretchFactor = 0.0
    self.smoke.particleColor = (.41, .42, .48)
    self.smoke.blendMode = scn.ParticleBlendMode.SCNParticleBlendModeScreen
    
    self.smokeHandle.addParticleSystem(self.smoke)
        
    #add physics constraints between engine and wagons
    engineCar = scene.rootNode.childNodeWithName("EngineCar", recursively=False)
    wagon1 = scene.rootNode.childNodeWithName("Wagon1", recursively=False)
    wagon2 = scene.rootNode.childNodeWithName("Wagon2", recursively=False)
    
    min, max = engineCar.getBoundingBox()        
    wmin, wmax = wagon1.getBoundingBox()
        
    #Tie EngineCar & Wagon1
    joint = scn.PhysicsBallSocketJoint(bodyA=engineCar.physicsBody, anchorA=scn.Vector3(max.x, min.y, 0), bodyB=wagon1.physicsBody, anchorB=scn.Vector3(wmin.x, wmin.y, 0))
    scene.physicsWorld.addBehavior(joint)
        
    #Wagon1 & Wagon2
    joint = scn.PhysicsBallSocketJoint(bodyA=wagon1.physicsBody, anchorA=scn.Vector3(wmax.x + 0.1, wmin.y, 0), bodyB=wagon2.physicsBody, anchorB=scn.Vector3(wmin.x - 0.1, wmin.y, 0))
    scene.physicsWorld.addBehavior(joint)

    
  def setupVehicle(self, scene):
    chassisNode = scn.Node()
    carScene = scn.Scene(url="resources/rc_car_PY.scn")
    chassisNode = carScene.rootNode.childNodeWithName("rccarBody", recursively=False)
        
    #setup the chassis
    chassisNode.position = scn.Vector3(0, 10, 30)
    chassisNode.rotation = scn.Vector4(0, 1, 0, M_PI)
        
    body = scn.PhysicsBody.dynamicBody()
    body.allowsResting = False
    body.mass = 80
    body.restitution = 0.1
    body.friction = 0.5
    body.rollingFriction = 0
        
    chassisNode.physicsBody = body
    scene.rootNode.addChildNode(chassisNode)
        
    self.pipeNode = chassisNode.childNodeWithName("pipe", recursively=False)
    self.myReactor = scn.ParticleSystem()
    
    self.myReactor.birthRate = 1000
    self.myReactor.birthLocation = scn.ParticleBirthLocation.SCNParticleBirthLocationSurface
    self.myReactor.loops = True
    self.myReactor.emissionDuration = 1
    self.myReactor.emissionDurationVariation = 0
    self.myReactor.idleDuration = 0
    self.myReactor.idleDurationVariation = 0.
    self.myReactor.emittingDirection = (0, 1, 0)
    self.myReactor.spreadingAngle = 10
    self.myReactor.particleAngleVariation = 180
    self.myReactor.particleDiesOnCollision = False
    self.myReactor.particleLifeSpan = 0.15
    self.myReactor.particleLifeSpanVariation = 0.05
    self.myReactor.particleVelocity = 40.
    self.myReactor.particleVelocityVariation = 40.
    self.myReactor.particleImage = ui.Image.named('resources/spark.png')
    self.myReactor.particleSize = 1.
    self.myReactor.particleSizeVariation = 1.
    self.myReactor.particleIntensity = 1.
    self.myReactor.particleIntensityVariation = 0.4
    self.myReactor.stretchFactor = 0.0
    self.myReactor.particleColor = (.87, .45, .0)
    self.myReactor.blendMode = scn.ParticleBlendMode.SCNParticleBlendModeAdditive
        
    self.myReactorDefaultBirthRate = self.myReactor.birthRate
    self.myReactor.birthRate = 0
    self.pipeNode.addParticleSystem(self.myReactor)
        
    #add wheels
    wheel0Node = chassisNode.childNodeWithName("wheelLocator_FL", recursively=True)
    wheel1Node = chassisNode.childNodeWithName("wheelLocator_FR", recursively=True)
    wheel2Node = chassisNode.childNodeWithName("wheelLocator_RL", recursively=True)
    wheel3Node = chassisNode.childNodeWithName("wheelLocator_RR", recursively=True)

    wheel0 = scn.PhysicsVehicleWheel(node=wheel0Node)
    wheel1 = scn.PhysicsVehicleWheel(node=wheel1Node)
    wheel2 = scn.PhysicsVehicleWheel(node=wheel2Node)
    wheel3 = scn.PhysicsVehicleWheel(node=wheel3Node)

    min, max = wheel0Node.getBoundingBox()
       
    wheelHalfWidth = 0.5 * (max.x - min.x)

    p = wheel0Node.convertPosition((0, 0, 0), toNode=chassisNode)
    p = (p.x+wheelHalfWidth, p.y, p.z)
    wheel0.connectionPosition = p
    
    p = wheel1Node.convertPosition((0, 0, 0), toNode=chassisNode)
    p = (p.x-wheelHalfWidth, p.y, p.z)
    wheel1.connectionPosition = p
        
    p = wheel2Node.convertPosition((0, 0, 0), toNode=chassisNode)
    p = (p.x+wheelHalfWidth, p.y, p.z)
    wheel2.connectionPosition = p
    
    p = wheel3Node.convertPosition((0, 0, 0), toNode=chassisNode)
    p = (p.x-wheelHalfWidth, p.y, p.z)
    wheel3.connectionPosition = p
        
    #create the physics vehicle
    vehicle = scn.PhysicsVehicle(chassisBody=chassisNode.physicsBody, wheels=[wheel0, wheel1, wheel2, wheel3])
    scene.physicsWorld.addBehavior(vehicle)
        
    self.myVehicle = vehicle
    return chassisNode
    
  def setupAccelerometer(self):
    motion.start_updates()
    
  def update(self, view, atTime):
    if self.overlayScene.close:
      self.shutDown()
    if self.doubleTap:
      self.handleDoubleTap()
      return
      
    
  def didSimulatePhysics(self, view, atTime):
      
    engineForce = 0
    brakingForce = 0
    
    accelerometer = motion.get_gravity()
    if accelerometer[0] > 0:
      self.myOrientation = accelerometer[1] * 1.3
    else:
      self.myOrientation = -accelerometer[1] * 1.3
      
    orientation = self.myOrientation
    
    #drive: 1 touch = accelerate, 2 touches = backward, 3 touches = brake
    if self.touchCount == 1:
      engineForce = self.defaultEngineForce
      self.myReactor.birthRate = self.myReactorDefaultBirthRate
    elif self.touchCount == 2:
      engineForce = -self.defaultEngineForce
      self.myReactor.birthRate = 0
    elif self.touchCount == 3:
      brakingForce = 100
      self.myReactor.birthRate = 0
    else:
      brakingForce = self.defaultBrakingForce
      self.myReactor.birthRate = 0
      
    myVehicleSteering = -orientation
    if orientation == 0:
      myVehicleSteering = myVehicleSteering * 0.9
    if myVehicleSteering < -self.steeringClamp:
      myVehicleSteering = -self.steeringClamp
    elif myVehicleSteering > self.steeringClamp:
      myVehicleSteering = self.steeringClamp
      
    #update the vehicle steering and acceleration
    self.myVehicle.setSteeringAngle(myVehicleSteering, forWheelAtIndex=0)
    self.myVehicle.setSteeringAngle(myVehicleSteering, forWheelAtIndex=1)

    self.myVehicle.applyEngineForce(engineForce, forWheelAtIndex=2)
    self.myVehicle.applyEngineForce(engineForce, forWheelAtIndex=3)

    self.myVehicle.applyBrakingForce(brakingForce, forWheelAtIndex=2)
    self.myVehicle.applyBrakingForce(brakingForce, forWheelAtIndex=3)
    
    self.ReorientCarIfNeeded()
    
    if self.overlayScene.myCameraButton.clicked:
      #play a sound
      self.myCameraNode.runAction(self.overlayScene.myCameraButton.clickAction)
      #change the point of view
      self.changePointOfView()
      return
    
    #make camera follow the car node
    car = self.myVehicleNode.presentationNode
    carPos = car.position

    targetPos = scn.Vector3(carPos.x, 30.0, carPos.z + 25.0)
    cameraPos = self.myCameraNode.position

    cameraPos = scn.Vector3(cameraPos.x * (1.0 - self.cameraDamping) + targetPos.x * self.cameraDamping,
                            cameraPos.y * (1.0 - self.cameraDamping) + targetPos.y * self.cameraDamping,
                            cameraPos.z * (1.0 - self.cameraDamping) + targetPos.z * self.cameraDamping)
                 
    self.myCameraNode.position = cameraPos
        
    if not self.inCarView:
      #move spot light in front of the camera
      frontPosition = self.scnView.pointOfView.presentationNode.convertPosition(scn.Vector3(0, 0, -30), toNode=scn.nil)
      self.mySpotLightNode.position = scn.Vector3(frontPosition.x, 80.0, frontPosition.z)
      self.mySpotLightNode.rotation = scn.Vector4(1,0,0, -M_PI/2)
    else:
      #move spot light on top of the car
      self.mySpotLightNode.position = scn.Vector3(carPos.x, 80.0, carPos.z + 30.0)
      self.mySpotLightNode.rotation = scn.Vector4(1,0,0, -M_PI/2.8)
      
    self.overlayScene.mySpeedNeedle.zRotation = -(abs(self.myVehicle.speedInKilometersPerHour) * M_PI / self.maxSpeed)


  def changePointOfView(self):
    currentPointOfView = self.scnView.pointOfView
    
    index = self.pointOfViews.index(currentPointOfView) + 1
    if index == len(self.pointOfViews): index = 0

    self.inCarView = index != 0
    
    #set it with an implicit transaction
    scn.Transaction.begin()
    scn.Transaction.setAnimationDuration(0.75)
    self.scnView.pointOfView = self.pointOfViews[index]
    scn.Transaction.commit()
    
  def touch_1(self, data):
    if data.state == Gestures.Gestures.BEGAN:
      self.touchCount = 1
    elif data.state == Gestures.Gestures.ENDED:
      self.touchCount = 0
      
  def touch_2(self, data):
    if data.state == Gestures.Gestures.BEGAN:
      self.touchCount = 2
    elif data.state == Gestures.Gestures.ENDED:
      self.touchCount = 0
    
  def touch_3(self, data):
    if data.state == Gestures.Gestures.BEGAN:
      self.touchCount = 3
    elif data.state == Gestures.Gestures.ENDED:
      self.touchCount = 0
      
  def touch_dt(self, data):
    self.doubleTap = True
    
  def handleDoubleTap(self):
    self.myCameraNode.removeAllActions()
    self.pipeNode.removeAllParticleSystems()
    self.smokeHandle.removeAllParticleSystems()
    self.scnView.scene.physicsWorld.removeAllBehaviors()
    self.scnView.scene.paused = True
    scene = self.setupScene()
            
    #present it
    self.scnView.scene = scene
    self.scnView.pointOfView = self.myCameraNode
        
    #tweak physics
    self.scnView.scene.physicsWorld.speed = 4.0
        
    self.touchCount = 0
    self.doubleTap = False
    
  def ReorientCarIfNeeded(self):
    car = self.myVehicleNode.presentationNode
    carPos = car.position
    
    self.ticks += 1
    
    t = car.worldTransform
    if t.m22 <= 0.1:
      self.check += 1
      if self.check == 3:
        self.tryVar += 1
        if self.tryVar == 3:
          self.tryVar = 0
          self.myVehicleNode.rotation = (0, 0, 0, 0)
          self.myVehicleNode.position = (carPos.x, carPos.y + 10, carPos.z)
          self.myVehicleNode.physicsBody.resetTransform()
        else:
          x = random.uniform(-5., 5.)
          z = random.uniform(-5., 5.)
          pos = (x, 0, z)
          self.myVehicleNode.physicsBody.applyForce((0, 300, 0), pos, True)
        self.check = 0
    else:
      self.check = 0
    self.ticks = 0
    
  def shutDown(self):
    motion.stop_updates()
    self.g.remove_all_gestures(self.main_view)
    self.myCameraNode.removeAllActions()
    self.pipeNode.removeAllParticleSystems()
    self.smokeHandle.removeAllParticleSystems()
    self.scnView.scene.physicsWorld.removeAllBehaviors()
    self.scnView.scene.paused = True
    
    for aView in self.main_view.subviews:
      self.main_view.remove_subview(aView)
      
    self.scnView.removeFromSuperview()
    
    self.main_view.close()
    ui.delay(self.exit, 2.0)
    
  def exit(self):
    raise SystemExit()
    
GameViewController.run()
