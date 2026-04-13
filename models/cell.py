class Cell:
    def __init__(self):
        self.raw_value = ""
        self.value     = None
        self.type      = None   # "number" | "text" | "formula" | "error"

    def set_value(self, raw_value):
        self.raw_value = raw_value
        self._detect_type()

    def _detect_type(self):
        v = self.raw_value

        if not isinstance(v, str) or v.strip() == "":
            self.value = None
            self.type  = None
            return

        if v.startswith("="):
            self.type  = "formula"
            self.value = None
            return

        try:
            self.value = float(v)
            self.type  = "number"
        except ValueError:
            self.value = v
            self.type  = "text"

    def set_error(self, msg):
        self.value = f"#ERR: {msg}"
        self.type  = "error"

    def clear(self):
        self.raw_value = ""
        self.value     = None
        self.type      = None

    def __repr__(self):
        return f"Cell(type={self.type}, value={self.value!r})"