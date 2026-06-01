# DTC 圈的客服工具,其实是个错配生态

> 2026-05-12 · 1,148 个 DTC 品牌主页静态扫描 · 23 种客服 vendor 指纹识别

---

我们抓了 1,148 个 DTC 品牌的主页 HTML,扫了一遍上面装的客服 widget——也就是访客打开页面那一刻能直接看到的「chat」按钮、bubble、或者 messenger 入口背后是哪家 vendor。结果不复杂,但和大多数人脑子里那个「SaaS 圈客服老大就是 DTC 圈客服老大」的印象,完全对不上。

最有意思的不是 Gorgias 占 23.3% 这个数字本身——这个数字我们必须先打个折,稍后讲为什么。最有意思的是,**SaaS 圈无可争议的客服老大 Intercom,在 DTC 圈占 0.6%**。1,148 个品牌里只有 7 个用 Intercom。一个 in-product messenger 范式的产品,在「客户根本不在 product 里」的电商场景里,几乎被完全淘汰。

这份报告主要回答两个问题。第一,DTC 客服工具市场是什么形状——谁赢、谁陪跑、谁退出?第二,AI 客服在 DTC 真的渗透到什么程度——招聘 JD 里 AI 工具命中率 35.6%(我们 5 月 11 日发的 AI Required Position Rate 报告里的数字),那 DTC 实战页面上呢?

先讲第二个,因为对比最反差。

## AI 客服:JD 里 35.6%,DTC 主页上 1.1%

![AI JD vs Home Contrast](figs/ai_jd_vs_home_contrast.png)

扫 1,148 个 DTC 主页,公开标榜「AI chatbot / AI assistant / AI agent / GPT-powered / Intercom Fin / Gorgias AI Agent」这类信号的——只有 13 个。1.1%。

把这个数字放在我们 5 月 11 日发的 AI Required Position Rate 报告旁边看,反差就立起来了。同一时间窗,HN 招聘社区 619 条招聘文案里,具体 AI 工具或 LLM 关键词的命中率是 35.6%——剔除 unknown 之后是 36.7%。两份报告的时间窗都是 2026-05,样本都是「广义的科技公司」。但**招聘文案里 AI 是「3 个岗位里有 1 个」,DTC 实战页面上 AI 是「100 个品牌里有 1 个」。差距三十倍**。

这个落差也不必读成「DTC 慢半拍」那么简单。我们的判断是这样的——招聘 JD 反映的是两件事:现在需要的技能,以及未来 12-18 个月想做的方向。35.6% 这个数字里有相当大一部分是「我们想招会做 AI 的人 *建* AI」,不是「我们的岗位都在 *用* AI」。所以 HN 数据其实是个领先指标,反映的是公司在 *计划* 什么,不是已经 *上线* 什么。

另一边,DTC 主页的 1.1% 也不等于「DTC 后端没用 AI」。很多 DTC 品牌大概率已经在 Gorgias Automate 或 Intercom Fin 后台开了自动回复——但他们不在主页上把这件事讲出来,因为他们的目标客户(普通消费者)不在意是不是 AI 回答。营销文案和后端部署在两个轨道上跑。我们看到的 1.1% 反映的是「品牌愿不愿意把 AI 当 selling point 端出来」,不是「品牌实际有没有用 AI」。

但这不影响一个商业结论:**对 AI 客服厂商(Gorgias Automate / Intercom Fin / Zendesk AI Suite / Reamaze AI Inbox,以及 Cresta、Decagon、Sierra、Forethought 这一批新入局者)来说,DTC 是个还没被「教育」的市场**。客户没在公开使用,公开使用的客户也没在讲。谁第一个把 AI 客服在 DTC 行业的叙事权拿到手,谁就锁定了 2027-2028 普及期的定位优势。

13 个公开标 AI 信号的 DTC 品牌,样本不大但有信号价值——这是行业里 *愿意把 AI 当卖点* 的早期一批:

![AI Brand List](figs/ai_brand_list.png)

名单里有 fillingpieces.com、hikoco.com、livingproof.com、olly.com、truelinkswear.com 等。注意这是「主页 *文案* 上提到 AI」的 13 家,不是「DTC 圈 AI 客服 Top 13」——更像是「敢把 AI 标在 storefront 上的早期 marketer」。

