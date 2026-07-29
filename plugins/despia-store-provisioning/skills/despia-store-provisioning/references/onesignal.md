# OneSignal push setup

Push is the default native capability on a Despia build, so this runs on almost every setup. It's two independent platform configurations plus the Despia editor, and the iOS half depends on provisioning work already being done.

## Contents

- [Create the OneSignal app](#create-the-onesignal-app)
- [iOS: APNs](#ios-apns)
- [Android: Firebase Cloud Messaging](#android-firebase-cloud-messaging)
- [The Despia side](#the-despia-side)
- [Testing](#testing)
- [Common failures](#common-failures)

## Create the OneSignal app

One OneSignal app covers both platforms - don't create two.

1. OneSignal dashboard → **New App/Website**
2. Name it the same as the app, so it's findable later
3. Choose a platform to configure first; the other is added afterwards under **Settings → Push & In-App → Platforms**
4. At the end, copy the **App ID**, and the **REST API Key** from Settings → Keys & IDs

The App ID is a public identifier and goes in the client. The REST API Key is a secret used from the user's backend to send notifications - it must never go into the web app's frontend code. Say that plainly; it's the most common security mistake in this integration.

## iOS: APNs

Requires from the provisioning run: the APNs `.p8`, its Key ID, the Team ID, and the app's Bundle ID. Also requires the Push Notifications capability enabled on the identifier and, for rich notifications, the OneSignal service extension identifier and the `.onesignal` App Group - see `references/apple-developer-portal.md`.

1. **Settings → Push & In-App → Platforms → Apple iOS (APNs)** → Activate
2. Choose **.p8 Auth Key** - not a .p12 certificate. The .p8 doesn't expire; certificates do, annually, and that's an outage waiting a year out
3. Upload the `.p8`, then enter:
   - **Key ID** - must match the uploaded file
   - **Team ID** - top right of the Apple developer account
   - **Bundle ID** - exact, case-sensitive
4. Save

Remember which `.p8` this is: the one from **Certificates, Identifiers & Profiles → Keys**. The App Store Connect API key goes to Despia and the In-App Purchase key goes to RevenueCat. All three download with the same filename shape.

## Android: Firebase Cloud Messaging

Android push runs through Firebase, so there's a Firebase project to create even though nothing else in the app uses Firebase. Google's legacy FCM API is fully deprecated - the current setup is a **service account JSON**, not a server key. If the user has an old key starting with `AIz...`, it's dead and needs replacing.

1. **Firebase Console** → Add project (or select an existing one)
2. Register the Android app with the **exact package name** from Despia
3. **Project settings → Cloud Messaging** - if the Firebase Cloud Messaging API (V1) shows as disabled, open it in Cloud Console and enable it, then wait a few minutes
4. **Project settings → Service accounts → Generate new private key** → downloads a JSON
5. OneSignal → **Settings → Push & In-App → Platforms → Google Android (FCM)** → Activate → **Select file** → upload that JSON → Save

If OneSignal rejects it as invalid, the service account is missing roles. Firebase's default account has them; a custom one needs **Firebase Cloud Messaging API Admin** (for `cloudmessaging.messages.create`), granted in Google Cloud Console under IAM & Admin - not in Firebase.

**Never swap in a JSON from a different Firebase project** on an app that already has subscribers. Existing devices are tied to the old Sender ID and stop receiving notifications. OneSignal warns about this; take the warning seriously.

This Firebase service account JSON is a fourth distinct credential - it is not the Play Console service account used by Despia and RevenueCat, and they aren't interchangeable.

## The Despia side

In the Despia editor, enable push and enter the **OneSignal App ID**. This is an editor change: it needs a rebuild and a new submission, not an over-the-air update.

The web-layer work - prompting for permission at a sensible moment, tagging users with their own user ID so notifications can be targeted, handling deep links from a notification - is documented at `setup.despia.com/native-features/onesignal/`. The user-identity pattern matters more than it looks: without it, they can only broadcast to everyone.

## Testing

1. Rebuild and install on a real device - push does not work in a simulator
2. Accept the permission prompt
3. OneSignal → **Audience → Subscriptions**, confirm the device appears
4. Send a test message to that subscription
5. Test with the app closed, not just foregrounded - that's the case people actually care about

## Common failures

**Nothing arrives on iOS.** Bundle ID mismatch between OneSignal and the build is the first thing to check, then the Key ID, then whether Push Notifications is actually enabled on the identifier, then whether the app was rebuilt after any of those changed.

**Nothing arrives on Android.** Usually a legacy server key still configured, a JSON from the wrong Firebase project, or a package name mismatch.

**Rich notifications don't show images or buttons.** The OneSignal service extension identifier or the `.onesignal` App Group is missing or not linked. Basic push still works, which is why this goes unnoticed until someone sends an image.

**Worked in testing, stopped later.** A .p12 certificate was used instead of a .p8 and it expired. Replace it with a .p8.

**Device never appears in Subscriptions.** The App ID in Despia is wrong or missing, or the build predates it being set.
