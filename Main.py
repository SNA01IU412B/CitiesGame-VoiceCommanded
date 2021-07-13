from gtts import gTTS
import csv
import random
import time
import playsound
import speech_recognition as sr


def listen_me():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ваш город: ")
        audio = r.listen(source)
    # recognize speech using Google Speech Recognition
    try:
        our_speech = r.recognize_google(audio, language="ru")
        print(our_speech+"\n")
        if our_speech == "пока":
            say_message("До встречи")
            print("До встречи!")
            exit()
        return our_speech
    except sr.UnknownValueError:
        return "ошибка"
    except sr.RequestError:
        return "ошибка"


def town_last_letter(my):
     o = -1
     while my[o] == "ъ" or my[o] == "ё" or my[o] == "ь" or my[o] == "ы":
         o = o - 1
     last_letter = my[o].upper()
     return last_letter


def find_town(letter, data):
    found = []
    flag = 0
    for each in data:
        if each.find(letter) == 0:
            found.append(each)
            flag = 1
    if flag == 0:
        print("No such a town")
    return found


def say_message(message):
    voice = gTTS(message, lang="ru")
    file_voice_name = "audio_"+str(time.time())+"_"+str(random.randint(0,10000))+".mp3"
    voice.save(file_voice_name)
    playsound.playsound(file_voice_name)


def say_town(towns):
    answer = towns[random.randint(0, len(towns)-1)]
    say_message(answer)
    o = -1
    while answer[o] == "ъ" or answer[o] == "ё" or answer[o] == "ь" or answer[o] =="ы":
        o = o - 1
    new_letter = answer[o]
    print("Мой город:",answer,"\nВам на:",new_letter.upper())
    return new_letter.upper()


with open('city.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    adr = []
    cities = []
    for row in reader:
        adr.append(row[0])
    adr.pop(0)
    for each in adr:
        if each.find(",") != -1:
            a = each.find(",")
            part_city = each[a + 1:]
            while part_city.find(",") != -1:
                a = part_city.find(",")
                part_city = part_city[a+1:]
            n = part_city.find("г")
            while part_city[n+1] != " ":
                n = part_city.find("г", n+1)
            city = part_city[n+2:]
            cities.append(city)
        else:
            n = each.find("г")
            while each[n+1] != " ":
                n = each.find("г", n+1)
            city = each[n+2:]
            cities.append(city)
    print(cities)
    my_town = listen_me()
    my_letter = town_last_letter(my_town)
    town_found = find_town(my_letter, cities)
    comp_last_letter = say_town(town_found)
    while True:
        my_town = listen_me()
        f = 0
        if my_town[0] == comp_last_letter:
            for each in cities:
                if my_town == each:
                    my_letter = town_last_letter(my_town)
                    town_found = find_town(my_letter, cities)
                    comp_last_letter = say_town(town_found)
                    i = 0
                    while i < len(cities):
                        if cities[i] == town_found:
                            cities.pop(i)
                        if cities[i] == my_town:
                            cities.pop(i)
                    f = 1
            if f == 0:
                print("Нет такого города в России")
                say_message("Нет такого города в России")
        else:
            print("Не та буква")
            say_message("Не та буква")