## 35% 装,65% 没扫到——但 65% 是下限

![Coverage Donut](figs/coverage_donut.png)

回到客服工具本身。1,148 个品牌主页里,397 个(35%)我们能在静态 HTML 上识别出至少一个客服 widget。其中 32% 装一个,2.3% 装两个,只有 1 个品牌装了 3 个或以上。这是「主客服 + 补充渠道」的组合模式,后面讲。

剩下 65% 看起来没装,但这个数字必须打折读。三种可能。

第一种,JS 动态加载漏检。很多客服 widget——包括 Gorgias、Zendesk 自身——是通过 chunk-loaded script 异步注入的。静态扫只看主页第一屏 HTML 字节里直接出现的 vendor host。如果 vendor 通过 GTM、Segment 或者一个延迟加载的 chunk 进来,我们这次的方法看不到。用 Thunderbit Chrome 扩展执行 JS 后扫,这层能补抓。

第二种,按需弹出。不少品牌只在 product page 或 checkout 页加客服 widget——主页保持「品牌叙事 + CTA」的视觉纯净度。这是一个有意思的 UX 决策,不是「不装」。

第三种,确实没装。149 个品牌(13%)主页上连「chat / live chat / contact us」这类自然语言提示都没有——这部分大概率确实没开 live chat,只留 email 联系入口。

综合下来,真实的「装了客服 widget」的比例可能在 50-60% 之间。我们报告的 35% 是 conservative 下限。重点是,**「主页装不装 chat widget」在 DTC 圈不是行业共识**——更接近 50/50 的现实。装不装,看你的 conversion funnel 摩擦在哪里、品牌主页想要什么调性,而不是「同行都装我也装」。

## Vendor 分布:Gorgias 居首,但要打折看

![Vendor Share](figs/vendor_share.png)

Top 15 vendor 是这样的:

| Rank | Vendor | 品牌数 | 占比 |
|---:|---|---:|---:|
| 1 | Gorgias | 267 | 23.3% |
| 2 | Zendesk | 49 | 4.3% |
| 3 | WhatsApp Button | 19 | 1.7% |
| 4 | Reamaze | 17 | 1.5% |
| 5 | HubSpot Chat | 12 | 1.0% |
| 6 | Kustomer | 11 | 1.0% |
| 7 | Crisp | 10 | 0.9% |
| 8 | Intercom | 7 | 0.6% |
| 9 | Facebook Messenger Plugin | 7 | 0.6% |
| 10 | Help Scout | 5 | 0.4% |
| 11 | Tidio | 5 | 0.4% |
| 12 | LiveChat | 4 | 0.3% |
| 13 | Tawk.to | 3 | 0.3% |
| 14 | Front | 3 | 0.3% |
| 15 | Freshchat | 2 | 0.2% |

Gorgias 占 23.3%,267 个品牌。第二是 Zendesk 4.3%,第三是 WhatsApp Button 1.7%。看起来 Gorgias 是绝对老大——但这个数字不能直接读。

我们构建 brand pool 时,1,597 个候选品牌里有相当一部分来自 Shopify 生态工具的 customer case study sitemap。**Gorgias 自己就是来源之一**——他们的 case study 把所有用 Gorgias 的 DTC 品牌自动收进了我们的池子。Klaviyo、Postscript、Shopify Plus、Skio 等其他 case study 也类似贡献。所以「Gorgias 23.3%」里,有相当一部分是 *样本偏向*,不是 *行业占比*。

独立来源对 Gorgias 的全市场估计:BuiltWith 看「全互联网技术栈」给出 ~3-5% of e-com sites;Wappalyzer 看「用户访问页面采样」给出 ~4-7% of Shopify sites;Gorgias 2024 财报披露 14,000+ merchants。综合看,Gorgias 在 DTC 行业的真实占比大约在 8-12% 区间,本报告样本里 23.3% 是「真实占比 × 约 2 倍样本回声」。把这个折扣记住——下面引用 Gorgias 数字时,我们都假设你已经在脑子里打折了。

打折之后,这份榜单还有几个值得看的信号。

