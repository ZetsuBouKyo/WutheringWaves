import os
from decimal import Decimal
from pathlib import Path
from typing import Union

import yaml

from ww.calc.damage import Damage
from ww.calc.simulated_echoes import (
    HalfBuiltAtkSimulatedEchoes,
    SimulatedEchoes,
    Theory1SimulatedEchoes,
)
from ww.calc.simulated_resonators import (
    HalfBuiltAtkSimulatedResonators,
    SimulatedResonators,
    Theory1SimulatedResonators,
)
from ww.crud.template import get_template
from ww.docs.mkdocs_settings import MkdocsSettings
from ww.html.image.damage import get_max_damage
from ww.html.image.damage_distribution import (
    _get_resonator_damages as get_team_resonator_damages,
)
from ww.html.image.output_method import (
    RIGHT_ARROW_ICON_FPATH,
    get_asset,
    get_html_template_output_methods,
)
from ww.html.image.resonator import get_element_class_name, merge_resonator_model
from ww.html.image.resonator_damage_compare import (
    _get_damages as get_resonator_damage_compare_damage,
)
from ww.locale import ZhTwEnum, _
from ww.model import SkillBaseAttrEnum
from ww.model.buff import SkillBonusTypeEnum
from ww.model.docs import DocsModel
from ww.model.resonator_skill import ResonatorSkillTypeEnum
from ww.model.template import TemplateModel, TemplateRowActionEnum
from ww.utils import get_jinja2_template
from ww.utils.number import (
    get_percentage_str,
    to_number_string,
    to_percentage_str,
    to_trimmed_number_string,
)

# mkdocs
DEFAULT_MKDOCS_FPATH = "./mkdocs.yml"
MKDOCS_FPATH = "./build/html/mkdocs.yml"

DOCS_FPATH = "./data/v1/zh_tw/docs.yml"


def get_resonator_skill_base_damage(
    resonator_damage_distribution,
    skill_enum: Union[SkillBonusTypeEnum, ResonatorSkillTypeEnum],
) -> Decimal:
    base_damage = Decimal("0.0")
    for e in skill_enum:
        base_damage += resonator_damage_distribution.get_damage(e.name.lower())
    return base_damage


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

    def export_resonator_template_damage(
        self,
        resonator_template: TemplateModel,
        output_fpath: str,
        simulated_echoes: SimulatedEchoes,
        simulated_resonators: SimulatedResonators,
    ):
        template_damage_fpath = "./html/docs/resonator/template_damage.jinja2"

        template = get_jinja2_template(template_damage_fpath)

        monster_id = _(ZhTwEnum.MONSTER_LV_90_RES_20)
        resonator_ids = [
            resonator.resonator_name for resonator in resonator_template.resonators
        ]

        # Tables
        echoes_table = simulated_echoes.get_table()
        resonators_table = (
            simulated_resonators.get_resonators_table_for_damage_distribution()
        )
        calculated_resonators_table = (
            simulated_resonators.get_calculated_resonators_table(resonators_table)
        )

        # Resonator skill damage distribution
        damage = Damage(
            monster_id=monster_id,
            resonators_table=resonators_table,
            calculated_resonators_table=calculated_resonators_table,
        )

        damage_distributions = damage.get_damage_distributions_with_labels(
            resonator_template.id,
            resonator_ids[0],
            resonator_ids[1],
            resonator_ids[2],
            monster_id=monster_id,
        )
        damage_distribution = damage_distributions.get("", None)

        # Detailed damage
        calculated_rows = damage.get_calculated_rows(
            resonator_template.id,
            resonator_ids[0],
            resonator_ids[1],
            resonator_ids[2],
            monster_id,
            is_default=True,
        )

        html_str = template.render(
            template=resonator_template,
            resonators_table=resonators_table,
            calculated_resonators_table=calculated_resonators_table,
            damage_distribution=damage_distribution,
            calculated_rows=calculated_rows,
            merge_resonator_model=merge_resonator_model,
            get_element_class_name=get_element_class_name,
            get_max_damage=get_max_damage,
            get_percentage_str=get_percentage_str,
            get_resonator_skill_base_damage=get_resonator_skill_base_damage,
            get_team_resonator_damages=get_team_resonator_damages,
            to_number_string=to_number_string,
            to_percentage_str=to_percentage_str,
            to_trimmed_number_string=to_trimmed_number_string,
            ResonatorSkillTypeEnum=ResonatorSkillTypeEnum,
            SkillBaseAttrEnum=SkillBaseAttrEnum,
            SkillBonusTypeEnum=SkillBonusTypeEnum,
            ZhTwEnum=ZhTwEnum,
            _=_,
            str=str,
            Decimal=Decimal,
        )

        output_fpath = Path(output_fpath)
        os.makedirs(output_fpath.parent, exist_ok=True)
        with output_fpath.open(mode="w", encoding="utf-8") as fp:
            fp.write(html_str)

    def export_resonator_template_damage_by_theory_1(
        self, resonator_template: TemplateModel
    ):
        md5 = resonator_template.get_md5()
        output_fpath = (
            f"./build/html/docs/resonator/template/{md5}/theory_1/damage_analysis.md"
        )

        # Simulation
        prefix = _(ZhTwEnum.ECHOES_THEORY_1)
        simulated_echoes = Theory1SimulatedEchoes(prefix)
        simulated_resonators = Theory1SimulatedResonators(
            prefix, "", resonator_template
        )

        self.export_resonator_template_damage(
            resonator_template, output_fpath, simulated_echoes, simulated_resonators
        )

    def export_resonator_template_damage_by_half_built_atk(
        self, resonator_template: TemplateModel
    ):
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/half_built_atk/damage_analysis.md"

        # Simulation
        prefix = _(ZhTwEnum.ECHOES_HALF_BUILT_ATK)
        simulated_echoes = HalfBuiltAtkSimulatedEchoes(prefix)
        simulated_resonators = HalfBuiltAtkSimulatedResonators(
            prefix, "", resonator_template
        )

        self.export_resonator_template_damage(
            resonator_template, output_fpath, simulated_echoes, simulated_resonators
        )

    def export_resonator_templates(self):
        template_fpath = "./html/docs/resonator/template.jinja2"
        output_path = "./build/html/docs/resonator/template"

        template = get_jinja2_template(template_fpath)

        output_path = Path(output_path)
        os.makedirs(output_path, exist_ok=True)

        for resonator in self._docs_model.resonators:
            for template_id in resonator.template_ids:
                resonator_template = get_template(template_id)

                all_output_methods = get_html_template_output_methods(
                    resonator_template.rows, labels=[""], is_docs=True
                )
                output_methods = all_output_methods.get("", None)
                if output_methods is None:
                    continue

                html_str = template.render(
                    template=resonator_template,
                    output_methods=output_methods,
                    right_arrow_src=get_asset(RIGHT_ARROW_ICON_FPATH),
                    ZhTwEnum=ZhTwEnum,
                    _=_,
                )

                md5 = resonator_template.get_md5()
                fname = f"{md5}.md"
                output_fpath = output_path / fname

                with output_fpath.open(mode="w", encoding="utf-8") as fp:
                    fp.write(html_str)

                url = f"/resonator/template/{md5}/index.html"
                self._template_id_to_relative_url[template_id] = url

                self.export_resonator_template_damage_by_theory_1(resonator_template)
                self.export_resonator_template_damage_by_half_built_atk(
                    resonator_template
                )

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
