import os
import sys
from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split

from src.exception import CustomException
from src.logger import logging


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "data.csv")
    source_data_path: str = os.path.join("notebook", "data", "stud.csv")


class DataIngestion:
    def __init__(self) -> None:
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self) -> tuple[str, str]:
        """
        Read source data, save raw copy, split train/test data, and persist artifacts.
        """
        logging.info("Entered data ingestion method.")
        try:
            df = pd.read_csv(self.ingestion_config.source_data_path)
            logging.info(
                "Read source dataset successfully from %s.",
                self.ingestion_config.source_data_path,
            )

            os.makedirs(
                os.path.dirname(self.ingestion_config.raw_data_path),
                exist_ok=True,
            )

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw dataset saved at %s.", self.ingestion_config.raw_data_path)

            logging.info("Initiating train-test split.")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(
                self.ingestion_config.train_data_path,
                index=False,
                header=True,
            )
            test_set.to_csv(
                self.ingestion_config.test_data_path,
                index=False,
                header=True,
            )
            logging.info("Data ingestion is complete.")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e, sys) from e



if __name__ == "__main__":
    ingestion = DataIngestion()
    train_data_path, test_data_path = ingestion.initiate_data_ingestion()
    print(f"Train data saved to: {train_data_path}")
    print(f"Test data saved to: {test_data_path}")
    