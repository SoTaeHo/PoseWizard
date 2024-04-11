# PoseWizard
<img width="531" alt="result" src="https://github.com/SoTaeHo/PoseWizard/assets/91146046/04733323-f9e6-491a-896a-e6ecb9da88e2">

----------------------

<img width="350" alt="define_pentagon" src="https://github.com/SoTaeHo/PoseWizard/assets/91146046/3a53419c-a4d1-4e83-b2e0-1ecc4470cac3">

camera calibration을 진행하여 camera matrix K와 distortion coefficient를 구한 뒤, cv.solvePnP()를 사용하여 camera pose estimation을 진행해준다.

<img width="350" alt="draw_pentagon" src="https://github.com/SoTaeHo/PoseWizard/assets/91146046/4e941d56-d551-4d09-91c4-f23d6fbfe3ac">

이후 미리 정의해놓은 checkboard상의 bottom_points와 top_points의 위치를 cv.projectPoints()의 인자에 포함시켜 영상에 오각형을 그려준다.


calibration.py : 캘리브레이션의 결과를 출력해주는 파일

main.py : 캘리브레이션의 결과를 토대로 camera pose estimation 및 AR 물체를 그려주는 파일
