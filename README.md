# PCR simulator

```
javac pcr.java
java pcr primer.txt sequences.fa
```
result will be like:
```
2
3
66.67% sequences are found
```
the first line, number of sequnce found
the second line, number of sequence in the query

#### remove_align.java
```
javac remove_align.java
java remove_align input.fa output.fa
```

#### get_degenerate.py
```
python get_degenerate.py primer.txt > output.txt
```