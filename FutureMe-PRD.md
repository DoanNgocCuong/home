# PRD: FutureMe
## AI-Powered Personal Future Simulation Platform
**Version:** 1.0
**Author:** SU (su.aitool@thecoach.ai)
**Date:** March 15, 2026
**Status:** Draft
**Market:** Southeast Asia (SEA), expand global
**Monetization:** Freemium SaaS

---

## 1. Problem Statement

Mỗi ngày, hàng triệu người ở Đông Nam Á đứng trước những quyết định lớn thay đổi cuộc đời: nghỉ việc để khởi nghiệp, chuyển ngành, kết hôn, di cư, đầu tư. Họ tìm kiếm lời khuyên từ bạn bè (thiên lệch), fortune tellers (không evidence-based), hoặc life coaches (đắt đỏ, $200-2,000/tháng, khó tiếp cận ở SEA).

Kết quả: 73% professionals ở SEA báo cáo "decision anxiety" khi đối mặt career changes (LinkedIn SEA Workforce Report 2025). 68% startup founders ở VN/ID/TH thất bại trong 2 năm đầu, phần lớn vì quyết định sai ở giai đoạn sớm mà không ai cảnh báo (TOPICA Founder Institute data).

Không có công cụ nào cho phép một người "sống thử" quyết định của mình trước khi cam kết — thấy hậu quả ở 6 tháng, 1 năm, 3 năm, từ chính dữ liệu tính cách và thói quen của họ.

**FutureMe giải quyết vấn đề này** bằng cách tạo ra hàng trăm "phiên bản tương lai" AI của chính người dùng, mỗi phiên bản sống trong một scenario khác nhau, cho phép người dùng quan sát kết quả, chat với future-self, và ra quyết định với sự tự tin cao hơn.

---

## 2. Goals

### User Goals
- **G1: Giảm decision anxiety.** Người dùng cảm thấy tự tin hơn 50% khi ra quyết định lớn sau khi chạy simulation (đo bằng pre/post survey, thang 1-10).
- **G2: Self-awareness sâu hơn.** Người dùng phát hiện ít nhất 2 patterns/blind spots về bản thân mà họ không biết trước đó (đo bằng post-simulation feedback: "Bạn có khám phá điều gì mới về bản thân?").
- **G3: Hành động cụ thể.** 60%+ người dùng thực hiện ít nhất 1 action item từ insight của simulation trong vòng 7 ngày.

### Business Goals
- **G4: Product-Market Fit tại SEA.** Đạt 10,000 active users trong 6 tháng đầu, với 40%+ retention D30.
- **G5: Revenue.** Đạt $20K MRR trong 12 tháng từ freemium conversion (target 5% free → paid).
- **G6: Platform play.** Onboard 50 coaches/therapists sử dụng FutureMe trong sessions của họ trong 12 tháng.

---

## 3. Non-Goals (v1)

- **Không dự đoán sự kiện cụ thể.** FutureMe không nói "bạn sẽ được tăng lương vào tháng 7." Nó show patterns và probabilities, không phải fortune telling. Lý do: accuracy claims tạo liability và phá vỡ trust khi sai.

- **Không thay thế therapy/coaching chuyên nghiệp.** FutureMe là công cụ self-exploration, không phải treatment. Sẽ có safety rails redirect đến professionals khi phát hiện dấu hiệu mental health crisis. Lý do: regulatory risk + ethical responsibility.

- **Không tích hợp real-time external data (stock market, news).** v1 chỉ dùng thông tin người dùng cung cấp + knowledge base tĩnh. Lý do: complexity quá cao, cần validate core value trước.

- **Không support team/organization simulation.** v1 chỉ cho cá nhân. Mô phỏng tổ chức là roadmap v3. Lý do: cá nhân dễ validate, ít data input hơn, viral potential cao hơn.

- **Không build mobile app native.** v1 là responsive web app (PWA). Lý do: ship nhanh hơn, iterate dễ hơn, đủ cho SEA market (mobile web usage cao).

