# Student Performance Predictor

This is a small end-to-end machine learning project that predicts a student's
math score from a few background details plus their reading and writing scores.

The project is intentionally simple: it reads the dataset, prepares the data,
trains several regression models, saves the best model, and lets you make new
predictions from Python.

## What The Project Does

- Loads the student performance dataset from `notebook/data/stud.csv`
- Splits the data into train and test files inside `artifacts/`
- Builds a preprocessing pipeline for categorical and numerical columns
- Trains multiple regression models
- Saves the best model as `artifacts/model.pkl`
- Uses the saved model and preprocessor to predict new math scores

## Project Structure

```text
first_ml_project/
├── artifacts/                  # Generated data, preprocessor, and trained model
├── notebook/                   # Dataset and analysis notebook
├── src/
│   ├── components/             # Data ingestion, transformation, and training logic
│   ├── pipeline/               # Training and prediction entry points
│   ├── exception.py            # Custom exception formatting
│   ├── logger.py               # Log setup
│   └── utils.py                # Save/load helper functions
├── requirements.txt
├── setup.py
└── README.md
```

## Setup

From the project folder, install the dependencies:

```powershell
pip install -r requirements.txt
```

If you are using a virtual environment, activate it first.

## Train The Model

Run the training pipeline from the project root:

```powershell
python -m src.pipeline.train_piprline
```

This will create or update:

- `artifacts/data.csv`
- `artifacts/train.csv`
- `artifacts/test.csv`
- `artifacts/preprocessor.pkl`
- `artifacts/model.pkl`

At the end, you should see the best model score printed in the terminal.

Note: the file is currently named `train_piprline.py`, so the command uses
`train_piprline`. The typo is part of the current project structure.

## Make A Prediction

After training, you can predict a math score with:

```powershell
python -c "from src.pipeline.predict_pipeline import CustomData, PredictPipeline; data=CustomData(gender='female', race_ethnicity='group C', parental_level_of_education='some college', lunch='standard', test_preparation_course='completed', reading_score=90, writing_score=88); print(PredictPipeline().predict(data.get_data_as_data_frame()))"
```

The prediction pipeline expects these fields:

- `gender`
- `race_ethnicity`
- `parental_level_of_education`
- `lunch`
- `test_preparation_course`
- `reading_score`
- `writing_score`

It returns the predicted `math_score`.

## Example Input

```python
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

data = CustomData(
    gender="female",
    race_ethnicity="group C",
    parental_level_of_education="some college",
    lunch="standard",
    test_preparation_course="completed",
    reading_score=90,
    writing_score=88,
)

prediction = PredictPipeline().predict(data.get_data_as_data_frame())
print(prediction)
```

## Notes

- Logs are written to the `logs/` folder.
- CatBoost runtime logs are ignored with `catboost_info/` in `.gitignore`.
- The current trained model artifact is stored at `artifacts/model.pkl`.

## Why This Project Matters

This project is a practical first ML pipeline: it is not just a notebook, and it
is not only a model file. It shows the full workflow from raw data to reusable
prediction code, which is the part that starts to feel like real machine
learning engineering.
