Merchant Routes
====================

The Merchant Routes is an open source application for creating routes for foot merchandisers, couriers, etc.
In Merchant Routes uses Google Maps API (Directions API, Geocoding API)

Main Features
---------------
- Points
  - In db.sqlite3 file includes data on stores «Diksi», «Karusel'», «Perekrestok», «BILLA», «Viktoriya», «TD Holding-Centr»
  - All points you can see in map.
  - You can add additional points in two ways:
    - If you want to add one or more points - this can be done from the UI application.
    - If you need to add many points - use the command:

    python manage.py loadmarket <file.txt>

- Routes
  - Determination of the optimal walking route for given points for a given starting point.
  - Determination of the optimal walking route for the given points with automatic determination of the starting point.
 The starting point is any one of the points that enters the radius zone of the nearest metro station.
  - Display the calculated route on the map.
  - The finished route can be uploaded to the format *.xlsx

Requirements
---------------

  - Python 3.6 or later.
  - Django 2.0 or later.
  - Other requirements you can see in requirements.txt
  - A Google Maps API key.

API keys
~~~~~~~~~~~~~~~~~~~~~~

You can get a API key in https://developers.google.com/maps/web-services/


Running tests

Support
---------------