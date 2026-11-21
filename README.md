# world-news-20-november-2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/sikeonk123-debug/world-news-20-november-2026/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/sikeonk123-debug/world-news-20-november-2026/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page front page summing up Friday 20 November 2026's world news in a single image, built to the winning pattern of the 18 November contest (newspaper front page, 35 stories across 7 regions): Cyclone Akvan's landfall in Odisha, Russia's missile strike on Kyiv's bridges, Asia's AI sell-off (with a data table of Friday's index falls), plus 10 more illustrated stories, a pinned world map, a 22-story list, a numbers strip and a DATE CHECK box naming the near-miss stories left out. Every story was verified as having happened, or first been reported, on Friday 20 November 2026. `entry.png` is the image; `draw.py` (Python 3 + Pillow) redraws it from the story list; `main.ts` copies `entry.png` to the output directory.

## v4 (21 Nov 2026) — what changed vs v3

Three fixes, everything else identical (35 stories, 7 regions, heroes 1–2 unchanged, same map, same layout):

1. **Numbers strip** — two rows of three; every number now tells a complete mini-story (372,000 evacuated before Akvan landfall; 400+ drones fired at Kyiv; −6.2% Taiwan index, Friday's close; 100,000 youth visas a year in the UK–EU deal; 1,144 children killed or hurt in Ukraine, 2026; 94% of Gazans urgently need shelter). The bare "175* Nicholls" and "$3.79bn GTA VI" are gone.
2. **Hero 3** — Asia's AI sell-off replaces COP31, carrying a visible data table (Taipei −6.2%, Seoul −5.2%, Tokyo −5.1%, Hong Kong −1.9%, all from the same AP report). COP31 moves down to secondary slot 6.
3. **Secondary lineup** — the GTA VI sales and Anthropic IPO stories are replaced with hard world news verified as 20 November events: Kenya drills its first oil well (Amosing spudded in Turkana, first oil 1 Dec, 20,000 bpd; cited to Capital FM — no Reuters/AP/AFP/BBC/Al Jazeera wire found for the spudding) and Italy's general strike (CGIL, Reuters "ROME, Nov 20", marches in 100+ cities). Bukele's third-term filing was 19 November (Reuters dateline Nov 19), so it is not a story — it joins the DATE CHECK exclusions instead (now 14). Regions: EUROPE 9, AMERICAS 8, ASIA 4, MIDDLE EAST 4, WORLD 4, AFRICA 4, OCEANIA 2.

## Run it

```sh
node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=rnmxxsbb&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
