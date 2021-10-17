import cv2
import numpy as np

count = []
counter = 0

def find_blobs(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]

    contours = cv2.findContours(thresh, cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)[0]

    coordinates = []
    s1 = 20
    # print(cnts)

    global counter
    global count

    count.append(len(contours))

    if counter == 10:
        counter = 0
        print(count)
    else:
        counter += 1

    for contour in contours:
        if s1 < cv2.contourArea(contour):
            M = cv2.moments(contour)

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            cv2.circle(frame, (cX, cY), 15, (0, 255, 0), -1)

            coordinates.append((cX, cY))

    # print("\nDots number: {}".format(len(xcnts)))
    # print(f"coordinates: {coordinates}")
    return coordinates

def calculate_positions(coordinates, im):
    size = im.shape

    image_points = np.array(coordinates, dtype="double")

    # 3D model points.
    model_points = np.array([
        (0.0, 0.0, 0.0),  # Center
        (-150, -150, 0),  # Left up
        (150, -150, 0),  # Right up
        (-150, 150, 0),  # Left down
        (150, 150, 0),  # Right down
    ])

    # Camera internals
    focal_length = size[1]
    center = (size[1] / 2, size[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]],
         [0, focal_length, center[1]],
         [0, 0, 1]], dtype="double"
    )

    print("Camera Matrix :\n {0}".format(camera_matrix))

    dist_coeffs = np.zeros((4, 1))  # Assuming no lens distortion
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                  dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    print("Rotation Vector:\n {0}".format(rotation_vector))
    print("Translation Vector:\n {0}".format(translation_vector))

    # Project a 3D point (0, 0, 1000.0) onto the image plane.
    # We use this to draw a line sticking out of the nose

    (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector,
                                                     translation_vector, camera_matrix, dist_coeffs)

    for p in image_points:
        cv2.circle(im, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

    p1 = (int(image_points[0][0]), int(image_points[0][1]))
    p2 = (int(nose_end_point2D[0][0][0]), int(nose_end_point2D[0][0][0]))

    cv2.line(im, p1, p2, (255, 0, 0), 4)