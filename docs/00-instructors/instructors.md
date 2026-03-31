---
title: Instructor Guide
---

These workshops are inspired by the
[Carpentries](https://carpentries.org) model: live coding, learner-centered
pacing, and a commitment to welcoming everyone
regardless of background. We do not assume prior napari experience for the
introductory workshop, and we invest heavily in setup, so that the first hour
is not lost to installation problems.

Key principles:

- **Accessibility before features.** A learner who can open an image and
  poke around is more valuable than one who saw a polished demo and is
  intimidated.
- **I → We → You.** Every concept is introduced by the instructor (I), then
  worked through together as a group (We), then given as a free-exploration
  exercise (You).
- **Screen real-estate awareness.** Use light mode; increase GUI size. 
  Walk participants through how to replicate the views. 
- **Safety.** Follow the Code of Conduct; normalise questions in
  chat or in the shared document.

(diversity-equity-and-inclusion)=
# Diversity, Equity, and Inclusion

We are committed to building an inclusive environment. The workshop expects participants to follow the napari community
[Code of Conduct](https://napari.org/stable/community/code_of_conduct.html) and
the [Carpentries DEI statement](https://carpentries.org/about-us/#diversity-equity-and-inclusion-statement).

Practical commitments:

- Closed captions and transcription enabled by default in Zoom.
- Zulip workshop stream for participant Q&A and sharing.
- Post-workshop survey explicitly solicits accessibility and inclusion
  feedback.

# Roles

## Lead instructor

- Drives the screen — napari is always visible, not slides
- Narrates every action out loud ("I'm clicking File > Open Sample >
  napari builtins > Cells 3D + 2Ch")
- Watches the Zulip workshop stream and Zoom chatfor questions during exercises
- Advances through the [session schedule](../01-intro-napari/index.md#session-schedule)
  and calls time

## Helper instructor

- Monitor the Zoom chat and Zulip workshop stream throughout
- Join breakout rooms during "You" exercises; one helper per room minimum
- DM participants with technical issues and escalate to breakout as needed
- Signal the lead instructor (via Zoom reaction or private chat) if the group
  is falling behind

## Before the session

- Join the workshop Zulip stream and say hello before the session.
- Read the [Carpentries Instructor Training handbook](https://carpentries.github.io/instructor-training/instructor/index.html)
  — at minimum the sections on motivation, live coding, and managing a diverse
  classroom.
- Read the [napari Code of Conduct](https://napari.org/stable/community/code_of_conduct.html)
  and be prepared to enforce it.
- Familiarise yourself with the DEI statement and commitments (see
  [Diversity, Equity, and Inclusion](#diversity-equity-and-inclusion) above).
- Test the bundle install on your own machine in a clean environment if
  possible.
- Install the napari bundle on your machine and run through the materials at
  least once.
- During practice, set your display scale higher or use an env var scale to `QT_SCALE_FACTOR=1.5`
  see the [presentation instructions](#presentation-instructions) for details.
- Close all applications except napari and a browser tab for the Zulip workshop stream
- Join the Zoom call **10 minutes early** to test screen sharing

# I → We → You in Practice

Every concept follows the same arc:

| Phase | Who drives | What happens |
|---|---|---|
| **I** | Lead instructor | Instructor demos the feature live in napari with narration. Participants watch. |
| **We** | Everyone together | Instructor and participants do the same steps simultaneously. "Now you do it with me." |
| **You** | Participants | Breakout rooms or independent exploration. Curated task is provided. |

**Key rule:** Use napari on-screen, and try not to have the workshop materials document on the shared screen. The
materials are only a reference — show learners the actual interface and your thought process.

# Live Teaching Tips

- **Slow down.** Learners are watching, clicking, and reading simultaneously.
  Pause after every action; ask "is everyone with me?" at natural breakpoints.
- **Narrate.** Say the full menu path aloud: "Plugins menu, then Install /
  Uninstall Plugins." Don't assume learners can see your mouse.
- **Use the command palette in addition to GUI pathways** (`Ctrl+Shift+P` / `Cmd+Shift+P`) 
  for live demos — it is searchable and visible to the whole screen.
- **Tidy the viewer.** Delete layers you no longer need so learners can
  focus. An empty layer list is less intimidating than an accumulation of
  semi-related layers.
- **Mistakes are teaching moments.** Getting something wrong and fixing it live
  is one of the most effective teaching moments — it normalises confusion.
- **No jargon without definition.** Define every term the first time you use
  it; do not assume knowledge of numpy, zarr, OME, etc.

# Online Delivery (Zoom)

See also the Carpentries
[resources for online workshops](https://docs.carpentries.org/resources/workshops/resources_for_online_workshops.html).

- **Do not Disturb Mode.** Close email, notifications, and anything else that
  could pop up over the screen share.
- **Chat:** A helper should own the Zoom chat, summarising or escalating
  questions. The lead instructor should not be reading chat while teaching.
- **Reactions:** Ask learners to use the 👍 Zoom reaction to signal they are
  ready to move on, and ✋ to signal they are stuck.
- **Breakout rooms:** Announce when rooms are opening and closing, and give
  a 2-minute warning before returning to main. State the task clearly (in
  Zoom chat, in the Zulip stream, and verbally) before opening rooms.

(presentation-instructions)=
# Presentation Instructions

## Scaling the napari UI for teaching

For workshops, prefer Qt application scaling over text-only font changes.
This scales the full napari interface, including toolbars, buttons, dialogs,
and other controls.

Recommended launch settings:

- Start with `1.5` on standard laptop/projector setups.
- Try `1.75` or `2` only if the display is still hard to read.
- Add `QT_SCALE_FACTOR_ROUNDING_POLICY=PassThrough` if using Qt5 (<v0.7.0) to avoid excessive rounding up to integer scale factors (PassThrough is the Qt6 default).

Windows PowerShell:

```powershell
$env:QT_SCALE_FACTOR = "1.5"
napari
```

To launch with the bundle, on Windows target the napari launch command `.bat` in the bundle's `Menu` directory:

```powershell
$env:QT_SCALE_FACTOR = "1.5"
& "C:\Users\timmo\AppData\Local\napari-0.7.0\envs\napari-0.7.0\Menu\napari (0.7.0).bat"
```

Unix shells (`bash`, `zsh`):

```bash
export QT_SCALE_FACTOR=1.5
napari
```

Defaults and reset behavior:

- If these variables are unset, Qt falls back to its normal platform DPI
  handling. There is no napari-specific custom default for UI enlargement.
- These commands are not permanent. They affect only the current shell session
  and processes launched from it.
- Opening a new terminal resets them unless the user added them to a shell
  profile or set them as persistent system environment variables.
- To reset them in the current PowerShell session:

```powershell
Remove-Item Env:QT_SCALE_FACTOR -ErrorAction SilentlyContinue
Remove-Item Env:QT_SCALE_FACTOR_ROUNDING_POLICY -ErrorAction SilentlyContinue
```

- To reset them in the current Unix shell session:

```bash
unset QT_SCALE_FACTOR
unset QT_SCALE_FACTOR_ROUNDING_POLICY
```

# Opening Segment (first 10 minutes)

Run through this checklist at the start of every session:

- Welcome everyone and introduce all instructors and helpers by name.
- State the Code of Conduct:

  > *"We expect all participants to be respectful and to follow the
  > [napari Code of Conduct](https://napari.org/stable/community/code_of_conduct.html).
  > If you experience or witness a violation, please DM an instructor or email
  > conduct@napari.org."*

- Read the DEI commitment (brief version):

  > *"This workshop is designed for everyone regardless of background,
  > nationality, or prior experience. We actively work to make it accessible.
  > Please tell us if we can do better."*

- Share the Zulip workshop stream link in chat and ask everyone to post
  an introduction (field and type of images they work with) in the **#workshops** stream.
- Share the Zulip invite link and encourage participants to join the
  napari community.
- Explain Zoom conventions:
  - Mute when not speaking
  - Use chat for questions — a helper will relay or answer
  - Use reactions (👍 ready to move on; ✋ stuck or need help)
  - Video on if comfortable, off if not
- Ask if anyone has accessibility needs we should accommodate (private DM is
  fine).
- State the rough schedule and when the breaks will be.

# Closing Segment (last 20–30 minutes)

- Ask aloud for a debrief: *"What is one thing that was confusing?"*
  and *"What are you most excited to try after today?"*
- Share the post-workshop survey link in chat and in the Zulip workshop stream.
- Point to key community resources:
  - [napari.org](https://napari.org/stable/) — documentation and gallery
  - [napari-hub.org](https://napari-hub.org) — plugin discovery
  - [Zulip](https://napari.zulipchat.com) — community chat
  - [image.sc](https://forum.image.sc/) — image analysis forum
- Invite participants to join the napari community — contributions are
  welcome at all levels (docs, testing, plugins, core).
- Keep the Zoom meeting open for 10 minutes after the official end time
  for lingering questions.

# After the Workshop (instructor tasks)

- Submit any bugs or issues discovered during the live session as GitHub
  issues, linking to the relevant lesson file.
- Collect and summarise survey results for the team.
- Post a follow-up message in the Zulip workshop stream with any resources,
  links, or tips mentioned during the session.
