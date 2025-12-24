# sundance-screenings-2024
## Description
This Python + Selenium script extracts film info and in-person screening times for the 2025 Sundance Film Festival.

This is based on the original 2024 version:
https://github.com/KevinPayravi/sundance-screenings-2024

URLs for all 2025 films are in `urls.py`. Script is in `sundance.py`.

The script outputs two CSV files at the end of execution:
* `output-films-YYYY-MM-DD-HH:MM:SS.csv`, a list of the films and programs. Includes each film's category, description, tags, and credits when available.
  * Note that the individual short films that are within an encompassing program (e.g. short film programs) are not parsed.
* `output-screenings-YYYY-MM-DD-HH:MM:SS.csv`, a list of in-person screenings. Includes screening type (premiere vs screening), time, venue, and city.
