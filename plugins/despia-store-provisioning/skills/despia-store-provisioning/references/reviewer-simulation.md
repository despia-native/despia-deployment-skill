# Reviewer simulation

Run this before every submission. One avoided rejection saves the user a week, and roughly a third of apps are rejected at least once - almost always for something visible in ten minutes of looking.

Two passes: walk the app as a reviewer would, then verify the native features actually work on a device.

## Pass 1 - walk it like a reviewer

Open the app the way a reviewer will: a device or a phone-sized browser, a fresh session, no existing account, the demo credentials as provided. Not the founder's logged-in browser with their data in it.

### The first thirty seconds

Reviewers form a verdict fast. Check:

- Does it open to something usable, or a login wall with no way past?
- Do the provided demo credentials work, right now, from a clean session?
- Is there content, or empty states everywhere?
- Does it look like an app or a website in a frame? Header height, tab bar, safe areas, touch targets, no hover-only interactions

### Then walk every path

- Every button and link - anything dead or 404 is a rejection
- Any link leaving the app: does it open in the system browser where it should, or trap the user in a WebView with no back?
- The paywall: does it load products, or show an empty sheet? An empty paywall is an automatic rejection
- Sign-up and sign-out, then relaunch - is the session still there?
- Any feature named in the description or shown in a screenshot: does it exist and work?

### The checklist that catches most rejections

| Check | Guideline it prevents |
|---|---|
| Demo credentials work from a clean session | 2.1 |
| No blank or white screens, especially after auth | 2.1 |
| Native features present and actually reachable | 4.2 |
| Doesn't read as a desktop site on a phone | 4.2 |
| Digital goods sold through native billing only, no Stripe links | 3.1.1 |
| Sign in with Apple present if other social logins are | 4.8 |
| ATT prompt appears if AppsFlyer or AdMob are in the build | 5.1.2 |
| Account deletion reachable in-app | 5.1.1 |
| Privacy policy URL loads without a login | 5.1.1 |
| Screenshots and description match what the app actually does | 2.3 |
| Nothing labelled "coming soon" or "beta" in the UI | 2.2 |
| Permission prompts have specific, non-generic reasons | 5.1.1 |
| No placeholder or lorem text anywhere | 2.3 |

Report findings the same way as the audit: **FAIL** you can fix, **BLOCK** they must fix, **WARN** worth knowing. Then fix what you can and re-walk the affected paths.

## Pass 2 - smoke test the native layer

The store console can't tell you any of this, and it's the difference between a build that passes and one that comes back. Needs a real device with the current build installed - simulators can't do push or purchases.

- **Push**: permission prompt appears, device shows in OneSignal subscriptions, test notification arrives with the app closed
- **Purchases**: sandbox purchase completes end to end and appears in RevenueCat's customer history; restore purchases works
- **Deep links**: a link from the user's domain opens the app rather than the browser - which means `apple-app-site-association` and `assetlinks.json` are actually hosted and reachable
- **OTA**: change something trivial in the web app, deploy, force-close, reopen - does it appear? If not, the service worker is the usual culprit
- **Safe areas**: nothing under the notch, nothing behind the home indicator, on a device that has them
- **Offline**: airplane mode, reopen - a controlled offline state rather than a white screen
- **Rotation and keyboard**: no layout collapse, no content hidden behind the keyboard

## Report it as a go / no-go

End with a verdict, not a list:

```
REVIEWER SIMULATION - Example App

Ready to submit, with 2 things to fix first:

FAIL   Demo account   the credentials in App Review Info don't work -
                      I get "invalid password" from a clean session
FAIL   Dead link      "Help" in Settings goes to a 404
WARN   Empty states   the demo account has no data; a reviewer sees
                      blank screens on 3 of 5 tabs

PASS   Native features, paywall, ATT prompt, deletion flow,
       privacy policy, safe areas, push, OTA

Both FAILs are quick. Fix them and this looks like a clean submission.
```

If something is a likely rejection rather than a certain one, say so with the odds you actually believe - "this will probably come back for 4.2" is more useful than a hedge, and being right builds the trust that makes the next warning land.
