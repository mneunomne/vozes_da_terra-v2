from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer, player_for, from_file
import player
import sys
import wave
from thread import *
from pynput import keyboard
import datetime 
import os
from pydub import AudioSegment
from gui import *
from argparse import ArgumentParser

from gui import *

parser = ArgumentParser()
parser.add_argument("-g", "--GUI", dest="settings",
                    help="Display Graphic Interface", default=False)

# parametros de áudio
max_length = 1000000
max_interval = 12000
max_continuous_silence = 500
min_length = 150
sample_rate = 48000
energy_threshold = 51

asource = ADSFactory.ads(record=True, max_time = max_length, sampling_rate = sample_rate)

sample_width = asource.get_sample_width()
channels = asource.get_channels()
# START VALIDATOR
validator = AudioEnergyValidator(sample_width=sample_width, energy_threshold = energy_threshold)
tokenizer = StreamTokenizer(validator=validator, min_length=1, max_length=max_length, max_continuous_silence=max_continuous_silence)

audio_folder = 'new_audios/'
MODE = 'ECHO'

useGui = True

if useGui:
  root = Tk()
  display = GUI(root)

def init():
  listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
  listener.start()
  listen()
  

def listen():
  ## abrir microfone
  if useGui:
    display.set_state('listening')
  asource.open()
  print("\n  ** Make some noise (dur:{}, energy:{})...".format(max_length, energy_threshold))      
  ## começar tokenizer
  tokenizer.tokenize(asource, callback=onDetection)
  asource.close()

def on_press(key):
  return ''

def on_release(key):
  if hasattr(key, 'char'):
    global MODE
    if key.char == 'e':
      MODE = 'ECHO'
      print('set mode to', MODE)
    if key.char == 'r':
      MODE = 'RANDOM'
      print('set mode to', MODE)
    if key.char == 'q':
      asource.close()
      sys.exit(0)

def onDetection(data, start, end):
  log = "Acoustic activity at: {0}--{1}".format(start, end)
  print(log)
  display.display_text(log)
  filename = savefile(data, start, end)
  print('current mode', MODE)
  if MODE == 'RANDOM':
    randomfile = player.getRandomFile()
    display.display_text('playing random ' + randomfile)
    player.play(randomfile)
  if MODE == 'ECHO':
    display.display_text('playing recorded ' + filename)
    player.play(filename)
  print("finished playing")

def savefile(data, start, end):
  filename = audio_folder + '{:%Y-%m-%d_%H:%M:%S}'.format(datetime.datetime.now())
  # filename = audio_folder + "teste_{0}_{1}.wav".format(start, end)      
  # create folder if 'audios' doesnt exist
  if not os.path.exists(os.path.dirname(filename)):
      try:
          os.makedirs(os.path.dirname(filename))
      except OSError as exc: # Guard against race condition
          if exc.errno != errno.EEXIST:
              raiseRec

  # save wav file
  waveFile = wave.open(filename, 'wb')
  waveFile.setnchannels(channels)
  waveFile.setsampwidth(sample_width)
  waveFile.setframerate(sample_rate)
  waveFile.writeframes(b''.join(data))
  waveFile.close()

  # normalize volume
  sound = AudioSegment.from_file(filename, "wav")
  normalized_sound = match_target_amplitude(sound, -15.0)
  with_fade = normalized_sound.fade_in(200).fade_out(200)
  with_fade.export(filename, format="wav")
  
  print('audio saved at', filename)
  return filename

def match_target_amplitude(sound, target_dBFS):
  change_in_dBFS = target_dBFS - sound.dBFS
  return sound.apply_gain(change_in_dBFS)

init()