from html2text import html2text
from lxml import html

from ww.commands.crawl.utils import clear_text
from ww.locale import ZhTwEnum, _


class EchoParser:
    def __init__(self, html_str: str):
        self.html_str = html_str
        self.tree = html.fromstring(self.html_str)
        self.data = {}

    def parse(self, pattern: str):
        elements = self.tree.xpath(pattern)
        if elements:
            length = len(elements)
            if length != 1:
                print(f"Elements: {length}")
                return
            for element in elements:
                h = html.tostring(
                    element, pretty_print=True, method="html", encoding=str
                )

                h_text = html2text(h)
                h_text = clear_text(h_text)

        return h_text

    def get_description(self):
        return self.parse(
            '//div[@class="content-container"]/span[@class="description"]'
        )

    def get_name(self):
        return self.parse('//div[@class="content-container"]/span[@class="name"]')

    def get_data(self):
        return self.get_name(), self.get_description()
