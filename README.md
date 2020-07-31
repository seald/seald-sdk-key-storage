# Seald-SDK-Key-Storage

## Installation

### Docker

```
$ docker build . -t seald/seald-sdk-key-storage
$ docker run --rm -it -p 8000:8000 seald/seald-sdk-key-storage
```

### Configuration

Environments variable:

- `SSKS_BASE_DIR` (default: `/ssks-data`): directory containing data.
- `SSKS_DEBUG` (default: `FALSE`): if set to `TRUE`, `uvicorn` debug mode
will be enabled.

## Usage

- `POST /push/`
  - Push data to be stored
  - Accept a JSON dictionary containing keys `app_id`, `username`, `secret`,
  `data_b64`
  - `app_id`, `username`, `secret` must match `"^[A-Za-z0-9-_]+$"`
  - `data_b64` must match `"^[A-Za-z0-9/=]+$"`
  - If succeeded, return `{"status": "ok"}`
- `POST /search/`
  - Search stored data
  - Accept a JSON dictionary containing keys `app_id`, `username`, `secret`
  - `app_id`, `username`, `secret` must match `"^[A-Za-z0-9-_]+$"`
  - If succeeded, return `{"data_b64": [DATA]}`
