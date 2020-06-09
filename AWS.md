= How to set up in AWS

1. need 2 ECR repos, one for postgres, one for reviewbot
1. the ECS cluster used must be ec2 because this project relies on docker links
1. The task definition needs to set these env vars on the containers:
 1. `POSTGRES_PASSWORD` (must be identical on both the postgres and reviewbot containers)
 1. `SLACK_BOT_ACCESS_TOKEN` (the access token from slack)
 1. `SLACK_BOT_USER_TOKEN` (user token from slack)
 1. These should all be done in SSM to avoid compromising sekrits

All of this is currently set up in relab, look for resources in the above services with the 'reviewbot' namespace
