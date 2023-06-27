import os, cv2, json, sys
import numpy as np
import logging

from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.conf import settings
from .forms import VideoForm
from ultralytics import YOLO
from datetime import datetime

form = VideoForm()
form_data = { 'form': form }

# logging -----------------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# logging end --------------------------------

def uploadIn(request) :
    return render(request, 'upload/uploadIn.html', form_data)

def uploadOut(request) :
    return render(request, 'upload/uploadOut.html', form_data)

def uploadWork(request) :
    return render(request, 'upload/uploadWork.html', form_data)

# --- 업로드 ----

def uploadInSubmit(request):
    if request.method == 'POST':
       
        video = request.FILES['files[]'] # 비디오 파일 불러오기
        base_dir = os.path.dirname(os.path.abspath(__file__)) # 현재 base 위치 지정
        model_path = os.path.join(base_dir, 'model', 'fire.pt') #  model 불러오기 -> 모델은 upload/model/내에 있음!
        model = YOLO(model_path) # 모델 실행
        return StreamingHttpResponse(generate_frames(video, model, 'internal'), content_type='multipart/x-mixed-replace; boundary=frame')
    return render(request, 'upload/uploadIn.html')


# 영상 추출
def generate_frames(video, model, where):
    if where == 'internal' :
        # 국사 내부 로그
        internal_log_handler = logging.FileHandler(f'log/internal/{datetime.now().strftime("%Y-%m-%d")}.log')
        internal_log_handler.setLevel(logging.INFO)
        logger.addHandler(internal_log_handler)
        
    cap = cv2.VideoCapture(video.temporary_file_path()) # 영상 지정
    frame_height = int(cap.get(4))
    frame_width = int(cap.get(3))

    # video writer 설정
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30.0
    frame_size = (640, 480)
    vid_num = 0
    flag = 0

    while cap.isOpened():
        ret, frame = cap.read() # 영상 프레임 읽기
        if not ret: #영상 재생이 안될 경우 break
            break
        frame = cv2.resize(frame, frame_size)
        # 모델 실행 및 프레임 처리
        results = model.predict(frame,verbose = False, conf = 0.7)[0] # 모델을 예측함 ; 예측률 70% 이상이 아니면 예측 continue
        frame_predicted = results.plot(prob = False, conf = False) # model numpy로 가져옴 #model size와 같음
        
        datas = json.loads(results.tojson()) # 모델 결과 추출 -> log로 보낼 내용들
        now_time = datetime.now()

        # 영상 저장 위치 지정
        if flag == 0 :
            os.makedirs(f"{settings.MEDIA_ROOT}/fire/", exist_ok= True)
            output_file = f"{settings.MEDIA_ROOT}/fire/{vid_num}_output.mp4"
            video_writer = cv2.VideoWriter(output_file, codec, fps, frame_size)
            flag = 1
            save_time = datetime.now()

        ################## 영상 log 남김!! #########################
        arr = results.boxes.cls.cpu().numpy()
        if len(arr) > 0 :
            class_counts = np.vectorize(results.names.get)(arr)
            for label in class_counts:
                times_check = now_time.strftime('%Y-%m-%d %H:%M:%S')
                logger.info(f"{times_check} {label} ") # 시간, 라벨
            
        # 영상 저장 중..
        if flag == 1:
            video_writer.write(frame_predicted)

        _, jpeg_frame = cv2.imencode('.jpg', frame_predicted) # cv2.imshow가 안되기 때문에 대체하였음
        frame_bytes = jpeg_frame.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        
        # 영상 저장
        time_diff = now_time - save_time
        if time_diff.total_seconds() >= 3:
            video_writer.release()
            flag = 0
            vid_num += 1
