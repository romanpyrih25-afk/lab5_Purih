import sys

PAIRS = {")": "(", "}": "{", ">": "<"}
OPENING = set(PAIRS.values())


class ValidationError(ValueError):
    def __init__(self, message, idx=None):
        self.idx = idx or []
        if self.idx:
            message = f"{message} на позиціях: {', '.join(map(str, self.idx))}"
        super().__init__(message)


class StringValidator:
    _message = "Дужки незбалансовані"

    def __init__(self, text):
        self.text = text

    def find_errors(self):
        stack = []
        errors = []
        for i, char in enumerate(self.text):
            if char in OPENING:
                stack.append((char, i))
            elif char in PAIRS:
                if stack and stack[-1][0] == PAIRS[char]:
                    stack.pop()
                else:
                    errors.append(i)
        errors.extend(i for _, i in stack)
        return sorted(errors)

    def highlight(self, errors):
        marks = [" "] * len(self.text)
        for i in errors:
            marks[i] = "^"
        return f"{self.text}\n{''.join(marks).rstrip()}"

    def _is_balanced(self):
        errors = self.find_errors()
        if errors:
            raise ValidationError(self._message, idx=errors)

    def validate(self):
        try:
            self._is_balanced()
        except ValidationError as err:
            print(self.highlight(err.idx), file=sys.stderr)
            raise err
        return True


def main():
    input_text = input("Введіть строку: ")
    validator = StringValidator(input_text)
    if validator.validate():
        print("Строка валідна")


if __name__ == "__main__":
    main()
