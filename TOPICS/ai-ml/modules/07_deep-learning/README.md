# Module 07: Deep Learning

[← Module 06: Neural Networks](../06_neural-networks/) | [Topic Home](../../README.md) | [Next → Module 08: NLP and Transformers](../08_nlp-and-transformers/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-red)
![Time](https://img.shields.io/badge/time-16--20h-orange)

> Deep learning with PyTorch: convolutional neural networks for images, recurrent networks for sequences, and regularization techniques (batch normalization, dropout, transfer learning).

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

Deep learning is where the theory of Module 06 meets practical scale. Modern deep learning frameworks (PyTorch, TensorFlow) handle automatic differentiation — you define the forward pass, and the framework computes all gradients automatically. This frees you to focus on architecture, data, and training dynamics.

This module covers the two most important neural network architectures before Transformers: **Convolutional Neural Networks (CNNs)** for spatial data (images, audio spectrograms) and **Recurrent Neural Networks (RNNs) / LSTMs** for sequential data (time series, text). It also covers the practical techniques that made deep learning work at scale: batch normalization, dropout, learning rate scheduling, and transfer learning.

---

## Prerequisites

### Required Modules

- [[ai-ml/modules/06_neural-networks]] — Forward pass, backprop, activation functions, initialization
- [[ai-ml/modules/05_model-evaluation]] — Evaluation and metrics; training curves

### Required Concepts

- **PyTorch basics** — tensors, autograd, `nn.Module`
- **GPU computing** — understanding `device` in PyTorch (CPU vs. CUDA)

---

## Objectives

By the end of this module, you will be able to:

1. Implement a CNN with convolutional, pooling, and fully-connected layers in PyTorch for image classification
2. Explain how convolutions exploit spatial locality and parameter sharing
3. Implement an LSTM in PyTorch for sequence classification or next-token prediction
4. Apply batch normalization and dropout and explain what problem each solves
5. Fine-tune a pre-trained CNN (transfer learning) on a new dataset with limited data
6. Read and interpret training/validation loss curves to diagnose overfitting and learning rate issues

---

## Theory

### Convolutional Neural Networks

Fully-connected layers treat all input features equally — a pixel at position (0,0) has no special relationship to its neighbor at (0,1). Images have spatial structure: nearby pixels are related. CNNs exploit this with two key ideas:

1. **Local connectivity:** each neuron connects to only a small local region (receptive field)
2. **Weight sharing:** the same filter is applied at every position, reducing parameters

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Define a CNN for MNIST (28x28 grayscale images, 10 classes)
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        # Convolutional layers
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32,
                                kernel_size=3, padding=1)  # Output: 32x28x28
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)  # Output: 64x28x28
        self.pool = nn.MaxPool2d(2, 2)    # Halves spatial dimensions

        # Batch normalization — stabilizes training
        self.bn1 = nn.BatchNorm2d(32)
        self.bn2 = nn.BatchNorm2d(64)

        # Fully-connected classifier
        self.fc1 = nn.Linear(64 * 7 * 7, 128)  # After 2 pooling layers: 28/4=7
        self.fc2 = nn.Linear(128, 10)

        # Dropout for regularization
        self.dropout = nn.Dropout(0.5)

        self.relu = nn.ReLU()

    def forward(self, x):
        # Block 1: conv -> batchnorm -> relu -> pool
        x = self.pool(self.relu(self.bn1(self.conv1(x))))  # -> 32x14x14
        # Block 2: conv -> batchnorm -> relu -> pool
        x = self.pool(self.relu(self.bn2(self.conv2(x))))  # -> 64x7x7
        # Flatten for FC layers
        x = x.view(x.size(0), -1)                          # -> 64*7*7 = 3136
        x = self.dropout(self.relu(self.fc1(x)))
        x = self.fc2(x)
        return x   # Raw logits — loss function applies softmax

# PyTorch training loop
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN().to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

