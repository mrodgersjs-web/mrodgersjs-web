---
source: https://www.youtube.com/watch?v=4wgyBYllC5c
video_id: 4wgyBYllC5c
channel: Funnel
title: "Getting started with Funnel: Activate your marketing data with CAPI"
scraped: 2026-08-28
tags: [product-growth, capi, first-party-data, marketing-attribution, conversion-tracking]
---
# Getting started with Funnel: Activate your marketing data with CAPI

A walkthrough of using Funnel’s Activate Conversion API (CAPI) feature to send first-party conversion data from your source of truth back to ad platforms, improving attribution, ROAS, and campaign performance amid signal loss.

## Procedure / models distilled
- Treat first-party CRM and offline conversion data as the most accurate signal in a privacy-restricted, third-party-cookie-declining landscape.
- Import your conversion source-of-truth data into Funnel via the Connect section before attempting an upload.
- Open Activate → Create a Conversion Upload and select the destination ad platform.
- Pre-create the conversion action on the ad platform side, since most platforms require this before receiving data.
- Select the correct platform credentials and the matching conversion action that defines which “bucket” the conversions land in.
- Map at least one user identifier field so the ad platform can match conversions to real users and strengthen attribution.
- Map conversion time and conversion value fields using either platform-native fields or custom fields already built in Funnel.
- Use advanced settings to customize scheduling cadence so uploads align with operational and reporting needs.
- Preview the mapped dataset before creating and uploading to validate the output.
- Return to the upload details page to monitor status and ongoing health.
- Use CAPI uploads to feed the ad platform algorithms fresh conversion signals, aiming for more conversions and lower cost per action.
- Focus budget on customers that drive revenue rather than optimizing for website clicks alone.

## Failure modes named
- Sending conversion data without setting up the corresponding conversion action on the ad platform first.
- Mapping uploads without at least one user identifier, which prevents match-back and weakens attribution.
- Optimizing campaigns on clicks or proxy signals instead of actual revenue-driving conversions.
- Continuing to rely primarily on third-party cookies as privacy restrictions reduce their reliability.
- Skipping the preview step and uploading with incorrectly mapped fields.

## Studio relevance
04 leverage - how the studio uses this card.
