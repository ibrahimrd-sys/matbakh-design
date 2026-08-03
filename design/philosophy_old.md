# Design philosophy

> **PLACEHOLDER.** Replace this file with your existing
> `matbakh_design_philosophy.md`. The manifest already links to it, so once you
> drop it in at this path nothing else needs changing.

It records the settled decisions and the open questions. Keep it next to the
prototypes rather than in a document store — a reviewer who disagrees with a
screen should be one click from the reasoning behind it.

---

## Settled: no music-app integration

**Decided 30 July 2026. Not revisiting without new evidence.**

Matbakh does not integrate with Spotify or any other music service. Cooks who
want music open their own app; the home button is four seconds away.

Why, on the record:

- **Streaming playback would exclude most of the audience.** Spotify's Web
  Playback SDK and every playback endpoint require full Premium — and
  mobile-only tiers like Lite and Premium Mini are excluded, which is exactly
  what most Egyptian subscribers hold. The API reports those plans as
  `"product": "premium"` anyway, so the failure cannot even be detected cleanly
  before it happens.
- **It fights the counter-top posture.** Mobile browsers block transferred
  playback as autoplay; recovery needs a deliberate tap. Every failure mode
  lands on a cook with wet hands.
- **Downloaded playlists are not an alternative.** Spotify's offline cache is
  encrypted DRM. Reading it is defeated technically and prohibited by the terms.
- **Terms risk.** Spotify's platform terms bar commercial streaming
  integrations. Matbakh is a commercial product.
- **It moves no number that matters.** The launch gate is commerce attach rate.
  Music does not touch it.

**What this leaves open, and is worth doing:** the timer alarm has to be audible
over music already playing on the same speaker. A web page cannot duck another
app's volume, so the alarm must cut through on its own — a sound-design problem,
not an integration one. A missed 40-minute stock is a ruined dish, and that is
true today with no integration at all.

If music returns, the only shape worth considering is licensed instrumental
audio Matbakh owns outright — offline, duckable, no third party — and that is a
Ramadan sponsorship asset, not a launch feature.
