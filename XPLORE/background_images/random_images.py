# Code slightly modified from : https://gist.github.com/jeff-mccarthy/3e04e39014046ffb36e36e001da74449
# Download random images

import os
import urllib.request

# Welcome message
print('Download random stock images from picsum.photos\n(* images download to the current directory)')

# Paths
# get current working directory
cwd = os.getcwd()

# Images
# python 2 uses raw_input() to return a string, python 3 uses input()
imgNum = int(input('Enter number of images: '))  # Convert to int
imgDim = input('Enter image size (e.g. 640x480): ').split('x')

# change directory to current working directory
# os.path.join(a,b) if you want to allow custom paths
os.chdir(cwd)

for i in range(1, imgNum + 1):
    i = str(i)
    urllib.request.urlretrieve(('https://picsum.photos/' + imgDim[0] + '/' + imgDim[1] + '?random'), ('stock-image-' + i + '.jpg'))
