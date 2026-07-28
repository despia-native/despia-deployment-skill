# Apple Developer Portal

Everything here happens at `developer.apple.com/account` under **Certificates, Identifiers & Profiles**. Requires an active paid Developer Program membership and Account Holder or Admin role.

## Contents

- [The bundle ID map](#the-bundle-id-map)
- [Registering the core Bundle ID](#registering-the-core-bundle-id)
- [Creating App Groups](#creating-app-groups)
- [Linking App Groups to the identifier](#linking-app-groups-to-the-identifier)
- [Extension identifiers](#extension-identifiers)
- [APNs Auth Key](#apns-auth-key)
- [Finding the Team ID](#finding-the-team-id)
- [Things that are permanent](#things-that-are-permanent)

## The bundle ID map

Take the core Bundle ID from Despia and derive the rest. Below, `com.despia.myapp` stands in for whatever Despia shows - substitute the real value everywhere.

| Module | Identifier | App Group | Capabilities |
|---|---|---|---|
| Core app | `com.despia.myapp` | all four below | App Attest, App Groups, Associated Domains, iCloud (CloudKit), Push Notifications (Broadcast) |
| OneSignal service extension | `com.despia.myapp.OneSignalNotificationServiceExtension` | `group.com.despia.myapp.onesignal` | App Groups, Associated Domains, Push Notifications (Broadcast) |
| App Clip | `com.despia.myapp.Clip` | `group.com.despia.myapp.Clip` | App Groups, Associated Domains, Push Notifications |
| Share extension | `com.despia.myapp.ShareExtensionTarget` | `group.com.despia.myapp.sharetarget` | App Groups |
| Home widget | `com.despia.myapp.ImageWidget` | `group.com.despia.myapp.widgetsharing` | App Groups |

Note the group suffixes do not mirror the extension suffixes - `ShareExtensionTarget` pairs with `sharetarget`, `ImageWidget` pairs with `widgetsharing`. Copy them from this table rather than deriving them.

**Only create what the app uses.** For the Standard profile that's the core identifier, the OneSignal extension identifier, and the `.onesignal` App Group. Skip the rest unless the Despia project has App Clip, share extension, or widgets enabled. Extra identifiers are harmless in isolation but each one is another object that has to keep matching.

## Registering the core Bundle ID

1. **Certificates, Identifiers & Profiles → Identifiers → +**
2. Select **App IDs** → Continue
3. Select type **App** → Continue
4. **Description**: plain text, no special characters. **This name must be unique - every identifier needs its own.** Naming several identifiers the same thing breaks deployment, and the error you get later says nothing about names. Use a consistent scheme so the set stays readable:

   | Identifier | Description |
   |---|---|
   | `com.despia.myapp` | MyApp |
   | `com.despia.myapp.OneSignalNotificationServiceExtension` | MyApp OneSignal |
   | `com.despia.myapp.Clip` | MyApp Clip |
   | `com.despia.myapp.ShareExtensionTarget` | MyApp Share |
   | `com.despia.myapp.ImageWidget` | MyApp Widget |

   App Groups need distinct names too - "MyApp OneSignal Group", "MyApp Widget Group". Build the whole naming set in the matrix up front rather than inventing names one at a time, which is how duplicates happen.
5. **Bundle ID**: choose **Explicit** (never Wildcard - wildcards can't carry push or app groups) and paste the value from Despia exactly. It is case-sensitive.
6. Tick the capabilities the app needs. For Standard: **Push Notifications** and **App Groups**. Add **Associated Domains** if deep linking is on, **iCloud** with CloudKit if storage vault is on, **App Attest** if the full profile applies.
7. Continue → review the summary → **Register**

Then reopen the identifier from the list and confirm the Bundle ID string character for character against Despia. A single wrong character here produces a signing failure much later with no obvious cause.

## Creating App Groups

App Groups are how the main app and its extensions share data. They're a separate identifier type.

1. **Identifiers → +**
2. Select **App Groups** → Continue
3. **Description**: e.g. "MyApp OneSignal"
4. **Identifier**: `group.com.despia.myapp.onesignal` - the `group.` prefix is required
5. Continue → **Register**

Repeat for each group the app needs. Create the groups before linking, since the link step selects from existing groups.

## Linking App Groups to the identifier

Creating a group does nothing until it's attached to each identifier that uses it.

1. **Identifiers →** click the App ID
2. Find **App Groups** in the capability list, make sure it's ticked
3. Click **Configure** (or **Edit**)
4. Tick every group this identifier needs
5. **Continue → Save**

Apple may show a warning that changing capabilities invalidates existing provisioning profiles. For a Despia app that's expected - Despia regenerates profiles on the next build. Reassure the user and continue.

Do this for the core identifier and for each extension identifier, using only the group(s) from the map that belong to it.

## Extension identifiers

Same flow as the core Bundle ID, with the extension's own capability set from the map. The OneSignal service extension is the one that matters for the Standard profile - without it, rich push (images, media, action buttons) silently doesn't work, though basic push still does.

## APNs Auth Key

**This is the OneSignal key, not the Despia one.** It's created under Keys in the developer portal and it goes to OneSignal. The other `.p8` in this process - the App Store Connect API key, created under Users and Access in App Store Connect - goes to Despia. Both download with near-identical filenames. Don't cross them.

This key is what lets OneSignal send push to the app. It's team-wide: one key covers every app in the team.

**Check for an existing key first.** Apple allows a maximum of two active APNs Auth Keys per team, and the private key can't be re-downloaded. If the team already has one and the user still has the `.p8`, reuse it. Only generate a new one if none exists or the file is genuinely lost (in which case revoke the old one after the new one is confirmed working).

1. **Certificates, Identifiers & Profiles → Keys → +**
2. **Key Name**: something recognisable, e.g. "APNs Key - MyApp"
3. Tick **Apple Push Notifications service (APNs)**
4. If offered an environment or Bundle ID restriction, leave it unrestricted (team-wide) unless the user has a reason to scope it
5. Continue → **Register**
6. **Download** - warn the user first. This is the only download. The file lands as `AuthKey_XXXXXXXXXX.p8`. **Confirm it's on disk before leaving the page** - if it isn't, the key is dead and no retry will recover it. Don't generate a second key to try again; switch to the user's Chromium browser and have them download it there
7. Record the **Key ID** (the 10-character string, also in the filename)

OneSignal then needs three things: the `.p8` file, the Key ID, and the Team ID. Those go into the OneSignal dashboard under the iOS platform settings, along with the app's Bundle ID.

Do that upload yourself if you can - open OneSignal, attach the file, fill the three fields, save, and confirm it shows as configured. Handing a founder a `.p8` and a set of instructions is where push setups get abandoned half-finished. If you can't move files, guide them through it and verify the result before moving on.

## Finding the Team ID

Top right of the developer account page, or **Membership details**. Ten characters, letters and digits. Despia and OneSignal both ask for it.

## Things that are permanent

- A deleted Bundle ID **cannot be re-registered** with the same string. Never delete one to "start clean".
- App Group identifiers behave the same way.
- `.p8` private keys download once. There is no recovery, only revoke-and-replace.
- Capability changes are reversible, but removing a capability invalidates profiles and breaks any live build depending on it.
