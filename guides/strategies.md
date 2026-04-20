# Strategy Guide

This document outlines how to design, implement, and manage trading strategies within the AI Trading Bot. Strategies can be rule-based, machine learning–driven, or hybrid.

---

## 1. Strategy Types

### Rule-Based
- Simple conditions (e.g., moving average crossover).
- Easy to test and explain.
- Example:
  ```python
  if short_ma > long_ma:
      signal = "BUY"
  else:
      signal = "SELL"
