# Tracks to Digital Awareness

A work in progress. You should probably go read the Wiki, or something, until we make this better.

1. Install all the libs:

`pip install -Ur requirements.txt`

2. Put a copy of your database in the `private` folder, or comment out the `test_mode = True` line then run:

`python sqlreader.py`

3. Now pipe the resulting extracted content into our data packager, and save the resulting output, like this:

```
cat private/websites.csv | python packager.py datapackage > datapackage/data/places_100.csv
```

4. ???

5. Profit!!!
