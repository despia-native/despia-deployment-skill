# Rejection fixes

Diagnosing a rejection is the easy half. This file is the other half: what actually gets changed, where, and whether it ships over the air or needs a rebuild.

**Before writing any Despia SDK code, fetch the relevant page from `setup.despia.com`.** The exact scheme names and payload shapes are documented there and they change; writing them from memory produces code that silently no-ops. The fixes below give the shape of the change and the page to read - not invented API signatures.

## Contents

- [How to run a fix](#how-to-run-a-fix)
- [4.2 Minimum functionality](#42-minimum-functionality)
- [Looks like a website](#looks-like-a-website)
- [3.1.1 External payments for digital goods](#311-external-payments-for-digital-goods)
- [2.1 Crashes, blank screens, login walls](#21-crashes-blank-screens-login-walls)
- [ATT and tracking](#att-and-tracking)
- [Account deletion](#account-deletion)
- [Privacy policy and data declarations](#privacy-policy-and-data-declarations)
- [Sign in with Apple missing](#sign-in-with-apple-missing)
- [OTA or rebuild](#ota-or-rebuild)

## How to run a fix

1. Read the reviewer's note and the guideline number - the note says what they saw, the number says which rule
2. Fetch the matching page from the Despia rejection library (`references/submission-and-rejections.md` has the map)
3. Reproduce it yourself in the browser before changing anything. If you can't reproduce it, you don't understand it yet
4. Make the change, or hand the user an exact diff with the file and location if you can't write to their codebase
5. Verify by reproducing the reviewer's path again
6. Say clearly whether this ships over the air or needs a rebuild, then reply in Resolution Center

Most Despia users build in Lovable, Claude Code, Cursor, or similar. If you can't edit their project directly, produce the change as a paste-ready block with a one-line instruction on where it goes - that's still most of the work done for them.

## 4.2 Minimum functionality

**What the reviewer saw:** an app that does nothing a mobile browser wouldn't.

**The fix is added native capability, not an argument.** Pick features the app can plausibly use and wire them properly - a feature that exists but is never triggered is worse than none, because it reads as gaming the rule:

| Feature | Fits when | Docs |
|---|---|---|
| Push notifications | Anything with updates, orders, messages | `/native-features/onesignal/` |
| Biometrics | Anything with a login or sensitive data | `/native-features/biometrics` |
| Camera / photo | Uploads, profiles, scanning | `/native-features/camera-roll` |
| Haptics | Any interactive UI - cheap and immediate | `/native-features/haptic-feedback` |
| Offline support | Content the user re-reads | `/native-features/service-workers` |
| Native purchases | Any paid product | `/payments/revenuecat/` |
| Location | Anything local or delivery-based | `/native-features/gps-location` |
| Share sheet | Any shareable content | `/native-features/share-dialog` |

Two or three implemented well beat six half-wired. Push plus one thing tied to the app's actual purpose is the usual answer.

Then say so explicitly in the reply: name the features, and say where in the app a reviewer will find them.

## Looks like a website

Often bundled with 4.2, sometimes its own note. The fix is design, and it's the one case where the honest answer is "this needs real work in the web app":

- Native-height header and bottom tab bar rather than a desktop nav
- Safe-area handling so content doesn't sit under the notch or home indicator - `/native-features/safe-areas`
- Touch targets at 44pt minimum, no hover-dependent interactions
- Momentum scrolling, no fixed desktop-width containers
- No browser chrome artifacts: no "click here", no footer sitemap, no cookie banner
- Transitions between views rather than full page reloads

`/best-practices/frontend/structure` and `/roadblocks/runtime/wrong-framework` cover the patterns. If the app fails most of these, tell the user plainly that this is a redesign, not a tweak - stringing them along through three more rejections is worse.

## 3.1.1 External payments for digital goods

**What the reviewer saw:** Stripe checkout, a payment link, or a web upgrade page selling something consumed inside the app.

Digital goods and subscriptions must use native billing. Physical goods and real-world services must *not*. The fix:

1. Replace the digital-goods checkout path with native purchase calls - `/payments/revenuecat/`
2. Set up products, entitlements and offerings - `references/revenuecat-iap.md`
3. Remove links that route to external purchase pages, including in help text and emails opened in-app
4. Keep Stripe for physical goods, and route those flows to the system browser rather than the WebView - `/native-features/external-links`

`/store-rejections/common-rejection/in-app-purchases` has the current guidance. This is a rebuild.

## 2.1 Crashes, blank screens, login walls

Three different causes behind one guideline.

**Blank or white screen.** Usually an auth redirect leaving the WebView, or a service worker serving a broken cache. `/roadblocks/runtime/empty-pages` and `/store-rejections/common-rejection/blank-screen-redirects`. If the app has a service worker, check it first - a bad one breaks OTA updates and produces white pages.

**Login wall.** The reviewer couldn't get in. Provide demo credentials in App Review Information, verify they work from a clean session, and make sure the account has realistic data. This alone resolves a large share of 2.1s and needs no code change at all.

**Lost session.** Users - and reviewers - logged out on relaunch. `/roadblocks/runtime/lost-auth-tokens`.

## ATT and tracking

Triggered when AppsFlyer or AdMob are present, or when the privacy declarations claim tracking.

- The ATT prompt must actually appear, before any tracking-dependent SDK initialises
- `NSUserTrackingUsageDescription` must be specific about what the app does with the data - generic strings get rejected on their own
- Declared IDFA usage must match observed behaviour in both directions: prompting without declaring, or declaring without prompting, both fail

`/roadblocks/deployment/apple-ios/att-and-tracking` and `/store-rejections/common-rejection/tracking-transparency`. Info.plist strings are a rebuild; prompt timing is web layer.

## Account deletion

Both stores require in-app account deletion for any app with accounts, and it's the most common thing a solo founder simply hasn't built.

Needs: a visible path in the app (usually Settings → Account → Delete account), a confirmation step, a backend endpoint that actually deletes or anonymises, and for Play a publicly reachable web deletion URL declared in the console.

If they haven't built it, that's a backend change - scope it honestly rather than describing it as a checkbox.

## Privacy policy and data declarations

Rejected for missing, unreachable, or inaccurate. The policy must be live without a login, cover every SDK in the build, and match the App Privacy and Data safety answers exactly. `references/assets-and-pages.md` covers generating one; `references/declarations.md` covers matching them.

## Sign in with Apple missing

If the app offers Google, Facebook, or other third-party login on iOS, Apple requires Sign in with Apple alongside it. `/native-features/oauth/apple` and `/store-rejections/common-rejection/social-login-options`. Web layer plus a capability - so a rebuild.

## OTA or rebuild

The question users care about most. Get it right, because telling someone to rebuild unnecessarily costs them a credit and days.

**Ships over the air:** design and layout, copy, flows, ATT prompt timing, adding a deletion UI that calls an existing endpoint, removing external payment links, most 4.2 responses that are about design rather than capability.

**Needs a rebuild:** enabling any native feature in the Despia editor, Info.plist usage strings, capabilities, ATT entitlement, push or purchase configuration, icons and splash.

Either way, the user still replies in Resolution Center - an OTA fix is invisible to a reviewer who isn't told to look again.
