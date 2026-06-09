# Module 08: NLP and Transformers

[← Module 07: Deep Learning](../07_deep-learning/) | [Topic Home](../../README.md) | [Next → Module 09: ML Engineering](../09_ml-engineering/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-advanced-red)
![Time](https://img.shields.io/badge/time-14--18h-orange)

> Text processing, word embeddings (Word2Vec/GloVe), the attention mechanism, the Transformer architecture (BERT, GPT), and fine-tuning pre-trained models with HuggingFace Transformers.

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

Natural Language Processing (NLP) is the application of ML to text and language. For most of ML history, NLP required heavy feature engineering: tokenization, stemming, TF-IDF, hand-crafted grammars. The Transformer architecture (2017) changed everything. Pre-trained Transformers like BERT and GPT can be fine-tuned to achieve state-of-the-art performance on most NLP tasks with minimal task-specific engineering.

This module builds up from first principles: text preprocessing, word embeddings as the first neural representation of language, the attention mechanism as the key insight behind Transformers, the full Transformer architecture, and practical fine-tuning with HuggingFace. By the end, you will be able to fine-tune a BERT model for text classification with ~10 lines of Python.

---

## Prerequisites

### Required Modules

- [[ai-ml/modules/06_neural-networks]] — Neural networks, backpropagation
- [[ai-ml/modules/07_deep-learning]] — PyTorch, embeddings, sequence processing basics

### Required Concepts

- **PyTorch `nn.Module`** — defining and training neural networks
- **Softmax and cross-entropy** — used in attention and classification heads

---

## Objectives

By the end of this module, you will be able to:

1. Preprocess text for ML: tokenization, vocabulary building, padding, and subword tokenization
2. Explain word embeddings and implement a Word2Vec-style training objective
3. Explain the self-attention mechanism: queries, keys, values, and the attention score computation
4. Implement a simplified Transformer encoder from scratch in PyTorch
5. Fine-tune a pre-trained BERT model using the HuggingFace `Trainer` API
6. Evaluate NLP models using task-specific metrics (BLEU, ROUGE, perplexity, F1)

---

## Theory

### Text Preprocessing and Embeddings

Text cannot be fed directly to neural networks — it must be converted to numbers. The two steps are tokenization (splitting text into tokens) and embedding (mapping tokens to dense vectors).

```python
from transformers import AutoTokenizer

# Modern NLP uses subword tokenization (BPE, WordPiece)
# This handles unknown words by splitting them into known subwords
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

text = "The quick brown fox jumps over the lazy dog"
tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

print(f"Input IDs shape: {tokens['input_ids'].shape}")
print(f"Tokens: {tokenizer.convert_ids_to_tokens(tokens['input_ids'][0])}")
# Output: ['[CLS]', 'the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog', '[SEP]']
# Note: BERT adds [CLS] and [SEP] tokens
```

**Word2Vec** learned that words with similar meanings appear in similar contexts. The embedding for "king" - "man" + "woman" ≈ "queen" — arithmetic on meaning. This was the first demonstration that dense vector representations capture semantic relationships.

```python
# Conceptual Word2Vec: skip-gram objective
# Given a target word, predict its context words
# This forces semantically similar words to have similar embeddings

import torch
import torch.nn as nn

class SkipGramModel(nn.Module):
    """Simplified Word2Vec skip-gram."""
    def __init__(self, vocab_size, embed_dim):
        super().__init__()
        self.embeddings = nn.Embedding(vocab_size, embed_dim)
        self.out_embeddings = nn.Embedding(vocab_size, embed_dim)

    def forward(self, target_word, context_words):
        target_embed = self.embeddings(target_word)       # (batch, embed_dim)
        context_embed = self.out_embeddings(context_words) # (batch, embed_dim)
        # Dot product: high score = similar meaning
        score = (target_embed * context_embed).sum(dim=1)
        return score
```

### The Attention Mechanism

The key insight behind Transformers is **self-attention**: each token in a sequence attends to all other tokens and computes a weighted sum of their representations. This allows direct modeling of long-range dependencies — no more vanishing gradients over long sequences.

Given queries Q, keys K, and values V (all linear projections of the input):

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class SelfAttention(nn.Module):
    """
    Single-head self-attention.
    Full Transformers use multi-head attention — multiple attention heads in parallel.
    """
    def __init__(self, embed_dim):
        super().__init__()
        self.embed_dim = embed_dim
        # Three linear projections: query, key, value
        self.W_q = nn.Linear(embed_dim, embed_dim, bias=False)
        self.W_k = nn.Linear(embed_dim, embed_dim, bias=False)
        self.W_v = nn.Linear(embed_dim, embed_dim, bias=False)
        self.W_out = nn.Linear(embed_dim, embed_dim)

    def forward(self, x, mask=None):
        """
        x: (batch_size, seq_len, embed_dim)
        mask: optional mask to prevent attending to padding tokens
        """
        Q = self.W_q(x)  # (batch, seq_len, embed_dim)
        K = self.W_k(x)  # (batch, seq_len, embed_dim)
        V = self.W_v(x)  # (batch, seq_len, embed_dim)

        # Scaled dot-product attention scores
        scale = math.sqrt(self.embed_dim)
        scores = torch.bmm(Q, K.transpose(1, 2)) / scale  # (batch, seq_len, seq_len)

        # Apply mask (set padding positions to -inf before softmax)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float("-inf"))

        # Softmax: convert scores to attention weights (sum to 1 per query)
        weights = F.softmax(scores, dim=-1)  # (batch, seq_len, seq_len)

        # Weighted sum of values
        output = torch.bmm(weights, V)      # (batch, seq_len, embed_dim)
        return self.W_out(output), weights  # Return weights for visualization

# Test the attention mechanism
seq_len, embed_dim = 10, 64
x = torch.randn(2, seq_len, embed_dim)  # Batch of 2 sequences
attn = SelfAttention(embed_dim)
output, weights = attn(x)
print(f"Input shape:  {x.shape}")
print(f"Output shape: {output.shape}")   # Same shape as input
print(f"Weights shape: {weights.shape}") # (2, 10, 10) — attention matrix
```

### Fine-Tuning BERT with HuggingFace

```python
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
)
from datasets import load_dataset
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

