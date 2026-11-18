# bracket-validator-purih

Валідатор строки, який перевіряє правильність закривання дужок `()`, `{}`, `<>`.

## Встановлення

```bash
pip install -i https://test.pypi.org/simple/ bracket-validator-purih
```

## Використання

```bash
bracket-validator
```

```
Введіть строку: <div><p>{ test }}</p</div>
<div><p>{ test }}</p</div>
                ^^
ValidationError: Дужки незбалансовані на позиціях: 16, 17
```

```python
from bracket_validator import StringValidator

StringValidator("(a{b}<c>)").validate()  # True
```
