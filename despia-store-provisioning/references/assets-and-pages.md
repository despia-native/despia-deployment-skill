# Assets and required pages

Everything the stores require that a solo founder typically doesn't have: an icon that meets spec, a splash screen, and four web pages that block submission by their absence.

## Contents

- [App icons](#app-icons)
- [Splash screen](#splash-screen)
- [Feature graphic](#feature-graphic)
- [Privacy policy](#privacy-policy)
- [Terms of service](#terms-of-service)
- [Support page](#support-page)
- [Account deletion page](#account-deletion-page)
- [Deep link files](#deep-link-files)

## App icons

Both platforms need 1024 × 1024 PNG with **no alpha channel**. An alpha channel fails the build or gets rejected, and it's the default export from most design tools - check it, don't assume.

If the user has a logo, compose the icon around it. If they don't, generate one from the brand: a single letterform or simple mark on a solid or subtly gradient background. Resist detail - icons render at 60px on a home screen, so anything intricate turns to mud.

**iOS**: standard padding, logo can sit closer to the edge. iOS applies its own corner radius, so supply a square with a full-bleed background - never pre-round the corners or add your own shadow.

**Android**: noticeably more padding - roughly 30-40% more safe area than the iOS version. Android crops and masks into the icon, so the mark must be smaller and centred. Despia previews this - check the preview rather than trusting the flat file.

Generate both from the same source with different safe areas, and show the user the pair side by side before uploading.

## Splash screen

1024 × 1024 GIF, **animated - it must have more than one frame**, and fewer than 200. **Transparent background for Android**; follow the platform section in the Despia docs for iOS, since the requirement differs.

The frame count is not a style preference. The splash renders through SwiftyGif, which needs a genuine animated GIF: a single-frame GIF - which is what most tools export when you give them a static image - fails. Over roughly 200 frames it breaks the other way. If the user wants a still logo, give it a minimal two-frame fade or scale so it satisfies the format while looking static.

Check the frame count of whatever you export rather than assuming. "Export as GIF" from a static design produces exactly the file that doesn't work, and the failure appears at build time, not at upload.

Keep animation under two or three seconds - a splash the user waits through is worse than none. Fade or scale in is enough; the goal is covering the WebView's first paint, not entertainment.

## Feature graphic

Android only, 1024 × 500, and **it blocks the Play listing from being submitted**. Easy to forget because it has no iOS equivalent.

App name, a short tagline, and the mark on a brand background. Keep text well inside the edges - Play crops it in some placements.

## Privacy policy

Required by both stores, must be live, must be reachable without a login, and must match the App Privacy and Data safety declarations exactly.

Generate it from the same SDK table used for the declarations - see `references/declarations.md`. It should cover:

- What's collected, and by which services, named: OneSignal, RevenueCat, AppsFlyer, PostHog, Stripe, whatever's actually in the build
- Why each category is collected
- Whether data is shared, and with whom
- How long it's kept
- How a user requests deletion, with the mechanism
- Children's data, if the app is available to under-13s
- A contact address that a person actually reads

**Say plainly that this is a generated starting point, not legal advice**, and that a founder operating in a regulated space or in the EU should have it reviewed. Don't let a generated policy read as though it's been lawyered.

Host it wherever their site lives - a page on their own domain is better than a third-party generator link, because the URL has to stay alive as long as the app does.

## Terms of service

Not always required, but needed for anything with subscriptions - and Apple expects auto-renewing subscription terms to be reachable. Cover the service, payment and renewal terms, cancellation, acceptable use, liability, and governing law. Same caveat as the privacy policy.

## Support page

Both stores require a support URL. It can be simple: what the app does, how to get help, an email address that works, and a short FAQ. A dead support URL is a rejection, so check that whatever they give actually resolves.

## Account deletion page

Google requires a **publicly reachable web URL** where a user can request account deletion, in addition to the in-app path. It must be usable without installing the app.

Minimum: what gets deleted, what's retained and for how long, and either a form or a clearly stated email process. Pair it with the in-app deletion flow - the store checks for both.

## Deep link files

If Associated Domains or App Links are enabled, the capability does nothing until these are hosted on the user's domain. This is the step people provision and then forget, so the feature quietly never works.

- **iOS**: `https://theirdomain.com/.well-known/apple-app-site-association` - JSON, served as `application/json`, **no file extension**, no redirects, HTTPS only. Contains the Team ID and Bundle ID
- **Android**: `https://theirdomain.com/.well-known/assetlinks.json` - contains the package name and the SHA-256 signing certificate fingerprint

Generate both with the real values, tell the user exactly where they go, and then **verify by fetching the URLs** - a redirect, a wrong content type, or a 404 all break it silently. `/native-features/deeplinking` has the current format.

The Android fingerprint comes from the signing key Despia uses. If the user can't find it, that's a support question rather than something to guess at.
