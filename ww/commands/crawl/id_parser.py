import json
import re
from html.parser import HTMLParser
from pathlib import Path

import requests


class WutheringWikiHTMLParser(HTMLParser):
    def __init__(self, target_class):
        super().__init__()
        self.target_class = target_class
        self.inside_target_div = False
        self.table = {}
        self.pattern = r"\d+"
        self.current_names = []
        self.current_ids = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "div":
            if (
                "class" in attrs_dict
                and self.target_class in attrs_dict["class"].split()
            ):
                self.inside_target_div = True
        self.current_name = attrs_dict.get("data-name", None)
        if self.current_name is not None:
            self.current_names.append(self.current_name)
            self.current_name = None

        if tag == "a" and self.inside_target_div:
            attrs_dict = dict(attrs)
            href = attrs_dict.get("href", None)
            if href is None:
                return
            matches = re.findall(self.pattern, href)
            self.current_id = matches[0]
            if self.current_id is not None:
                self.current_ids.append(self.current_id)
                self.current_id = None

    def handle_endtag(self, tag):
        if tag == "div" and self.inside_target_div:
            self.inside_target_div = False


def id_parser(url: str, fpath: str):
    resp = requests.get(url)
    html = resp.text

    id_parser = WutheringWikiHTMLParser("itementry")
    id_parser.feed(html)

    ids = id_parser.current_ids
    names = id_parser.current_names
    data = {}
    for i in range(len(ids)):
        data[ids[i]] = names[i]

    fpath = Path(fpath)
    with fpath.open(mode="w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)
