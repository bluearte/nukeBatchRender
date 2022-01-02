import os
import sys

def GetEpisodes():
   episodes = []
   return episodes

def GetSequences(episode=None):
   sequences = []
   return sequences

def GetShots(episode=None, sequence=None):
   shots = []
   return shots

def GetNukeScripts(episode=None, sequence=None, shot=None, verbose=False):
   location = "{root}/{episode}/{sequence}/{shot}".format(episode, sequence, shot)
   nk_files = []
   for each_nukescripts in os.listdir(location):
      nk_file = os.path.join(location, each_nukescripts).replace("\\", "/")
      if os.path.exists(nk_file):
         if not each_nukescripts.endswith(".nk~"):
            nk_files.append(each_nukescripts)
   
   return nk_files