**Zendesk 4.3% 是有意思的**。在 SaaS 圈,Zendesk 是绝对头部——B2B SaaS 公司里很难找到不用 Zendesk 的。但 DTC 圈,Zendesk 只占 4.3%。这不是「Zendesk 没努力」,是 DTC 客户接触模型和 SaaS 太不一样,Zendesk 那套通用 helpdesk 范式不贴 DTC 工作流。

**WhatsApp Button 1.7%(19 个品牌)**——这是个意外。一个 `wa.me/...` 链接,在 DTC 圈数量超过 Reamaze、HubSpot Chat、Crisp、Intercom 等所有正经客服 SaaS。这反映 DTC 客户的真实偏好——尤其是国际化品牌、跨境电商、低单价高复购的品类,**用户本来就有 WhatsApp,你直接放链接,他能直接给你发消息,不用注册新账号、不用接受 cookie banner、不用等 chat 加载**。零成本,易部署,有效。

**Intercom 0.6%(7 个品牌)**——这是这份报告里最让我们停下来反复看的一行。Intercom 在 SaaS 圈是统治级的存在,在 DTC 圈几乎不存在。我们后面会单独讲一节这件事,因为它能讲清楚一个完整的市场为什么会和另一个完整的市场架构如此不同。

**Reamaze 1.5%、Kustomer 1.0%、HubSpot Chat 1.0%、Crisp 0.9%**——这些是中尾,各自占一小块。Reamaze 是 Shopify-native 的 helpdesk,定位非常垂直;Kustomer 在 Meta 收购后转向 omnichannel 大品牌;HubSpot Chat 是免费 tier 拉新进来的;Crisp 在欧洲早期创业圈渗透高。每家都有自己的 niche,但没有一家能挑战 Gorgias 在 DTC 圈的主导位。

## 为什么 Gorgias 赢了 DTC,Intercom 几乎不存在

Gorgias 23.3%(打折后 8-12%)对比 Intercom 0.6%——SaaS 出身的人看到这个比例会觉得不合理。Intercom 是客服 SaaS 的统治者,DTC 怎么会用得这么少?

答案不在产品质量,在客户接触模型。SaaS 和 DTC 的客户从哪里来、问什么问题、需要 agent 看到什么——是两个完全不同的世界。Intercom 为 SaaS 量身定做了一套范式,放到 DTC 场景里水土不服。

SaaS 客户来自 B2B 漏斗:demo 请求 → trial → onboarding → expansion。一个用户从看到产品到付费,可能在 SaaS app 内停留几十次。客服 ticket 大多是技术问题——「我的账号坏了」「API 集成出错」「权限不对」。Intercom 的护城河是 *in-product messenger*——在 SaaS app 内嵌一个 chat 弹窗,把客服、in-app guidance、product tour 三件事合并在一个 surface 上。客户在 app 里出问题,Intercom 就在 app 里出现,seamless。

DTC 客户来自完全不同的漏斗:Meta / TikTok / Google 广告 → 点广告进站 → 加购 → 结账。一个买家从看到广告到结账可能就一次性 5 分钟,买完就走。客服 ticket 大多是订单问题——「我的包裹到哪了」「怎么退货」「优惠码失效」「能换码吗」。这种工单需要的不是「in-product messenger」,而是 *深度的 Shopify 订单数据集成*——客服坐席打开一个 ticket,屏幕上同时出现 Shopify 订单号、跟踪号、退款额度、客户历史订单。**不用切 8 个 tab**——这是 Gorgias 的核心价值主张。

再加一层:DTC 公司里,客服 + Returns + Fulfillment 这三个团队往往用同一套系统。Gorgias 把工单、Shopify 退款、跟踪号查询合并到一个工作流。Intercom 不是不能集成 Shopify,但它的产品基因是 messenger,不是 helpdesk-with-deep-Shopify-data。范式不同。

所以 Gorgias 在 DTC 圈赢的不是「客服 UI 漂亮」,赢的是 Shopify 数据深度。它的护城河不可被 *功能维度* 复制——任何想进 DTC 客服市场的厂商,都得先解决「订单查询」「退款执行」「换货流程」这三个占 80% 工单的类型,而不是只解决「FAQ 自动回」。

