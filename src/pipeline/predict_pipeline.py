import os
import sys
from dataclasses import dataclass

import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import load_object


@dataclass
class CustomData:
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    reading_score: float
    writing_score: float

    def get_data_as_data_frame(self) -> pd.DataFrame:
        """
        Convert one prediction request into the model's expected dataframe shape.
        """
        try:
            data = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(data)

        except Exception as e:
            raise CustomException(e, sys) from e


class PredictPipeline:
    def __init__(
        self,
        model_path: str = os.path.join("artifacts", "model.pkl"),
        preprocessor_path: str = os.path.join("artifacts", "preprocessor.pkl"),
    ) -> None:
        self.model_path = model_path
        self.preprocessor_path = preprocessor_path

    def predict(self, features: pd.DataFrame):
        """
        Transform input features and return math score predictions.
        """
        try:
            logging.info("Loading model and preprocessor for prediction.")
            model = load_object(file_path=self.model_path)
            preprocessor = load_object(file_path=self.preprocessor_path)

            transformed_features = preprocessor.transform(features)
            if hasattr(transformed_features, "toarray"):
                transformed_features = transformed_features.toarray()

            predictions = model.predict(transformed_features)

            logging.info("Prediction completed successfully.")
            return predictions

        except Exception as e:
            raise CustomException(e, sys) from e
