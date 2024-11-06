class Variable:
    def __init__(self, name, content, generic):
        self.name = name
        self.content = content
        self.__generic = generic

    def __str__(self):
        _str = "\n\t'" + self.name + "': '"

        if self.__generic:
            _str += "%"

        _str += self.content + "'"

        return _str


class DLObject:
    def __init__(self, name):
        self.name = name
        self.__vars = []
        self.__objs = []

    def __str__(self):
        _str = "'" + self.name + "': [{\n"

        for var in self.__vars:
            _str += str(var)

        for obj in self.__objs:
            _str += str(obj)

        _str += "\n\t}]\n"

        return _str

    def put_variable(self, name, content, generic=True):
        for var in self.__vars:
            if name == var.name:
                var.content = content

                return

        self.__vars.append(Variable(name, content, generic))

    def put_object(self, obj):
        self.__objs.append(obj)


class DataLayer:
    def __init__(self, event):
        self.__event = event
        self.__vars = []
        self.__objs = []

    def __str__(self):
        _str = "dataLayer.push({\n\t'event': '" + self.__event + "'" + ("," if len(self.__vars) > 0
                                                                               or len(self.__objs) > 0 else "")

        for var in self.__vars:
            _str += str(var) + ("," if self.__vars.index(var) < len(self.__vars) - 1
                                                or len(self.__objs) > 0 else "") + "\n"

        _str += "\n\t"

        for obj in self.__objs:
            _str += str(obj)

        _str += "})"

        return _str

    def get_variable(self, name):
        for var in self.__vars:
            if name == var.name:
                return var

        return None

    def put_variable(self, name, content, generic=True):
        for var in self.__vars:
            if name == var.name:
                var.content = content

                return

        self.__vars.append(Variable(name, content, generic))

    def put_var_list(self, vars):
        for var in vars:
            if len(vars) < 2:
                self.put_variable(var[0], var[1])

            else:
                self.put_variable(var[0], var[1], var[2])

    def put_object(self, obj):
        self.__objs.append(obj)
