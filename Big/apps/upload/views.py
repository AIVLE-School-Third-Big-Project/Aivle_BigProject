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
from collections import Counter, deque

form = VideoForm()
form_data = { 'form': form }

logging.getLogger().propagate = False

def uploadIn(request) :
    return render(request, 'upload/uploadIn.html', form_data)

def uploadOut(request) :
    return render(request, 'upload/uploadOut.html', form_data)

def uploadWork(request) :
    return render(request, 'upload/uploadWork.html', form_data)

# --- 업로드 ----
def uploadOutSubmit(request):
    if request.method == 'POST':
       
        try :
            video = request.FILES['files[]'] # 비디오 파일 불러오기
            base_dir = os.path.dirname(os.path.abspath(__file__)) # 현재 base 위치 지정
            model_path = os.path.join(base_dir, 'model', 'human.pt') #  model 불러오기 -> 모델은 upload/model/내에 있음!
            model = YOLO(model_path) # 모델 실행
            return StreamingHttpResponse(generate_frames_external(video, model), content_type='multipart/x-mixed-replace; boundary=frame')
        
        except KeyError :
            return render(request, 'upload/noFileUpload.html')
        except ValueError :
            return render(request, 'upload/videoValueError.html')
        
    return render(request, 'upload/uploadOut.html')


def uploadInSubmit(request):
    if request.method == 'POST':
        try :
            video = request.FILES['files[]'] # 비디오 파일 불러오기
            base_dir = os.path.dirname(os.path.abspath(__file__)) # 현재 base 위치 지정
            model_path = os.path.join(base_dir, 'model', 'fire.pt') #  model 불러오기 -> 모델은 upload/model/내에 있음!
            model = YOLO(model_path) # 모델 실행
            return StreamingHttpResponse(generate_frames_internal(video, model), content_type='multipart/x-mixed-replace; boundary=frame')
        except KeyError :
            return render(request, 'upload/noFileUpload.html')
        except ValueError :
            return render(request, 'upload/videoValueError.html')
        
    return render(request, 'upload/uploadIn.html')

def uploadWorkSubmit(request):
    if request.method == 'POST':
       
        try :
            video = request.FILES['files[]'] # 비디오 파일 불러오기
            base_dir = os.path.dirname(os.path.abspath(__file__)) # 현재 base 위치 지정
            model_path = os.path.join(base_dir, 'model', 'ppe.pt') #  model 불러오기 -> 모델은 upload/model/내에 있음!
            model = YOLO(model_path) # 모델 실행
            return StreamingHttpResponse(generate_frames_Work(video, model), content_type='multipart/x-mixed-replace; boundary=frame')
        except KeyError :
            return render(request, 'upload/noFileUpload.html')
        except ValueError :
            return render(request, 'upload/videoValueError.html')
    return render(request, 'upload/uploadWork.html')

# --- 업로드 ---

