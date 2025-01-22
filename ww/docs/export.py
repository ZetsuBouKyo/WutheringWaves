import json
import os
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import yaml
from pydantic import BaseModel

from ww.calc.damage import Damage
from ww.calc.simulated_resonators import SimulatedResonators
from ww.crud.resonator import get_resonator_names
from ww.crud.template import get_template, get_template_path
from ww.docs.mkdocs_settings import MkdocsSettings
from ww.html.image.output_method import (
    RIGHT_ARROW_ICON_FPATH,
    get_asset,
    get_html_template_output_methods,
)
from ww.html.image.resonator import (
    get_element_class_name,
    get_element_icon_url,
    get_resonator_icon_url,
    merge_resonator_model,
)
from ww.locale import ZhTwEnum, _
from ww.logging import logger_cli
from ww.model import SkillBaseAttrEnum
from ww.model.buff import SkillBonusTypeEnum
from ww.model.docs import DocsModel, DocsTierModel, DocsTiersModel
from ww.model.resonator import ResonatorInformationModel
from ww.model.resonator_skill import ResonatorSkillTypeEnum
from ww.model.simulation import SimulationTypeEnum
from ww.model.template import (
    TemplateDamageDistributionModel,
    TemplateHtmlDamageAnalysisModel,
    TemplateHtmlEchoComparisonModel,
    TemplateHtmlOutputMethodModel,
    TemplateHtmlResonatorModel,
    TemplateModel,
)
from ww.tables.resonator import (
    ResonatorSkillTable,
    ResonatorsTable,
    get_resonator_information,
)
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

CACHE_HOME_PATH = "./build/html/cache"

DOCS_FPATH = "./data/v1/zh_tw/docs.yml"
DOCS_HOME_PATH = "./build/html/docs"


# url
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


def get_echo_comparison_url(md5: str, prefix: str, no: str) -> str:
    return f"/resonator/template/{md5}/{prefix}/echo_comparison/{no}/index.html"


def get_tier_url(field_name: str, model_name: str) -> str:
    return f"/tier/{field_name}/{model_name}/index.html"


def get_tier_md_fpath(field_name: str, model_name: str) -> str:
    return f"./build/html/docs/tier/{field_name}/{model_name}.md"


def get_cache_fpath_by_md_fpath(
    md_fpath: str,
    cache_home_path: str = CACHE_HOME_PATH,
    docs_home_path: str = DOCS_HOME_PATH,
) -> Path:
    cache_home_path = Path(CACHE_HOME_PATH)
    docs_home_path = Path(DOCS_HOME_PATH)
    md_fpath = Path(md_fpath)
    relative_md_fpath = md_fpath.relative_to(docs_home_path)
    cache_fpath = cache_home_path / relative_md_fpath
    return cache_fpath.with_suffix(".json")


def save_cache(
    model: Union[TemplateHtmlDamageAnalysisModel, TemplateHtmlEchoComparisonModel],
    md_fpath: str,
):
    cache_fpath = get_cache_fpath_by_md_fpath(md_fpath)
    os.makedirs(cache_fpath.parent, exist_ok=True)
    with cache_fpath.open(mode="w", encoding="utf-8") as fp:
        d = model.model_dump(mode="json", serialize_as_any=True, warnings=False)
        json.dump(d, fp, indent=4, ensure_ascii=False)


def get_cache(
    resonator_tempalte: TemplateModel, md_fpath: str, pydantic_model: BaseModel
) -> Optional[Union[TemplateHtmlDamageAnalysisModel, TemplateHtmlEchoComparisonModel]]:
    cache_fpath = get_cache_fpath_by_md_fpath(md_fpath)
    if not cache_fpath.exists():
        return None

    resonator_tempalte_id = resonator_tempalte.id
    resonator_tempalte_fpath = get_template_path(resonator_tempalte_id)
    if resonator_tempalte_fpath is None:
        return None

    cache_file_mtime = cache_fpath.stat().st_mtime
    resonator_tempalte_mtime = resonator_tempalte_fpath.stat().st_mtime

    if resonator_tempalte_mtime > cache_file_mtime:
        return None

    with cache_fpath.open(mode="r", encoding="utf-8") as fp:
        d = json.load(fp)

    cache = pydantic_model(**d)
    return cache


