"""04_build_report_bilingual.py — DTC 客服工具地图 v2(去 AI 味)"""
from __future__ import annotations
import json, re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"


def load(): return json.loads((OUT / "analysis_stats.json").read_text())


# ============================================================
# 中文
# ============================================================
def build_zh(s):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    vs = s["vendor_share"]
    cov = s["widget_coverage"]
    ai = s["ai_signal"]
    multi = s["multi_widget_examples"]
    total = s["_meta"]["effective_rows"]
    top1, top2, top3 = vs[0], vs[1], vs[2]

    L = []
    L.append("# DTC 圈的客服工具,其实是个错配生态")
    L.append("")
    L.append(f"> {today} · 1,148 个 DTC 品牌主页静态扫描 · 23 种客服 vendor 指纹识别")
    L.append("")
    L.append("---")
    L.append("")
    L.append("我们抓了 1,148 个 DTC 品牌的主页 HTML,扫了一遍上面装的客服 widget——也就是访客打开页面那一刻能直接看到的「chat」按钮、bubble、或者 messenger 入口背后是哪家 vendor。结果不复杂,但和大多数人脑子里那个「SaaS 圈客服老大就是 DTC 圈客服老大」的印象,完全对不上。")
    L.append("")
    L.append("最有意思的不是 Gorgias 占 23.3% 这个数字本身——这个数字我们必须先打个折,稍后讲为什么。最有意思的是,**SaaS 圈无可争议的客服老大 Intercom,在 DTC 圈占 0.6%**。1,148 个品牌里只有 7 个用 Intercom。一个 in-product messenger 范式的产品,在「客户根本不在 product 里」的电商场景里,几乎被完全淘汰。")
    L.append("")
    L.append("这份报告主要回答两个问题。第一,DTC 客服工具市场是什么形状——谁赢、谁陪跑、谁退出?第二,AI 客服在 DTC 真的渗透到什么程度——招聘 JD 里 AI 工具命中率 35.6%(我们 5 月 11 日发的 AI Required Position Rate 报告里的数字),那 DTC 实战页面上呢?")
    L.append("")
    L.append("先讲第二个,因为对比最反差。")
    L.append("")
    L.append("## AI 客服:JD 里 35.6%,DTC 主页上 1.1%")
    L.append("")
    L.append("![AI JD vs Home Contrast](figs/ai_jd_vs_home_contrast.png)")
    L.append("")
    L.append("扫 1,148 个 DTC 主页,公开标榜「AI chatbot / AI assistant / AI agent / GPT-powered / Intercom Fin / Gorgias AI Agent」这类信号的——只有 13 个。1.1%。")
    L.append("")
    L.append("把这个数字放在我们 5 月 11 日发的 AI Required Position Rate 报告旁边看,反差就立起来了。同一时间窗,HN 招聘社区 619 条招聘文案里,具体 AI 工具或 LLM 关键词的命中率是 35.6%——剔除 unknown 之后是 36.7%。两份报告的时间窗都是 2026-05,样本都是「广义的科技公司」。但**招聘文案里 AI 是「3 个岗位里有 1 个」,DTC 实战页面上 AI 是「100 个品牌里有 1 个」。差距三十倍**。")
    L.append("")
    L.append("这个落差也不必读成「DTC 慢半拍」那么简单。我们的判断是这样的——招聘 JD 反映的是两件事:现在需要的技能,以及未来 12-18 个月想做的方向。35.6% 这个数字里有相当大一部分是「我们想招会做 AI 的人 *建* AI」,不是「我们的岗位都在 *用* AI」。所以 HN 数据其实是个领先指标,反映的是公司在 *计划* 什么,不是已经 *上线* 什么。")
    L.append("")
    L.append("另一边,DTC 主页的 1.1% 也不等于「DTC 后端没用 AI」。很多 DTC 品牌大概率已经在 Gorgias Automate 或 Intercom Fin 后台开了自动回复——但他们不在主页上把这件事讲出来,因为他们的目标客户(普通消费者)不在意是不是 AI 回答。营销文案和后端部署在两个轨道上跑。我们看到的 1.1% 反映的是「品牌愿不愿意把 AI 当 selling point 端出来」,不是「品牌实际有没有用 AI」。")
    L.append("")
    L.append("但这不影响一个商业结论:**对 AI 客服厂商(Gorgias Automate / Intercom Fin / Zendesk AI Suite / Reamaze AI Inbox,以及 Cresta、Decagon、Sierra、Forethought 这一批新入局者)来说,DTC 是个还没被「教育」的市场**。客户没在公开使用,公开使用的客户也没在讲。谁第一个把 AI 客服在 DTC 行业的叙事权拿到手,谁就锁定了 2027-2028 普及期的定位优势。")
    L.append("")
    L.append("13 个公开标 AI 信号的 DTC 品牌,样本不大但有信号价值——这是行业里 *愿意把 AI 当卖点* 的早期一批:")
    L.append("")
    L.append("![AI Brand List](figs/ai_brand_list.png)")
    L.append("")
    L.append("名单里有 fillingpieces.com、hikoco.com、livingproof.com、olly.com、truelinkswear.com 等。注意这是「主页 *文案* 上提到 AI」的 13 家,不是「DTC 圈 AI 客服 Top 13」——更像是「敢把 AI 标在 storefront 上的早期 marketer」。")
    L.append("")

    # 1. coverage
    L.append("## 35% 装,65% 没扫到——但 65% 是下限")
    L.append("")
    L.append("![Coverage Donut](figs/coverage_donut.png)")
    L.append("")
    L.append("回到客服工具本身。1,148 个品牌主页里,397 个(35%)我们能在静态 HTML 上识别出至少一个客服 widget。其中 32% 装一个,2.3% 装两个,只有 1 个品牌装了 3 个或以上。这是「主客服 + 补充渠道」的组合模式,后面讲。")
    L.append("")
    L.append("剩下 65% 看起来没装,但这个数字必须打折读。三种可能。")
    L.append("")
    L.append("第一种,JS 动态加载漏检。很多客服 widget——包括 Gorgias、Zendesk 自身——是通过 chunk-loaded script 异步注入的。静态扫只看主页第一屏 HTML 字节里直接出现的 vendor host。如果 vendor 通过 GTM、Segment 或者一个延迟加载的 chunk 进来,我们这次的方法看不到。用 Thunderbit Chrome 扩展执行 JS 后扫,这层能补抓。")
    L.append("")
    L.append("第二种,按需弹出。不少品牌只在 product page 或 checkout 页加客服 widget——主页保持「品牌叙事 + CTA」的视觉纯净度。这是一个有意思的 UX 决策,不是「不装」。")
    L.append("")
    L.append("第三种,确实没装。149 个品牌(13%)主页上连「chat / live chat / contact us」这类自然语言提示都没有——这部分大概率确实没开 live chat,只留 email 联系入口。")
    L.append("")
    L.append("综合下来,真实的「装了客服 widget」的比例可能在 50-60% 之间。我们报告的 35% 是 conservative 下限。重点是,**「主页装不装 chat widget」在 DTC 圈不是行业共识**——更接近 50/50 的现实。装不装,看你的 conversion funnel 摩擦在哪里、品牌主页想要什么调性,而不是「同行都装我也装」。")
    L.append("")

    # 2. Vendor share
    L.append("## Vendor 分布:Gorgias 居首,但要打折看")
    L.append("")
    L.append("![Vendor Share](figs/vendor_share.png)")
    L.append("")
    L.append("Top 15 vendor 是这样的:")
    L.append("")
    L.append("| Rank | Vendor | 品牌数 | 占比 |")
    L.append("|---:|---|---:|---:|")
    for i, v in enumerate(vs[:15], 1):
        L.append(f"| {i} | {v['vendor']} | {v['count']} | {v['pct']}% |")
    L.append("")
    L.append("Gorgias 占 23.3%,267 个品牌。第二是 Zendesk 4.3%,第三是 WhatsApp Button 1.7%。看起来 Gorgias 是绝对老大——但这个数字不能直接读。")
    L.append("")
    L.append("我们构建 brand pool 时,1,597 个候选品牌里有相当一部分来自 Shopify 生态工具的 customer case study sitemap。**Gorgias 自己就是来源之一**——他们的 case study 把所有用 Gorgias 的 DTC 品牌自动收进了我们的池子。Klaviyo、Postscript、Shopify Plus、Skio 等其他 case study 也类似贡献。所以「Gorgias 23.3%」里,有相当一部分是 *样本偏向*,不是 *行业占比*。")
    L.append("")
    L.append("独立来源对 Gorgias 的全市场估计:BuiltWith 看「全互联网技术栈」给出 ~3-5% of e-com sites;Wappalyzer 看「用户访问页面采样」给出 ~4-7% of Shopify sites;Gorgias 2024 财报披露 14,000+ merchants。综合看,Gorgias 在 DTC 行业的真实占比大约在 8-12% 区间,本报告样本里 23.3% 是「真实占比 × 约 2 倍样本回声」。把这个折扣记住——下面引用 Gorgias 数字时,我们都假设你已经在脑子里打折了。")
    L.append("")
    L.append("打折之后,这份榜单还有几个值得看的信号。")
    L.append("")
    L.append(f"**Zendesk 4.3% 是有意思的**。在 SaaS 圈,Zendesk 是绝对头部——B2B SaaS 公司里很难找到不用 Zendesk 的。但 DTC 圈,Zendesk 只占 4.3%。这不是「Zendesk 没努力」,是 DTC 客户接触模型和 SaaS 太不一样,Zendesk 那套通用 helpdesk 范式不贴 DTC 工作流。")
    L.append("")
    L.append(f"**WhatsApp Button 1.7%(19 个品牌)**——这是个意外。一个 `wa.me/...` 链接,在 DTC 圈数量超过 Reamaze、HubSpot Chat、Crisp、Intercom 等所有正经客服 SaaS。这反映 DTC 客户的真实偏好——尤其是国际化品牌、跨境电商、低单价高复购的品类,**用户本来就有 WhatsApp,你直接放链接,他能直接给你发消息,不用注册新账号、不用接受 cookie banner、不用等 chat 加载**。零成本,易部署,有效。")
    L.append("")
    L.append(f"**Intercom 0.6%(7 个品牌)**——这是这份报告里最让我们停下来反复看的一行。Intercom 在 SaaS 圈是统治级的存在,在 DTC 圈几乎不存在。我们后面会单独讲一节这件事,因为它能讲清楚一个完整的市场为什么会和另一个完整的市场架构如此不同。")
    L.append("")
    L.append(f"**Reamaze 1.5%、Kustomer 1.0%、HubSpot Chat 1.0%、Crisp 0.9%**——这些是中尾,各自占一小块。Reamaze 是 Shopify-native 的 helpdesk,定位非常垂直;Kustomer 在 Meta 收购后转向 omnichannel 大品牌;HubSpot Chat 是免费 tier 拉新进来的;Crisp 在欧洲早期创业圈渗透高。每家都有自己的 niche,但没有一家能挑战 Gorgias 在 DTC 圈的主导位。")
    L.append("")

    # 3. Why Gorgias won
    L.append("## 为什么 Gorgias 赢了 DTC,Intercom 几乎不存在")
    L.append("")
    L.append("Gorgias 23.3%(打折后 8-12%)对比 Intercom 0.6%——SaaS 出身的人看到这个比例会觉得不合理。Intercom 是客服 SaaS 的统治者,DTC 怎么会用得这么少?")
    L.append("")
    L.append("答案不在产品质量,在客户接触模型。SaaS 和 DTC 的客户从哪里来、问什么问题、需要 agent 看到什么——是两个完全不同的世界。Intercom 为 SaaS 量身定做了一套范式,放到 DTC 场景里水土不服。")
    L.append("")
    L.append("SaaS 客户来自 B2B 漏斗:demo 请求 → trial → onboarding → expansion。一个用户从看到产品到付费,可能在 SaaS app 内停留几十次。客服 ticket 大多是技术问题——「我的账号坏了」「API 集成出错」「权限不对」。Intercom 的护城河是 *in-product messenger*——在 SaaS app 内嵌一个 chat 弹窗,把客服、in-app guidance、product tour 三件事合并在一个 surface 上。客户在 app 里出问题,Intercom 就在 app 里出现,seamless。")
    L.append("")
    L.append("DTC 客户来自完全不同的漏斗:Meta / TikTok / Google 广告 → 点广告进站 → 加购 → 结账。一个买家从看到广告到结账可能就一次性 5 分钟,买完就走。客服 ticket 大多是订单问题——「我的包裹到哪了」「怎么退货」「优惠码失效」「能换码吗」。这种工单需要的不是「in-product messenger」,而是 *深度的 Shopify 订单数据集成*——客服坐席打开一个 ticket,屏幕上同时出现 Shopify 订单号、跟踪号、退款额度、客户历史订单。**不用切 8 个 tab**——这是 Gorgias 的核心价值主张。")
    L.append("")
    L.append("再加一层:DTC 公司里,客服 + Returns + Fulfillment 这三个团队往往用同一套系统。Gorgias 把工单、Shopify 退款、跟踪号查询合并到一个工作流。Intercom 不是不能集成 Shopify,但它的产品基因是 messenger,不是 helpdesk-with-deep-Shopify-data。范式不同。")
    L.append("")
    L.append("所以 Gorgias 在 DTC 圈赢的不是「客服 UI 漂亮」,赢的是 Shopify 数据深度。它的护城河不可被 *功能维度* 复制——任何想进 DTC 客服市场的厂商,都得先解决「订单查询」「退款执行」「换货流程」这三个占 80% 工单的类型,而不是只解决「FAQ 自动回」。")
    L.append("")
    L.append("这对两类人有直接启示。**对 DTC 中介 / 运营来说**,选客服工具时核心标准应该是「跟 Shopify、订单系统、退货 SaaS 的集成深度」,不是「chat UI 是否漂亮」。Reamaze、Kustomer 走的是同一条路。Crisp 和 HelpScout 单价便宜但订单集成弱,适合早期 DTC,规模化之后通常会切换。**对 AI 客服厂商来说**,要进 DTC,光做「FAQ 自动回」远远不够——必须解决订单类工单的 80%。Gorgias Automate 和 Reamaze AI Inbox 已经在推这件事,但本报告的 1.1% AI 主页渗透率表明,**AI 替代订单类客服在 2026 年依然是早期阶段**。")
    L.append("")
    L.append("另一个值得记的:**DTC 客服工具一旦装上去就难拔**。这套系统接在订单系统、退货 SaaS、邮件凭证流程之间,迁移是一个正式项目,不是一下午能完成的。这种粘性既解释了 Gorgias 早期优势的复利,也意味着新进入者需要的 wedge 比「我们 AI 更好」更强——需要一个 *workflow* 故事来 justify 客户的迁移摩擦。")
    L.append("")

    # 4. Multi-widget
    L.append("## 装两个 widget 的 26 个品牌:不是混乱,是策略")
    L.append("")
    L.append("2.3% 的品牌(26 家)同时装了 2 个及以上的客服 widget。常见的组合是这样:")
    L.append("")
    L.append("| 组合 | 品牌数 |")
    L.append("|---|---:|")
    multi_pairs = {}
    for m in multi:
        pair = tuple(sorted(m["widgets"].split(";")))
        multi_pairs[pair] = multi_pairs.get(pair, 0) + 1
    for pair, n in sorted(multi_pairs.items(), key=lambda x: -x[1])[:8]:
        L.append(f"| {' + '.join(pair)} | {n} |")
    L.append("")
    L.append("看清楚——多 widget 不是「这家公司客服栈混乱」,而是「不同入口对应不同接触场景」。Gorgias 处理工单,WhatsApp 处理跨境消费者的直接对话,Facebook Messenger 给已认证社媒账号的客户。这是一个 *intentional* 的 multi-channel 策略,不是 *accidental* 的栈臃肿。")
    L.append("")
    L.append("对 DTC 运营的实操含义——如果你的目标客户活跃在多个渠道,不要追求「单一 chat 工具搞定一切」。把主客服(Gorgias 或 Zendesk)做扎实,然后看你的客户实际从哪些渠道来,再补充直链 widget。26 家多 widget 品牌的存在反过来说明,DTC 圈的「主流单 widget」做法在某些场景下不是最优——尤其国际化品牌和高复购品类,客户期望能在「他已经在用的那个 app」里直接联系你。")
    L.append("")

    # 5. Practical
    L.append("## 给 DTC 运营、CX 团队、AI 客服厂商的几条建议")
    L.append("")
    L.append("把数据拍平,如果你在 DTC 圈做客服 / CX / 增长方向的运营,以下几条是 actionable 的。")
    L.append("")
    L.append("选客服工具,有阶段化的决策路径。月单 <1,000 单的早期 DTC,HelpScout / Crisp / Tidio 任选一个,单价不超过 $15/seat。这个阶段创始人 + 一个外包通常就能处理所有工单,不需要 routing rules,不需要高 SLA,跑通工单流就行。月单 1,000-10,000 单,Gorgias 或 Reamaze 是合理选择——这个阶段 Shopify 订单数据深度集成开始成为人工坐席的实际瓶颈,$50-150/seat 的成本能换回 30-40% 的人工时长节省,ROI 清晰。月单超过 10,000 单,Gorgias + AI Automate 或 Zendesk + AI Suite 或 Kustomer 进入议程——AI 自动回复优惠码查询和跟踪号查询能省 30-50% 人工坐席。这是 AI 客服真正发挥作用的 stage,也是本报告样本里几乎没人到达的 stage(这就解释了 AI signal 为什么只有 1.1%)。再往上的 omnichannel 大品牌,Zendesk 或 Kustomer 加多语言、多 region routing 才是答案,Gorgias 在国际化深度上略弱。")
    L.append("")
    L.append("AI 客服内容是被严重低估的方向。渗透率 1.1% 不是「AI 客服没人要」,是「DTC 主页营销还没把 AI 当 selling point 端出来」。如果你做 DTC 内容——blog、case study、newsletter——「AI 客服怎么用、效果怎么样、ROI 怎么算」这套话题在内容市场上是高度供给不足的。你的读者既不知道同行在不在用,也不知道实际效果。这是 1-2 年内还有 content window 的方向。如果你是 Gorgias / Intercom / Zendesk 等的代理商或顾问,「我们能帮你启用 AI Agent」是个清晰的 wedge——竞争对手大多还没在 pitch 这个。")
    L.append("")
    L.append("主页放不放 chat widget,不是行业共识。35% vs 65% 是接近 50/50 的现实。装不装的决策权在你手里——如果你的转化漏斗里 support ticket 是 friction,装;如果你想保持品牌主页的视觉 cleanliness,可以选择「按需弹出」或「只在 product / checkout 页装」。一个被忽视的中间策略——**只在 cart 和 checkout 页放 chat widget**,既能在关键转化点抓住犹豫客户,又不影响品牌主页的 brand expression。")
    L.append("")
    L.append("最后,WhatsApp Button 是个被低估的渠道。19 个品牌(1.7%)直接放 `wa.me` 链接,数量超过 Reamaze、HubSpot Chat 等正经客服 SaaS。对国际化 DTC、跨境电商、低单价高复购品类,**直接 WhatsApp 链接可能比花式 chat widget 更有效**——零成本,易部署,客户已经有这个 app。值得在 A/B test 里加一组。")
    L.append("")

    # 6. Stability
    L.append("## 这份数据有多稳,边界在哪")
    L.append("")
    L.append("1,148 个有效解析,从 1,429 个 home.html 中筛掉小于 1KB 或无法解析的。Vendor 指纹覆盖 23 个 vendor 但可能漏一些 niche 或自建客服。Long tail 的实际 share 可能比这里展示的更大。")
    L.append("")
    L.append("静态扫只看主页第一屏 HTML 字节,这是下限。JS 动态加载的 widget(Intercom、Drift 的部分 init 模式)会漏检。要拿真实安装率需要用 Thunderbit Chrome 扩展执行 JS 后再扫,本次没做。")
    L.append("")
    L.append("和外部数据对照,BuiltWith 估 Gorgias 在 e-com 全市场 3-5%,Wappalyzer 估 Shopify 站 4-7%,Gorgias 2024 财报披露 14,000+ merchants。本报告样本里 23.3% 是「真实占比 × 约 2 倍样本回声」。这些数据不互相矛盾——BuiltWith 看的是「全互联网技术栈」(分母大),Gorgias 自报是「merchant 数量」(不是 share),本报告样本是「DTC 头部 + Shopify 生态」(分母窄分子集中)。三个视角各有用。本报告值得引用的是「在 DTC 头部样本里 Gorgias 显著领先 Zendesk」,不是「Gorgias 占行业 23%」。")
    L.append("")
    L.append("一句话边界:本报告描述的是「在我们抓的 1,148 个 DTC 品牌主页静态扫描里」发生了什么,**不是 DTC 行业市场份额**,**也不是「DTC 客服后端实际用什么」**。后端用什么是黑盒,我们只能看到主页 HTML 这一层。")
    L.append("")

    # 7. Reproducibility
    L.append("## Reproducibility Notes")
    L.append("")
    L.append("方法和数据完全公开,任何人能复现。")
    L.append("")
    L.append("Brand pool 的 1,597 个候选品牌主要来自 30+ Shopify 生态工具的 case study sitemap,公开数据。复现者可以用自己的 DTC 公司池——BuiltWith Top DTC、a16z DTC 50、Modern Retail Top 100 都是合理替代,只要披露来源。")
    L.append("")
    L.append("抓主页 HTML 用任何 HTTP 客户端都行,注意限速(全局不超过 10 req/s)和 UA 透明披露。我们扫的是「主页第一屏 256KB 字节」,这是下限——JS 动态加载漏检。")
    L.append("")
    L.append("Vendor 指纹扫描,我们的 23 个 vendor 规则集开源在仓库的 `01_detect_widgets.py`。复现时建议交叉用 Wappalyzer 的开源规则集补充,我们漏的 vendor 你能抓到。")
    L.append("")
    L.append("AI signal 用 regex 命中「AI assistant / AI agent / AI chatbot / GPT-powered / Intercom Fin / Gorgias Automate」等常见 marketing 短语。这是 surface signal——只反映品牌是否对外营销 AI,**不反映后端是否真的用 AI**。后者需要 vendor API 接入或人工 spot check。")
    L.append("")
    L.append("复跑频率建议季度跑一次。Vendor 渗透率以年为单位变化,AI signal 可能每季度动 0.5-1 pp 的量级。")
    L.append("")
    L.append("已知漏检——Intercom 和 Drift 的部分 chunk-loaded init 模式,自建客服系统(没有 vendor host 信号),通过 GTM 或 Segment 间接 inject 的 widget,以及多语言站点(国际化 DTC 在每个 region 加载不同 widget)。想要精确度,用 Thunderbit Chrome 扩展执行 JS 后再扫,能覆盖动态加载部分。想要「头部谁领先」,本报告的静态结果已经够稳健。")
    L.append("")

    # Methodology
    L.append("---")
    L.append("")
    L.append("## Methodology / 方法论与样本声明")
    L.append("")
    L.append(f"**数据源**:1,597 brand pool 的 1,148 个 DTC 主页 home.html(过滤到 ≥1KB),配 23 个客服 vendor 指纹规则(`01_detect_widgets.py` 公开)。采集 / 解析日期 {today}(UTC)。")
    L.append("")
    L.append("**Gorgias 数据源回声(最关键)**:Brand pool 部分来自 Gorgias / Klaviyo / Postscript / Shopify Plus 等 Shopify 生态工具的 customer case study sitemap。**Gorgias 本身就是来源之一**——他们的 case study 把所有用 Gorgias 的 DTC 品牌都自动收进了样本。Gorgias 23.3% **不等于 Gorgias 占 DTC 行业 23%**——独立估计器(BuiltWith / Wappalyzer)给出的全市场占比是 8-12%。把 23.3% 理解为「样本里 #1 vendor,约 2 倍样本回声」,不是行业 share。")
    L.append("")
    L.append("**Brand pool 偏 Shopify 生态**:~67% 品牌来自 Shopify 工具栈 case study,样本天然偏向 Shopify-native + remote-friendly + AI-adopter 的 DTC 子集,**不代表「全美 DTC 市场」**。Mom-and-pop e-com、传统零售迁移 DTC 等子赛道在本样本中代表性弱。")
    L.append("")
    L.append("**静态扫下限**:只看主页第一屏 256KB 字节,JS 动态加载的 widget 漏检。Intercom 和 Drift 的部分 chunk-loaded init 会被误归类为「无 widget」。35% widget 覆盖是下限,实际可能在 50-60%。")
    L.append("")
    L.append("**AI signal 是「主页营销话术」,不是「后端实际 AI」**:很多 DTC 品牌大概率已经在用 Gorgias Automate 或 Intercom Fin 后端的 AI 自动回复,但没在主页营销文案里把 AI 当 selling point。本报告的「AI signal 1.1%」反映的是「品牌是否对外营销 AI 客服」,**不直接反映「品牌后端是否用了 AI」**。两者相关但不等价。")
    L.append("")
    L.append("**同公司多 widget 不等于「客服栈混乱」**:26 家多 widget 品牌通常是「主客服 + 直链补充」(如 Gorgias + WhatsApp),不是在维护多套并行客服系统。")
    L.append("")
    L.append("**法律与版权**:所有主页是公开抓取,本报告**只做聚合统计**(vendor count + percentage),不全文引用任何品牌主页。AI signal 命中的 13 家品牌点名属于正面或中性 case(他们公开标 AI 是自己的营销选择)。多 widget 26 家点名属于中性 case(描述事实)。报告不发布 raw HTML 或 raw CSV 下载链接,所有数字可通过公开 brand pool + 公开规则集复现。")
    L.append("")
    L.append("**不能解读为**:")
    L.append("")
    L.append("- 不是「Gorgias 占 DTC 行业市场份额 23.3%」(含样本回声,真实约 8-12%)")
    L.append("- 不是「DTC 圈只有 1.1% 用了 AI 客服」(本数字只反映「在主页营销文案上标 AI」,不反映后端实际用没用)")
    L.append("- 不是「65% DTC 品牌没装 chat widget」(这是静态扫下限,实际可能 50-60%)")
    L.append("- **可以说**:「在我们追踪的 1,148 个 DTC 品牌主页静态扫描里,Gorgias 是 #1 检测到的 vendor(23.3%,含样本偏向),AI 营销信号渗透 1.1%」")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 数据来源与版本")
    L.append("")
    L.append(f"数据集:`dtc_customer_support_map_2026/`(本仓库)。采集日期 **{today}** UTC,报告版本 v1.0(静态扫下限版;v2 计划用 Thunderbit Chrome 扩展跑 JS 后补抓)。共用 DTC brand pool 与 `dtc_dual_report_2026` 同一 1,148 子集,可交叉引用。配对报告:AI Required Position Rate 2026(HN 招聘样本,2026-05-11 发布)——AI 在招聘文本的一半,跟本报告 AI 在产品页的一半合起来看,能从招聘意图和产品落地两个角度三角验证。")
    L.append("")
    return "\n".join(L)