# 국사 내부 영상 추출 ------------------------------------------------- #!fire - 이근섭
def generate_frames_internal(video, model):
    
    log_directory = 'log/'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        
    # 영상 이름 뒤 숫자 지정 ------------------------------------------------ 김유민
    number_fire = 0 # 날짜 영상저장 번호        
    while os.path.exists(f'{settings.STATICFILES_DIRS[0]}/videoLog/fire/{datetime.now().strftime("%Y-%m-%d")}/fire-{datetime.now().strftime("%Y-%m-%d")}-{number_fire}.mp4') :
        number_fire+=1
    
    
    # 국사 내부 로그 경로 : 클래스-날짜-넘버.log
    text_log_path = log_directory + f'fire-{datetime.now().strftime("%Y-%m-%d")}-{number_fire}.log'
        
    cap = cv2.VideoCapture(video.temporary_file_path()) # 영상 지정
    frame_height = int(cap.get(4))
    frame_width = int(cap.get(3))

    # video writer 설정
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30.0
    frame_size = (640, 480)
    vid_num = 0
    flag = 0
    

    # 전체 영상 저장
    os.makedirs(f"{settings.STATICFILES_DIRS[0]}/videoLog/fire/{datetime.now().strftime('%Y-%m-%d')}/", exist_ok= True)
    output_all_file = f"{settings.STATICFILES_DIRS[0]}/videoLog/fire/{datetime.now().strftime('%Y-%m-%d')}/fire-{datetime.now().strftime('%Y-%m-%d')}-{number_fire}.mp4"
    all_video_writer = cv2.VideoWriter(output_all_file, codec, fps, frame_size)

    # 영상 폴더 지정 ------------------------------------------------ 김유민
    noramlize_check_size = 3
    fire_check  = deque(maxlen= noramlize_check_size) #영상 정확성? 체크
    smoke_check = deque(maxlen= noramlize_check_size) #영상 정확성? 체크
    frame_count = 0
    fire_check_name = 'fire'
    smoke_check_name = 'smoke'
    while cap.isOpened():
        frame_in_fire = 0 # 프레임에 워커가 있는지 확인
        frame_in_smoke = 0
        ret, frame = cap.read() # 영상 프레임 읽기
        if not ret: #영상 재생이 안될 경우 break
            break
        frame = cv2.resize(frame, frame_size)
        # 모델 실행 및 프레임 처리
        results = model.predict(frame,verbose = False, conf = 0.7)[0] # 모델을 예측함 ; 예측률 70% 이상이 아니면 예측 continue
        frame_predicted = results.plot(prob = False, conf = False) # model numpy로 가져옴 #model size와 같음
        
        now_time = datetime.now()
        ################## 영상 log 남김!! #########################
        arr = results.boxes.cls.cpu().numpy()
        if len(arr) > 0 :
            class_counts = np.vectorize(results.names.get)(arr)
            if fire_check_name in class_counts:
                frame_in_fire = fire_check_name
            if smoke_check_name in class_counts:
                frame_in_smoke = smoke_check_name

        fire_check.append(frame_in_fire)
        smoke_check.append(frame_in_smoke)

        if fire_check.count('fire') == noramlize_check_size:
            frame_in_fire = "fire"

        if smoke_check.count('smoke') == noramlize_check_size:
            frame_in_smoke = "smoke"

        # 화재 발생 감지 및 영상 저장 위치 지정
        if ((frame_in_smoke == "smoke") or (frame_in_fire == 'fire')) and (flag == 0) :

            flag = 1
            for label in class_counts:
                times_check = now_time.strftime('%Y-%m-%d %H:%M:%S')

                # 로그 파일 작성
                with open(text_log_path, "a") as file:
                        file.write(f"{times_check} {label}\n")
            

        all_video_writer.write(frame_predicted)

        _, jpeg_frame = cv2.imencode('.jpg', frame_predicted) # cv2.imshow가 안되기 때문에 대체하였음
        frame_bytes = jpeg_frame.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        

        if flag == 1:
            frame_count += 1
     
    all_video_writer.release()


# 국사 외부 영상 추출 ------------------------------------------------- !human 이근섭
##  model algorithm
def point_in_polygon(point, polygon):
    point = Point(point)
    polygon = Polygon(polygon)
    if polygon.contains(point):
        return "invade"
    else:
        return "person"
    
