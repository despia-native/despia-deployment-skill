# Despia handoff

Despia is the source of truth at the start and the destination at the end. This file covers both directions.

## Read out of Despia before touching Apple or Google

| Value | Where | Used for |
|---|---|---|
| iOS Bundle ID | Project → iOS | Every Apple identifier, derived extension IDs, App Groups |
| Android Bundle ID / package name | Project → Android → Bundle ID | Play package name registration |
| App display name | Project settings | App Store Connect app record, Play listing |
| Enabled native features | Editor / feature toggles | Deciding which identifiers and capabilities to create |
| Dynamic App Store Source URL | Dashboard | Sanity check - must be HTTPS and must load |

Feature toggles map to provisioning like this:

- Push / OneSignal → Push Notifications capability, `.onesignal` App Group, OneSignal service extension identifier, APNs key
- Deep linking / universal links → Associated Domains capability, plus an `apple-app-site-association` file on the user's domain
- Home widgets → widget identifier + `.widgetsharing` group
- Share extension → share identifier + `.sharetarget` group
- App Clip → Clip identifier + `.Clip` group
- Storage vault / iCloud KVS → iCloud capability with CloudKit
- HealthKit, camera, location and similar → no portal work, but they need specific Info.plist usage strings; generic ones get rejected at review

## Paste back into Despia

Field by field. Missing any of these produces a build that fails or ships wrong.

| Field | Value | Notes |
|---|---|---|
| App name | The display name | |
| Start URL | The **real** HTTPS production URL | Never leave a placeholder like `https://example.com` - shipping that is a dead app |
| Bundle ID | Must match the registered identifier exactly | Read it back character by character |
| Version | e.g. `1.0.0` | |
| Apple Development Team | Select the correct team | The approved Team ID, not a personal or client team |
| App Store Connect API key | Issuer ID, Key ID, and its `.p8` | The key from **Users and Access → Integrations**, App Manager role |
| **Numeric App Store App ID** | e.g. `6795471561` | Not the Bundle ID. Found in App Store Connect → your app → **App Information → General Information → Apple ID**. It only exists after the listing is created, which is one reason the listing comes before deployment |
| Google Play service account JSON | Upload the file | |

## Uploading assets

Despia shows several visually identical "Upload Icon" buttons, one per section. They are not interchangeable and there's no warning if you use the wrong one.

- **Select the button inside the correct section** - iOS icon, Android icon, or Splash - every time. Confirm the section heading before clicking, not after
- **Upload one at a time and wait for "Finished"** before starting the next. Concurrent uploads and early navigation both produce assets that appear staged but aren't stored
- **Confirm all three show as complete** before publishing anything

## Publishing and verifying

The deployment consumes a credit, so getting this right matters more than usual.

1. Confirm every field above is set and all three assets show "Finished"
2. Ask the user before publishing - it costs them
3. Click **Publish Project once**
4. Open **Build History** and click **Refresh**

**Build History is the only authoritative status.** The "Publishing App — In Progress" panel is not proof that a build was accepted, and Build History itself can show stale data until Refresh is clicked. A successful build appears as an entry with version, platform, date and status.

**Never click Publish again because nothing seems to be happening.** Refresh Build History first. Repeated clicks produce duplicate builds, and each one spends a credit of the user's money.

## Paste into OneSignal, not Despia

Push credentials go to OneSignal's dashboard, under the iOS platform settings. **This is the other `.p8`** - the APNs Auth Key, generated under **Certificates, Identifiers & Profiles → Keys** in the developer portal. It never goes to Despia, and the App Store Connect API key never goes to OneSignal.

- APNs `.p8` file
- Key ID (10 characters)
- Team ID (10 characters)
- The app's Bundle ID

Both keys download as `AuthKey_XXXXXXXXXX.p8`, differing only in the Key ID. Check the Key ID against the console before each upload - a swapped pair produces two failures that point nowhere near the cause: Despia rejects its credential, and push silently never sends.

A Bundle ID mismatch between OneSignal and the built app is the other common reason push "works" in the dashboard but never arrives on a device.

## Assets, since they block builds

| Asset | Size | Format | Background |
|---|---|---|---|
| iOS icon | 1024 × 1024 | PNG | Solid, no transparency |
| Android icon | 1024 × 1024 | PNG | Solid, no transparency, extra safe padding - Android crops in |
| Splash screen | 1024 × 1024 | GIF, **2-199 frames** | Transparent for Android; follow the platform section in the Despia docs for iOS |
| Play feature graphic | 1024 × 500 | PNG/JPEG | Any |

The iOS icon is required even for an Android-only build. An alpha channel on an icon fails the build or gets rejected by Apple.

## What needs a rebuild vs. what ships over the air

Worth telling the user explicitly, because it changes how they think about all of this.

**Rebuild required** (rare, once or twice a year): bundle ID or package name, capabilities and permissions, icons, splash screen, push configuration, associated domains, App Groups, anything changed in the Despia editor.

**Ships instantly over the air**: everything in the web app - UI, content, business logic, bug fixes, new features. No store review, no rebuild, no build credits.

The provisioning work in this skill is the one-time cost that buys them the OTA workflow afterwards. Say that - it reframes an hour of console clicking as something they only do once.
