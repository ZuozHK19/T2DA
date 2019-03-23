# Tracks to Digital Awareness

A work in progress. More details can be found [in the wiki](https://github.com/ZuozHK19/T2DA/wiki/Project-Idea)

## Instructions

1) Install all the libs:

`pip install -Ur requirements.txt`

2) Close your browser and run our graphical client:

`python GUI.py`

3) Push the button.

## Console instructions

You can also use our tool on the command line:

1) Close your browser, then run:

`python sqlreader.py`

Optionally put a copy of your cached SQLite database in the `private` folder if you want to keep your browser running.

2) Now pipe the resulting extracted content into our data packager, and save the resulting output, like this:

```
cat private/websites.csv | python packager.py datapackage > datapackage/data/places_100.csv
```
3) Look at the contents of the `datapackage` folder for the resulting (anonymized) data and report.

4) ???

5) Profit!!!
