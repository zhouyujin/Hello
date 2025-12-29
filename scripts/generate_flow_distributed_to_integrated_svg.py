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

  <g transform="translate(90,110)">
    <text class="title" x="0" y="0" font-size="44" fill="#0B2E6B">\u4ece\u5206\u6563\u5f0f\u6d41\u7a0b\u5230\u4e00\u4f53\u5316\u6d41\u7a0b</text>
    <text class="txt" x="0" y="34" font-size="18" fill="#4D6A9B">\u7edf\u4e00\u53e3\u5f84 \u00b7 \u6d41\u7a0b\u4f18\u5316 \u00b7 \u53ef\u590d\u7528\u7ec4\u4ef6 \u00b7 \u6807\u51c6\u5316\u8f93\u51fa</text>
  </g>

  <!-- Left: Distributed -->
  <g transform="translate(90,210)">
    <text class="sub" x="0" y="0" font-size="26" fill="#2E4C7D">\u5206\u6563\u5f0f\u6d41\u7a0b</text>
    <text class="mono" x="0" y="28" font-size="12" fill="#6B86B5">multi-team / multi-script / multi-standard</text>

    <g opacity="0.95">
      <g fill="#FFFFFF" stroke="#D3E0F5" stroke-width="2">
        <rect x="0" y="70" width="160" height="54" rx="12"/>
        <rect x="0" y="150" width="160" height="54" rx="12"/>
        <rect x="0" y="230" width="160" height="54" rx="12"/>
        <rect x="0" y="310" width="160" height="54" rx="12"/>
        <rect x="0" y="390" width="160" height="54" rx="12"/>

        <rect x="220" y="110" width="160" height="54" rx="12"/>
        <rect x="220" y="250" width="160" height="54" rx="12"/>
        <rect x="220" y="390" width="160" height="54" rx="12"/>

        <rect x="440" y="70" width="160" height="54" rx="12"/>
        <rect x="440" y="190" width="160" height="54" rx="12"/>
        <rect x="440" y="310" width="160" height="54" rx="12"/>
        <rect x="440" y="430" width="160" height="54" rx="12"/>
      </g>

      <g fill="none" stroke="#A9BDE2" stroke-width="3" stroke-linecap="round" opacity="0.65">
        <path d="M 160 97 C 220 80, 260 120, 220 137"/>
        <path d="M 160 177 C 250 165, 290 220, 220 277"/>
        <path d="M 160 257 C 240 260, 310 260, 440 97"/>
        <path d="M 160 337 C 240 335, 320 320, 440 217"/>
        <path d="M 160 417 C 270 410, 330 455, 440 337"/>
        <path d="M 380 137 C 425 135, 420 90, 440 97"/>
        <path d="M 380 277 C 420 280, 420 230, 440 217"/>
        <path d="M 380 417 C 430 410, 420 360, 440 337"/>
        <path d="M 600 97 C 650 120, 670 170, 720 170"/>
        <path d="M 600 217 C 650 235, 670 275, 720 270"/>
        <path d="M 600 337 C 650 355, 675 395, 720 395"/>
        <path d="M 600 457 C 650 470, 680 520, 720 520"/>
      </g>

      <g class="txt" font-size="14" fill="#2E4C7D">
        <text x="18" y="104">\u6570\u636e\u51c6\u5907</text>
        <text x="18" y="184">\u811a\u672cA</text>
        <text x="18" y="264">\u811a\u672cB</text>
        <text x="18" y="344">\u53e3\u5f84\u4e0d\u4e00</text>
        <text x="18" y="424">\u4eba\u5de5\u6c47\u603b</text>

        <text x="238" y="144">\u73af\u5883\u914d\u7f6e</text>
        <text x="238" y="284">\u591a\u699c\u5355\u62fc\u88c5</text>
        <text x="238" y="424">\u91cd\u590d\u5f00\u53d1</text>

        <text x="458" y="104">\u8bc4\u6d4b\u6267\u884c</text>
        <text x="458" y="224">\u6307\u6807\u8ba1\u7b97</text>
        <text x="458" y="344">\u62a5\u8868\u751f\u6210</text>
        <text x="458" y="464">\u53d1\u5e03/\u5bf9\u9f50</text>
      </g>

      <g transform="translate(720,126)" fill="#FFFFFF" stroke="#D3E0F5" stroke-width="2">
        <rect x="0" y="0" width="160" height="54" rx="12"/>
        <rect x="0" y="100" width="160" height="54" rx="12"/>
        <rect x="0" y="200" width="160" height="54" rx="12"/>
        <rect x="0" y="300" width="160" height="54" rx="12"/>
      </g>
      <g class="txt" font-size="14" fill="#2E4C7D">
        <text x="740" y="160">\u7ed3\u679c\u6587\u4ef6</text>
        <text x="740" y="260">\u622a\u56fe</text>
        <text x="740" y="360">\u4e34\u65f6\u62a5\u8868</text>
        <text x="740" y="460">\u90ae\u4ef6\u540c\u6b65</text>
      </g>
    </g>
  </g>

  <!-- Middle arrow -->
  <g transform="translate(980,455)">
    <path d="M 0 85 L 120 85 L 120 45 L 220 120 L 120 195 L 120 155 L 0 155 Z"
          fill="url(#blue)" filter="url(#shadow)"/>
    <text class="mono" x="32" y="230" font-size="12" fill="#6B86B5">unify &amp; streamline</text>
  </g>

  <!-- Right: Integrated -->
  <g transform="translate(1210,210)">
    <text class="sub" x="0" y="0" font-size="26" fill="#0B2E6B">\u4e00\u4f53\u5316\u6d41\u7a0b</text>
    <text class="mono" x="0" y="28" font-size="12" fill="#6B86B5">standard input \u2192 unified orchestration \u2192 reusable modules \u2192 standard output</text>

    <g transform="translate(0,110)">
      <g fill="#FFFFFF" stroke="#D3E0F5" stroke-width="2">
        <rect x="0" y="0" width="180" height="54" rx="12"/>
        <rect x="0" y="80" width="180" height="54" rx="12"/>
        <rect x="0" y="160" width="180" height="54" rx="12"/>
        <rect x="0" y="240" width="180" height="54" rx="12"/>
      </g>
      <g class="txt" font-size="14" fill="#2E4C7D">
        <text x="20" y="34">\u4efb\u52a1/\u6570\u636e</text>
        <text x="20" y="114">\u914d\u7f6e/\u8d44\u6e90</text>
        <text x="20" y="194">\u699c\u5355\u9700\u6c42</text>
        <text x="20" y="274">\u6a21\u578b\u7248\u672c</text>
      </g>
      <path d="M 205 12 C 235 12, 235 12, 235 12 L 235 282 C 235 282, 235 282, 205 282"
            fill="none" stroke="#0B3D91" stroke-width="10" stroke-linecap="round"/>
    </g>

    <g transform="translate(280,170)" filter="url(#shadow)">
      <rect x="0" y="0" width="980" height="250" rx="24" fill="#FFFFFF" stroke="#CFE0FB" stroke-width="2"/>

      <g transform="translate(28,42)">
        <g>
          <rect x="0" y="0" width="200" height="70" rx="16" fill="#F1F7FF" stroke="#CFE0FB"/>
          <text class="sub" x="26" y="30" font-size="16" fill="#0B2E6B">\u6807\u51c6\u5316\u8f93\u5165</text>
          <text class="mono" x="26" y="52" font-size="12" fill="#6B86B5">schema / validator</text>
        </g>
        <g transform="translate(240,0)">
          <rect x="0" y="0" width="200" height="70" rx="16" fill="#F1F7FF" stroke="#CFE0FB"/>
          <text class="sub" x="26" y="30" font-size="16" fill="#0B2E6B">\u7edf\u4e00\u8c03\u5ea6</text>
          <text class="mono" x="26" y="52" font-size="12" fill="#6B86B5">orchestrator</text>
        </g>
        <g transform="translate(480,0)">
          <rect x="0" y="0" width="200" height="70" rx="16" fill="#F1F7FF" stroke="#CFE0FB"/>
          <text class="sub" x="26" y="30" font-size="16" fill="#0B2E6B">\u53ef\u590d\u7528\u6a21\u5757</text>
          <text class="mono" x="26" y="52" font-size="12" fill="#6B86B5">runner / metric / report</text>
        </g>
        <g transform="translate(720,0)">
          <rect x="0" y="0" width="200" height="70" rx="16" fill="#F1F7FF" stroke="#CFE0FB"/>
          <text class="sub" x="26" y="30" font-size="16" fill="#0B2E6B">\u6807\u51c6\u5316\u8f93\u51fa</text>
          <text class="mono" x="26" y="52" font-size="12" fill="#6B86B5">dashboards / artifacts</text>
        </g>

        <g fill="none" stroke="#1E88E5" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
          <path d="M 200 35 L 235 35"/>
          <path d="M 435 35 L 475 35"/>
          <path d="M 680 35 L 715 35"/>
        </g>
        <g fill="#1E88E5">
          <path d="M 236 35 l -12 -8 v16 z"/>
          <path d="M 476 35 l -12 -8 v16 z"/>
          <path d="M 716 35 l -12 -8 v16 z"/>
        </g>
      </g>

      <g transform="translate(28,150)">
        <rect x="0" y="0" width="924" height="72" rx="18" fill="url(#blue)" opacity="0.10"/>
        <rect x="0" y="0" width="924" height="72" rx="18" fill="none" stroke="#D7E6FF"/>
        <text class="sub" x="24" y="30" font-size="16" fill="#0B2E6B">\u6548\u7387\u63d0\u5347</text>
        <text class="txt" x="24" y="54" font-size="14" fill="#2E4C7D">\u79d1\u5b66\u63a8\u7406\u8bc4\u6d4b\u5468\u671f\uff1a7\u5929 \u2192 30\u5c0f\u65f6\uff1b\u591a\u7c7b\u578b\u699c\u5355\u8bc4\u6d4b\uff1a\u81f3\u5c114\u4eba\u534f\u4f5c \u2192 \u5355\u4eba\u5b8c\u6210</text>
        <text class="mono" x="740" y="44" font-size="12" fill="#0B2E6B">cycle \u2193 ~82%  |  manpower \u2193 ~75%</text>
      </g>
    </g>
  </g>

  <g transform="translate(90,1015)">
    <text class="mono" x="0" y="0" font-size="12" fill="#7A93BF">Figure: distributed-to-integrated evaluation pipeline (blue minimalist)</text>
  </g>
</svg>
"""

    out = Path("/workspace/assets/flow_distributed_to_integrated.svg")
    out.write_text(svg, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()

