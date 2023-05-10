from typing import List
import mlflow
import mlflow.sklearn

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from config.config import logger

lr = LogisticRegression()
svc = SVC()
dt = DecisionTreeClassifier()
rf = RandomForestClassifier()

models = [lr, svc, dt, rf]
model_name = ["Logistic Regression", "SVC", "Decision Tree", "Random Forest"]
scores = []


def model1(df: pd.DataFrame):
    X = df.drop(["Machine failure", "type_of_failure"], axis=1)
    y = df["Machine failure"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    for i, m in enumerate(models):
        m.fit(X_train, y_train)
        y_pred = m.predict(X_test)
        acc = accuracy_score(y_test, y_pred) * 100
        prec = precision_score(y_test, y_pred) * 100
        rec = recall_score(y_test, y_pred) * 100
        f1 = f1_score(y_test, y_pred) * 100
        scores.append([acc, prec, rec, f1])

        with mlflow.start_run():
            mlflow.sklearn.log_model(m, model_name[i])
            mlflow.log_metric("Accuracy", acc)
            mlflow.log_metric("Precision", prec)
            mlflow.log_metric("Recall", rec)
            mlflow.log_metric("F1", f1)

    scores_df = pd.DataFrame(
        columns=["Model"], data=["Logistic Regression", "SVC", "Decision Tree", "Random Forest"]
    )
    scores_df = pd.concat(
        [scores_df, pd.DataFrame(scores, columns=["Accuracy", "Precision", "Recall", "F1"])], axis=1
    )
    best_model_idx = scores_df["F1"].idxmax()
    best_model = models[best_model_idx]

    # mlflow.sklearn.log_model(best_model, "best_model")

    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    report = classification_report(y_test, y_pred)

    # mlflow.log_text('Classification Report', report)

    logger.info("Best Model: {}".format(best_model))
    logger.info(f"Classification Report:\n{report}")



    return scores_df, best_model, report


def model2(df: pd.DataFrame):
    X = df.drop(["Machine failure", "type_of_failure"], axis=1)
    y = df["type_of_failure"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    for i, m in enumerate(models):
        m.fit(X_train, y_train)
        y_pred = m.predict(X_test)
        acc = accuracy_score(y_test, y_pred) * 100
        prec = precision_score(y_test, y_pred, average="macro") * 100
        rec = recall_score(y_test, y_pred, average="macro") * 100
        f1 = f1_score(y_test, y_pred, average="macro") * 100
        scores.append([acc, prec, rec, f1])

        with mlflow.start_run():
            mlflow.sklearn.log_model(m, model_name[i])
            mlflow.log_metric("Accuracy", acc)
            mlflow.log_metric("Precision", prec)
            mlflow.log_metric("Recall", rec)
            mlflow.log_metric("F1", f1)

    scores_df = pd.DataFrame(
        columns=["Model"], data=["Logistic Regression", "SVC", "Decision Tree", "Random Forest"]
    )
    scores_df = pd.concat(
        [scores_df, pd.DataFrame(scores, columns=["Accuracy", "Precision", "Recall", "F1"])], axis=1
    )

    best_model_idx = scores_df["F1"].idxmax()
    best_model = models[best_model_idx]
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    report = classification_report(y_test, y_pred)
    logger.info("Best Model: {}".format(best_model))
    logger.info(f"Classification Report:\n{report}")

    return scores_df, best_model, report
