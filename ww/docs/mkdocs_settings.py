import yaml


class MkdocsSettings:

    def __init__(self, mkdocs_settings: dict, mkdocs_fpath: str):
        self._mkdocs_settings = mkdocs_settings
        self._mkdocs_fpath = mkdocs_fpath

        self.update_resonator_outline()

    def save(self):
        with open(self._mkdocs_fpath, "w", encoding="utf-8") as fp:
            yaml.dump(
                self._mkdocs_settings,
                fp,
                allow_unicode=True,
                default_flow_style=False,
                encoding="utf-8",
                indent=2,
                sort_keys=False,
            )

    def update_resonator_outline(self):
        self._mkdocs_settings["nav"].append({"共鳴者": [{"概要": "resonators.md"}]})