---

## 4. Target Users & Personas

### Persona 1: "Minh" — Startup Founder đang cân nhắc pivot (Primary)
- 28 tuổi, Ho Chi Minh City
- Running a B2B SaaS startup, 8 employees, pre-revenue
- Đang cân nhắc: pivot sang AI product hay tiếp tục đường cũ?
- Pain: Không ai trong circle hiểu context đủ sâu để tư vấn. Mentor nói "follow your gut" nhưng gut feeling mâu thuẫn
- Behavior: Đọc Medium, dùng Notion, ChatGPT daily, LinkedIn active
- Willingness to pay: $19-29/tháng cho tool giúp ra quyết định

### Persona 2: "Linh" — Mid-career Professional muốn chuyển ngành
- 32 tuổi, Jakarta
- 7 năm trong banking, muốn chuyển sang tech/product management
- Đang cân nhắc: nghỉ việc đi học bootcamp hay tự học part-time?
- Pain: Sợ mất thu nhập, sợ tuổi "quá già" để chuyển ngành, gia đình phản đối
- Behavior: Dùng TikTok, Instagram, Glassdoor, career forums
- Willingness to pay: $9-19/tháng, rất price-sensitive

### Persona 3: "Coach Thanh" — Life Coach sử dụng FutureMe trong sessions (Secondary)
- 40 tuổi, Bangkok
- Certified ICF coach, 50 clients/tháng
- Muốn: tool trực quan giúp client "thấy" hậu quả quyết định thay vì chỉ nói
- Pain: Client thường stuck ở "what if" — nói mãi không đủ, cần visual proof
- Behavior: Dùng Zoom, Calendly, Notion, các coaching platforms
- Willingness to pay: $49-99/tháng nếu cải thiện session quality

---

## 5. User Stories

### Epic 1: Onboarding & Profile Building

**US-1.1** As Minh (founder), I want to build my FutureMe profile through a natural conversation (not boring forms) so that the AI understands my personality, habits, and context without feeling like an interrogation.
- Acceptance: Conversational onboarding, 5-7 minutes, covers personality traits, daily habits, current situation, key goals. User can skip sections and add later.

**US-1.2** As Linh (professional), I want to connect my existing data (LinkedIn, calendar patterns, health app) so that FutureMe has richer context without me typing everything manually.
- Acceptance: Optional integrations. Clearly explain what data is used and why. Works fine without any connections.

**US-1.3** As any user, I want to see my "Personal Profile Card" summarizing what FutureMe knows about me so that I can verify accuracy and correct mistakes.
- Acceptance: Visual card showing personality traits, top habits, goals, key context. Edit button on every section. "Accuracy confidence" indicator.

### Epic 2: Simulation Creation & Execution

**US-2.1** As Minh, I want to describe a decision I'm facing in plain language ("Should I pivot my startup to AI?") and get FutureMe to run a simulation so that I can see multiple possible futures.
- Acceptance: Free-text input. AI extracts the decision, identifies key variables, confirms understanding before running. Shows progress indicator during simulation.

**US-2.2** As Minh, I want to define custom scenarios to compare ("pivot to AI" vs "stay current course" vs "shut down and join a company") so that I see them side by side.
- Acceptance: Support 2-4 scenarios per simulation. Each scenario runs independently. Results shown in comparative view.

**US-2.3** As any user, I want the simulation to use MY actual personality and habits (not generic assumptions) so that the results feel personally relevant.
- Acceptance: Simulation agents carry user's actual personality traits, decision-making patterns, risk tolerance, energy patterns, and known strengths/weaknesses from profile.

**US-2.4** As Linh, I want to see simulation results at multiple time horizons (6 months, 1 year, 3 years) so that I understand both short-term pain and long-term outcomes.
- Acceptance: Timeline view with key events, branching points, and probability indicators at each horizon.

**US-2.5** As any user, I want the simulation to show me PATTERNS and RISKS I didn't think of so that I expand my blind spots.
- Acceptance: Each simulation report includes "Surprises" section — patterns that emerged across 100+ agent runs that user likely didn't anticipate.

