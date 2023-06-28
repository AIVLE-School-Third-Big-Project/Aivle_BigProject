import os, cv2, json, sys, os
import numpy as np
import logging

from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.conf import settings
from .forms import VideoForm
from ultralytics import YOLO
from datetime import datetime, timedelta

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from collections import Counter

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
def uploadOutSubmit(request):
    if request.method == 'POST':
       
        video = request.FILES['files[]'] # 비디오 파일 불러오기
        base_dir = os.path.dirname(os.path.abspath(__file__)) # 현재 base 위치 지정
        model_path = os.path.join(base_dir, 'model', 'human.pt') #  model 불러오기 -> 모델은 upload/model/내에 있음!
        model = YOLO(model_path) # 모델 실행
        return StreamingHttpResponse(generate_frames_external(video, model), content_type='multipart/x-mixed-replace; boundary=frame')
    return render(request, 'upload/uploadOut.html')


def uploadInSubmit(request):
    if request.method == 'POST':
       
        video = request.FILES['files[]'] # 비디오 파일 불러오기
        base_dir = os.path.dirname(os.path.abspath(__file__)) # 현재 base 위치 지정
        model_path = os.path.join(base_dir, 'model', 'fire.pt') #  model 불러오기 -> 모델은 upload/model/내에 있음!
        model = YOLO(model_path) # 모델 실행
        return StreamingHttpResponse(generate_frames_internal(video, model), content_type='multipart/x-mixed-replace; boundary=frame')
    return render(request, 'upload/uploadIn.html')

def uploadWorkSubmit(request):
    if request.method == 'POST':
       
        video = request.FILES['files[]'] # 비디오 파일 불러오기
        base_dir = os.path.dirname(os.path.abspath(__file__)) # 현재 base 위치 지정
        model_path = os.path.join(base_dir, 'model', 'ppe.pt') #  model 불러오기 -> 모델은 upload/model/내에 있음!
        model = YOLO(model_path) # 모델 실행
        return StreamingHttpResponse(generate_frames_Work(video, model), content_type='multipart/x-mixed-replace; boundary=frame')
    return render(request, 'upload/uploadWork.html')

# --- 업로드 ---

# 국사 내부 영상 추출 -------------------------------------------------
def generate_frames_internal(video, model):
    
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
    
    # 영상 폴더 지정 ------------------------------------------------ 김유민
    number_fire = 0 # 날짜 영상저장 번호        
    while os.path.exists(f'{settings.MEDIA_ROOT}/fire/{datetime.now().strftime("%Y-%m-%d")}/{number_fire}/') :
        number_fire+=1
    # 영상 폴더 지정 ------------------------------------------------ 김유민

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
            os.makedirs(f"{settings.MEDIA_ROOT}/fire/{datetime.now().strftime('%Y-%m-%d')}/{number_fire}/", exist_ok= True)
            output_file = f"{settings.MEDIA_ROOT}/fire/{datetime.now().strftime('%Y-%m-%d')}/{number_fire}/{vid_num}_output.mp4"
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


# 국사 외부 영상 추출 -------------------------------------------------
##  model algorithm
def point_in_polygon(point, polygon):
    point = Point(point)
    polygon = Polygon(polygon)
    if polygon.contains(point):
        return "invade"
    else:
        return "person"
    
