from notion_client import notion_post


# DATABASE LOOKUPS


def fetch_relation_lookup(database_id, title_property_name):

payload = {

"page_size": 100

}


results = notion_post(f"/databases/{database_id}/query", payload)

lookup = {}


if not results:

return lookup


for row in results.get("results", []):

props = row.get("properties", {})


if title_property_name not in props:

continue


title_data = props[title_property_name].get("title", [])

if not title_data:

continue


title = "".join(

[x.get("plain_text", "") for x in title_data]

).strip()


if title:

lookup[title] = row["id"]


return lookup
