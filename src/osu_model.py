from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB

# from roc import plot_roc

df = pd.read_csv("data/csv/basic_osu_df.csv")

y = df.pop("mapper").values
X = df.values

X_train, X_test, y_train, y_test = train_test_split(X, y)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

print("\n8. score:", rf.score(X_test, y_test))

# 8. score: 0.9678030303030303

y_predict = rf.predict(X_test)
print("\n9. confusion matrix:")
print(confusion_matrix(y_test, y_predict))

# 9. confusion matrix:
# [[191  10]
#  [  7 320]]

print("\n10. precision:", precision_score(y_test, y_predict, pos_label="Sotarks"))
print("    recall:", recall_score(y_test, y_predict, pos_label="Sotarks"))

# 10. precision: 0.9696969696969697
#     recall: 0.9785932721712538

rf = RandomForestClassifier(n_estimators=30, oob_score=True)
rf.fit(X_train, y_train)
print("\n11: accuracy score:", rf.score(X_test, y_test))
print("    out of bag score:", rf.oob_score_)

# 11: accuracy score: 0.9696969696969697
#     out of bag score: 0.9601518026565465

feature_importances = np.argsort(rf.feature_importances_)
print("\n12: top five:", list(df.columns[feature_importances[-1:-6:-1]]))
n = 10  # top 10 features

# 12: top five: ['sampleindex', 'sliderbezierratio', 'sliderperfectratio', 'samplesetnormalratio', 'sliderlinearratio']

# importances = forest_fit.feature_importances_[:n]
importances = rf.feature_importances_[:n]
std = np.std([tree.feature_importances_ for tree in rf.estimators_], axis=0)
indices = np.argsort(importances)[::-1]
features = list(df.columns[indices])

# Print the feature ranking
print("\n13. Feature ranking:")

for f in range(n):
    print("%d. %s (%f)" % (f + 1, features[f], importances[indices[f]]))

# 13. Feature ranking:
# 1. sliderbezierratio (0.156728)
# 2. sliderperfectratio (0.089751)
# 3. sliderlinearratio (0.050499)
# 4. sliderslides (0.023497)
# 5. sliderpointamount (0.013989)
# 6. newcombolen (0.013538)
# 7. sliderpointdistance (0.010713)
# 8. sliderlen (0.009811)
# 9. slidervelocity (0.007166)
# 10. slidercatmullratio (0.000126)

# Plot the feature importances of the forest
fig, ax2 = plt.subplots()

ax2.bar(range(10), importances[indices], yerr=std[indices], color="r", align="center")
ax2.set_xticks(range(10))
ax2.set_xticklabels(features, rotation=90)
ax2.set_xlim([-1, 10])
ax2.set_xlabel("importance")
ax2.set_title("Feature Importances")

plt.savefig("images/graph/Feature_Importances.png")

num_trees = range(5, 50, 5)
accuracies = []
for n in num_trees:
    tot = 0
    for i in range(5):
        rf = RandomForestClassifier(n_estimators=n)
        rf.fit(X_train, y_train)
        tot += rf.score(X_test, y_test)
    accuracies.append(tot / 5)
fig, ax = plt.subplots()
ax.plot(num_trees, accuracies)
ax.set_xlabel("Number of Trees")
ax.set_ylabel("Accuracy")
ax.set_title("Accuracy vs Num Trees")
plt.savefig("images/graph/Accuracy_vs_Num_Trees.png")

num_features = range(1, len(df.columns) + 1)
accuracies = []
for n in num_features:
    tot = 0
    for i in range(5):
        rf = RandomForestClassifier(max_features=n)
        rf.fit(X_train, y_train)
        tot += rf.score(X_test, y_test)
    accuracies.append(tot / 5)
fig, ax1 = plt.subplots()
ax1.plot(num_features, accuracies)
ax1.set_xlabel("Number of Features")
ax1.set_ylabel("Accuracy")
ax1.set_title("Accuracy vs Num Features")
plt.savefig('images/graph/Accuracy_vs_Num_Features".png')


def get_scores(classifier, X_train, X_test, y_train, y_test, **kwargs):
    model = classifier(**kwargs)
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)
    return (
        model.score(X_test, y_test),
        precision_score(y_test, y_predict, pos_label="Sotarks"),
        recall_score(y_test, y_predict, pos_label="Sotarks"),
    )


print("\n16. Model, Accuracy, Precision, Recall")
# 16. Model, Accuracy, Precision, Recall
#     Random Forest: (0.9621212121212122, 0.9595015576323987, 0.9777777777777777)
print(
    "    Random Forest:",
    get_scores(
        RandomForestClassifier,
        X_train,
        X_test,
        y_train,
        y_test,
        n_estimators=25,
        max_features=5,
    ),
)
print(
    "    Logistic Regression:",
    get_scores(LogisticRegression, X_train, X_test, y_train, y_test),
)
print(
    "    Decision Tree:",
    get_scores(DecisionTreeClassifier, X_train, X_test, y_train, y_test),
)
print("    Naive Bayes:", get_scores(MultinomialNB, X_train, X_test, y_train, y_test))


print(
    "17. Use the included `plot_roc` function to visualize the roc curve of each model"
)
# plot_roc(X, y, RandomForestClassifier, "Random_Forest", n_estimators=25, max_features=5)
# plot_roc(X, y, LogisticRegression, "Logistic_Regression")
# plot_roc(X, y, DecisionTreeClassifier, "Decision_Tree")

plt.show()
