from PIL import Image
import numpy as np
index = 0
path = 'image(1).png'
image = Image.open(path).convert('RGB')
image = np.asarray(image)

image = image.tolist()
progress = len(image)
output = ""
#output += "("
output += "def draw_x_image(x, y):\n"
output += "image_line = []\n"
for lst in image:
    output += "image_line = ("
    for x in range(len(lst)):
        output += "(" + str(lst[x][0]) + ", " + str(lst[x][1]) + ", " + str(lst[x][0]) + ")"
        if x < len(lst) - 1:
            output += ", "
    output += ")\n"
    output += "for h in range(400): draw_pixel(x + h, y - " + str(index + 1) + ", image_line[h])\n"
    index += 1
    print(progress)
    progress -= 1
#output += ")"


print("\nDone!")
with open("demofile.txt", "a") as f:
    f.write(output)