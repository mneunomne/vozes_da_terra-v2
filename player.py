# list audio files
import glob
def listFiles(path):
  return glob.glob(path + '*.wav')

import random
def getNextFile(files):
  return random.choice(files)

import pyaudio
import wave
CHUNK = 1024

def getRandomFile():
  files = listFiles('audios/')
  filename = getNextFile(files)
  return filename

def play(filename):
  # opem file
  f = wave.open(filename, 'rb')
  p = pyaudio.PyAudio()
  #open stream  
  stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                  channels = f.getnchannels(),  
                  rate = f.getframerate(),  
                  output = True)
  # read data
  data = f.readframes(CHUNK)
  #play stream  
  while data:
      stream.write(data)  
      data = f.readframes(CHUNK)
  #stop stream  
  stream.stop_stream()  
  stream.close()  
  #close PyAudio  
  p.terminate()
  