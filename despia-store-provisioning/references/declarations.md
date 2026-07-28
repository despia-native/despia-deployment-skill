# Declarations and compliance forms

Apple's App Privacy questionnaire and Google's Data safety form are where non-technical founders get stuck hardest, because the honest answer is "I don't know what my app collects" - and they're right, they didn't write the SDKs.

You do know. Every SDK in a Despia build has a knowable data footprint, and the answers follow from which features are switched on. Work them out, fill them in, then have the user confirm before you commit.

**How to handle the attestation.** These forms are legal statements the user is responsible for. Do the work - derive every answer, enter it, explain what each one means in a line. Then show the completed set and get one explicit yes before submitting it. Don't ask them twelve questions they can't answer, and don't submit a legal declaration they've never seen.

## Contents

- [What each SDK collects](#what-each-sdk-collects)
- [Apple: App Privacy](#apple-app-privacy)
- [Apple: the other declarations](#apple-the-other-declarations)
- [Google: Data safety](#google-data-safety)
- [Google: the other declarations](#google-the-other-declarations)
- [Getting it wrong](#getting-it-wrong)

## What each SDK collects

Derive from the Despia project's enabled features. This is the table that turns "I don't know" into a filled form.

| Feature enabled | Data types | Linked to user? | Used for tracking? |
|---|---|---|---|
| OneSignal push | Device ID, push token, usage data | Yes if the app identifies users | No, unless combined with ads |
| RevenueCat purchases | Purchase history, user ID | Yes | No |
| Stripe payments | Purchase history, payment info handled by Stripe | Yes | No |
| AppsFlyer attribution | Device ID, advertising ID, usage data | Yes | **Yes** - this one triggers ATT |
| AdMob ads | Advertising ID, usage data, coarse location | Yes | **Yes** |
| PostHog analytics | Usage data, device ID, product interaction | Depends on identify() | No |
| Clerk auth | Email, name, user ID | Yes | No |
| GPS location | Precise or coarse location | Yes | No |
| HealthKit | Health and fitness data | Yes | Never - Apple prohibits it |
| Contacts | Contacts | Yes | No |
| Camera, photos | User content | Yes | No |
| Crash logs | Diagnostics | Usually no | No |

Plus whatever the web app itself collects - the account fields, anything sent to their own backend. Ask: "does your app have accounts, and what do you ask people for when they sign up?"

**Tracking has a specific meaning:** linking this app's data with third-party data for advertising or sharing with a data broker. AppsFlyer and AdMob mean yes and require the ATT prompt. Analytics alone does not.

## Apple: App Privacy

**App Store Connect → your app → App Privacy → Edit**

For each data type: is it collected, is it linked to the user's identity, is it used for tracking, and what for (App Functionality, Analytics, Product Personalisation, Advertising, Developer's Advertising). Walk the table above and answer per row.

Also on the page: a privacy policy URL, live and reachable without a login. Nothing submits without it.

## Apple: the other declarations

**Export compliance.** Asked on every build. An app that only uses HTTPS is generally exempt, and that's the usual answer for a Despia app - but frame it as "your app uses standard HTTPS encryption only, which qualifies as exempt; confirm that's accurate for you" rather than clicking through it. Answering it once in the build settings stops the per-upload prompt.

**Advertising identifier (IDFA).** Yes if AdMob or AppsFlyer are on. Then tick what it's used for, and the app must actually show the ATT prompt - a mismatch here is a guaranteed rejection.

**Content rights.** Does the app contain third-party content, and do they have rights to it.

**Age rating.** A questionnaire about violence, sexual content, drugs, gambling, and user-generated content. **User-generated content and unrestricted web access both raise the rating** - if the app has open comments or an in-app browser, answer honestly and expect 12+ or 17+.

## Google: Data safety

**Play Console → Policy → App content → Data safety**

Same underlying facts, different structure. Per data type: collected or shared, ephemeral or not, required or optional, and the purpose. Then:

- Is data encrypted in transit? Yes, for any HTTPS app
- Can users request deletion? If the app has accounts, there must be a way - and Google now wants a deletion URL. Flag this early if the user has no account-deletion flow; it's a build-blocker they can't fix in the console
- Independent security review, if any - almost always no

The Data safety answers must match the App Privacy answers. Different wording, same facts.

## Google: the other declarations

Under **App content**, all mandatory:

- **Privacy policy** URL
- **Ads** - does the app contain ads
- **App access** - if anything is behind a login, provide working demo credentials, or the reviewer sees a login wall and rejects it. This is the single most common Play rejection for Despia-style apps
- **Content rating** questionnaire - generates IARC ratings
- **Target audience and content** - age groups; anything targeting under-13 pulls in Families policy and much stricter rules
- **News app**, **COVID / health**, **financial features**, **government app** declarations - usually no, but each must be answered
- **Data safety** as above

## Getting it wrong

An inaccurate declaration isn't a form error, it's a policy violation - both stores can pull the app after it's live, and Apple rejects mismatches between declared data and observed SDK behaviour routinely.

So: don't understate to make the form simpler, and don't overstate to be safe either - declaring data you don't collect scares users on the product page for no reason.

When you genuinely can't determine something - what the user's own backend does with data, what a third-party service they added retains - ask, and if they don't know, say so plainly rather than guessing on their behalf. That's the one place where a wrong answer is theirs to own and not yours to invent.