### Epic 3: Future Self Conversation

**US-3.1** As Minh, I want to chat with "3-year-future-me" from a specific scenario so that I can ask questions and get personal advice from someone who's "been through it."
- Acceptance: Chat interface. Future-self speaks in first person, references events from the simulation, has opinions and emotions consistent with the simulated experience.

**US-3.2** As Linh, I want to ask my future-self emotional questions ("Am I happy?" "Do I regret it?") and get authentic, nuanced answers so that I evaluate decisions beyond just career metrics.
- Acceptance: Future-self responds with emotional depth — not just facts. Acknowledges trade-offs. Can express regret, satisfaction, surprise. Never gives one-dimensional answers.

**US-3.3** As Coach Thanh, I want to let my client chat with their future-self during a coaching session so that the client has a breakthrough moment without me lecturing.
- Acceptance: "Share session" link. Coach can observe the conversation. Client controls the chat. Coach can suggest questions via side panel.

### Epic 4: Simulation Report & Insights

**US-4.1** As any user, I want a comprehensive simulation report I can save and revisit so that I can reflect over time, not just in the moment.
- Acceptance: PDF-exportable report. Sections: Executive Summary, Scenario Comparison, Key Patterns, Risks & Opportunities, Blind Spots, Recommended Actions. Saved in user account permanently.

**US-4.2** As Minh, I want to see probability distributions ("35% of simulations led to success, 42% to pivot, 23% to shutdown") so that I understand likelihoods, not just stories.
- Acceptance: Visual probability charts. Clear methodology note: "Based on 200 AI simulations of your profile. Not a prediction — an exploration of possibilities."

**US-4.3** As any user, I want to see which SPECIFIC habits or traits of mine most influenced the outcomes so that I know what to change.
- Acceptance: "Key Influence Factors" section ranking which traits/habits had highest impact on outcomes. E.g., "Your low delegation tendency was the #1 factor in 67% of burnout scenarios."

**US-4.4** As Linh, I want actionable next steps based on simulation insights so that I know what to do THIS WEEK, not just vague future direction.
- Acceptance: 3-5 concrete, time-bound action items. E.g., "This week: Talk to 2 people who switched from banking to tech after age 30" — not "Consider your options carefully."

### Epic 5: Social & Sharing

**US-5.1** As Linh, I want to share a beautiful summary card of my simulation on social media so that I can start a conversation and maybe inspire others.
- Acceptance: Auto-generated visual card (Instagram/LinkedIn format). Shows scenario, key insight, one powerful quote from future-self. No sensitive personal data unless user explicitly includes it.

**US-5.2** As any user, I want to see anonymized simulation trends ("72% of founders who pivoted to AI in Q1 2026 simulations showed positive 3-year outcomes") so that I see community patterns.
- Acceptance: Aggregated insights dashboard. Fully anonymized. Opt-in only.

### Epic 6: Coaching Integration

**US-6.1** As Coach Thanh, I want a coach dashboard where I can manage multiple clients' simulations so that I can use FutureMe as a standard tool in my practice.
- Acceptance: Dashboard with client list, recent simulations, key insights per client. Client must grant explicit permission.

**US-6.2** As Coach Thanh, I want to inject "what if" variables into a client's simulation mid-session ("What if they hired a co-founder?") so that we can explore scenarios together in real-time.
- Acceptance: "God mode" panel for coaches. Inject variables, re-run partial simulation in <2 minutes, see updated results.

---

## 6. Requirements

### Must-Have (P0) — v1 MVP

