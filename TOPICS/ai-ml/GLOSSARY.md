# Glossary: Artificial Intelligence and Machine Learning

> Definitions of key terms used throughout this topic. Terms are listed alphabetically. Cross-links point to the module where each term is introduced and applied in depth.

---

## A

### Activation Function

A mathematical function applied to the output of a neuron in a neural network that introduces non-linearity into the model. Without activation functions, a network of any depth would be equivalent to a single linear layer. Common activation functions include ReLU (Rectified Linear Unit), sigmoid, and tanh. See [[ai-ml/modules/06_neural-networks]].

---

## B

### Backpropagation

The algorithm used to compute gradients of the loss function with respect to the weights in a neural network. It applies the chain rule of calculus to propagate error signals backward through the network from the output layer to the input layer. These gradients are then used by an optimization algorithm (such as gradient descent) to update the weights. See [[ai-ml/modules/06_neural-networks]].

### Batch

A subset of the training dataset used for a single gradient update step. Training on batches (mini-batch gradient descent) is more computationally efficient than processing one example at a time and less noisy than processing the entire dataset at once. Typical batch sizes range from 32 to 512 examples. See [[ai-ml/modules/06_neural-networks]].

### Bias (statistical)

In the bias-variance tradeoff, bias refers to the error introduced by approximating a real-world problem with a simplified model. A high-bias model (e.g., linear regression on a non-linear problem) systematically underfits. Not to be confused with the bias parameter in a neuron (see below). See [[ai-ml/modules/01_introduction]].

### Bias (neuron parameter)

A learnable scalar offset added to the weighted sum of inputs in a neuron, before the activation function. Written as $b$ in $output = f(w \cdot x + b)$. The bias allows the activation function to be shifted, giving the network greater flexibility. See [[ai-ml/modules/06_neural-networks]].

---

## E

### Epoch

One complete pass through the entire training dataset during model training. Training typically requires many epochs (tens to hundreds) before the model converges. The number of epochs is a hyperparameter. An epoch consists of multiple batch updates. See [[ai-ml/modules/06_neural-networks]].

---

## F

### Feature

An individual measurable property or characteristic of the phenomenon being observed. In a dataset, features are the input variables (columns) used to make predictions. Raw features may be transformed or combined to create derived features through feature engineering. See [[ai-ml/modules/01_introduction]].

---

## G

### Gradient Descent

An iterative optimization algorithm that minimizes a loss function by moving the model parameters in the direction of the negative gradient. At each step, parameters are updated as: $\theta \leftarrow \theta - \alpha \nabla_\theta L(\theta)$, where $\alpha$ is the learning rate and $\nabla_\theta L$ is the gradient of the loss. Variants include stochastic (SGD), mini-batch, Adam, and RMSProp. See [[ai-ml/modules/02_math-for-ml]] and [[ai-ml/modules/06_neural-networks]].

---

## H

### Hyperparameter

A parameter of the learning process that is set before training begins and is not learned from the data. Examples include learning rate, number of layers, number of neurons per layer, regularization strength, and batch size. Hyperparameter tuning (via grid search, random search, or Bayesian optimization) is a major part of model development. Contrast with **weight** (a parameter learned from data). See [[ai-ml/modules/05_model-evaluation]].

---

## L

### Label

The target output variable in a supervised learning problem — the value the model is trained to predict. In a classification problem, the label is a class (e.g., "spam" / "not spam"). In a regression problem, the label is a continuous value (e.g., house price). Also called the target, output, or ground truth. See [[ai-ml/modules/01_introduction]].

### Loss Function

A function that measures the discrepancy between the model's predictions and the true labels. The goal of training is to minimize the loss function. Common loss functions include mean squared error (MSE) for regression and cross-entropy loss for classification. The choice of loss function encodes assumptions about the problem. See [[ai-ml/modules/02_math-for-ml]] and [[ai-ml/modules/06_neural-networks]].

---

## O

### Overfitting

A condition where a model performs well on the training data but poorly on unseen test data, because it has memorized training examples rather than learning generalizable patterns. Signs include a large gap between training and validation loss. Overfitting is addressed through regularization, early stopping, dropout, and collecting more data. See [[ai-ml/modules/01_introduction]] and [[ai-ml/modules/05_model-evaluation]].

---

## R

### Regularization

A technique for reducing overfitting by adding a penalty term to the loss function that discourages complex models. L1 regularization (Lasso) adds the absolute value of weights; L2 regularization (Ridge) adds the squared value of weights. Regularization introduces a bias-variance tradeoff: stronger regularization reduces variance (overfitting) but increases bias (underfitting). See [[ai-ml/modules/03_supervised-learning]].

---

## T

### Test Set

A held-out portion of the dataset that is used only at the very end of the modeling process to estimate generalization performance. The test set must never be used during model development, hyperparameter tuning, or feature selection — otherwise the reported test performance is optimistic and misleading. See [[ai-ml/modules/01_introduction]] and [[ai-ml/modules/05_model-evaluation]].

### Training Set

The portion of the dataset used to fit the model parameters. The model sees training examples during gradient descent and adjusts its weights to minimize the training loss. The training set should be representative of the population the model will be deployed on. See [[ai-ml/modules/01_introduction]].

---

## W

### Weight

A learnable parameter in a machine learning model — specifically, the scalar multiplier applied to an input feature (in linear models) or to a connection between neurons (in neural networks). Weights are initialized randomly and updated during training via gradient descent. The entire set of weights defines the model. See [[ai-ml/modules/06_neural-networks]].
