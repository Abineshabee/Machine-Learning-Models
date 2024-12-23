from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os


class Model:
    
    def __init__(self):
        base_path = os.path.dirname("./")
        
        vectorizer_path = os.path.join(base_path, 'vectorizer.pkl')
        self.vectorizer = joblib.load(vectorizer_path)
        
        model_path = os.path.join(base_path, 'my_model.pkl')
        self.model = joblib.load(model_path)

    def predict(self, single_query):
        single_query_transformed = self.vectorizer.transform(single_query)
        return self.model.predict(single_query_transformed)
        
    def predict_proba(self, single_query):
        single_query_transformed = self.vectorizer.transform(single_query)
        return self.model.predict_proba(single_query_transformed)

if __name__ == "__main__":
    model_instance = Model()
    
    sample_input = ["SELECT * F 2@@@@ROM users --  #;"]
    
    prediction = model_instance.predict(sample_input)

    prediction_proba = model_instance.predict_proba(sample_input)
    
    print(f"MODEL_PREDICTION &nbsp;&nbsp; : {prediction[0]}")
    print(f"PREDICTION_PROBA  : {prediction_proba}")

    if prediction_proba[0][0] > prediction_proba[0][1] :
        print(f"CLASS             : [ 0 ] ")
        print(f"CLASS_PROBA       : { ( prediction_proba[0][0] ) * 100 }")

    else :
        print(f"CLASS             : [ 1 ] ")
        print(f"CLASS_PROBA       : { ( prediction_proba[0][1] ) * 100 }")
    
    # Interpret the prediction
    if prediction[0] == 1:
        print(f"SQL_Injection     : True")
    else:
        print(f"SQL_Injection     : False")

