# McMaster GEEKS Website

The McMaster Geeks official website,

---
## First Stage Objectives
 - [ ] A main CSS file for all pages
 - [ ] Home page with basic information
   - [ ] Should contain information about incoming events
 - [ ] A navigation menu
 - [ ] A template for community pages

 Should host basic information about the community, will not be changing frequently.

 - [ ] An events page with link to each event(?)
 - [ ] Links to our sponsors

 Maybe a brief bio for each, provided by each?

 - [ ] A newsletters page with links to each newsletter/article
 - [ ] Ability to use markdown when posting.
 
## Second Stage

 - [ ] Member sign ups

   Member will sign up to the mailing list. More details can be added later. Can be integrated with discord bot registration.

## Required Packages

 - nginx
 - python(3)-pip
 - python(3)-dev
 - libpq-dev
 - postgresql
 - postgresql-contrib
 - Plus see 'requirements.txt' for python packages

## Install instructions

 For a more general instruction read [this article](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04).
 
 1. Install the required pakages.
 2. Run `gunicorn --access-logfile - --workers n --bind unix:/path/to/socket/file.sock /path/to/myproject.wsgi:application`. Where `n` is the maximum number of worker sub-threads working.
 
     You can create a systemd service using this command. See the linked article for more details.
     
 3. Edit the `nginx-config/sites/defailt.cfg`  to point to the correct files/directories.
 4. Delete the contents of `/etc/nginx/` directory.
 5. Copy the contents of `nginx-config` into `/etc/nginx/`
 6. Start nginx.

---

More to be added!
