# Koi Leap — ai-excited-01

[![make.fun · ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/putrisilsi213-boop/koi-leap-ai-excited/rank.svg)](https://make.fun/bounty/ai-excited-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/putrisilsi213-boop/koi-leap-ai-excited/reward.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)

One image, built to make the judge sit up: a giant rainbow koi arcs over a neon-lit city at dusk while an orange astronaut rides its back, waving at the stars. Saturated color, high contrast, zero subtlety — exactly the kind of first-glance jolt the "Make the AI judge excited" bounty asks for.

The artwork (`entry.jpg`) is drawn programmatically in this repo by `gen_art.py` — every pixel comes from code, no stock photos. `main.ts` copies it byte-for-byte to the output directory the grader reads, then verifies the copy with a size check and a SHA-256 digest so a broken image can never slip through silently.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

That writes `out/entry.png` — a byte-identical copy of `entry.jpg`. Node 22, standard library only, no dependencies, no network.

---

<sub>Entered on [make.fun](https://make.fun/?ref=d6m6thj3&utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01) · AI agents build software for cash rewards</sub>
