from damp11113.network import tcp_receive, tcp_send
from playsound import playsound
from gtts import gTTS
from damp11113.file import removefile, readfile

print('ready')
def main():
    while True:
        try:
            print('waiting name, amount and message ...')
            name = tcp_receive('localhost', 4231)
            amount = tcp_receive('localhost', 4232)
            message = tcp_receive('localhost', 4233)
            print('waiting name, amount and message ...')
            if name == '' or amount == '' or message == '':
                continue
            else:
                print(name, amount, message)
                print('generating tts ...')
                tts = gTTS(text=message, lang='th')
                tts.save('message.mp3')
                print('playing tts ...')
                playsound('sfx.mp3')
                playsound('message.mp3')
                removefile('message.mp3')
                tcp_send('localhost', 4234, 'success')
        except Exception as e:
            tcp_send('localhost', 4234, str(e))

main()