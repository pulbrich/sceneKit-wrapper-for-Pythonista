"""
physics vehicle demo with autonome cars
(c) Peter Ulbrich, 2019
"""

from objc_util import *
import sceneKit as scn
import ui
import math
import random
from enum import IntEnum
import weakref


DEBUG = False
MAXCARS = 3 # max 5, set it lower for weaker devices
ENGINESOUND = True # set it to False for weaker devices or if too many cars
MAXACTIVEREVERSE = 2

def distance(aNode, bNode):
  a = aNode.position
  b = bNode.position
  return dist(a, b)
  
def dist(a, b):
  return math.sqrt(sum((x-y)**2 for x,y in zip(list(a),list(b))))
  
def length(a):
  return math.sqrt(sum(x**2 for x in a))
  
def dot(v1, v2):
  return sum(x*y for x,y in zip(list(v1),list(v2)))
  
def det2(v1, v2):
  return v1[0]*v2[1] - v1[1]*v2[0]
  
class Demo:
  if DEBUG:
    w, h = ui.get_window_size()
    status_label = ui.Label()
    status_label.frame = (0,0,w,25)
    status_label.background_color = 'white'
    status_label.text = 'Running'
    def setStatus(self):
      line = 'cache: '+str(scn.cacheSize())+' '
      for aCar in self.cars:
        prg = str(aCar.current_program.name)
        if aCar.current_program == CarProgram.reverse:
          prg += '/'+str(aCar.program_table[aCar.current_program].counter)
        line += aCar.name+': '+ prg +'  '
      self.status_label.text = line
    
  @classmethod
  def run(cls):
    cls().main()
    
  @on_main_thread
  def main(self):
    self.main_view = ui.View()
    w, h = ui.get_window_size()
    self.main_view.frame = (0, 0, w, h)
    self.main_view.name = 'vehicle demo'
    
    self.close_button = ui.Button()
    self.close_button.action = self.close
    self.close_button.frame = (20, 40, 40, 40)
    self.close_button.background_image = ui.Image.named('emj:No_Entry_2')

    if DEBUG:  
      self.scene_view = scn.View((0,25,w,h-25), superView=self.main_view)
      self.scene_view.showsStatistics = True
    else:
      self.scene_view = scn.View((0, 0, w, h), superView=self.main_view)
    self.scene_view.preferredFramesPerSecond = 30
      
    self.scene_view.autoresizingMask = scn.ViewAutoresizing.FlexibleHeight | scn.ViewAutoresizing.FlexibleWidth
    self.scene_view.allowsCameraControl = False
    
    self.scene_view.scene = scn.Scene()
    self.root_node = self.scene_view.scene.rootNode 
    
    self.scene_view.backgroundColor = (.77, .97, 1.0)
    self.scene_view.delegate = self
    
    self.physics_world = self.scene_view.scene.physicsWorld
    self.physics_world.speed = 2.
    self.physics_world.contactDelegate = self
    
    if DEBUG:
      marker1 = scn.Sphere(0.1)
      marker1.firstMaterial.emission.contents = (1.0, .14, .14)
      marker1.firstMaterial.diffuse.contents = (.0, .0, .0)
      Demo.marker_node1 = scn.Node.nodeWithGeometry(marker1)
      Demo.marker_node1.name = 'marker1'
      self.root_node.addChildNode(Demo.marker_node1)
     
      marker2 = scn.Sphere(0.1)
      marker2.firstMaterial.emission.contents = (.17, .0, 1.0)
      marker2.firstMaterial.diffuse.contents = (.0, .0, .0)
      Demo.marker_node2 = scn.Node.nodeWithGeometry(marker2)
      Demo.marker_node2.name = 'marker2'
      self.root_node.addChildNode(Demo.marker_node2)
    
    floor_geometry = scn.Floor()
    floor_geometry.reflectivity = 0.05
    tile_image = ui.Image.named('plf:Ground_DirtCenter')
    tile_number = 5
    tile_factor = scn.Matrix4(tile_number, 0.0, 0.0, 0.0, 0.0, tile_number, 0.0, 0.0, 0.0, 0.0, tile_number, 0.0, 0.0, 0.0, 0.0, 1.0)
    floor_geometry.firstMaterial.diffuse.contents = tile_image
    floor_geometry.firstMaterial.diffuse.intensity = 0.8
    floor_geometry.firstMaterial.diffuse.contentsTransform = tile_factor
    floor_geometry.firstMaterial.diffuse.wrapS, floor_geometry.firstMaterial.diffuse.wrapT = scn.WrapMode.Repeat, scn.WrapMode.Repeat
    floor_geometry.firstMaterial.locksAmbientWithDiffuse = True
    self.floor_node = scn.Node.nodeWithGeometry(floor_geometry)
    self.floor_node.name = 'Floor'
    self.floor_node.physicsBody = scn.PhysicsBody.staticBody()
    self.root_node.addChildNode(self.floor_node)
    
    cars = [dict(name='red', position=(5, 0, 0), volume=1.),
            dict(name='yellow', too_far=25, body_color=(1.0, .78, .0), position=(-5, 0, -2), sound='game:Pulley', volume=0.1),
            dict(name='blue', too_far=30, body_color=(.0, .61, 1.0), position=(-12, 0, -6), sound='game:Woosh_1', volume=0.5),
            dict(name='green', too_far=18, body_color=(.0, .82, .28), position=(10, 0, -10), sound='casino:DiceThrow3', volume=0.8),
            dict(name='pink', too_far=20, body_color=(.91, .52, .62), position=(5, 0, 10), sound='casino:DieThrow3', volume=0.5)]      
    self.cars =[Car(world=self, props=cars[i]) for i in range(min(MAXCARS, len(cars)))]
    
    self.free_flags = []
    for i in range(2*len(self.cars)):
      node = scn.Node()
      self.free_flags.append(node)
      self.root_node.addChildNode(node)
    self.used_flags = {}
    
    self.crash = Sparks().particleSystem
    self.crash_sound = scn.AudioSource('game:Crashing')
    self.crash_action = scn.Action.playAudioSource(self.crash_sound, False)
    
    self.road_blocks_node = scn.Node()
    self.road_blocks = []
    
    self.road_blocks.append(RoadBlock(w=1.6, l=25, name='block 0', position=(28, 6)))
    self.road_blocks.append(RoadBlock(w=20, l=1.6, name='block 1', position=(-2, -12)))
    self.road_blocks.append(RoadBlock(w=8, l=1.6, name='block 2', position=(-10, 6), rotation=-math.pi/6))
    self.road_blocks.append(RoadBlock(w=40, l=1.6, name='block 3', position=(-40, 0), rotation=-math.pi/3))
    self.road_blocks.append(RoadBlock(w=0.8, h=3, l=0.8, name='start', position=(0, 0)))
    
    for aBlock in self.road_blocks: self.road_blocks_node.addChildNode(aBlock.block_node)    
    self.root_node.addChildNode(self.road_blocks_node)

    self.camera_node = scn.Node()
    self.camera_node.camera = scn.Camera()
    self.camera_node.camera.zFar = 150
    carPos = self.cars[0].node.position
    self.camera_node.position = scn.Vector3(carPos.x+5, 10, carPos.z+30)    
    self.root_node.addChildNode(self.camera_node)
    
    self.light_node = scn.Node()
    self.light_node.position = (50, 50, 50)
    self.light_node.lookAt(self.root_node.position)
    self.light = scn.Light()
    self.light.type = scn.LightTypeDirectional
    self.light.castsShadow = True
    self.light.shadowSampleCount = 16
    self.light.color = (.95, 1.0, .98)
    self.light_node.light = self.light
    self.root_node.addChildNode(self.light_node)
    
    self.ambient_node = scn.Node()
    self.ambient = scn.Light()
    self.ambient.type = scn.LightTypeAmbient
    self.ambient.color = (.38, .42, .45, .1)
    self.ambient_node.light = self.ambient
    self.root_node.addChildNode(self.ambient_node)
    
    self.scene_view.pointOfView = self.camera_node
    
    if DEBUG: self.main_view.add_subview(Demo.status_label)
    
    self.close = False
    self.shut_down = False
    self.main_view.add_subview(self.close_button)
    self.main_view.present(hide_title_bar=~DEBUG)

    
  def close(self, sender):
    self.close = True
    self.main_view.remove_subview(self.close_button)
    
  def shutDown(self):
    self.shut_down = True
    for aCar in self.cars:
      aCar.smoker_node.removeAllParticleSystems()
      aCar.tire_node.removeAllParticleSystems()
      if ENGINESOUND:
        aCar.sound.loops = False
        aCar.chassis_node.removeAllAudioPlayers()
    for aNode in self.used_flags.values():
      aNode.removeAllParticleSystems()
      aNode.removeAllAudioPlayers()
    self.physics_world.removeAllBehaviors()
    self.scene_view.scene.paused = True
    self.main_view.close()
    ui.delay(self.exit, 1.5)
    
  def exit(self):
    raise SystemExit()
    
  def update(self, view, atTime):
    if self.close:
      if ~self.shut_down: self.shutDown()
      return
      
    cx, cz, node_dist = 0., 0., 99999999999.
    camPos = self.camera_node.position
    for aCar in self.cars:
      aCar.current_speed = abs(aCar.vehicle.speedInKilometersPerHour)
      aCar.node = aCar.chassis_node.presentationNode
      aCar.position = aCar.node.position
      cx += aCar.position.x
      cz += aCar.position.z
      node_dist = min(node_dist, abs(aCar.position.z-camPos.z))

      if aCar.current_program == CarProgram.reverse or aCar.current_program == CarProgram.obstacle:
        pass
      else:
        obstacles = list(view.nodesInsideFrustumWithPointOfView(aCar.camera_node.presentationNode))
        try:
          obstacles.remove(self.floor_node)
        except ValueError: pass
        if len(obstacles) > 0:
          aCar.setProgram(CarProgram.obstacle)
          
        elif length(aCar.position) > random.uniform(aCar.too_far, aCar.too_far+30):
          aCar.setProgram(CarProgram.turn_back)

      aCar.move(view, atTime)
      
    self.camera_node.lookAt((cx/len(self.cars), camPos.y, cz/len(self.cars)))
    if sum(1 for aCar in self.cars if view.isNodeInsideFrustum(aCar.node, self.camera_node)) < len(self.cars):
      self.camera_node.position = (camPos.x, camPos.y, camPos.z+0.1)
    elif node_dist < 15:
      self.camera_node.position = (camPos.x, camPos.y, camPos.z+0.05)
    elif node_dist > 35:
      self.camera_node.position = (camPos.x, camPos.y, camPos.z-0.03)
            
  def didBeginContact(self, aWorld, aContact):
    key = frozenset([aContact.nodeA, aContact.nodeB])
    if self.free_flags and key not in self.used_flags:
      flag_node = self.free_flags.pop()
      self.used_flags[key] = flag_node
      contactPoint = aContact.contactPoint
      flag_node.position = (contactPoint.x, contactPoint.y, contactPoint.z)
      flag_node.addParticleSystem(self.crash)
      flag_node.runAction(self.crash_action)
      
  def didUpdateContact(self, aWorld, aContact):
    key = frozenset([aContact.nodeA, aContact.nodeB])
    if key in self.used_flags:
      flag_node = self.used_flags[key]
      contactPoint = aContact.contactPoint
      flag_node.position = (contactPoint.x, contactPoint.y, contactPoint.z)
          
  def didEndContact(self, aWorld, aContact):
    key = frozenset([aContact.nodeA, aContact.nodeB])
    if key in self.used_flags:
      flag_node = self.used_flags.pop(key)
      flag_node.removeAllParticleSystems()
      self.free_flags.append(flag_node)
    
