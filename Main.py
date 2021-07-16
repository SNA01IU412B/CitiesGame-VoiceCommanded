from gtts import gTTS
import csv
import random
import time
import playsound
import speech_recognition as sr
import os


def import_list_from(file):
    f = open(file, 'r', encoding='utf-8')
    reader = csv.reader(f)
    list = []
    for item in reader:
        list.append(item[0])
    return list


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


def town_to_blacklist(black_list, town):
    black_list.append(town)
    return black_list


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


def listen_me(black_list, city_list):
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
        while check_if_inlist(black_list, my_speech) == 1:
            check_for_endgame(city_list, black_list, my_speech[0])
            print(my_speech, "уже называли")
            say_message("уже называли")
            print("Нажмите Enter и назовите город")
            k = input()
            my_speech = listen_me(black_list, city_list)
            print(my_speech)
        my_speech[0].upper()
        return my_speech
    except sr.UnknownValueError:
        return "ошибка"
    except sr.RequestError:
        return "ошибка"


def town_last_letter(black_list, my):
     o = -1
     if check_if_inlist(black_list, "йошкар-ола") == 1:
         if my[o] == "й":
             o = o - 1
     while my[o] == "ъ" or my[o] == "ё" or my[o] == "ь" or my[o] == "ы":
         o = o - 1
         if check_if_inlist(black_list, "йошкар-ола") == 1:
             if my[o] == "й":
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


def main():
    cities_list = []
    print("В какие города сыграем?\n"
                "1-Русские\n"
                "2-Мировые")
    say_message("В какие города сыграем?")
    u = input()
    while u != "1" and u != "2":
        print("Не смешно")
        say_message("Не смешно")
        u = input()
    if u == "1":
        cities_list = import_list_from('rus_cities.csv')
    elif u == "2":
        cities_list = import_list_from('wold_cities.csv')
    else:
        print("Ошибка чтения")
        exit()
    blacklist = []
    #print(cities_list)
    print("Нажмите Enter и назовите город")
    k = input()
    my_town = listen_me(blacklist, cities_list)
    blacklist = town_to_blacklist(black_list=blacklist, town=my_town)
    my_letter = town_last_letter(blacklist, my_town)
    town_found = find_town(my_letter, cities_list, blacklist)
    blacklist = town_to_blacklist(black_list=blacklist, town=town_found)
    comp_last_letter = say_town(town_found)
    while True:
        print("Нажмите Enter и назовите город")
        k = input()
        my_town = listen_me(blacklist, cities_list)
        blacklist = town_to_blacklist(black_list=blacklist, town=my_town)
        f = 0
        if my_town[0].upper() == comp_last_letter:
            if check_if_inlist(cities_list, my_town) == 1:
                my_letter = town_last_letter(blacklist, my_town)
                town_found = find_town(my_letter, cities_list, blacklist)
                blacklist = town_to_blacklist(black_list=blacklist, town=town_found)
                comp_last_letter = say_town(town_found)
            else:
                print("Нет такого города в России")
                say_message("Нет такого города в России")
        else:
            print("Не та буква, вам на: ", comp_last_letter)
            say_message("Не та буква")


if __name__ == "__main__":
    main()
