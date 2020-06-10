import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print('Lo escucho')
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print('Usted dijo: {}'.format(text))
    except:
        print('No se reconocio')
