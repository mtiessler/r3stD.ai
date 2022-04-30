import cv2
 
# Opens the inbuilt camera of laptop to capture video.
cap = cv2.VideoCapture(r"2022_04_30_1320074500.mp4")
i = 0
 
while(cap.isOpened()):
    ret, frame = cap.read()
     
    # This condition prevents from infinite looping
    # incase video ends.
    if ret == False:
        break
     
    # Save Frame by Frame into disk using imwrite method
    print("Saving frame: ", i)
    cv2.imwrite('output/Frame{:05d}.jpg'.format(i), frame)
    i += 1
 
cap.release()
cv2.destroyAllWindows()