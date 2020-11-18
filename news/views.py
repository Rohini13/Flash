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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import news18_scraper as n18S
import toi_scraper as toiS
from dd_news_scraper import get_dd_articles
from ndtv_scraper import get_ndtv_articles
from sources import NEWS_SOURCES
import tele_scraper as teleS
from fake_news_predictor import predict


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


def readAloud(req):
    engine = pyttsx3.init()
    end = len(apps.headlines)
    start = apps.idx % end
    for i in range(start, end):
        if apps.flag:
            apps.idx = i % end
            break
        engine.say(apps.headlines[i])
        engine.runAndWait()
    apps.flag = False
    return render(req, 'news/home_alt.html',
    {'title': "Reading aloud...", 'toi_news': apps.toi_news, 'ht_news': apps.ht_news})


def stop(req):
    apps.flag = True
    return redirect('/')


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