# Organizer Guide

This document is for the people handling the **logistics** of running a napari
workshop: ticketing, communications, Zoom setup, and day-of coordination.
For the teaching side (how to present, troubleshoot, and pace), see
[01_instructors.md](instructors.md).

## Pre-Workshop Checklists

Adapted from the
[Carpentries workshop checklists](https://docs.carpentries.org/resources/workshops/checklists.html).

### >2 weeks before

- Confirm workshop dates, times, and timezone coverage with the instructor team
- Set up ticketing on `ti.to`:
  - Title, date, description, logo, color scheme
  - Ticket price: **$20 USD** (pilot rate); NumFOCUS adds a ~5.1% fee (covers Stripe + `ti.to`)
  - Seat cap: **20 per session** with a waitlist enabled
  - No discount codes for pilots; add them for future workshops
  - Enable attendee questions if you want dietary/accessibility info
- Publish on socials (see [Social Media Templates](#social-media-templates)):
  - [napari Zulip](https://napari.zulipchat.com) `#events` and `#general`
  - [image.sc forum](https://forum.image.sc/) under `napari` tag
  - LinkedIn, Bluesky, Mastodon
- Plan a **second wave** of social posts ~1 week before each session
- Add both sessions to the napari community calendar and the image.sc forum events page
- Set up pre-workshop Zulip topics for the session (see [Zulip Stream Setup](#zulip-stream-setup))
- Set up the [Zulip workshop stream](#zulip-stream-setup)

### 2 weeks before

- Confirm instructor team and helper roles; communicate expectations
- Send the [pre-workshop email](#pre-workshop-email-template) to registered participants via `ti.to`
- Set up Zoom meeting (see [Zoom Setup](#zoom-setup)):
  - Enable breakout rooms
  - Enable captions / live transcription
  - Set co-hosts (all instructors and helpers)
  - Record locally if participants consent?


### 1 week before

- Create the pre-workshop survey
- Confirm the Zulip workshop stream is set up and topics are pre-populated
- Send a reminder email to participants with:
  - Zoom link (do not post publicly)
  - Gentle, reminder to install the bundle *before* the workshop
  - Zulip workshop stream link
  - Pre-workshop survey
- Test screen sharing + Qt scaling on the presenter machine
- Run a full tech rehearsal with at least one instructor



### Day of

- Open Zoom **15 minutes early**; admit helpers and instructors first
- Share the Zulip workshop stream link in Zoom chat as soon as participants start joining
- Confirm screen sharing is working and Qt scaling is set (see [scaling guide](instructors.md#scaling-the-napari-ui-for-teaching))
- Set up breakout rooms in advance (pre-assign or let Zoom auto-assign)

### After the workshop

- Send the post-workshop survey to participants (see below)
- Hold a brief instructor debrief (15–30 min): what worked, what to fix
- Collect and summarise survey results and share with the team
- Post a follow-up in the Zulip workshop stream with resources mentioned
  during the session; keep the stream open for follow-up questions
- Publish a brief retrospective summary
- Close the `ti.to` listing once the waitlist is no longer useful

(zoom-setup)=
## Zoom Setup

See the Carpentries
[online workshop resources](https://docs.carpentries.org/resources/workshops/resources_for_online_workshops.html)
for detailed Zoom guidance. Key settings for napari workshops:

| Setting | Recommended value |
|---|---|
| Waiting room | Enabled; admit participants once instructors are ready |
| Breakout rooms | Enabled; pre-assign or auto-assign by session |
| Live captions | Enabled (Zoom AI Companion) |
| Recording | Local recording with participant consent; do not auto-record to cloud |
| Co-hosts | All instructors and helpers -- must be done inside Zoom meeting because of numFOCUS license |
| Chat | Save chat automatically; share log with participants after |
| Screen sharing | Host and co-hosts only (prevent accidental shares) to start |

**Breakout room tips:**
- Create rooms *before* the session starts in the Zoom web portal for faster
  assignment on the day.
- Set a timer so rooms close automatically; helpers return to main.

(zulip-stream-setup)=
## Zulip Stream Setup

A dedicated Zulip stream gives participants a place to ask questions before,
during, and after the workshop.

- Create a thread in  `#workshops`
- Pin a welcome message with:
  - Workshop schedule and Zoom links (for participants)
  - Bundle download link
  - Code of Conduct link
  - Workshop materials link
- Create pre-set topics for participants to use during the session:
  - **Welcome & introductions** — participants post their name, field, and type of images they work with
  - **Installation issues** — for troubleshooting before and during the workshop
  - **Screenshots** — participants post screenshots from breakout exercises
  - **Block 1 Q&A**, **Block 2 Q&A**, **Block 3 Q&A**, **Block 4 Q&A** — per-block question threads
- Include the Zulip stream invite link in the pre-workshop email and Zoom
  chat on the day.
- After the workshop, announce the stream in `#general` so the broader
  community can benefit from the Q&A.

## Ticketing (`ti.to`)

These workshops run through [NumFOCUS](https://numfocus.org/) on
`ti.to`. Key decisions documented during the 2026 pilot planning:

- **Price:** $20 USD per participant for the pilot; revisit for future workshops
  (pay-what-you-can, regional pricing, and discount codes are all supported by
  `ti.to` once we have sponsor partnerships)
- **NumFOCUS fee:** ~5.1% covers Stripe and `ti.to` fees; can be built into
  ticket price or shown separately
- **Seat cap:** 20 per session; enable the waitlist
- **Event duplication:** `ti.to` supports duplicating events — use this when
  scheduling future cohorts
- **Attendee messaging:** `ti.to` supports markdown email to all registrants —
  use this for the pre-workshop email and reminder

(pre-workshop-email-template)=
## Pre-Workshop Email Template

Send via `ti.to` **one week before** the workshop and again **the day before**.
Adapt the bracketed fields.

```markdown
**Subject:** [napari workshop] See you [DATE] — setup instructions inside

Hi {{first_name}},

We're looking forward to seeing you at the {{event_title}}
on **[DATE]** at **[TIME]**
([convert to your timezone] (TIME_AND_DATE_WORK_CLOCK)).

**Before the workshop:**

Fill out the [pre-workshop survey] (SURVEY_LINK) to help us tailor the session to your needs.
After the workshop, we'll share a follow-up survey to get your feedback, so that we can improve future sessions.

This workshop will be run on the recently released napari 0.7.0 bundled application.
We encourage you to install the napari bundled app before we start — installation can
take a few minutes and troubleshooting can be challenging to do live during the
session.  Follow the
[installation instructions](https://napari.org/workshops/intro-napari/setup/)
for your operating system.
If you are working on an institutional device,
please follow your institution's software guidelines,
and reach out to your IT department if you need help.

Once napari opens and you see an empty viewer, you're all set. You can preview the workshop at https://napari.org/workshops/intro-napari/

**Day of the workshop:**

Zoom link: [ZOOM_LINK]
*(keep this private — do not share publicly)*

**What to expect:**

- This is a **GUI-only** workshop — no Python or coding knowledge required.
- We'll work through napari together on-screen, so have napari open and
  ready on your computer.
- There will be short breaks and time for your own exploration.

**Questions before the workshop?**
Post in the [napari Zulip chat] (ZULIP_WORKSHOP_LINK) or reply to
this email.

**Code of Conduct:** All participants are expected to follow the
[napari Code of Conduct](https://napari.org/stable/community/code_of_conduct.html).

See you soon!
[INSTRUCTOR_NAME] and the napari team
```

(zulip-workshop-topics-template)=
## Zulip Workshop Topics Template

Set these topics up in a new **#napari-workshop-[DATE]** Zulip stream before each session.
Post a pinned welcome message in each topic so participants know what it's for.

| Topic | Purpose |
|---|---|
| `Welcome & introductions` | Icebreaker: name, field, type of images |
| `Installation Questions and Troubleshooting` | Pre-workshop and day-of install help |
| `Resources & links` | Links shared during the session; stays open after |
| `Screenshots` | Participants post screenshots from breakout exercises |
| `Block 1 Q&A` | Questions during Welcome & First Images |
| `Block 2 Q&A` | Questions during Exploring the napari GUI |
| `Block 3 Q&A` | Questions during Plugins and Annotation |
| `Block 4 Q&A` | Questions during Interactive Analysis |


**Suggested welcome message for the Screenshots topic:**

```markdown
Hi everyone! Use this topic to post screenshots from today's breakout
exercises. To take a screenshot in napari, press **Alt+C** to copy the
canvas or **Shift+Alt+C** to copy the canvas with the viewer UI,
then paste here with Ctrl+V (or Cmd+V on macOS).

We'd love to see what you find! Add a quick note about what you're looking at.
```

## Post-Workshop Survey

Send a short survey within 24 hours of the workshop. Suggested questions:

1. How would you rate the workshop overall? (1–5)
2. What was the most useful thing you learned?
3. What was unclear or confusing?
4. Did you experience any technical problems? If so, what?
5. How did you hear about this workshop?
6. Would you recommend this workshop to a colleague? (Yes / No / Maybe)
7. Is there anything related to accessibility or inclusion that we should
   improve?

Google Forms or a NumFOCUS-approved survey tool works well. Share the link in
the final 10 minutes of the session and in the post-workshop email.

(social-media-templates)=
## Social Media Templates

Extracted and adapted from workshop planning notes. Tailor dates and links
before posting.

### LinkedIn

```markdown
🔬 Registration is open for our pilot **Introduction to napari Workshop**!

napari is a powerful open-source, multi-dimensional image viewer for
scientific data analysis in Python. This hands-on, GUI-only workshop is
designed for biologists, imaging specialists, and data scientists — no
Python or napari experience required.

**What you'll learn:**  
→ Loading and exploring multi-dimensional datasets  
→ Customizing visualizations for your research  
→ Discovering and using community plugins  

✅ **$20 USD pilot price** | 🪑 Limited to 20 participants | 🌐 Virtual

📅 **[DATE 1]** — [TIME + TZ] | Register: LINK_1  
📅 **[DATE 2]** — [TIME + TZ] | Register: LINK_2

\#napari \#Python \#ImageAnalysis \#BioImaging \#OpenSource
```

### Bluesky / Mastodon (thread)

```markdown
**1/3** Registration is open for a pilot Introduction to napari Workshop!
napari is open-source image viewer for scientific data analysis. Hands-on,
GUI-only — no Python required.
\#napari \#Python \#ImageAnalysis \#OpenSource

**2/3** ✅ $20 USD pilot | 20 seats | virtual
📅 [DATE 1] — [TIME] | [LINK_1]
📅 [DATE 2] — [TIME] | [LINK_2]

**3/3** These are pilot workshops — you'll be among the first to use the
new materials. More workshops to follow! Feedback welcome.
```

### Zulip / image.sc

```markdown
**Introduction to napari workshop — registration open!**

We're running two pilot virtual workshops for anyone who wants to get
started with napari's GUI. No Python required.

- [DATE 1], [TIME + TZ] — Register: LINK_1
- [DATE 2], [TIME + TZ] — Register: LINK_2

Cost: $20 USD | 20 seats per session | bundled app install

Questions? Reply here or drop into #workshops (add stream link).
```