def generate_frames_external(video, model):
    
    log_directory = 'log/'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    # 영상 폴더 지정 ------------------------------------------------ 김유민
    number_human = 0 # 날짜 영상저장 번호        
    while os.path.exists(f'{settings.STATICFILES_DIRS[0]}/videoLog/human/{datetime.now().strftime("%Y-%m-%d")}/human-{datetime.now().strftime("%Y-%m-%d")}-{number_human}.mp4') :
        number_human+=1
        
    # 국사 외부 로그 경로 : 클래스-날짜-넘버.log
    text_log_path = log_directory + f'human-{datetime.now().strftime("%Y-%m-%d")}-{number_human}.log'
    
    cap = cv2.VideoCapture(video.temporary_file_path()) # 영상 지정
    frame_height = int(cap.get(4))
    frame_width = int(cap.get(3))
    
    # video writer 설정
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30.0
    frame_size = (640, 480)
    vid_num = 0
    flag = 0
    save_time = 5
    
    
    # 전체 영상 저장
    os.makedirs(f"{settings.STATICFILES_DIRS[0]}/videoLog/human/{datetime.now().strftime('%Y-%m-%d')}/", exist_ok= True)
    output_all_file = f"{settings.STATICFILES_DIRS[0]}/videoLog/human/{datetime.now().strftime('%Y-%m-%d')}/human-{datetime.now().strftime('%Y-%m-%d')}-{number_human}.mp4"
    all_video_writer = cv2.VideoWriter(output_all_file, codec, fps, frame_size)

    # 영상 폴더 지정 ------------------------------------------------ 김유민
    noramlize_check_size = 3
    invade_check = deque(maxlen= noramlize_check_size) #영상 정확성? 체크
    frame_count = 0
    while cap.isOpened():
        frame_check = 0
        frame_in_invade = 0 # 프레임에 invade가 있는지 확인
        ret, frame = cap.read() # 영상 프레임 읽기
        if not ret: #영상 재생이 안될 경우 break
                break
        frame = cv2.resize(frame, frame_size)
        frame_predicted = frame.copy()  # 원본 영상의 복사본 생성
        points = [(281, 426), (648, 210), (977, 226), (978, 477), (470, 713)]


        # 좌표 리사이즈
        resized_points = []
        for point in points:
            x = int(point[0] * frame_size[0] / frame_width)
            y = int(point[1] * frame_size[1] / frame_height)
            resized_points.append((x, y))
        points = resized_points

        # 다각형 그리기
        
        mask = np.zeros_like(frame_predicted[:, :, 0])
        points_arr = np.array(points)
        
        cv2.polylines(frame_predicted, [points_arr.astype(np.int32)], isClosed=True, color=(0, 0, 255), thickness=2)  # 다각형 테두리를 빨간색으로 그림


        # 모델 실행 및 프레임 처리
        # model inside
        results = model.predict(frame_predicted,verbose = False, conf = 0.7, classes = [0,1])[0] # 모델을 예측함 ; 예측률 70% 이상이 아니면 예측 continue
        boxes = results.boxes.cpu().numpy()

        if len(points) > 3:
            class_check = []
            for box in boxes:
                r = box.xyxy[0].astype(int)
                ct = box.xywh[0].astype(int)
                text_position = (r[0], r[1] - 10)
                class_name = point_in_polygon(ct[:2], points)
                cv2.rectangle(frame_predicted, r[:2], r[2:], (255, 255, 255), 2)
                cv2.putText(frame_predicted, class_name, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
                class_check.append(class_name)
            class_counts = Counter(class_check)

        now_time = datetime.now()

        # invade 확인
        if 'invade' in  class_counts:
            frame_in_invade = 'invade'

        invade_check.append(frame_in_invade)
        if invade_check.count('invade') == noramlize_check_size:
            frame_check = "invade"

        # 영상 저장 위치 지정
        if ('invade' == frame_check) and (flag == 0) :
            
            ################## 영상 log 남김!! #########################
            class_counts = {key: value for key, value in class_counts.items() if key != 'person'}
            for label, count in class_counts.items():
                times_check = now_time.strftime('%Y-%m-%d %H:%M:%S')
                
                # 로그 파일 작성
                with open(text_log_path, "a") as file:
                    file.write(f"{times_check} {label} {count}명\n")


        # 영상 저장 중..
        all_video_writer.write(frame_predicted)

        _, jpeg_frame = cv2.imencode('.jpg', frame_predicted) # cv2.imshow가 안되기 때문에 대체하였음
        frame_bytes = jpeg_frame.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        
        # 영상 저장
        if flag == 1:
            frame_count += 1    
    all_video_writer.release()
                
                
# 작업자 안전 영상 추출 ------------------------------------------------- !ppe 이근섭
def generate_frames_Work(video, model):
    
    log_directory = 'log/'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    # 영상 폴더 지정 ------------------------------------------------ 김유민
    number_ppe = 0 # 날짜 영상저장 번호        
    while os.path.exists(f'{settings.STATICFILES_DIRS[0]}/videoLog/ppe/{datetime.now().strftime("%Y-%m-%d")}/ppe-{datetime.now().strftime("%Y-%m-%d")}-{number_ppe}.mp4') :
        number_ppe+=1
        
    # 작업 안전 로그 경로 : 클래스-날짜-넘버.log
    text_log_path = log_directory + f'ppe-{datetime.now().strftime("%Y-%m-%d")}-{number_ppe}.log'
    
    cap = cv2.VideoCapture(video.temporary_file_path()) # 영상 지정
    frame_height = int(cap.get(4))
    frame_width = int(cap.get(3))

    # video writer 설정
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30.0
    frame_size = (640, 480)
    vid_num = 0
    flag = 0

    # 전체 영상 저장
    os.makedirs(f"{settings.STATICFILES_DIRS[0]}/videoLog/ppe/{datetime.now().strftime('%Y-%m-%d')}/", exist_ok= True)
    output_all_file = f"{settings.STATICFILES_DIRS[0]}/videoLog/ppe/{datetime.now().strftime('%Y-%m-%d')}/ppe-{datetime.now().strftime('%Y-%m-%d')}-{number_ppe}.mp4"
    all_video_writer = cv2.VideoWriter(output_all_file, codec, fps, frame_size)

    # 영상 정확성 체크 ------------------------------------------------ 김유민
    noramlize_check_size = 5
    W_check = deque(maxlen= noramlize_check_size) #영상 정확성? 체크
    WH_check = deque(maxlen= noramlize_check_size) #영상 정확성? 체크
    WV_check = deque(maxlen= noramlize_check_size) #영상 정확성? 체크
    frame_count = 0
    W_check_name = 'W'
    WH_check_name = 'WH'
    WV_check_name = 'WV'

    while cap.isOpened():
        frame_check_W = None
        frame_check_WH = 0
        frame_check_WV = 0
        frame_in_W = 0 # 프레임에 워커가 있는지 확인
        frame_in_WH = 0 # 프레임에 헬멧 착용한 워커가 있는지 확인
        frame_in_WV = 0 # 프레임에 조끼 착용한 워커가 있는지 확인

        ret, frame = cap.read() # 영상 프레임 읽기
        if not ret: #영상 재생이 안될 경우 break
            break
        frame = cv2.resize(frame, frame_size)
        # 모델 실행 및 프레임 처리
        results = model.predict(frame,verbose = False, iou = 0.7 )[0] # 모델을 예측함 ; 예측률 70% 이상이 아니면 예측 continue#conf = 0.7
        frame_predicted = results.plot(prob = False, conf = False) # model numpy로 가져옴 #model size와 같음
        

        ################## 영상 log 남김!! #########################
        now_time = datetime.now()
        arr = results.boxes.cls.cpu().numpy()
        if len(arr) > 0 :
            class_counts = np.vectorize(results.names.get)(arr)

            if W_check_name in class_counts:
                frame_in_W = W_check_name
            if WH_check_name in class_counts:
                frame_in_WH = WH_check_name
            if WV_check_name in class_counts:
                frame_in_WV = WV_check_name

        W_check.append(frame_in_W)
        WH_check.append(frame_in_WH)
        WV_check.append(frame_in_WV)

        if W_check.count('W') == noramlize_check_size:
            frame_check_W = "W"

        if W_check.count('WH') == noramlize_check_size:
            frame_check_WV = "WH"

        if W_check.count('WV') == noramlize_check_size:
            frame_check_WV = "WV"

        # 사건 발생 및 발생 영상 저장 위치 지정
        if ((frame_check_W== 'W') or (frame_check_WH == 'WH') or (frame_check_WV == 'WV')) and (flag == 0):
            for label in class_counts:
                
                times_check = now_time.strftime('%Y-%m-%d %H:%M:%S')

                # 로그 파일 작성
                with open(text_log_path, "a") as file:
                    file.write(f"{times_check} {label}\n")

            
        # 영상 저장 중..
        _, jpeg_frame = cv2.imencode('.jpg', frame_predicted) # cv2.imshow가 안되기 때문에 대체하였음
        frame_bytes = jpeg_frame.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')
        
        # 영상 저장
        if flag == 1:
            frame_count += 1    
    all_video_writer.release()
