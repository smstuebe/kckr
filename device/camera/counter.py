#%%
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("C:\\Users\\sv\\Downloads\\IMG_20140625_233602.jpg")
#
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# This just hides x and y tick values by passing in 
# empty lists to make the output a little cleaner 
plt.xticks([]), plt.yticks([]) 
plt.show()

#%%