class CarProgram(IntEnum):
  idle = 0
  turn_back = 1
  obstacle = 2
  reverse = 3
  
class Idle:
  def __init__(self, car):
    self.desired_speed_kmh = random.gauss(40, 5)
    self.steering = Steering([-Steering.max_steering for i in range(int(Steering.steps/5))], [Steering.max_steering for i in range(int(Steering.steps/5))])
    self.car = weakref.ref(car)()
    
  def move(self, view, atTime):
    angle = self.steering.nextSteeringAngle(bounce=True)
    desired_speed_kmh = 0.5*self.desired_speed_kmh * (1+(Steering.max_steering-abs(angle))/Steering.max_steering)
    self.car.control(angle, desired_speed_kmh)
    
  def activate(self, current_angle):
    self.steering.setToAngle(current_angle, random.choice([-1, 1])*random.randint(1, 3))
    
class Turn_back: 
  def __init__(self, car):
    self.desired_speed_kmh = 45
    self.steering = Steering()
    self.car = weakref.ref(car)()
    
  def move(self, view, atTime):
    if length(self.car.position) > self.release * self.car.too_far:
      angle = self.steering.nextSteeringAngle(bounce=False)
      desired_speed_kmh = 0.5*self.desired_speed_kmh * (1+(Steering.max_steering-abs(angle))/Steering.max_steering)
      self.car.control(angle, desired_speed_kmh)
    else:
      self.steering.steering_dir *= -1
      self.car.popProgram()
      
  def activate(self, current_angle):
    self.release = random.uniform(0.6, 2.0)
    self.home = (random.uniform(-60, 40), random.uniform(-30, 50))
    v, p = self.car.physicsBody.velocity, self.car.position
    vel = (v.x, v.z)
    pos = (p.x-self.home[0], p.z-self.home[1])
    angle_math = math.atan2(det2(pos, vel), dot(pos, vel))
    self.steering.steering_dir = 5 if angle_math < self.steering.currentSteeringAngle else -5
    self.steering.setToAngle(current_angle, self.steering.steering_dir)
    