# Load MNIST data
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))  # MNIST mean and std
])
# (dataset loading code omitted — requires torchvision download)

def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss, correct = 0, 0
    for X, y in loader:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        output = model(X)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        correct += (output.argmax(1) == y).sum().item()
    return total_loss / len(loader), correct / len(loader.dataset)
```

### LSTMs for Sequences

Recurrent Neural Networks process sequences by maintaining a hidden state that is updated at each timestep. The basic RNN suffers from vanishing gradients over long sequences. The Long Short-Term Memory (LSTM) adds gating mechanisms to control what information is stored, forgotten, and output.

```python
import torch
import torch.nn as nn

class TextClassifierLSTM(nn.Module):
    """
    LSTM-based sequence classifier.
    Input: sequence of token IDs
    Output: class logits
    """
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_classes, n_layers=2,
                 dropout=0.3):
        super().__init__()
        # Embedding layer: maps token IDs to dense vectors
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        # LSTM: processes the sequence
        self.lstm = nn.LSTM(
            input_size=embed_dim,
            hidden_size=hidden_dim,
            num_layers=n_layers,
            batch_first=True,   # Input shape: (batch, seq_len, embed_dim)
            dropout=dropout,
            bidirectional=True  # Reads sequence in both directions
        )
        # Classifier head
        self.classifier = nn.Linear(hidden_dim * 2, n_classes)  # *2 for bidirectional
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # x: (batch_size, seq_len) — token IDs
        embedded = self.dropout(self.embedding(x))   # (batch, seq_len, embed_dim)
        output, (hidden, cell) = self.lstm(embedded) # output: (batch, seq_len, hidden*2)
        # Use the final hidden state of both directions
        hidden_final = torch.cat([hidden[-2], hidden[-1]], dim=1)  # (batch, hidden*2)
        return self.classifier(self.dropout(hidden_final))

# Example instantiation
model = TextClassifierLSTM(
    vocab_size=10000,
    embed_dim=128,
    hidden_dim=256,
    n_classes=2,
)
print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

# Test with dummy input
x = torch.randint(0, 10000, (32, 100))  # Batch of 32 sequences, length 100
output = model(x)
print(f"Output shape: {output.shape}")  # (32, 2)
```

### Transfer Learning

Training deep networks from scratch requires large datasets and significant compute. Transfer learning reuses the weights of a model trained on a large dataset (e.g., ImageNet) as a starting point for a new task. The pre-trained model has already learned useful low-level features (edges, textures) that transfer across domains.

```python
import torch
import torch.nn as nn
from torchvision import models

# Load a pre-trained ResNet-18 (trained on ImageNet with 1000 classes)
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# Strategy 1: Feature extraction — freeze all layers, only train the classifier
for param in model.parameters():
    param.requires_grad = False  # Freeze everything

# Replace the final classification layer for our new task (e.g., 2 classes)
n_features = model.fc.in_features
model.fc = nn.Linear(n_features, 2)  # Only this layer has trainable params
# Result: ~500K trainable params instead of ~11M

# Strategy 2: Fine-tuning — unfreeze all layers after initial training
for param in model.parameters():
    param.requires_grad = True   # Unfreeze
# Now fine-tune the whole network with a small learning rate
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)  # Small LR for fine-tuning
```

### Batch Normalization and Dropout

**Batch normalization** normalizes layer inputs to have zero mean and unit variance within each mini-batch. This stabilizes training, allows higher learning rates, and acts as a mild regularizer.

**Dropout** randomly zeroes out a fraction of neurons during training. This prevents neurons from co-adapting and forces the network to learn redundant representations — a strong regularizer.

```python
import torch.nn as nn

# Batch norm is placed BEFORE the activation in modern practice
# (though the original paper placed it after)
class ConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))
        # Order: conv -> batchnorm -> relu

