# Advent of Code Challenge Problems

## Bootstrap a new day
Use `copier` to invoke the Python template and set up files for a new solution:

```console
$ copier copy --trust gh:gahjelle/template-aoc-python .
```

Answer the questions and allow the hook to download your personal input.
Then download the data for the new day:

```commandline
python download_input.py <year> <day>
```
or from the directory:

```commandline
aocd > input.txt
```

## Finish up a solution

```commandline
python <day_file> input.txt > output.py.txt
```

## References

  * https://github.com/gahjelle/advent_of_code/tree/main/python
  * https://realpython.com/python-advent-of-code/#solving-advent-of-code-with-python
  * https://github.com/wimglenn/advent-of-code-data#quickstart
