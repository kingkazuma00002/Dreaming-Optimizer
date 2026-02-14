# Dreaming: Stagnation-Triggered Noise Injection (STNI) 🌙

> **"Exploration should be triggered by optimization dynamics, not by time schedules."**

**Dreaming** is a novel optimization algorithm designed to escape high-dimensional saddle points.
Unlike Simulated Annealing, Dreaming injects "impulse noise" only when stagnation is detected.

## 📄 Paper & Blog
- **Blog Post (Japanese):** [Click Here](https://kakitima1.hatenablog.com/entry/2026/02/14/135131)
- **Paper (PDF):** (ここにPDFへのリンクが入る予定)

## ⚡ Quick Start
```python
import torch
from dreaming import DreamingOptimizer

# Setup Dreaming Optimizer (wrapping SGD)
opti