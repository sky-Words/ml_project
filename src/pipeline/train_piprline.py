import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_trainer import DataTrainer
from src.components.data_transformation import DataTransformation
from src.exception import CustomException
from src.logger import logging


class TrainPipeline:
    def run_pipeline(self) -> float:
        """
        Run ingestion, transformation, and model training.
        """
        try:
            logging.info("Training pipeline started.")

            ingestion = DataIngestion()
            train_data_path, test_data_path = ingestion.initiate_data_ingestion()

            transformation = DataTransformation()
            train_array, test_array, _ = transformation.initiate_data_transformation(
                train_data_path=train_data_path,
                test_path=test_data_path,
            )

            trainer = DataTrainer()
            best_model_score = trainer.initiate_model_trainer(
                train_array=train_array,
                test_array=test_array,
            )

            logging.info(
                "Training pipeline completed with best R2 score %.4f.",
                best_model_score,
            )
            return best_model_score

        except Exception as e:
            raise CustomException(e, sys) from e


if __name__ == "__main__":
    score = TrainPipeline().run_pipeline()
    print(f"Best model R2 score: {score:.4f}")
