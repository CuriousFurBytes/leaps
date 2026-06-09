# Test: Module 01 — Introduction to AI and Machine Learning

**Instructions:** Answer all questions. Write your answers directly below each question.
Bonus questions are optional and can raise your score above 100%.

**Total Points:** 37 pts (Easy: 5 × 1 pt + Medium: 5 × 2 pts + Hard: 4 × 3 pts + Expert: 2 × 5 pts)
**Bonus Available:** 5 pts

---

## Section 1: Easy Questions (1 pt each)

**Q1.** Which of the following is NOT an example of machine learning?
a) A spam filter trained on millions of emails
b) An if-else rules engine that flags transactions over $10,000
c) A recommendation system that learns from your watch history
d) A neural network that classifies images

> Answer:

**Q2.** What is the defining characteristic that distinguishes machine learning from traditional rule-based programming?

> Answer:

**Q3.** You have a dataset of 10,000 customer records with a column indicating whether each customer churned (1 = churned, 0 = stayed). You want to predict churn for new customers. What type of ML problem is this — supervised, unsupervised, or reinforcement learning? Why?

> Answer:

**Q4.** Define the term "overfitting" in one sentence.

> Answer:

**Q5.** In a train/test split, which set should a preprocessing scaler (e.g., `StandardScaler`) be fitted on?

> Answer:

---

## Section 2: Medium Questions (2 pts each)

**Q6.** Explain the difference between the AI, ML, and deep learning hierarchy. Give one concrete real-world example of a system that uses AI but NOT ML.

> Answer:

**Q7.** A colleague reports that their model achieves 98% accuracy on a medical imaging dataset. You notice the dataset has 2% positive (disease) cases and 98% negative cases. Why might this 98% accuracy be misleading? What would you ask to evaluate the model properly?

> Answer:

**Q8.** Explain the bias-variance tradeoff. In a learning curve, what does it look like when a model is underfitting? What does it look like when a model is overfitting?

> Answer:

**Q9.** Why must the test set only be used once, at the very end of model development? What goes wrong if you use it during hyperparameter tuning?

> Answer:

**Q10.** What is the purpose of using `stratify=y` in `train_test_split`? When would failing to stratify cause a serious problem?

> Answer:

---

## Section 3: Hard Questions (3 pts each)

**Q11.** Write Python code that:
1. Loads the `breast_cancer` dataset from scikit-learn
2. Splits it 80/20 with stratification
3. Scales features using `StandardScaler` (correctly — no data leakage)
4. Trains a `DecisionTreeClassifier` with `max_depth=5`
5. Prints the test accuracy

> Answer:

```python
# Write your code here
```

**Q12.** The following code contains a critical bug. Identify the bug, explain why it matters, and write the corrected version.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.datasets import load_breast_cancer

cancer = load_breast_cancer()
X, y = cancer.data, cancer.target

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # <-- potential issue here?

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)
model = SVC()
model.fit(X_train, y_train)
score = model.score(X_test, y_test)
print(f"Accuracy: {score:.2%}")
```

> Answer:

**Q13.** You train a model and observe: training accuracy = 99.7%, validation accuracy = 61.3%. Diagnose the problem, explain the underlying cause, and propose three specific interventions to fix it, ordered from most to least likely to help.

> Answer:

**Q14.** Compare supervised and unsupervised learning: what does each require, what does each produce, and when would you choose unsupervised over supervised even if you had labeled data?

> Answer:

---

## Section 4: Expert Questions (5 pts each)

**Q15.** Design a complete ML evaluation workflow for the following scenario:

> You are building a fraud detection system for an e-commerce company. The dataset has 0.1% fraud rate (heavily imbalanced). The business impact of a missed fraud (false negative) is 50× greater than the cost of a false positive (flagging a legitimate transaction for review). You need to present results to both the engineering team and the CFO.

Your answer should cover:
- Which train/test splitting strategy and why
- Which evaluation metrics you would report and why
- How you would interpret the model's threshold setting given the business constraints
- What you would show the engineering team vs. the CFO

> Answer:

**Q16.** Synthesize the ML workflow and bias-variance tradeoff into a coherent debugging playbook:

> You have deployed a model that was performing at 91% AUC-ROC. Six months later, AUC-ROC on fresh data has dropped to 74%. What are all the possible explanations for this degradation? For each explanation, describe: (1) how you would confirm that is the cause, and (2) what you would do to fix it.

> Answer:

---

## Bonus Question (5 pts)

**Bonus 1.** The reinforcement learning paradigm was deliberately excluded from the ML workflow diagram in this module (which focused on supervised learning). Sketch (in text/pseudocode) how the RL workflow differs: what replaces the "dataset," what replaces the "loss function," and how the "deployment" and "evaluation" phases are fundamentally different. Give a concrete example of an industrial RL application. (+5 pts)

> Answer:
