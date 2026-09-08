import cv2

image = cv2.imread("darren.JPG")

[w,h,c] = image.shape

#filter based on red color, as cv2 read B, G, and R (so layer 0 is blue, layer 1 is green, and layer 2 is Red) (by looping)
for i in range(w):
    for j in range(h):
        image[i,j,1] = 0
        image[i,j,0] = 0
        
cv2.imshow("image merah", image)

# for camera filter

cap = cv2.VideoCapture(0) # index 0 for webcam, other index depends if u have obs, camo studio, or other installed

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Same as the previous one which is the looping, but in this case its faster, because of no loops
    frame[:, :, 0] = 0  # Blue = 0
    frame[:, :, 1] = 0  # Green = 0

    cv2.imshow("Camera Filter merah", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()