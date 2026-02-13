class DistanceTable:
    def __init__(self, locations, matrix):
        self.locations = locations
        self.matrix = matrix
        self.index = {loc: i for i, loc in enumerate(locations)}

    def _clean(self, text):
        if text is None:
            return ""

        s = str(text).replace("\n", " ").strip()

        # Treat the hub consistently
        if s.upper() == "HUB":
            return "HUB"

        # Remove zip in parentheses: "195 W Oakland Ave (84115)" -> "195 W Oakland Ave"
        if "(" in s:
            s = s.split("(")[0].strip()

        # Normalize extra spacing
        s = " ".join(s.split())
        return s

    def distance(self, from_loc, to_loc):
        a = self._clean(from_loc)
        b = self._clean(to_loc)

        if a == b:
            return 0.0

        if a not in self.index or b not in self.index:
            raise KeyError(f"Unknown location: '{a}' or '{b}'")

        i = self.index[a]
        j = self.index[b]

        d = self.matrix[i][j]
        if d is None:
            d = self.matrix[j][i]

        if d is None:
            raise ValueError(f"No distance found between '{a}' and '{b}'")

        return float(d)