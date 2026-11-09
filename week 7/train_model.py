import boto3, pandas as pd, io, joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

s3 = boto3.client('s3')
bucket, key = 'mlops-lambton-bucket', 'iris.csv'
obj = s3.get_object(Bucket=bucket, Key=key)
df = pd.read_csv(io.BytesIO(obj['Body'].read()))

X, y = df.iloc[:, :-1], df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y)
model = RandomForestClassifier().fit(X_train, y_train)
joblib.dump(model, 'rf_model.pkl')
s3.upload_file('rf_model.pkl', bucket, 'rf_model.pkl')
print("Model trained and uploaded to S3")
