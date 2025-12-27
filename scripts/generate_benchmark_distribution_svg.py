from __future__ import annotations

from pathlib import Path


def main() -> None:
    # Keep source ASCII-only; write UTF-8 output deterministically.
    # We avoid special typographic glyphs that sometimes get mangled in toolchains.
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
  <defs>
    <radialGradient id="bgRadial" cx="40%" cy="30%" r="75%">
      <stop offset="0%" stop-color="#0E1633"/>
      <stop offset="55%" stop-color="#070B14"/>
      <stop offset="100%" stop-color="#05070F"/>
    </radialGradient>

    <linearGradient id="panelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0A1127" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#070B14" stop-opacity="0.88"/>
    </linearGradient>

    <pattern id="grid" width="64" height="64" patternUnits="userSpaceOnUse">
      <path d="M 64 0 L 0 0 0 64" fill="none" stroke="#1A2A5A" stroke-opacity="0.25" stroke-width="1"/>
      <path d="M 64 32 L 0 32" fill="none" stroke="#1A2A5A" stroke-opacity="0.18" stroke-width="1"/>
      <path d="M 32 64 L 32 0" fill="none" stroke="#1A2A5A" stroke-opacity="0.18" stroke-width="1"/>
    </pattern>

    <filter id="glowCyan" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feColorMatrix in="b" type="matrix"
        values="0 0 0 0 0
                0 0 0 0 0.95
                0 0 0 0 1
                0 0 0 0.9 0" result="c"/>
      <feMerge>
        <feMergeNode in="c"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glowMagenta" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feColorMatrix in="b" type="matrix"
        values="1 0 0 0 0.95
                0 0 0 0 0.1
                0 0 0 0 0.9
                0 0 0 0.85 0" result="c"/>
      <feMerge>
        <feMergeNode in="c"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glowPurple" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feColorMatrix in="b" type="matrix"
        values="0.7 0 0 0 0.7
                0 0 0 0 0.35
                0 0 0 0 1
                0 0 0 0.85 0" result="c"/>
      <feMerge>
        <feMergeNode in="c"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glowGreen" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feColorMatrix in="b" type="matrix"
        values="0 0 0 0 0.1
                0 0 0 0 1
                0 0 0 0 0.55
                0 0 0 0.85 0" result="c"/>
      <feMerge>
        <feMergeNode in="c"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glowOrange" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feColorMatrix in="b" type="matrix"
        values="1 0 0 0 1
                0 0 0 0 0.6
                0 0 0 0 0.1
                0 0 0 0.8 0" result="c"/>
      <feMerge>
        <feMergeNode in="c"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="14" stdDeviation="10" flood-color="#000000" flood-opacity="0.55"/>
    </filter>

    <style>
      .t-title { font-family: Inter, "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", system-ui, -apple-system, "Segoe UI", Arial, sans-serif; font-weight: 700; letter-spacing: 0.5px; }
      .t-sub   { font-family: Inter, "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", system-ui, -apple-system, "Segoe UI", Arial, sans-serif; font-weight: 500; letter-spacing: 0.2px; }
      .t-mono  { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
      .chip    { font-family: Inter, "Noto Sans CJK SC", "PingFang SC", "Microsoft YaHei", system-ui, -apple-system, "Segoe UI", Arial, sans-serif; font-weight: 600; }
    </style>
  </defs>

  <rect x="0" y="0" width="1920" height="1080" fill="url(#bgRadial)"/>
  <rect x="0" y="0" width="1920" height="1080" fill="url(#grid)" opacity="0.9"/>
  <path d="M 0 175 C 460 120, 720 210, 980 170 C 1240 130, 1500 55, 1920 110"
        fill="none" stroke="#3B8CFF" stroke-opacity="0.18" stroke-width="2"/>
  <path d="M 0 915 C 520 860, 880 1010, 1180 930 C 1480 850, 1700 780, 1920 820"
        fill="none" stroke="#9A6BFF" stroke-opacity="0.16" stroke-width="2"/>

  <g transform="translate(90,82)">
    <text class="t-title" x="0" y="0" font-size="40" fill="#EAF1FF">\u8bc4\u6d4b\u57fa\u51c6\u5206\u5e03</text>
    <text class="t-sub" x="0" y="34" font-size="18" fill="#9FB3D9">Benchmark landscape  |  \u79d1\u6280\u98ce\u77e2\u91cf\u56fe\uff08\u9002\u7528\u4e8ePPT\uff09</text>
  </g>

  <g transform="translate(90,980)">
    <rect x="0" y="-32" width="520" height="62" rx="14" fill="url(#panelGrad)" stroke="#1D2C57" stroke-opacity="0.9" filter="url(#softShadow)"/>
    <circle cx="24" cy="-1" r="6" fill="#26D6FF" filter="url(#glowCyan)"/>
    <text class="t-sub" x="44" y="6" font-size="16" fill="#CFE0FF">\u72b6\u6001\uff1a\u5df2\u96c6\u6210/\u5df2\u5f00\u53d1\uff08\u5168\u90e8\u57fa\u51c6\uff09</text>
    <text class="t-mono" x="44" y="28" font-size="12" fill="#7E97C7">Total benchmarks: 33  |  Distribution by domain</text>
  </g>

  <!-- Donut: center (960,540), r=220, stroke=28 -->
  <g>
    <circle cx="960" cy="540" r="252" fill="none" stroke="#2C3E78" stroke-opacity="0.25" stroke-width="2"/>
    <circle cx="960" cy="540" r="205" fill="none" stroke="#1B2B55" stroke-opacity="0.55" stroke-width="1.5"/>

    <!-- Total=33; circumference ~ 1382.3 (r=220). -->
    <!-- Segment lengths: 12=502.7, 3=125.7, 4=167.6, 13=544.6, 1=41.9 -->
    <g transform="rotate(-90 960 540)">
      <circle cx="960" cy="540" r="220" fill="none" stroke="#26D6FF" stroke-width="28" stroke-linecap="round"
              stroke-dasharray="502.7 879.6" stroke-dashoffset="0" filter="url(#glowCyan)"/>
      <circle cx="960" cy="540" r="220" fill="none" stroke="#9A6BFF" stroke-width="28" stroke-linecap="round"
              stroke-dasharray="125.7 1256.6" stroke-dashoffset="-520" filter="url(#glowPurple)"/>
      <circle cx="960" cy="540" r="220" fill="none" stroke="#28F59D" stroke-width="28" stroke-linecap="round"
              stroke-dasharray="167.6 1214.7" stroke-dashoffset="-660" filter="url(#glowGreen)"/>
      <circle cx="960" cy="540" r="220" fill="none" stroke="#FF3CC7" stroke-width="28" stroke-linecap="round"
              stroke-dasharray="544.6 837.7" stroke-dashoffset="-850" filter="url(#glowMagenta)"/>
      <circle cx="960" cy="540" r="220" fill="none" stroke="#FFB14A" stroke-width="28" stroke-linecap="round"
              stroke-dasharray="41.9 1340.4" stroke-dashoffset="-1420" filter="url(#glowOrange)"/>
    </g>

    <g filter="url(#softShadow)">
      <circle cx="960" cy="540" r="150" fill="url(#panelGrad)" stroke="#233560" stroke-opacity="0.9"/>
      <circle cx="960" cy="540" r="150" fill="none" stroke="#26D6FF" stroke-opacity="0.18" stroke-width="2"/>
      <text class="t-title" x="960" y="518" font-size="54" text-anchor="middle" fill="#EAF1FF">33</text>
      <text class="t-sub" x="960" y="548" font-size="16" text-anchor="middle" fill="#9FB3D9">\u6838\u5fc3\u8bc4\u6d4b\u57fa\u51c6</text>
      <text class="t-mono" x="960" y="574" font-size="12" text-anchor="middle" fill="#6F87B4">Scientific  |  Long-context  |  Math  |  Multimodal  |  Instruction</text>
    </g>
  </g>

  <!-- Connectors -->
  <g opacity="0.9">
    <path d="M 960 290 L 960 235" stroke="#26D6FF" stroke-opacity="0.55" stroke-width="2" fill="none"/>
    <path d="M 720 470 L 505 430" stroke="#9A6BFF" stroke-opacity="0.45" stroke-width="2" fill="none"/>
    <path d="M 1200 470 L 1415 430" stroke="#28F59D" stroke-opacity="0.45" stroke-width="2" fill="none"/>
    <path d="M 1045 760 L 1215 875" stroke="#FF3CC7" stroke-opacity="0.45" stroke-width="2" fill="none"/>
    <path d="M 875 760 L 700 875" stroke="#FFB14A" stroke-opacity="0.45" stroke-width="2" fill="none"/>
  </g>

  <!-- Panels -->
  <g transform="translate(560,120)" filter="url(#softShadow)">
    <rect x="0" y="0" width="800" height="220" rx="22" fill="url(#panelGrad)" stroke="#26D6FF" stroke-opacity="0.62" stroke-width="2.5" filter="url(#glowCyan)"/>
    <text class="t-title" x="28" y="52" font-size="26" fill="#EAF1FF">\u79d1\u5b66\u63a8\u7406</text>
    <text class="t-mono" x="160" y="52" font-size="13" fill="#7E97C7">12 benchmarks</text>
    <g transform="translate(28,78)">
      <rect x="0" y="0" width="128" height="28" rx="14" fill="#0B1B36" stroke="#1D4C7A" stroke-opacity="0.8"/>
      <circle cx="16" cy="14" r="5" fill="#26D6FF" filter="url(#glowCyan)"/>
      <text class="chip" x="28" y="19" font-size="12" fill="#CFE0FF">\u5df2\u96c6\u6210/\u5df2\u5f00\u53d1</text>
    </g>
    <text class="t-sub" x="28" y="138" font-size="14" fill="#CFE0FF">Scibench | GPQA-Diamond | TOMG-Bench | ChemBench | MasCQA | MSQA_Long | MSQA_Short</text>
    <text class="t-sub" x="28" y="166" font-size="14" fill="#CFE0FF">LLM-MSE | ProteinLMBench | LAB bench | Qiskit HumanEval | PHYSICS</text>
    <path d="M 28 188 L 772 188" stroke="#1D2C57" stroke-opacity="0.9" stroke-width="1"/>
    <text class="t-mono" x="28" y="208" font-size="12" fill="#7E97C7">Domain focus: scientific reasoning &amp; STEM evaluation</text>
  </g>

  <g transform="translate(120,360)" filter="url(#softShadow)">
    <rect x="0" y="0" width="520" height="220" rx="22" fill="url(#panelGrad)" stroke="#9A6BFF" stroke-opacity="0.62" stroke-width="2.5" filter="url(#glowPurple)"/>
    <text class="t-title" x="28" y="52" font-size="26" fill="#EAF1FF">\u957f\u6587\u672c</text>
    <text class="t-mono" x="132" y="52" font-size="13" fill="#7E97C7">3 benchmarks</text>
    <g transform="translate(28,78)">
      <rect x="0" y="0" width="128" height="28" rx="14" fill="#0B1B36" stroke="#3B2C7A" stroke-opacity="0.8"/>
      <circle cx="16" cy="14" r="5" fill="#9A6BFF" filter="url(#glowPurple)"/>
      <text class="chip" x="28" y="19" font-size="12" fill="#CFE0FF">\u5df2\u96c6\u6210/\u5df2\u5f00\u53d1</text>
    </g>
    <text class="t-sub" x="28" y="138" font-size="14" fill="#CFE0FF">CLongEval | InfiniteBench | InternalLongtext</text>
    <path d="M 28 162 L 492 162" stroke="#1D2C57" stroke-opacity="0.9" stroke-width="1"/>
    <text class="t-mono" x="28" y="186" font-size="12" fill="#7E97C7">Domain focus: long-context understanding &amp; retrieval</text>
  </g>

  <g transform="translate(1280,360)" filter="url(#softShadow)">
    <rect x="0" y="0" width="520" height="220" rx="22" fill="url(#panelGrad)" stroke="#28F59D" stroke-opacity="0.62" stroke-width="2.5" filter="url(#glowGreen)"/>
    <text class="t-title" x="28" y="52" font-size="26" fill="#EAF1FF">\u6570\u5b66</text>
    <text class="t-mono" x="112" y="52" font-size="13" fill="#7E97C7">4 benchmarks</text>
    <g transform="translate(28,78)">
      <rect x="0" y="0" width="128" height="28" rx="14" fill="#0B1B36" stroke="#1D7A58" stroke-opacity="0.8"/>
      <circle cx="16" cy="14" r="5" fill="#28F59D" filter="url(#glowGreen)"/>
      <text class="chip" x="28" y="19" font-size="12" fill="#CFE0FF">\u5df2\u96c6\u6210/\u5df2\u5f00\u53d1</text>
    </g>
    <text class="t-sub" x="28" y="138" font-size="14" fill="#CFE0FF">AIME2024 | AIME2025-I | LiveMathBench | AMC23</text>
    <path d="M 28 162 L 492 162" stroke="#1D2C57" stroke-opacity="0.9" stroke-width="1"/>
    <text class="t-mono" x="28" y="186" font-size="12" fill="#7E97C7">Domain focus: competition math &amp; step-by-step reasoning</text>
  </g>

  <g transform="translate(1040,800)" filter="url(#softShadow)">
    <rect x="0" y="0" width="820" height="240" rx="22" fill="url(#panelGrad)" stroke="#FF3CC7" stroke-opacity="0.62" stroke-width="2.5" filter="url(#glowMagenta)"/>
    <text class="t-title" x="28" y="52" font-size="26" fill="#EAF1FF">\u591a\u6a21\u6001</text>
    <text class="t-mono" x="148" y="52" font-size="13" fill="#7E97C7">13 benchmarks</text>
    <g transform="translate(28,78)">
      <rect x="0" y="0" width="128" height="28" rx="14" fill="#0B1B36" stroke="#7A1D62" stroke-opacity="0.8"/>
      <circle cx="16" cy="14" r="5" fill="#FF3CC7" filter="url(#glowMagenta)"/>
      <text class="chip" x="28" y="19" font-size="12" fill="#CFE0FF">\u5df2\u96c6\u6210/\u5df2\u5f00\u53d1</text>
    </g>
    <text class="t-sub" x="28" y="138" font-size="14" fill="#CFE0FF">MMMU | SFE | MMStar | Math Vista | Math Vision | Physics | MicroVQA | MSEarthMCQ</text>
    <text class="t-sub" x="28" y="166" font-size="14" fill="#CFE0FF">XLRS-Bench | ScienceOlympiad | VRSBench | GMAI-MMBench | Galaxy 10 DECaLS</text>
    <path d="M 28 192 L 792 192" stroke="#1D2C57" stroke-opacity="0.9" stroke-width="1"/>
    <text class="t-mono" x="28" y="216" font-size="12" fill="#7E97C7">Domain focus: vision-language reasoning &amp; multi-sensor knowledge</text>
  </g>

  <g transform="translate(120,800)" filter="url(#softShadow)">
    <rect x="0" y="0" width="700" height="240" rx="22" fill="url(#panelGrad)" stroke="#FFB14A" stroke-opacity="0.62" stroke-width="2.5" filter="url(#glowOrange)"/>
    <text class="t-title" x="28" y="52" font-size="26" fill="#EAF1FF">\u6307\u4ee4\u9075\u5faa</text>
    <text class="t-mono" x="190" y="52" font-size="13" fill="#7E97C7">1 benchmark</text>
    <g transform="translate(28,78)">
      <rect x="0" y="0" width="128" height="28" rx="14" fill="#0B1B36" stroke="#7A4A1D" stroke-opacity="0.8"/>
      <circle cx="16" cy="14" r="5" fill="#FFB14A" filter="url(#glowOrange)"/>
      <text class="chip" x="28" y="19" font-size="12" fill="#CFE0FF">\u5df2\u96c6\u6210/\u5df2\u5f00\u53d1</text>
    </g>
    <text class="t-sub" x="28" y="138" font-size="14" fill="#CFE0FF">IFEval</text>
    <path d="M 28 162 L 672 162" stroke="#1D2C57" stroke-opacity="0.9" stroke-width="1"/>
    <text class="t-mono" x="28" y="186" font-size="12" fill="#7E97C7">Domain focus: instruction following &amp; controllability</text>
  </g>

  <g opacity="0.65" transform="translate(1490,56)">
    <rect x="0" y="0" width="360" height="44" rx="14" fill="#0A1127" stroke="#1D2C57" stroke-opacity="0.9"/>
    <text class="t-mono" x="18" y="28" font-size="12" fill="#8CA5D6">Generated: benchmark distribution (SVG for PPT)</text>
  </g>
</svg>
"""

    out = Path("/workspace/assets/benchmark_distribution.svg")
    out.write_text(svg, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