class Obstacle:
  def __init__(self, car):
    self.desired_speed_kmh = 15
    self.steering = Steering()
    self.car = weakref.ref(car)()

  def move(self, view, atTime):
    min_dist, dir, carFlag = self.car.scan() 
    if (min_dist < 4.0 and ~carFlag) or (min_dist < 8.0 and carFlag):
      self.car.setProgram(CarProgram.reverse)
    elif min_dist > 15:
      self.car.popProgram()
    elif min_dist < 8:
      self.steering.steering_dir = -9*dir
    else:
      self.steering.steering_dir *= -1     
    angle = self.steering.nextSteeringAngle(bounce=False)  
    self.car.control(angle, self.desired_speed_kmh)
    
  def activate(self, current_angle):
    self.steering.setToAngle(current_angle, 1)
    
class Reverse():
  activeSlot = MAXACTIVEREVERSE
  def __init__(self, car):
    self.desired_speed_kmh = 10.0
    self.steering = Steering()
    self.car = weakref.ref(car)()
    self.counter = 0
    
  def move(self, view, atTime):
    if DEBUG: self.car.world.setStatus()
    if self.counter == 0: #init
      self.counter = 1
      self.car.stop(self.steering.nextSteeringAngle(bounce=False))
    elif self.counter == 1: #stop
      if self.car.current_speed < 0.2 and Reverse.activeSlot > 0:
        self.steering.steering_dir *= -1
        Reverse.activeSlot -= 1
        self.counter = 2
      else:
        self.car.stop(self.steering.nextSteeringAngle(bounce=False))      
    elif self.counter == 2: #reverse
      min_front_dst, dir, carFrontFlag = self.car.scan() 
      min_rear_dst, carRearFlag = self.car.back_scan()
      if min_rear_dst < 2.0 or (min_front_dst > 8 and dist(self.car.position, self.entry_position)) > 2:
        self.steering.steering_dir *= -1
        self.counter = 3
      else:
        angle = self.steering.nextSteeringAngle(bounce=False)
        self.car.control(angle, 0.5*self.desired_speed_kmh, reverse=True)
    elif self.counter == 3: #stop
      if self.car.current_speed < 0.2:
        self.counter = 4
      else:
        self.car.stop(self.steering.nextSteeringAngle(bounce=False))
    elif self.counter == 4: #forward
      min_front_dst, dir, carFrontFlag = self.car.scan()
      if min_front_dst > 20 and dist(self.car.position, self.entry_position) > 5:
          Reverse.activeSlot += 1
          self.car.popProgram()         
      elif min_front_dst < 3:
        self.counter = 1
        Reverse.activeSlot += 1
      else:
        self.car.control(self.steering.nextSteeringAngle(bounce=False), self.desired_speed_kmh)
      
  def activate(self, current_angle):
    self.steering.steering_dir = int(math.copysign(10, current_angle))
    self.entry_position = self.car.position
    self.counter = 0
    self.steering.setToAngle(current_angle, self.steering.steering_dir)
     
