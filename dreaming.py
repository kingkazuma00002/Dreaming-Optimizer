import torch
import numpy as np

class DreamingOptimizer:
    def __init__(self, params, base_optimizer, stagnation_window=20, tolerance=1e-3, noise_scale=2.0, **kwargs):
        """
        Dreaming Optimizer (Stagnation-Triggered Noise Injection)
        """
        self.params = list(params)
        self.opt = base_optimizer(self.params, **kwargs)
        
        self.stagnation_window = stagnation_window
        self.tolerance = tolerance
        self.noise_scale = noise_scale
        
        self.history = []
        self.last_noise_step = 0
        self.steps = 0

    def zero_grad(self):
        self.opt.zero_grad()

    def step(self, current_loss):
        self.steps += 1
        self.history.append(current_loss)
        
        # 履歴が長すぎたら古いものを捨てる
        if len(self.history) > self.stagnation_window:
            self.history.pop(0)

        # 1. 停滞（Stagnation）を検知する
        is_stagnating = False
        if len(self.history) >= self.stagnation_window:
            improvement = max(self.history) - min(self.history)
            if improvement < self.tolerance:
                # 連続してノイズを入れないように少し待つ
                if self.steps - self.last_noise_step > self.stagnation_window:
                    is_stagnating = True

        # 2. 夢を見る（ノイズ注入）か、進む（通常更新）か
        if is_stagnating:
            print(f"[Dreaming] Stagnation detected at step {self.steps}. Injecting noise! 🌙")
            self._inject_noise()
            self.last_noise_step = self.steps
            self.history = [] # ジャンプしたら履歴をリセット
        else:
            self.opt.step()

    def _inject_noise(self):
        with torch.no_grad():
            for p in self.params:
                noise = torch.randn_like(p) * self.noise_scale
                p.add_(noise)