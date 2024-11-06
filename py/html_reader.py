from urllib.request import urlopen, Request

from html.parser import HTMLParser

class HTMLTag:
    def __init__(self, name):
        self.__name = name
        self.__attrs = []
        self.parent = None
        self.__children = []
        self.data = None

    def get_tags(self, tag):
        if tag is None:
            return None

        tags = []

        if tag == self.__name:
            tags.append(self)

        for child in self.__children:
            tags += child.get_tags(tag)

        return tags

    def get_attr_tags(self, name, content=None, case=True):
        if name is None:
            return None

        tags = []

        for attr in self.__attrs:
            if type(content) == list:
                for key in content:
                    if attr[1] is not None and (name == '' or name == attr[0])\
                            and ((not case and key.lower() in attr[1].lower()) or (case and key in attr[1])):
                        tags.append(self)

                        break

            if name == attr[0] and (content == attr[1] or content is None):
                tags.append(self)

        for child in self.__children:
            tags += child.get_attr_tags(name, content)

        return tags

    def get_data_tags(self, data):
        if data is None:
            return None

        tags = []

        if data == self.data:
            tags.append(self)

        for child in self.__children:
            tags += child.get_data_tags(data)

        return tags

    def get_name(self):
        return self.__name

    def set_attr(self, attr):
        self.__attrs.append(attr)

    def get_attr(self, name):
        for attr in self.__attrs:
            if name == attr[0]:
                return attr

        return None

    def push_child(self, child):
        self.__children.append(child)

    def get_child(self, name):
        for child in self.__children:
            if name == child.get_name():
                return child

        return None


class HTMLReader(HTMLParser):
    def read_url(self, url):
        self.__url = url
        self.__data = urlopen(
            Request(self.__url, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8')
        self.__head = None
        self.__tag = None

        self.feed(self.__data)

        return self.__data

    def render(self):
        return self.__head

    def handle_starttag(self, tag, attrs):
        node = HTMLTag(tag)

        if self.__head is None:
            self.__head = node

        else:
            prev = self.__tag
            node.parent = prev
            prev.push_child(node)

        self.__tag = node

        for attr in attrs:
            self.__tag.set_attr(attr)

    def handle_endtag(self, tag):
        self.__tag = self.__tag.parent

    def handle_data(self, data):
        if self.__tag is None:
            return

        self.__tag.data = data
