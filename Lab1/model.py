# Standard imports
import numpy as np
import pandas as pd

# Models & preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_log_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer 


# Load data
train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

# Save PassengerId
test_ids = test_df["Id"]

# Drop the target from train
y = train_df["SalePrice"]
X = train_df.drop(["SalePrice"], axis=1)

# Combine both for preprocessing
combined = pd.concat([X, test_df], axis=0)

# Identify numeric and categorical columns
num_features = combined.select_dtypes(include=["int64", "float64"]).columns
cat_features = combined.select_dtypes(include=["object"]).columns

# Preprocess: fill missing values + one-hot encode categories
numeric_transformer = Pipeline(steps=[
    ("fillna", SimpleImputer(strategy="median"))
])

categorical_transformer = Pipeline(steps=[
    ("fillna", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, num_features),
        ("cat", categorical_transformer, cat_features)
    ])

# Choose model
model = RandomForestRegressor(
    n_estimators=250,
    random_state=42,
    n_jobs=-1
)

# Full pipeline
clf = Pipeline(steps=[("preprocess", preprocessor),
                    ("model", model)
                   ])

# Train model
clf.fit(X, y)

# Predict on test
preds = clf.predict(test_df)

# Make submission file
submission = pd.DataFrame({
    "Id": test_ids,
    "SalePrice": preds
})

submission.to_csv("submission.csv", index=False)
print("Saved submission.csv")
