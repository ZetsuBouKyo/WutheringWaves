from html2text import html2text
from lxml import html

from ww.commands.crawl.utils import clear_text
from ww.locale import ZhTwEnum, _


class WeaponParser:
    def __init__(self, html_str: str):
        self.html_str = html_str
        self.tree = html.fromstring(self.html_str)
        self.data = {}

    def get_name_pattern(self) -> str:
        return f'//span[@class="skillname"]'

    def get_description_pattern(self) -> str:
        return f'//span[@class="skilldescription"]'

    def parse(self, pattern: str, key_name: str):
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

                print(h_text)
                self.data[key_name] = h_text

    def get_data(self):
        self.parse(self.get_name_pattern(), _(ZhTwEnum.NAME))
        self.parse(self.get_description_pattern(), _(ZhTwEnum.DESCRIPTION))
        return self.data
