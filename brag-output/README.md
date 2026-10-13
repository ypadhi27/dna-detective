# DNA Detective research film

A 24-second, 1920 × 1080 film created with Brag and HyperFrames. It shows the actual simulated S06 verdict and the project's detection-rate figure. No real sequencing results are depicted.

- `brag.mp4`: full video with original ambient score.
- `brag.jpg`: selected poster frame, also baked into frame zero.
- `brag.gif`: compact animated preview for GitHub.
- `composition/`: editable, deterministic HyperFrames source and local assets.
- `share-copy.txt`: accompanying caption.

To render from the checked-in composition:

```bash
cd composition
npm run check
npm run render -- --quality delivery --output ../brag.mp4
```

Fonts and sound-effect credits are in `composition/assets/ATTRIBUTION.md`. The music was synthesized specifically for this film, with its generator included. No voiceover is used.
