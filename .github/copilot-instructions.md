# Chat Instructions

- The user is working on this game with their son.
- Provide instructions and code step-by-step.
- The goal is for both the user and their son to learn about coding and making video games.
- Explain concepts clearly and avoid doing too much at once.

---

# Game Overview

**Title:** Dreamiverse
**Genre:** 2D side-scrolling adventure
**Engine:** Python + pygame
**Goal:** Defeat the Nightmare King once and for all
**Setting:** The Dreamiverse — the dream connections between every mind in the universe
**Main character:** The Dreamiverse Warrior
**Controls (planned):** left, right, jump, melee attack, ranged attack, shield, start, settings

---

# Current Status (May 2026)

## What is working
- 900×600 window with a sky-blue background
- Floor/ground image rendered at bottom of screen
- Player sprite (48×80 px) spawns centred above the floor
- Left/right movement with screen boundary clamping
- Jump with gravity and ground collision
- F11 toggles fullscreen; ESC quits
- 3-frame run animation cycling when moving (left/right auto-flipped)
- Jump pose (run_frame_3) shown while airborne
- Idle pose (run_frame_1) shown when standing still
- One enemy that patrols between two boundaries
- Enemy changes image based on distance to player (look vs attack pose)
- Player loses a heart on collision with enemy and respawns at centre
- 3-heart health display (red circles, top-left)
- Game Over screen with R to restart / Q to quit
- Git repo at https://github.com/dusanpolovina/dreamiverse.git

## Known issues / things to fix
- `player_health` variable is declared twice at the top of the file (duplicate lines)
- `jump_speed = -22.5` — using a float for velocity; works but integer would be cleaner
- The fullscreen toggle code (F11 / ESC) was written but the screen is currently set to fixed 900×600 (fullscreen lines are commented out) — needs decision on which to use
- No scrolling background — world is a single static screen
- Enemy collision resets the player position but does not play a hit animation or provide brief invincibility
- No attack mechanic for the player yet (melee/ranged/shield all unimplemented)
- Animation frames (run_frame_1/2/3) were cropped from a Piskel sprite sheet — may need art polish

---

# Todo / Roadmap

## Short term
- [ ] Remove duplicate `player_health` declaration
- [ ] Add a player attack (melee) — key: Z or left Ctrl
- [ ] Add a brief invincibility period after taking a hit (flashing sprite)
- [ ] Draw a dedicated jump sprite frame in Piskel and wire it in

## Medium term
- [ ] Scrolling background / camera that follows the player
- [ ] Multiple enemies with different patrol ranges
- [ ] Enemy health and death animation
- [ ] Ranged attack (throw a projectile)
- [ ] Shield / block mechanic

## Longer term
- [ ] Level 2 with a new background/tileset
- [ ] Boss fight — the Nightmare King
- [ ] Sound effects and background music
- [ ] Start screen / main menu
- [ ] Settings screen (volume, controls)
- [ ] Save/load progress

