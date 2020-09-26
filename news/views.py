from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
import pyttsx3
from . import apps
from django.contrib import auth
import pyrebase
from datetime import datetime, timezone, timedelta
from bs4 import NavigableString, Comment


def str_is_set(string):
    """
    Return False if string is empty True otherwise.
    """
    return string


def is_string(obj):
    """
    Returns True if obj is string False if not.
    """
    return not isinstance(obj, Comment) and isinstance(obj, NavigableString)


def to_utc(timestamp):
    return timestamp.astimezone(tz=timezone.utc)


def set_ist_zone(timestamp):
    timestamp.replace(
        tzinfo=timezone(timedelta(hours=5, minutes=30))
    )


def ist_to_utc(timestamp):
    set_ist_zone(timestamp)
    return to_utc(timestamp)


def remove_duplicate_entries(objects, key, prefer=None):
    """
    Return a new list of objects after removing all duplicate objects based on
    key. If prefer argument is provided, among duplicate objects, the one whose
    obj[prefer] giving False value is discarded
    """
    unique_set = set()

    def is_unique(obj):
        "Return False x[key] is present in set, True otherwise."
        if obj == None:
            return False
        if obj[key] not in unique_set:
            unique_set.add(obj[key])
            return True
        return False

    if prefer is None:
        return list(filter(is_unique, objects))

    preferred = {}
    for obj in objects:
        # obj[key] assumed always hashable
        prkey = obj[key]
        if preferred.get(prkey) is None:
            preferred[prkey] = obj
            continue
        if not preferred[prkey][prefer]:
            preferred[prkey] = obj

    return list(preferred.values())


def get_all_content(objects):
    """
    Call this function with a list of objects. Make sure there are no duplicate
    copies of an object else downloading might take long time.
    """

    def get_content(obj):
        from time import sleep
        sleep(0.7)
        response = requests.get(obj["link"])
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup.find_all("div",{ "class":"article-bnow-box"}):
                obj['location'] = tag.find_all("strong")[1]
                print(obj['location'])
            for tag in soup.find_all("article", {"class":"article-content-box first_big_character"}):
                for t in tag.find_all("p"):
                    obj['content'] = obj['content']+"\n" + t.get_text()
                    print(t.get_text())
            for tag in soup.find_all("div", {"class": "article-box"}):
                obj['title']=tag.find("h1").get_text()
            for tag in soup.find_all("div", {"class": "article-bimg"}):
                obj['image']=tag.find("img").get('src')
        return "NA"

    for obj in objects:
        get_content(obj)


def get_headline_details(obj):
    if (obj['href'][0] == '/'):
        obj['href'] = 'https://www.news18.com' + obj['href']
    try:
        return {
            "content": "",
            "link": obj["href"].split("?")[0],
            "scraped_at": datetime.utcnow().isoformat(),
            "time": None,
            "location": None,
            "source": "CNN-News18",
            "title": "",
            "image": None
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_chronological_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all("a", {"class": "vodeoiconb"}):
            tag.parent.decompose()
        for tag in soup.find_all("span", {"class": "video_icon_ss"}):
            tag.parent.parent.decompose()
        a_tags = (
                soup.find("div", {"class": "hotTopic"}).find_all("a") +
                soup.find("div", {"class": "blog-list"}).find_all("a")
        )
        headlines = remove_duplicate_entries(
            map(get_headline_details, a_tags),
            "link"
        )
        get_all_content(headlines)  # Fetch contents separately
        return headlines
    return None


def get_trending_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all("span", {"class": "video_icon_ss"}):
            tag.parent.parent.decompose()
        a_tags = soup.find("div", id="left").find("div", {
            "class": "flex-box"
        }).find_all("a")
        headlines = remove_duplicate_entries(
            map(get_headline_details, a_tags),
            "link"
        )
        return headlines
    return None


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
    # urlVar2 = "https://rb.gy/iz9zp8"
    urlVar2 = "https://www.news18.com/"
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
    toi_images = toi_soup.find_all('img')
    toi_headings = toi_headings[2:20]
    toi_images = toi_images[3:20]
    apps.toi_news = []
    apps.toi_news_images = []
    apps.ht_news_images = []

    apps.headlines.append('News from Times of India are as follows:')
    for th in toi_headings:
        apps.headlines.append(th.text)
        apps.toi_news.append(th.text)

    for ti in toi_images:
        if 'data-src' in ti.attrs:
            apps.toi_news_images.append(ti.attrs['data-src'])

    pages = 'https://www.news18.com/world/page-{}/'
    head2 = get_chronological_headlines(pages.format(1))
    for h in head2:
        for k in h.keys():
            print (k,h[k])

    headlines = get_trending_headlines(urlVar2)
    n18_h = []
    n18_img = []
    n18_content = []

    for h in head2:
        n18_h.append(h['title'])
        n18_img.append(h['image'])
        n18_content.append(h['content'])

    return render(req, 'news/index.html',{'range1': range(len(apps.toi_news_images)), 'range2': range(len(n18_h)), 'toi_news': apps.toi_news,'toi_news_images': apps.toi_news_images, 'n18_h': n18_h, 'n18_img': n18_img, 'n18_content': n18_content})


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
    return render(req, 'news/index.html',
                  {'name': "reading aloud...", 'toi_news': apps.toi_news, 'ht_news': apps.ht_news})


def stop(req):
    apps.flag = True
    return redirect('/')
