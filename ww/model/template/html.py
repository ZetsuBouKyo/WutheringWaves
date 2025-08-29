from decimal import Decimal
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel

from ww.model.template.base import TemplateModel
from ww.model.template.calculated_row import CalculatedTemplateRowModel
from ww.model.template.damage import TemplateDamageDistributionModel


class TemplateHtmlResonatorModel(BaseModel):
    resonator_src: str = ""
    element: str = ""
    element_src: str = ""
    element_en: str = ""

    name: str = ""
    chain: str = ""
    weapon_name: str = ""
    weapon_rank: str = ""
    weapon_level: str = ""

    level: str = ""
    hp: str = ""
    attack: str = ""
    defense: str = ""
    crit_rate: str = ""
    crit_dmg: str = ""
    energy_regen: str = ""

    resonance_skill_dmg_bonus: str = ""
    basic_attack_dmg_bonus: str = ""
    heavy_attack_dmg_bonus: str = ""
    resonance_liberation_dmg_bonus: str = ""
    healing_bonus: str = ""

    physical_dmg_bonus: str = ""
    glacio_dmg_bonus: str = ""
    fusion_dmg_bonus: str = ""
    electro_dmg_bonus: str = ""
    aero_dmg_bonus: str = ""
    spectro_dmg_bonus: str = ""
    havoc_dmg_bonus: str = ""

    physical_dmg_res: str = ""
    glacio_dmg_res: str = ""
    fusion_dmg_res: str = ""
    electro_dmg_res: str = ""
    aero_dmg_res: str = ""
    spectro_dmg_res: str = ""
    havoc_dmg_res: str = ""

    normal_attack_lv: str = ""
    resonance_skill_lv: str = ""
    resonance_liberation_lv: str = ""
    forte_circuit_lv: str = ""
    intro_skill_lv: str = ""
    inherent_skill_1: str = ""
    inherent_skill_2: str = ""

    def get_element_class_name_for_docs(cls) -> str:
        return f"wuwa-{cls.element_en}"

    echo_hp: str = ""
    echo_hp_p: str = ""
    echo_atk: str = ""
    echo_atk_p: str = ""
    echo_def: str = ""
    echo_def_p: str = ""
    echo_crit_rate: str = ""
    echo_crit_dmg: str = ""
    echo_energy_regen: str = ""
    echo_sonata_1: str = ""
    echo_sonata_2: str = ""
    echo_sonata_3: str = ""
    echo_sonata_4: str = ""
    echo_sonata_5: str = ""
    echo_resonance_skill_dmg_bonus: str = ""
    echo_basic_attack_dmg_bonus: str = ""
    echo_heavy_attack_dmg_bonus: str = ""
    echo_resonance_liberation_dmg_bonus: str = ""
    echo_coordinated_attack_dmg_bonus: str = ""
    echo_echo_dmg_bonus: str = ""
    echo_healing_bonus: str = ""
    echo_glacio_dmg_bonus: str = ""
    echo_fusion_dmg_bonus: str = ""
    echo_electro_dmg_bonus: str = ""
    echo_aero_dmg_bonus: str = ""
    echo_spectro_dmg_bonus: str = ""
    echo_havoc_dmg_bonus: str = ""


class TemplateHtmlOutputMethodActionModel(BaseModel):
    name: str = ""
    src: str = ""
    skill_id: str = ""
    time_start: str = ""
    time_end: str = ""
    index_1_based: str = ""


class TemplateHtmlOutputMethodModel(BaseModel):
    resonator_name: str = ""
    resonator_src: str = ""
    actions: List[TemplateHtmlOutputMethodActionModel] = []
    comments: List[str] = []

    def is_none(cls) -> bool:
        if not cls.resonator_name or len(cls.actions) == 0:
            return True
        return False


class TemplateHtmlDamageAnalysisModel(BaseModel):
    resonator_template: TemplateModel = TemplateModel()
    resonator_models: Dict[str, TemplateHtmlResonatorModel] = {}
    damage_distribution: TemplateDamageDistributionModel = (
        TemplateDamageDistributionModel()
    )
    damage_distributions_with_buffs: List[
        Tuple[str, TemplateDamageDistributionModel]
    ] = []
    calculated_rows: List[CalculatedTemplateRowModel] = []
    output_methods: List[TemplateHtmlOutputMethodModel] = []


class TemplateHtmlEchoComparisonModel(BaseModel):
    resonator_template: TemplateModel = TemplateModel()
    resonator_ids: List[str] = []
    resonator_models: Dict[str, TemplateHtmlResonatorModel] = {}
    damage_distributions: List[TemplateDamageDistributionModel] = []
    base_damage: Decimal = Decimal("0.0")
