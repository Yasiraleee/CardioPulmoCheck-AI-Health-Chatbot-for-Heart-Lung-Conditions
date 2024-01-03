import spacy
import pickle
#import speech_recognition as sr
from flask import Flask,render_template,request,url_for,flash,json
nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

@app.route("/")
def Index():
    return render_template("index.html")
@app.route("/HealthCheckup")
def HealthCheckup():
    return render_template("HealthCheckup.html")
@app.route("/Help")
def Help():
    return render_template("Help.html")
@app.route("/Contact")
def Contact():
    return render_template("Contact.html")


attributes_dict = {
    'AGE': None,
    'HighBP': None,
    'HighChol': None,
    'Stroke': None,
    'Diabetes': None,
    'PhysActivity': None,
    'GenHlth': None,
    'PhysHlth': None,
    'DiffWalk': None,
    'GENDER': None,
    'SMOKING': None,
    'YELLOW_FINGERS': None,
    'SHORTNESS OF BREATH': None,
    'WHEEZING': None,
    'ALLERGY ': None,
    'SWALLOWING DIFFICULTY': None,
    'COUGHING': None,
    'ALCOHOL CONSUMING': None
}
questions = {
    'AGE': 'What is your Age?',
    'HighBP': 'Are you having HighBP?',
    'HighChol': 'Are you having HighChol?',
    'Stroke':'Are you facing Strokes?',
    'Diabetes': 'Do you have Diabetes?',
    'PhysActivity': 'Do You Walk regulary enough?',
    'GenHlth': 'Your Mental Health in 1-5 range?',
    'PhysHlth': 'Your Physical Health in 1-30 range?',
    'DiffWalk': 'Do you face Difficulty in Walking?',
    'SMOKING':'Are you a Smoker?',
    'YELLOW_FINGERS': 'Do you have Yellow Fingers?',
    'SHORTNESS OF BREATH': 'Are you facing Shortness of Breath?',
    'WHEEZING': 'Do you have Wheezing?',
    'ALLERGY ': 'Are you Allergic to dust?',
    'SWALLOWING DIFFICULTY': 'Are you facing any Swallowing Difficulty?',
    'COUGHING': 'Do you have Cough?',
    'ALCOHOL CONSUMING': 'Do you drink Alcohol?',
    'sample':'Are You Having A Good Day?'
}
order_list_1 = ['GENDER','AGE','SMOKING','YELLOW_FINGERS','ALLERGY ','WHEEZING','ALCOHOL CONSUMING','COUGHING','SHORTNESS OF BREATH','SWALLOWING DIFFICULTY']
order_list_2 = ['HighBP', 'HighChol', 'Stroke', 'Diabetes', 'PhysActivity', 'GenHlth', 'PhysHlth', 'DiffWalk', 'GENDER', 'AGE']
def create_list(dictionary, order_keys):
    result_list = [[dictionary[key] for key in order_keys if key in dictionary]]
    return result_list

values_iterator = iter(questions.values())
key_iterator = iter(questions.keys())
answers = []
ind = -1
score=0
score1=0
gender=1


@app.route('/api/DataInput', methods=['POST'])
def DataInput():
    global score
    global score1
    global ind
    global gender
    data = request.get_json()
    O_Msg = data["sentence"]
    doc = nlp(O_Msg)
    if ind==-1:
        for token in doc:
            if token.text=="male":
                gender=1
            else:
                gender=0

    if attributes_dict["ALCOHOL CONSUMING"]!= None:
        lung = create_list(attributes_dict, order_list_1)
        heart = create_list(attributes_dict, order_list_2)
        lung[0][0] = gender
        heart[0][8] = gender
        print(lung)
        with open('Lung_model_pickle','rb') as f:
            mod = pickle.load(f)
            pred = mod.predict(lung)
            pred = pred.tolist()
            print("Lung:", pred)
        with open('Heart_model_pickle', 'rb') as f:
            mod = pickle.load(f)
            pred1 = mod.predict(heart)
            pred1 = pred1.tolist()
            print("Heart:", pred1)
        if pred[0] == 1 and pred1[0] == 0:
            pr = "We are sorry to tell you have lung cancer! 😔"
        elif pred1[0] == 1 and pred[0] == 0:
            pr = "We are sorry to tell you that you have Heart disease! 😔"
        elif pred1[0] == 1 and pred[0] == 1:
            pr = "We are sorry to tell you that you have Lung cancer and Heart disease! 😔"
        else:
            pr = "Yay! You are healthy! 🥳"
        latest_answer = {
            "ans": pr
        }
    else:
        ind += 1
        if ind < len(questions):
            for token in doc:
                if token.text=="yes":
                    attributes_dict[next(key_iterator)] = 1
                elif token.text=="no":
                    attributes_dict[next(key_iterator)] = 0
                elif token.like_num:
                    variable_as_int = int(token.text)
                    attributes_dict[next(key_iterator)] = variable_as_int
            latest_answer = {
                "ans": next(values_iterator)
            }
        else:
            latest_answer = {
                "ans": "No more questions"
            }
    return json.dumps(latest_answer)


if __name__ == "__main__":
    app.run(debug=True)