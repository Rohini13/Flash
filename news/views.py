from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
import pyttsx3
from . import apps
from django.contrib import auth
import pyrebase

config = {
    'apiKey': "AIzaSyA7HJuzOo0HtJHZ7JZzv5yRszv7NjXNdps",
    'authDomain': "flash-94511.firebaseapp.com",
    'databaseURL': "https://flash-94511.firebaseio.com",
    'projectId': "flash-94511",
    'storageBucket': "flash-94511.appspot.com",
    'messagingSenderId': "72525595158",
    'appId': "1:72525595158:web:e642b67374c69b05f02b37",
    'measurementId': "G-5NQB6CC1JK"
}
firebase = pyrebase.initialize_app(config)
authenticate = firebase.auth()
database = firebase.database()


def signIn(request):
    return render(request, "news/signin.html")


def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authenticate.sign_in_with_email_and_password(email, password)
    except:
        message = "Invalid Credentials"
        return render(request, "news/signin.html", {"msg": message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    return render(request, "news/welcome.html", {"e": email})


def logout(request):
    auth.logout(request)
    return render(request, "news/signin.html")


def signUp(request):
    return render(request, "news/signup.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate.create_user_with_email_and_password(email, password)
    uid = user['localId']
    data = {"name": name, "status": "1"}
    database.child("users").child(uid).child("details").set(data)

    return render(request, "news/signin.html")


def index(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs"
    urlVar2 = "https://rb.gy/iz9zp8"
    title = "Recent Headlines"
    return display(req, urlVar, urlVar2, title)


def index1(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/world"
    urlVar2 = "https://rb.gy/al7v06"
    title = "World"
    return display(req, urlVar, urlVar2, title)


def index2(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/india"
    urlVar2 = "https://rb.gy/wasqbr"
    title = "Local"
    return display(req, urlVar, urlVar2, title)


def index3(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/gadgets"
    urlVar2 = "https://rb.gy/9r5k0w"
    title = "Science and Technology"
    return display(req, urlVar, urlVar2, title)


def index4(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/business"
    urlVar2 = "https://rb.gy/u5mivs"
    title = "Business and Economy"
    return display(req, urlVar, urlVar2, title)


def index5(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/lifestyle"
    urlVar2 = "https://rb.gy/ee2r4a"
    title = "Health and Lifestyle"
    return display(req, urlVar, urlVar2, title)


def index6(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/sports"
    urlVar2 = "https://rb.gy/nyv5as"
    title = "Sports"
    return display(req, urlVar, urlVar2, title)


def index7(req):
    urlVar = "https://timesofindia.indiatimes.com/briefs/entertainment"
    urlVar2 = "https://rb.gy/s78u6n"
    title = "Entertainment"
    return display(req, urlVar, urlVar2, title)


def display(req, urlVar, urlVar2, title):
    apps.idx = 0
    apps.headlines = []
    toi_r = requests.get(urlVar)
    toi_soup = BeautifulSoup(toi_r.content, 'html5lib')
    toi_headings = toi_soup.find_all('h2')
    toi_headings = toi_headings[3:20]
    apps.toi_news = []

    apps.headlines.append('News from Times of India are as follows:')
    for th in toi_headings:
        apps.headlines.append(th.text)
        apps.toi_news.append(th.text)

    # Getting news from Hindustan Times
    ht_r = requests.get(urlVar2)
    ht_soup = BeautifulSoup(ht_r.content, 'html5lib')
    ht_headings = ht_soup.findAll('h3')
    ht_headings = ht_headings[3:20]
    ht_news = []

    apps.headlines.append('News from Hindustan Times are as follows:')
    for hth in ht_headings:
        apps.headlines.append(hth.text)
        ht_news.append(hth.text)
    return render(req, 'news/index.html', {'name': title, 'toi_news': apps.toi_news, 'ht_news': ht_news})


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
    return render(req, 'news/index.html', {'name':"reading aloud...", 'toi_news': apps.toi_news, 'ht_news': apps.ht_news})


def stop(req):
    apps.flag = True
    return redirect('/')