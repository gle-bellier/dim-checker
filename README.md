# DimChecker

Useful tool for functions, neural networks, or callable objects output dimensions checking. It allows fast testing and relies on pattern string for easy use. 
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

