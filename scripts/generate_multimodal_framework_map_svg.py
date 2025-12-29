from __future__ import annotations

from pathlib import Path


def main() -> None:
    # ASCII-only source; write clean UTF-8 output.
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="100%" stop-color="#EEF4FF"/>
    </linearGradient>
    <linearGradient id="blue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1E88E5"/>
      <stop offset="100%" stop-color="#0B3D91"/>
    </linearGradient>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="10" stdDeviation="10" flood-color="#0B2E6B" flood-opacity="0.16"/>
    </filter>
    <style>
      .title { font-family: Inter, "Noto Sans CJK SC", "Microsoft YaHei", system-ui, -apple-system, "Segoe UI", Arial, sans-serif; font-weight: 700; }
      .sub { font-family: Inter, "Noto Sans CJK SC", "Microsoft YaHei", system-ui, -apple-system, "Segoe UI", Arial, sans-serif; font-weight: 600; }
      .txt { font-family: Inter, "Noto Sans CJK SC", "Microsoft YaHei", system-ui, -apple-system, "Segoe UI", Arial, sans-serif; font-weight: 500; }
      .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
    </style>
  </defs>

  <rect x="0" y="0" width="1920" height="1080" fill="url(#bg)"/>

  <!-- Header -->
  <g transform="translate(90,110)">
    <text class="title" x="0" y="0" font-size="44" fill="#0B2E6B">\u591a\u6a21\u6001\u7edf\u4e00\u6846\u67b6\u9002\u914d\u80fd\u529b\u7248\u56fe</text>
    <text class="txt" x="0" y="34" font-size="18" fill="#4D6A9B">\u4ece0\u52301\u6784\u5efa\u8bc4\u6d4b\u80fd\u529b\uff1a\u6846\u67b6\u6807\u51c6\u5316 \u00b7 \u6a21\u5757\u590d\u7528 \u00b7 \u699c\u5355\u751f\u4ea7\u5316</text>
  </g>

  <!-- Left narrative -->
  <g transform="translate(90,220)">
    <rect x="0" y="0" width="620" height="760" rx="24" fill="#FFFFFF" stroke="#CFE0FB" stroke-width="2" filter="url(#shadow)"/>
    <g transform="translate(34,44)">
      <text class="sub" x="0" y="0" font-size="24" fill="#0B2E6B">\u4ece0\u52301\u8bbe\u8ba1\u4e0e\u843d\u5730</text>
      <text class="txt" x="0" y="36" font-size="16" fill="#2E4C7D">\u6838\u5fc3\u601d\u8def\uff1a\u7edf\u4e00\u5165\u53e3\uff0c\u89e3\u8026\u63a5\u5165\uff0c\u6a21\u677f\u5316\u751f\u4ea7\u699c\u5355\uff0c\u6807\u51c6\u5316\u4ea7\u51fa</text>

      <g transform="translate(0,90)">
        <g>
          <circle cx="10" cy="10" r="8" fill="url(#blue)"/>
          <text class="sub" x="30" y="16" font-size="18" fill="#0B2E6B">\u6280\u672f\u9009\u578b</text>
          <text class="txt" x="30" y="44" font-size="14" fill="#4D6A9B">\u9009\u62e9\u7edf\u4e00\u6846\u67b6\u4f5c\u4e3a\u5f00\u53d1\u57fa\u5ea7\uff0c\u652f\u6301\u591a\u4efb\u52a1\u591a\u6a21\u6001</text>
        </g>
        <g transform="translate(0,90)">
          <circle cx="10" cy="10" r="8" fill="url(#blue)"/>
          <text class="sub" x="30" y="16" font-size="18" fill="#0B2E6B">\u6846\u67b6\u653b\u575a</text>
          <text class="txt" x="30" y="44" font-size="14" fill="#4D6A9B">\u6570\u636e\u96c6\u63a5\u5165\u3001\u8c03\u8bd5\u6539\u9020\u3001\u672c\u5730\u5316\u4f18\u5316\u4e0e\u7ec4\u4ef6\u5316</text>
        </g>
        <g transform="translate(0,180)">
          <circle cx="10" cy="10" r="8" fill="url(#blue)"/>
          <text class="sub" x="30" y="16" font-size="18" fill="#0B2E6B">\u4f53\u7cfb\u6784\u5efa</text>
          <text class="txt" x="30" y="44" font-size="14" fill="#4D6A9B">\u6c89\u6dc0\u6807\u51c6\u6307\u6807\u4f53\u7cfb\uff0c\u4ea7\u51fa\u53ef\u590d\u7528\u6d41\u7a0b\u4e0e\u6a21\u677f</text>
        </g>
        <g transform="translate(0,270)">
          <circle cx="10" cy="10" r="8" fill="url(#blue)"/>
          <text class="sub" x="30" y="16" font-size="18" fill="#0B2E6B">\u6210\u679c\u6c89\u6dc0</text>
          <text class="txt" x="30" y="44" font-size="14" fill="#4D6A9B">\u5b9e\u73b0\u6982\u8981\u5316\u62a5\u8868\u3001\u7ed3\u679c\u53ef\u8ffd\u6eaf\uff0c\u4e3a\u670d\u52a1\u5316/\u90e8\u7f72\u8f7b\u91cf\u5316\u6253\u57fa\u7840</text>
        </g>
      </g>

      <g transform="translate(0,520)">
        <rect x="0" y="0" width="552" height="160" rx="20" fill="#F1F7FF" stroke="#D7E6FF"/>
        <text class="sub" x="22" y="34" font-size="18" fill="#0B2E6B">\u8f93\u51fa\u6982\u89c8</text>
        <text class="txt" x="22" y="64" font-size="14" fill="#2E4C7D">\u5f00\u53d1 <tspan class="sub" fill="#0B3D91">13</tspan> \u4e2a\u591a\u6a21\u6001\u699c\u5355\u5e76\u6d41\u7a0b\u6807\u51c6\u5316</text>
        <text class="txt" x="22" y="92" font-size="14" fill="#2E4C7D">\u540c\u4e00\u4e2a\u6846\u67b6\u53ef\u6269\u5c55\u63a5\u5165\u65b0\u57fa\u51c6\uff08Custom Benchmark\uff09</text>
        <text class="mono" x="22" y="126" font-size="12" fill="#6B86B5">foundation → adapters → templates → leaderboards → service</text>
      </g>
    </g>
  </g>

  <!-- Center framework (blueprint-ish) -->
  <g transform="translate(760,250)" filter="url(#shadow)">
    <rect x="0" y="0" width="1060" height="690" rx="26" fill="#FFFFFF" stroke="#CFE0FB" stroke-width="2"/>
    <g transform="translate(36,40)">
      <text class="sub" x="0" y="0" font-size="26" fill="#0B2E6B">Unified Multimodal Evaluation Framework</text>
      <text class="mono" x="0" y="26" font-size="12" fill="#6B86B5">standard adapters / templates / metrics / reporting</text>

      <!-- Layers -->
      <g transform="translate(0,70)">
        <!-- Foundation -->
        <rect x="0" y="0" width="620" height="140" rx="22" fill="#F7FBFF" stroke="#D7E6FF"/>
        <rect x="20" y="24" width="220" height="44" rx="14" fill="url(#blue)" opacity="0.12"/>
        <text class="sub" x="30" y="54" font-size="16" fill="#0B2E6B">\u6846\u67b6\u57fa\u5ea7 (Foundation)</text>
        <text class="txt" x="30" y="88" font-size="14" fill="#2E4C7D">\u8fd0\u884c\u5668 / \u8d44\u6e90\u7ba1\u7406 / \u7f13\u5b58 / \u65e5\u5fd7 / \u4efb\u52a1\u961f\u5217</text>
        <text class="mono" x="30" y="114" font-size="12" fill="#6B86B5">runner • scheduler • cache • trace</text>

        <!-- Adapters -->
        <g transform="translate(0,170)">
          <rect x="0" y="0" width="620" height="170" rx="22" fill="#F7FBFF" stroke="#D7E6FF"/>
          <rect x="20" y="24" width="220" height="44" rx="14" fill="url(#blue)" opacity="0.12"/>
          <text class="sub" x="30" y="54" font-size="16" fill="#0B2E6B">\u9002\u914d\u5c42 (Adapters)</text>
          <g class="txt" font-size="14" fill="#2E4C7D">
            <text x="30" y="88">\u6570\u636e\u9002\u914d\uff1aVQA / OCR / Chart / Geo / Video / Multi-image</text>
            <text x="30" y="116">\u6a21\u578b\u9002\u914d\uff1aVLM / API / \u672c\u5730\u90e8\u7f72 / Batch inference</text>
            <text x="30" y="144">\u8bc4\u6d4b\u8f93\u51fa\uff1aJSONL / Parquet / \u6307\u6807\u62a5\u8868 / \u5bf9\u6bd4\u770b\u677f</text>
          </g>
        </g>

        <!-- Templates + Metrics -->
        <g transform="translate(0,360)">
          <rect x="0" y="0" width="620" height="200" rx="22" fill="#F7FBFF" stroke="#D7E6FF"/>
          <rect x="20" y="24" width="260" height="44" rx="14" fill="url(#blue)" opacity="0.12"/>
          <text class="sub" x="30" y="54" font-size="16" fill="#0B2E6B">\u6a21\u677f\u4e0e\u6307\u6807 (Templates &amp; Metrics)</text>
          <g class="txt" font-size="14" fill="#2E4C7D">
            <text x="30" y="92">\u4efb\u52a1\u6a21\u677f\uff1a\u9009\u62e9\u9898 / \u7b80\u7b54 / \u591a\u5f62\u5f0f\u89e3\u6790 / \u8bc1\u636e\u5bf9\u9f50</text>
            <text x="30" y="120">\u6307\u6807\u7cfb\u7edf\uff1aaccuracy / score / robustness / \u6545\u969c\u5206\u7c7b</text>
            <text x="30" y="148">\u62a5\u8868\u6a21\u5757\uff1a\u699c\u5355\u5b9e\u65f6\u66f4\u65b0\uff0c\u7ed3\u679c\u53ef\u8ffd\u6eaf</text>
          </g>
          <text class="mono" x="30" y="176" font-size="12" fill="#6B86B5">standardized pipeline enables leaderboard production at scale</text>
        </g>
      </g>

      <!-- Right: Completed leaderboards -->
      <g transform="translate(680,70)">
        <rect x="0" y="0" width="330" height="540" rx="22" fill="#0B3D91" opacity="0.05" stroke="#D7E6FF"/>
        <text class="sub" x="22" y="44" font-size="18" fill="#0B2E6B">\u5df2\u5b8c\u6210\u591a\u6a21\u6001\u699c\u5355</text>
        <text class="mono" x="22" y="66" font-size="12" fill="#6B86B5">13 leaderboards</text>

        <g fill="#FFFFFF" stroke="#CFE0FB" stroke-width="2">
          <rect x="22" y="92" width="286" height="54" rx="14"/>
          <rect x="22" y="162" width="286" height="54" rx="14"/>
          <rect x="22" y="232" width="286" height="54" rx="14"/>
          <rect x="22" y="302" width="286" height="54" rx="14"/>
          <rect x="22" y="372" width="286" height="54" rx="14"/>
          <rect x="22" y="442" width="286" height="70" rx="14"/>
        </g>
        <g class="txt" font-size="14" fill="#2E4C7D">
          <text x="44" y="126">ScienceOlympiad</text>
          <text x="44" y="196">GMAI-MMBench</text>
          <text x="44" y="266">VRSBench</text>
          <text x="44" y="336">MMMU / MMStar</text>
          <text x="44" y="406">MSEarthMCQ / MicroVQA</text>
          <text x="44" y="476">Custom Benchmark (plug-in)</text>
          <text class="mono" x="44" y="500" font-size="12" fill="#6B86B5">adapter + template + metric</text>
        </g>
      </g>

      <!-- Connector lines (blueprint style) -->
      <g fill="none" stroke="#1E88E5" stroke-opacity="0.35" stroke-width="3">
        <path d="M 620 140 C 660 140, 660 140, 680 140"/>
        <path d="M 620 255 C 660 255, 660 255, 680 255"/>
        <path d="M 620 470 C 660 470, 660 470, 680 470"/>
      </g>
      <g fill="#1E88E5" opacity="0.6">
        <path d="M 680 140 l -16 -10 v20 z"/>
        <path d="M 680 255 l -16 -10 v20 z"/>
        <path d="M 680 470 l -16 -10 v20 z"/>
      </g>
    </g>
  </g>

  <g transform="translate(90,1015)">
    <text class="mono" x="0" y="0" font-size="12" fill="#7A93BF">Figure: multimodal unified framework capability map (blue minimalist)</text>
  </g>
</svg>
"""

    out = Path("/workspace/assets/multimodal_framework_map.svg")
    out.write_text(svg, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

