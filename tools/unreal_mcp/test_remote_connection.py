from __future__ import annotations

import json

import ue_remote


if __name__ == "__main__":
    print(json.dumps(ue_remote.discover(wait_seconds=2.5), ensure_ascii=False, indent=2))
