from __future__ import annotations

import pytest

from myelectricaldatapy import EnedisAnalytics

from .consts import DATASET_30 as DS_30
from .consts import DATASET_DAILY as DS_DAILY
from .consts import DATASET_DAILY_COMPARE as DS_COMPARE

PDL = "012345"
TOKEN = "xxxxxxxxxxxxx"


@pytest.mark.asyncio
async def test_hours_analytics() -> None:
    """Test analytics compute."""
    dataset = DS_30["meter_reading"]["interval_reading"]
    cumsum = 1000
    intervals = [("01:30:00", "08:00:00"), ("12:30:00", "14:00:00")]
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        freq="H",
        groupby=True,
        summary=True,
        cumsum=cumsum,
        prices=(0.17, 0.18),
    )
    assert resultat[0]["notes"] == "HC"
    assert resultat[0]["value"] == 0.618
    assert resultat[0].get("sum_value") is not None
    assert resultat[0].get("sum_price") is not None
    print(resultat)

    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        freq="H",
        groupby=True,
        prices=(0.17, 0.18),
    )
    assert resultat[0]["notes"] == "HC"
    assert resultat[0]["value"] == 0.618
    assert resultat[2]["price"] == 0.55152
    assert resultat[0].get("sum_value") is None
    print(resultat)

    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=True,
        intervals=intervals,
        freq="H",
        groupby=True,
        prices=(0.17, 0.18),
    )
    print(resultat)

    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        freq="30T",
        groupby=True,
    )
    assert resultat[48]["notes"] == "HP"
    assert resultat[48]["value"] == 0.672
    print(resultat)

    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        freq="H",
        groupby=True,
    )
    assert resultat[27]["value"] == 0.672
    assert resultat[28]["value"] == 0.624
    print(resultat)

    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        freq="D",
        groupby=True,
        summary=True,
        cumsum=cumsum,
        prices=(0.17, 0.18),
    )
    assert resultat[0]["value"] == 33.951
    assert resultat[3]["value"] == 43.608
    print(resultat)


@pytest.mark.asyncio
async def test_daily_analytics() -> None:
    dataset = DS_30["meter_reading"]["interval_reading"]
    cumsum = 0
    intervals = [("01:30:00", "08:00:00"), ("12:30:00", "14:00:00")]
    dataset = DS_DAILY["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        freq="D",
        groupby=True,
        summary=True,
        cumsum=cumsum,
        prices=(0.17, 0.18),
    )
    assert resultat[359]["value"] == 68.68
    print(resultat)


@pytest.mark.asyncio
async def test_compare_analytics() -> None:
    cumsum = 0
    intervals = [("01:30:00", "08:00:00"), ("12:30:00", "14:00:00")]
    dataset = DS_30["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat1 = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        freq="D",
        groupby=True,
        summary=True,
        cumsum=cumsum,
        prices=(0.17, 0.18),
        start_date="2023-02-28",
    )
    print(resultat1)
    sum_value = 0
    for rslt in resultat1:
        sum_value = sum_value + rslt["value"]

    sum_value_1 = resultat1[2]["sum_value"] + resultat1[5]["sum_value"]
    assert sum_value == sum_value_1
    dataset = DS_COMPARE["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat2 = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        freq="D",
        groupby=True,
        summary=True,
        cumsum=cumsum,
        prices=(0.17, 0.18),
        start_date="2023-02-28",
    )
    assert sum_value == resultat2[2]["sum_value"]
    print(resultat2)