def generate_frames_external(video, model):
    
    # 국사 외부 로그
    external_log_handler = logging.FileHandler(f'log/external/{datetime.now().strftime("%Y-%m-%d")}.log')
    external_log_handler.setLevel(logging.INFO)
    logger.addHandler(external_log_handler)
    
    cap = cv2.VideoCapture(video.temporary_file_path()) # 영상 지정
    frame_height = int(cap.get(4))
    frame_width = int(cap.get(3))
    
    # video writer 설정
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30.0
    frame_size = (640, 480)
    vid_num = 0
    flag = 0
    save_time = datetime.now()
    
     # 영상 폴더 지정 ------------------------------------------------ 김유민
    number_human = 0 # 날짜 영상저장 번호        
    while os.path.exists(f'{settings.MEDIA_ROOT}/human/{datetime.now().strftime("%Y-%m-%d")}/{number_human}/') :
        number_human+=1
    # 영상 폴더 지정 ------------------------------------------------ 김유민
    
    while cap.isOpened():
        ret, frame = cap.read() # 영상 프레임 읽기
        if not ret: #영상 재생이 안될 경우 break
                break
        frame = cv2.resize(frame, frame_size)
        frame_copy = frame.copy()  # 원본 영상의 복사본 생성
        points = [(281, 426), (648, 210), (977, 226), (978, 477), (470, 713)]


        # 좌표 리사이즈
        resized_points = []
        for point in points:
            x = int(point[0] * frame_size[0] / frame_width)
            y = int(point[1] * frame_size[1] / frame_height)
            resized_points.append((x, y))
        points = resized_points

        # 다각형 그리기
        
        mask = np.zeros_like(frame_copy[:, :, 0])
        points_arr = np.array(points)
        
        cv2.polylines(frame_copy, [points_arr.astype(np.int32)], isClosed=True, color=(0, 0, 255), thickness=2)  # 다각형 테두리를 빨간색으로 그림


        # 모델 실행 및 프레임 처리
        # model inside
        results = model.predict(frame_copy,verbose = False, conf = 0.7, classes = [0,1])[0] # 모델을 예측함 ; 예측률 70% 이상이 아니면 예측 continue
        boxes = results.boxes.cpu().numpy()

        # 
        class_check = []
        for box in boxes:
            r = box.xyxy[0].astype(int)
            ct = box.xywh[0].astype(int)
            text_position = (r[0], r[1] - 10)
            class_name = point_in_polygon(ct[:2], points)
            cv2.rectangle(frame_copy, r[:2], r[2:], (255, 255, 255), 2)
            cv2.putText(frame_copy, class_name, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
            class_check.append(class_name)
        class_counts = Counter(class_check)

        now_time = datetime.now()

        # 영상 저장 위치 지정
        if ('invade' in class_check) and (flag == 0) :
            os.makedirs(f"{settings.MEDIA_ROOT}/human/{datetime.now().strftime('%Y-%m-%d')}/{number_human}/", exist_ok= True)
            output_file = f"{settings.MEDIA_ROOT}/human/{datetime.now().strftime('%Y-%m-%d')}/{number_human}/{vid_num}_output.mp4"
            video_writer = cv2.VideoWriter(output_file, codec, fps, frame_size)
            flag = 1
            save_time = datetime.now()

        ################## 영상 log 남김!! #########################
        for label, count in class_counts.items():
            times_check = now_time.strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"{times_check} {label} {count}명") # 시간, 라벨

        # 영상 저장 중..
        if flag == 1:
            video_writer.write(frame_copy)

        _, jpeg_frame = cv2.imencode('.jpg', frame_copy) # cv2.imshow가 안되기 때문에 대체하였음
        frame_bytes = jpeg_frame.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        
        # 영상 저장
        if flag == 1:
            time_diff = now_time - save_time
            
            if time_diff.total_seconds() >= 3:
                print(now_time + timedelta(seconds=3))
                video_writer.release()
                flag = 0
                vid_num += 1
                
                
                
# 작업자 안전 영상 추출 -------------------------------------------------
def generate_frames_Work(video, model):
    
    log_directory = 'log/WorkSafe/'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    # 작업자 안전 로그
    Work_log_handler = logging.FileHandler(f'log/WorkSafe/{datetime.now().strftime("%Y-%m-%d")}.log')
    Work_log_handler.setLevel(logging.INFO)
    logger.addHandler(Work_log_handler)
    
    cap = cv2.VideoCapture(video.temporary_file_path()) # 영상 지정
    frame_height = int(cap.get(4))
    frame_width = int(cap.get(3))

    # video writer 설정
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30.0
    frame_size = (640, 480)
    vid_num = 0
    flag = 0

    # 영상 폴더 지정 ------------------------------------------------ 김유민
    number_ppe = 0 # 날짜 영상저장 번호        
    while os.path.exists(f'{settings.MEDIA_ROOT}/ppe/{datetime.now().strftime("%Y-%m-%d")}/{number_ppe}/') :
        number_ppe+=1
    # 영상 폴더 지정 ------------------------------------------------ 김유민
        
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
            os.makedirs(f"{settings.MEDIA_ROOT}/ppe/{datetime.now().strftime('%Y-%m-%d')}/{number_ppe}/", exist_ok= True)
            output_file = f"{settings.MEDIA_ROOT}/ppe/{datetime.now().strftime('%Y-%m-%d')}/{number_ppe}/{vid_num}_output.mp4"
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
