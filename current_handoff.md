# Pytrader Weekly Options Handoff

**Date:** 2026-04-14
**Source Repo:** `sanprat/Signalcraft`
**Latest Verified Commit:** `84d2742`

## Confirmed

- `data-scripts/dhan_client.py`
  - `REQUIRED_DATA` includes `oi`, `iv`, `spot`, `strike`
  - `get_expiry_list()` uses Dhan payload:
    - `{"UnderlyingScrip": SECURITY_IDS[index], "UnderlyingSeg": "IDX_I"}`
  - `get_expiry_list()` now handles both response shapes:
    - `{"data": ["2025-04-24", ...]}`
    - `{"data": {"expiryDates": ["2025-04-24", ...]}}`

- Canonical options parquet schema is in place across:
  - `data-scripts/parquet_writer.py`
  - `data-scripts/daily_updater.py`
  - `data-scripts/dhan_bulk_loader.py`
  - schema: `time, open, high, low, close, volume, oi, iv, spot`

- Compatibility:
  - old 6-column parquet remains readable
  - new 9-column parquet is writable/readable

- `data-scripts/options_audit.py`
  - fixed `ec10/ec11` being miscounted as `ec1`
  - fixed timestamp-overlap logic to use real range comparison
  - current production verdict is `partially_ready`

- Tests:
  - `data-scripts/test_options_infrastructure.py` passing locally

## Verified On VPS

- Historical expired weekly options data already exists under `/app/data`
- Underlying data exists for `NIFTY`, `BANKNIFTY`, `FINNIFTY`
- `get_expiry_list("NIFTY")` works after parser fix
- `options_audit.py` reports:
  - historical options coverage present
  - no current-week `ec0` files present
  - final verdict: `PARTIALLY_READY`

## Current Blockers

1. `data-scripts/dhan_bulk_loader.py` fails in Docker because `tqdm` is missing from the backend container environment.
2. `data-scripts/daily_updater.py --fno-live-only` returns all empty results in production.
3. Current-week `ec0` ingestion is therefore not production-valid yet.

## Immediate Next Actions

1. Add `tqdm` to the backend/container dependencies and rebuild the backend image.
2. Debug live current-week options retrieval in `daily_updater.py` / `dhan_client.py`.
3. Treat `rollingoption` with `expiry_code=0` as unproven for live weekly options until real data is confirmed.
4. Keep audit verdict as `partially_ready` until `ec0` files are actually populated.

## Useful Production Commands

```bash
docker exec -it signalcraft-backend /bin/sh -c 'cd /app && python data-scripts/options_audit.py'
docker exec -it signalcraft-backend /bin/sh -c 'cd /app && python data-scripts/dhan_bulk_loader.py --expiries 26'
docker exec -it signalcraft-backend /bin/sh -c 'cd /app && python data-scripts/daily_updater.py --fno-live-only'
```
