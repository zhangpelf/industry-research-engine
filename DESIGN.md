---
name: 行业研究报告生成器
description: AI-powered industry research report generator
colors:
  primary: "#6366f1"
  primary-hover: "#4f46e5"
  primary-active: "#4338ca"
  primary-soft: "#eeeffd"
  neutral-bg: "#f8f9fc"
  neutral-surface: "#ffffff"
  neutral-border: "#e2e4f0"
  neutral-muted: "#6b6d8a"
  neutral-text: "#1a1a2e"
  success: "#10b981"
  warning: "#f59e0b"
  error: "#ef4444"
  badge-bg: "#eef2ff"
  badge-text: "#4f46e5"
  tracking-progress: "#6366f1"
  tracking-track: "#e2e4f0"
typography:
  display:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "clamp(2rem, 4vw, 3.25rem)"
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "1.125rem"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "normal"
  body:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  label:
    fontFamily: "Inter, system-ui, -apple-system, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: "normal"
  mono:
    fontFamily: "JetBrains Mono, Menlo, monospace"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  sm: "8px"
  md: "12px"
  lg: "16px"
  pill: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "0.75rem 2rem"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
  input-default:
    backgroundColor: "{colors.neutral-surface}"
    textColor: "{colors.neutral-text}"
    rounded: "{rounded.md}"
    padding: "0.75rem 1.25rem"
  input-focus:
    backgroundColor: "{colors.neutral-surface}"
    textColor: "{colors.neutral-text}"
    rounded: "{rounded.md}"
  sidebar:
    backgroundColor: "{colors.neutral-surface}"
  tab-default:
    textColor: "{colors.neutral-muted}"
  tab-selected:
    textColor: "{colors.primary}"
---

# Design System: 行业研究报告生成器

## 1. Overview

**Creative North Star: "The Dispatch"**

A research tool that reads like a tech publication — crisp, editorial, with the energy of a newsroom rather than the silence of a dashboard. The design bridges professional credibility (trustworthy numbers, clear hierarchy) with the vibrant readability of modern tech media (36Kr, PingWest, The Verge). Every element is in service of the core loop: type an industry → see results. No decoration that doesn't earn its place.

The system explicitly rejects three adjacent aesthetics: the generic SaaS dashboard (gray cards, metric tiles, thin borders), the old-school financial terminal (dark navy, gold accents, dense grids), and the "AI tool" cliché (gradient text, glassmorphism, numbered section markers). It lands in the space between — clean like Linear, editorial like Stratechery, purposeful like a terminal but without the bloat.

**Key Characteristics:**
- **Content-forward.** Search and reading are the primary tasks.
- **Low friction.** The shortest path from input to output, surfaced in the UI.
- **One accent, restrained.** Indigo-purple appears on ≤10% of the surface. Its rarity is the point.
- **Flat layout with intentional depth.** Shadows only appear on interactive elements in hover state.
- **Single type family.** Inter carries everything — no second font, no display face for headings.

### Named Rules

