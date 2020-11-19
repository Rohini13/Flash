from django.shortcuts import render, redirect
from multiprocessing import Pool
import os
from sys import path
import pyttsx3
from . import apps
import django
django.setup()
from django.contrib.auth.models import User
from .models import FlashUser, CategoryString, NewspaperString
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import pyttsx3
import speech_recognition as sr
import os
import multiprocessing

path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import news18_scraper as n18S
import toi_scraper as toiS
from dd_news_scraper import get_dd_articles
from ndtv_scraper import get_ndtv_articles
from sources import NEWS_SOURCES
import tele_scraper as teleS
from fake_news_predictor import predict


def speak(audio):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User said: ", query, "\n")

    except Exception as e:
        print(e)
        print("Unable to recognize your voice.")
        return "None"

    return query


def loading(request):
    return render(request, "news/loading_page.html")


def index(req):
    toiURL = NEWS_SOURCES["Times of India"]["home"]
    news18URL = NEWS_SOURCES["NEWS18"]["home"]
    ddnewsURL = NEWS_SOURCES["DD News"]["home"]
    ndtvURL = NEWS_SOURCES["NDTV"]["home"]
    teleURL = NEWS_SOURCES["Telegraph"]["home"]
    title = "Recent"
    return multithreadingFunc(req, toiURL, news18URL, ddnewsURL, ndtvURL, teleURL, title)


def index1(req):
    toiURL = NEWS_SOURCES["Times of India"]["world"]
    news18URL = NEWS_SOURCES["NEWS18"]["world"]
    ddnewsURL = NEWS_SOURCES["DD News"]["world"]
    ndtvURL = NEWS_SOURCES["NDTV"]["world"]
    teleURL = NEWS_SOURCES["Telegraph"]["world"]
    title = "World"
    return multithreadingFunc(req, toiURL, news18URL, ddnewsURL, ndtvURL, teleURL, title)


def index2(req):
    toiURL = NEWS_SOURCES["Times of India"]["local"]
    news18URL = NEWS_SOURCES["NEWS18"]["local"]
    ddnewsURL = NEWS_SOURCES["DD News"]["local"]
    ndtvURL = NEWS_SOURCES["NDTV"]["local"]
    teleURL = NEWS_SOURCES["Telegraph"]["local"]
    title = "India"
    return multithreadingFunc(req, toiURL, news18URL, ddnewsURL, ndtvURL, teleURL, title)


def index3(req):
    toiURL = NEWS_SOURCES["Times of India"]["technology"]
    news18URL = NEWS_SOURCES["NEWS18"]["technology"]
    ddnewsURL = NEWS_SOURCES["DD News"]["technology"]
    ndtvURL = NEWS_SOURCES["NDTV"]["technology"]
    teleURL = NEWS_SOURCES["Telegraph"]["technology"]
    title = "Science"
    return multithreadingFunc(req, toiURL, news18URL, ddnewsURL, ndtvURL, teleURL, title)


def index4(req):
    toiURL = NEWS_SOURCES["Times of India"]["business"]
    news18URL = NEWS_SOURCES["NEWS18"]["business"]
    ddnewsURL = NEWS_SOURCES["DD News"]["business"]
    ndtvURL = NEWS_SOURCES["NDTV"]["business"]
    teleURL = NEWS_SOURCES["Telegraph"]["business"]
    title = "Economy"
    return multithreadingFunc(req, toiURL, news18URL, ddnewsURL, ndtvURL, teleURL, title)


def index5(req):
    toiURL = NEWS_SOURCES["Times of India"]["health"]
    news18URL = NEWS_SOURCES["NEWS18"]["health"]
    ddnewsURL = NEWS_SOURCES["DD News"]["health"]
    ndtvURL = NEWS_SOURCES["NDTV"]["health"]
    teleURL = NEWS_SOURCES["Telegraph"]["health"]
    title = "Health"
    return multithreadingFunc(req, toiURL, news18URL, ddnewsURL, ndtvURL, teleURL, title)


def index6(req):
    toiURL = NEWS_SOURCES["Times of India"]["sports"]
    news18URL = NEWS_SOURCES["NEWS18"]["sports"]
    ddnewsURL = NEWS_SOURCES["DD News"]["sports"]
    ndtvURL = NEWS_SOURCES["NDTV"]["sports"]
    teleURL = NEWS_SOURCES["Telegraph"]["sports"]
    title = "Sports"
    print('here')
    return multithreadingFunc(req, toiURL, news18URL, ddnewsURL, ndtvURL, teleURL, title)


def index7(req):
    toiURL = NEWS_SOURCES["Times of India"]["entertainment"]
    news18URL = NEWS_SOURCES["NEWS18"]["entertainment"]
    ddnewsURL = NEWS_SOURCES["DD News"]["entertainment"]
    ndtvURL = NEWS_SOURCES["NDTV"]["entertainment"]
    teleURL = NEWS_SOURCES["Telegraph"]["entertainment"]
    title = "Entertainment"
    return multithreadingFunc(req, toiURL, news18URL, ddnewsURL, ndtvURL, teleURL, title)


