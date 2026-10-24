from datetime import datetime, timezone
from urllib.parse import urlparse


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


def map_post(item):
    post = item.get("post", {})
    creator = item.get("creator", {})
    community = item.get("community", {})
    counts = item.get("counts", {})
    post_id = post.get("id")
    name = post.get("name", "")
    url = post.get("url") or ""
    body = post.get("body") or ""
    published = post.get("published", "")
    created = to_epoch(published)
    community_name = community.get("name", "")
    community_id = community.get("id")
    creator_name = creator.get("name", "")
    creator_id = creator.get("id")
    score = counts.get("score", 0)
    upvotes = counts.get("upvotes", 0)
    downvotes = counts.get("downvotes", 0)
    comments = counts.get("comments", 0)
    nsfw = bool(post.get("nsfw", False))
    locked = bool(post.get("locked", False))
    domain = ""
    if url:
        try:
            domain = urlparse(url).netloc
        except ValueError:
            domain = ""
    data = {
        "id": str(post_id) if post_id is not None else "",
        "name": f"t3_{post_id}" if post_id is not None else "",
        "title": name,
        "author": creator_name,
        "author_fullname": f"t2_{creator_id}" if creator_id is not None else "",
        "subreddit": community_name,
        "subreddit_name_prefixed": f"r/{community_name}",
        "subreddit_id": f"t5_{community_id}" if community_id is not None else "",
        "url": url,
        "permalink": f"/r/{community_name}/comments/{post_id}/",
        "created_utc": created,
        "created": int(created) if created else 0,
        "score": score,
        "ups": upvotes,
        "downs": downvotes,
        "num_comments": comments,
        "over_18": nsfw,
        "over18": nsfw,
        "locked": locked,
        "archived": False,
        "stickied": False,
        "clicked": False,
        "saved": False,
        "hidden": False,
        "is_self": bool(body),
        "selftext": body,
        "selftext_html": None,
        "thumbnail": "",
        "domain": domain,
        "gilded": 0,
        "total_awards_received": 0,
        "is_video": False,
        "post_hint": "self" if body and not url else "link",
        "spoiler": False,
        "upvote_ratio": 1.0,
        "view_count": None,
        "likes": None,
        "suggested_sort": None,
        "all_awardings": [],
        "awarders": [],
        "media_only": False,
        "can_mod_post": False,
        "is_crosspostable": True,
        "pinned": False,
        "subreddit_type": "public",
        "subreddit_subscribers": 0,
    }
    return {"kind": "t3", "data": data}


def build_post_response(limit, posts):
    children = [map_post(item) for item in posts]
    after = None
    if children:
        last_id = posts[-1].get("post", {}).get("id")
        if last_id is not None:
            after = f"t3_{last_id}"
    return {
        "kind": "Listing",
        "data": {
            "modhash": "",
            "dist": len(children),
            "children": children,
            "after": after,
            "before": None,
            "geo_filter": "",
        },
    }
