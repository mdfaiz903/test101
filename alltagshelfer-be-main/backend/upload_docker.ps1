docker build -t alltagshelfer-be:0.1.0 .
docker tag alltagshelfer-be:0.1.0 europe-west3-docker.pkg.dev/alltagshelfer-381319/alltagshelfer/alltagshelfer-be:0.1.0
docker push europe-west3-docker.pkg.dev/alltagshelfer-381319/alltagshelfer/alltagshelfer-be:0.1.0
