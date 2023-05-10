import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, classification_report
from config.config import logger

lr = LogisticRegression()
svc = SVC()
dt = DecisionTreeClassifier()
rf = RandomForestClassifier()

models = [lr, svc, dt, rf]
scores = []

def model1(df):
    
    X = df.drop(['Machine failure', 'type_of_failure'], axis=1)
    y = df['Machine failure']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    for m in models:
        m.fit(X_train, y_train)
        y_pred = m.predict(X_test)
        acc = accuracy_score(y_test, y_pred) * 100
        prec = precision_score(y_test, y_pred) * 100
        rec = recall_score(y_test, y_pred) * 100
        f1 = f1_score(y_test, y_pred) * 100
        scores.append([acc, prec, rec, f1])

    scores_df = pd.DataFrame(columns=['Model'], data=['Logistic Regression', 'SVC', 'Decision Tree', 'Random Forest'])
    scores_df = pd.concat([scores_df, pd.DataFrame(scores, columns=['Accuracy', 'Precision', 'Recall', 'F1'])], axis=1)
    best_model_idx = scores_df['F1'].idxmax()
    best_model = models[best_model_idx]

    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    report = classification_report(y_test, y_pred)
    logger.info("Best Model: {}".format(best_model))
    logger.info(f"Classification Report:\n{report}")
    return scores_df, best_model, report

def model2(df):
    X = df.drop(['Machine failure', 'type_of_failure'], axis=1)
    y = df['type_of_failure']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    for m in models:
        m.fit(X_train, y_train)
        y_pred = m.predict(X_test)
        acc = accuracy_score(y_test, y_pred) * 100
        prec = precision_score(y_test, y_pred, average='macro') * 100
        rec = recall_score(y_test, y_pred, average='macro') * 100
        f1 = f1_score(y_test, y_pred, average='macro') * 100
        scores.append([acc, prec, rec, f1])

    scores_df = pd.DataFrame(columns=['Model'], data=['Logistic Regression', 'SVC', 'Decision Tree', 'Random Forest'])
    scores_df = pd.concat([scores_df, pd.DataFrame(scores, columns=['Accuracy', 'Precision', 'Recall', 'F1'])], axis=1)

    best_model_idx = scores_df['F1'].idxmax()
    best_model = models[best_model_idx]
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    report = classification_report(y_test, y_pred)
    logger.info("Best Model: {}".format(best_model))
    logger.info(f"Classification Report:\n{report}")

    return scores_df, best_model, report





    