def get_damage_analysis_cache(
    resonator_tempalte: TemplateModel, md_fpath: str
) -> Optional[TemplateHtmlDamageAnalysisModel]:
    return get_cache(resonator_tempalte, md_fpath, TemplateHtmlDamageAnalysisModel)


def get_echo_comparison_cache(
    resonator_tempalte: TemplateModel, md_fpath: str
) -> Optional[TemplateHtmlEchoComparisonModel]:
    return get_cache(resonator_tempalte, md_fpath, TemplateHtmlEchoComparisonModel)


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
        force: bool = False,
    ):

        with open(default_mkdocs_fpath, encoding="utf-8") as fp:
            mkdocs_settings = yaml.safe_load(fp)

        with open(docs_fpath, encoding="utf-8") as fp:
            docs_settings = yaml.safe_load(fp)

        self._docs_model = DocsModel(**docs_settings)
        self._docs_model.check()

        self._mkdocs_settings = MkdocsSettings(mkdocs_settings, mkdocs_fpath)
        self._resonator_name_to_info: Dict[str, ResonatorInformationModel] = {}

        self._force = force

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
            template_id_to_affixes_15_1,
            template_id_to_affixes_20_small,
            template_id_to_affixes_20_skill_bonus,
            template_tiers,
            resonator_name_to_template_ids,
        ) = self.export_resonator_templates()
        self.export_resonator_outline(
            resonator_name_to_template_ids,
            template_id_to_relative_url,
            template_id_to_affixes_15_1,
            template_id_to_affixes_20_small,
            template_id_to_affixes_20_skill_bonus,
        )
        self.export_resonators(resonator_name_to_template_ids)

        self.export_tier_outline(template_tiers)
        self.export_3_resonators_tier_barhs(
            template_tiers,
            template_id_to_relative_url,
            template_id_to_affixes_15_1,
            template_id_to_affixes_20_small,
            template_id_to_affixes_20_skill_bonus,
        )

    def export_resonator_echo_comparison(
        self,
        echo_comparison_model: TemplateHtmlEchoComparisonModel,
        output_fpath: str,
    ):
        template_fpath = "./html/docs/resonator/template_echo_damage_compare.jinja2"
        template = get_jinja2_template(template_fpath)

        resonator_template = echo_comparison_model.resonator_template
        resonator_ids = echo_comparison_model.resonator_ids
        resonator_models = echo_comparison_model.resonator_models
        damage_distributions = echo_comparison_model.damage_distributions
        base_damage = echo_comparison_model.base_damage

        html_str = template.render(
            template=resonator_template,
            resonator_ids=resonator_ids,
            resonator_models=resonator_models,
            damage_distributions=damage_distributions,
            base_damage=base_damage,
            get_percentage_str=get_percentage_str,
            to_number_string=to_number_string,
            ZhTwEnum=ZhTwEnum,
            _=_,
        )

        export_html(output_fpath, html_str)

    def export_resonator_echo_comparison_without_cache(
        self,
        resonator_template: TemplateModel,
        output_fpath: str,
        simulated_resonators: SimulatedResonators,
        resonators_table: ResonatorsTable,
    ):
        calculated_resonators = simulated_resonators.get_calculated_resonators(
            resonators_table
        )
        calculated_resonators_table = calculated_resonators.get_table()
        resonator_ids = calculated_resonators.get_ids()

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

        damages = []
        resonator_models: Dict[str, TemplateHtmlResonatorModel] = {}
        for damage_distribution in damage_distributions:
            for (
                resonator_damage_distribution
            ) in damage_distribution.resonators.values():
                resonator_id = resonator_damage_distribution.resonator_id
                resonator_model = merge_resonator_model(
                    resonator_id,
                    resonators_table,
                    calculated_resonators_table,
                    is_docs=True,
                )
                resonator_models[resonator_id] = resonator_model

                damages.append(resonator_damage_distribution.damage)

        damage_distributions.sort(
            key=lambda damage_distribution: damage_distribution.damage, reverse=True
        )

        base_damage = max(damages)

        echo_comparison_model = TemplateHtmlEchoComparisonModel(
            resonator_template=resonator_template,
            resonator_ids=resonator_ids,
            resonator_models=resonator_models,
            damage_distributions=damage_distributions,
            base_damage=base_damage,
        )
        save_cache(echo_comparison_model, output_fpath)

        return self.export_resonator_echo_comparison(
            echo_comparison_model, output_fpath
        )

    def export_resonator_echo_comparison_with_prefix(
        self,
        prefix: str,
        resonator_name: str,
        resonator_template: TemplateModel,
        output_fpath: str,
    ):
        if not self._force:
            echo_comparison_model = get_echo_comparison_cache(
                resonator_template, output_fpath
            )
            if echo_comparison_model is not None:
                return self.export_resonator_echo_comparison(
                    echo_comparison_model, output_fpath
                )
            logger_cli.debug("Echo damage comparison: updating...")

        simulated_resonators = SimulatedResonators(resonator_template)
        _, resonators_table = (
            simulated_resonators.get_resonators_for_echo_comparison_with_prefix(
                resonator_name, prefix
            )
        )

        return self.export_resonator_echo_comparison_without_cache(
            resonator_template,
            output_fpath,
            simulated_resonators,
            resonators_table,
        )

    def export_resonator_echo_comparison_with_affixes_15_1(
        self, resonator_no: str, resonator_name: str, resonator_template: TemplateModel
    ):
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/affixes_15_1/echo_comparison/{resonator_no}.md"

        prefix = _(ZhTwEnum.ECHOES_AFFIXES_15_1)

        self.export_resonator_echo_comparison_with_prefix(
            prefix, resonator_name, resonator_template, output_fpath
        )

    def export_resonator_echo_comparison_with_affixes_20_small(
        self, resonator_no: str, resonator_name: str, resonator_template: TemplateModel
    ):
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/affixes_20_small/echo_comparison/{resonator_no}.md"

        prefix = _(ZhTwEnum.ECHOES_AFFIXES_20_SMALL)
        self.export_resonator_echo_comparison_with_prefix(
            prefix, resonator_name, resonator_template, output_fpath
        )

    def export_resonator_echo_comparison_with_affixes_20_skill_bonus(
        self, resonator_no: str, resonator_name: str, resonator_template: TemplateModel
    ):
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/affixes_20_skill_bonus/echo_comparison/{resonator_no}.md"
        if not self._force:
            echo_comparison_model = get_echo_comparison_cache(
                resonator_template, output_fpath
            )
            if echo_comparison_model is not None:
                return self.export_resonator_echo_comparison(
                    echo_comparison_model, output_fpath
                )
            logger_cli.debug("Echo damage comparison: updating...")

        simulated_resonators = SimulatedResonators(resonator_template)
        _, resonators_table = (
            simulated_resonators.get_resonators_for_echo_comparison_with_affixes_20_skill_bonus(
                resonator_name
            )
        )

        return self.export_resonator_echo_comparison_without_cache(
            resonator_template,
            output_fpath,
            simulated_resonators,
            resonators_table,
        )

    def export_template_damage_analysis(
        self,
        damage_analysis_model: TemplateHtmlDamageAnalysisModel,
        output_fpath: str,
    ) -> TemplateDamageDistributionModel:
        template_damage_fpath = "./html/docs/resonator/template_damage.jinja2"
        template = get_jinja2_template(template_damage_fpath)

        resonator_template = damage_analysis_model.resonator_template
        resonator_models = damage_analysis_model.resonator_models
        damage_distribution = damage_analysis_model.damage_distribution
        damage_distributions_with_buffs = (
            damage_analysis_model.damage_distributions_with_buffs
        )
        calculated_rows = damage_analysis_model.calculated_rows
        output_methods = damage_analysis_model.output_methods

        html_str = template.render(
            template=resonator_template,
            resonator_models=resonator_models,
            damage_distribution=damage_distribution,
            damage_distributions_with_buffs=damage_distributions_with_buffs,
            calculated_rows=calculated_rows,
            output_methods=output_methods,
            get_percentage_str=get_percentage_str,
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

    def export_template_damage_analysis_without_cache(
        self,
        resonator_template: TemplateModel,
        output_methods: List[TemplateHtmlOutputMethodModel],
        output_fpath: str,
        simulated_resonators: SimulatedResonators,
        resonators_table: ResonatorsTable,
    ) -> TemplateDamageDistributionModel:
        monster_id = _(ZhTwEnum.MONSTER_LV_90_RES_20)

        calculated_resonators = simulated_resonators.get_calculated_resonators(
            resonators_table
        )
        calculated_resonators_table = calculated_resonators.get_table()
        resonator_ids = calculated_resonators.get_3_ids()

        # Resonator skill damage distribution
        damage = Damage(
            monster_id=monster_id,
            resonators_table=resonators_table,
            calculated_resonators_table=calculated_resonators_table,
        )

        resonator_models: Dict[str, TemplateHtmlResonatorModel] = {}
        for resonator_id in resonator_ids:
            if not resonator_id:
                continue

            resonator_model = merge_resonator_model(
                resonator_id,
                resonators_table,
                calculated_resonators_table,
                is_docs=True,
            )

            if resonator_model is None:
                continue

            resonator_models[resonator_model.name] = resonator_model

        damage_distributions = damage.get_damage_distributions_with_labels(
            resonator_template.id,
            resonator_ids[0],
            resonator_ids[1],
            resonator_ids[2],
            monster_id=monster_id,
        )
        damage_distribution: Optional[TemplateDamageDistributionModel] = (
            damage_distributions.get("", None)
        )
        damage_distributions_with_buffs = damage.get_damage_distributions_with_buffs(
            resonator_template.id,
            resonator_ids[0],
            resonator_ids[1],
            resonator_ids[2],
            monster_id=monster_id,
        )

        # Detailed damage
        calculated_rows = damage.get_calculated_rows(
            resonator_template.id,
            resonator_ids[0],
            resonator_ids[1],
            resonator_ids[2],
            monster_id,
            is_default=True,
        )

        damage_analysis_model = TemplateHtmlDamageAnalysisModel(
            resonator_template=resonator_template,
            resonator_models=resonator_models,
            damage_distribution=damage_distribution,
            damage_distributions_with_buffs=damage_distributions_with_buffs,
            calculated_rows=calculated_rows,
            output_methods=output_methods,
        )

        save_cache(damage_analysis_model, output_fpath)

        return self.export_template_damage_analysis(damage_analysis_model, output_fpath)

    def export_template_damage_analysis_with_prefix(
        self,
        prefix: str,
        resonator_template: TemplateModel,
        output_methods: List[TemplateHtmlOutputMethodModel],
        output_fpath: str,
        simulated_resonators: SimulatedResonators,
    ) -> TemplateDamageDistributionModel:
        if not self._force:
            damage_analysis_model = get_damage_analysis_cache(
                resonator_template, output_fpath
            )
            if damage_analysis_model is not None:
                return self.export_template_damage_analysis(
                    damage_analysis_model, output_fpath
                )
            logger_cli.debug("Damage analysis: updating...")

        resonators_table = simulated_resonators.get_3_resonators_with_prefix(prefix)

        return self.export_template_damage_analysis_without_cache(
            resonator_template,
            output_methods,
            output_fpath,
            simulated_resonators,
            resonators_table,
        )

    def export_template_damage_analysis_with_affixes_15_1(
        self,
        resonator_template: TemplateModel,
        output_methods: List[TemplateHtmlOutputMethodModel],
    ) -> TemplateDamageDistributionModel:
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/affixes_15_1/damage_analysis.md"

        # Simulation
        prefix = _(ZhTwEnum.ECHOES_AFFIXES_15_1)
        simulated_resonators = SimulatedResonators(resonator_template)

        return self.export_template_damage_analysis_with_prefix(
            prefix,
            resonator_template,
            output_methods,
            output_fpath,
            simulated_resonators,
        )

    def export_template_damage_analysis_with_affixes_20_small(
        self,
        resonator_template: TemplateModel,
        output_methods: List[TemplateHtmlOutputMethodModel],
    ) -> TemplateDamageDistributionModel:
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/affixes_20_small/damage_analysis.md"

        # Simulation
        prefix = _(ZhTwEnum.ECHOES_AFFIXES_20_SMALL)
        simulated_resonators = SimulatedResonators(resonator_template)

        return self.export_template_damage_analysis_with_prefix(
            prefix,
            resonator_template,
            output_methods,
            output_fpath,
            simulated_resonators,
        )

    def export_template_damage_analysis_with_affixes_20_skill_bonus(
        self,
        resonator_template: TemplateModel,
        output_methods: List[TemplateHtmlOutputMethodModel],
    ) -> TemplateDamageDistributionModel:
        md5 = resonator_template.get_md5()
        output_fpath = f"./build/html/docs/resonator/template/{md5}/affixes_20_skill_bonus/damage_analysis.md"

        if not self._force:
            damage_analysis_model = get_damage_analysis_cache(
                resonator_template, output_fpath
            )
            if damage_analysis_model is not None:
                return self.export_template_damage_analysis(
                    damage_analysis_model, output_fpath
                )
            logger_cli.debug("Damage analysis: updating...")

        simulated_resonators = SimulatedResonators(resonator_template)

        resonators_table = (
            simulated_resonators.get_3_resonators_with_affixes_20_skill_bonus()
        )

        return self.export_template_damage_analysis_without_cache(
            resonator_template,
            output_methods,
            output_fpath,
            simulated_resonators,
            resonators_table,
        )

    def export_resonator_templates(
        self,
    ) -> Tuple[
        Dict[str, str],
        Dict[str, TemplateDamageDistributionModel],
        Dict[str, TemplateDamageDistributionModel],
        Dict[str, TemplateDamageDistributionModel],
        DocsTiersModel,
        Dict[str, List[str]],
    ]:
        template_id_to_relative_url = {}
        template_id_to_affixes_15_1 = {}
        template_id_to_affixes_20_small = {}
        template_id_to_affixes_20_skill_bonus = {}
        template_tiers = DocsTiersModel(
            t=DocsTierModel(
                title=_(ZhTwEnum.DOCS_TIER_0_1_TITLE),
                msg=_(ZhTwEnum.DOCS_TIER_0_1_MSG_1),
            ),
            t_1_1=DocsTierModel(
                title=_(ZhTwEnum.DOCS_TIER_1_1_TITLE),
            ),
            t_2_1=DocsTierModel(
                title=_(ZhTwEnum.DOCS_TIER_2_1_TITLE),
            ),
            t_3_1=DocsTierModel(
                title=_(ZhTwEnum.DOCS_TIER_3_1_TITLE),
            ),
            t_4_1=DocsTierModel(
                title=_(ZhTwEnum.DOCS_TIER_4_1_TITLE),
            ),
            t_5_1=DocsTierModel(
                title=_(ZhTwEnum.DOCS_TIER_5_1_TITLE),
            ),
            t_6_1=DocsTierModel(
                title=_(ZhTwEnum.DOCS_TIER_6_1_TITLE),
            ),
            t_6_5=DocsTierModel(
                title=_(ZhTwEnum.DOCS_TIER_6_5_TITLE),
            ),
        )
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

                self.export_resonator_echo_comparison_with_affixes_15_1(
                    resonator_no, resonator_name, resonator_template
                )
                logger_cli.debug("Echo damage comparison: Affixes 15-1 finished.")

                self.export_resonator_echo_comparison_with_affixes_20_small(
                    resonator_no, resonator_name, resonator_template
                )
                logger_cli.debug("Echo damage comparison: Affixes 20 Small finished.")

                self.export_resonator_echo_comparison_with_affixes_20_skill_bonus(
                    resonator_no, resonator_name, resonator_template
                )
                logger_cli.debug(
                    "Echo damage comparison: Affixes 20 Skill BonusSkill Bonus finished."
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
                get_echo_comparison_url=get_echo_comparison_url,
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

            affixes_15_1_damage_distribution = (
                self.export_template_damage_analysis_with_affixes_15_1(
                    resonator_template, output_methods
                )
            )
            logger_cli.debug("Damage analysis: Affixes 15-1 finished.")

            affixes_20_small_damage_distribution = (
                self.export_template_damage_analysis_with_affixes_20_small(
                    resonator_template, output_methods
                )
            )
            logger_cli.debug("Damage analysis: Affixes 20 Small finished.")

            affixes_20_skill_bonus_damage_distribution = (
                self.export_template_damage_analysis_with_affixes_20_skill_bonus(
                    resonator_template, output_methods
                )
            )
            logger_cli.debug(
                "Damage analysis: Affixes 20 Skill BonusSkill Bonus finished."
            )

            template_id_to_affixes_15_1[template_id] = affixes_15_1_damage_distribution
            template_id_to_affixes_20_small[template_id] = (
                affixes_20_small_damage_distribution
            )
            template_id_to_affixes_20_skill_bonus[template_id] = (
                affixes_20_skill_bonus_damage_distribution
            )

            if template.is_tier:
                template_tiers.t.ids.append(template_id)
            if template.is_1_1_tier:
                template_tiers.t_1_1.ids.append(template_id)
            if template.is_2_1_tier:
                template_tiers.t_2_1.ids.append(template_id)
            if template.is_3_1_tier:
                template_tiers.t_3_1.ids.append(template_id)
            if template.is_4_1_tier:
                template_tiers.t_4_1.ids.append(template_id)
            if template.is_5_1_tier:
                template_tiers.t_5_1.ids.append(template_id)
            if template.is_6_1_tier:
                template_tiers.t_6_1.ids.append(template_id)
            if template.is_6_5_tier:
                template_tiers.t_6_5.ids.append(template_id)

            logger_cli.debug(f"Template ID: {template_id} calculated.")

        return (
            template_id_to_relative_url,
            template_id_to_affixes_15_1,
            template_id_to_affixes_20_small,
            template_id_to_affixes_20_skill_bonus,
            template_tiers,
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
        title = f"[{resonator_name}] {title}"
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
        template_id_to_affixes_15_1: Dict[str, TemplateDamageDistributionModel],
        template_id_to_affixes_20_small: Dict[str, TemplateDamageDistributionModel],
        template_id_to_affixes_20_skill_bonus: Dict[
            str, TemplateDamageDistributionModel
        ],
    ):
        template_fpath = "./html/docs/resonator/outline.jinja2"
        template = get_jinja2_template(template_fpath)
        comparisons = self._docs_model.comparisons

        resonator_names = get_resonator_names()
        for resonator_name in resonator_names:
            template_ids = resonator_name_to_template_ids.get(resonator_name, [])
            resonator_info = self._get_resonator_information(resonator_name)
            resonator_no = resonator_info.no
            resonator_comparisons = comparisons.get(resonator_name, None)
            resonator_skills = ResonatorSkillTable(resonator_name).get_skills_model()

            html_str = template.render(
                resonator_no=resonator_no,
                resonator_name=resonator_name,
                resonator_comparisons=resonator_comparisons,
                resonator_skills=resonator_skills,
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
                    SimulationTypeEnum.AFFIXES_15_1.value,
                    comparison.get_md5(),
                    resonator_no,
                    resonator_name,
                    comparison.template_ids,
                    template_id_to_relative_url,
                    template_id_to_affixes_15_1,
                )
                self.export_resonator_comparison(
                    comparison.title,
                    SimulationTypeEnum.AFFIXES_20_SMALL.value,
                    comparison.get_md5(),
                    resonator_no,
                    resonator_name,
                    comparison.template_ids,
                    template_id_to_relative_url,
                    template_id_to_affixes_20_small,
                )
                self.export_resonator_comparison(
                    comparison.title,
                    SimulationTypeEnum.AFFIXES_20_SKILL_BONUS.value,
                    comparison.get_md5(),
                    resonator_no,
                    resonator_name,
                    comparison.template_ids,
                    template_id_to_relative_url,
                    template_id_to_affixes_20_skill_bonus,
                )

    def export_resonators(self, resonator_name_to_template_ids: Dict[str, List[str]]):
        template_fpath = "./html/docs/resonators.jinja2"
        output_fpath = "./build/html/docs/resonators.md"

        template = get_jinja2_template(template_fpath)

        resonator_names = [
            name
            for name in get_resonator_names()
            if name
            not in [_(ZhTwEnum.ROVER_SPECTRO_FEMALE), _(ZhTwEnum.ROVER_HAVOC_FEMALE)]
        ]
        calculated_resonator_names = list(resonator_name_to_template_ids.keys())
        calculated_resonator_names.sort(
            key=lambda name: self._get_resonator_information(name).no
        )
        resonator_names.sort(key=lambda name: self._get_resonator_information(name).no)

        html_str = template.render(
            resonator_names=resonator_names,
            calculated_resonator_names=calculated_resonator_names,
            get_element_icon_url=get_element_icon_url,
            get_resonator_icon_url=get_resonator_icon_url,
            get_resonator_information=self._get_resonator_information,
            get_resonator_outline_url=get_resonator_outline_url,
            ZhTwEnum=ZhTwEnum,
            _=_,
        )

        export_html(output_fpath, html_str)

    def export_tier_outline(
        self,
        docs_tiers: DocsTiersModel,
    ):
        template_fpath = "./html/docs/tier/outline.jinja2"
        output_fpath = "./build/html/docs/tier/outline.md"

        template = get_jinja2_template(template_fpath)

        field_names = docs_tiers.model_fields.keys()

        html_str = template.render(
            docs_tiers=docs_tiers,
            field_names=field_names,
            getattr=getattr,
            get_tier_url=get_tier_url,
            SimulationTypeEnum=SimulationTypeEnum,
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
        message: str = "",
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
            message=message,
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
        docs_tiers: DocsTiersModel,
        template_id_to_relative_url: Dict[str, str],
        template_id_to_affixes_15_1: Dict[str, TemplateDamageDistributionModel],
        template_id_to_affixes_20_small: Dict[str, TemplateDamageDistributionModel],
        template_id_to_affixes_20_skill_bonus: Dict[
            str, TemplateDamageDistributionModel
        ],
    ):
        field_names = docs_tiers.model_fields.keys()

        for field_name in field_names:
            docs_tier: DocsTierModel = getattr(docs_tiers, field_name)
            title = docs_tier.title
            message = docs_tier.msg
            template_ids = docs_tier.ids
            if len(template_ids) == 0:
                continue

            affixes_15_1_title = f"[{_(ZhTwEnum.ECHOES_AFFIXES_15_1)}] {title}"
            affixes_15_1_fpath = get_tier_md_fpath(
                field_name, SimulationTypeEnum.AFFIXES_15_1.value
            )
            self.export_3_resonators_tier_barh(
                affixes_15_1_title,
                template_ids,
                template_id_to_relative_url,
                template_id_to_affixes_15_1,
                affixes_15_1_fpath,
                message=message,
            )

            affixes_20_small_title = f"[{_(ZhTwEnum.ECHOES_AFFIXES_20_SMALL)}] {title}"
            affixes_20_small_fpath = get_tier_md_fpath(
                field_name, SimulationTypeEnum.AFFIXES_20_SMALL.value
            )
            self.export_3_resonators_tier_barh(
                affixes_20_small_title,
                template_ids,
                template_id_to_relative_url,
                template_id_to_affixes_20_small,
                affixes_20_small_fpath,
                message=message,
            )

            affixes_20_skill_bonus = (
                f"[{_(ZhTwEnum.ECHOES_AFFIXES_20_SKILL_BONUS)}] {title}"
            )
            affixes_20_skill_bonus_fpath = get_tier_md_fpath(
                field_name, SimulationTypeEnum.AFFIXES_20_SKILL_BONUS.value
            )
            self.export_3_resonators_tier_barh(
                affixes_20_skill_bonus,
                template_ids,
                template_id_to_relative_url,
                template_id_to_affixes_20_skill_bonus,
                affixes_20_skill_bonus_fpath,
                message=message,
            )
