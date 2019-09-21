'''audio modul, to be included in sceneKit'''

from objc_util import nsurl
import os

import sceneKit
from .sceneKitEnv import *
from .sceneKitNode import *

class AudioSource(CInst):
  def __init__(self, url=None, fileName=None, named=None, ID=None):
    if named is not None: fileName=named
    if url is not None:
      self.ID = SCNAudioSource.alloc().initWithURL_(nsurl(self.convertURL(url)))
    elif fileName is not None:
      self.ID = SCNAudioSource.audioSourceNamed_(fileName)    
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = SCNAudioSource.alloc()
      
# for Pythonista built-in sounds
  def convertURL(self, url):
    pythonistaSoundDir = os.path.abspath(os.path.join(os.__file__, '../../../..')+'/Media/Sounds/')
    soundFileExtention = '.caf'
    (root, ext) = os.path.splitext(url)
    if len(ext) == 0:
      root = root.replace(':', '/')
      url = pythonistaSoundDir+'/'+root+soundFileExtention
    return url

  @classmethod
  def audioSourceNamed(cls, fileName=None, named=None):
    return cls(fileName=fileName, named=named)
    
  def initWithFileNamed(self, name=None, fileNamed=None):
    if fileNamed is not None: name=fileNamed
    self.ID.initWithFileNamed_(name)    
  initWithFile = initWithFileNamed
  
  def initWithURL(self, url=None):
    return self.ID.initWithURL_(nsurl(self.convertURL(url)))

  def setPositional(self, aBool):
    self.ID.setPositional_(aBool)    
  def isPositional(self):
    return self.ID.positional()
  positional = property(isPositional, setPositional)
  
  def load(self):
    self.ID.load()
    
  def setVolume(self, aVolume):
    self.ID.setVolume_(aVolume)    
  def getVolume(self):
    return self.ID.volume()
  volume = property(getVolume, setVolume)
  
  def setRate(self, aRate):
    self.ID.setRate_(aRate)    
  def getRate(self):
    return self.ID.rate()
  rate = property(getRate, setRate)
  
  def setReverbBlend(self, aReverbBlend):
    self.ID.setReverbBlend_(aReverbBlend)    
  def getReverbBlend(self):
    return self.ID.reverbBlend()
  reverbBlend = property(getReverbBlend, setReverbBlend)
  
  def setLoops(self, aBool):
    self.ID.setLoops_(aBool)    
  def getLoops(self):
    return self.ID.loops()
  loops = property(getLoops, setLoops)
  
  def setShouldStream(self, aBool):
    self.ID.setShouldStream_(aBool)    
  def getShouldStream(self):
    return self.ID.shouldStream()
  shouldStream = property(getShouldStream, setShouldStream)
  
class AudioPlayer(CInst):
  def __init__(self, source=None, audioNode=None, ID=None):
    if source is not None:
      self.ID = SCNAudioPlayer.audioPlayerWithSource_(source.ID)
    elif audioNode is not None:
      self.ID = SCNAudioPlayer.audioPlayerWithAVAudioNode_(audioNode)
    elif ID is not None:
      self.ID = ID
    else:
      self.ID = SCNAudioPlayer.alloc()
      
  @classmethod
  def audioPlayerWithSource(cls, source=None):
    return cls(source=source)
    
  @classmethod
  def audioPlayerWithAVAudioNode(cls, audioNode=None, AVAudioNode=None, avAudioNode=None):
    if AVAudioNode is not None: audioNode = AVAudioNode
    if avAudioNode is not none: audioNode = avAudioNode
    return cls(audioNode=audioNode)
      
  def initWithSource(self, source=None):
    self.ID.initWithSource_(source.ID)
    
  def initWithAVAudioNode(self, audioNode=None, AVAudioNode=None, avAudioNode=None):
    if AVAudioNode is not None: audioNode = AVAudioNode
    if avAudioNode is not None: audioNode = avAudioNode
    self.ID.initWithAVAudioNode_(audioNode)
    
  def getAudioSource(self):
    return sceneKit.AudioSource.outof(self.ID.audioSource())
  audioSource = property(getAudioSource, None)
  
  def getAudioNode(self):
    return self.ID.audioNode()
  audioNode = property(getAudioNode, None)
  
  def setWillStartPlayback(self, aBlock):
    self.audioSourceWillStartPlayback = AudioSourceWillStartStopPlaybackBlock(aBlock)
    self.ID.setWillStartPlayback_(self.audioSourceWillStartPlayback.blockCode)    
  def getWillStartPlayback(self):
    return self.audioSourceWillStartPlayback.pCode
  willStartPlayback = property(getWillStartPlayback, setWillStartPlayback)
  
  def setDidFinishPlayback(self, aBlock):
    self.audioSourceDidFinishPlayback = AudioSourceWillStartStopPlaybackBlock(aBlock)
    self.ID.setDidFinishPlayback_(self.audioSourceDidFinishPlayback.blockCode)    
  def getDidFinishPlayback(self):
    return self.audioSourceDidFinishPlayback.pCode
  didFinishPlayback = property(getDidFinishPlayback, setDidFinishPlayback)
  
  
class AudioSourceWillStartStopPlaybackBlock:
  def __init__(self, block):    
    self.blockCode = ObjCBlock(self.blockInterface, restype=None, argtypes=[c_void_p])
    self.pCode = block
      
  def blockInterface(self, _cmd):
    self.pCode()
