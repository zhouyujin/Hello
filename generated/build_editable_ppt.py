from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Pt


TEMPLATE_PATH = "/workspace/2025年度部门工作总结参考模板及要求.pptx"
OUTPUT_PATH = "/workspace/generated/2025工作及发展总结-可编辑版.pptx"


TITLE_FONT = "Source Han Sans CN Bold"
BODY_FONT = "微软雅黑"
TITLE_COLOR = RGBColor(0x06, 0x5D, 0xDF)
BODY_COLOR = RGBColor(0x00, 0x00, 0x00)


@dataclass(frozen=True)
class SlideSpec:
    title: str
    subtitle: str | None = None
    bullets: Sequence[str] | None = None
    footer_note: str | None = None


def _set_shape_text(
    shape,
    text: str,
    *,
    font_name: str | None = None,
    font_size_pt: int | None = None,
    bold: bool | None = None,
    color: RGBColor | None = None,
):
    if not getattr(shape, "has_text_frame", False):
        return
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    font = run.font
    if font_name is not None:
        font.name = font_name
    if font_size_pt is not None:
        font.size = Pt(font_size_pt)
    if bold is not None:
        font.bold = bold
    if color is not None:
        font.color.rgb = color


def _set_bullets(
    shape,
    bullets: Iterable[str],
    *,
    font_name: str = BODY_FONT,
    font_size_pt: int = 14,
    color: RGBColor = BODY_COLOR,
):
    if not getattr(shape, "has_text_frame", False):
        return
    tf = shape.text_frame
    tf.clear()
    first = True
    for b in bullets:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.text = b
        p.level = 0
        if p.runs:
            run = p.runs[0]
        else:
            run = p.add_run()
            run.text = b
        font = run.font
        font.name = font_name
        font.size = Pt(font_size_pt)
        font.bold = False
        font.color.rgb = color


def _add_title(slide, title: str):
    # Match template title box geometry approximately
    left = 271_032
    top = 194_575
    width = 11_000_000
    height = 600_000
    tb = slide.shapes.add_textbox(left, top, width, height)
    _set_shape_text(
        tb,
        title,
        font_name=TITLE_FONT,
        font_size_pt=30,
        bold=True,
        color=TITLE_COLOR,
    )


def _add_subtitle(slide, subtitle: str):
    left = 516_000
    top = 639_337
    width = 10_640_060
    height = 875_881
    tb = slide.shapes.add_textbox(left, top, width, height)
    _set_shape_text(tb, subtitle, font_name=BODY_FONT, font_size_pt=18, bold=True, color=BODY_COLOR)


def _add_body(slide, bullets: Sequence[str], footer_note: str | None = None):
    left = 713_310
    top = 1_400_000
    width = 11_340_000
    height = 3_900_000
    body = slide.shapes.add_textbox(left, top, width, height)
    _set_bullets(body, bullets, font_name=BODY_FONT, font_size_pt=16, color=BODY_COLOR)

    if footer_note:
        left_f = 635_400
        top_f = 5_588_115
        width_f = 9_897_745
        height_f = 506_730
        ft = slide.shapes.add_textbox(left_f, top_f, width_f, height_f)
        _set_shape_text(ft, footer_note, font_name=BODY_FONT, font_size_pt=14, bold=True, color=BODY_COLOR)


def add_simple_content_slide(prs: Presentation, spec: SlideSpec):
    blank_layout = prs.slide_layouts[3]  # "空白"
    slide = prs.slides.add_slide(blank_layout)
    _add_title(slide, spec.title)
    if spec.subtitle:
        _add_subtitle(slide, spec.subtitle)
    if spec.bullets:
        _add_body(slide, spec.bullets, footer_note=spec.footer_note)
    return slide


