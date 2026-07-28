# Screenshots

A Despia app is a web app in a native shell, which means the real UI is already reachable in a browser. That's an unusual advantage: you can capture genuine screens without a device, a simulator, or a build, and then design proper store screenshots around them.

This matters more than founders expect. Screenshots are the highest-leverage asset on a store page - most people decide from the first two thumbnails in search results, before reading a word. A raw unframed screen capture with no caption converts badly, and that's what almost everyone ships.

## Contents

- [Learn the app before capturing](#learn-the-app-before-capturing)
- [Capturing real screens](#capturing-real-screens)
- [Designing the screenshots](#designing-the-screenshots)
- [Sizes](#sizes)
- [Getting them into the stores](#getting-them-into-the-stores)
- [What gets rejected](#what-gets-rejected)

## Learn the app before capturing

Don't ask "which screens do you want". They don't know, and it's your job to have an opinion.

1. **Get the web app URL** - it's the Dynamic App Store Source in Despia, so you may already have it
2. **Open it and actually read it.** Navigate the app, see what it does, notice which screens carry the value. Do this before asking anything - arriving with "your dashboard and the booking flow look like the strongest two, plus the profile screen" is a much better conversation than an open question
3. **Read their landing page too**, if they have one. The value propositions are usually already written there, better than they'd phrase them on the spot
4. **Then confirm and fill gaps:** "Here's what I'd show and the line I'd put on each. What's the one thing people love most about it?" Their answer to that becomes the first screenshot

If the app needs a login, ask for a demo account - you'll need one for review anyway, so it's not an extra ask.

**Use realistic content.** Empty states and placeholder data make an app look dead. If the account you're capturing has nothing in it, ask them to add a few real-looking entries first, or capture from an account that does. This is the single biggest quality difference between screenshots that work and screenshots that don't.

## Capturing real screens

Open the app in a browser at a phone viewport - 390 × 844 CSS pixels is a good iPhone default, 412 × 915 for Android - and capture at 3× device pixel ratio so the result is sharp at store resolution.

Before capturing:

- Dismiss cookie banners, chat widgets, and dev overlays - they're not part of the app
- Scroll to the top
- Check nothing is mid-load or mid-animation
- Watch for anything personal in the frame: real names, emails, addresses, phone numbers, payment details. Blur or replace it

Capture four to six screens: the main screen first, then the two or three that carry the app's actual value, then something that builds trust if it exists.

## Designing the screenshots

Don't ship the bare capture. Compose each one in HTML/CSS and render it at the exact required pixel size - that gives full control over type, spacing, and framing, and produces a consistent set.

A composition that works:

- **Caption at the top**, one short benefit line, large and legible at thumbnail size. This is the mistake everyone makes - text sized for a desktop monitor is unreadable in search results. If it isn't legible when scaled to about 15% width, it's too small
- **The device-framed or full-bleed screen below**, occupying most of the height
- **A background** that carries the brand: solid, subtle gradient, or a soft accent colour pulled from the app's own palette
- **The same layout across the whole set** - varying the design per slide looks unfinished

Content rules:

- One benefit per screenshot, in the user's own language, not feature names
- The strongest one goes first; assume most people see only screenshots one and two
- Read as a sequence, so the set tells a small story rather than repeating the same claim
- Benefits over features: "Get paid in 2 days" beats "Invoicing module"

Save PNGs to disk at full size, then show the user before uploading anything - this is a visual asset and they'll have opinions worth hearing.

## Sizes

Apple currently needs one iPhone size and, if the app supports iPad, one iPad size - the store scales the rest:

| Target | Portrait pixels |
|---|---|
| iPhone 6.9" | 1290 × 2796 (1320 × 2868 also accepted) |
| iPad 13" | 2064 × 2752 (2048 × 2732 also accepted) |

Google Play:

| Asset | Spec |
|---|---|
| Phone screenshots | 2-8, 16:9 or 9:16, min 320px, max 3840px on any side |
| Feature graphic | 1024 × 500, required |

**Read the required sizes off the upload panel in the console rather than trusting this table.** Apple has changed its screenshot requirements repeatedly and states the current list right there in the media manager. Generate to whatever it says.

Both stores: RGB, no alpha channel, PNG or JPEG.

## Getting them into the stores

**If you can drive the browser**, upload them directly - App Store Connect's media manager on the version page, Play Console under Main store listing → Graphics. Confirm each set previews correctly afterwards.

**If you can't**, save the files to a folder, name them in display order (`01-home.png`, `02-booking.png`), tell the user exactly where they are, and walk them through the upload one store at a time. Give the drag-and-drop target by name.

The feature graphic is Android-only and easy to forget - it blocks the Play listing from being submitted, and it's a 1024 × 500 banner you can compose the same way.

## What gets rejected

- **Screenshots that don't match the app.** Mockups, "coming soon" panels, or features that aren't built. Apple checks this, and it's a guaranteed rejection
- **Device frames of the wrong platform** - an iPhone frame on a Play listing looks careless and can be flagged
- **Text that overpromises** in ways the app doesn't deliver
- **Anything with someone's real personal data in it**

If the app looks like a desktop website squeezed into a phone, screenshots will make that obvious to a reviewer. Say so plainly - it's a 4.2 rejection waiting to happen, and it's a design fix in the web app, not a screenshot fix.
