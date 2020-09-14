from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
import pyttsx3
from . import apps
from django.contrib import auth
import pyrebase
config ={

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
authe = firebase.auth()
database = firebase.database()
def signIn(request):

    return render(request,"news/signin.html")

def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('password')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message="Invalid Credentials"
        return render(request, "news/signin.html", {"msg": message})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    return render(request, "news/welcome.html", {"e":email})

def logout(request):
    auth.logout(request)
    return render(request, "news/signin.html")

def signUp(request):

    return render(request, "news/signup.html")

def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('password')

    user= authe.create_user_with_email_and_password(email, passw)
    uid = user['localId']
    data = {"name": name, "status": "1" }
    database.child("users").child(uid).child("details").set(data)

    return render(request, "news/signin.html")

headlines=[]
# Getting news from Times of India
toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
toi_soup = BeautifulSoup(toi_r.content, 'html5lib')
toi_headings = toi_soup.find_all('h2')
toi_headings = toi_headings[3:20]
toi_news = []

headlines.append('News from Times of India are as follows:')
for th in toi_headings:
    headlines.append(th.text)
    toi_news.append(th.text)

# Getting news from Hindustan Times
ht_r = requests.get("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pKVGlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen")
ht_soup = BeautifulSoup(ht_r.content, 'html5lib')
ht_headings = ht_soup.findAll('h3')
ht_headings = ht_headings[3:20]
ht_news = []

headlines.append('News from Hindustan Times are as follows:')
for hth in ht_headings:
    headlines.append(hth.text)
    ht_news.append(hth.text)


def index(req):
    return render(req, 'news/index.html', {'toi_news':toi_news, 'ht_news': ht_news})

def readAloud(req):
    engine = pyttsx3.init()
    end = len(headlines)
    start = apps.idx%end
    for i in range(start,end):
        if apps.flag:
            apps.idx=i%end
            break
        engine.say(headlines[i])
        engine.runAndWait()
    apps.flag=False
    return render(req, 'news/index.html', {'toi_news': toi_news, 'ht_news': ht_news})

def stop(req):
    apps.flag = True
    return redirect('/')