| ID | Requirement | Acceptance Criteria |
|----|-------------|-------------------|
| P0-01 | Conversational onboarding | User completes profile in 5-7 min conversational flow. Covers: personality (Big Five proxy), daily habits (5+ habits), current situation, top 3 goals. Skip-able sections. |
| P0-02 | Decision input & scenario setup | User describes decision in free text. AI extracts decision + generates 2-3 scenarios. User can edit/add scenarios (max 4). Confirmation screen before simulation runs. |
| P0-03 | Multi-agent simulation engine | Run 100-500 AI agents per scenario, each carrying user's personality profile. Agents simulate 6mo/1yr/3yr timelines. Engine produces probability distributions + emergent patterns. Powered by MiroFish core engine. |
| P0-04 | Simulation report | Report includes: scenario comparison, probability distribution, key patterns, blind spots, top 3 influence factors, 3-5 action items. Viewable in-app. PDF export. |
| P0-05 | Future-self chat | User can chat with AI persona representing their "future self" from any simulated scenario. Future-self maintains personality consistency, references simulation events, responds with emotional nuance. |
| P0-06 | User authentication | Email + password registration. Google OAuth. Magic link login. SEA phone number support (VN, ID, TH, PH). |
| P0-07 | Freemium gating | Free tier: 1 simulation/month, 3 future-self chats/simulation, basic report. Paid tier ($19/mo): unlimited simulations, unlimited chats, full report + PDF, priority processing. |
| P0-08 | Multi-language | English + Vietnamese + Bahasa Indonesia at launch. Thai within 3 months. Language auto-detected from browser, switchable in settings. |
| P0-09 | Mobile-responsive web app | PWA. Works on mobile Chrome/Safari. Offline: view saved reports. Install prompt on mobile. |
| P0-10 | Safety rails | Detect crisis keywords (suicide, self-harm, abuse). Redirect to local crisis hotlines (VN: 1800-599-100, ID: 119, TH: 1323). Block simulation if input contains harmful intent. Disclaimer on every report: "This is an exploration tool, not a prediction or medical advice." |

### Nice-to-Have (P1) — Fast Follow (Month 2-4)

| ID | Requirement | Notes |
|----|-------------|-------|
| P1-01 | Social sharing cards | Auto-generated visual cards for Instagram/LinkedIn/TikTok. Template variations. |
| P1-02 | LinkedIn data import | OAuth integration. Pull career history, skills, connections count for richer profile. |
| P1-03 | "What-if" variable injection | After simulation, change 1-2 variables and re-run partial simulation to see impact. |
| P1-04 | Community insights dashboard | Anonymized aggregate trends: "What are people in your age/industry simulating?" |
| P1-05 | Simulation history & comparison | Compare current simulation with past simulations. Track how decisions evolved. |
| P1-06 | Notification reminders | "It's been 3 months since your simulation. How did the decision turn out? Update us!" — feeds back into accuracy improvement. |

### Future Considerations (P2) — v2/v3

| ID | Requirement | Notes |
|----|-------------|-------|
| P2-01 | Coach/Therapist dashboard | Multi-client management, session sharing, "God mode" variable injection. |
| P2-02 | API for B2B integrations | Coaching platforms, HR tech, EdTech can embed FutureMe simulations. |
| P2-03 | Real-time data enrichment | Connect news, market data, industry trends to make simulations context-aware. |
| P2-04 | Organization/Team simulation | Simulate team dynamics, company growth, hiring decisions. |
| P2-05 | Outcome tracking & model improvement | Users report actual outcomes → feed back into simulation accuracy over time. |
| P2-06 | Voice-based interaction | Talk to future-self via voice (critical for SEA markets with lower text literacy). |

---

## 7. Technical Architecture (High-Level)

### System Overview

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Frontend   │────▶│   API Layer  │────▶│  Simulation      │
│   (Vue/React)│◀────│   (FastAPI)  │◀────│  Engine          │
│   PWA        │     │              │     │  (MiroFish Core)  │
└──────────────┘     └──────┬───────┘     └────────┬─────────┘
                            │                      │
                     ┌──────▼───────┐     ┌────────▼─────────┐
                     │  PostgreSQL  │     │  Agent Memory     │
                     │  (Users,     │     │  (Zep / Redis)    │
                     │   Profiles,  │     │                   │
                     │   Reports)   │     └──────────────────┘
                     └──────────────┘
                            │
                     ┌──────▼───────┐
                     │  LLM Layer   │
                     │  (Claude /   │
                     │   Qwen)      │
                     └──────────────┘
