from datetime import datetime, timezone


def to_epoch(value):
    if not value:
        return 0.0
    text = value.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return 0.0
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


def map_community(item):
    community = item.get("community", {})
    counts = item.get("counts", {})
    name = community.get("name", "")
    community_id = community.get("id")
    published = community.get("published", "")
    created = to_epoch(published)
    icon = community.get("icon") or ""
    banner = community.get("banner") or ""
    description = community.get("description") or ""
    nsfw = bool(community.get("nsfw", False))
    restricted = bool(community.get("posting_restricted_to_mods", False))
    data = {
        "id": str(community_id) if community_id is not None else "",
        "name": f"t5_{community_id}" if community_id is not None else "",
        "display_name": name,
        "display_name_prefixed": f"r/{name}",
        "title": community.get("title") or name,
        "public_description": description,
        "description": description,
        "description_html": None,
        "subscribers": counts.get("subscribers", 0),
        "active_user_count": counts.get("users_active_month"),
        "accounts_active": counts.get("users_active_month"),
        "over18": nsfw,
        "over_18": nsfw,
        "quarantine": False,
        "restrict_posting": restricted,
        "restrict_commenting": False,
        "icon_img": icon,
        "banner_img": banner,
        "community_icon": icon,
        "primary_color": "",
        "key_color": "",
        "lang": "en",
        "created_utc": created,
        "created": int(created) if created else 0,
        "url": f"/r/{name}/",
        "subreddit_type": "public",
        "submission_type": "any",
        "spoilers_enabled": False,
        "allow_images": True,
        "allow_videos": True,
        "allow_polls": True,
        "user_is_subscriber": None,
        "user_is_moderator": None,
        "user_is_banned": None,
        "wiki_enabled": None,
    }
    return {"kind": "t5", "data": data}


def build_response(limit, communities):
    children = [map_community(item) for item in communities]
    return {
        "kind": "Listing",
        "data": {
            "modhash": "",
            "dist": len(children),
            "children": children,
            "after": None,
            "before": None,
            "geo_filter": "",
        },
    }
