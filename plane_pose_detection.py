
#!/usr/bin/env python

import cv2
import numpy as np
path = "images/drone_station2.png"
from preprossesing.count_white_dots import find_coords

# Read Image
im = cv2.imread(path);
size = im.shape

#2D image points. If you change the image, you need to change vector
# image_points = np.array([
#                             (222, 570),     # Center
#                             (250, 530),     # Left up
#                             (116, 540),     # Right up
#                             (324, 600),     # Left down
#                             (190, 616),     # Right down
#                         ], dtype="double")
coordinates = [(262, 304), (64, 103), (453, 103), (61, 510), (468, 502)]
image_points = np.array(coordinates, dtype="double")

# 3D model points.
model_points = np.array([
                            (0.0, 0.0, 0.0),  # Center
                            (-150, -150, 0),  # Left up
                            (150, -150, 0),  # Right up
                            (-150, 150, 0),    # Left down
                            (150, 150, 0),     # Right down
                        ])

# Camera internals
focal_length = size[1]
center = (size[1]/2, size[0]/2)
camera_matrix = np.array(
                         [[focal_length, 0, center[0]],
                         [0, focal_length, center[1]],
                         [0, 0, 1]], dtype="double"
                         )

print("Camera Matrix :\n {0}".format(camera_matrix))

dist_coeffs = np.zeros((4,1)) # Assuming no lens distortion
(success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

print("Rotation Vector:\n {0}".format(rotation_vector))
print("Translation Vector:\n {0}".format(translation_vector))


# Project a 3D point (0, 0, 1000.0) onto the image plane.
# We use this to draw a line sticking out of the nose

(nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

for p in image_points:
    cv2.circle(im, (int(p[0]), int(p[1])), 3, (0,0,255), -1)


p1 = (int(image_points[0][0]), int(image_points[0][1]))
p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][1]))

cv2.line(im, p1, p2, (255,0,0), 2)

# Display image
cv2.imshow("Output", im)
cv2.waitKey(0)