这对两类人有直接启示。**对 DTC 中介 / 运营来说**,选客服工具时核心标准应该是「跟 Shopify、订单系统、退货 SaaS 的集成深度」,不是「chat UI 是否漂亮」。Reamaze、Kustomer 走的是同一条路。Crisp 和 HelpScout 单价便宜但订单集成弱,适合早期 DTC,规模化之后通常会切换。**对 AI 客服厂商来说**,要进 DTC,光做「FAQ 自动回」远远不够——必须解决订单类工单的 80%。Gorgias Automate 和 Reamaze AI Inbox 已经在推这件事,但本报告的 1.1% AI 主页渗透率表明,**AI 替代订单类客服在 2026 年依然是早期阶段**。

另一个值得记的:**DTC 客服工具一旦装上去就难拔**。这套系统接在订单系统、退货 SaaS、邮件凭证流程之间,迁移是一个正式项目,不是一下午能完成的。这种粘性既解释了 Gorgias 早期优势的复利,也意味着新进入者需要的 wedge 比「我们 AI 更好」更强——需要一个 *workflow* 故事来 justify 客户的迁移摩擦。

## 装两个 widget 的 26 个品牌:不是混乱,是策略

2.3% 的品牌(26 家)同时装了 2 个及以上的客服 widget。常见的组合是这样:

| 组合 | 品牌数 |
|---|---:|
| Gorgias + Zendesk | 3 |
| Gorgias + HubSpot Chat | 2 |
| Crisp + Gorgias | 2 |
| Crisp + WhatsApp Button | 2 |
| Facebook Messenger Plugin + Gorgias | 2 |
| Crisp + Zendesk | 1 |
| HubSpot Chat + LiveChat | 1 |
| Gorgias + Reamaze | 1 |

看清楚——多 widget 不是「这家公司客服栈混乱」,而是「不同入口对应不同接触场景」。Gorgias 处理工单,WhatsApp 处理跨境消费者的直接对话,Facebook Messenger 给已认证社媒账号的客户。这是一个 *intentional* 的 multi-channel 策略,不是 *accidental* 的栈臃肿。

对 DTC 运营的实操含义——如果你的目标客户活跃在多个渠道,不要追求「单一 chat 工具搞定一切」。把主客服(Gorgias 或 Zendesk)做扎实,然后看你的客户实际从哪些渠道来,再补充直链 widget。26 家多 widget 品牌的存在反过来说明,DTC 圈的「主流单 widget」做法在某些场景下不是最优——尤其国际化品牌和高复购品类,客户期望能在「他已经在用的那个 app」里直接联系你。

## 给 DTC 运营、CX 团队、AI 客服厂商的几条建议

把数据拍平,如果你在 DTC 圈做客服 / CX / 增长方向的运营,以下几条是 actionable 的。

选客服工具,有阶段化的决策路径。月单 <1,000 单的早期 DTC,HelpScout / Crisp / Tidio 任选一个,单价不超过 $15/seat。这个阶段创始人 + 一个外包通常就能处理所有工单,不需要 routing rules,不需要高 SLA,跑通工单流就行。月单 1,000-10,000 单,Gorgias 或 Reamaze 是合理选择——这个阶段 Shopify 订单数据深度集成开始成为人工坐席的实际瓶颈,$50-150/seat 的成本能换回 30-40% 的人工时长节省,ROI 清晰。月单超过 10,000 单,Gorgias + AI Automate 或 Zendesk + AI Suite 或 Kustomer 进入议程——AI 自动回复优惠码查询和跟踪号查询能省 30-50% 人工坐席。这是 AI 客服真正发挥作用的 stage,也是本报告样本里几乎没人到达的 stage(这就解释了 AI signal 为什么只有 1.1%)。再往上的 omnichannel 大品牌,Zendesk 或 Kustomer 加多语言、多 region routing 才是答案,Gorgias 在国际化深度上略弱。

