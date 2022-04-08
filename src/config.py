# CoinTaxman
# Copyright (C) 2021  Carsten Docktor <https://github.com/provinzio>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import configparser
from datetime import datetime
from os import environ
from pathlib import Path

from dateutil.relativedelta import relativedelta

import core

# Dir and file paths
BASE_PATH = Path(__file__).parent.parent.absolute()
CONFIG_FILE = BASE_PATH / "config.ini"
ACCOUNT_STATMENTS_PATH = BASE_PATH / "account_statements"
DATA_PATH = BASE_PATH / "data"
EXPORT_PATH = BASE_PATH / "export"
TMP_LOG_FILEPATH = BASE_PATH / "tmp.log"

# General config
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

try:
    COUNTRY = core.Country[config["BASE"].get("COUNTRY", "GERMANY")]
except KeyError as e:
    raise NotImplementedError(
        f"Your country {e} is currently not supported. Please create an Issue or PR."
    )

TAX_YEAR = int(config["BASE"].get("TAX_YEAR", "2021"))
REFETCH_MISSING_PRICES = config["BASE"].getboolean("REFETCH_MISSING_PRICES")
MEAN_MISSING_PRICES = config["BASE"].getboolean("MEAN_MISSING_PRICES")
CALCULATE_UNREALIZED_GAINS = config["BASE"].getboolean("CALCULATE_UNREALIZED_GAINS")
MULTI_DEPOT = config["BASE"].getboolean("MULTI_DEPOT")

# Read in environmental variables.
if _env_country := environ.get("COUNTRY"):
    COUNTRY = core.Country[_env_country]
if _env_tax_year := environ.get("TAX_YEAR"):
    try:
        TAX_YEAR = int(_env_tax_year)
    except ValueError as e:
        raise ValueError(
            "Unable to convert environment variable `TAX_YEAR` to int"
        ) from e

# Country specific constants.
if COUNTRY == core.Country.GERMANY:
    FIAT_CLASS = core.Fiat.EUR
    PRINCIPLE = core.Principle.FIFO

    def IS_LONG_TERM(buy: datetime, sell: datetime) -> bool:
        return buy + relativedelta(years=1) < sell


else:
    raise NotImplementedError(
        f"Your country {COUNTRY} is currently not supported. "
        "Please create an Issue or PR."
    )

# Program specific constants.
FIAT = FIAT_CLASS.name  # Convert to string.