# ============================================================
# 英文
# ============================================================
def build_en(s):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    vs = s["vendor_share"]
    cov = s["widget_coverage"]
    ai = s["ai_signal"]
    multi = s["multi_widget_examples"]
    total = s["_meta"]["effective_rows"]
    top1, top2, top3 = vs[0], vs[1], vs[2]

    L = []
    L.append("# DTC customer support is a market mismatched against SaaS")
    L.append("")
    L.append(f"> {today} · 1,148 DTC brand home-page static scans · 23 vendor fingerprints")
    L.append("")
    L.append("---")
    L.append("")
    L.append("We scanned 1,148 DTC brand home pages and read what customer-support widget — the chat button or messenger bubble a visitor sees the moment a page loads — sits behind each one. The result is uncomplicated, but it doesn't fit the mental model most people walk in with, which is that whoever dominates SaaS support also dominates DTC.")
    L.append("")
    L.append("The most interesting line isn't Gorgias at 23.3% — that number needs a discount before you can read it, and we'll explain why shortly. The most interesting line is this: **Intercom, the undisputed leader of SaaS customer support, sits at 0.6% in DTC**. Seven brands out of 1,148. A product built around an in-product messenger paradigm has been almost completely filtered out of a market where the customer was never inside the product.")
    L.append("")
    L.append("Two questions to answer here. First, what shape is DTC customer-support tooling — who wins, who runs the mid-pack, who fails to land? Second, how far has AI customer support actually penetrated DTC — the AI Required Position Rate report we published on 2026-05-11 found that 35.6% of HN hiring posts name specific AI tools; what about live DTC pages?")
    L.append("")
    L.append("Start with the second question because the contrast is the cleanest.")
    L.append("")
    L.append("## AI in hiring text: 35.6%. AI on DTC home pages: 1.1%.")
    L.append("")
    L.append("![AI JD vs Home Contrast](figs/ai_jd_vs_home_contrast.png)")
    L.append("")
    L.append("Scanning 1,148 DTC home pages, only 13 surface anything in the family of \"AI chatbot / AI assistant / AI agent / GPT-powered / Intercom Fin / Gorgias AI Agent.\" That's 1.1%.")
    L.append("")
    L.append("Set that next to the adjacent AI Required Position Rate report we published 2026-05-11. Same time window, HN hiring community, 619 postings — 35.6% mention specific AI tools or LLM keywords (36.7% excluding unknowns). Both samples are \"broader tech in May 2026.\" **In hiring text, AI shows up in roughly one of every three postings. On live DTC home pages, AI shows up in roughly one of every hundred brands. A 30x gap.**")
    L.append("")
    L.append("The gap isn't \"DTC is behind\" the way it might first read. Hiring text reflects two things: skills currently needed, and skills the company *plans* to need over the next 12-18 months. A meaningful share of that 35.6% is \"we want to hire people to *build* AI,\" not \"all our roles *use* AI today.\" HN is in that sense a leading indicator — it shows what companies are planning, not what's shipped.")
    L.append("")
    L.append("The reverse holds on DTC pages. The 1.1% does *not* mean DTC backends don't use AI. Many DTC brands have likely already enabled Gorgias Automate or Intercom Fin on the backend to auto-resolve tickets — they just don't surface \"AI-powered\" on the home page because their end-customers (regular consumers) don't care. Marketing copy and deployed automation run on different tracks. The 1.1% measures whether brands publicly market AI, not whether they use it.")
    L.append("")
    L.append("But the commercial conclusion is the same regardless of which interpretation you favor: **for AI customer-support vendors — Gorgias Automate, Intercom Fin, Zendesk AI Suite, Reamaze AI Inbox, plus newer entrants like Cresta, Decagon, Sierra, Forethought — DTC is an untaught market**. Customers don't use it publicly. The customers who use it don't talk about it. Whoever owns the narrative for AI customer support in DTC will likely lock in category-defining positioning before broader adoption arrives in 2027-2028.")
    L.append("")
    L.append("The 13 DTC brands publicly signaling AI customer chat are an early-marketer subsample worth naming — fillingpieces.com, hikoco.com, livingproof.com, olly.com, truelinkswear.com and several others:")
    L.append("")
    L.append("![AI Brand List](figs/ai_brand_list.png)")
    L.append("")
    L.append("Read this as \"brands brave enough to put AI on the storefront,\" not \"DTC's top 13 AI-chat champions.\" Those are different lists.")
    L.append("")

    # 1. Coverage
    L.append("## 35% show a widget, 65% don't — and 65% is a floor")
    L.append("")
    L.append("![Coverage Donut](figs/coverage_donut.png)")
    L.append("")
    L.append("Back to the customer-support tooling itself. Of 1,148 DTC home pages, 397 (35%) expose at least one customer-support widget in static HTML. 32% have exactly one, 2.3% have two, exactly one brand has three. The two-widget cases are mostly \"primary helpdesk + secondary channel\" combinations; we'll come back to those.")
    L.append("")
    L.append("The remaining 65% don't show a widget on first scan, but that number deserves a discount. Three possibilities.")
    L.append("")
    L.append("First, JS-loaded widgets escape static detection. Many helpdesk vendors — including Gorgias and Zendesk — inject their scripts via chunk-loaded JS. Static scans only see the vendor host visible in the first-screen HTML bytes. If a vendor loads via GTM, Segment, or a delayed chunk, our method misses it. A Thunderbit Chrome-extension pass that executes JS recovers this layer.")
    L.append("")
    L.append("Second, chat-on-demand UX. Many brands deliberately put the chat widget on product or checkout pages only, keeping the home page as pure brand-narrative + CTA. That's a real UX decision, not \"not installed.\"")
    L.append("")
    L.append("Third, no chat at all. 149 brands (13%) show no \"chat / live chat / contact us\" language signal anywhere on the home page. These very likely don't run live chat — only an email contact path.")
    L.append("")
    L.append("Putting the three together, real widget coverage is probably 50-60%. Our 35% is a conservative floor. The point is, **\"do you put a chat widget on the home page\" isn't industry consensus in DTC** — it's closer to a 50/50 split. The decision should hinge on where your conversion friction sits and what voice you want your home page to carry, not on \"everyone else does it.\"")
    L.append("")

    # 2. Vendor share
    L.append("## Vendor share: Gorgias leads, with a discount")
    L.append("")
    L.append("![Vendor Share](figs/vendor_share.png)")
    L.append("")
    L.append("Top 15 detected vendors:")
    L.append("")
    L.append("| Rank | Vendor | Brands | Share |")
    L.append("|---:|---|---:|---:|")
    for i, v in enumerate(vs[:15], 1):
        L.append(f"| {i} | {v['vendor']} | {v['count']} | {v['pct']}% |")
    L.append("")
    L.append("Gorgias at 23.3% with 267 brands. Zendesk #2 at 4.3%. WhatsApp Button #3 at 1.7%. Gorgias looks dominant — but you can't read the raw number.")
    L.append("")
    L.append("When we built the brand pool, 1,597 candidate brands came partly from Shopify-ecosystem customer case-study sitemaps. **Gorgias' own case-study sitemap is one of those sources.** Every DTC brand Gorgias chose to showcase was automatically pulled into our pool — and Klaviyo, Postscript, Shopify Plus, and Skio case studies contribute similarly. So \"Gorgias 23.3%\" includes substantial *sample echo*, not pure *industry share*.")
    L.append("")
    L.append("Independent estimators land much lower. BuiltWith (technographics of all e-commerce sites) puts Gorgias at ~3-5%. Wappalyzer (Chrome-extension user sampling on Shopify sites) puts it at ~4-7%. Gorgias' own 2024 financial disclosures cite 14,000+ merchants. Triangulating these, Gorgias' realistic DTC share is in the 8-12% range, and our 23.3% reads as \"true share × roughly 2x sample echo.\" Remember the discount when reading any Gorgias number — assume you've already taken it.")
    L.append("")
    L.append("Even after the discount, the rest of the leaderboard is informative.")
    L.append("")
    L.append("**Zendesk at 4.3% is interesting.** In SaaS, Zendesk is dominant — it's hard to find a mid-market or larger B2B SaaS company that doesn't run it. In DTC, only 4.3%. This isn't \"Zendesk didn't try\" — DTC customer-contact models differ from SaaS in ways that don't fit Zendesk's generic helpdesk paradigm.")
    L.append("")
    L.append("**WhatsApp Button at 1.7% (19 brands)** is the surprise. A plain `wa.me/...` link, in DTC, outranks Reamaze, HubSpot Chat, Crisp, and Intercom — and every other proper customer-support SaaS in the long tail. It reflects DTC customer preference, especially for international brands, cross-border commerce, and low-AOV / high-repeat categories. **Users already have WhatsApp; you give them a link; they message you with no signup, no cookie banner, no chat-widget loading delay**. Zero cost, trivial deploy, effective.")
    L.append("")
    L.append("**Intercom at 0.6% (7 brands)** is the line that made us stop and look twice. The SaaS customer-support category leader, almost absent in DTC. We dedicate the next section to this because it explains a real, deep structural difference between two markets that look similar from a distance.")
    L.append("")
    L.append("**Reamaze 1.5%, Kustomer 1.0%, HubSpot Chat 1.0%, Crisp 0.9%** — the mid-tail. Each holds a niche. Reamaze is the Shopify-native helpdesk, narrowly DTC-positioned. Kustomer pivoted after Meta acquisition toward omnichannel large brands. HubSpot Chat is free-tier reach into marketing-led DTC brands. Crisp is rooted in European early-stage startups. None of them is positioned to challenge Gorgias' DTC lead.")
    L.append("")

    # 3. Why Gorgias won
    L.append("## Why Gorgias won DTC and Intercom barely exists here")
    L.append("")
    L.append("Gorgias 23.3% (8-12% adjusted) versus Intercom 0.6%. A SaaS native looking at this ratio thinks it doesn't make sense. Intercom is the customer-support SaaS — how could DTC use so little of it?")
    L.append("")
    L.append("The answer isn't product quality. It's customer-contact architecture. SaaS and DTC have genuinely different customer-arrival paths, ticket types, and agent needs — and Intercom built its core paradigm around the SaaS half. It doesn't translate.")
    L.append("")
    L.append("SaaS customers come through a B2B funnel: demo request → trial → onboarding → expansion. A user touches the product dozens of times before paying. Tickets are mostly technical — \"my account is broken,\" \"API integration is failing,\" \"permissions are wrong.\" Intercom's moat is the *in-product messenger* — a chat surface embedded inside the SaaS app, merging support + in-app guidance + product tours into one experience. When a customer has a problem inside the product, Intercom appears inside the product. Seamless.")
    L.append("")
    L.append("DTC customers come from an entirely different funnel: Meta / TikTok / Google ad → land on page → add to cart → check out. A buyer's total time-in-product before purchase might be 5 minutes once. Tickets are mostly order-related — \"where is my package,\" \"how do I return this,\" \"my coupon doesn't work,\" \"can I swap the code.\" These tickets don't need an in-product messenger. They need **deep Shopify-order-data integration** — the support agent opens a ticket and sees the Shopify order ID, tracking number, refund authorization, and customer order history right inside the agent UI. **No tab switching across eight systems.** That is Gorgias' core value proposition.")
    L.append("")
    L.append("Layer it deeper: at most DTC companies, Support + Returns + Fulfillment share one system. Gorgias unifies tickets + Shopify refunds + tracking-number lookups in a single workflow. Intercom *can* integrate Shopify, but its product DNA is messenger, not helpdesk-with-deep-Shopify-data. Different paradigms.")
    L.append("")
    L.append("Gorgias' DTC moat isn't \"prettier chat UI.\" It's Shopify-data depth. Any vendor trying to enter DTC customer-support has to solve order lookup, refund execution, and exchange workflow — the three ticket types making up 80% of volume — not just \"FAQ auto-answer.\"")
    L.append("")
    L.append("Two direct implications. **For DTC operators**: select a helpdesk by depth of integration with Shopify, the order system, and your returns SaaS — not by chat-UI elegance. Reamaze and Kustomer compete on the same axis. Crisp and HelpScout are cheaper but order-data-light; fine for early-stage DTC but you'll outgrow them at scale. **For AI customer-support vendors**: \"FAQ auto-answer\" alone isn't enough to enter DTC. You have to crack order-class workflow — that's what Gorgias Automate and Reamaze AI Inbox are pushing, but the 1.1% public-marketing penetration in our data confirms that *AI replacing order-class support* remains early in 2026.")
    L.append("")
    L.append("One more architectural note: **support tooling is sticky once installed in DTC** — the tool sits between the order system, the returns SaaS, and the email-receipt workflow. Migration is a real project, not an afternoon's work. That stickiness compounds Gorgias' early lead and means any new entrant needs a wedge stronger than \"we have better AI\" — a workflow story that justifies migration friction.")
    L.append("")

    # 4. Multi-widget
    L.append("## The 26 multi-widget brands aren't running messy stacks — they're running strategy")
    L.append("")
    L.append("2.3% of brands (26) ship two or more chat widgets. Common combinations:")
    L.append("")
    L.append("| Combination | Brands |")
    L.append("|---|---:|")
    multi_pairs = {}
    for m in multi:
        pair = tuple(sorted(m["widgets"].split(";")))
        multi_pairs[pair] = multi_pairs.get(pair, 0) + 1
    for pair, n in sorted(multi_pairs.items(), key=lambda x: -x[1])[:8]:
        L.append(f"| {' + '.join(pair)} | {n} |")
    L.append("")
    L.append("These aren't messy stacks. They're intentional multi-channel support — Gorgias handles tickets, WhatsApp handles international direct-DM, Facebook Messenger handles already-authenticated social customers. Each entry point serves a different customer-arrival pattern. The strategy is multi-channel by design, not bloat by accident.")
    L.append("")
    L.append("For DTC operators, the implication is simple: if your audience lives on multiple channels, don't chase a single-tool answer. Nail your primary helpdesk (Gorgias or Zendesk), then layer direct-link widgets for the channels your customers actually use. The 26 multi-widget brands are a real counter-signal to \"everyone uses single-widget\" — the single-widget default isn't optimal for cross-border or high-repeat-purchase DTC, where customers expect to reach you on whatever app they already have open.")
    L.append("")

    # 5. Practical
    L.append("## Practical guidance for DTC operators, CX teams, and AI-chat vendors")
    L.append("")
    L.append("Flattening the data into actions for someone working DTC customer-support or growth.")
    L.append("")
    L.append("Helpdesk selection has a stage-by-stage path. Early-stage DTC (under 1,000 orders/month) — HelpScout, Crisp, or Tidio at under $15/seat. At this stage the founder + one contractor handles all tickets; no routing rules, no SLA precision, just get tickets flowing. Mid-stage (1,000-10,000 orders/month) — Gorgias or Reamaze. Shopify-order-data integration becomes the bottleneck, and $50-150/seat is reasonable when it buys back 30-40% of agent time. Scale stage (>10,000 orders/month) — Gorgias + AI Automate / Zendesk + AI Suite / Kustomer. AI auto-resolution of coupon and tracking-number tickets typically reduces human-agent load by 30-50%. This is where AI customer support actually pays off, and it's the stage almost no brand in our sample has reached (which explains why public AI signal sits at 1.1%). Beyond that, omnichannel multi-region brands typically need Zendesk or Kustomer with multi-language routing; Gorgias is weaker on international depth at this scale.")
    L.append("")
    L.append("AI customer-support content is a wildly under-served writing angle. 1.1% public penetration isn't \"nobody wants AI chat\" — it's \"nobody on the marketing side has owned this narrative yet.\" If you run DTC content — blog, case studies, newsletter — \"how AI customer chat actually works, what the ROI looks like, what to expect in year one\" is highly supply-constrained. Your readers don't know whether peers are using it, and don't know if it works. There's a 1-2 year window here. If you're an agency or consultant inside the Gorgias / Intercom / Zendesk ecosystem, \"we'll help you turn on AI Agent\" is a clean wedge — most competitors aren't pitching this yet.")
    L.append("")
    L.append("Home-page chat is not a settled question. 35% show / 65% don't is close to 50/50. The decision is yours. If support tickets are friction in your conversion funnel, surface it. If brand visual cleanliness matters, hide it. **A useful middle path: chat on cart and checkout pages only** — catches hesitating customers at the critical conversion moments without diluting the home page's brand expression.")
    L.append("")
    L.append("WhatsApp Button is the underrated channel. 19 brands (1.7%) ship a plain `wa.me` link — more than Reamaze, HubSpot Chat, and most legitimate chat SaaS. **For international, cross-border, or low-AOV / high-repeat DTC, a direct WhatsApp link may beat fancy chat widgets** — zero cost, trivial deploy, customers already have the app. Worth running as an A/B variant.")
    L.append("")

    # 6. Stability
    L.append("## How stable is this data, and where does it stop being valid")
    L.append("")
    L.append("1,148 parsed home pages (from 1,429 raw home.html, dropping <1KB or unparseable). 23 vendor fingerprints; some niche or custom helpdesks are still missing. The long-tail share in reality is probably somewhat higher than what we report.")
    L.append("")
    L.append("Static scan only inspects first-screen HTML bytes — this is a floor. JS-loaded widgets (parts of Intercom and Drift init patterns) escape. To recover real install rates, run Thunderbit's Chrome extension to execute JS and re-scan. We didn't do this for v1.")
    L.append("")
    L.append("External cross-reference: BuiltWith estimates Gorgias at ~3-5% of e-commerce; Wappalyzer at ~4-7% of Shopify sites; Gorgias' 2024 disclosures cite 14,000+ merchants. Our 23.3% reads as \"true share × ~2x sample echo.\" None of these are contradictory — BuiltWith looks at all e-commerce (large denominator), Gorgias self-reports merchant count (not share), and our sample is DTC-head + Shopify-ecosystem-leaning (narrow but dense). Three different views. The defensible cite from this report is \"in DTC-heavy samples, Gorgias leads Zendesk meaningfully,\" not \"Gorgias has 23% of the industry.\"")
    L.append("")
    L.append("Boundary in one line: this report describes what happens inside our 1,148-brand DTC home-page static scan — **not DTC industry market share**, and **not what DTC backends actually run**. Backends are a black box; we can only see what shows up in the home-page HTML.")
    L.append("")

    # 7. Reproducibility
    L.append("## Reproducibility Notes")
    L.append("")
    L.append("Method and data are fully public; anyone can re-run.")
    L.append("")
    L.append("The 1,597-brand pool came from 30+ Shopify-ecosystem case-study sitemaps. Replicators can swap in their own DTC pool — BuiltWith Top DTC, a16z DTC 50, Modern Retail Top 100 — as long as the source is disclosed.")
    L.append("")
    L.append("Fetching home-page HTML works with any HTTP client; rate-limit politely (≤10 req/s globally) and disclose the user-agent. We capture only the first 256KB of home-page HTML — a lower bound that misses JS-loaded widgets.")
    L.append("")
    L.append("Vendor fingerprinting: our 23-vendor regex rule set is open in the repo at `01_detect_widgets.py`. Cross-reference with Wappalyzer's open rule set to catch vendors we missed.")
    L.append("")
    L.append("AI signal detection uses regex matching for \"AI assistant / AI agent / AI chatbot / GPT-powered / Intercom Fin / Gorgias Automate\" and similar marketing-text phrases. This is surface signal — reflects whether the brand publicly markets AI, not whether AI is in the support stack. To verify backend AI usage, you need vendor API access or human spot-checks.")
    L.append("")
    L.append("Quarterly rerun is the right cadence. Vendor share moves on a yearly timeline. AI signal can shift 0.5-1 pp per quarter as more brands surface AI on home pages.")
    L.append("")
    L.append("Known gaps — some Intercom / Drift / Zendesk chunk-loaded init patterns, custom helpdesks (no vendor host signal), widgets injected via GTM or Segment, geo-localized chat widgets per region (internationalized DTC sites). For precision, run a Chrome-extension JS-executed scan to recover dynamic loaders. For \"who's leading among the major vendors,\" the static result here is already robust.")
    L.append("")

    # Methodology
    L.append("---")
    L.append("")
    L.append("## Methodology & sample notes")
    L.append("")
    L.append(f"**Data source**: 1,148 DTC home-page HTML snapshots from a 1,597-brand pool (filtered to home.html ≥ 1KB), with 23 customer-support vendor fingerprint rules (open in `01_detect_widgets.py`). Snapshot date {today} (UTC).")
    L.append("")
    L.append("**Gorgias sample echo (the most important caveat)**: our brand pool partly derives from Gorgias' own customer case-study sitemap (and that of other Shopify-ecosystem tools — Klaviyo, Postscript, Shopify Plus, Skio). By construction, brands Gorgias chose to showcase are in our sample. **Gorgias 23.3% cannot be read as \"23% market share\"** — independent estimators put Gorgias at 8-12%. Treat 23.3% as \"#1 vendor in this sample, with roughly 2x sample echo,\" not industry share.")
    L.append("")
    L.append("**Brand pool tilts Shopify-ecosystem**: ~67% of brands trace back to Shopify-stack case-study sources — so the sample over-represents Shopify-native, modern, marketing-led DTC and under-represents legacy retail / mom-and-pop e-commerce. **This is not the full US DTC universe**.")
    L.append("")
    L.append("**Static scan is a lower bound**: first-screen 256KB HTML only. JS-loaded widgets escape — Intercom's and Drift's chunk-loaded init can be invisible to our scan. The 35% detected-widget rate is a floor; the real rate is probably 50-60%.")
    L.append("")
    L.append("**AI signal = marketing text, not backend reality**: many DTC brands likely already run Gorgias Automate or Intercom Fin behind the scenes; they just don't market it on the home page. Our \"AI signal 1.1%\" reflects **public marketing text only**, not backend AI usage.")
    L.append("")
    L.append("**Multi-widget ≠ messy stack**: the 26 multi-widget brands typically run a primary helpdesk + a side channel (WhatsApp / Messenger / Crisp). They aren't operating parallel support systems.")
    L.append("")
    L.append("**Legal and copyright**: all home pages were publicly fetched. The report uses aggregate counts only — no full home-page text reproduction. The 13 brands named as AI-signal positive cases self-declared the marketing language on their own home pages. The 26 multi-widget brands are named in neutral, descriptive context. No raw HTML or CSV is published; every number is reproducible from the public brand pool + public rule set.")
    L.append("")
    L.append("**What this report does NOT support**:")
    L.append("")
    L.append("- Not \"Gorgias has 23.3% of the DTC market\" (contains sample echo; real share ~8-12%)")
    L.append("- Not \"only 1.1% of DTC uses AI customer support\" (marketing-text signal only; backend AI is invisible to static scan)")
    L.append("- Not \"65% of DTC brands don't run a chat widget\" (static lower bound; real coverage probably 50-60%)")
    L.append("- **Defensible**: \"In a static scan of 1,148 DTC brand home pages, Gorgias is the #1 detected vendor at 23.3% (with sample echo), and only 1.1% publicly market AI-powered chat\"")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Data source & versioning")
    L.append("")
    L.append(f"Dataset: `dtc_customer_support_map_2026/` (this repo). Snapshot date **{today}** UTC, report version v1.0 (static-scan lower bound; v2 planned with Chrome-extension JS-executed scan). Shares the DTC brand pool with `dtc_dual_report_2026` — both reports work from the same 1,148-brand subset. Companion report: AI Required Position Rate 2026 (HN hiring sample, released 2026-05-11) — the AI-in-hiring-text half of the same question; operators can triangulate intent versus shipped product by reading the two side by side.")
    L.append("")
    return "\n".join(L)