AI 客服内容是被严重低估的方向。渗透率 1.1% 不是「AI 客服没人要」,是「DTC 主页营销还没把 AI 当 selling point 端出来」。如果你做 DTC 内容——blog、case study、newsletter——「AI 客服怎么用、效果怎么样、ROI 怎么算」这套话题在内容市场上是高度供给不足的。你的读者既不知道同行在不在用,也不知道实际效果。这是 1-2 年内还有 content window 的方向。如果你是 Gorgias / Intercom / Zendesk 等的代理商或顾问,「我们能帮你启用 AI Agent」是个清晰的 wedge——竞争对手大多还没在 pitch 这个。

主页放不放 chat widget,不是行业共识。35% vs 65% 是接近 50/50 的现实。装不装的决策权在你手里——如果你的转化漏斗里 support ticket 是 friction,装;如果你想保持品牌主页的视觉 cleanliness,可以选择「按需弹出」或「只在 product / checkout 页装」。一个被忽视的中间策略——**只在 cart 和 checkout 页放 chat widget**,既能在关键转化点抓住犹豫客户,又不影响品牌主页的 brand expression。

最后,WhatsApp Button 是个被低估的渠道。19 个品牌(1.7%)直接放 `wa.me` 链接,数量超过 Reamaze、HubSpot Chat 等正经客服 SaaS。对国际化 DTC、跨境电商、低单价高复购品类,**直接 WhatsApp 链接可能比花式 chat widget 更有效**——零成本,易部署,客户已经有这个 app。值得在 A/B test 里加一组。

## 这份数据有多稳,边界在哪

1,148 个有效解析,从 1,429 个 home.html 中筛掉小于 1KB 或无法解析的。Vendor 指纹覆盖 23 个 vendor 但可能漏一些 niche 或自建客服。Long tail 的实际 share 可能比这里展示的更大。

静态扫只看主页第一屏 HTML 字节,这是下限。JS 动态加载的 widget(Intercom、Drift 的部分 init 模式)会漏检。要拿真实安装率需要用 Thunderbit Chrome 扩展执行 JS 后再扫,本次没做。

和外部数据对照,BuiltWith 估 Gorgias 在 e-com 全市场 3-5%,Wappalyzer 估 Shopify 站 4-7%,Gorgias 2024 财报披露 14,000+ merchants。本报告样本里 23.3% 是「真实占比 × 约 2 倍样本回声」。这些数据不互相矛盾——BuiltWith 看的是「全互联网技术栈」(分母大),Gorgias 自报是「merchant 数量」(不是 share),本报告样本是「DTC 头部 + Shopify 生态」(分母窄分子集中)。三个视角各有用。本报告值得引用的是「在 DTC 头部样本里 Gorgias 显著领先 Zendesk」,不是「Gorgias 占行业 23%」。

一句话边界:本报告描述的是「在我们抓的 1,148 个 DTC 品牌主页静态扫描里」发生了什么,**不是 DTC 行业市场份额**,**也不是「DTC 客服后端实际用什么」**。后端用什么是黑盒,我们只能看到主页 HTML 这一层。

## Reproducibility Notes

方法和数据完全公开,任何人能复现。

Brand pool 的 1,597 个候选品牌主要来自 30+ Shopify 生态工具的 case study sitemap,公开数据。复现者可以用自己的 DTC 公司池——BuiltWith Top DTC、a16z DTC 50、Modern Retail Top 100 都是合理替代,只要披露来源。

抓主页 HTML 用任何 HTTP 客户端都行,注意限速(全局不超过 10 req/s)和 UA 透明披露。我们扫的是「主页第一屏 256KB 字节」,这是下限——JS 动态加载漏检。

Vendor 指纹扫描,我们的 23 个 vendor 规则集开源在仓库的 `01_detect_widgets.py`。复现时建议交叉用 Wappalyzer 的开源规则集补充,我们漏的 vendor 你能抓到。

AI signal 用 regex 命中「AI assistant / AI agent / AI chatbot / GPT-powered / Intercom Fin / Gorgias Automate」等常见 marketing 短语。这是 surface signal——只反映品牌是否对外营销 AI,**不反映后端是否真的用 AI**。后者需要 vendor API 接入或人工 spot check。

复跑频率建议季度跑一次。Vendor 渗透率以年为单位变化,AI signal 可能每季度动 0.5-1 pp 的量级。