**The One Accent Rule.** Primary indigo-purple (#6366f1) is reserved for interactive states, active selection, and the primary action. Never decorative. Never on backgrounds.

**The No-Dashboard Rule.** Metric tiles, big-number hero sections, and sticky sidebar menus are forbidden. This is a search-and-read tool, not a monitoring console.

## 2. Colors

A cool-leaning neutral palette anchored by a single indigo-purple accent. The neutrals drift slightly toward purple-cast gray rather than warm beige or pure slate, so the accent feels native rather than bolted on.

### Primary

- **Signal Indigo** (#6366f1, oklch(58% 0.22 285)): Primary buttons, active tab indicators, focus rings, selected state. The only saturated color on screen.
- **Deep Indigo** (#4f46e5, oklch(50% 0.2 285)): Button hover.
- **Night Indigo** (#4338ca, oklch(43% 0.19 285)): Button active/pressed.
- **Indigo Haze** (#eeeffd, oklch(94% 0.02 285)): Subtle background tint for selected items, badge backgrounds.

### Neutral

- **Cool Canvas** (#f8f9fc, oklch(97.5% 0.004 270)): Page background. Slightly cooler than pure white, low chroma toward indigo.
- **White Surface** (#ffffff): Cards, sidebar, input fields, elevated containers.
- **Silver Thread** (#e2e4f0, oklch(90% 0.008 280)): Borders, dividers, input strokes at rest.
- **Slate Muted** (#6b6d8a, oklch(55% 0.02 280)): Secondary text, placeholder text, tab labels (unselected).
- **Deep Charcoal** (#1a1a2e, oklch(16% 0.02 280)): Primary text, headings. High contrast against backgrounds.

### Semantic

- **Evergreen** (#10b981): Success states, completion indicators.
- **Amber** (#f59e0b): Warnings, attention calls.
- **Coral** (#ef4444): Errors, destructive actions.

### Named Rules

**The One Voice Rule.** The primary accent is used on ≤10% of any given screen. Its rarity is the point. If a screen has more than three indigo-purple elements, two of them should be removed or demoted to neutral.

**The Cool Baseline Rule.** Neutrals drift cool (toward 270–285° hue, chroma < 0.02). Never warm. A warm neutral on this canvas reads as a bug.

## 3. Typography

**Display & Body Font:** Inter (system-ui, -apple-system, sans-serif fallback)

**Character:** Single-weight sans-serif throughout. Inter's tall x-height and open apertures keep dense research text readable at body sizes while its crispness at display weights gives headings editorial energy. No second font needed — product register operates on earned familiarity, not typographic contrast.

### Hierarchy

- **Display** (800, clamp(2rem, 4vw, 3.25rem), 1.15): Page title only. Used once per view, on the main header.
- **Headline** (700, 1.5rem, 1.3): Section headings within reports, modal titles.
- **Title** (600, 1.125rem, 1.4): Subsection headings, sidebar group titles.
- **Body** (400, 1rem, 1.6): Primary reading text. Max line length 70ch.
- **Label** (500, 0.875rem, 1.4): Button text, tab labels, metadata, field labels.
- **Mono** (400, 0.875rem): Code blocks, technical data snippets in reports.

### Named Rules

**The Body First Rule.** Body text at 1rem/400 is the design's anchor. Everything else sizes relative to it. If a heading looks too large, reduce it — display should never exceed 3.25rem on this surface.

## 4. Elevation

Flat surfaces with subtle lift for interactive states. The system uses tonal layering (light neutral background → white surface for containers) rather than drop shadows to create depth at rest. Shadows appear only as a response to interaction.

### The Flat-by-Default Rule

Surfaces are flat at rest. A card on Cool Canvas has no shadow — its white surface against the tinted background provides enough separation. Shadows appear exclusively on hover (buttons, interactive cards) and on floating elements (tab bar). This keeps the interface quiet and scannable.

### Shadow Vocabulary

- **Button Rest** — No shadow. Flat against surface.
- **Button Hover** — `0 4px 12px rgba(99, 102, 241, 0.25), 0 2px 4px rgba(99, 102, 241, 0.1)`: Indigo-tinted shadow to match the accent. Only on primary action.
- **Floating Container** — `0 2px 8px rgba(0, 0, 0, 0.06)`: Tab bar, sticky headers. Minimal, barely perceptible.
- **Modal/Overlay** — `0 16px 48px rgba(0, 0, 0, 0.12)`: Deep shadow only for modals and dialogs.

## 5. Components

### Primary Button

- **Shape:** Gently curved (12px radius, `{rounded.md}`)
- **Rest:** Signal Indigo background, white label (500/0.875rem/1.4), 0.75rem 2rem padding, no shadow
- **Hover:** Deep Indigo background, indigo-tinted shadow lifts 2px, 200ms ease-out
- **Active:** Night Indigo background, no shadow, returns to baseline
- **Disabled:** Slate Muted text on Silver Thread background, no interaction

### Input / Text Field

- **Shape:** Gently curved (12px radius), full-width with internal label
- **Rest:** White background, Silver Thread border (1px), Deep Charcoal text
- **Focus:** Signal Indigo border, 4px Indigo Haze focus ring (`box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15)`), 200ms ease-out
- **Placeholder:** Slate Muted, 4.5:1 contrast minimum
- **Disabled:** Silver Thread background, Slate Muted text

### Sidebar

- **Style:** White panel, right-side border (Silver Thread, 1px), no shadow at rest
- **Header:** Deep Charcoal, Title weight (600, 1.125rem)
- **Form Controls:** Labels in Slate Muted, compact spacing. Select inputs at 8px radius (`{rounded.sm}`)
- **Status Badge:** Indigo Haze background, Deep Indigo text, pill shape (`{rounded.pill}`), 2px 10px padding, 0.8rem
- **Tech Stack Line:** Slate Muted secondary text, no icon

### Tabs

- **Style:** White pill container (16px radius, `{rounded.lg}`), subtle floating shadow
- **Tab Item:** 1rem/600, Slate Muted text, 1rem vertical padding
- **Selected:** Signal Indigo text, 3px indigo underline indicator (3px height, pill ends)
- **Hover:** Transition text color toward indigo, 200ms ease

### Progress Bar

- **Track:** Silver Thread, 8px height, pill shape
- **Fill:** Signal Indigo, pill shape, 300ms ease width transition
- **Status Text:** Slate Muted label, positioned above or beside track

### Alert / Status Boxes

- **Shape:** 12px radius, 1rem 1.25rem padding
- **Style:** White background, no border at rest, `{shadow.floating}` if elevated
- **Icon + text layout:** Leading icon, inline message text
- **Colors match semantic palette:** Green for success, Amber for warning, Coral for error

### Chips / Quick-Select Buttons

- **Shape:** 8px radius (`{rounded.sm}`), compact padding
- **Rest:** Silver Thread border, white background, Deep Charcoal text
- **Hover:** Signal Indigo border, Indigo Haze background tint
- **Active:** Signal Indigo background, white text

## 6. Do's and Don'ts

### Do:

- **Do** keep backgrounds neutral (Cool Canvas) — the indigo accent earns its place by being rare.
- **Do** use `text-wrap: balance` on headings, `text-wrap: pretty` on body paragraphs.
- **Do** cap body text line length at 70ch — research text needs readable line lengths.
- **Do** use the pill shape (`{rounded.pill}`) only for badges and progress bars — everywhere else uses 8–16px.
- **Do** use 150–250ms transitions for state changes — users are in flow, don't make them wait.
- **Do** use skeleton loading states for report content — spinners are reserved for initialization only.
- **Do** ensure body text contrast ≥4.5:1 against its background (Deep Charcoal on Cool Canvas passes at 14:1).

### Don't:

- **Don't** use gradient text (`background-clip: text` gradients) — verbatim from PRODUCT.md's anti-references.
- **Don't** use glassmorphism, blur-backdrops, or frosted-glass effects — they belong nowhere in this system.
- **Don't** use numbered section markers (01 / 02 / 03) as decorative scaffolding above sections.
- **Don't** use side-stripe borders (`border-left` > 1px as colored accent on cards or callouts).
- **Don't** use big-number metric tiles — this is not a dashboard, this is a research tool.
- **Don't** use display fonts or serifs for UI labels, buttons, or data — Inter carries everything.
- **Don't** use dark mode as default — the scene is desktop office during work hours, ambient-lit, light mode fits.
- **Don't** use bounce or elastic easing on animations — use cubic-bezier(0.4, 0, 0.2, 1) or similar ease-out curves.
- **Don't** orchestrate page-load animations — content should appear immediately, not sequence in.
- **Don't** use the primary accent on inactive states — only active/interactive/hover elements get indigo.
- **Don't** use the SaaS grey-card-plus-icon-plus-label template for empty sections — design empty states that teach.
