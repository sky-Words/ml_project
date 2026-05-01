import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")


class DataTrainer:
    def __init__(self) -> None:
        self.data_trainer_config = DataTrainerConfig()

    @staticmethod
    def evaluate_models(x_train, y_train, x_test, y_test, models: dict) -> dict:
        """
        Train each candidate model and return its test R2 score.
        """
        try:
            report = {}

            for model_name, model in models.items():
                logging.info("Training model: %s", model_name)
                model.fit(x_train, y_train)

                y_test_pred = model.predict(x_test)
                test_model_score = r2_score(y_test, y_test_pred)

                report[model_name] = test_model_score
                logging.info("%s R2 score: %.4f", model_name, test_model_score)

            return report

        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_model_trainer(self, train_array, test_array) -> float:
        """
        Train multiple regression models, save the best one, and return its R2 score.
        """
        try:
            logging.info("Splitting training and test arrays.")

            x_train = train_array[:, :-1]
            y_train = train_array[:, -1]
            x_test = test_array[:, :-1]
            y_test = test_array[:, -1]

            models = {
                "Random Forest": RandomForestRegressor(random_state=42),
                "Decision Tree": DecisionTreeRegressor(random_state=42),
                "Gradient Boosting": GradientBoostingRegressor(random_state=42),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(random_state=42),
                "CatBoosting Regressor": CatBoostRegressor(
                    verbose=False,
                    random_state=42,
                ),
                "AdaBoost Regressor": AdaBoostRegressor(random_state=42),
            }

            model_report = self.evaluate_models(
                x_train=x_train,
                y_train=y_train,
                x_test=x_test,
                y_test=y_test,
                models=models,
            )

            best_model_score = max(model_report.values())
            best_model_name = max(model_report, key=model_report.get)
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException(
                    Exception("No best model found with an R2 score above 0.6."),
                    sys,
                )

            logging.info(
                "Best model: %s with R2 score: %.4f",
                best_model_name,
                best_model_score,
            )

            save_object(
                file_path=self.data_trainer_config.trained_model_file_path,
                obj=best_model,
            )

            logging.info(
                "Saved trained model to %s.",
                self.data_trainer_config.trained_model_file_path,
            )

            return best_model_score

        except Exception as e:
            raise CustomException(e, sys) from e
