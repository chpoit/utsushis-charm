class SimpleSemVer:
    def __init__(self, version=None):
        if not version:
            version = 0
        if type(version) not in (str, float, int):
            raise TypeError(
                "Invalid type used for SimpleSemVer, must be str, int or float"
            )

        self.version = str(version)
        self.major = self.minor = self.patch = 0

        parts = self.version.split(".")
        self.major = int(parts[0])

        if len(parts) > 1:
            self.minor = int(parts[1])
        if len(parts) > 2:
            self.patch = int(parts[2])

    def __eq__(self, other):
        other = SimpleSemVer._fix_type(other)
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __lt__(self, other):
        other = SimpleSemVer._fix_type(other)
        if self.major < other.major:
            return True
        if self.minor < other.minor:
            return True
        if self.patch < other.patch:
            return True
        return False

    def __gt__(self, other):
        other = SimpleSemVer._fix_type(other)
        return other < self

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    @staticmethod
    def _fix_type(data):
        if type(data) is not SimpleSemVer:
            data = SimpleSemVer(data)

        return data