# IMPORTANT: batch norm behaves differently in train vs eval mode
# In training: normalizes using batch statistics
# In eval: uses running mean/std accumulated during training
model.train()  # Activates batch norm training behavior (uses batch stats)
model.eval()   # Activates batch norm eval behavior (uses running stats)
# ALWAYS call model.eval() before inference!
```

---

## Key Concepts

**Convolutional Layer** — A layer that applies a learned filter (kernel) at every position of the input via convolution. Exploits translation equivariance: a feature detector works wherever the feature appears.

**Receptive Field** — The region of the input that influences a particular neuron's output. Deeper layers have larger receptive fields, capturing higher-level features.

**Pooling** — A downsampling operation (max pool, average pool) that reduces spatial dimensions, providing translation invariance and reducing computation.

**Batch Normalization** — Normalizes activations within a mini-batch, stabilizing training and reducing sensitivity to initialization.

**Dropout** — A regularization technique that randomly deactivates neurons during training, preventing overfitting by forcing redundant representations.

**Transfer Learning** — Using weights pre-trained on a large dataset as the starting point for a new task. Dramatically reduces data and compute requirements.

---

## Examples

### Example 1: Diagnosing Training Curves

```python
# A well-trained model shows:
# - Both train and val loss decreasing together
# - Val loss close to train loss (small gap = good generalization)
# - Learning rate decay helps when loss plateaus

# Signs of overfitting:
# - Train loss decreasing but val loss increasing
# - Large gap between train and val accuracy

# Signs of underfitting:
# - Both train and val loss high and not decreasing
# - Try: more epochs, larger model, lower regularization, higher learning rate

# Signs of learning rate too high:
# - Loss oscillates wildly or diverges
# - Try: reduce learning rate by 10x

# Signs of learning rate too low:
# - Loss decreases very slowly
# - Try: use learning rate finder (fast.ai technique)
print("Diagnosing training curves is a key skill — study your loss curves at every training run.")
```

---

## Common Pitfalls

### Pitfall 1: Forgetting `model.eval()` During Inference

Batch normalization and dropout behave differently during training vs. inference. Forgetting to call `model.eval()` before inference will give wrong results.

```python
# WRONG: model stays in training mode
model.train()
with torch.no_grad():
    predictions = model(X_test)  # BN uses batch stats, dropout still active!

# CORRECT:
model.eval()
with torch.no_grad():
    predictions = model(X_test)  # BN uses running stats, dropout disabled
```

### Pitfall 2: Not Using `with torch.no_grad():` During Inference

Without `no_grad()`, PyTorch builds the computation graph for all forward passes, consuming extra memory and time.

### Pitfall 3: Exploding Gradients in RNNs

RNNs are prone to exploding gradients over long sequences. The standard fix is gradient clipping.

```python
# Clip gradients before the optimizer step
loss.backward()
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
optimizer.step()
```

---

## Cross-Links

- [[ai-ml/modules/06_neural-networks]] — The numpy foundations that PyTorch automates
- [[ai-ml/modules/08_nlp-and-transformers]] — Transformers replace RNNs for most NLP tasks; this module explains why
- [[ai-ml/modules/09_ml-engineering]] — Serving PyTorch models in production
- [[async-python]] — Async patterns used in model serving APIs

---

## Summary

- **CNNs exploit spatial structure via local connectivity and weight sharing.** They learn a hierarchy of features: edges → textures → parts → objects.
- **LSTMs solve the vanishing gradient problem for sequences** using gating mechanisms. They are now largely replaced by Transformers for NLP but remain relevant for time series.
- **Batch normalization stabilizes training** by normalizing activations within each mini-batch. Always use `model.train()` / `model.eval()` to control its behavior.
- **Dropout is the most widely used regularizer for neural networks.** It is disabled at inference time.
- **Transfer learning dramatically reduces data requirements.** Start with feature extraction (freeze the pre-trained weights), then fine-tune with a small learning rate.
- **Reading training curves is a core skill.** Every loss curve tells a story about what the model is learning and what is going wrong.
