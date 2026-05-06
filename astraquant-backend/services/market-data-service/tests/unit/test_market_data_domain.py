from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from astra_common.errors import AppError
from app.domain.services.data_gap_detector import DataGapDetector
from app.domain.services.data_quality_checker import DataQualityChecker
from app.domain.services.funding_rate_normalizer import FundingRateNormalizer
from app.domain.services.instrument_normalizer import InstrumentNormalizer
from app.domain.services.kline_normalizer import KlineNormalizer
from app.domain.services.mark_price_normalizer import MarkPriceNormalizer
from app.domain.services.sync_window_planner import SyncWindowPlanner


def test_kline_normalizer():
    item = KlineNormalizer().normalize({"exchange": "okx", "internal_symbol": "BTC-USDT-SWAP", "exchange_symbol": "BTC-USDT-SWAP", "timeframe": "5m", "timestamp": 1760000000000, "open": "81000", "high": "81200", "low": "80900", "close": "81150", "volume": "123.45", "quote_volume": "10000000"})
    assert item.exchange == "OKX"
    assert item.close == Decimal("81150")


def test_kline_normalizer_invalid_ohlc():
    with pytest.raises(AppError):
        KlineNormalizer().normalize({"exchange": "OKX", "internal_symbol": "BTC-USDT-SWAP", "exchange_symbol": "BTC-USDT-SWAP", "timeframe": "5m", "timestamp": 1760000000000, "open": "81000", "high": "80000", "low": "80900", "close": "81150", "volume": "1", "quote_volume": "1"})


def test_funding_rate_normalizer():
    item = FundingRateNormalizer().normalize({"exchange": "OKX", "internal_symbol": "BTC-USDT-SWAP", "exchange_symbol": "BTC-USDT-SWAP", "funding_rate": "0.0001", "realized_rate": "0.0001", "funding_time": 1760000000000, "next_funding_time": 1760028800000, "mark_price": "81420.1"})
    assert item.funding_rate == Decimal("0.0001")


def test_mark_price_normalizer():
    item = MarkPriceNormalizer().normalize({"exchange": "OKX", "internal_symbol": "BTC-USDT-SWAP", "exchange_symbol": "BTC-USDT-SWAP", "mark_price": "81420.1", "index_price": "81418.9", "timestamp": 1760000000000})
    assert item.index_price == Decimal("81418.9")


def test_instrument_normalizer():
    item = InstrumentNormalizer().normalize({"exchange": "OKX", "internal_symbol": "BTC-USDT-SWAP", "exchange_symbol": "BTC-USDT-SWAP", "contract_type": "swap", "status": "active"})
    assert item.internal_symbol == "BTC-USDT-SWAP"


def test_gap_detector_no_gap():
    start = datetime(2026, 1, 1, tzinfo=UTC)
    times = [start, start + timedelta(minutes=5), start + timedelta(minutes=10)]
    gaps = DataGapDetector().detect(times, start, start + timedelta(minutes=15), "5m")
    assert gaps == []


def test_gap_detector_with_gap():
    start = datetime(2026, 1, 1, tzinfo=UTC)
    gaps = DataGapDetector().detect([start], start, start + timedelta(minutes=15), "5m")
    assert gaps[0]["expected_count"] == 2


def test_quality_checker_pass():
    start = datetime(2026, 1, 1, tzinfo=UTC)
    rows = [{"ts": start, "open": "1", "high": "2", "low": "1", "close": "2"}]
    report = DataQualityChecker().check_klines(rows, "OKX", "BTC-USDT-SWAP", "5m", start, start + timedelta(minutes=5))
    assert report["status"] == "PASS"


def test_quality_checker_failed():
    start = datetime(2026, 1, 1, tzinfo=UTC)
    report = DataQualityChecker().check_klines([], "OKX", "BTC-USDT-SWAP", "5m", start, start + timedelta(hours=1))
    assert report["status"] == "FAILED"


def test_sync_window_planner():
    start = datetime(2026, 1, 1, tzinfo=UTC)
    windows = SyncWindowPlanner().plan_kline_windows(start, start + timedelta(days=20), "5m")
    assert len(windows) == 2