class Steering:
  max_steering = math.pi/9
  steps = 7*30
  
  def __init__(self, lead=[], tail=[]):
    self.steering_angles = lead + [-Steering.max_steering+i*Steering.max_steering/Steering.steps for i in range(2*Steering.steps+1)] + tail
    self.steering_lead = len(lead)
    self.steering_neutral = self.steering_lead + Steering.steps
    self.steering_current = self.steering_neutral
    self.steering_dir = 1
    
  def nextSteeringAngle(self, bounce=True):
    next = self.steering_current + self.steering_dir
    if next > len(self.steering_angles)-1:
      if bounce: self.steering_dir = -1
      return self.steering_angles[-1]
    elif next < 0:
      if bounce: self.steering_dir = 1
      return self.steering_angles[0]
    else:
      self.steering_current = next
      return self.steering_angles[next]
      
  def setToAngle(self, angle, direction):
    for i in range(self.steering_lead, len(self.steering_angles)):
      if self.steering_angles[i] > angle:
        break
    self.steering_current = i
    self.steering_dir = direction
         
  @property
  def currentSteeringAngle(self):
    return self.steering_angles[self.steering_current]
    
class Car:
  programs=[Idle, Turn_back, Obstacle, Reverse]
  def __init__(self, world=None, props={}):
    self.world = world    
    self.physics_world = world.physics_world
    self.buildCar(body_color=props.pop('body_color', (.6, .0, .0)), sound_file=props.pop('sound', 'casino:DiceThrow2'), sound_volume=props.pop('volume', 1.0))
    self.chassis_node.position = props.pop('position', (0,0,0))
    self.name = props.pop('name', 'car')
    self.chassis_node.name = self.name
    self.program_table =[aProg(self) for aProg in Car.programs]
    self.current_program = CarProgram.idle
    self.program_stack = [self.current_program]
    self.brake_light = False
    self.too_far = props.pop('too_far', 30)
    self.current_speed = 0
    self.node = self.chassis_node
    self.position = self.chassis_node.position
    
     
  def move(self, view, atTime):
    self.program_table[self.current_program].move(view, atTime)
    
  def scan(self, rays=15):
    dret, dir, car = 999999999999., -1, False
    hit_list = []

    p1L = self.node.convertPosition(self.radar_p1L)
    pSL = self.node.convertPosition(self.radar_pSL)
    p1R = self.node.convertPosition(self.radar_p1R)
    pSR = self.node.convertPosition(self.radar_pSR)
    
    p1C = ((p1L.x+p1R.x)/2, (p1L.y+p1R.y)/2, (p1L.z+p1R.z)/2)
    
    for i in range(rays):
      p1i = self.node.convertPosition((self.radar_p1L.x + (self.radar_p1R.x-self.radar_p1L.x)*i/rays, self.radar_p1L.y, self.radar_p1L.z))
      p2i = self.node.convertPosition(((self.radar_p2L.x + (self.radar_p2R.x-self.radar_p2L.x)*i/rays), self.radar_p2L.y, self.radar_p2L.z if i%2 == 0 else 2*self.radar_p2L.z))
      hit_list.append(self.physics_world.rayTestWithSegmentFromPoint(p1i, p2i,{scn.PhysicsTestSearchModeKey:scn.PhysicsTestSearchModeClosest}))
      
    hit_list.append(self.physics_world.rayTestWithSegmentFromPoint(p1L, pSL,{scn.PhysicsTestSearchModeKey:scn.PhysicsTestSearchModeClosest}))
    
    hit_list.append(self.physics_world.rayTestWithSegmentFromPoint(p1R, pSR,{scn.PhysicsTestSearchModeKey:scn.PhysicsTestSearchModeClosest}))
    
    for i in range(len(hit_list)):
      if len(hit_list[i]) == 0: continue
      d = dist(hit_list[i][0].worldCoordinates, p1C)
      if d < dret:
        dret = d
        dir = -1 if i < (rays+2)/2 else 1
        car = (hit_list[i][0].node.categoryBitMask & 1 << 1) != 0
    return (dret, dir, car)
    
  def back_scan(self, rays=7):
    dret, car = 999999999999., False
    hit_list = []

    p1L = self.node.convertPosition((self.radar_p1L.x, self.radar_p1L.y, -self.radar_p1L.z))
    pSL = self.node.convertPosition((self.radar_pSL.x, self.radar_pSL.y, -self.radar_pSL.x))
    p1R = self.node.convertPosition((self.radar_p1R.x, self.radar_p1R.y, -self.radar_p1R.z))
    pSR = self.node.convertPosition((self.radar_pSR.x, self.radar_pSR.y, -self.radar_pSR.z))
    
    p1C = ((p1L.x+p1R.x)/2, (p1L.y+p1R.y)/2, (p1L.z+p1R.z)/2)
    
    for i in range(rays):
      p1i = self.node.convertPosition((self.radar_p1L.x + (self.radar_p1R.x-self.radar_p1L.x)*i/rays, self.radar_p1L.y, -self.radar_p1L.z))
      p2i = self.node.convertPosition(((self.radar_p2L.x + (self.radar_p2R.x-self.radar_p2L.x)*i/rays), self.radar_p2L.y, -self.radar_p2L.z if i%2 == 0 else -2*self.radar_p2L.z))
      hit_list += self.physics_world.rayTestWithSegmentFromPoint(p1i, p2i,{scn.PhysicsTestSearchModeKey:scn.PhysicsTestSearchModeClosest})
      
    for aHit in hit_list:
      d = dist(aHit.worldCoordinates, p1C)
      if d < dret: 
        dret = d
        car = (aHit.node.categoryBitMask & 1 << 1) != 0
    return (dret, car)
      
  def control(self, angle=0, desired_speed_kmh=0, reverse=False):
    multiplier = -1.2 if reverse else 1
    self.vehicle.setSteeringAngle(angle, 0)
    self.vehicle.setSteeringAngle(angle, 1)
    
    self.camera_controller_node.rotation = (0, 1, 0, -angle/2)
    
    if  self.current_speed < desired_speed_kmh:
      self.vehicle.applyEngineForce(multiplier*950, 0)
      self.vehicle.applyEngineForce(multiplier*950, 1)
      self.vehicle.applyBrakingForce(0, 2)
      self.vehicle.applyBrakingForce(0, 3)
      self.brakeLights(on=False)
      self.smoke.birthRate = 700+(desired_speed_kmh - self.current_speed)**2.5
    elif self.current_speed > 1.2*desired_speed_kmh:
      self.vehicle.applyEngineForce(0, 0)
      self.vehicle.applyEngineForce(0, 1)
      self.vehicle.applyBrakingForce(multiplier*20, 2)
      self.vehicle.applyBrakingForce(multiplier*20, 3)
      self.brakeLights(on=True)
      self.smoke.birthRate = 0.
    else:
      self.vehicle.applyEngineForce(0, 0)
      self.vehicle.applyEngineForce(0, 1)
      self.vehicle.applyBrakingForce(0, 2)
      self.vehicle.applyBrakingForce(0, 3)
      self.brakeLights(on=False)
      self.smoke.birthRate = 0.
     
  def stop(self, angle=0):
    factor = 30 #60
    self.vehicle.setSteeringAngle(angle, 0)
    self.vehicle.setSteeringAngle(angle, 1)
    self.vehicle.applyEngineForce(0, 0)
    self.vehicle.applyEngineForce(0, 1)
    self.vehicle.applyBrakingForce(factor, 2)
    self.vehicle.applyBrakingForce(factor, 3)
    self.brakeLights(on=True)
    self.smoke.birthRate = 0.
    
    self.camera_controller_node.rotation = (0, 1, 0, -angle/2)

  def setProgram(self, car_program, *args, **kwargs):
    if self.current_program != car_program:
      current_angle = self.program_table[self.current_program].steering.currentSteeringAngle
      self.program_stack.append(self.current_program)
      self.current_program = car_program
      self.program_table[self.current_program].activate(current_angle)
      if DEBUG: self.world.setStatus()
      
  def popProgram(self, *args, **kwargs):
    current_angle = self.program_table[self.current_program].steering.currentSteeringAngle
    self.current_program = self.program_stack.pop()
    self.program_table[self.current_program].activate(current_angle)
    if DEBUG: self.world.setStatus()
    
  def brakeLights(self, on=False):
    if ~self.brake_light and on:
      self.lampGlasBack.firstMaterial.emission.contents = self.lampBack_colors[1]
      self.brake_light = True
    elif self.brake_light and ~on:
      self.lampGlasBack.firstMaterial.emission.contents = self.lampBack_colors[0]
      self.brake_light = False
       
  def buildCar(self, body_color=None, sound_file=None, sound_volume=1.0):
    self.chassis_node = scn.Node()
    self.chassis_node.categoryBitMask = 1 << 1
    
    self.camera_controller_node = scn.Node()

    self.camera_node = scn.Node()
    self.camera_node.position = (0, 1.6, 2.05)
    self.camera_node.lookAt((0, 0.9, 10))
    self.camera = scn.Camera()    
    self.camera.zNear = 0.25
    self.camera.zFar = 10
    self.camera.fieldOfView = 35
    self.camera_node.camera = self.camera
    
    self.camera_controller_node.addChildNode(self.camera_node)
    self.chassis_node.addChildNode(self.camera_controller_node)

    self.radar_p1L = scn.Vector3(1.2, 1.3, 2.05)
    self.radar_p2L = scn.Vector3(4.5, 0.8, 20)
    self.radar_pSL = scn.Vector3(10., 0.8, 2.4)
    self.radar_p1R = scn.Vector3(-1.2, 1.3, 2.05)
    self.radar_p2R = scn.Vector3(-4.5, 0.8, 20)
    self.radar_pSR = scn.Vector3(-10., 0.8, 2.4)
    
    self.body_material = scn.Material()
    self.body_material.diffuse.contents = body_color
    self.body_material.specular.contents = (.88, .88, .88)
    
    self.body = scn.Box(2, 1, 4, 0.2)
    self.body.firstMaterial = self.body_material

    self.body_node = scn.Node.nodeWithGeometry(self.body)
    self.body_node.position = (0, 0.75, 0)
    self.chassis_node.addChildNode(self.body_node)
    
    self.physicsBody = scn.PhysicsBody.dynamicBody()
    self.physicsBody.allowsResting = False
    self.physicsBody.mass = 1200
    self.physicsBody.restitution = 0.1
    self.physicsBody.damping = 0.3
    self.chassis_node.physicsBody = self.physicsBody
    
    self.top = scn.Box(1.6, 0.6, 1.8, 0.1)
    self.top.firstMaterial = self.body_material
    self.top_node = scn.Node.nodeWithGeometry(self.top)
    self.top_node.position = (0, 0.5+0.2, 0)
    self.body_node.addChildNode(self.top_node)
    
    self.door1 = scn.Box(2.02, 1-0.2, 1.8/2.2, 0.08)
    self.door1.firstMaterial = self.body_material
    self.door1_node = scn.Node.nodeWithGeometry(self.door1)
    self.door1_node.position = (0, 0.1, 1.8/4)
    self.body_node.addChildNode(self.door1_node)
    
    self.door2_node = scn.Node.nodeWithGeometry(self.door1)
    self.door2_node.position = (0, 0.1, -1.8/4+0.1)
    self.body_node.addChildNode(self.door2_node)
    
    self.window_material = scn.Material()
    self.window_material.diffuse.contents = (.64, .71, .75, 0.6)
    self.window_material.specular.contents = (.88, .88, .88, 0.8)
    
    self.sideW1 = scn.Box(1.61, 0.6-0.1, 1.8/2.2, 0.08)
    self.sideW1.firstMaterial = self.window_material
    self.sideW1_node = scn.Node.nodeWithGeometry(self.sideW1)
    self.sideW1_node.position = (0, 0.5+0.2, 1.8/4)
    self.body_node.addChildNode(self.sideW1_node)
    
    self.sideW2_node = scn.Node.nodeWithGeometry(self.sideW1)
    self.sideW2_node.position = (0, 0.5+0.2, -1.8/4+0.1)
    self.body_node.addChildNode(self.sideW2_node)
    
    self.window_materials = [scn.Material() for i in range(6)]
    self.window_materials[0] = self.window_material
    self.window_materials[2] = self.window_material
    for i in [1, 3, 4, 5]:
      self.window_materials[i] = self.body_material
    
    alpha = math.pi/5
    self.frontW = scn.Box(1.4, 0.6/math.cos(alpha), 0.1, 0.06)
    self.frontW.materials = self.window_materials
    self.frontW_node = scn.Node.nodeWithGeometry(self.frontW)
    self.frontW_node.position = (0, 0.5+0.2-0.05, 1.8/2+math.tan(alpha)*0.6/2-0.1)
    self.frontW_node.rotation = (1, 0, 0, -alpha)
    self.body_node.addChildNode(self.frontW_node)
    
    alpha = math.pi/5
    self.frontW2 = scn.Box(1.3, 0.6/math.cos(alpha), 0.3, 0.0)
    self.frontW2.firstMaterial = self.window_material
    self.frontW2_node = scn.Node.nodeWithGeometry(self.frontW2)
    self.frontW2_node.position = (0, 0.5+0.2-0.05-0.2, 1.8/2+math.tan(alpha)*0.6/2-0.08)
    self.frontW2_node.rotation = (1, 0, 0, -alpha)
    self.body_node.addChildNode(self.frontW2_node)
    
    alpha = math.pi/3.2
    self.rearW = scn.Box(1.4, 0.6/math.cos(alpha), 0.2, 0.2)
    self.rearW.materials = self.window_materials
    self.rearW_node = scn.Node.nodeWithGeometry(self.rearW)
    self.rearW_node.position = (0, 0.5+0.2-0.0417, -1.8/2-math.tan(alpha)*0.6/2+0.15)
    self.rearW_node.rotation = (1, 0, 0, alpha)
    self.body_node.addChildNode(self.rearW_node)
    
    alpha = math.pi/3.2
    self.rearW2 = scn.Box(1.3, 0.6/math.cos(alpha), 0.3, 0.05)
    self.rearW2.firstMaterial = self.window_material
    self.rearW2_node = scn.Node.nodeWithGeometry(self.rearW2)
    self.rearW2_node.position = (0, 0.5+0.2-0.05-0.2, -1.8/2-math.tan(alpha)*0.6/2+0.1)
    self.rearW2_node.rotation = (1, 0, 0, alpha)
    self.body_node.addChildNode(self.rearW2_node)
    
    self.nose = scn.Pyramid(2-0.4, 0.15, 1-0.2)
    self.nose.firstMaterial = self.body_material
    self.nose_node = scn.Node.nodeWithGeometry(self.nose)
    self.nose_node.position = (0, 0.75, 2-0.03)
    self.nose_node.rotation = (1, 0, 0, math.pi/2)
    self.chassis_node.addChildNode(self.nose_node)
    
    self.lampBack_colors = [(.6, .0, .0), (1.0, .0, .0)]
    
    self.front_spot = scn.Light()
    self.front_spot.type = scn.LightTypeSpot
    self.front_spot.castsShadow = False
    self.front_spot.color = (1.0, 1.0, .95)
    self.front_spot.spotInnerAngle = 20
    self.front_spot.spotOuterAngle = 25
    self.front_spot.attenuationEndDistance = 15
    
    self.exhaust = scn.Tube(0.05, 0.07, 0.08)
    self.exhaust.firstMaterial.metalness.contents = (.5, .5, .5)
    self.exhaust_node = scn.Node.nodeWithGeometry(self.exhaust)
    self.exhaust_node.position = (0.5, -0.42, -2.04)
    self.exhaust_node.rotation = (1, 0, 0, math.pi/2)
    self.body_node.addChildNode(self.exhaust_node)
    
    self.smoke = scn.ParticleSystem()
    self.smoke.emitterShape = scn.Sphere(0.01)
    self.smoke.birthLocation = scn.ParticleBirthLocation.SCNParticleBirthLocationSurface
    self.smoke.birthRate =6000
    self.smoke.loops = True
    self.smoke.emissionDuration = 0.08
    self.smoke.idleDuration = 0.4
    self.smoke.idleDurationVariation = 0.2
    self.smoke.particleLifeSpan = 0.3
    self.smoke.particleLifeSpanVariation = 1.2
    self.smoke.particleColor = (1., 1., 1., 1.)
    self.smoke.particleColorVariation = (.6, .0, .6, 0.)
    self.smoke.blendMode = scn.ParticleBlendMode.Multiply
    self.smoke.birthDirection = scn.ParticleBirthDirection.Random
    self.smoke.particleVelocity = 2.
    self.smoke.particleVelocityVariation = 3.5
    self.smoke.acceleration = (0., 15, 0.)
    self.sizeAnim = scn.CoreBasicAnimation()
    self.sizeAnim.fromValue = 0.1
    self.sizeAnim.toValue = 0.0
    self.size_con = scn.ParticlePropertyController.controllerWithAnimation(self.sizeAnim)    
    self.smoke.propertyControllers = {scn.SCNParticlePropertySize:self.size_con}

    self.smoker_node = scn.Node()
    self.smoker_node.position = (0., -0.15, 0.)
    self.smoker_node.addParticleSystem(self.smoke)
    self.exhaust_node.addChildNode(self.smoker_node)
    
    self.lamp = scn.Tube(0.12, 0.15, 4.07)
    self.lamp.firstMaterial.metalness.contents = (.93, .93, .93)
    self.lampGlasFront = scn.Sphere(0.13)
    self.lampGlasFront.firstMaterial.emission.contents = (.92, .93, .66)
    self.lampGlasBack = scn.Sphere(0.13)
    self.lampGlasBack.firstMaterial.diffuse.contents = 'black'
    self.lampGlasBack.firstMaterial.emission.contents = self.lampBack_colors[0]
    
    self.lamp_nodeR = scn.Node.nodeWithGeometry(self.lamp)
    self.lamp_nodeR.position = (-0.6, 0.75, 0.015)
    self.lamp_nodeR.rotation = (1, 0, 0, math.pi/2)
    self.chassis_node.addChildNode(self.lamp_nodeR)
    self.lamp_nodeL = scn.Node.nodeWithGeometry(self.lamp)
    self.lamp_nodeL.position = (0.6, 0.75, 0.015)
    self.lamp_nodeL.rotation = (1, 0, 0, math.pi/2)
    self.chassis_node.addChildNode(self.lamp_nodeL)
    
    self.lampGlasFront_nodeR = scn.Node.nodeWithGeometry(self.lampGlasFront)
    self.lampGlasFront_nodeR.position = (0, 1.95, 0)
    self.lampGlasFront_nodeR.lookAt((0, 45, 10))
    self.lampGlasFront_nodeR.light = self.front_spot
    self.lamp_nodeR.addChildNode(self.lampGlasFront_nodeR)    
    self.lampGlasBack_nodeR = scn.Node.nodeWithGeometry(self.lampGlasBack)
    self.lampGlasBack_nodeR.position = (0, -1.95, 0)
    self.lamp_nodeR.addChildNode(self.lampGlasBack_nodeR)
    
    self.lampGlasFront_nodeL = scn.Node.nodeWithGeometry(self.lampGlasFront)
    self.lampGlasFront_nodeL.position = (0, 1.95, 0)
    self.lampGlasFront_nodeL.lookAt((0, 45, 10))
    self.lampGlasFront_nodeL.light = self.front_spot
    self.lamp_nodeL.addChildNode(self.lampGlasFront_nodeL)    
    self.lampGlasBack_nodeL = scn.Node.nodeWithGeometry(self.lampGlasBack)
    self.lampGlasBack_nodeL.position = (0, -1.95, 0)
    self.lamp_nodeL.addChildNode(self.lampGlasBack_nodeL)
    
    self.wheel_nodes = [scn.Node()]
    self.tire = scn.Tube(0.12, 0.35, 0.25)
    self.tire.firstMaterial.diffuse.contents = 'black'
    self.wheel_nodes[0].position = (0.94, 0.4, 2-0.6)
    self.tire_node = scn.Node.nodeWithGeometry(self.tire)
    self.tire_node.rotation = (0, 0, 1, math.pi/2)
    self.wheel_nodes[0].addChildNode(self.tire_node)
    
    self.trace = scn.ParticleSystem()
    self.trace.birthRate = 750
    self.trace.loops = True
    self.trace.emissionDuration = 0.1
    self.trace.particleLifeSpan = 4.6
    self.trace.particleLifeSpanVariation = 5
    self.trace.particleSize = 0.02
    self.trace.particleColor = (.1, .1, .1, 1.)
    self.trace.particleColorVariation = (0.1, 0.1, 0.1, 0.1)
    self.trace.blendMode = scn.ParticleBlendMode.Replace
    self.trace.emitterShape = scn.Cylinder(0.02, 0.26)
    self.trace.birthLocation = scn.ParticleBirthLocation.SCNParticleBirthLocationVolume
    self.trace.handle(scn.ParticleEvent.Birth, [scn.ParticlePropertyPosition], self.traceParticleEventBlock)

    self.tire_node.addParticleSystem(self.trace)

    self.rim = scn.Cylinder(0.14, 0.1)
    self.rim.firstMaterial.diffuse.contents = 'gray' 
    self.rim.firstMaterial.specular.contents = (.88, .88, .88)
    self.rim_node = scn.Node.nodeWithGeometry(self.rim)
    self.rim_node.name = 'rim'
    self.rim_node.position = (0, 0.06, 0)
    self.tire_node.addChildNode(self.rim_node)
    self.rim_deco = scn.Text('Y', 0.05)
    self.rim_deco.font = ('Arial Rounded MT Bold', 0.3)
    self.rim_deco.firstMaterial.diffuse.contents = 'black' 
    self.rim_deco.firstMaterial.specular.contents = (.88, .88, .88)
    self.rim_deco_node = scn.Node.nodeWithGeometry(self.rim_deco)
    self.rim_deco_node.name = 'deco'
    self.rim_deco_node.position = (-0.1, 0.03, -1.12)
    self.rim_deco_node.rotation = (1, 0, 0, math.pi/2)
    self.rim_node.addChildNode(self.rim_deco_node)
    
    self.wheel_nodes.append(self.wheel_nodes[0].clone())
    self.wheel_nodes[1].position = (-0.94, 0.4, 2-0.6)
    self.wheel_nodes[1].childNodeWithName('rim', True).position = (0, -0.06, 0)
    self.wheel_nodes[1].childNodeWithName('deco', True).position = (-0.1, -0.03, -1.12)
    self.wheel_nodes[1].childNodeWithName('rim', True).rotation = (0, 1, 0, -math.pi/7)
    
    self.wheel_nodes.append(self.wheel_nodes[0].clone())
    self.wheel_nodes[2].position = (0.94, 0.4, -2+0.7)
    self.wheel_nodes[2].childNodeWithName('rim', True).rotation = (0, 1, 0, math.pi/7)
    
    self.wheel_nodes.append(self.wheel_nodes[0].clone())
    self.wheel_nodes[3].position = (-0.94, 0.4, -2+0.7)
    self.wheel_nodes[3].childNodeWithName('rim', True).position = (0, -0.06, 0)
    self.wheel_nodes[3].childNodeWithName('deco', True).position = (-0.1, -0.03, -1.12)
    self.wheel_nodes[3].childNodeWithName('rim', True).rotation = (0, 1, 0, math.pi/3)
    
    for aNode in self.wheel_nodes: self.chassis_node.addChildNode(aNode)
    
    self.wheels = [scn.PhysicsVehicleWheel(node=aNode) for aNode in self.wheel_nodes]    
    for i in [0, 1]: self.wheels[i].suspensionRestLength = 1.3     
    for i in [2, 3]: self.wheels[i].suspensionRestLength = 1.4
    for aWheel in self.wheels: aWheel.maximumSuspensionTravel = 150
    
    self.chassis_node.physicsBody.contactTestBitMask = scn.PhysicsCollisionCategory.Default.value
    self.chassis_node.physicsBody.continuousCollisionDetectionThreshold = 2.
    self.vehicle = scn.PhysicsVehicle(chassisBody=self.chassis_node.physicsBody, wheels=self.wheels)
    self.physics_world.addBehavior(self.vehicle)
    self.world.root_node.addChildNode(self.chassis_node)

    if ENGINESOUND:    
      self.sound = scn.AudioSource(sound_file)
      self.sound.load()
      self.sound.loops = True
      self.sound.volume = sound_volume
      self.sound_player = scn.AudioPlayer.audioPlayerWithSource(self.sound)
      self.chassis_node.addAudioPlayer(self.sound_player)
    
    
  def traceParticleEventBlock(self, propValues, prop, particleIndex):
    propValues[1] = 0.
    
