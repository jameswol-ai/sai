import os
import joblib


class MLBrain:


    def __init__(self):

        self.model=None

        self.load()



    def load(self):

        path="models/model.pkl"


        if os.path.exists(path):

            self.model=joblib.load(
                path
            )



    def predict(self,features):


        if self.model is None:

            return {

                "signal":"WAIT",

                "confidence":0

            }


        result=self.model.predict(
            features
        )


        return {

            "signal":
                result[0],

            "confidence":
                80

        }