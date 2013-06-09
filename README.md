# dumper - printf debug on GUI

When programming and debugging, sometimes you print internal status to stdout.  Dumper provides equivalent using Tkinter.

Currently dumper supports only grid output -- good for Sudoku, Game of Life, etc.

```python
>>> from dumper import grid
>>> g = grid.Grid(dim=(5, 10))
>>> g.dump('12345\nabcde\nox xo\n\n-----')

```