def main():
    prs = Presentation(TEMPLATE_PATH)

    # Repurpose slide 1 as section cover (01)
    s1 = prs.slides[0]
    _set_shape_text(
        s1.shapes[0],
        "01 2025年度工作完成情况复盘",
        font_name=TITLE_FONT,
        font_size_pt=30,
        bold=True,
        color=TITLE_COLOR,
    )
    _set_shape_text(
        s1.shapes[3],
        "围绕“模型评测体系搭建与优化、评测基准研发、跨团队协同支撑”三大模块，总结年度业绩与管理职责完成情况，复盘亮点与不足。",
        font_name=BODY_FONT,
        font_size_pt=18,
        bold=True,
        color=BODY_COLOR,
    )
    _set_shape_text(
        s1.shapes[1],
        "目录\\n1）总体目标达成情况（定量+定性）\\n2）人才与组织建设情况\\n3）亮点：三项主要贡献\\n4）不足：结果分析与复盘",
        font_name=BODY_FONT,
        font_size_pt=16,
        bold=True,
        color=BODY_COLOR,
    )
    _set_shape_text(
        s1.shapes[2],
        "聚焦核心专项：以数据/案例/事实清晰呈现“效率、质量、可复用能力”提升。",
        font_name=BODY_FONT,
        font_size_pt=14,
        bold=True,
        color=BODY_COLOR,
    )

    # Repurpose slide 2 as "总体目标达成情况（定量+定性）"
    s2 = prs.slides[1]
    _set_shape_text(
        s2.shapes[0],
        "总体目标达成情况（定量+定性）",
        font_name=TITLE_FONT,
        font_size_pt=30,
        bold=True,
        color=TITLE_COLOR,
    )
    _set_shape_text(
        s2.shapes[1],
        "总体目标：支撑主线模型迭代与对标评测，以标准化评测流程提升效率与结论可信度。",
        font_name=BODY_FONT,
        font_size_pt=18,
        bold=True,
        color=BODY_COLOR,
    )
    _set_shape_text(
        s2.shapes[3],
        "结果导向：用统一口径与可复用流程，保障“快出结论、可复现、可对比”。",
        font_name=BODY_FONT,
        font_size_pt=14,
        bold=True,
        color=BODY_COLOR,
    )
    _set_shape_text(
        s2.shapes[2],
        "定量成果\\n- 累计完成超100个模型评测（文本+多模态）\\n- 集成18个文本评测基准（12科学推理/4数学/3长文/1指令遵循）\\n- 科学推理类评测周期：7天 → 30小时\\n- 多类型榜单评测：从至少4人协作 → 1人集中落地\\n- 多模态评测从0到1：复用VLMEvalKit，研发13个多模态榜单\\n\\n定性成果\\n- 构建覆盖文本/多模态、基础/强化训练模型的全链条评测能力\\n- 输出多批关键评测结论，为模型迭代与对标提供核心数据支撑\\n- 推动评测环境多场地迁移落地，保障评测连续性与协同效率",
        font_name=BODY_FONT,
        font_size_pt=16,
        bold=True,
        color=BODY_COLOR,
    )

    # Additional slides for 01
    add_simple_content_slide(
        prs,
        SlideSpec(
            title="人才与组织建设情况",
            subtitle="组织能力沉淀：标准化、可复用、可共享",
            bullets=[
                "评测流程标准化：形成可复用的评测流程与操作规范，降低上手与协同成本",
                "评测底座复用：复用EvalScope/VLMEvalKit两大框架，完成环境适配、源码整理与说明文档",
                "跨团队协同：与榜单同事/模型组对齐口径与答案验证方式，保障评测结论一致与可复现",
                "资源与环境建设：推进评测环境迁移与资源同步，提升评测吞吐与稳定性",
            ],
            footer_note="组织产出以“流程+工具+文档”三件套沉淀，支撑后续规模化评测与自动化演进。",
        ),
    )

    add_simple_content_slide(
        prs,
        SlideSpec(
            title="亮点：对组织的三项主要贡献",
            subtitle="业务管理 / 组织建设 / 团队建设",
            bullets=[
                "① 业务管理成果：完成主线与竞品模型的性能摸底与横向对比，持续输出关键评测结论，支撑模型迭代决策",
                "② 组织建设成果：评测体系一体化（统一口径+流程优化），文本评测基准集中管理；多模态评测从0到1体系化落地",
                "③ 团队建设成果：将多类型榜单评测集中落地，显著降低多人协作成本；推动知识与经验沉淀（代码/文档/规范），便于团队复用",
            ],
            footer_note="关键突破：效率提升（7天→30小时）+ 能力拓展（多模态13榜单）+ 协作降本（多人→单人集中）。",
        ),
    )

    add_simple_content_slide(
        prs,
        SlideSpec(
            title="不足：结果分析与总结复盘",
            subtitle="问题聚焦：新基准预研不足 → 集成延迟",
            bullets=[
                "问题：科学文献类基准开发中，对评测维度调研不够深入；测试阶段发现短板——相似度计算不支持多模型并行评测，且维度不足以体现“科研创新Idea生成”能力",
                "影响：适配难点预判不足，导致该基准未能及时集成到整体评测体系，影响推进效率",
                "根因：技术细节预研不足（框架能力边界、评测指标设计、适配成本评估）",
                "改进：面对新框架/新领域，提前拆解核心难点与验证路径；先做小样本PoC与可行性验证，再规模化集成",
            ],
            footer_note="启示：技术预研是效率杠杆；“先验证关键假设，再投入工程化”可显著降低返工与延期风险。",
        ),
    )

    # Section 02 cover + plan slides
    add_simple_content_slide(
        prs,
        SlideSpec(
            title="02 2026年重点工作计划",
            subtitle="面向经营与效率：聚焦评测底座自动化、体系化与影响力输出",
            bullets=[
                "总体方向：多模态评测优化 + 自动化流水线搭建 + 跨团队核心项目深度参与",
                "目标牵引：提升评测效率/稳定性/可复现性，持续为模型迭代提供高质量结论",
                "产出规划：评测平台与知识沉淀（工具/规范/文档） + 知识产权（专利1-2篇）",
            ],
            footer_note="建议：聚焦2026年核心重点工作，明确里程碑与责任人，保障“拿结果”。",
        ),
    )

    add_simple_content_slide(
        prs,
        SlideSpec(
            title="2026｜业务管理策略与规划",
            subtitle="策略：统一底座 + 自动化流水线 + 结论可追溯",
            bullets=[
                "评测流水线自动化：评测任务编排、资源调度、结果汇总与可视化，减少人工重复操作",
                "统一评测底座：整合文本与多模态评测能力，形成统一口径、统一产物与版本化管理",
                "质量保障机制：指标计算逻辑校准、回归验证与基准版本冻结，提升结论可信度",
                "交付节奏：按“月度里程碑+重点模型/榜单清单”推进，确保关键节点稳定交付",
            ],
        ),
    )

    add_simple_content_slide(
        prs,
        SlideSpec(
            title="2026｜组织能力与团队建设举措",
            subtitle="举措：知识库沉淀 + 最佳实践复用 + 协同提效",
            bullets=[
                "建立开源框架技术知识库：系统沉淀适配难点、解决方案与最佳实践，团队共享复用",
                "标准化资产建设：评测操作手册、故障排查SOP、评测报告模板与复现实验脚本",
                "跨团队协同机制：与模型/数据/平台侧对齐接口与口径，减少“返工与口径不一致”",
                "个人成长与影响力：持续提升AI领域技术深度，参与核心项目攻关；输出专利1-2篇",
            ],
        ),
    )

    prs.save(OUTPUT_PATH)
    print(f"saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
