class MarkingPlan:
    def __init__(self):
        self.__event = []
        self.__included = []
        self.__description = []
        self.__triggers = []
        self.__hit_type = []

    def __str__(self):
        _str = "| Nom | Inclus | Description | Déclencheurs | Type de hit |\n---\n"

        for i in range(self.count()):
            item = self.get_index(i)

            _str += "| " + self.__event[i] + " | " + self.__included[i] + " | " + self.__description[i] + " | " \
                    + self.__triggers[i] + " | " + (self.__hit_type[i] if self.__hit_type[i] is not None else "-") \
                    + " |" + ("\n" if i < self.count() else "")

        return _str

    def get(self, event):
        for i in range(len(self.__event)):
            if event == self.__event[i]:
                return self.__event[i], self.__included[i], self.__description[i], self.__triggers[i], \
                       self.__hit_type[i]

        return None

    def put(self, marking):
        for i in range(len(self.__event)):
            if marking == self.__event:
                self.__event = marking[0]
                self.__included = marking[1]
                self.__description = marking[2]
                self.__triggers = marking[3]
                self.__hit_type = marking[4]

                return

        self.__event.append(marking[0])
        self.__included.append(marking[1])
        self.__description.append(marking[2])
        self.__triggers.append(marking[3])
        self.__hit_type.append(marking[4])

    def get_index(self, idx):
        if idx >= self.count():
            return None

        return (self.__event[idx], self.__included[idx], self.__description[idx], self.__triggers[idx],
                self.__hit_type[idx])

    def count(self):
        return len(self.__event)
