# videoLog views
import os
from django.shortcuts import render
from django.conf import settings

def videoLog(request, pathes=''):
    base_dir = settings.BASE_DIR
    log_folder_path = os.path.join(base_dir, 'log')
    folder_path = os.path.join(log_folder_path, pathes)
    
    if os.path.isfile(folder_path):
        with open(folder_path, 'r') as file:
            content = file.read()
        return render(request, 'videoLog/videoTextLog.html', {'content': content})
    else:
        file_list = []
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            is_dir = os.path.isdir(item_path)
            file_list.append({'name': item, 'is_dir': is_dir})
        return render(request, 'videoLog/videoTextLog.html', {'folder_path': pathes, 'file_list': file_list})


def videoPlayerLog(request, pathes=''):
    base_dir = settings.STATICFILES_DIRS[0]
    base_dir = os.path.join(base_dir, 'videoLog')
    folder_path = os.path.join(base_dir, pathes)
    
    if os.path.isfile(folder_path):
        _, file_extension = os.path.splitext(folder_path)
        if file_extension.lower() == '.mp4':
            print()
            print('folder_path : ',folder_path)
            print()
            return render(request, 'videoLog/videoLogPlayer.html', { 'folder_path' : folder_path})

    else:
        file_list = []
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            is_dir = os.path.isdir(item_path)
            file_list.append({'name': item, 'is_dir': is_dir})
        return render(request, 'videoLog/videoLog.html', {'folder_path': pathes, 'file_list': file_list})
