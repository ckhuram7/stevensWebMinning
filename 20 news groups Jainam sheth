from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from nltk.corpus import stopwords
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
import os

'''
ADD PREDICT LABEL GRIDSEARCH FUNCTION
COMPARE WITH ADD_LABEL OUTPUT TO GET ACCURACY
'''

def add_label(path):
    if "comp" in path:
        return("comp")
    elif "sport" in path:
        return("sport")
    elif "rec" in path:
        return("rec")
    elif "politics" in path:
        return("politics")
    
def runtrain(path):
    review=[]
    lable=[]
    for folder in train_set:
        for filename in os.listdir(path+"/"+folder):
            file_contents=open(path+"/"+folder+"/"+filename, 'rt').read()
            first,rest=file_contents.split('\n\n',1)
            review.append(rest.strip().replace('\t',''))
            lab=add_label(folder)
            lable.append(lab)
    print(len(review))
    print(len(lable))
    return review,lable

def runtest(path):
    review=[]
    lable=[]
    for folder in test_set:
        for filename in os.listdir(path+"/"+folder):
            file_contents=open(path+"/"+folder+"/"+filename, 'rt').read()
            first,rest=file_contents.split('\n\n',1)
            review.append(rest.strip().replace('\t',''))
            lab=add_label(folder)
            lable.append(lab)
    print(len(review))
    print(len(lable))
    return review,lable



base_path=(r"C:\Users\Jainam Sheth\Downloads\BIA 660\20_newsgroups")
test_set=["comp.windows.x","rec.sport.baseball","talk.politics.misc","rec.autos"]
not_req=["comp.graphics","alt.atheism","comp.sys.ibm.pc.hardware","misc.forsale","comp.sys.mac.hardware","sci.crypt","sci.electronics","sci.med","sci.space","soc.religion.christian","talk.religion.misc"]
train_set=["comp.os.ms-windows.misc","rec.motorcycles","rec.sport.hockey","talk.politics.guns","talk.politics.mideast"]


rev_train,labels_train=runtrain(r"C:\Users\Jainam Sheth\Downloads\BIA 660\20_newsgroups")
rev_test,labels_test=runtest(r"C:\Users\Jainam Sheth\Downloads\BIA 660\20_newsgroups")


counter = CountVectorizer(stop_words=stopwords.words('english'))
counter.fit(rev_train)
#count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(rev_train)#transform the training data
counts_test = counter.transform(rev_test)
##clf=LogisticRegression()##74.87
##clf=MLPClassifier(hidden_layer_sizes=(15,),random_state=9)##85.175
clf=MLPClassifier()##85.175
##clf=SVC()##
##clf=RandomForestClassifier()
##clf=SVC(kernel="linear",C=0.25,random_state=101)##71.35
##clf=SGDClassifier(loss='modified_huber',random_state=101)##73.15
##clf=RandomForestClassifier()
clf.fit(counts_train,labels_train)#use hard voting to predict (majority voting)
pred=clf.predict(counts_test)#print accuracy
print (accuracy_score(pred,labels_test))
