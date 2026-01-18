from PIL import Image
import numpy as np
from collections import deque
from math import sin

# load the image and convert into 
# numpy array
img = Image.open('bob.png')
numpydata = np.asarray(img)

frame = 0

for x in range(30):
    oldpixels = list(numpydata)

    for i in range(len(oldpixels)):
        current_list = deque(oldpixels[i])
        if i % 2 == 0:
            current_list.rotate(int(sin(((frame) + i) / 5) * 4))
        else:
            current_list.rotate(int(sin(((frame) + i) / 5) * -4))
        
        oldpixels[i] = list(current_list)

    array = np.array(oldpixels, dtype=np.uint8)
                
    # Use PIL to create an image from the new array of pixels
    new_image = Image.fromarray(array)
    new_image.save(str(x + 1) + '.png')
    frame += 0.5 * 3.14159