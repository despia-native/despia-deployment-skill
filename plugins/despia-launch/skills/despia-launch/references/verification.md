# Verification

The audit is the payoff of the whole flow. Provisioning fails silently - Apple and Google will happily let a user finish with a group linked to the wrong identifier or a capability that was never ticked, and the first symptom is an opaque build error days later that they have no way to trace back.

This is also a **standalone entry point**. "Can you check my setup is right?", "why won't my build sign?", and "did I do this correctly?" all land here without any of the earlier steps having been run by you.

## How to run it

**Read-only.** Open, read, compare, close. Never fix something mid-audit - a fix changes state you're still auditing, and the user loses the picture of what was actually wrong. Collect every finding, report, propose, then act only on an explicit yes.

Take the provision matrix as the expected state. If you didn't build one (standalone audit), build it now from the Despia project before opening anything else - otherwise you're checking Apple against Apple, which always passes.

## Cross-object consistency

These are the checks worth the most, because no single console can catch them. One string has to be identical in five places:

| Check | Compare | Failure means |
|---|---|---|
| Core identity | Despia iOS Bundle ID = Apple identifier = App Store Connect record's Bundle ID = OneSignal app Bundle ID | Push silently never arrives, or the build signs against the wrong record |
| Android identity | Despia package name = registered Play package name = the listing's package | Uploads rejected; unfixable without a new listing |
| Team | Team ID in Despia = Team ID in OneSignal = the team that owns the identifiers | Key rejected as invalid with no useful error |
| Same team throughout | Every identifier, group, key, and the App Store Connect record all live under the approved Team ID - not split across a personal and a client team | Signing fails with nothing pointing at the cause, and the misplaced objects usually can't be moved |
| APNs key | Key ID in OneSignal = Key ID of an active APNs key in the developer portal | Push fails only in production, often after launch |
| Key routing | The `.p8` in Despia is the App Store Connect API key (matches the Key ID under Users and Access), and the `.p8` in OneSignal is the APNs key (matches a Key ID under Keys) | Swapped keys: Despia rejects its credential and push never sends, with neither error naming a key |
| Extension pairing | Each extension identifier's group = the group the matrix assigns it | Rich push, widgets, or share silently do nothing |

Compare character by character, case included. Do not eyeball a 10-character Key ID.

## Apple Developer Portal checks

For each identifier in the matrix:

- It exists, as an **Explicit** App ID (not Wildcard)
- The string matches exactly
- **Its name is unique across the team's identifiers.** Two identifiers sharing a name breaks deployment, and nothing in the build error points at it - this check is cheap and catches a failure that is otherwise very hard to diagnose
- Every capability the matrix requires is enabled
- **No capability the matrix doesn't require is enabled.** Extras aren't neutral - an entitlement the build doesn't carry can fail signing, and iCloud or Associated Domains enabled by accident drags in configuration the user never did
- App Groups is configured, and the selected groups are exactly the matrix set - no missing ones, no extras
- The identifier belongs to the team the user is actually building under

For App Groups:

- Each group in the matrix exists, with the `group.` prefix
- The suffixes match the map (`sharetarget` for the share extension, `widgetsharing` for the widget - these do not mirror their identifier suffixes)

For keys:

- An active APNs key exists, and the user still has the `.p8`
- No more than two APNs keys are active (Apple's limit; a third can't be created)

## App Store Connect checks

- An app record exists for this Bundle ID, and only one. **Without it nothing can be uploaded and TestFlight doesn't exist for the app** - this is the check that matters most on the App Store Connect side
- The record's Bundle ID is the matrix value, not a similar one from another project
- Platform is correct
- An internal testing group exists and has at least one tester in it, including the user's own Apple ID
- API key exists as a **Team Key** with **App Manager** access - not Admin, not Developer. Despia only accepts App Manager, and the role can't be changed after creation, so a wrong role means generating a new key
- Issuer ID and Key ID recorded, `.p8` still in the user's possession
- Agreements: which are in effect, which are outstanding. Paid Applications matters the moment there's any in-app purchase
- Whether the account role can do what's still left

## Google Play checks

- Package name registered and matching
- A Cloud project is linked under API access
- Google Play Android Developer API is enabled on that project
- The credential is a genuine **service account** - the JSON contains `"type": "service_account"` and a `client_email`, not user or OAuth client credentials
- The service account email has been invited under Users and permissions and shows as **Admin**, or at minimum **App admin** on the target app
- The JSON key is uploaded to Despia
- An internal testing track exists with an email list attached, including the user's own Google account

Remember the two false alarms before flagging anything: permissions can take up to 24 hours to propagate, and a brand-new listing often needs one manual upload before the API path works.

## Despia-side checks

- Source URL is HTTPS, loads, and is the **real production URL** - not a placeholder or staging address
- Version is set
- The correct Apple Development Team is selected
- The **numeric App Store App ID** is entered, and matches the Apple ID on the App Store Connect listing
- Icons and splash uploaded into their correct sections, each showing complete, correct dimensions, correct transparency, splash between 2 and 199 frames
- All credentials the project asks for are filled in
- No feature is toggled on in the editor whose provisioning is missing from the portal - this is the check that catches someone enabling widgets last week and never provisioning them

## The report

Give the user a flat list. No prose walkthrough of what you clicked.

```
AUDIT - Example App

PASS   Bundle ID           com.example.app matches across Despia, Apple, ASC, OneSignal
PASS   Push capability     enabled on core identifier
PASS   App Group           group.com.example.app.onesignal created and linked to both IDs
FAIL   Widget identifier   Despia has widgets enabled, com.example.app.ImageWidget not registered
FAIL   iCloud              enabled on core identifier but unused - remove
WARN   APNs key            2 of 2 active keys, one unaccounted for
BLOCK  Paid Applications   not accepted - you must accept this, only the Account Holder can
PASS   Play package        com.example.app registered and linked
WARN   Service account     created 10 min ago, permissions may take up to 24h to propagate

3 issues I can fix now. 1 needs you. 2 are just timing.
Fix the two FAILs?
```

Four states, and the distinction matters more than the count:

- **PASS** - verified against the matrix
- **FAIL** - wrong, and you can fix it
- **BLOCK** - wrong, and only the user can fix it (role, agreement, payment, anything legal)
- **WARN** - probably fine, worth knowing (propagation delays, unexplained keys, name mismatches that don't break anything)

End with what you'd do next and ask before doing it. A user who can see the difference between "3 I can fix" and "1 needs you" knows exactly how much of their attention this needs - which for most non-technical founders is the actual thing they wanted from the whole process.

## After fixing

Re-run only the checks that were failing, and the cross-object checks - a fix on one side can break a match on the other. Show the corrected lines, not the whole report again.