```

### Core Components

**Profile Engine:** Converts conversational input → structured personality/habit/context model. Uses Big Five personality mapping, habit categorization, and situational analysis. Stored as a "Personal Seed" — the input for MiroFish.

**Simulation Engine (MiroFish-based):**
- Takes Personal Seed + Decision Scenarios as input
- Creates 100-500 AI agents per scenario, each an instance of the user's personality
- Runs parallel simulations across 3 time horizons (6mo, 1yr, 3yr)
- Uses GraphRAG for relationship mapping between life factors
- Outputs: event timelines, probability distributions, emergent patterns, influence factor rankings

**Future-Self Chat Engine:** Post-simulation, creates a persistent AI persona from a specific scenario branch. Persona carries: personality traits from profile, memories from simulation events, emotional state consistent with outcomes, opinions formed through simulated experience.

**Report Generator:** Aggregates simulation data into structured, human-readable reports. Statistical summaries, pattern extraction, blind spot identification, actionable recommendations.

### Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | Vue 3 + TypeScript + Tailwind | MiroFish frontend is Vue-based, maintain consistency |
| Backend API | Python 3.12 + FastAPI | MiroFish backend is Python, shared ecosystem |
| Simulation | MiroFish engine (OASIS/CAMEL-AI) | Proven multi-agent simulation, 24K stars, active development |
| Database | PostgreSQL 16 | Relational data (users, profiles, reports) |
| Agent Memory | Zep Cloud | MiroFish native integration, long-term agent memory |
| Cache/Queue | Redis | Session management, job queue for simulations |
| LLM | Claude API (primary) + Qwen (backup) | Claude for quality, Qwen for cost optimization on high-volume tasks |
| Search | GraphRAG | Relationship mapping between life factors |
| Storage | S3-compatible (MinIO/Cloudflare R2) | Report PDFs, sharing card images |
| Deploy | Docker + Railway (staging) → AWS ECS (production) | Progressive deployment strategy |
| CDN | Cloudflare | SEA edge locations, fast for target markets |
| Monitoring | Sentry + PostHog | Error tracking + product analytics |

### Data Architecture

```
Personal Seed (JSON):
{
  "personality": {
    "openness": 0.72,
    "conscientiousness": 0.85,
    "extraversion": 0.45,
    "agreeableness": 0.68,
    "neuroticism": 0.38
  },
  "habits": [
    {"name": "morning_exercise", "frequency": "4x/week", "impact": "high"},
    {"name": "reading", "frequency": "daily", "duration": "30min"},
    {"name": "social_media", "frequency": "3h/day", "impact": "negative"}
  ],
  "situation": {
    "age": 28,
    "location": "Ho Chi Minh City",
    "career": "Founder, B2B SaaS, 8 employees, pre-revenue",
    "finances": "12 months runway",
    "relationships": "married, 1 child (2yo)",
    "health": "good, mild anxiety, sleep 6h/night"
  },
  "goals": [
    "Build profitable company",
    "Be present for family",
    "Financial independence by 35"
  ],
  "decision": "Should I pivot to AI product or stay current course?",
  "scenarios": [
    "Pivot to AI: rebuild product, new market, 6-month timeline",
    "Stay course: double down on current customers, profitability focus",
    "Hybrid: add AI features gradually while maintaining current product"
  ]
}
```

### Simulation Pipeline

```
Step 1: Seed Preparation (5s)
  Personal Seed → GraphRAG entity extraction
  → Relationship mapping (career ↔ family ↔ finance ↔ health)

Step 2: Agent Population (10s)
  Create 200 agents per scenario (600 total for 3 scenarios)
  Each agent = user's personality + scenario-specific initial conditions
  Agents assigned to "life domains": career, finance, relationship, health, personal growth

