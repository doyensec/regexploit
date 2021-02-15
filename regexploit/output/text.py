POLYNOMIAL_DEGREES = [
    "linear",
    "quadratic",
    "cubic",
    "quartic",
    "quintic",
    "sextic",
    "septic",
    "octic",
    "nonic",
    "decic",
]


class TextOutput:
    def __init__(self, js_flavour: bool = False):
        self.first_for_regex = True
        self.regexes = 0
        self.js_flavour = js_flavour

    def next(self):
        """Next regex being processed."""
        self.first_for_regex = True
        self.regexes += 1

    def record(self, redos, pattern, *, filename=None, lineno=None, context=None):
        if self.first_for_regex:
            if filename:
                if lineno is not None:
                    print(f"Vulnerable regex in {filename} #{lineno}")
                else:
                    print(f"Vulnerable regex in {filename}")
            print(f"Pattern: {pattern}")
            if context:
                print(f"Context: {context}")
            print("---")
            self.first_for_regex = False
        print(redos)
        stars = "\u2b50" * min(10, redos.starriness)
        degree = (
            "exponential"
            if redos.starriness > 10
            else POLYNOMIAL_DEGREES[redos.starriness - 1]
            if redos.starriness > 0
            else "?"
        )
        print(f"Worst-case complexity: {redos.starriness} {stars} ({degree})")
        print(f"Repeated character: {redos.repeated_character}")
        if redos.killer:
            print(f"Final character to cause backtracking: {redos.killer}")
        print(f"Example: {redos.example(self.js_flavour)}\n")
