from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif
from sklearn import model_selection
from sklearn.externals import joblib
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

frase="en que plataforma sirve este bot"

def preprocess(X,y):
    ### test_size is the percentage of events assigned to the test set
    ### (remainder go into training)
    features_train, features_test, labels_train, labels_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=42)


   ### text vectorization--go from strings to lists of numbers
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
    features_train_transformed = vectorizer.fit_transform(features_train)
    features_test_transformed  = vectorizer.transform(features_test)
    joblib.dump(vectorizer, 'vectorizer_intent.pkl')

   ### feature selection, because text is super high dimensional and
    ### can be really computationally chewy as a result
    selector = SelectPercentile(f_classif, percentile=10)
    selector.fit(features_train_transformed, labels_train)
    joblib.dump(selector, 'selector_intent.pkl')
    features_train_transformed = selector.transform(features_train_transformed).toarray()
    features_test_transformed  = selector.transform(features_test_transformed).toarray()
    return features_train_transformed, features_test_transformed, labels_train, labels_test


def cleanPhrase(phrase):
    return phrase.replace("!","").replace(".","").replace(",","").replace(":","").lower()


def create_pkl_intent(new_phrase):
    with open("../preparacion_dataset/data_final_inflado_intencion.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    features = [cleanPhrase(frase[2:]) for frase in content]
    targets = [frase[0] for frase in content]
    features_train, features_test, labels_train, labels_test=preprocess(features,targets)
    lin_svc = svm.LinearSVC(C=100).fit(features_train, labels_train)
    print("svm acc: "+str(accuracy_score(labels_test, lin_svc.predict(features_test))))

    rfc = RandomForestClassifier(n_estimators=300).fit(features_train, labels_train)
    print("Random forest acc: "+str(accuracy_score(labels_test, rfc.predict(features_test))))

    vect = joblib.load("vectorizer_intent.pkl")
    select = joblib.load('selector_intent.pkl')
    features_transformed = vect.transform([new_phrase])
    features = select.transform(features_transformed).toarray()
    print(lin_svc.predict(features))

def intent(new_phrase):
    vect = joblib.load("vectorizer_intent.pkl")
    select = joblib.load('selector_intent.pkl')
    features_transformed = vect.transform([new_phrase])
    features = select.transform(features_transformed).toarray()

    #print(lin_svc.predict(features))


create_pkl_intent(frase)