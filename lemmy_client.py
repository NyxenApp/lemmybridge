import json
import urllib.request

from config import load_instance


def fetch_communities(limit):
    instance = load_instance()
    url = f"{instance}/api/v3/community/list?sort=TopAll&type_=All&limit={limit}"
    req = urllib.request.Request(url, headers={"User-Agent": "lemmybridge/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    return payload.get("communities", [])
