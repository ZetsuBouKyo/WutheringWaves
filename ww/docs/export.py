import os
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Tuple, Union

import yaml

from ww.calc.damage import Damage
from ww.calc.simulated_resonators import SimulatedResonators
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
from ww.html.image.resonator import (
    get_element_class_name,
    get_resonator_icon_url,
    merge_resonator_model,
)
from ww.locale import ZhTwEnum, _
from ww.logging import logger_cli
from ww.model import SkillBaseAttrEnum
from ww.model.buff import SkillBonusTypeEnum
from ww.model.docs import DocsModel
from ww.model.resonator import ResonatorInformationModel
from ww.model.resonator_skill import ResonatorSkillTypeEnum
from ww.model.simulation import SimulationTypeEnum
from ww.model.template import (
    TemplateDamageDistributionModel,
    TemplateHtmlOutputMethodModel,
    TemplateModel,
)
from ww.tables.resonator import get_resonator_information
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


# url
TIER_THEORY_1_URL: str = "/tier/theory_1/index.html"
TIER_HALF_BUILT_ATK_URL: str = "/tier/half_built_atk/index.html"
TIER_HALF_BUILT_SKILL_BONUS_URL: str = "/tier/half_built_skill_bonus/index.html"


def get_resonator_skill_base_damage(
    resonator_damage_distribution,
    skill_enum: Union[SkillBonusTypeEnum, ResonatorSkillTypeEnum],
) -> Decimal:
    base_damage = Decimal("0.0")
    for e in skill_enum:
        base_damage += resonator_damage_distribution.get_damage(e.name.lower())
    return base_damage


def get_resonator_outline_url(no: str) -> str:
    return f"/resonator/{no}/outline/index.html"


def get_resonator_dps_comparison_url(md5: str, prefix: str, no: str) -> str:
    return f"/resonator/{no}/comparison/{prefix}/{md5}/resonator_dps/index.html"


def get_resonator_dps_comparison_md(md5: str, prefix: str, no: str) -> str:
    return (
        f"./build/html/docs/resonator/{no}/comparison/{prefix}/{md5}/resonator_dps.md"
    )


def get_team_dps_comparison_url(md5: str, prefix: str, no: str) -> str:
    return f"/resonator/{no}/comparison/{prefix}/{md5}/team_dps/index.html"


def get_team_dps_comparison_md(md5: str, prefix: str, no: str) -> str:
    return f"./build/html/docs/resonator/{no}/comparison/{prefix}/{md5}/team_dps.md"


def get_damage_analysis_url(md5: str, prefix: str) -> str:
    return f"/resonator/template/{md5}/{prefix}/damage_analysis/index.html"


def get_echo_damage_comparison_url(md5: str, prefix: str, no: str) -> str:
    return f"/resonator/template/{md5}/{prefix}/echo_damage_comparison/{no}/index.html"


