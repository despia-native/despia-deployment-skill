# RevenueCat and in-app purchases

The longest and most failure-prone part of shipping a paid app. It spans App Store Connect, Google Play Console, Google Cloud, RevenueCat, and the Despia editor, and several steps have delays measured in hours where nothing looks broken but nothing works.

Tell the user that shape up front. "This one takes a couple of sessions - some of it is waiting on Apple and Google, not on us" prevents the assumption that something is wrong.

## Contents

- [Apple credentials](#apple-credentials)
- [Creating products in App Store Connect](#creating-products-in-app-store-connect)
- [Google credentials](#google-credentials)
- [Creating products in Google Play](#creating-products-in-google-play)
- [Real-time developer notifications](#real-time-developer-notifications)
- [RevenueCat: products, entitlements, offerings](#revenuecat-products-entitlements-offerings)
- [The Despia side](#the-despia-side)
- [Testing](#testing)
- [Submitting for review](#submitting-for-review)
- [Known delays and failures](#known-delays-and-failures)

## Apple credentials

RevenueCat needs, per app: **App name, Bundle ID, In-App Purchase Key**, and for StoreKit 1 apps the **App-Specific Shared Secret**.

**In-App Purchase Key - required.** This is a *third* `.p8`, distinct from the APNs key and the App Store Connect API key.

1. App Store Connect → **Users and Access → Integrations → In-App Purchase**
2. **Generate In-App Purchase Key** (or **+** next to Active if one exists)
3. Name it, generate, **download once**
4. Copy the **Issuer ID from this page** - it is not the same Issuer ID as the App Store Connect API page, and using the wrong one is a common failure where RevenueCat's save silently resets the form
5. In RevenueCat → project → the App Store app → **In-app purchase key configuration** → upload the `.p8`, with Key ID and Issuer ID

One In-App Purchase Key covers every app in the same App Store Connect account.

**App-Specific Shared Secret** - only needed for StoreKit 1, which Apple has deprecated. If the RevenueCat SDK is v5+ / StoreKit 2, the In-App Purchase Key replaces it. If RevenueCat's dashboard asks: App Store Connect → your app → **General → App Information → App-Specific Shared Secret → Manage → Generate**. It's a 32-character string, not a file. Regenerating invalidates the old one.

**App Store Connect API Key** - optional here, used by RevenueCat to import products and prices automatically. This can be the same App Manager key created for Despia; RevenueCat needs its own upload of it under the **App Store Connect API** tab. Worth doing - it saves retyping every product identifier.

## Creating products in App Store Connect

Under the app → **Monetization → Subscriptions** (or In-App Purchases for one-time products).

**Subscriptions** live inside a **subscription group**. Products in the same group are upgrade/downgrade paths for each other, so monthly and annual of the same plan belong together. Create the group first, name it something the user will recognise later.

Per product:

- **Reference name** - internal
- **Product ID** - permanent, cannot be reused even after deletion. Use a stable convention like `pro_monthly`, `pro_annual`, and settle it with the user before creating anything
- **Duration** and **price** - pick a price tier; Apple generates the international prices
- **Localization** - display name and description, at least one language, required
- **Review information** - a **screenshot is required**, and a missing one is the usual reason a product sits in "Missing Metadata"

A product in **Missing Metadata** won't import into RevenueCat and won't be purchasable. If a product looks invisible everywhere, check its status here first.

Also set up, once per app: an **App Store subscription privacy policy URL**, and optionally the subscription terms - Apple blocks submission without them.

## Google credentials

RevenueCat's Play service account has **different requirements from Despia's**. Despia's needs no Cloud IAM roles; RevenueCat's does.

1. In Google Cloud, enable three APIs on the project: **Google Play Android Developer API**, **Google Play Developer Reporting API**, and **Cloud Pub/Sub API**. Skipping Pub/Sub produces an explicit error when connecting Google later
2. Service account with Cloud IAM roles **Pub/Sub Editor** (or Admin) and **Monitoring Viewer**
3. Generate a JSON key
4. Invite the service account email in Play Console → Users and permissions, with financial data and release permissions
5. Upload the JSON in RevenueCat → the Play Store app → service credentials, then use **Validate Credentials**

If a Cloud Console banner offers to "create credentials" through a wizard, ignore it - that produces an API key or OAuth client, which is not what's needed.

**Can it be the same service account as Despia's?** Yes, if it carries both the Cloud IAM roles above and the Play Console permissions. Simpler to reuse one; just be explicit with the user about which JSON is uploaded where, and don't assume a JSON already uploaded to Despia has the roles RevenueCat needs - check.

## Creating products in Google Play

**Monetize → Products → Subscriptions** (or In-app products).

Play's model has three layers, which surprises people coming from Apple:

- **Subscription** - the thing itself, with a permanent product ID
- **Base plan** - billing period and price, attached to the subscription
- **Offer** - optional free trial or intro price, attached to a base plan

Each layer has to be **activated** separately. A subscription with an inactive base plan simply doesn't exist to the SDK, and nothing warns you.

Play also requires the app to have a release on some track before monetisation is fully usable - this is why products and credentials often only start working after the first upload.

## Real-time developer notifications

Not strictly required, but RevenueCat strongly recommends it and it fixes lag in subscription status, charts, and webhooks.

1. In RevenueCat's Play app settings, below the credentials, either pick an existing Pub/Sub topic or let RevenueCat create one → **Connect to Google**
2. Copy the generated **topic ID**
3. Play Console → app → **Monetize → Monetization setup → Real-time developer notifications** → paste the topic name, select the option covering subscriptions, voided purchases, and one-time products
4. Send a test notification from Play Console and confirm RevenueCat receives it

If the test fails, add `google-play-developer-notifications@system.gserviceaccount.com` as a principal on that Pub/Sub topic with the **Pub/Sub Publisher** role.

Apple's equivalent is App Store Server Notifications, configured with the URL RevenueCat provides under the app's server notifications settings.

## RevenueCat: products, entitlements, offerings

Three concepts, and users routinely conflate them:

- **Product** - mirrors a store product, one per store product, identifier must match exactly
- **Entitlement** - what access the user gets, e.g. `pro`. Products attach to it. The app checks the entitlement, never the product
- **Offering** - what the paywall shows, containing packages (monthly, annual) that point at products

Import products from the stores if the API key is connected, rather than typing identifiers by hand - a typo here produces an empty paywall with no error.

Then: create one entitlement, attach every product that grants it, create a default offering with the packages the paywall should show.

**Test Store**: RevenueCat projects include one for development. If the user has been testing with it, the app must be switched to the real platform API key before submission, or purchases silently do nothing in production.

## The Despia side

In the Despia editor, enable the purchases feature and enter the **RevenueCat public SDK key** - the platform-specific one, from RevenueCat → project → API keys. Not the secret key, which never goes in a client.

Enabling purchases is an editor change, which means it is **not** an over-the-air update: it needs a rebuild and a new store submission. Say that before they enable it, because it changes what they need to plan for.

The web-layer implementation - calling the purchase and paywall schemes, checking entitlements, syncing user IDs - is documented at `setup.despia.com/payments/revenuecat/`. Point them there, or write the calls if you're also doing the app work.

## Testing

- **iOS**: sandbox testers from App Store Connect → Users and Access → Sandbox. Must test on a real device; the simulator can't do purchases. Sandbox subscription durations are compressed
- **Android**: license testers under Play Console → Setup → License testing, and the app must be installed from a Play track, not sideloaded
- Confirm the purchase appears in RevenueCat's Customer History - that's the proof the whole chain works

## Submitting for review

Apple reviews in-app purchases alongside a build. For the first submission, the products must be attached to the version being submitted - a very common miss, and the app comes back rejected for a paywall that leads nowhere.

Each product also needs its review screenshot and notes. If the paywall is behind a login, give reviewers a demo account that reaches it.

Google reviews subscriptions as part of the app; active products with an active base plan are live once the app is.

## Known delays and failures

- **Play credentials take up to 36 hours to activate**, sometimes longer. RevenueCat may show "credentials need attention" the whole time. A known nudge: edit and save any product description in Play Console to force a refresh
- **The app usually has to exist on a Play track** before credentials validate
- **Missing Metadata** on an Apple product blocks everything downstream, silently
- **Inactive base plan** on Play does the same
- **Empty paywall** almost always means product identifiers don't match, offerings aren't configured, or the app is still on the Test Store key. `setup.despia.com/roadblocks/revenue-cat/missing-item` covers this case
- **Paid Applications agreement not in effect** - no product will ever load. Check this first when nothing works at all
