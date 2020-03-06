# -*- coding: utf-8 -*-

import os
import re
import shutil
import time

from .. import PKGDIR

# CONFIG_VERSION
__version__ = 1

class ConfigParser:

    """
    holds and manage the configuration.
    current dict layout:
    {

     section : {
      option : {
            value:
            type:
            desc:
      }
      desc:

    }
    """

    _CONFLINE = re.compile(
        r'\s*(?P<T>.+?)\s+(?P<N>[^ ]+?)\s*:\s*"(?P<D>.+?)"\s*=\s?(?P<V>.*)'
    )
    _VERSION = re.compile(r"\s*version\s*:\s*(\d+)")

    def __init__(self, userdir):
        """
        Constructor.
        """
        from ..utils.logger import getLogger
        self.log = getLogger('error', level='ERROR')
        
        self.config = {}  #: the config values

        configdir = os.path.join(userdir, "settings")
        os.makedirs(configdir, exist_ok=True)

        self.configpath = os.path.join(configdir, "pycrawler.conf")

        self.check_version()

        self.read_default_config()

    def check_version(self, n=0):
        """
        determines if config need to be copied.
        """
        try:
            if not os.path.exists(self.configpath):
                os.makedirs(os.path.dirname(self.configpath), exist_ok=True)
                shutil.copy(
                    os.path.join(PKGDIR, "config", "default.conf"),
                    self.configpath,
                )
                os.chmod(self.configpath, 0o600)

            with open(self.configpath) as fp:
                content = fp.read()

            m_ver = self._VERSION.search(content)
            if m_ver is None or int(m_ver.group(1)) < __version__:
                shutil.copy(
                    os.path.join(PKGDIR, "config", "default.conf"),
                    self.configpath,
                )
                print("Old version of config was replaced")

        except Exception:
            if n < 3:
                time.sleep(1)
                self.check_version(n + 1)
            else:
                raise

    def read_default_config(self):
        """
        reads the config file.
        """
        self.config = self.parse_config(
            os.path.join(PKGDIR, "config", "default.conf")
        )

        try:
            homeconf = self.parse_config(self.configpath)
            self.update_values(homeconf, self.config)
        except Exception as exc:
            self.log.exception(exc)

    def parse_config(self, config):
        """
        parses a given configfile.
        """
        with open(config) as fp:

            config = fp.read()

            config = config.splitlines()[1:]

            conf = {}

            section, option, value, typ, desc = "", "", "", "", ""

            listmode = False

            for line in config:
                comment = line.rfind("#")
                if (
                    line.find(":", comment) < 0 > line.find("=", comment)
                    and comment > 0
                    and line[comment - 1].isspace()
                ):
                    line = line.rpartition("#")  #: removes comments
                    if line[1]:
                        line = line[0]
                    else:
                        line = line[2]

                line = line.strip()

                try:
                    if line == "":
                        continue
                    elif line.endswith(":"):
                        section, none, desc = line[:-1].partition("-")
                        section = section.strip()
                        desc = desc.replace('"', "").strip()
                        conf[section] = {"desc": desc}
                    else:
                        if listmode:
                            if line.endswith("]"):
                                listmode = False
                                line = line.replace("]", "")

                            value += [
                                self.cast(typ, x.strip()) for x in line.split(",") if x
                            ]

                            if not listmode:
                                conf[section][option] = {
                                    "desc": desc,
                                    "type": typ,
                                    "value": value,
                                }

                        else:
                            m = self._CONFLINE.search(line)

                            typ = m.group("T")
                            option = m.group("N")
                            desc = m.group("D").strip()
                            value = m.group("V").strip()

                            if value.startswith("["):
                                if value.endswith("]"):
                                    listmode = False
                                    value = value[:-1]
                                else:
                                    listmode = True

                                value = [
                                    self.cast(typ, x.strip())
                                    for x in value[1:].split(",")
                                    if x
                                ]
                            else:
                                value = self.cast(typ, value)

                            if not listmode:
                                conf[section][option] = {
                                    "desc": desc,
                                    "type": typ,
                                    "value": value,
                                }

                except Exception as exc:
                    self.log.exception(exc)

        return conf

    def update_values(self, config, dest):
        """
        sets the config values from a parsed config file to values in destination.
        """
        for section in config.keys():
            if section in dest:
                for option in config[section].keys():
                    if option in ("desc", "outline"):
                        continue

                    if option in dest[section]:
                        dest[section][option]["value"] = config[section][option][
                            "value"
                        ]

                        # else:
                        #    dest[section][option] = config[section][option]

                        # else:
                        #    dest[section] = config[section]

    def save_config(self, config, filename):
        """
        saves config to filename.
        """
        with open(filename, mode="w") as fp:
            os.chmod(filename, 0o600)
            fp.write(f"version: {__version__} \n")
            for section in sorted(config.keys()):
                fp.write(f'\n{section} - "{config[section]["desc"]}":\n')

                for option, data in sorted(
                    config[section].items(), key=lambda _x: _x[0]
                ):
                    if option in ("desc", "outline"):
                        continue

                    if isinstance(data["value"], list):
                        value = "[ \n"
                        for x in data["value"]:
                            value += f"\t\t{x},\n"
                        value += "\t\t]\n"
                    else:
                        value = str(data["value"]) + "\n"

                    fp.write(f'\t{data["type"]} {option} : "{data["desc"]}" = {value}')

    def cast(self, typ, value):
        """
        cast value to given format.
        """
        if typ == "int":
            return int(value)

        elif typ == "float":
            return float(value)

        elif typ == "str":
            return "" if value is None else str(value)

        elif typ == "bytes":
            return b"" if value is None else bytes(value)

        elif typ == "bool":
            value = "" if value is None else str(value)
            return value.lower() in ("1", "true", "on", "yes", "y")

        elif typ == "time":
            value = "" if value is None else str(value)
            if not value:
                value = "0:00"
            if ":" not in value:
                value += ":00"
            return value

        elif typ in ("file", "folder"):
            return os.path.realpath("" if value is None else os.fsdecode(value))

        else:
            return value

    def save(self):
        """
        saves the configs to disk.
        """
        self.save_config(self.config, self.configpath)

    def __getitem__(self, section):
        """
        provides dictonary like access: c['section']['option']
        """
        return Section(self, section)

    def get(self, section, option):
        """
        get value.
        """
        return self.config[section][option]["value"]

    def set(self, section, option, value):
        """
        set value.
        """
        value = self.cast(self.config[section][option]["type"], value)

        self.config[section][option]["value"] = value
        self.save()

    def toggle(self, section, option):
        self.set(section, option, self.get(section, option) ^ True)

    def get_meta_data(self, section, option):
        """
        get all config data for an option.
        """
        return self.config[section][option]


class Section:
    """
    provides dictionary like access for configparser.
    """

    def __init__(self, parser, section):
        """
        Constructor.
        """
        self.parser = parser
        self.section = section

    def __getitem__(self, item):
        """
        getitem.
        """
        return self.parser.get(self.section, item)

    def __setitem__(self, item, value):
        """
        setitem.
        """
        self.parser.set(self.section, item, value)
