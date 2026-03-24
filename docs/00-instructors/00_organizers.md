# Organizer Guide

This document is for the people handling the **logistics** of running a napari
workshop: ticketing, communications, Zoom setup, and day-of coordination.
For the teaching side (how to present, troubleshoot, and pace), see
[01_instructors.md](01_instructors.md).

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
- Create a HackMD shared-notes document for each session (see [HackMD Template](#hackmd-shared-notes-template))
- Set up the [Zulip workshop stream](#zulip-stream-setup)

### 2 weeks before

- Confirm instructor team and helper roles; communicate expectations
- Send the [pre-workshop email](#pre-workshop-email-template) to registered participants via `ti.to`
- Set up Zoom meeting (see [Zoom Setup](#zoom-setup)):
  - Enable breakout rooms
  - Enable captions / live transcription
  - Set co-hosts (all instructors and helpers)
  - Record locally if participants consent?
- Confirm the HackMD link is shareable and populated with the template

### 1 week before

- Send a reminder email to participants with:
  - Zoom link (do not post publicly)
  - Gentle, reminder to install the bundle *before* the workshop
  - HackMD link
- Test screen sharing + Qt scaling on the presenter machine
- Run a full tech rehearsal with at least one instructor
- Create the pre-workshop survey

### Day of

- Open Zoom **15 minutes early**; admit helpers and instructors first
- Share the HackMD link in Zoom chat as soon as participants start joining
- Confirm screen sharing is working and Qt scaling is set (see [scaling guide](01_instructors.md#scaling-the-napari-ui-for-teaching))
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
  - HackMD link for each session
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


> **Subject:** [napari workshop] See you [DATE] — setup instructions inside
>
> Hi [NAME],
>
> We're looking forward to seeing you at the **Introduction to napari workshop**
> on **[DATE]** at **[TIME]**
> ([convert to your timezone](https://www.timeanddate.com/worldclock/converter.html)).
>
> **Before the workshop:**
>
> This workshop will be run on the recently released napari 0.7.0 bundled application.
> We encourage you to install the napari bundled app before we start — installation can
> take a few minutes and troubleshooting can be challenging to do live during the
> session.  Follow the
> [installation instructions](https://napari.org/dev/getting_started/installation.html#installation-bundle-conda)
> for your operating system.
> If you are working on an institutional device,
> please follow your institution's software guidelines,
> and reach out to your IT department if you need help.
> 
> Once napari opens and you see an empty viewer, you're all set.
>
> **On the day:**
>
> - Zoom link: [ZOOM_LINK] *(keep this private — do not share publicly)*
> - Shared notes for the session: [ETHERPAD_LINK]
>
> **What to expect:**
>
> - This is a **GUI-only** workshop — no Python or coding knowledge required.
> - We'll work through napari together on-screen, so have napari open and
>   ready on your computer.
> - There will be short breaks and time for your own exploration.
>
> **Questions before the workshop?**
> Post in the [napari Zulip chat](https://napari.zulipchat.com) or reply to
> this email.
>
> **Code of Conduct:** All participants are expected to follow the
> [napari Code of Conduct](https://napari.org/stable/community/code_of_conduct.html).
>
> See you soon!
> [INSTRUCTOR_NAME] and the napari team


(hackmd-shared-notes-template)=
## HackMD Shared-Notes Template

See the Carpentries
[Etherpads guide](https://docs.carpentries.org/resources/communications/etherpads.html)
for general shared-notes best practices. Shared notes serve as:

- A live Q&A space (participants post questions; helpers answer in-doc)
- An accessibility aid (participants who mishear or miss something can catch up)
- A record of key links shared during the session

Create one HackMD document per session. Suggested structure:

```markdown
# Introduction to napari — [DATE]

**Instructors:** [NAMES]
**Zoom link:** [ZOOM_LINK] (do not post publicly)
**Workshop materials:** https://napari.org/workshops/


## Icebreaker

What field are you from, and what kind of images do you work with?
Add your answer below:

- 


## Key Links

- Setup instructions: https://napari.org/workshops/01-intro-napari/00_setup.html
- napari docs: https://napari.org/stable/
- napari hub (plugins): https://napari-hub.org
- Zulip community chat: https://napari.zulipchat.com
- napari gallery: https://napari.org/stable/gallery

## Questions & Answers

Post questions here — helpers will answer during breaks or as they come up.

### Block 1



### Block 2



### Block 3



### Block 4



## Feedback (end of session)

What went well?

- 

What could be improved?

- 

What are you most excited to try after today?

- 
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

> 🔬 Registration is open for our pilot **Introduction to napari Workshop**!
>
> napari is a powerful open-source, multi-dimensional image viewer for
> scientific data analysis in Python. This hands-on, GUI-only workshop is
> designed for biologists, imaging specialists, and data scientists — no
> Python or napari experience required.
>
> **What you'll learn:**  
> → Loading and exploring multi-dimensional datasets  
> → Customizing visualizations for your research  
> → Discovering and using community plugins  
>
> ✅ **$20 USD pilot price** | 🪑 Limited to 20 participants | 🌐 Virtual
>
> 📅 **[DATE 1]** — [TIME + TZ] | Register: LINK_1  
> 📅 **[DATE 2]** — [TIME + TZ] | Register: LINK_2
>
> \#napari \#Python \#ImageAnalysis \#BioImaging \#OpenSource

### Bluesky / Mastodon (thread)

> **1/3** Registration is open for a pilot Introduction to napari Workshop!
> napari is open-source image viewer for scientific data analysis. Hands-on,
> GUI-only — no Python required.
> \#napari \#Python \#ImageAnalysis \#OpenSource
>
> **2/3** ✅ $20 USD pilot | 20 seats | virtual
> 📅 [DATE 1] — [TIME] | [LINK_1]
> 📅 [DATE 2] — [TIME] | [LINK_2]
>
> **3/3** These are pilot workshops — you'll be among the first to use the
> new materials. More workshops to follow! Feedback welcome.

### Zulip / image.sc

> **Introduction to napari workshop — registration open!**
>
> We're running two pilot virtual workshops for anyone who wants to get
> started with napari's GUI. No Python required.
>
> - [DATE 1], [TIME + TZ] — Register: LINK_1
> - [DATE 2], [TIME + TZ] — Register: LINK_2
>
> Cost: $20 USD | 20 seats per session | bundled app install
>
> Questions? Reply here or drop into #workshops (add stream link).
