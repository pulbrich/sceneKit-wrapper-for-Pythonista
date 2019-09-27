'''
In the original version this was an SKScene. For easier integration it was rewritten with objects from the Phytonista ui module.
'''
import ui
import io
import math
from PIL import Image

import sceneKit as scn

M_PI_2 = math.pi/2

class SpeedNeedle:
  def __init__(self):
    self.view = ui.ImageView()
    self.view.content_mode = ui.CONTENT_CENTER

    self.image_base = Image.open("resources/needle.png")
    size = self.image_base.size
    self.image_base = self.image_base.resize((int(size[0]*0.55), int(size[1]*0.55)))
    size = self.image_base.size
    self.image = Image.new("RGBA", (2*size[1], 2*size[1]), None)
    self.image.paste(self.image_base, (size[1], 0))
    self.image = self.image.rotate(90)
    
    self.zRotation = 0.0
    
    
  def get_zRotation(self):
    return self._zRotation/180.*math.pi
  def set_zRotation(self, angle):
    self._zRotation = angle/math.pi*180.
    self.draw_needle()
  zRotation = property(get_zRotation, set_zRotation)
    
    
  def draw_needle(self):
    needle = self.image.rotate(self._zRotation)    
    with io.BytesIO() as bIO:
      needle.save(bIO, 'PNG')
      ret_im = ui.Image.from_data(bIO.getvalue())
    self.view.image = ret_im
    
class CameraButton:
  def __init__(self):
    self.view = ui.Button()
    self.image = ui.Image.named("resources/video_camera.png")
    self.view.background_image = self.image
    self.view.action = self.setClicked
    self._clicked = False
    
    self.sound = scn.AudioSource("resources/click.caf")
    self.clickAction = scn.Action.playAudioSource(self.sound, False)
    
  def setClicked(self, sender):
    self._clicked = True

  @property
  def clicked(self):
    ret = self._clicked
    self._clicked = False
    return ret
      
class OverlayScene:
  def __init__(self, main_view):
    
    #add the speed gauge
    
    myImage = ui.Image.named("resources/speedGauge.png")
    self.myImage_view = ui.ImageView()
    self.myImage_view.frame = (20, int(main_view.frame[3]-1.5*myImage.size.height), myImage.size.width, myImage.size.height)
    self.myImage_view.image = myImage
    main_view.add_subview(self.myImage_view)
    
    #add the needle
    
    self.mySpeedNeedle = SpeedNeedle()   
    self.mySpeedNeedle.view.frame = (self.myImage_view.frame[0], self.myImage_view.frame[1]+self.myImage_view.frame[3]//2-8, self.myImage_view.frame[2], self.myImage_view.frame[3])
    main_view.add_subview(self.mySpeedNeedle.view)
    
    #add the camera button
    
    self.myCameraButton = CameraButton()
    self.myCameraButton.view.frame = (main_view.frame[2]-20-self.myCameraButton.image.size.width, int(main_view.frame[3]-1.5*myImage.size.height+10), self.myCameraButton.image.size.width, self.myCameraButton.image.size.height)
    main_view.add_subview(self.myCameraButton.view)
    
    #add a close button
    self.close_button = ui.Button()
    self.close_button.action = self.closeClick
    self.close_button.frame = (20, 40, 40, 40)
    self.close_button.background_image = ui.Image.named('emj:No_Entry_2')
    self.close = False
    main_view.add_subview(self.close_button)
    
  def closeClick(self, sender):
    self.close = True