# Load dataset — SST-2 is a binary sentiment classification task
dataset = load_dataset("glue", "sst2")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize(examples):
    return tokenizer(examples["sentence"], truncation=True, padding="max_length",
                     max_length=128)

tokenized = dataset.map(tokenize, batched=True)

# Load pre-trained BERT with a classification head for 2 classes
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased", num_labels=2
)
# BERT has ~110M parameters; the classification head adds ~1.5K

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, predictions),
        "f1": f1_score(labels, predictions, average="binary"),
    }

training_args = TrainingArguments(
    output_dir="./bert-sst2",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    learning_rate=2e-5,          # Small LR for fine-tuning pre-trained weights
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["validation"],
    compute_metrics=compute_metrics,
)

# trainer.train()  # ~30 min on GPU; omit in testing
# Expected result: ~93% accuracy on SST-2 (BERT paper reports 93.5%)
print("BERT fine-tuning setup complete. Call trainer.train() to start.")
```

---

## Key Concepts

**Tokenization** — Converting text to a sequence of tokens (words, subwords, or characters). Modern models use subword tokenization (BPE, WordPiece) to handle any vocabulary while keeping the vocabulary size manageable.

**Word Embedding** — A dense vector representation of a word that captures semantic meaning. Words used in similar contexts have similar embeddings.

**Self-Attention** — A mechanism where each token attends to all other tokens, computing a weighted sum of values based on query-key similarity. Enables direct long-range dependencies.

**Multi-Head Attention** — Running multiple attention heads in parallel, each attending to different aspects of the relationships between tokens. The outputs are concatenated and projected.

**BERT** — Bidirectional Encoder Representations from Transformers. Pre-trained on masked language modeling (MLM) and next sentence prediction (NSP). Bidirectional context. Best for classification and understanding tasks.

**GPT** — Generative Pre-trained Transformer. Pre-trained on next-token prediction. Unidirectional (causal). Best for generation tasks.

**Fine-Tuning** — Continuing training of a pre-trained model on a new task with a small learning rate. The pre-trained representations adapt to the task-specific distribution.

---

## Examples

### Example 1: Zero-Shot Classification with HuggingFace Pipeline

```python
from transformers import pipeline

# No fine-tuning needed for zero-shot: the model uses NLI to classify
classifier = pipeline("zero-shot-classification",
                       model="facebook/bart-large-mnli")

texts = [
    "The new iPhone has an amazing camera.",
    "Stocks fell sharply on Tuesday amid inflation concerns.",
    "Scientists discover new species of deep-sea fish.",
]
labels = ["technology", "finance", "science", "sports"]

for text in texts:
    result = classifier(text, candidate_labels=labels)
    print(f"Text: {text[:50]}...")
    print(f"  Predicted: {result['labels'][0]} (score: {result['scores'][0]:.3f})")
```

---

## Common Pitfalls

### Pitfall 1: Using the Full Dataset for Tokenizer Vocabulary Building

The tokenizer vocabulary must be built on training data only. HuggingFace pre-trained tokenizers already have a fixed vocabulary — this pitfall applies to training a tokenizer from scratch.

### Pitfall 2: Forgetting the `[CLS]` Token for BERT Classification

BERT uses the `[CLS]` token's representation for classification. When using the raw BERT output, take `last_hidden_state[:, 0, :]` (the first token).

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("bert-base-uncased")
outputs = model(**tokens)
cls_representation = outputs.last_hidden_state[:, 0, :]  # [CLS] token
```

### Pitfall 3: Learning Rate Too High for Fine-Tuning

Pre-trained weights are fragile — a high learning rate will destroy the useful representations. Use learning rates in the range [1e-5, 5e-5] for fine-tuning Transformer models.

---

## Cross-Links

- [[ai-ml/modules/07_deep-learning]] — PyTorch, embeddings, and the neural network foundations used here
- [[ai-ml/modules/10_llms-and-generative-ai]] — LLMs extend these Transformer foundations to much larger scale
- [[ai-ml/modules/09_ml-engineering]] — Serving Transformer models as APIs
- [[ai-ml/modules/11_responsible-ai]] — Bias in NLP models is a well-documented and important problem

---

## Summary

- **Text must be converted to numeric representations.** Subword tokenization (BPE, WordPiece) handles out-of-vocabulary words by splitting them into known subwords.
- **Word embeddings map words to dense vectors where semantically similar words are close.** Word2Vec and GloVe introduced this; modern models learn embeddings contextually (different senses get different vectors).
- **Self-attention is the core mechanism of Transformers.** It allows each token to directly attend to every other token, enabling long-range dependencies without vanishing gradients.
- **BERT is bidirectional; GPT is unidirectional.** Use BERT for classification and understanding; GPT for generation.
- **Fine-tuning is the standard workflow.** Load a pre-trained model, add a task-specific head, train with a small learning rate for a few epochs.
- **HuggingFace Transformers makes fine-tuning ~10 lines of code.** But understanding the architecture under the hood is what this module is for.
