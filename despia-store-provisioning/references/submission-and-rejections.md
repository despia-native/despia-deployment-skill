# Submission and rejections

## Contents

- [Pre-submission checklist](#pre-submission-checklist)
- [Submitting](#submitting)
- [When a rejection lands](#when-a-rejection-lands)
- [The Despia rejection library](#the-despia-rejection-library)
- [Writing the reply to review](#writing-the-reply-to-review)
- [Resubmitting](#resubmitting)

## Pre-submission checklist

Run it and report as a list, same style as the audit. Anything missing blocks submission and the console won't always say which thing.

**Apple**

- Build uploaded, processed, and selected on the version
- Name, subtitle, description, keywords, promotional text
- Screenshots for every required size, RGB, no transparency, matching the actual app
- Support URL and privacy policy URL both live without a login
- Category, age rating, price
- App Privacy complete
- Export compliance, IDFA, content rights answered
- Demo account if anything is behind a login
- Agreements in effect - Paid Applications if there's any purchase

**Google**

- AAB uploaded to a track
- Title, short description, full description
- Feature graphic 1024×500, at least two screenshots
- All App content sections green: privacy policy, ads, app access, content rating, target audience, data safety
- Store settings and contact details
- For personal accounts, the closed testing requirement satisfied - read the rule off their console rather than quoting a number

## Submitting

Fill everything, run the checklist, show it, and **let the user press Submit.** Not because the click is hard, but because submission starts a review against their developer account, and the person whose account it is should be the one to start it. Say plainly that it's ready and what the button is.

Then set expectations: Apple typically 1-2 days, occasionally up to a week. Google typically 1-3 days, longer for a first release on a new account. Tell them the app can be rejected and that it's routine, not a verdict - roughly a third of apps get rejected at least once, and it usually means one fixable thing.

## When a rejection lands

The user will paste the rejection message, often panicking. Order of operations:

1. **Say it's normal and fixable, in one line.** Not a paragraph of reassurance - they want the fix.
2. **Find the guideline number.** Apple cites it explicitly (4.2, 2.1, 5.1.1). Google cites a policy name. That's your lookup key.
3. **Read what the reviewer actually said**, including screenshots attached in Resolution Center. The guideline number tells you the category; the reviewer's note tells you what they saw.
4. **Check the Despia rejection library** before reasoning from scratch - most of these are known and already written up.
5. **Diagnose against the actual app**, not the guideline text. 4.2 on a Despia build is usually design or missing native features; 2.1 is usually a crash or a login wall with no demo account.
6. **Give the fix and whether it needs a rebuild.** This is the question they care about most: a web-layer fix ships over the air in minutes, a native config change means a rebuild and a new submission.

## The Despia rejection library

`setup.despia.com` has pages written for these exact situations, and `blog.despia.com` has longer pieces. Fetch the relevant page rather than improvising - it carries the current recommended fix, which drifts as the stores change.

Known pages under `setup.despia.com`:

| Rejection | Path |
|---|---|
| Overview | `/store-rejections/introduction` |
| 4.2 minimum functionality | `/store-rejections/common-rejection/minimum-functionality` |
| Looks like a website, not an app | `/store-rejections/common-rejection/non-mobile-design` |
| In-app purchase issues | `/store-rejections/common-rejection/in-app-purchases` |
| Misleading or dark-pattern paywalls | `/store-rejections/common-rejection/deceptive-paywalls` |
| Privacy policy missing or inadequate | `/store-rejections/common-rejection/privacy-policy` |
| ATT / tracking transparency | `/store-rejections/common-rejection/tracking-transparency` |
| Social login without the native option | `/store-rejections/common-rejection/social-login-options` |
| Blank or white screen during auth | `/store-rejections/common-rejection/blank-screen-redirects` |
| AI processing without consent | `/store-rejections/common-rejection/ai-processing` |
| Collecting unnecessary personal data | `/store-rejections/common-rejection/user-specific-data` |
| Too similar to existing apps | `/store-rejections/common-rejection/spam-and-copies` |

Related build-side pages: `/roadblocks/deployment/apple-ios/att-and-tracking`, `/roadblocks/deployment/apple-ios/health-kit`, `/roadblocks/deployment/update-bundle-id`, and the runtime pages under `/roadblocks/runtime/` for blank screens, lost auth tokens, and OTA failures.

The full index is at `setup.despia.com/llms.txt` - check it if the rejection doesn't match anything above, since pages get added.

## Writing the reply to review

Most rejections are answered in Resolution Center, and the reply matters as much as the fix. What works:

- Address the specific guideline they cited, by number
- State what changed, concretely. "We added Face ID login, push notifications, and offline mode" beats "we have improved the app"
- If they misunderstood something, explain it politely and neutrally - reviewers are people and there's a human on the other end who can reconsider
- Include demo credentials again, even if they were already provided
- Keep it short. Nobody is reading three paragraphs

Never argue the guideline itself, and never resubmit unchanged with a longer explanation - that reliably burns another review cycle.

## Resubmitting

- **Web-layer fix** (design, copy, flows, most 4.2 responses): ships over the air. No rebuild, no new binary - but the user still replies in Resolution Center so the reviewer looks again
- **Native change** (capabilities, permissions, ATT, new SDK): rebuild in Despia, upload, select the new build, resubmit
- Second reviews are usually faster than the first

Tell them which of the two they're in. Not knowing whether they need a rebuild is what makes a rejection feel unbounded.
