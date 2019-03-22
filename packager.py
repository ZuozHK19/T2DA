import csv, sys
from datetime import datetime
from datapackage import Package
from urllib.parse import urlparse

package = Package('datapackage/datapackage.json', base_path='datapackage')
# print("Loaded Data Package %s v%s" % (package.descriptor['name'], package.descriptor['version']))
schema = package.descriptor['resources'][0]['schema']
fields = [f['name'] for f in schema['fields']]
print(",".join(fields))

reader = csv.reader(sys.stdin)
headers = next(reader, None)
col = []
for h in headers: col.append(h)
# print("Header: %r" % (col))

rowcount = 0
for r in reader:
    row = {}
    for i, h in enumerate(col): row[h] = r[i]
    # print("Row: %r" % (row))

    # Conversions
    domain = urlparse(row['url']).hostname
    if not domain: continue
    datetimeiso8601 = ''
    if row['last_visit_date']:
        datetimeiso8601 = datetime.utcfromtimestamp(
            int(row['last_visit_date'])/1000000
        ).isoformat()
    category = ''
    is_risky = True
    is_verified = False

    place = {
        "domain": domain,
        "title": row['title'] or '',
        "timestamp": row['last_visit_date'] or '',
        "datetime": datetimeiso8601 or '',
        "description": row['description'] or '',
        "image_url": row['preview_image_url'] or '',
        "category": category,
        "is_risky": str(is_risky),
        "is_verified": str(is_verified),
    }

    output = ",".join(["%r"%place[f] for f in fields])
    print(output)

    rowcount = rowcount + 1
