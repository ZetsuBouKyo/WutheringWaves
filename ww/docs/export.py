import os
from pathlib import Path

import yaml

from ww.crud.template import get_template
from ww.docs.mkdocs_settings import MkdocsSettings
from ww.html.template.output_method import (
    RIGHT_ARROW_ICON_FPATH,
    get_asset,
    get_html_template_output_methods,
)
from ww.locale import ZhTwEnum, _
from ww.model.docs import DocsModel
from ww.model.template import TemplateRowActionEnum
from ww.utils import get_jinja2_template, get_md5

# mkdocs
DEFAULT_MKDOCS_FPATH = "./mkdocs.yml"
MKDOCS_FPATH = "./build/html/mkdocs.yml"

DOCS_FPATH = "./data/v1/zh_tw/docs.yml"


class Docs:
    def __init__(
        self,
        docs_fpath: str = DOCS_FPATH,
        default_mkdocs_fpath: str = DEFAULT_MKDOCS_FPATH,
        mkdocs_fpath: str = MKDOCS_FPATH,
    ):

        with open(default_mkdocs_fpath, encoding="utf-8") as fp:
            try:
                mkdocs_settings = yaml.safe_load(fp)
            except yaml.YAMLError as exc:
                print(exc)
                return

        with open(docs_fpath, encoding="utf-8") as fp:
            try:
                docs_settings = yaml.safe_load(fp)
            except yaml.YAMLError as exc:
                print(exc)
                return

        self._docs_model = DocsModel(**docs_settings)
        self._mkdocs_settings = MkdocsSettings(mkdocs_settings, mkdocs_fpath)

        self._template_id_to_relative_url = {}

    def export(self):
        self._mkdocs_settings.save()

        self.export_resonator_templates()
        self.export_resonator_outline()

    def export_resonator_templates(self):
        template_fpath = "./html/docs/resonator/template.jinja2"
        output_path = "./build/html/docs/resonator/template"

        template = get_jinja2_template(template_fpath)

        output_path = Path(output_path)
        os.makedirs(output_path, exist_ok=True)

        for resonator in self._docs_model.resonators:
            for template_id in resonator.template_ids:
                resonator_tempalte = get_template(template_id)

                all_output_methods = get_html_template_output_methods(
                    resonator_tempalte.rows, labels=[""], is_docs=True
                )
                output_methods = all_output_methods.get("", None)
                if output_methods is None:
                    continue

                html_str = template.render(
                    template=resonator_tempalte,
                    output_methods=output_methods,
                    right_arrow_src=get_asset(RIGHT_ARROW_ICON_FPATH),
                    ZhTwEnum=ZhTwEnum,
                    _=_,
                )

                md5 = get_md5(template_id)
                fname = f"{md5}.md"
                output_fpath = output_path / fname

                with output_fpath.open(mode="w", encoding="utf-8") as fp:
                    fp.write(html_str)

                url = f"/resonator/template/{md5}/index.html"
                self._template_id_to_relative_url[template_id] = url

    def export_resonator_outline(self):
        template_fpath = "./html/docs/resonator/outline.jinja2"
        output_fpath = "./build/html/docs/resonator/outline.md"

        template = get_jinja2_template(template_fpath)

        html_str = template.render(
            docs_settings=self._docs_model,
            template_id_to_relative_url=self._template_id_to_relative_url,
            ZhTwEnum=ZhTwEnum,
            _=_,
        )

        output_fpath = Path(output_fpath)
        os.makedirs(output_fpath.parent, exist_ok=True)
        with output_fpath.open(mode="w", encoding="utf-8") as fp:
            fp.write(html_str)
