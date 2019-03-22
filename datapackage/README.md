Container for anonymized representations of tracks taken through users through digital services, initially web browser histories, developed for an [open data hackday](https://digitallearninglab.ch/project/60).

Initially generated from a Mozilla browser history exported to CSV form with the [Datapackage.py CLI](https://github.com/frictionlessdata/datapackage-py#cli), like this:

`datapackage infer moz_places_100.csv > datapackage.json`

..then expanded using the http://create.frictionlessdata.io/ tool and hand-tweaked to perfection.

The **data** folder contains a sample file of the author's first 100 browser history entries, contributed here for public education & possibly amusement, processed with the `packager.py` tool in the T2DA project.

## License

The content in this repository is licensed under the CC-BY 4.0 License (see the [LICENSE.md](LICENSE.md) file for details) unless stated otherwise.

[![License: Creative Commons Attribution 4.0](https://licensebuttons.net/l/by/4.0/80x15.png)](https://creativecommons.org/licenses/by/4.0/)
