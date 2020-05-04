# Reviewbot!

This bot will manage a list of code reviews for your team, allowing users to add/remove/list them.  This makes it easy for developers to register new reviews and then have reviewers come along later and find code to look at without anyone having to *gasp* talk to other people.

# Development/Deployment

This is designed to be run in docker, the docker-compose file describes the configuration.

The deployment needs the following environment variables to be set in order to run properly:
  1. SLACK_BOT_USER_TOKEN: the auth token for slack
  1. POSTGRES_PASSWORD: password for accessing the postgres container defined in docker-compose.yml

It can be started locally as follows:
```
sudo docker-compose SLACK_BOT_USER_TOKEN=$SLACK_BOT_USER_TOKEN POSTGRES_PASSWORD=$POSTGRES_PASSWORD up -d
```

The bot is split into two parts, the bot and a basic data layer.  The bot implements all the commands and starts the slack connection, the data layer does what it does best.

# Testing
There aren't any tests currently, but when developing, call all the basic commands to make sure they still work

# Future improvements

1. formatting sucks
1. multiple tags per review
1. add optional syntax to tag a user or users on review completion (something like "@reviewbot followup add <review ID> <user handle>")
