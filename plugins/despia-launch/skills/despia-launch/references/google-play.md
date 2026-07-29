# Google Play

Android needs much less than iOS. There are no identifiers to register, no capabilities to enable, no signing keys to create - Despia handles signing. The one artifact that has to come out of the user's account is a **service account JSON key**, which is what lets Despia upload builds to their Play account.

## Contents

- [Register the package name first](#register-the-package-name-first)
- [Creating the app listing](#creating-the-app-listing)
- [Link a Google Cloud project](#link-a-google-cloud-project)
- [Create the service account and JSON key](#create-the-service-account-and-json-key)
- [Grant Play Console permissions](#grant-play-console-permissions)
- [Verify it works](#verify-it-works)
- [Testing track requirements](#testing-track-requirements)

## Register the package name first

Google changed the order here: the package name is registered **before** the app listing is created, and it cannot be changed afterwards.

1. Copy the Bundle ID from **Despia → Project → Android → Bundle ID**
2. In Play Console, use **Register package name** and paste it
3. Confirm

Paste, never retype. This is a one-way door - confirm the value with the user before submitting it. A wrong package name means a support request to Despia and a brand new Play listing with no reviews or installs carried over.

## Creating the app listing

**Create app**, then fill in app name, default language, app-or-game, free-or-paid. The package name is already bound from the previous step. Free-or-paid is another one-way door: an app published as free can never be switched to paid.

## Link a Google Cloud project

Play Console needs to know which Cloud project holds the service account.

1. Play Console → **Settings / Setup → API access**
2. If no project is linked, either link an existing Google Cloud project or create one from here
3. The Google account doing this must be the Play Console **account owner**, or an admin with the relevant permission

If prompted, or if the API access page shows the API as disabled, enable the **Google Play Android Developer API** for that project in the Cloud Console under APIs & Services. The Play Developer Reporting API is not needed.

## Create the service account and JSON key

In the **Google Cloud Console**, with the linked project selected:

1. **IAM & Admin → Service Accounts → Create Service Account**
2. Name it something obvious, e.g. `despia-publisher`
3. **Create and continue**
4. **Skip the Cloud IAM roles step** - grant nothing here. Play permissions are granted separately in Play Console, and Cloud roles do nothing for publishing.
5. **Done**
6. In the list, open the new account (or its **⋮ → Manage keys**) → **Keys → Add key → Create new key → JSON**
7. The JSON downloads immediately - warn the user first. It's named something like `project-123456-a1b2c3d4.json`.
8. Copy the service account **email** (`something@project-id.iam.gserviceaccount.com`) - you need it in the next step, and it's also inside the JSON as `client_email`

This JSON is a credential that can publish to their Play account. Treat it exactly like a password: never paste its contents anywhere, never open it in a shared document, and tell the user to keep the file somewhere safe rather than in Downloads.

## Grant Play Console permissions

The key is useless until the service account email is invited to the Play Console as a user and granted access.

1. Play Console → **Users and permissions → Invite new users**
2. In the email field, enter the **service account email** (`something@project-id.iam.gserviceaccount.com`). It is a real invitable identity - this is not a mistake, and there is no separate "service account" section to use instead.
3. Grant **Admin (all permissions)** at account level. If the user is uncomfortable granting account-level Admin, **App admin** on the specific app is the minimum that works with Despia - anything narrower will fail on upload.
4. Invite / save

There's no confirmation email to accept; service accounts are granted access directly.

**It has to be a service account, not a person.** A JSON exported from a user account, an OAuth client secret, or a downloaded credentials file of any other type will be rejected. The correct file has `"type": "service_account"` on the first or second line and contains `client_email` and `private_key`.

## Verify it works

Two known delays that look like failure:

- **Propagation.** New service account permissions can take a while to become effective, occasionally up to 24 hours. If Despia rejects the JSON immediately after setup, wait before debugging.
- **The first upload.** Google generally requires the first release for a brand-new app to exist in the console before API-based uploads succeed. If the very first automated upload fails on a new listing, upload one AAB manually to an internal testing track, then retry.

Errors mentioning a project not being linked point back to the API access page - the Cloud project link is the step most often skipped.

## Set up the testing track

Same principle as TestFlight: create the track and the tester list now, so the first build has somewhere to land and someone to reach.

1. App → **Testing → Internal testing**
2. **Testers** tab → **Create email list**
3. Name the list, paste the email addresses, save
4. Select the list for this track and save

Internal testing on Play allows up to 100 testers and needs no review, so builds are available within minutes of upload. Testers get an opt-in link - **send it to them**, since nothing arrives automatically. They open the link, accept, then install from the Play Store like any other app.

**Ask who they want testing** rather than creating an empty list: "Same testers as iOS, or a different group? I need Google account emails - the address has to match the account on their Android device." That last detail matters; a work email that isn't a Google account silently doesn't work.

Confirm the user's own address is on the list.

## Testing track requirements

Personal / individual developer accounts have to run a closed testing period with a minimum number of testers for a minimum number of days before production access opens. Organisation accounts don't.

Google has changed both the tester count and the duration more than once. **Read the requirement text shown in the user's own console** rather than quoting a number - the console states the current rule for that specific account, and giving a stale number here sends people off to recruit the wrong number of testers.
