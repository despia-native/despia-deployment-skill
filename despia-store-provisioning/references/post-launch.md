# After launch

The skill doesn't end at "approved". Everything here is work a hired developer would keep doing, and most of it is invisible until it breaks.

## Contents

- [The expiry calendar](#the-expiry-calendar)
- [Shipping updates](#shipping-updates)
- [Reviews and ratings](#reviews-and-ratings)
- [Subscription health](#subscription-health)
- [Appeals and expedited review](#appeals-and-expedited-review)
- [Store presence over time](#store-presence-over-time)

## The expiry calendar

These are the silent killers. Each one takes an app that has been working for months and breaks it with no deploy, no change, and no warning the user will notice.

| Expires | Consequence | Lead time |
|---|---|---|
| Apple Developer Program membership, annually | App removed from sale, builds blocked | Renew a month early |
| Google Play developer account (payment method on file) | Publishing blocked | Keep the card current |
| APNs `.p12` certificate, if one is used instead of a `.p8` | Push stops dead | Migrate to `.p8` - it doesn't expire |
| Apple agreements when Apple revises them | **In-app purchases stop loading** until re-accepted | Check whenever IAP suddenly breaks |
| Play Data safety and content rating recertification | Listing flagged, updates blocked | Whenever Play asks |
| App Store Connect API and In-App Purchase keys, if revoked | Uploads fail, RevenueCat validation fails | Only on revocation |
| Domain and hosting for privacy policy, support, AASA files | Deep links and compliance break | Same renewal as the domain |

Hand the user this list at the end of the first launch, with their own dates filled in. It's the single most useful thing to leave behind, because none of it is discoverable from inside the app.

The Apple agreements one deserves special mention: Apple periodically revises the Paid Applications agreement, and until the Account Holder re-accepts, every in-app purchase silently stops loading. Founders lose days to this, and nothing in the app or the console points at it. **Check agreements first any time IAP breaks with no code change.**

## Shipping updates

**Web-layer changes** ship over the air. No submission, no review, no credit. This is most of what they'll do.

**Native changes** - editor settings, capabilities, icons, push or purchase config - need a rebuild and a new submission:

1. Bump the version and build number in Despia
2. Rebuild, upload, wait for processing
3. Add "What's New" text - required for Apple, and users read it
4. Select the build on the version, resubmit
5. Consider **phased release** on Apple, which rolls out over seven days and can be paused if something breaks

Second and later reviews are usually faster than the first. Tell them that; the first review's wait sets a pessimistic expectation.

## Reviews and ratings

- Both stores let the developer respond publicly, and it's worth doing - a reply on a one-star review is read by every future browser of the page
- Reply to negative reviews with what changed or what will, not with defensiveness
- Ratings prompts belong at a moment of success, never on launch or mid-task
- A wave of one-stars after an update usually means a regression - check crash reports and recent OTA deploys before assuming it's taste

## Subscription health

If the app monetises, this is where the money actually leaks:

- **Failed renewals and billing retry** - a chunk of churn is involuntary and recoverable with a prompt
- **Refunds and chargebacks** flow through RevenueCat; make sure entitlements revoke correctly
- **Grace periods** keep access alive during a retry rather than locking a paying customer out
- **Server notifications** must stay connected on both stores, or subscription status drifts out of date silently
- **Price changes** have their own consent rules on both platforms

Point them at `/best-practices/backend/revenuecat/webhooks` and `/best-practices/backend/revenuecat/cron-jobs` - the cron sync exists precisely because webhooks fail sometimes.

## Appeals and expedited review

**Appeals.** If a rejection is genuinely wrong, Apple has an appeal path separate from Resolution Center. Use it for a factual misunderstanding - never as a first move, and never for a rule they simply dislike. A calm, specific, evidence-backed appeal does sometimes win.

**Expedited review.** Apple grants a limited number for genuine emergencies: a critical bug affecting users, a security issue, or a hard deadline tied to a real event. Requesting one for an ordinary release burns credibility that isn't easily rebuilt, so use it rarely and honestly.

**Removal or suspension** is a different and more serious path. If an app is pulled, read the notice carefully, fix the cited cause completely before responding, and treat repeated violations as escalating - Google in particular suspends developer accounts, not just apps.

## Store presence over time

- Metadata other than the app name is editable at any time - iterate on the subtitle, keywords, and screenshots rather than treating launch copy as final
- Apple's promotional text updates without a build; useful for announcements
- Watch which keywords actually deliver installs and adjust the field over successive releases
- Seasonal screenshot updates are cheap and measurably effective

Encourage a small, regular loop here. Most solo founders ship once and never touch the listing again, and it's the highest-leverage thing they're leaving on the table.
