# Intake

The intake is the closest thing this flow has to a user interface. Done well, the user answers six questions in plain language and everything after that is derivation. Done badly, they're asked to supply values they've never heard of and they bounce.

## Contents

- [The questions](#the-questions)
- [Deriving the matrix](#deriving-the-matrix)
- [The confirmation block](#the-confirmation-block)
- [When they don't know an answer](#when-they-dont-know-an-answer)

## The questions

Ask in one or two batches. If you can read the Despia project directly, fill those fields yourself and only ask for what's missing - never make someone look up a value you're already looking at.

**1. Which stores?** iOS, Android, or both.

**2. Your iOS Bundle ID.** "It's in Despia under Project → iOS. It looks like `com.yourcompany.yourapp`. Paste it exactly as shown - it's locked to your app's signing and can't be changed later."

**3. Your Android package name.** "Despia also calls this Bundle ID, under Project → Android. Usually the same string as iOS, but check - if they differ, I need both."

**4. Your app's name as it should appear on the App Store.** "30 characters max, and it has to be unique across the whole App Store. Have a backup in mind - good names go fast."

**5. What does your app need to do?** Multi-select, phrased as outcomes:

- Send notifications to users when the app is closed
- Show notifications with images or buttons in them
- Open your website links directly in the app instead of the browser
- Show a widget on the user's home screen
- Let users share content from other apps into yours
- Offer a lightweight preview of the app without installing it
- Sell subscriptions or in-app purchases
- Keep users logged in after they delete and reinstall

Never ask "do you need App Groups" or "which targets do you want". Those are outputs of this question, not inputs.

**6. Account access.** "Do you have an active Apple Developer account, and are you the account holder? And do you have a Google Play Console account?" If they don't know their role, you'll see it in the portal - but asking costs nothing and can save the whole session.

**6b. Which team.** If their Apple account belongs to more than one team - their own plus an employer's, or an agency with client accounts - establish which one this app belongs to and record the **Team ID**, not just the name. Names are similar and get changed; the ten-character Team ID doesn't. Everything gets checked against it later, and work done in the wrong team generally can't be moved.

**7. Who's testing?** "Once the app builds, who should be able to install it? Give me email addresses - yours, anyone on your team, anyone giving you feedback. For Android they need to be Google accounts, ideally the one on their phone." Ask this during intake even though the testing groups get created later, so the user isn't hunting for addresses at the point where they're finally close to seeing their app on a device.

Cross-check answer 5 against Despia's actual feature toggles. If the user says no widgets but the project has widgets enabled, ask - one of the two is wrong, and finding out now is cheap.

## Deriving the matrix

| They said | Targets / identifiers | App Groups | Capabilities on the core ID | Other |
|---|---|---|---|---|
| Notifications when app is closed | none | none | Push Notifications | APNs key + OneSignal setup |
| Notifications with images or buttons | `.OneSignalNotificationServiceExtension` | `group.<id>.onesignal` | App Groups | Group linked to both IDs |
| Website links open in app | none | none | Associated Domains | `apple-app-site-association` file on their domain |
| Home screen widget | `.ImageWidget` | `group.<id>.widgetsharing` | App Groups | none |
| Share into the app | `.ShareExtensionTarget` | `group.<id>.sharetarget` | App Groups | none |
| Preview without installing | `.Clip` | `group.<id>.Clip` | App Groups | none |
| Subscriptions or purchases | none | none | none | Paid Applications agreement, RevenueCat |
| Survives reinstall | none | none | iCloud (CloudKit) | none |

Push is on the Standard profile by default even if the user didn't ask for it - see the scope section in SKILL.md for why, and say it in one sentence rather than adding it silently.

Anything not on this list adds nothing to the matrix. Don't provision speculatively.

## The confirmation block

Read the derived matrix back before touching a console. Plain list, no jargon in the left column:

```
Here's what I'll set up in your Apple account:

  Your app                com.example.app
  Push notifications      capability + APNs key
  Rich notifications      extra identifier com.example.app.OneSignalNotificationServiceExtension
                          shared storage group.com.example.app.onesignal
  Deep links              Associated Domains capability
  App Store listing       "Example" - reserved when I create it

Not setting up: widgets, share extension, App Clip (you said you don't need them)

Google:
  Package name            com.example.app - registered before the listing, permanent
  Publishing access       service account so Despia can upload builds for you

Look right?
```

The "not setting up" line matters. It's how the user catches a feature they forgot to mention, and it's cheaper to add now than after the identifiers exist.

## When they don't know an answer

- **No Bundle ID yet** - it's generated in Despia when the project is created. Point them at Project → iOS rather than inventing one.
- **Not sure about their Apple role** - open Membership details and read it out.
- **Not sure what features they need** - default to the Standard profile: push only. Everything else can be added later by registering another identifier; the core Bundle ID is the only piece that's genuinely permanent.
- **No Apple Developer account** - $99/year, enrolment can take 24-48 hours, and organisation enrolment needs a D-U-N-S number which takes longer. Say that up front; it's the longest lead time in the entire process and people plan launches around not knowing it.
