# DimChecker

Useful tool for functions, neural networks, or callable objects output dimensions checking. It allows fast testing and relies on pattern string for easy use. 
```python
DimChecker().test_dims(nn, "bcl->bn(2*c+1)l", n=16)
```
