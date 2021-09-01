# Alexa Skill - Spreadsheet Organizer

<p align="center">
  <img alt="Icon" src="images/illustration.jpg" width="60%">
</p>

## :dizzy: About

This Open-Source Alexa Skill will help you to manage spreadsheets on Google Sheets. You can perform this skill on any Amazon Echo device.

You can find spreadsheet templates at **source/samples**.

_Use cases:_

- [Diet spreadsheet](source/samples/diet_spreadsheet.xlsx): You can ask for Alexa your last meal and add a new meal

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

## :wrench: Build

```bash
sam build
```

## :mag_right: Local Test

```bash
sam local invoke SpreadsheetOrganizerFunction --env-vars config/config.json --event tests/launchrequest-event.json

sam local invoke SpreadsheetOrganizerFunction --env-vars config/config.json --event tests/intentrequest-event.json
```

## :cloud: Deploy

```bash
sam deploy --stack-name spreadsheet-organizer-skill --resolve-s3 --capabilities CAPABILITY_IAM --parameter-overrides ParameterKey=GOOGLESPREADSHEETID,ParameterValue="$(jq -r '.Parameters.GOOGLESPREADSHEETID' 'config/config.json')" ParameterKey=SPREADSHEETRANGE,ParameterValue="$(jq -r '.Parameters.SPREADSHEETRANGE' 'config/config.json')" ParameterKey=GOOGLESHEETAPIKEY,ParameterValue="$(jq -r '.Parameters.GOOGLESHEETAPIKEY' 'config/config.json')" ParameterKey=SKILLID,ParameterValue="$(jq -r '.Parameters.SKILLID' 'config/config.json')"
```

## :scroll: License Summary

[![CC0](https://i.creativecommons.org/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)

## :heart: Contributors

<table>
  <tr>
<td align="center"><a href="https://github.com/gabrielmartinigit"><img style="border-radius: 100%; " src="https://avatars2.githubusercontent.com/u/30352127?s=460&u=aeb656ad7a9ba7c7531db7bdd65ff76d5a452753&v=4" width="100px; " alt=""/><br /><sub><b>Gabriel Martini</b></sub></a><br /></td>
  </tr>
</table>
