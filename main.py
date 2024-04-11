import numpy as np
import cv2 as cv

# The given video and calibration data
video_file = './mycheckerboard.mp4'
# K = np.array([[432.7390364738057, 0, 476.0614994349778],
#               [0, 431.2395555913084, 288.7602152621297],
#               [0, 0, 1]])
# dist_coeff = np.array([-0.2852754904152874, 0.1016466459919075, -0.0004420196146339175, 0.0001149909868437517, -0.01803978785585194])

K = np.array([[1.10609014e+03, 0.00000000e+00, 3.61767044e+02],
              [0.00000000e+00, 1.10955128e+03, 6.29851568e+02],
              [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist_coeff = np.array([0.1923464,  -0.54927128, -0.00272621,  0.00240072, -0.64792052])

board_pattern = (9, 6) # change board_pattern
board_cellsize = 0.025
board_criteria = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK

# Open a video
video = cv.VideoCapture(video_file)
assert video.isOpened(), 'Cannot read the given input, ' + video_file

# Define the bottom and top of the pentagon
bottom_points = np.array([
    [4, 3, 0], [4.5, 2, 0], [5.5, 2, 0], [6, 3, 0], [5, 4, 0]
]) * board_cellsize
top_points = np.array([
    [4, 3, -1], [4.5, 2, -1], [5.5, 2, -1], [6, 3, -1], [5, 4, -1]
]) * board_cellsize

# Prepare 3D points on a chessboard
obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

# Run pose estimation
while True:
    # Read an image from the video
    valid, img = video.read()
    if not valid:
        break

    # Estimate the camera pose
    success, img_points = cv.findChessboardCorners(img, board_pattern, board_criteria)
    if success:
        ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K, dist_coeff)


        # Draw the pentagon pillar on the image
        bottom_projected, _ = cv.projectPoints(bottom_points, rvec, tvec, K, dist_coeff)
        top_projected, _ = cv.projectPoints(top_points, rvec, tvec, K, dist_coeff)
        cv.polylines(img, [np.int32(bottom_projected)], True, (255, 0, 0), 2)
        cv.polylines(img, [np.int32(top_projected)], True, (0, 0, 255), 2)
        for b, t in zip(bottom_projected, top_projected):
            cv.line(img, np.int32(b.flatten()), np.int32(t.flatten()), (0, 255, 0), 2)

        # Print the camera position
        R, _ = cv.Rodrigues(rvec)  # Alternative) `scipy.spatial.transform.Rotation`
        p = (-R.T @ tvec).flatten()
        info = f'XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]'
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    # Show the image and process the key event
    cv.imshow('Pose Estimation (Chessboard)', img)
    key = cv.waitKey(10)
    if key == ord(' '):
        key = cv.waitKey()
    if key == 27:  # ESC
        break

video.release()
cv.destroyAllWindows()
