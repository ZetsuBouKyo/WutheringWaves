from typing import List

from pydantic import BaseModel


class TemplateHtmlResonatorModel(BaseModel):
    name: str = ""
    chain: str = ""
    element: str = ""
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

    resonator_src: str = ""
    element_class_name: str = ""
    element_src: str = ""


class TemplateHtmlOutputMethodModel(BaseModel):
    resonator_name: str = ""
    actions: List[str] = []