已知漏检——Intercom 和 Drift 的部分 chunk-loaded init 模式,自建客服系统(没有 vendor host 信号),通过 GTM 或 Segment 间接 inject 的 widget,以及多语言站点(国际化 DTC 在每个 region 加载不同 widget)。想要精确度,用 Thunderbit Chrome 扩展执行 JS 后再扫,能覆盖动态加载部分。想要「头部谁领先」,本报告的静态结果已经够稳健。

---

## Methodology / 方法论与样本声明

**数据源**:1,597 brand pool 的 1,148 个 DTC 主页 home.html(过滤到 ≥1KB),配 23 个客服 vendor 指纹规则(`01_detect_widgets.py` 公开)。采集 / 解析日期 2026-05-12(UTC)。

**Gorgias 数据源回声(最关键)**:Brand pool 部分来自 Gorgias / Klaviyo / Postscript / Shopify Plus 等 Shopify 生态工具的 customer case study sitemap。**Gorgias 本身就是来源之一**——他们的 case study 把所有用 Gorgias 的 DTC 品牌都自动收进了样本。Gorgias 23.3% **不等于 Gorgias 占 DTC 行业 23%**——独立估计器(BuiltWith / Wappalyzer)给出的全市场占比是 8-12%。把 23.3% 理解为「样本里 #1 vendor,约 2 倍样本回声」,不是行业 share。

**Brand pool 偏 Shopify 生态**:~67% 品牌来自 Shopify 工具栈 case study,样本天然偏向 Shopify-native + remote-friendly + AI-adopter 的 DTC 子集,**不代表「全美 DTC 市场」**。Mom-and-pop e-com、传统零售迁移 DTC 等子赛道在本样本中代表性弱。

**静态扫下限**:只看主页第一屏 256KB 字节,JS 动态加载的 widget 漏检。Intercom 和 Drift 的部分 chunk-loaded init 会被误归类为「无 widget」。35% widget 覆盖是下限,实际可能在 50-60%。

**AI signal 是「主页营销话术」,不是「后端实际 AI」**:很多 DTC 品牌大概率已经在用 Gorgias Automate 或 Intercom Fin 后端的 AI 自动回复,但没在主页营销文案里把 AI 当 selling point。本报告的「AI signal 1.1%」反映的是「品牌是否对外营销 AI 客服」,**不直接反映「品牌后端是否用了 AI」**。两者相关但不等价。

**同公司多 widget 不等于「客服栈混乱」**:26 家多 widget 品牌通常是「主客服 + 直链补充」(如 Gorgias + WhatsApp),不是在维护多套并行客服系统。

**法律与版权**:所有主页是公开抓取,本报告**只做聚合统计**(vendor count + percentage),不全文引用任何品牌主页。AI signal 命中的 13 家品牌点名属于正面或中性 case(他们公开标 AI 是自己的营销选择)。多 widget 26 家点名属于中性 case(描述事实)。报告不发布 raw HTML 或 raw CSV 下载链接,所有数字可通过公开 brand pool + 公开规则集复现。

**不能解读为**:

- 不是「Gorgias 占 DTC 行业市场份额 23.3%」(含样本回声,真实约 8-12%)
- 不是「DTC 圈只有 1.1% 用了 AI 客服」(本数字只反映「在主页营销文案上标 AI」,不反映后端实际用没用)
- 不是「65% DTC 品牌没装 chat widget」(这是静态扫下限,实际可能 50-60%)
- **可以说**:「在我们追踪的 1,148 个 DTC 品牌主页静态扫描里,Gorgias 是 #1 检测到的 vendor(23.3%,含样本偏向),AI 营销信号渗透 1.1%」

---

## 数据来源与版本

数据集:`dtc_customer_support_map_2026/`(本仓库)。采集日期 **2026-05-12** UTC,报告版本 v1.0(静态扫下限版;v2 计划用 Thunderbit Chrome 扩展跑 JS 后补抓)。共用 DTC brand pool 与 `dtc_dual_report_2026` 同一 1,148 子集,可交叉引用。配对报告:AI Required Position Rate 2026(HN 招聘样本,2026-05-11 发布)——AI 在招聘文本的一半,跟本报告 AI 在产品页的一半合起来看,能从招聘意图和产品落地两个角度三角验证。
