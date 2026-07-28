# App Store Connect

Everything here happens at `appstoreconnect.apple.com`. The identifiers in `apple-developer-portal.md` must exist first - the Bundle ID appears here as a dropdown, not a text field.

## Contents

- [Creating the app record](#creating-the-app-record)
- [App Store Connect API key](#app-store-connect-api-key)
- [Agreements, Tax, and Banking](#agreements-tax-and-banking)
- [Declarations and metadata](#declarations-and-metadata)
- [TestFlight](#testflight)
- [Store listing metadata](#store-listing-metadata)

## Creating the app record

**Apps → + → New App**

| Field | What to enter |
|---|---|
| Platforms | iOS (add others only if the user asked) |
| Name | Public App Store name, 30 characters max, **unique across the entire App Store** |
| Primary Language | The app's main language |
| Bundle ID | Select the identifier registered earlier - it appears by its description |
| SKU | Internal reference, never shown publicly. The bundle ID or a slug works fine |
| User Access | Full Access unless the user runs a large team |

Then **Create**.

**Record the numeric Apple ID immediately.** Once the record exists, open **App Information → General Information** and copy the **Apple ID** - a number like `6795471561`. Despia needs this, and it is not the Bundle ID. It doesn't exist until the listing is created, which is part of why the listing has to come before deployment rather than after.

Two things reliably go wrong here:

**The Bundle ID isn't in the dropdown.** Either it was registered as a Wildcard rather than Explicit, or the portal hasn't propagated yet. Wait a minute and reload before assuming anything is broken. If it's still missing, check the identifier type on the developer portal.

**The name is taken.** App names are reserved globally and first-come. Creating the record reserves it, which is why this is a one-way door worth confirming - ask the user for their exact preferred name and a fallback before you start. The subtitle (30 chars) can carry keywords the name can't.

## App Store Connect API key

**This is the Despia key, not the OneSignal one.** Despia uploads builds to App Store Connect on the user's behalf, and this is the credential it uses. The other `.p8` in this process - the APNs Auth Key, created under Keys in the developer portal - goes to OneSignal instead. Both files download as `AuthKey_XXXXXXXXXX.p8` and only the Key ID tells them apart.

Despia needs three things from here: **Issuer ID**, **Key ID**, and the `.p8` file.

**The key must be created with the App Manager role. Not Admin, not Developer - App Manager.** Despia only accepts App Manager. A key generated with any other access level will be rejected, and the user has to generate a new one, because the role can't be changed after creation.

### Finding the page

This is the hardest page in App Store Connect to find, and the label people search for isn't the label on screen. Getting there:

1. From the App Store Connect home page, click **Users and Access** (top navigation, alongside Apps and Analytics - not inside an individual app)
2. Along the top of that page there are tabs: Users, Sandbox, **Integrations**, and possibly others. Click **Integrations**
3. In the left sidebar under Integrations, select **App Store Connect API**
4. Two sub-sections appear: **Team Keys** and **Individual Keys**. You want **Team Keys** - an individual key is tied to one person's account and breaks if they leave or lose access

If Integrations isn't visible at all, the signed-in account doesn't have a sufficient role. If the user is searching for "API access" or "API keys" in the interface and finding nothing, this is why - it's under Users and Access, which most people never open.

### Creating the key

1. **Team Keys → Generate API Key** (or **+**)
2. **Name**: e.g. "Despia"
3. **Access**: **App Manager**
4. **Generate**
5. Copy the **Issuer ID** - it sits above the key list as its own labelled field, and is shared by every key on the team. It looks like a UUID: `69a6de70-...`
6. Copy the **Key ID** from the new key's row - 10 characters
7. **Download API Key** - warn first, this is one-time, lands as `AuthKey_XXXXXXXXXX.p8`

If Generate is greyed out or missing, the account's role isn't sufficient - team key creation is restricted to the Account Holder, and depending on team settings, Admins. Hand that back to the user rather than trying to work around it.

Then take it the rest of the way: upload the `.p8` into Despia along with the Issuer ID and Key ID in the same run, rather than leaving the user with a file in Downloads and instructions. If you can't handle files, walk them through the upload step by step and confirm Despia shows the key as accepted. Never paste the contents of the `.p8` into chat.

## Agreements, Tax, and Banking

**Business → Agreements, Tax, and Banking**

- Free apps need the standard Apple Developer Program License Agreement in effect.
- Paid apps and anything with in-app purchases need the **Paid Applications** agreement, which requires completed tax forms and a bank account.

**Do not accept an agreement for the user.** These are contracts, they can generally only be accepted by the Account Holder or Legal role, and an agent clicking through them is not appropriate regardless of role. Check the status, report exactly which agreement is outstanding, and tell the user what it blocks. An unsigned Paid Applications agreement is a common reason IAP products never load in RevenueCat, and the error surfaces nowhere near the cause.

## Declarations and metadata

Both live in their own reference files now:

- **Declarations** - App Privacy, export compliance, IDFA, content rights, age rating: `references/declarations.md`. Derive the answers from the SDKs the project uses, fill them in, explain each, then get one explicit confirmation before committing. They're legal statements in the user's name, but that's a reason to show your work, not a reason to hand someone a blank form they can't fill.
- **Metadata and ASO** - `references/store-metadata.md`
- **Submission and rejections** - `references/submission-and-rejections.md`

## TestFlight

**The app record has to exist first.** There is no TestFlight without it - no record means no upload target, so builds fail and the user cannot get the app onto a single device. This is why step 5 is never skipped, even for someone who says they only want to test for now.

Once Despia's build lands and finishes processing (10-30 minutes after upload):

### Internal testing group

Create one if the app doesn't have it - a fresh app record has no groups, and without a group there is nobody to send a build to.

1. Open the app → **TestFlight** tab
2. Under **Internal Testing** in the sidebar, **+** to create a group
3. Name it something plain: "Internal" or "Team"
4. Enable **automatically distribute new builds** so the user isn't re-approving every rebuild
5. Add testers

Internal testers must already be users on the App Store Connect account, up to 100 of them. Adding someone who isn't on the team is a two-part job: invite them under **Users and Access** first (Developer role is enough to test, and is the least access that works), then add them to the group.

**Ask who they want testing.** Don't guess and don't create an empty group. "Who should get access to test builds? I need their email addresses - usually yourself, anyone else on your team, and whoever's giving you feedback." Then set them up, and tell them each person gets an email invite and needs the TestFlight app from the App Store.

The user themselves is the one people forget. Confirm their own Apple ID is on the list.

### External testing

Up to 10,000 testers, needs a beta review pass first (24-48 hours). Worth mentioning as the next step for anyone testing beyond their own team, but don't set it up unprompted - it puts a review in the path.

### Build stuck in Processing

Over an hour usually means missing export compliance information or an invalid binary. Check the Activity tab and the account email for a rejection notice.

## Store listing metadata

Write the copy for the user rather than handing them empty fields - see `references/store-metadata.md` for the ASO rules and the drafting approach. Required before submission:

- Name (30), subtitle (30), description (4000), keywords (100 chars comma-separated, no spaces after commas)
- Screenshots for the required device sizes, RGB, no transparency
- Support URL and privacy policy URL, both live and reachable without login
- Category, age rating, pricing

Fill everything, run the pre-submission checklist in `references/submission-and-rejections.md`, then let the user press Submit - it's their developer account the review runs against.
