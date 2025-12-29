# Benchmark Distribution Chart (PPT Asset)

This repo contains a **tech-style benchmark distribution** graphic generated from the benchmark list in the provided image.

## Output files

- `assets/benchmark_distribution.svg` (recommended for PPT: vector, crisp at any size)
- `assets/benchmark_distribution.png` (preview raster, 3840×2160)

## Regenerate

```bash
python3 scripts/generate_benchmark_distribution_svg.py
rsvg-convert -w 3840 -h 2160 -o assets/benchmark_distribution.png assets/benchmark_distribution.svg
```