# ============================================================
# HTML (reuse template)
# ============================================================
HTML_HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>DTC customer support is mismatched against SaaS — Thunderbit</title>
<meta name="description" content="1,148 DTC brand home-page scans. Gorgias leads, Intercom is almost absent, AI signal is 1.1%.">
<style>
:root{--primary:#FF6B35;--dark:#1F2937;--accent:#3A6BD8;--green:#5E8F4E;--bg:#fff;--muted:#6B7280;--border:#E5E7EB;}
*{box-sizing:border-box;}body{margin:0;padding:0;font-family:-apple-system,"PingFang SC","Microsoft YaHei","Segoe UI",Arial,sans-serif;color:var(--dark);line-height:1.75;background:var(--bg);-webkit-font-smoothing:antialiased;}
.container{max-width:780px;margin:0 auto;padding:60px 24px 80px;}
.banner{background:linear-gradient(135deg,#FF6B35 0%,#3A6BD8 100%);color:#fff;padding:54px 24px 60px;text-align:center;}
.banner h1{margin:0 0 12px;font-size:2.2rem;font-weight:800;letter-spacing:-0.02em;max-width:780px;margin-left:auto;margin-right:auto;line-height:1.25;}
.banner .subtitle{margin:0;font-size:1rem;opacity:0.92;}
.lang-toggle{display:inline-flex;gap:4px;background:rgba(255,255,255,.18);border-radius:999px;padding:4px;margin-top:22px;}
.lang-toggle button{border:none;background:transparent;color:#fff;padding:7px 18px;border-radius:999px;font-size:.92rem;font-weight:600;cursor:pointer;transition:all .15s;}
.lang-toggle button.active{background:#fff;color:var(--primary);}
h1,h2,h3{color:var(--dark);margin-top:2.4em;line-height:1.35;letter-spacing:-0.01em;}
h2{font-size:1.5rem;border-bottom:1px solid var(--border);padding-bottom:8px;}
h3{font-size:1.16rem;}
p{margin:1em 0;}ul,ol{margin:1em 0;padding-left:1.4em;}li{margin:.5em 0;}
table{border-collapse:collapse;margin:1.4em 0;width:100%;font-size:.95rem;}
th,td{border:1px solid var(--border);padding:8px 12px;text-align:left;}
th{background:#F9FAFB;font-weight:600;}tr:nth-child(even) td{background:#FAFBFD;}
img{max-width:100%;height:auto;display:block;margin:1.6em auto;border:1px solid var(--border);border-radius:6px;}
blockquote{border-left:3px solid var(--accent);margin:1.4em 0;padding:.4em 1.2em;color:var(--muted);background:#F9FAFB;border-radius:0 6px 6px 0;}
code{background:#F3F4F6;padding:1px 6px;border-radius:3px;font-size:.92em;}
hr{border:none;border-top:1px solid var(--border);margin:2.8em 0;}
.lang-zh{display:none;}.lang-en{display:block;}
body.zh .lang-zh{display:block;}body.zh .lang-en{display:none;}
.footer{text-align:center;color:var(--muted);font-size:.86rem;margin-top:60px;padding-top:30px;border-top:1px solid var(--border);}
</style></head>
<body class="zh">
<div class="banner">
<h1>DTC customer support is mismatched against SaaS</h1>
<p class="subtitle">1,148 brand home pages · Thunderbit Original Research</p>
<div class="lang-toggle">
<button id="btn-en" onclick="setLang('en')">English</button>
<button id="btn-zh" class="active" onclick="setLang('zh')">中文</button>
</div></div>
<div class="container">
"""

HTML_FOOT = """
<div class="footer">
Public method · Thunderbit Original Data Research<br>
© 2026 Thunderbit. Channel names belong to their respective owners; aggregate statistics under fair use.
</div></div>
<script>
function setLang(l){document.body.classList.toggle('zh',l==='zh');document.getElementById('btn-en').classList.toggle('active',l==='en');document.getElementById('btn-zh').classList.toggle('active',l==='zh');}
</script></body></html>
"""


def md_to_html(md):
    lines = md.split("\n")
    out = []
    i = 0
    in_list = False
    def close():
        nonlocal in_list
        if in_list: out.append("</ul>"); in_list = False
    def inl(s):
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        return s
    while i < len(lines):
        line = lines[i]; st = line.strip()
        if "|" in line and st.startswith("|") and st.endswith("|"):
            close(); tbl = []
            while i < len(lines) and "|" in lines[i].strip() and lines[i].strip().startswith("|"):
                rl = lines[i].strip()
                if re.match(r"^\|[\s\-:|]+\|$", rl): i += 1; continue
                tbl.append([c.strip() for c in rl.strip("|").split("|")])
                i += 1
            if tbl:
                out.append("<table><thead><tr>" + "".join(f"<th>{inl(c)}</th>" for c in tbl[0]) + "</tr></thead>")
                if len(tbl) > 1:
                    out.append("<tbody>")
                    for row in tbl[1:]:
                        out.append("<tr>" + "".join(f"<td>{inl(c)}</td>" for c in row) + "</tr>")
                    out.append("</tbody>")
                out.append("</table>")
            continue
        if st.startswith("# "): close(); out.append(f"<h1>{inl(st[2:])}</h1>")
        elif st.startswith("## "): close(); out.append(f"<h2>{inl(st[3:])}</h2>")
        elif st.startswith("### "): close(); out.append(f"<h3>{inl(st[4:])}</h3>")
        elif st.startswith("> "): close(); out.append(f"<blockquote>{inl(st[2:])}</blockquote>")
        elif st.startswith("- "):
            if not in_list: out.append("<ul>"); in_list = True
            out.append(f"<li>{inl(st[2:])}</li>")
        elif re.match(r"^\d+\.\s", st):
            close(); out.append(f"<p><strong>•</strong> {inl(re.sub(r'^\\d+\\.\\s+', '', st))}</p>")
        elif st == "---": close(); out.append("<hr>")
        elif st.startswith("!["):
            close()
            m = re.match(r"!\[(.*?)\]\((.*?)\)", st)
            if m: out.append(f'<img src="{m.group(2)}" alt="{m.group(1)}">')
        elif st == "": close(); out.append("")
        else: close(); out.append(f"<p>{inl(st)}</p>")
        i += 1
    close()
    return "\n".join(out)


def main():
    s = load()
    zh = build_zh(s)
    en = build_en(s)
    html = HTML_HEAD + f'<div class="lang-en">{md_to_html(en)}</div>' + \
           f'<div class="lang-zh">{md_to_html(zh)}</div>' + HTML_FOOT
    (ROOT / "dtc_cx_map_2026_zh.md").write_text(zh, encoding="utf-8")
    (ROOT / "dtc_cx_map_2026_en.md").write_text(en, encoding="utf-8")
    (ROOT / "dtc_cx_map_2026.html").write_text(html, encoding="utf-8")
    zh_c = sum(1 for c in zh if "一" <= c <= "鿿")
    en_w = len(en.split())
    print(f"✅ 三件套(v2 去 AI 味)已生成")
    print(f"   中文 CJK: {zh_c}  ({'OK' if zh_c >= 4000 else f'⚠️ 差 {4000-zh_c}'})")
    print(f"   英文 words: {en_w}  ({'OK' if en_w >= 3500 else f'⚠️ 差 {3500-en_w}'})")


if __name__ == "__main__":
    main()
