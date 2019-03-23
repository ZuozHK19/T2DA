# Tracks to Digital Awareness

A work in progress. You should probably go read the Wiki, or something, until we make this better.

0. Get some lists of URLs/domains (in plain text form, one domain per line) and put them into *sites/good* and *sites/ugly* folders. We have some examples there to get you started. Here are some additional locations:

- http://www.phishtank.com/developer_info.php
- http://s3-us-west-1.amazonaws.com/umbrella-static/index.html
- https://filterlists.com/ (e.g. [uBlockFiltersPlus.txt](https://raw.githubusercontent.com/deathbybandaid/piholeparser/master/Subscribable-Lists/ParsedBlacklists/uBlockFiltersPlus.txt))
- https://github.com/fake-news-detector/api/issues/10
- https://opendata.rapid7.com/sonar.fdns_v2/

1. Install all the libs:

`pip install -Ur requirements.txt`

2. Put a copy of your cached database in the `private` folder, or comment out the `test_mode = True` line then run:

`python sqlreader.py`

3. Now pipe the resulting extracted content into our data packager, and save the resulting output, like this:

```
cat private/websites.csv | python packager.py datapackage > datapackage/data/places_100.csv
```

4. ???

5. Profit!!!
