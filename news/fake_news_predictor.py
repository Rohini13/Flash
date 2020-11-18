import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from django.contrib.staticfiles import finders


def predict(input):
    csv_path = finders.find('news/fake_or_real_news.csv')
    df = pd.read_csv(csv_path)
    df = df.set_index("Unnamed: 0")
    y = df.label
    df.drop("label", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(df['text'], y, test_size=0.33, random_state=53)
    count_vectorizer = CountVectorizer(stop_words='english')
    count_train = count_vectorizer.fit_transform(X_train)
    clf = MultinomialNB()
    clf.fit(count_train, y_train)
    new_input = [['x','x','x'],['x', input,'x']]
    df2 = pd.DataFrame(new_input, columns=['title','text','label'])
    y=df2.label
    df2.drop("label", axis=1)
    A, B, C, D = train_test_split(df2['text'], y, test_size=0.5,shuffle=False)
    temp = count_vectorizer.transform(B)
    new_output = clf.predict(temp)
    return new_output