def export_html(fpath: Union[str, Path], html_str: str):
    if type(fpath) is str:
        fpath = Path(fpath)
    os.makedirs(fpath.parent, exist_ok=True)
    with fpath.open(mode="w", encoding="utf-8") as fp:
        fp.write(html_str)


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
        self._docs_model.check()

        self._mkdocs_settings = MkdocsSettings(mkdocs_settings, mkdocs_fpath)
        self._resonator_name_to_info: Dict[str, ResonatorInformationModel] = {}

    def _get_resonator_information(
        self, resonator_name: str
    ) -> ResonatorInformationModel:
        info = self._resonator_name_to_info.get(resonator_name, None)
        if info is None:
            info = get_resonator_information(resonator_name)
            self._resonator_name_to_info[resonator_name] = info
        return info

    def export(self):
        self._mkdocs_settings.save()

        (
            template_id_to_relative_url,
            template_id_to_theory_1,
            template_id_to_half_built_atk,
            template_id_to_half_built_skill_bonus,
            template_ids_tier,
            resonator_name_to_template_ids,
        ) = self.export_resonator_templates()
        self.export_resonator_outline(
            resonator_name_to_template_ids,
            template_id_to_relative_url,
            template_id_to_theory_1,
            template_id_to_half_built_atk,
            template_id_to_half_built_skill_bonus,
        )
        self.export_resonators(resonator_name_to_template_ids)

        self.export_tier_outline()
        self.export_3_resonators_tier_barhs(
            template_ids_tier,
            template_id_to_relative_url,
            template_id_to_theory_1,
            template_id_to_half_built_atk,
            template_id_to_half_built_skill_bonus,
        )

    def export_resonator_echo_damage_comparison(
        self,
        resonator_template: TemplateModel,
        output_fpath: str,
        simulated_resonators: SimulatedResonators,
        resonator_ids: List[str],
        resonators_table,
    ):
        template_fpath = "./html/docs/resonator/template_echo_damage_compare.jinja2"
        template = get_jinja2_template(template_fpath)

        calculated_resonators_table = (
            simulated_resonators.get_calculated_resonators_table(resonators_table)
        )

        # Resonator damage distribution
        monster_id = _(ZhTwEnum.MONSTER_LV_90_RES_20)
        damage = Damage(
            monster_id=monster_id,
            resonators_table=resonators_table,
            calculated_resonators_table=calculated_resonators_table,
        )
        damage_distributions: List[TemplateDamageDistributionModel] = []
        for resonator_id in resonator_ids:
            dmg_distri = damage.get_damage_distributions_with_labels(
                resonator_template.id,
                resonator_id,
                "",
                "",
                monster_id=monster_id,
            )
            dmg_distri = dmg_distri.get("", None)
            if dmg_distri is None:
                continue
            damage_distributions.append(dmg_distri)

        resonators_info = {}
        damages = []
        for damage_distribution in damage_distributions:
            for (
                resonator_damage_distribution
            ) in damage_distribution.resonators.values():
                resonator_id = resonator_damage_distribution.resonator_id
                resonator_name = resonator_damage_distribution.resonator_name
                resonator_info = resonators_info.get(resonator_name, None)
                if resonator_info is None:
                    resonator_info = merge_resonator_model(
                        resonator_id,
                        resonators_table,
                        calculated_resonators_table,
                        is_docs=True,
                    )
                    if resonator_info:
                        resonators_info[resonator_name] = resonator_info
                damages.append(resonator_damage_distribution.damage)

        damage_distributions.sort(
            key=lambda damage_distribution: damage_distribution.damage, reverse=True
        )

        base_damage = max(damages)

        html_str = template.render(
            template=resonator_template,
            calculated_resonators_table=calculated_resonators_table,
            resonators_table=resonators_table,
            resonator_ids=resonator_ids,
            resonators_info=resonators_info,
            damage_distributions=damage_distributions,
            base_damage=base_damage,
            get_element_class_name=get_element_class_name,
            get_percentage_str=get_percentage_str,
            to_number_string=to_number_string,
            to_percentage_str=to_percentage_str,
            merge_resonator_model=merge_resonator_model,
            ZhTwEnum=ZhTwEnum,
            _=_,
        )

        export_html(output_fpath, html_str)

    def export_resonator_echo_damage_comparison_with_prefix(
        self,
        prefix: str,
        resonator_name: str,
        resonator_template: TemplateModel,
        output_fpath: str,
    ):
        simulated_resonators = SimulatedResonators(resonator_template)
        resonator_ids, resonators_table = (
            simulated_resonators.get_resonators_for_echo_comparison_with_prefix(
                resonator_name, prefix
            )
        )

        self.export_resonator_echo_damage_comparison(
            resonator_template,
            output_fpath,
            simulated_resonators,
            resonator_ids,
            resonators_table,
        )

    def export_resonator_echo_damage_comparison_with_theory_1(
        self, resonator_no: str, resonator_name: str, resonator_template: TemplateModel
    ):
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/theory_1/echo_damage_comparison/{resonator_no}.md"

        prefix = _(ZhTwEnum.ECHOES_THEORY_1)

        self.export_resonator_echo_damage_comparison_with_prefix(
            prefix, resonator_name, resonator_template, output_fpath
        )

    def export_resonator_echo_damage_comparison_with_half_built_atk(
        self, resonator_no: str, resonator_name: str, resonator_template: TemplateModel
    ):
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/half_built_atk/echo_damage_comparison/{resonator_no}.md"

        prefix = _(ZhTwEnum.ECHOES_HALF_BUILT_ATK)
        self.export_resonator_echo_damage_comparison_with_prefix(
            prefix, resonator_name, resonator_template, output_fpath
        )

    def export_resonator_echo_damage_comparison_with_half_built_skill_bonus(
        self, resonator_no: str, resonator_name: str, resonator_template: TemplateModel
    ):
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/half_built_skill_bonus/echo_damage_comparison/{resonator_no}.md"

        simulated_resonators = SimulatedResonators(resonator_template)
        resonator_ids, resonators_table = (
            simulated_resonators.get_resonators_for_echo_comparison_with_half_built_skill_bonus(
                resonator_name
            )
        )

        self.export_resonator_echo_damage_comparison(
            resonator_template,
            output_fpath,
            simulated_resonators,
            resonator_ids,
            resonators_table,
        )

    def export_template_damage_analysis(
        self,
        resonator_template: TemplateModel,
        output_methods: TemplateHtmlOutputMethodModel,
        output_fpath: str,
        simulated_resonators: SimulatedResonators,
        resonator_ids: List[str],
        resonators_table,
    ) -> TemplateDamageDistributionModel:
        template_damage_fpath = "./html/docs/resonator/template_damage.jinja2"
        template = get_jinja2_template(template_damage_fpath)
        monster_id = _(ZhTwEnum.MONSTER_LV_90_RES_20)

        calculated_resonators_table = (
            simulated_resonators.get_calculated_resonators_table(resonators_table)
        )

        # Resonator skill damage distribution
        damage = Damage(
            monster_id=monster_id,
            resonators_table=resonators_table,
            calculated_resonators_table=calculated_resonators_table,
        )

        _resonator_ids = ["", "", ""]
        for i in range(len(resonator_ids)):
            _resonator_ids[i] = resonator_ids[i]

        damage_distributions = damage.get_damage_distributions_with_labels(
            resonator_template.id,
            _resonator_ids[0],
            _resonator_ids[1],
            _resonator_ids[2],
            monster_id=monster_id,
        )
        damage_distribution = damage_distributions.get("", None)

        # Detailed damage
        calculated_rows = damage.get_calculated_rows(
            resonator_template.id,
            _resonator_ids[0],
            _resonator_ids[1],
            _resonator_ids[2],
            monster_id,
            is_default=True,
        )

        html_str = template.render(
            template=resonator_template,
            resonators_table=resonators_table,
            resonator_ids=resonator_ids,  # 1 <= len(resonator_ids) <= 3
            calculated_resonators_table=calculated_resonators_table,
            damage_distribution=damage_distribution,
            calculated_rows=calculated_rows,
            output_methods=output_methods,
            merge_resonator_model=merge_resonator_model,
            get_element_class_name=get_element_class_name,
            get_max_damage=get_max_damage,
            get_percentage_str=get_percentage_str,
            get_resonator_icon_url=get_resonator_icon_url,
            get_resonator_skill_base_damage=get_resonator_skill_base_damage,
            get_team_resonator_damages=get_team_resonator_damages,
            to_number_string=to_number_string,
            to_percentage_str=to_percentage_str,
            to_trimmed_number_string=to_trimmed_number_string,
            right_arrow_src=get_asset(RIGHT_ARROW_ICON_FPATH),
            ResonatorSkillTypeEnum=ResonatorSkillTypeEnum,
            SkillBaseAttrEnum=SkillBaseAttrEnum,
            SkillBonusTypeEnum=SkillBonusTypeEnum,
            ZhTwEnum=ZhTwEnum,
            _=_,
            str=str,
            Decimal=Decimal,
        )

        export_html(output_fpath, html_str)

        return damage_distribution

    def export_template_damage_analysis_with_prefix(
        self,
        prefix: str,
        resonator_template: TemplateModel,
        output_methods: TemplateHtmlOutputMethodModel,
        output_fpath: str,
        simulated_resonators: SimulatedResonators,
    ) -> TemplateDamageDistributionModel:
        resonator_ids, resonators_table = (
            simulated_resonators.get_3_resonators_with_prefix(prefix)
        )
        return self.export_template_damage_analysis(
            resonator_template,
            output_methods,
            output_fpath,
            simulated_resonators,
            resonator_ids,
            resonators_table,
        )

    def export_template_damage_analysis_with_theory_1(
        self,
        resonator_template: TemplateModel,
        output_methods: TemplateHtmlOutputMethodModel,
    ) -> TemplateDamageDistributionModel:
        md5 = resonator_template.get_md5()
        output_fpath = (
            f"./build/html/docs/resonator/template/{md5}/theory_1/damage_analysis.md"
        )

        # Simulation
        prefix = _(ZhTwEnum.ECHOES_THEORY_1)
        simulated_resonators = SimulatedResonators(resonator_template)

        return self.export_template_damage_analysis_with_prefix(
            prefix,
            resonator_template,
            output_methods,
            output_fpath,
            simulated_resonators,
        )

    def export_template_damage_analysis_with_half_built_atk(
        self,
        resonator_template: TemplateModel,
        output_methods: TemplateHtmlOutputMethodModel,
    ) -> TemplateDamageDistributionModel:
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/half_built_atk/damage_analysis.md"

        # Simulation
        prefix = _(ZhTwEnum.ECHOES_HALF_BUILT_ATK)
        simulated_resonators = SimulatedResonators(resonator_template)

        return self.export_template_damage_analysis_with_prefix(
            prefix,
            resonator_template,
            output_methods,
            output_fpath,
            simulated_resonators,
        )

    def export_template_damage_analysis_with_half_built_skill_bonus(
        self,
        resonator_template: TemplateModel,
        output_methods: TemplateHtmlOutputMethodModel,
    ) -> TemplateDamageDistributionModel:
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/half_built_skill_bonus/damage_analysis.md"

        simulated_resonators = SimulatedResonators(resonator_template)

        resonator_ids, resonators_table = (
            simulated_resonators.get_3_resonators_with_half_built_skill_bonus()
        )

        return self.export_template_damage_analysis(
            resonator_template,
            output_methods,
            output_fpath,
            simulated_resonators,
            resonator_ids,
            resonators_table,
        )

    def export_resonator_templates(
        self,
    ) -> Tuple[
        Dict[str, str],
        Dict[str, TemplateDamageDistributionModel],
        Dict[str, TemplateDamageDistributionModel],
        Dict[str, TemplateDamageDistributionModel],
        List[str],
        Dict[str, List[str]],
    ]:
        template_id_to_relative_url = {}
        template_id_to_theory_1 = {}
        template_id_to_half_built_atk = {}
        template_id_to_half_built_skill_bonus = {}
        template_ids_tier = []
        resonator_name_to_template_ids: Dict[str, List[str]] = {}

        template_fpath = "./html/docs/resonator/template.jinja2"
        output_path = "./build/html/docs/resonator/template"

        jinja2_template = get_jinja2_template(template_fpath)

        output_path = Path(output_path)
        os.makedirs(output_path, exist_ok=True)

        for template in self._docs_model.templates:
            template_id = template.id
            logger_cli.debug(f"Template ID: {template_id} calculating...")

            resonator_template = get_template(template_id)

            # Echo damage comparison
            echo_comparisons = []
            for resonator_name in template.echo_comparison:
                logger_cli.debug(f"Echo damage comparison: {resonator_name}")

                if resonator_name_to_template_ids.get(resonator_name, None) is None:
                    resonator_name_to_template_ids[resonator_name] = [template_id]
                else:
                    resonator_name_to_template_ids[resonator_name].append(template_id)

                resonator_no = self._get_resonator_information(resonator_name).no

                self.export_resonator_echo_damage_comparison_with_theory_1(
                    resonator_no, resonator_name, resonator_template
                )
                logger_cli.debug("Echo damage comparison: Theory 1 finished.")

                self.export_resonator_echo_damage_comparison_with_half_built_atk(
                    resonator_no, resonator_name, resonator_template
                )
                logger_cli.debug("Echo damage comparison: Half built ATK finished.")

                self.export_resonator_echo_damage_comparison_with_half_built_skill_bonus(
                    resonator_no, resonator_name, resonator_template
                )
                logger_cli.debug(
                    "Echo damage comparison: Half built Skill Bonus finished."
                )

                echo_comparisons.append((resonator_no, resonator_name))

            # Output method
            all_output_methods = get_html_template_output_methods(
                resonator_template.rows, labels=[""], is_docs=True
            )
            output_methods = all_output_methods.get("", None)
            assert (
                output_methods is not None
            ), f"{template_id} does not have output methods."

            html_str = jinja2_template.render(
                template=resonator_template,
                echo_comparisons=echo_comparisons,
                output_methods=output_methods,
                right_arrow_src=get_asset(RIGHT_ARROW_ICON_FPATH),
                get_damage_analysis_url=get_damage_analysis_url,
                get_echo_damage_comparison_url=get_echo_damage_comparison_url,
                ZhTwEnum=ZhTwEnum,
                _=_,
            )

            # Damage analysis
            md5 = resonator_template.get_md5()
            fname = f"{md5}.md"
            output_fpath = output_path / fname
            export_html(output_fpath, html_str)

            url = f"/resonator/template/{md5}/index.html"
            template_id_to_relative_url[template_id] = url

            theory_1_damage_distribution = (
                self.export_template_damage_analysis_with_theory_1(
                    resonator_template, output_methods
                )
            )
            logger_cli.debug("Damage analysis: Theory 1 finished.")

            half_built_atk_damage_distribution = (
                self.export_template_damage_analysis_with_half_built_atk(
                    resonator_template, output_methods
                )
            )
            logger_cli.debug("Damage analysis: Half built ATK finished.")

            half_built_skill_bonus_damage_distribution = (
                self.export_template_damage_analysis_with_half_built_skill_bonus(
                    resonator_template, output_methods
                )
            )
            logger_cli.debug("Damage analysis: Half built Skill Bonus finished.")

            template_id_to_theory_1[template_id] = theory_1_damage_distribution
            template_id_to_half_built_atk[template_id] = (
                half_built_atk_damage_distribution
            )
            template_id_to_half_built_skill_bonus[template_id] = (
                half_built_skill_bonus_damage_distribution
            )

            if template.is_tier:
                template_ids_tier.append(template_id)

            logger_cli.debug(f"Template ID: {template_id} calculated.")

        return (
            template_id_to_relative_url,
            template_id_to_theory_1,
            template_id_to_half_built_atk,
            template_id_to_half_built_skill_bonus,
            template_ids_tier,
            resonator_name_to_template_ids,
        )

    def export_resonator_comparison(
        self,
        title: str,
        prefix: str,
        md5: str,
        resonator_no: str,
        resonator_name: str,
        template_ids: List[str],
        template_id_to_relative_url: Dict[str, str],
        template_id_to_damage_distribution: Dict[str, TemplateDamageDistributionModel],
    ):
        team_fpath = get_team_dps_comparison_md(md5, prefix, resonator_no)
        self.export_3_resonators_tier_barh(
            title,
            template_ids,
            template_id_to_relative_url,
            template_id_to_damage_distribution,
            team_fpath,
        )

        resonator_fpath = get_resonator_dps_comparison_md(md5, prefix, resonator_no)
        self.export_1_resonators_tier_barh(
            title,
            resonator_name,
            template_ids,
            template_id_to_relative_url,
            template_id_to_damage_distribution,
            resonator_fpath,
        )

    def export_resonator_outline(
        self,
        resonator_name_to_template_ids: Dict[str, List[str]],
        template_id_to_relative_url: Dict[str, str],
        template_id_to_theory_1: Dict[str, TemplateDamageDistributionModel],
        template_id_to_half_built_atk: Dict[str, TemplateDamageDistributionModel],
        template_id_to_half_built_skill_bonus: Dict[
            str, TemplateDamageDistributionModel
        ],
    ):
        template_fpath = "./html/docs/resonator/outline.jinja2"
        template = get_jinja2_template(template_fpath)
        comparisons = self._docs_model.comparisons

        for resonator_name, template_ids in resonator_name_to_template_ids.items():
            resonator_info = self._get_resonator_information(resonator_name)
            resonator_no = resonator_info.no
            resonator_comparisons = comparisons.get(resonator_name, None)

            html_str = template.render(
                resonator_no=resonator_no,
                resonator_name=resonator_name,
                resonator_comparisons=resonator_comparisons,
                template_ids=template_ids,
                template_id_to_relative_url=template_id_to_relative_url,
                get_resonator_dps_comparison_url=get_resonator_dps_comparison_url,
                get_team_dps_comparison_url=get_team_dps_comparison_url,
                ZhTwEnum=ZhTwEnum,
                _=_,
            )
            output_fpath = f"./build/html/docs/resonator/{resonator_info.no}/outline.md"
            export_html(output_fpath, html_str)

            if resonator_comparisons is None:
                continue

            for comparison in resonator_comparisons:
                self.export_resonator_comparison(
                    comparison.title,
                    SimulationTypeEnum.THEORY_1.value,
                    comparison.get_md5(),
                    resonator_no,
                    resonator_name,
                    comparison.template_ids,
                    template_id_to_relative_url,
                    template_id_to_theory_1,
                )
                self.export_resonator_comparison(
                    comparison.title,
                    SimulationTypeEnum.HALF_BUILT_ATK.value,
                    comparison.get_md5(),
                    resonator_no,
                    resonator_name,
                    comparison.template_ids,
                    template_id_to_relative_url,
                    template_id_to_half_built_atk,
                )
                self.export_resonator_comparison(
                    comparison.title,
                    SimulationTypeEnum.HALF_BUILT_SKILL_BONUS.value,
                    comparison.get_md5(),
                    resonator_no,
                    resonator_name,
                    comparison.template_ids,
                    template_id_to_relative_url,
                    template_id_to_half_built_skill_bonus,
                )

    def export_resonators(self, resonator_name_to_template_ids: Dict[str, List[str]]):
        template_fpath = "./html/docs/resonators.jinja2"
        output_fpath = "./build/html/docs/resonators.md"

        template = get_jinja2_template(template_fpath)

        resonator_names = list(resonator_name_to_template_ids.keys())
        resonator_names.sort(key=lambda name: self._get_resonator_information(name).no)

        html_str = template.render(
            resonator_names=resonator_names,
            get_resonator_icon_url=get_resonator_icon_url,
            get_resonator_outline_url=get_resonator_outline_url,
            get_resonator_information=self._get_resonator_information,
            ZhTwEnum=ZhTwEnum,
            _=_,
        )

        export_html(output_fpath, html_str)

    def export_tier_outline(self):
        template_fpath = "./html/docs/tier/outline.jinja2"
        output_fpath = "./build/html/docs/tier/outline.md"

        template = get_jinja2_template(template_fpath)

        html_str = template.render(
            TIER_THEORY_1_URL=TIER_THEORY_1_URL,
            TIER_HALF_BUILT_ATK_URL=TIER_HALF_BUILT_ATK_URL,
            TIER_HALF_BUILT_SKILL_BONUS_URL=TIER_HALF_BUILT_SKILL_BONUS_URL,
            ZhTwEnum=ZhTwEnum,
            _=_,
        )

        export_html(output_fpath, html_str)

    def export_1_resonators_tier_barh(
        self,
        title: str,
        resonator_name: str,
        template_ids: List[str],
        template_id_to_relative_url: Dict[str, str],
        template_id_to_damage_distribution: Dict[str, TemplateDamageDistributionModel],
        output_fpath: str,
    ):
        template_fpath = "./html/docs/tier/resonator.jinja2"

        template = get_jinja2_template(template_fpath)

        template_ids.sort(
            key=lambda template_id: template_id_to_damage_distribution[
                template_id
            ].get_resonator_max_dps(resonator_name),
            reverse=True,
        )

        dps = []
        for template_id in template_ids:
            damage_distribution = template_id_to_damage_distribution.get(
                template_id, None
            )
            if damage_distribution is None:
                logger_cli.debug(f"Template ID: {template_id} is None.")
                continue
            dps.append(damage_distribution.get_resonator_max_dps(resonator_name))
        max_dps = max(dps)

        html_str = template.render(
            title=title,
            resonator_name=resonator_name,
            template_ids=template_ids,
            template_id_to_relative_url=template_id_to_relative_url,
            template_id_to_damage_distribution=template_id_to_damage_distribution,
            max_dps=max_dps,
            get_element_class_name=get_element_class_name,
            get_percentage_str=get_percentage_str,
            get_resonator_icon_url=get_resonator_icon_url,
            get_resonator_information=self._get_resonator_information,
            to_number_string=to_number_string,
            to_percentage_str=to_percentage_str,
            ZhTwEnum=ZhTwEnum,
            _=_,
        )

        export_html(output_fpath, html_str)

    def export_3_resonators_tier_barh(
        self,
        title: str,
        template_ids: List[str],
        template_id_to_relative_url: Dict[str, str],
        template_id_to_damage_distribution: Dict[str, TemplateDamageDistributionModel],
        output_fpath: str,
    ):
        template_fpath = "./html/docs/tier/barh.jinja2"

        template = get_jinja2_template(template_fpath)

        template_ids.sort(
            key=lambda template_id: template_id_to_damage_distribution[
                template_id
            ].get_max_dps(),
            reverse=True,
        )

        dps = []
        for template_id in template_ids:
            damage_distribution = template_id_to_damage_distribution.get(
                template_id, None
            )
            if damage_distribution is None:
                logger_cli.debug(f"Template ID: {template_id} is None.")
                continue
            dps.append(damage_distribution.get_max_dps())
        assert len(dps) > 0, f"{title}: {template_ids}"
        max_dps = max(dps)

        html_str = template.render(
            title=title,
            template_ids=template_ids,
            template_id_to_relative_url=template_id_to_relative_url,
            template_id_to_damage_distribution=template_id_to_damage_distribution,
            max_dps=max_dps,
            get_element_class_name=get_element_class_name,
            get_percentage_str=get_percentage_str,
            get_resonator_icon_url=get_resonator_icon_url,
            get_resonator_information=self._get_resonator_information,
            to_number_string=to_number_string,
            ZhTwEnum=ZhTwEnum,
            _=_,
        )

        export_html(output_fpath, html_str)

    def export_3_resonators_tier_barhs(
        self,
        template_ids: List[str],
        template_id_to_relative_url: Dict[str, str],
        template_id_to_theory_1: Dict[str, TemplateDamageDistributionModel],
        template_id_to_half_built_atk: Dict[str, TemplateDamageDistributionModel],
        template_id_to_half_built_skill_bonus: Dict[
            str, TemplateDamageDistributionModel
        ],
    ):
        theory_1_fpath = "./build/html/docs/tier/theory_1.md"
        self.export_3_resonators_tier_barh(
            _(ZhTwEnum.ECHOES_THEORY_1),
            template_ids,
            template_id_to_relative_url,
            template_id_to_theory_1,
            theory_1_fpath,
        )

        half_built_atk_fpath = "./build/html/docs/tier/half_built_atk.md"
        self.export_3_resonators_tier_barh(
            _(ZhTwEnum.ECHOES_HALF_BUILT_ATK),
            template_ids,
            template_id_to_relative_url,
            template_id_to_half_built_atk,
            half_built_atk_fpath,
        )

        half_built_skill_bonus_fpath = (
            "./build/html/docs/tier/half_built_skill_bonus.md"
        )
        self.export_3_resonators_tier_barh(
            _(ZhTwEnum.ECHOES_HALF_BUILT_SKILL_BONUS),
            template_ids,
            template_id_to_relative_url,
            template_id_to_half_built_skill_bonus,
            half_built_skill_bonus_fpath,
        )
