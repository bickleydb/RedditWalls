#Daniel Bickley
#Reddit Image Downloader

#Python Script that connects to the specified subreddits, and 
#grabs the hottest lets say 20 images on the subreddit. Currently,
#the script just grabs the images from imgur, but I will probably
#work on that later.

from PIL import Image
from StringIO import StringIO
import praw
import json
import pprint
import requests
import re
import os

user_agent = "BackgroundSaving by /u/Flaming_Sousa"
r = praw.Reddit(user_agent = user_agent)

numPics = 0
subReddits = ['fractalporn', 'gamerporn', 'avporn', 'geekporn', 'quotesporn',
              'architectureporn']

dirPath = "/home/daniel/wallpapers/"
fileList = os.listdir(dirPath)
for fileName in fileList:
  os.remove(dirPath+"/"+fileName)

for name in subReddits:
  numPics = 0
  subRedditName = name
  submissions = r.get_subreddit(subRedditName).get_hot(limit=20)
  for sub in submissions:
    url = sub.short_link
    headers = {'user-agent' : 'wallpaperdownloading test /u/flaming_sousa'}
    q = requests.get(url,headers=headers)
    webpage = q.text
    pattern = re.compile("content=\"(http://.*jpg|png|gif|apng)\"><")
    match = re.search(pattern,webpage)
    if match:
      t = requests.get(match.group(1))
      i = Image.open(StringIO(t.content))
      extention = match.group(1)[-3:]
      fileNamePat = re.compile("jpg")
      name = re.sub(fileNamePat,"jpeg",extention)
      i.save('/home/daniel/wallpapers/{}{}.{}'.format(subRedditName,numPics,name))
      numPics = numPics+1
