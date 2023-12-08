import os
import re

import moviepy.editor as mp
import pytube
from django.shortcuts import render


# defining function
def index(request):

    # checking whether request.method is post or not
    if request.method == 'POST':

        # getting link from frontend
        link = request.POST['link']
        video = pytube.YouTube(link)

        video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()  # noqa
        print('Baixado com sucesso')
        for file in os.listdir():
            if re.search('mp4', file):
                mp4_path = os.path.join(file)
                mp3_path = os.path.join(os.path.splitext(file)[0]+'.mp3')
                new_file = mp.AudioFileClip(mp4_path)
                new_file.write_audiofile(mp3_path)
                os.remove(mp4_path)

        # returning HTML page
        return render(request, 'index.html')
    return render(request, 'index.html')
