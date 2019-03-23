import csv, sys, os
from datetime import datetime
from datapackage import Package
from urllib.parse import urlparse


santaslist = {}
def get_lists_in_dir(subfolder):
    data = {}
    for (dirpath, dirnames, filenames) in os.walk(subfolder):
        for fn in filenames:
            with open(os.path.join(dirpath, fn), newline='') as f:
                title = fn.rstrip('.txt')
                data[title] = []
                for x in f.readlines():
                    xl = (urlparse( x.strip() ).hostname or x.strip()).lower()
                    if len(xl) > 1: data[title].append(xl)
                print("%d %s %s" % (len(data[title]), title, subfolder), file=sys.stderr)
    return data

def load_lists():
        if 'good' in santaslist: return
        # Load the filter lists
        print("Loading good lists ...", file=sys.stderr)
        santaslist['good'] = get_lists_in_dir(os.path.join('sites', 'good'))
        print("Loading ugly lists ...", file=sys.stderr)
        santaslist['ugly'] = get_lists_in_dir(os.path.join('sites', 'ugly'))

def process(BASE_PATH, reader):
    # Schema reader
    package = Package(
        os.path.join(BASE_PATH, 'datapackage.json'),
        base_path=BASE_PATH
    )
    schema = package.descriptor['resources'][0]['schema']
    fields = [f['name'] for f in schema['fields']]
    print("Loaded Data Package %s v%s" %
        (package.descriptor['name'],
         package.descriptor['version']), file=sys.stderr)

    # Get headers to start parsing CSV
    headers = next(reader, None)
    col = []
    for h in headers: col.append(h)
    # print("Input: %r" % (col), file=sys.stderr)

    return package, fields, col

def save_output(spamwriter, fields, places):
    # print("Output: %r" % (fields), file=sys.stderr)
    rowcount = len(places)

    if rowcount is 0:
        print("Uh-oh! Nothing to write home about.", file=sys.stderr)
    else:

        # Write the first row
        spamwriter.writerow(fields)
        for place in places:
            spamwriter.writerow([place[f] for f in fields])

        print("Wrote %d rows. Have a nice day!" % rowcount, file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        print("Path to Data Package required!", file=sys.stderr)
        exit()
    BASE_PATH = sys.argv[1]
    reader = csv.reader(sys.stdin)
    package, fields, col = process(BASE_PATH, reader)
    load_lists()
    places = get_places(reader, col)
    
    spamwriter = csv.writer(sys.stdout)
    save_output(spamwriter, fields, places)

def get_places(reader, col):
    places = []
    for r in reader:
        row = {}
        for i, h in enumerate(col): row[h] = r[i]
        # Parse the incoming row
        place = get_place(row)
        if place is None: continue
        places.append(place)
    return places

def get_place(row):
    # Conversions
    domain = urlparse(row['url']).hostname
    if not domain: return None
    domain = domain.lower()
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
