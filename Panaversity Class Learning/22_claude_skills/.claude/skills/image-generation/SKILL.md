---
name: image-generator
description: Use this skill to generate images using gemini.google.com for the given prompt
---

# Workflow: Browser-Based Image generation using playwright MCP

**CRITICAL: Use gemini.google.com ONLY (NOT google AI Studio, NOT other image generators)**

**Initialize once:**
1. Navigate to https://gemini.google.com/app (PlayWright MCP)
2. User signs in if needed (session persists)
3. Select "Create Image" tool (Nano Banan Pro)

**For EACH visual:**
1. **Type creative brief** directly into gemini chat textbox *use condensed format in batch mode - see Token Conservation below
2. **Press Enter** to submit.
3. **Wait 30-35 seconds** for generation
4. **Click "Download full size Image"** (6 gates below)
5. **Wait 3-5 seconds** for download completion
6. Inform user when the work is done.

**Principle:** New chat per visual prevents cross-contamination; immediate verification catches issues early; immediate embedding prevents orphans