import csv, sys, os
from datetime import datetime
from datapackage import Package
from urllib.parse import urlparse
from random import shuffle

santaslist = {}
santascount = {}
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
    santaslist['good'] = get_lists_in_dir(os.path.join('sites', 'good'))
    santascount['good'] = sum([len(santaslist['good'][l]) for l in santaslist['good']])
    print("Loaded %d from good lists." % santascount['good'], file=sys.stderr)
    santaslist['ugly'] = get_lists_in_dir(os.path.join('sites', 'ugly'))
    santascount['ugly'] = sum([len(santaslist['ugly'][l]) for l in santaslist['ugly']])
    print("Loaded %d from ugly lists." % santascount['ugly'], file=sys.stderr)

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

def get_date_from_stamp(ds):
    return datetime.utcfromtimestamp(
        int(ds)/1000000
    )

def get_place(row):
    # Conversions
    domain = urlparse(row['url']).hostname
    if not domain: return None
    domain = domain.lower()
    datetimeiso8601 = ''
    if row['last_visit_date']:
        datetimeiso8601 = get_date_from_stamp(
            row['last_visit_date']
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

def generate_summary(places):
    daterange = [int(p['timestamp']) for p in places if p['timestamp'] != '']
    uglylist = [p['domain'] for p in places if p['is_risky']]
    shuffle(uglylist)
    # uglylist = list(sorted(set(uglylist)))
    goodlist = [p['domain'] for p in places if p['is_verified']]
    shuffle(goodlist)
    # goodlist = list(sorted(set(goodlist)))

    return {
      "today": datetime.now().strftime("%d.%m.%y"),
      "count": {
        "total":    len(places),
        "risky":    sum(1 for p in places if p['is_risky']),
        "verified": sum(1 for p in places if p['is_verified'])
      },
      "db": {
        "total":    santascount['good'] + santascount['ugly'],
        "risky":    santascount['ugly'],
        "verified": santascount['good']
      },
      "daterange": {
        "from": datetime.utcfromtimestamp(min(daterange)/1000000).strftime("%d.%m.%y"),
        "to":   datetime.utcfromtimestamp(max(daterange)/1000000).strftime("%d.%m.%y"),
      },
      "risky":    uglylist[0:10],
      "verified": goodlist[0:10]
    }

def generate_stats(places):
    stats = []
    for p in places:
        p_type = 0
        if p['is_verified']: p_type = 1
        if not p['timestamp']: continue
        p_date = get_date_from_stamp(p['timestamp'])
        stats.append({
            'month': p_date.month,
            'hits': 1,
            'type': p_type
        })
    return stats

if __name__ == "__main__":
    main()
