from gtts import gTTS
import csv
import random
import time
import playsound
import speech_recognition as sr
import os


def find_all_by_first_letter(full_list, f_letter):
    i = 0
    f_letter.upper()
    found_list = []
    while i < len(full_list):
        if full_list[i][0] == f_letter:
            found_list.append(full_list[i])
        i = i + 1
    return found_list


def say_message(message):
    voice = gTTS(message, lang="ru")
    file_voice_name = "audio_"+str(time.time())+"_"+str(random.randint(0,10000))+".mp3"
    voice.save(file_voice_name)
    playsound.playsound(file_voice_name)
    os.remove(file_voice_name)


def say_town(town):
    answer = town
    say_message(answer)
    o = -1
    while answer[o] == "ъ" or answer[o] == "ё" or answer[o] == "ь" or answer[o] =="ы":
        o = o - 1
    new_letter = answer[o]
    print("Мой город:", answer, "\nВам на:", new_letter.upper())
    return new_letter.upper()


def town_to_blacklist(blacklist, town):
    blacklist.append(town)
    return blacklist


def check_if_inlist(list, town):
    i = 0
    flag = 0
    while i < len(list):
        if list[i] == town:
            flag = 1
            return 1
        else:
            i = i + 1
    if flag == 0:
        return 0


def check_for_endgame(city_list, black_list, letter_check):
    black_part = find_all_by_first_letter(black_list, letter_check)
    city_part = find_all_by_first_letter(city_list, letter_check)
    if black_part == city_part:
        print("Слова на эту букву кончились, игра окончена")
        say_message("Слова на эту букву кончились, игра окончена")
        exit()


def listen_me(black, citylist):
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ваш город: ")
        audio = r.listen(source)
    # recognize speech using Google Speech Recognition
    try:
        my_speech = r.recognize_google(audio, language="ru")
        print(my_speech+"\n")
        if my_speech == "пока":
            say_message("До встречи")
            print("До встречи!")
            exit()
        my_speech[0].upper()
        while check_if_inlist(black, my_speech) == 1:
            check_for_endgame(citylist, black, my_speech[0])
            print(my_speech, "уже называли")
            say_message("уже называли")
            my_speech = listen_me(black, citylist)
            print(my_speech)
        my_speech[0].upper()
        return my_speech
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


def find_town(letter, data, blacklist):
    towns_found = []
    flag = 0
    for each in data:
        if each.find(letter) == 0:
            if check_if_inlist(blacklist, each) == 0:
                towns_found.append(each)
                flag = 1
    if flag == 0:
        print("Города на эту букву кончились, конец игры")
        say_message("Города на эту букву кончились, конец игры")
        exit()
    c = random.randint(0, len(towns_found)-1)
    found = towns_found[c]
    return found


with open('city.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    adr = []
    cities = []
    blacklist = []
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
    p = 0
    while p < len(cities)-1:
        if cities[p].find("Йошкар-Ола") != -1:
            cities[p] = "Йошкар-ола"
        if cities[p].find("пгт") != -1:
            cities[p] = each[4:]
        p = p + 1
    print(cities)
    my_town = listen_me(blacklist, cities)
    blacklist = town_to_blacklist(blacklist=blacklist, town=my_town)
    my_letter = town_last_letter(my_town)
    town_found = find_town(my_letter, cities, blacklist)
    blacklist = town_to_blacklist(blacklist=blacklist, town=town_found)
    comp_last_letter = say_town(town_found)
    while True:
        my_town = listen_me(blacklist, cities)
        blacklist = town_to_blacklist(blacklist=blacklist, town=my_town)
        f = 0
        if my_town[0].upper() == comp_last_letter:
            if check_if_inlist(cities, my_town) == 1:
                my_letter = town_last_letter(my_town)
                town_found = find_town(my_letter, cities, blacklist)
                comp_last_letter = say_town(town_found)
            else:
                say_message("Нет такого города в России")
        else:
            print("Не та буква")
            say_message("Не та буква")
