# videoLog views
import os
from django.shortcuts import render
from django.conf import settings


def videoLog(request, pathes=''):
    base_dir = settings.STATICFILES_DIRS[0]
    base_dir = os.path.join(base_dir, 'videoLog')
    folder_path = os.path.join(base_dir, pathes)

    log_file_name = os.path.basename(pathes)
    log_file_name = log_file_name.split(".")[0]
    log_file_name = 'log/' + log_file_name + '.log'
    
    if os.path.isfile(folder_path):
        _, file_extension = os.path.splitext(folder_path)
        
        content = ''
        if file_extension.lower() == '.mp4':
            
            if os.path.isfile(log_file_name):
                    with open(log_file_name, 'r') as file:
                        content = file.read()
                        content = content.split('\n')
                        texts = []
                        for text in content :
                            tt = text.split(' ')

                            if len(tt) >= 4 :
                                day = tt[0]
                                time = tt[1]
                                fps = tt[2]
                                event = tt[3]
                                texts.append({'day':day,'event':event,'local':time ,'fps':round(int(fps)/24)})

            return render(request, 'videoLog/videoLogPlayer.html', { 'folder_path' : folder_path, 'content' : texts})
              

    else:
        file_list = []
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            is_dir = os.path.isdir(item_path)
            file_list.append({'name': item, 'is_dir': is_dir})
        return render(request, 'videoLog/videoLog.html', {'folder_path': pathes, 'file_list': file_list})