Step 3: Simulation Execution (2-5 min)
  Parallel simulation across 3 time horizons
  Agents interact, make decisions, face randomized life events
  Dynamic memory updates via Zep
  Checkpoint at 6mo, 1yr, 3yr

Step 4: Pattern Extraction (30s)
  Aggregate outcomes across 200 agents per scenario
  Identify: probability distributions, recurring patterns, critical branching points
  Rank influence factors by impact

Step 5: Report Generation (15s)
  Structure findings into report template
  Generate future-self personas for each scenario
  Create shareable summary card

Total: ~3-6 minutes per simulation
```

---

## 8. UX Flow (Key Screens)

### Screen 1: Landing Page
- Hero: "Gặp phiên bản tương lai của bạn" / "Meet Your Future Self"
- Sub: "Mô phỏng AI dựa trên tính cách, thói quen và quyết định thật của bạn"
- CTA: "Bắt đầu miễn phí" / "Start Free"
- Social proof: số simulations đã chạy, testimonials

### Screen 2: Conversational Onboarding
- Chat-like interface (not a form)
- AI asks questions naturally: "Kể tớ nghe về một ngày bình thường của bạn?"
- Progress indicator: 7 steps, ~5 minutes
- Skip buttons + "Tell me more" option on each step
- Personality result card at end: "Đây là profile của bạn — có đúng không?"

### Screen 3: Decision Input
- Large text area: "Quyết định bạn đang cân nhắc?"
- AI suggests scenarios based on decision
- User can edit/add scenarios (max 4)
- "Run Simulation" button with estimated time (3-6 min)

### Screen 4: Simulation Progress
- Animated visualization of agents interacting
- Real-time stats: "347 phiên bản bạn đang sống tương lai..."
- Timeline preview appearing gradually
- Not a boring loading screen — this IS the experience

### Screen 5: Results Dashboard
- Tab view: Scenario A | Scenario B | Scenario C | Compare
- Each scenario: Timeline (6mo → 1yr → 3yr), Probability pie chart, Key events
- Compare view: Side-by-side metrics across scenarios
- "Surprises" badge: patterns user didn't expect
- "Chat with Future Self" button per scenario

### Screen 6: Future-Self Chat
- Chat interface, future-self has avatar + name + age
- Header: "Bạn (3 năm sau) — Scenario: Pivot to AI"
- Suggested questions: "Tớ có hạnh phúc không?" "Quyết định nào tớ hối hận nhất?"
- "Switch scenario" dropdown to talk to different future-selves

### Screen 7: Report View
- Full report with all sections
- "Download PDF" button
- "Share on LinkedIn/Instagram" button
- "Schedule follow-up" — reminder to check back in 3/6 months

---

## 9. Success Metrics

### Leading Indicators (Week 1-4 post-launch)

| Metric | Target | Stretch | Measurement |
|--------|--------|---------|-------------|
| Onboarding completion rate | 60% | 75% | % users who complete profile (start → finish) |
| Simulation run rate | 80% of completed profiles | 90% | % profiled users who run at least 1 simulation |
| Future-self chat engagement | 3 messages avg/session | 7 messages | Avg messages sent in future-self chat |
| Simulation completion rate | 90% | 95% | % simulations that complete without error/abandon |
| Time to first insight | <8 minutes | <5 minutes | From signup to seeing first simulation result |
| Share rate | 10% | 20% | % users who share result card on social |

### Lagging Indicators (Month 1-6)

| Metric | Target | Stretch | Measurement |
|--------|--------|---------|-------------|
| D7 retention | 30% | 45% | % users returning within 7 days |
| D30 retention | 15% | 25% | % users returning within 30 days |
| Free → Paid conversion | 5% | 8% | % free users upgrading within 30 days |
| MRR | $5K (M3), $20K (M12) | $10K (M3), $40K (M12) | Monthly recurring revenue |
| NPS | 40 | 55 | Net Promoter Score (quarterly survey) |
| "Aha moment" rate | 70% | 85% | % users who report "discovered something new about themselves" in post-simulation survey |
| Action completion rate | 40% | 60% | % users who complete at least 1 recommended action within 7 days |
| Coach onboarding | 20 coaches (M6) | 50 coaches (M6) | Coaches actively using FutureMe with clients |

### North Star Metric

**"Simulations that changed a decision"** — % of users who report that FutureMe influenced their actual decision-making. Target: 30% within 6 months.

Measured via: Follow-up survey 30 days after simulation: "Did the simulation influence your decision?" (Yes, changed my decision / Yes, confirmed my direction / No impact / Haven't decided yet).

---

## 10. Monetization Details

### Free Tier
- 1 simulation per month
- 2 scenarios per simulation (max)
- 3 future-self chat messages per scenario
- Basic report (no PDF export)
- Community insights access

### Premium Tier — $19/month (SEA pricing, ~$29 USD equivalent globally later)
- Unlimited simulations
- 4 scenarios per simulation
- Unlimited future-self chats
- Full report + PDF export
- "What-if" variable injection (re-run with changes)
- Priority simulation processing (2 min vs 5 min)
- Simulation history & comparison
- No ads

### Coach Tier — $49/month (P2, post-launch)
- Everything in Premium
- Multi-client dashboard (up to 20 clients)
- "God mode" variable injection during sessions
- Session sharing links
- Client consent management
- Branded report templates

### Revenue Projections (Conservative)

```
Month 1-3:   5,000 users × 3% conversion × $19 = $2,850 MRR
Month 4-6:   15,000 users × 4% conversion × $19 = $11,400 MRR
Month 7-12:  40,000 users × 5% conversion × $19 = $38,000 MRR
Year 1 total: ~$200K ARR

