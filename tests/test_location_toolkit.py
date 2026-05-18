import json
import os
import sys

sys.path.insert(0, os.path.abspath("."))

from app.cosight.tool.location_toolkit import LocationToolkit


def test_extract_street_number_from_chinese_address():
    assert LocationToolkit._extract_street_number("上海市浦东新区碧波路８８９号") == 889


def test_place_street_number_resolve_parses_baidu_place_candidate():
    class FakeToolkit(LocationToolkit):
        def _baidu_place_search(self, query, region, ak, max_results):
            return [
                {
                    "name": "示例研发中心",
                    "address": "上海市浦东新区示例路321号",
                    "province": "上海市",
                    "city": "上海市",
                    "area": "浦东新区",
                    "location": {"lat": 31.0, "lng": 121.0},
                    "uid": "fake",
                }
            ]

    result = json.loads(
        FakeToolkit().place_street_number_resolve(
            query="示例研发中心",
            region="上海",
            baidu_ak="fake-ak",
            use_search_fallback=False,
        )
    )

    assert result["street_number"] == 321
    assert result["address"] == "上海市浦东新区示例路321号"
    assert result["source"] == "baidu_place"
