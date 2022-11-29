# DimChecker

Useful tool for functions, neural networks, or callable objects outputs dimensions checking. It allows fast testing and relies on pattern string for easy use. 
```python
DimChecker().test_dims(nn, "bcl->bn(2*c+1)l", n=16)
```


## Define Pattern

### Write pattern

A pattern is defined as two formulas separated by an arrow:

```python
pattern = "bcl -> b(2*c)l"
DimChecker().test_dims(nn, pattern)
```
On the left side of the arrow we have the _inputs formula_ and the _outputs formula_ on the right.


```python
in_formula = "bcl"
out_formula = "b(2*c)l"
pattern = in_formula + "->" + out_formula
DimChecker().test_dims(nn, pattern)
```

### Write formulas

#### simple case


Dimensions are defined by a single letter. Here a common machine learning input tensor of shape $\textit{Batch} \times \textit{Channel} \times \textit{Length}$ :
```python
formula = "bcl"
```
For 2D images of shape $\textit{Batch} \times \textit{Channel} \times \textit{Height} \times \textit{Width}$ we may use:

```python
formula = "bchw"
```

#### arithmetical expression



#### several inputs or outputs

To use several inputs or outputs we only need to separate them by commas:
```python
# several inputs
pattern = "bcl, bl -> bcl"
# several outputs
pattern = "bcl -> bcl, bl"
# several inputs or outputs
pattern = "bcl, bc ->bcl, bl"
DimChecker().test_dims(nn, pattern)
```

## Add Constraints

