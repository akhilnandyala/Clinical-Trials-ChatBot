# import pyaudio
# import speech_recognition as sr
#
# print(pyaudio.__version__)
# print(sr.__version__)
#
# r = sr.Recognizer()
#
# mic = sr.Microphone()
#
# print(sr.Microphone.list_microphone_names())
#
# with mic as source:
#     audio = r.listen(source)
#     print(r.recognize_google(audio))


# import speech_recognition as sr
#
# r = sr.Recognizer()
#
# with sr.Microphone() as source:
#     r.adjust_for_ambient_noise(source)
#     voice_data = r.record(source, duration=10)
#     text = r.recognize_google(voice_data, language='en')
#     print(text)