# Ship your app to the App Store and Google Play. This weekend. By yourself.

Most web-to-app platforms will happily sell you a publishing package. Store submission assistance, provisioning setup, "done for you" launch support. It runs well over $1,000, and what you get is someone clicking through consoles you could have clicked through yourself, if only you knew which buttons mattered.

Despia gives you the knowledge instead. This is **Despia Launch Agent**, an AI agent skill that walks the entire path from a finished web app to a live store listing, in your browser, with you. No agency. No retainer. No waiting three days for someone to reply to your email about a bundle ID.

**You keep the money and you keep the control.**

## What it actually does

Point a browser-capable AI agent at this skill and it runs the whole thing:

**Sets up your Apple and Google accounts**
Registers your Bundle IDs and App Groups, enables the right capabilities, creates your App Store Connect listing, generates your push and API keys, and gets your Google Play service account working. It knows which of the five near-identical credential files goes where, which is where most people lose an afternoon.

**Gets your app ready to be seen**
Writes your store copy and keywords using how each store actually ranks apps (they work completely differently). Captures your real screens and composes proper store screenshots. Generates your icons, splash screen, privacy policy, and the other pages the stores refuse to launch without.

**Fills in the forms nobody understands**
App Privacy, Data safety, export compliance, content ratings. It works out the honest answers from the features your app actually uses, explains each one in a sentence, and shows you the whole thing before anything is submitted in your name.

**Turns on the native features that get you approved**
Push notifications end to end, including the Firebase side for Android. In-app purchases end to end, including products, entitlements and offerings in RevenueCat. These are the features that stop a reviewer from calling your app "just a website".

**Catches rejections before Apple does**
Walks your app the way a reviewer will and tells you what is going to come back. A dead link, a login wall with no demo account, an empty paywall, a missing account deletion flow. One avoided rejection saves you a week.

**Fixes the ones that get through anyway**
Reads the rejection, finds the guideline, diagnoses it against your actual app, makes the change, and tells you the thing you most want to know: does this need a whole new build, or does it ship instantly over the air?

**Keeps you alive after launch**
Updates, reviews, subscription health, and the expiry calendar. That last one matters more than it sounds. Certificates expire, memberships lapse, and when Apple revises an agreement your in-app purchases quietly stop working until someone re-accepts it. Nothing in your app tells you. This does.

## What you need before you start

- A deployed web app on HTTPS
- An Apple Developer account, $99/year. **Start this first**, approval takes a day or two, and company accounts need a D-U-N-S number which takes longer
- A Google Play Console account, $25 once
- Chrome, or any Chromium browser. Safari automation is too limited to rely on
- Roughly a weekend, most of which is waiting on Apple and Google rather than working

## How it works with you

It is built for founders who do not write code, and it behaves like it.

**One step at a time.** Never a wall of instructions you have to hold in your head while switching tabs.

**It tells you where you are.** "That's step 4 of 10" and what's coming next, so the process has a visible end.

**It stops before anything permanent.** Registering a package name, reserving your app name, accepting a legal agreement, spending a build credit. It asks first, every time.

**It never guesses with your money.** Builds cost credits. It batches changes into one build and confirms with you before spending anything.

**When it cannot click, it guides.** Direct links to the exact page, the exact button to press, and it asks for a screenshot so it can check the work rather than taking your word for it.

**It checks everything at the end.** A full audit of both accounts against what your app actually needs, reported as: what's right, what it can fix, what only you can fix.

## What it does not do

Worth being straight with you.

- **It cannot guarantee approval.** Nothing can. It removes the avoidable rejections, which is most of them, not the judgment calls.
- **It does not write your app.** If your app looks like a desktop website squeezed onto a phone, that is a design problem and it will tell you so plainly rather than submitting and hoping.
- **It is not a lawyer.** It generates a privacy policy and terms as a starting point. If you are in health, finance, or handling EU user data, have a real one look at them.
- **It will not sign contracts for you.** Apple's agreements are yours to accept, and it will not click through them in your name.

## Getting started

1. Install the skill (below)
2. Open a chat with a browser-capable agent and say what you want: *"help me get my app on the App Store"*
3. Answer six questions about your app
4. Follow along

It works out the rest from your Despia project.

### Install it

**Claude Code** — two commands, and you get updates automatically whenever we improve it.

```
/plugin marketplace add despia-native/despia-deployment-skill
/plugin install despia-launch@despia
```

**Claude apps** — zip the `plugins/despia-launch/skills/despia-launch` folder and upload it under Settings → Capabilities → Skills.

**Any other agent** — one command installs it for Amp, Cline, Codex, Cursor, Antigravity and a dozen more, not just Claude Code.

```bash
npx skills add despia-native/despia-deployment-skill
```

**SkillUse** — this repository is itself a SkillUse registry.

```bash
npm install -g skilluse
skilluse repo add despia-native/despia-deployment-skill
skilluse install despia-launch
```

**Copy it in by hand** — if you would rather not install a plugin.

```bash
git clone https://github.com/despia-native/despia-deployment-skill.git
mkdir -p ~/.claude/skills
cp -r despia-deployment-skill/plugins/despia-launch/skills/despia-launch ~/.claude/skills/
```

Use `.claude/skills/` inside a project instead of `~/.claude/skills/` if you only want it for that project.

**Anything else that reads agent skills** — point it at `SKILL.md`. This follows the [Agent Skills](https://agentskills.io) open standard, and the reference files load themselves as they are needed, so there is nothing else to configure.

To check it took, ask your agent *"what skills do you have?"* — `despia-launch` should be in the list.

## What's inside

`SKILL.md` plus 18 reference files covering intake, the Apple Developer Portal, App Store Connect, Google Play, the Despia handoff, OneSignal, RevenueCat, store metadata and ASO, screenshots, assets and legal pages, privacy declarations, submission, reviewer simulation, rejection fixes, post-launch operations, guided mode for when the agent cannot click, a full verification audit, and troubleshooting for the failures that actually happen.

Every gotcha in there was learned the expensive way by someone else, so you do not have to.

## And if you get stuck, a human helps you. Free.

You are not on your own with an AI and a prayer. Despia users get real human developer support at no extra cost.

**humans@despia.com**

Actual developers, not a ticket queue. Send them the problem, the error, or the rejection notice and they will help you through it. That is included with Despia, not an upsell tier.

So the worst case here is not "stuck forever". It is "email a human and carry on".

## Help

- Free human developer email support: [humans@despia.com](mailto:humans@despia.com)
- Docs at setup.despia.com

## License

MIT. See [LICENSE](LICENSE). Use it, fork it, adapt it for your own stack.
