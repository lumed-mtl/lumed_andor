from dataclasses import asdict
from pathlib import Path

import tomli
import tomli_w
from dacite import from_dict

from lumed_andor.andor_control import AndorSettings


def export_setting(setting: AndorSettings, filepath: Path):
    export_dict = {"andor_setting": asdict(setting)}
    with open(filepath, "wb") as fp:
        tomli_w.dump(export_dict, fp)


def import_setting(filepath: Path) -> AndorSettings:
    with open(filepath, "rb") as fp:
        setting_dict = tomli.load(fp)["andor_setting"]

    print(setting_dict)
    andor_setting = from_dict(data_class=AndorSettings, data=setting_dict)
    return andor_setting


if __name__ == "__main__":

    s = AndorSettings()
    s.acquisition_mode = 2
    s.read_mode = 3
    s.target_exposure_time = 100
    s.target_temperature = -90

    fp_ = Path.home() / "Desktop/test.toml"
    export_setting(s, fp_)

    print(import_setting(fp_))
