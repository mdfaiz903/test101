# Overview

This document describes the services we use and why we use them. How to set up authentication and deploy to google cloud run.

## Used Services
- Google Cloud Run: Running our backend and frontend applications
- Cloud SQL: Hosting our Database
- Cloud SQL Admin API: To manage the database from the backend
- Secret Manager: To securely provide secrets to our container (we had to add the cloud run service user to the secret manager access control list)
- Google Artifact Registry: To host our docker images (1 for the backend, 1 for the frontend), the registry is named alltagshelfer


## Usage
- Download gcloud cli
- Login to gcloud cli after installation using `gcloud auth login`
    - Our region is europe-west3 (Frankfurt)
- Set project using `gcloud config set project alltagshelfer`
- Configure the authentication for docker: `gcloud auth configure-docker europe-west3-docker.pkg.dev`
- For public IP paths, Cloud Run provides encryption and connects using the Cloud SQL Auth proxy through Unix sockets:
    - `gcloud builds submit --tag gcr.io/alltagshelfer-381319/run-sql`
- Cloud SQL Proxy: Used to connect to database on google from your local machine
    - How to Authenticate: https://cloud.google.com/sql/docs/mysql/connect-auth-proxy#authentication-options

## Important Documentation Links
- https://cloud.google.com/sql/docs/postgres/connect-instance-cloud-run
- https://cloud.google.com/artifact-registry/docs/docker/authentication#gcloud-helper
- https://cloud.google.com/sql/docs/postgres/connect-instance-cloud-run#python_1 => client ssl certificate for the DB


## Domain Issues
Mapping Domains to Cloud Run is currently rather difficult and only available in certain regions.

Instead, Google Itself is recommending to map a custom domain to Cloud Run using Firebase Hosting.  
- https://cloud.google.com/run/docs/mapping-custom-domains#firebase