class RoadBlock:
  block_material = scn.Material()
  block_material.diffuse.contents = (.91, .91, .91)
  block_material.specular.contents = (.88, .88, .88)
  
  def __init__(self, w=1., h=1.8, l=2., name='block', position=(0., 0.), rotation=0.):
    self.block = scn.Box(w, h, l, 0.1)
    self.block.firstMaterial = RoadBlock.block_material
    self.block_node = scn.Node.nodeWithGeometry(self.block)
    self.block_node.name = name
    self.block_node.position = position if len(position) == 3 else (position[0], h/2-0.2, position[1])
    self.block_node.rotation = (0, 1, 0, rotation)
    self.block_node.physicsBody = scn.PhysicsBody.staticBody()
    self.block_node.physicsBody.contactTestBitMask = scn.PhysicsCollisionCategory.Default.value

class Sparks:
  def __init__(self):
    self.flag = scn.Sphere(0.05)
    self.particleSystem = scn.ParticleSystem()
    self.particleSystem.loops = True
    self.particleSystem.birthRate = 550
    self.particleSystem.emissionDuration = 2
    self.particleSystem.particleLifeSpan = 0.18
    self.particleSystem.particleLifeSpanVariation = 0.29
    self.particleSystem.particleVelocity = 8
    self.particleSystem.particleVelocityVariation = 15
    self.particleSystem.particleSize = 0.04
    self.particleSystem.particleSizeVariation = 0.03
    self.particleSystem.stretchFactor = 0.02
    self.particleSystemColorAnim = scn.CoreKeyframeAnimation()
    self.particleSystemColorAnim.values = [(.99, 1.0, .71, 0.8), (1.0, .52, .0, 0.8), (1., .0, .1, 1.), (.78, .0, .0, 0.3)]
    self.particleSystemColorAnim.keyTimes = (0., 0.1, 0.8, 1.)
    self.particleSystemProp_con = scn.ParticlePropertyController.controllerWithAnimation(self.particleSystemColorAnim)
    self.particleSystem.propertyControllers = {scn.SCNParticlePropertyColor:self.particleSystemProp_con}
    self.particleSystem.emitterShape = self.flag
    self.particleSystem.birthLocation = scn.ParticleBirthLocation.SCNParticleBirthLocationSurface
    self.particleSystem.birthDirection = scn.ParticleBirthDirection.Random
        
Demo.run()
