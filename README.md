# dzipcrack
Zip password guesser

# Available Parameters
- multiprocess
- string starts with
- string contains
- string endswith
- minlen
- maxlen
- charset
  
It supports also non legacy passwords

# How to use
```
python dzipcrack.py -B --starts 'C' --middle 'xx' --ends '@' --min_len 13 --max_len 13 --charset A1! protected.zip

-b Bruteforce
starts 'AAA'
middle 'BBB'
ends 'CCC'
min_len N
max_len N
charset:
  - A   uppercases
  - 1   digits
  - !   special characters
  - a   lowercases
```