Cost structure (Month 6):
  LLM API costs: ~$3,000/month (200 simulations/day × $0.50/sim)
  Infrastructure: ~$500/month (Railway → AWS)
  Total COGS: ~$3,500/month
  Gross margin: ~70%
```

---

## 11. Competitive Landscape

| Product | What it does | FutureMe differentiator |
|---------|-------------|------------------------|
| Co-Star / Pattern (Astrology) | "Predict" future based on stars | FutureMe dùng DATA THẬT của bạn, không phải vị trí sao |
| BetterHelp / Talkspace | Online therapy | FutureMe là exploration tool, không phải therapy. Complementary, not competitive |
| Crystal Knows | Personality AI for sales | Only personality — no simulation, no future-self chat |
| Replika | AI companion chat | General companion — not decision-focused, not simulation-based |
| Life Simulator games | Entertainment simulation | Games, not serious decision tools. No real personality data |
| McKinsey/BCG (scenario planning) | Enterprise strategy simulation | B2B, $500K+ contracts. FutureMe is B2C, $19/month |

**Moat:**
1. **Network effect:** More users → more aggregate data → better simulation accuracy → more users
2. **Personal data depth:** Over time, user profiles become deeply personal — switching cost increases
3. **MiroFish engine integration:** First-mover on applying swarm intelligence to personal decisions (not just enterprise/policy)

---

## 12. Risks & Mitigations

| Risk | Severity | Likelihood | Mitigation |
|------|----------|-----------|-----------|
| Users treat simulation as "prophecy" and make reckless decisions based on it | High | Medium | Prominent disclaimers on every screen. "Exploration, not prediction" messaging. Legal terms of service. |
| LLM hallucination produces harmful advice in future-self chat | High | Medium | Safety rails, content filtering, prohibited topics list. Future-self never advises on medical/legal/financial specifics. |
| Simulation results feel "generic" and not personal enough | High | High | This is the #1 product risk. Mitigate: invest heavily in profile depth, personality accuracy testing, user validation step. |
| Privacy concerns — users share deeply personal data | High | High | End-to-end encryption at rest. GDPR/PDPA compliance. Clear data deletion policy. No data sharing with third parties. Anonymization for aggregate insights. |
| MiroFish engine can't handle high concurrency | Medium | Medium | Queue system with priority tiers. Cache common simulation patterns. Horizontal scaling plan. |
| Low retention — users run 1 simulation and never return | Medium | High | Mitigate: follow-up reminders ("How did your decision turn out?"), new simulation prompts based on life events, community features, coach integration creates recurring usage. |
| Regulatory risk in SEA (AI prediction claims) | Medium | Low | Never use word "predict" in marketing. Frame as "explore" and "simulate." Legal review per country. |

---

## 13. Go-To-Market Strategy (SEA)

### Phase 1: Vietnam Launch (Month 1-3)
- **Channel:** TikTok + LinkedIn Vietnam (founder community is active on both)
- **Hook:** "Tớ vừa nói chuyện với phiên bản 3-năm-sau của mình. Nó bảo tớ đừng..." + share card
- **Influencer:** Partner with 5-10 Vietnam tech/startup KOLs to run simulations live on stream
- **Community:** Launch in Startup Vietnam, VFOSSA, tech Facebook groups
- **PR:** TechInAsia, e27 coverage

### Phase 2: Indonesia + Thailand (Month 4-6)
- Localize to Bahasa + Thai
- Partner with local coaching communities
- University partnerships (MBA programs, career centers)

### Phase 3: Regional + Global (Month 7-12)
- English version for global SEA expats + global professionals
- Product Hunt launch
- B2B partnerships with coaching platforms (CoachHub, BetterUp)

### Viral Loop
```
User runs simulation → Gets insight card
→ Shares on LinkedIn/TikTok: "My AI future-self told me..."
→ Friends curious → Sign up → Run their own simulation
→ Share their results → Cycle continues

