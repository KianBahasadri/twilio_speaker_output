from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
import subprocess
import time
import yt_dlp
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

@app.get('/')
def record_xml():
    return FileResponse('record.xml')

@app.get('/recording')
def download_recording(RecordingUrl):
    print(f"RecordingUrl:\n{RecordingUrl}")
    time.sleep(2)
    subprocess.run(['ffmpeg', '-i', RecordingUrl, '-f', 'alsa', 'default'])
    
@app.get('/sms')
def sms_reply(Body):
    resp = MessagingResponse()
    if 'http' not in Body:
        resp.message("Send a link to any video like youtube or reddit and it will play for kian")
        return Response(str(resp), media_type="text/xml")

    try: 
        with yt_dlp.YoutubeDL({}) as ydl:
            info = ydl.extract_info(Body, download=False)
            for f in info['formats'][::-1]:
                if 'audio' in f['format']:
                    url = f['url']
                    break
    except:
        resp.message("there was an error parsing the link you sent :(")
        return Response(str(resp), media_type="text/xml")
    
    try:
        subprocess.run(['ffmpeg', '-i', url, '-f', 'alsa', 'default'])
    except:
        resp.message("there was an error during audio playback of the file")
        return Response(str(resp), media_type="text/xml")

    resp.message("You trolled kian, I hope you're proud of yourself, what did you gain?")
    return Response(str(resp), media_type="text/xml")

