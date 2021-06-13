class SimpleSemVer:
    def __init__(self, version=None):
        if not version:
            version = 0
        self.version = str(version)
        self.major = self.minor = self.patch = 0

        parts = self.version.split(".")
        self.major = parts[0]

        if len(parts) > 1:
            self.minor = parts[1]
        if len(parts) > 2:
            self.patch = parts[2]

    def __eq__(self, other):
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __lt__(self, other):
        if self.major < other.major:
            return True
        if self.minor < other.minor:
            return True
        if self.patch < other.patch:
            return True
        return False

    def __gt__(self, other):
        return other < self

    def to_str(self):
        return self.version
