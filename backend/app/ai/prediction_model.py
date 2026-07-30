import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


class WorkflowRiskModel:

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        self.model_path = "app/ai/trained_model.pkl"


    def train(self, file_path):

        data = pd.read_csv(file_path)

        X = data.drop("risk", axis=1)
        y = data["risk"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        joblib.dump(self.model, self.model_path)

        return accuracy


    def load(self):
        self.model = joblib.load(self.model_path)


    def is_trained(self):
        return os.path.exists(self.model_path)


    def predict(self, features):

        prediction = self.model.predict(
            [features]
        )

        probability = self.model.predict_proba(
            [features]
        )

        return {
            "risk": int(prediction[0]),
            "confidence": float(max(probability[0]))
        }


workflow_model = WorkflowRiskModel()

        

        
