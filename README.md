# Blinkist

## Deployment
```
# https://cloud.google.com/functions/docs/deploying/filesystem
gcloud functions deploy send_email --runtime python37 --trigger-http

# https://cloud.google.com/appengine/docs/standard/python/getting-started/deploying-the-application
gcloud app deploy app.yaml cron.yaml
```

### Cloud Function

Using [environment variables](https://cloud.google.com/functions/docs/env-var):
```
gcloud functions deploy send_email --set-env-vars SENDGRID_API_KEY=$SENDGRID_API_KEY
gcloud functions deploy send_email --env-vars-file .env.yaml
```

Contents of .env.yaml
```
SENDGRID_API_KEY: xxxx
```
