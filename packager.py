import csv, sys, os
from datetime import datetime
from datapackage import Package
from urllib.parse import urlparse

spamwriter = csv.writer(sys.stdout)

if len(sys.argv) < 2:
    print("Path to Data Package required!", file=sys.stderr)
    exit()
BASE_PATH = sys.argv[1]

def main():
    # Schema reader
    package = Package(
        os.path.join(BASE_PATH, 'datapackage.json'),
        base_path=BASE_PATH
    )
    print("Loaded Data Package %s v%s" %
        (package.descriptor['name'],
         package.descriptor['version']), file=sys.stderr)

    schema = package.descriptor['resources'][0]['schema']
    fields = [f['name'] for f in schema['fields']]

    reader = csv.reader(sys.stdin)
    headers = next(reader, None)
    col = []
    for h in headers: col.append(h)

    print("Input: %r" % (col), file=sys.stderr)
    print("Output: %r" % (fields), file=sys.stderr)
    spamwriter.writerow(fields)

    rowcount = 0
    for r in reader:
        row = {}
        for i, h in enumerate(col): row[h] = r[i]
        # print("Row: %r" % (row))

        place = get_place(row)
        if place is None: continue

        spamwriter.writerow([place[f] for f in fields])
        rowcount = rowcount + 1

    print("Wrote %d rows. Have a nice day!" % rowcount, file=sys.stderr)

def get_place(row):
    # Conversions
    domain = urlparse(row['url']).hostname
    if not domain: return None
    datetimeiso8601 = ''
    if row['last_visit_date']:
        datetimeiso8601 = datetime.utcfromtimestamp(
            int(row['last_visit_date'])/1000000
        ).isoformat()

    category, is_risky, is_verified = evaluate_domain(domain)

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

def evaluate_domain(domain):
    category = ''
    is_risky = True
    is_verified = False
    return category, is_risky, is_verified

if __name__ == "__main__":
    main()