def multithreadingFunc(req, toiURL, news18URL, ddnewsURL, ndtvURL, teleURL, title):
    all_urls = [news18URL, teleURL,  ndtvURL, toiURL]
    p = Pool(4)
    apps.all_data = p.map(display2, all_urls)
    p.terminate()
    p.join()
    num = 99999
    flag = False
    if req.user.is_authenticated is True:
        flag = True
        num = req.user.id
        return render(req, 'news/home_alt.html', {'num': num, 'title': title,'news' : apps.all_data, 'logged_in': flag, 'user': req.user})
    else:
        return render(req, 'news/home_alt.html', {'num': num, 'title': title,'news' : apps.all_data, 'logged_in': flag})


def display2(url):
    if url.find('news18') != -1:
        n18_news = n18S.get_articles(url.format(1))
        if(n18_news!=None):
            for n in n18_news:
                if n["content"] == "" or n["title"] == "" or n["image"] == None:
                    n18_news.remove(n)
        else:
            print("None")
        print("news 18 done")
        return n18_news

    if url.find('telegraphindia') != -1:
        tele_news = teleS.get_articles(url.format(1))
        print("telegraph done")
        return tele_news

    if url.find('timesofindia') != -1:
        toi_news = toiS.get_articles(url)
        for t in toi_news:
            if t["content"] == "":
                toi_news.remove(t)
        print("toi done")
        return toi_news

    if url.find('ndtv') != -1:
        ndtv_news = get_ndtv_articles(url.format(1))
        for ndtv in ndtv_news:
            if ndtv["content"] == "":
                ndtv_news.remove(ndtv)
        print("ndtv done")
        return ndtv_news

    if url.find('ddnews') != -1:
        dd_news = get_dd_articles(url.format(1))
        for dd in dd_news:
            if dd["link"] == "#":
                dd_news.remove(dd)
            if dd["content"] == "":
                dd_news.remove(dd)
        print("dd news done")
        return dd_news


def details(req, newsid, articleid):
    article = apps.all_data[newsid][articleid]
    flag = False
    num = 99999
    if req.user.is_authenticated is True:
        flag = True
        num = req.user.id
    return render(req, 'news/single_page.html', {'num': num, 'logged_in': flag, 'article': article, 'all_articles': apps.all_data, 'newsid': newsid, 'articleid': articleid})


def developers(req):
    flag = False
    num = 99999
    if req.user.is_authenticated is True:
        flag = True
        num = req.user.id
    return render(req, 'news/developers.html', {'num': num, 'logged_in': flag})


def detect_fake_news(req):
    result = predict(req.POST['input_text'])
    content = req.POST['input_text']
    flag = False
    num = 99999
    if req.user.is_authenticated is True:
        flag = True
        num = req.user.id
    return render(req, 'news/fake_news.html',{'num': num, 'result':result[0], 'content':content, 'logged_in': flag})


@login_required(login_url='login')
def for_you(req, user_id):
    user = User.objects.get(pk=user_id)
    flashuser = FlashUser.objects.get(user=user)
    all_urls = list()
    for cat in flashuser.categories.all():
        for np in flashuser.newspapers.all():
            all_urls.append(NEWS_SOURCES[np.newspaper_obj][cat.category_obj])
    p = Pool(len(all_urls))
    apps.all_data = p.map(display2, all_urls)
    p.terminate()
    p.join()
    return render(req, 'news/for_you.html', {'num': req.user.id, 'news': apps.all_data, 'user': req.user})


def loginFunction(req):

    if req.method == "GET":
        return render(req, 'news/login.html', {'num': 99999})

    if req.method == "POST":
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect('for_you', user.id)
        else:
            return render(req, 'news/login.html', {'num': 99999})


def register(req):

    if req.method == "GET":
        return render(req, 'news/register.html', {'num': 99999})

    if req.method == "POST":
        if req.POST['password'] != req.POST['confirm_password']:
            return redirect('register')
        username = req.POST['username']
        password = req.POST['password']
        category_list = req.POST.getlist('category')
        newspaper_list = req.POST.getlist('newspaper')
        user = User.objects.create_user(username=username,password=password)
        user.save()
        flashuser = FlashUser.objects.create(user=user)
        for cat in category_list:
            obj = CategoryString.objects.get(category_obj=cat)
            flashuser.categories.add(obj)
        for newspaper in newspaper_list:
            obj = NewspaperString.objects.get(newspaper_obj=newspaper)
            flashuser.newspapers.add(obj)
        flashuser.save()
        return redirect('for_you', user.id)


