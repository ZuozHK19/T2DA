import csv, sys, os
from datetime import datetime
from datapackage import Package
from urllib.parse import urlparse

spamwriter = csv.writer(sys.stdout)

if len(sys.argv) < 2:
    print("Path to Data Package required!", file=sys.stderr)
    exit()
BASE_PATH = sys.argv[1]

santaslist = {}
def get_lists_in_dir(subfolder):
    data = {}
    for (dirpath, dirnames, filenames) in os.walk(subfolder):
        for fn in filenames:
            with open(os.path.join(dirpath, fn), newline='') as f:
                title = fn.rstrip('.txt')
                data[title] = [
                    urlparse( x.strip() ).hostname or x.strip()
                    for x in f.readlines()
                ]
                print("%d %s %s" % (len(data[title]), title, subfolder), file=sys.stderr)
    return data

def main():
    print("Loading good lists ...", file=sys.stderr)
    santaslist['good'] = get_lists_in_dir(os.path.join('sites', 'good'))
    print("Loading ugly lists ...", file=sys.stderr)
    santaslist['ugly'] = get_lists_in_dir(os.path.join('sites', 'ugly'))

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

    # print("Input: %r" % (col), file=sys.stderr)
    # print("Output: %r" % (fields), file=sys.stderr)
    spamwriter.writerow(fields)

    places = []
    rowcount = 0
    for r in reader:
        row = {}
        for i, h in enumerate(col): row[h] = r[i]

        place = get_place(row)
        if place is None: continue
        places.append(place)

        spamwriter.writerow([place[f] for f in fields])
        rowcount = rowcount + 1

    if rowcount is 0:
        print("Uh-oh! Nothing to write home about.", file=sys.stderr)
    else:
        c_risky    = sum(1 for p in places if p['is_risky'])
        c_verified = sum(1 for p in places if p['is_verified'])
        print("Verified: %d, Risky: %d" % (c_verified, c_risky), file=sys.stderr)
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

    return {
        "domain": domain,
        "title": row['title'] or '',
        "timestamp": row['last_visit_date'] or '',
        "datetime": datetimeiso8601 or '',
        "description": row['description'] or '',
        "image_url": row['preview_image_url'] or '',
        "category": category or '',
        "is_risky": is_risky,
        "is_verified": is_verified,
    }

def evaluate_domain(domain):
    category = None
    is_risky = False
    is_verified = False
    for l in santaslist['good']:
        # Include subdomains
        for d in santaslist['good'][l]:
            if domain.endswith(d):
                # print("%r %r" % (domain, d), file=sys.stderr)
                is_verified = True
                category = l
                break
    if not is_verified:
        for l in santaslist['ugly']:
            # Exact matches
            if domain in santaslist['ugly'][l]:
                # print(domain, file=sys.stderr)
                is_risky = True
                category = l
                break
    return category, is_risky, is_verified

if __name__ == "__main__":
    main()