Expected viral coefficient: 1.3-1.5 (each user brings 1.3 new users)
```

---

## 14. Timeline & Phasing

### Phase 0: Foundation (Week 1-2)
- Setup project, tech stack, MiroFish engine integration
- Profile engine prototype
- Basic auth + DB schema

### Phase 1: Core MVP (Week 3-6)
- Conversational onboarding
- Simulation engine (200 agents, 3 scenarios, 3 timelines)
- Basic report generation
- Future-self chat v1

### Phase 2: Polish & Launch (Week 7-8)
- Mobile-responsive PWA
- Vietnamese + English localization
- Freemium gating
- Safety rails
- Beta testing with 50 users

### Phase 3: Growth Features (Month 3-4)
- Social sharing cards
- Community insights
- LinkedIn data import
- "What-if" variable injection
- Bahasa Indonesia localization

### Phase 4: B2B2C (Month 5-6)
- Coach dashboard
- Session sharing
- API v1 for integrations
- Thai localization

---

## 15. Open Questions

| # | Question | Owner | Blocking? |
|---|----------|-------|-----------|
| Q1 | MiroFish AGPL-3.0 license — can we build a commercial SaaS on top? Need legal review on copyleft implications. | Legal | Yes — must resolve before development |
| Q2 | Optimal agent count per simulation: 100 vs 200 vs 500? Need benchmark for quality vs. cost vs. speed trade-off. | Engineering | No — can start with 100, scale up |
| Q3 | Should future-self chat be real-time streaming or generate full response? UX trade-off: streaming feels more "alive" but harder to filter for safety. | Product + Engineering | No |
| Q4 | PDPA (Thailand), PDP Law (Indonesia) compliance requirements for storing personality data? | Legal | Yes — must resolve before SEA expansion |
| Q5 | Partnership model with coaches: revenue share? flat fee? Do we certify "FutureMe Certified Coaches"? | Business | No — P2 feature |
| Q6 | Can we fine-tune a smaller model on simulation outputs to reduce LLM costs long-term? | Engineering | No — optimization for Month 6+ |
| Q7 | What personality assessment method is most accurate with 5-min conversational input? Big Five? MBTI proxy? Custom model? | Product + Research | No — can iterate |

---

*This is a living document. Last updated: March 15, 2026.*