@login_required(login_url='login')
def logoutFunction(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def edit_profile(req, user_id):
    if req.user.id != user_id:
        redirect('edit_profile', req.user.id)
    user = User.objects.get(pk=user_id)
    flashuser = FlashUser.objects.get(user=user)
    flag = {'local': False, 'health': False, 'business': False, 'entertainment': False, 'sports': False, 'world': False, 'technology': False, 'NEWS18': False, 'Times of India': False, 'NDTV': False, 'Telegraph': False}
    for cat in flashuser.categories.all():
        flag[cat.category_obj] = True
    for newspaper in flashuser.newspapers.all():
        flag[newspaper.newspaper_obj] = True
    flag2 = list(flag.values())
    return render(req, 'news/edit_profile.html', {'flashuser': flashuser, 'num': user_id, 'flag': flag2})


@login_required(login_url='login')
def changeUsername(req, user_id):
    if req.user.id != user_id:
        return redirect('edit_profile', req.user.id)
    user = User.objects.get(pk=user_id)
    flashuser = FlashUser.objects.get(user=user)
    user.username = req.POST['username']
    user.save()
    flashuser.user = user
    flashuser.save()
    return redirect('edit_profile', user_id)


@login_required(login_url='login')
def changePassword(req, user_id):
    if req.user.id != user_id:
        return redirect('edit_profile', req.user.id)
    if req.POST['password'] != req.POST['confirm_password']:
        return redirect('edit_profile', req.user.id)
    user = User.objects.get(pk=user_id)
    flashuser = FlashUser.objects.get(user=user)
    user.set_password(req.POST['password'])
    user.save()
    update_session_auth_hash(req, user)
    flashuser.user = user
    flashuser.save()
    return redirect('edit_profile', user_id)


@login_required(login_url='login')
def changeCategories(req, user_id):
    if req.user.id != user_id:
        return redirect('edit_profile', req.user.id)
    user = User.objects.get(pk=user_id)
    flashuser = FlashUser.objects.get(user=user)
    category_list = req.POST.getlist('category')
    flashuser.categories.all().delete()
    for cat in category_list:
        print(cat)
        obj = CategoryString.objects.get(category_obj=cat)
        flashuser.categories.add(obj)
    flashuser.save()
    return redirect('edit_profile', user_id)


@login_required(login_url='login')
def changeNewspapers(req, user_id):
    if req.user.id != user_id:
        return redirect('edit_profile', req.user.id)
    user = User.objects.get(pk=user_id)
    flashuser = FlashUser.objects.get(user=user)
    newspaper_list = req.POST.getlist('newspaper')
    flashuser.newspapers.all().delete()
    for newspaper in newspaper_list:
        obj = NewspaperString.objects.get(newspaper_obj=newspaper)
        flashuser.newspapers.add(obj)
    flashuser.save()
    return redirect('edit_profile', user_id)


def voice_command1(req):
    clear = lambda: os.system('cls')
    clear()
    speak('What can I do for you?')
    query = takeCommand().lower()
    if 'local' in query:
        speak('Directing to the local category')
        return redirect('index2')
    elif 'world' in query:
        speak('Directing to the world category')
        return redirect('index1')
    elif 'entertainment' in query:
        speak('Directing to the entertainment category')
        return redirect('index7')
    elif 'sports' in query:
        speak('Directing to the sports category')
        return redirect('index6')
    elif 'health' in query or 'lifestyle' in query:
        speak('Directing to the health and lifestyle category')
        return redirect('index5')
    elif 'business' in query or 'economy' in query:
        speak('Directing to the economy and business category')
        return redirect('index4')
    elif 'technology' in query or 'science' in query:
        speak('Directing to the science and technology category')
        return redirect('index3')
    elif 'home' in query or 'main' in query:
        speak('Directing to the main page')
        return redirect('index')
    elif 'read' in query:
        speak('to make me read an article, click on the read aloud button after expanding it')
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    elif 'for you' in query or 'for me' in query or 'my news' in query:
        if req.user.is_authenticated:
            speak('Directing to the news for you')
            return redirect('for_you', req.user.id)
        else:
            speak('You would need to login first')
            return redirect('login')
    elif 'login' in query or 'log in' in query or 'sign in' in query:
        speak('Taking you to the login page')
        return redirect('login')
    elif 'register' in query or 'sign up' in query:
        speak('Taking you to the register page')
        return redirect('register')
    elif 'logout' in query or 'log out' in query or 'sign out' in query:
        if req.user.is_authenticated:
            speak('Logging out')
            return redirect('logout')
        else:
            speak('You would need to login first')
            return redirect('login')
    elif 'edit profile' in query or 'edit my profile' or 'change profile' in query or 'change my profile' in query:
        if req.user.is_authenticated:
            speak('Taking you to the edit profile page')
            return redirect('edit_profile', req.user.id)
        else:
            speak('You would need to login first')
            return redirect('login')
    else:
        speak('Sorry, I could not understand')
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


def read(newsid, articleid, all_data):
    print(all_data)
    article = all_data[newsid][articleid]
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say("Reading the article for you. To make me stop, click on the stop button.")
    engine.runAndWait()
    engine.say(article['content'])
    engine.runAndWait()


def readAloud(req, newsid, articleid):
    apps.t = multiprocessing.Process(target=read, args=(newsid, articleid, apps.all_data))
    apps.t.start()
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


def stop(req):
    if apps.t is not None:
        apps.t.terminate()
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


def about(req):
    num = 99999
    flag = False
    if req.user.is_authenticated is True:
        num = req.user.id
        flag = True
    return render(req, 'news/about_us.html', {'num': num, 'flag': flag})