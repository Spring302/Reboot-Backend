from gtts import gTTS
from django.http import HttpResponse

def text_to_sound(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        # Convert text to sound
        sound = gTTS(text)
        # Save sound to file
        sound_file = 'sound.mp3'
        sound.save(sound_file)
        # Return sound file as response
        with open(sound_file, 'rb') as f:
            response = HttpResponse(f.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="sound.mp3"'
            return response