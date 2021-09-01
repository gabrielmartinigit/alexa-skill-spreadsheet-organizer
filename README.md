# Alexa Skill - Spreadsheet Organizer

## About

_Pre-requisites:_

- [Alexa Developer Account](https://developer.amazon.com/alexa/alexa-skills-kit)
- [Alexa Custom Skill](https://developer.amazon.com/docs/alexa/devconsole/create-a-skill-and-choose-the-interaction-model.html)
- Python 3.7
- [jq](https://stedolan.github.io/jq/tutorial/)
- Docker
- AWS Account
- [AWS CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started-set-up-credentials.html)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Google Account
- [Google Cloud Platform project](https://developers.google.com/workspace/guides/create-project)
- [Google Sheet credentials](https://developers.google.com/workspace/guides/create-credentials)
- Update values in **config/config.json** file

## Build

```bash
sam build
```

## Local Test

```bash
sam local invoke SpreadsheetOrganizerFunction --env-vars config/config.json --event tests/launchrequest-event.json

sam local invoke SpreadsheetOrganizerFunction --env-vars config/config.json --event tests/intentrequest-event.json
```

## Deploy

```bash
sam deploy --stack-name spreadsheet-organizer-skill --resolve-s3 --capabilities CAPABILITY_IAM --parameter-overrides ParameterKey=GOOGLESPREADSHEETID,ParameterValue="$(jq -r '.Parameters.GOOGLESPREADSHEETID' 'config/config.json')" ParameterKey=SPREADSHEETRANGE,ParameterValue="$(jq -r '.Parameters.SPREADSHEETRANGE' 'config/config.json')" ParameterKey=GOOGLESHEETAPIKEY,ParameterValue="$(jq -r '.Parameters.GOOGLESHEETAPIKEY' 'config/config.json')" ParameterKey=SKILLID,ParameterValue="$(jq -r '.Parameters.SKILLID' 'config/config.json')"
```

## License Summary

[![CC0](https://i.creativecommons.org/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)
