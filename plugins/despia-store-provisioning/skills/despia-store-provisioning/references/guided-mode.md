# Guided mode

Automation falls short regularly: no system browser automation in the session, an embedded browser that swallows downloads, a Safari user, a locked-down work machine, a step Apple gates behind the Account Holder. None of that is a failure - the failure is handing the user a shrug and a wall of instructions.

**Work the automation ladder in SKILL.md first.** Guided mode is the last rung, not the second. Before handing a step over, check whether computer use can drive a real browser, whether a local agent surface can handle the file, or whether a connector can bypass the console entirely. Most "I can't do this" moments are actually "I haven't tried the next surface".

When you do hand over, guided mode is a different mode of working, not a degraded one. You still run the process; the user's hands are the tool. That means you keep the state, you keep the pace, and **you verify every step yourself** rather than trusting "done".

## Contents

- [Handing over without losing them](#handing-over-without-losing-them)
- [Direct links](#direct-links)
- [Verify by screenshot](#verify-by-screenshot)
- [What to check per artifact](#what-to-check-per-artifact)
- [Resuming](#resuming)

## Handing over without losing them

Say what you can't do, in one line, with the reason and the alternative in the same breath. No apology spiral, no explanation of your architecture.

> I can't drive Chrome directly in this session, and the built-in browser isn't saving Apple's one-time key downloads. So you'll do this bit in Chrome and I'll take it from there - it's about two minutes.

Then:

- **One step per message.** Never a numbered list of nine.
- **Give the direct link**, not a navigation path. "Go to Users and Access, then Integrations, then find the tab" is three chances to end up somewhere else.
- **Say what they'll see when they land**, so they know they're in the right place before doing anything.
- **Say what to click, using the exact on-screen label.**
- **Say what should happen after**, and ask them to confirm it did.
- **Tell them the exact words to send back** when done - "say saved and I'll pick it up". Ambiguity about what you're waiting for is how sessions die.

## Direct links

Deep links save a non-technical user more time than any other single thing. Verify the destination loads before sending it - both consoles reorganise, and a stale link is worse than a path.

**Apple Developer**

| Destination | URL |
|---|---|
| Identifiers | `developer.apple.com/account/resources/identifiers/list` |
| App Groups | `developer.apple.com/account/resources/identifiers/list/applicationGroup` |
| Keys (APNs) | `developer.apple.com/account/resources/authkeys/list` |
| Create a key | `developer.apple.com/account/resources/authkeys/add` |
| Account home / Team ID | `developer.apple.com/account` |

**App Store Connect**

| Destination | URL |
|---|---|
| Apps | `appstoreconnect.apple.com/apps` |
| Users and Access | `appstoreconnect.apple.com/access/users` |
| API keys and In-App Purchase keys | `appstoreconnect.apple.com/access/integrations/api` |
| Agreements, Tax, and Banking | `appstoreconnect.apple.com/business` |

The API key and In-App Purchase key live on the same Integrations page in different sections - tell them which section, since picking the wrong one produces a key that looks right and fails later.

**Google**

| Destination | URL |
|---|---|
| Play Console | `play.google.com/console` |
| Cloud service accounts | `console.cloud.google.com/iam-admin/serviceaccounts` |
| Enable Play Developer API | `console.cloud.google.com/apis/library/androidpublisher.googleapis.com` |
| Firebase (Android push) | `console.firebase.google.com` |

**Services**

| Destination | URL |
|---|---|
| OneSignal | `dashboard.onesignal.com` |
| RevenueCat | `app.revenuecat.com` |

## Verify by screenshot

"Done" is not verification. For anything one-time, irreversible, or easy to get subtly wrong, ask for a screenshot and read it yourself.

Ask for it naturally and specifically: "screenshot that page for me before you close it - I want to check the Key ID matches." Framing it as your check rather than their test keeps it from feeling like homework.

Always verify by screenshot:

- Any identifier after creation - string and capabilities
- Any key page before they navigate away - the Key ID is on screen and nowhere else afterwards
- Anything with a role or permission attached
- Anything you'll later have to match against something else

Accept "done" for reversible, low-stakes steps. Asking for a screenshot of every click is its own way to lose someone.

When you read a screenshot, **say what you saw**. "That's the right Key ID and it matches the file - we're good" tells them the check was real. Silent approval feels like you weren't looking.

## What to check per artifact

| Artifact | What to confirm in the screenshot |
|---|---|
| Every screenshot | The team or account shown in the header - wrong team is silent and expensive |
| App ID | Exact string, Explicit not Wildcard, its own distinct name, correct capabilities ticked |
| App Group | `group.` prefix, exact suffix, linked to the right identifiers |
| APNs key | Key ID, that it's an APNs key, and that the file actually saved |
| App Store Connect API key | Key ID, Issuer ID, and **App Manager** role - not Admin |
| In-App Purchase key | Key ID and the Issuer ID **from that page**, which differs from the API page |
| Play service account | Email, and the Cloud IAM roles if RevenueCat will use it |
| Play permissions | Admin, or App admin on the target app |
| App record | Bundle ID selected, exact match |

## Resuming

When they come back:

1. Re-orient in one line before anything else - "picking up where we left off, identifiers and the push key are done"
2. Verify the thing they just did before moving on, even if they said it went fine
3. Continue at the next step with the progress marker - "that's 5 of 10"

If they hand you a file, confirm what you received - name and Key ID - before uploading it anywhere. A key with the wrong Key ID uploaded into the right field fails in a way that names nothing, and you'll both spend an hour on it.
