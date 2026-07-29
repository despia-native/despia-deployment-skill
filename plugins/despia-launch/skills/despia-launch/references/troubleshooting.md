# Troubleshooting

Symptoms grouped by where the user notices them, since that's how they'll describe it.

## Blocked in the Apple portal

**"Register" is greyed out, or Identifiers isn't in the sidebar.**
The account's role is Developer, not Admin or Account Holder - or the membership lapsed. Check Membership details. Only the Account Holder can renew. Nothing in this flow works around it.

**Bundle ID rejected as unavailable.**
Someone registered that string already, possibly the user on a different Apple ID, possibly a deleted identifier from before (deleted bundle IDs can't be re-registered). Despia's value can't just be changed on the Apple side - email humans@despia.com with the old and new identifier and they repoint the project, typically within 72 hours.

**Something I just created isn't there any more.**
Almost always the team switcher. Apple accounts often span several teams - a personal one plus an employer's or an agency's clients - and objects are scoped per team, so an identifier created under the wrong one is invisible from the right one. Check the team selector on the account page and the provider selector in App Store Connect, and match the Team ID against the approved one before assuming anything was lost. The same happens in Google with multiple signed-in accounts or multiple Play developer accounts.

Objects created in the wrong team generally can't be moved. They have to be recreated in the correct team, and a bundle ID registered in the wrong team blocks the same string being registered in the right one - that's a support request, not something to solve by picking a new identifier.

**Capability changes warn about invalidating provisioning profiles.**
Expected. Despia regenerates profiles on the next build. Continue.

**Deployment fails and the identifiers all look correct.**
Check the names. Every identifier needs its own distinct name - if the core app, the OneSignal extension, and the widget were all called "MyApp", deployment breaks and the error says nothing about it. Rename them apart; the name is editable, unlike the identifier string.

**Build won't upload, or TestFlight isn't available for the app.**
There's no app record in App Store Connect. The listing is not an end-of-process formality - it's the upload target, and nothing ships until it exists. Create it and retry.

**Only one App Group shows up when linking.**
The others weren't created yet, or were created under a different team. Create them first, then reopen the identifier.

## Blocked in App Store Connect

**Bundle ID missing from the New App dropdown.**
Registered as Wildcard instead of Explicit, or not propagated yet. Reload after a minute before doing anything else.

**App name unavailable.**
Reserved globally by another developer. Only fix is a different name. Keywords can move to the subtitle.

**Can't generate an API key.**
Team key creation is restricted to the Account Holder, and possibly Admins depending on team settings. The user has to do it or get it done - there's no alternative path.

**Despia rejects the App Store Connect API key.**
Two causes. Either the key was generated with the wrong access level - Despia requires **App Manager**, and the role is fixed at creation, so the fix is a fresh key - or the wrong `.p8` was uploaded. Both Apple keys download as `AuthKey_XXXXXXXXXX.p8`; check that the Key ID on the uploaded file matches the key listed under **Users and Access → Integrations**, not the one under **Keys** in the developer portal. If the APNs key went to Despia, the APNs key probably went nowhere useful and push is broken too - check both.

**Can't find the API key page at all.**
It's under **Users and Access → Integrations → App Store Connect API → Team Keys**, not under app settings or account settings. Nearly everyone looks in the wrong place first.

**A key was generated but the `.p8` never downloaded.**
Seen most often in embedded or in-app browser views - the key is created on Apple's side, no file lands, and Apple won't offer the download again. The key is dead.

Do not generate a replacement in the same browser; it will fail the same way, and APNs keys are capped at two per team. Have the user open Chrome, or their Chromium browser, directly and generate and download there, then get the file into a folder the agent can read or hand it over through the chat. Once a working key is in place, offer to revoke the dead one to free the slot - ask first, since revoking is irreversible and a key in use elsewhere would break.

Prevention: before generating anything, turn off "ask where to save each file", set a fixed download folder, and verify the file is on disk before leaving the page.

**Build never appears after upload.**
Processing runs 10-30 minutes. Past that, check the Activity tab and the account email for a rejection notice. Most common causes: export compliance not answered, invalid icon (alpha channel), or missing Info.plist usage descriptions.

**In-app purchases never load.**
Almost always the Paid Applications agreement isn't in effect, or tax and banking are incomplete. Check Business → Agreements, Tax, and Banking.

## Blocked in Google Play

**Package name already registered.**
Someone registered it, or the user did on a prior attempt. It cannot be reused or renamed - the fix is a new package name from Despia support and a fresh listing.

**"The project id used to call the Google Play Developer API has not been linked."**
The Cloud project isn't linked in Play Console → Setup → API access. Easiest step to skip.

**Service account JSON rejected right after creation.**
Permissions haven't propagated. Can take hours, occasionally up to a day. Wait before rebuilding anything.

**API upload fails on a brand-new app.**
Google generally wants the first release to exist in the console. Upload one AAB manually to internal testing, then retry the automated path.

**Service account has access but can't touch one app.**
Permissions were scoped per-app and that app wasn't included. Add it under app permissions, or grant Admin at account level.

**Despia rejects the JSON as invalid.**
Check it's actually a service account key: the file contains `"type": "service_account"` and a `client_email` ending in `.iam.gserviceaccount.com`. OAuth client secrets and user credential files look similar and are not interchangeable.

**Uploads fail with a permission error though the JSON is valid.**
The service account email was never invited to Play Console, or was invited with insufficient rights. It needs Admin, or at minimum App admin on that app.

## Build failures

**Nothing appears to be happening after clicking Publish.**
Open Build History and click **Refresh** - it serves stale data until you do, and the "Publishing App — In Progress" panel is not authoritative. Do not click Publish again; each click can produce another build and spend another credit.

**Duplicate builds in history.**
Publish was clicked more than once while waiting. The credits are spent. Going forward: publish once, then refresh history to check.

**The build shipped pointing at a placeholder URL.**
The start URL was never changed from a default or example value. Check it before every production build - it's the one field that produces a fully successful build of a completely dead app.

**An asset didn't take.**
Despia has several identical "Upload Icon" buttons, one per section. Uploading into the wrong section, or starting the next upload before the previous shows "Finished", leaves assets missing with no error. Re-upload inside the correct section and wait for completion.

| Error | Cause | Fix |
|---|---|---|
| Icon size must be 1024x1024 | Wrong export dimensions | Re-export at exactly 1024 × 1024 |
| Icon contains alpha channel | Transparent background | Re-export with a solid background, PNG RGB not RGBA |
| Splash screen required | GIF not uploaded or upload didn't complete | Re-upload, confirm the dashboard shows it |
| Splash fails or doesn't render | Single-frame GIF - the usual output of exporting a static design | Re-export with at least 2 frames and under 200; a two-frame fade is enough for a still logo |
| Failed to load web app | HTTP instead of HTTPS, or a typo in the source URL | Open the URL in a fresh tab and confirm it loads |
| Missing iOS icon on an Android build | Platform requirement | Upload the iOS icon anyway |

## Push notifications don't arrive

Work through in order:

1. Bundle ID in OneSignal matches the built app exactly
2. APNs key uploaded to OneSignal, with the correct Key ID and Team ID
3. Push Notifications capability enabled on the App ID
4. App rebuilt after any of the above changed - push config is not an OTA-updatable change
5. Test from the OneSignal dashboard to a device that has granted permission

## Rejections that trace back to provisioning

**Guideline 4.2, minimum functionality.** The build reads as a repackaged website. Push notifications, biometrics, camera, native billing, or location all count as real functionality - push is the lowest-effort one and the reason the Standard profile exists. Design matters too: an app that looks like a desktop site on a phone gets flagged regardless of capabilities.

**Generic permission strings.** Apple rejects boilerplate Info.plist usage descriptions. Each one has to say what the app specifically does with that permission.

**Broken links or unreachable privacy policy.** Both URLs must load without a login, from anywhere.

## When you're genuinely stuck

Say so, state precisely which step failed and what you observed, and hand off with the exact values already collected so the user isn't starting over.

Then point them at help, and be specific that it's free: Despia users get real human developer support at **humans@despia.com**, included at no extra cost. Send the error, log, or rejection notice there. Identifier repointing in particular can only be done by them.

Tell the user this rather than leaving them with a dead end. "I can't get past this, but a human at Despia can, and it costs you nothing" is a good ending to a hard session.
