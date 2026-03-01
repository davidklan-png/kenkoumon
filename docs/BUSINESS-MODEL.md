# Kenkoumon — Business Model

## Revenue Model

### Primary: Patient Subscription
- **Price:** ¥1,500/month (~$10 USD)
- **Includes:** Unlimited visit recording and processing, longitudinal profile maintenance, document ingestion (post-MVP), data export
- **Free tier:** One visit recording and report — enough to prove value before subscribing

### Why Subscription Over Per-Session
- Per-session pricing (¥500-2,000/visit) penalizes frequent use
- Subscription aligns incentives: patient uses the product more, data gets richer, value compounds
- Longitudinal profile only makes sense with recurring access
- Predictable revenue for the business

### Future Revenue Streams (Not V1)
- **Clinic subscription** (Stage 5): Clinics pay for enhanced features (patient report dashboard, aggregate insights). Only viable after patient adoption proves demand.
- **Premium tier:** Advanced features like AI-powered visit preparation, multi-language export, family accounts
- **API access:** Third-party health apps can access patient data (with patient consent) via paid API

---

## Target Market

### V1 Beachhead: English-Speaking Expats in Japan

**Market sizing:**
- Foreign residents in Japan: ~3.2 million (2024)
- English-speaking subset (US, UK, Australia, India, Philippines, international): ~500K-800K
- Those who visit doctors at least annually: ~60-70% → ~350K-500K
- Those who would consider a health app: ~20-30% → ~70K-150K
- Realistic early addressable market: ~70K-150K potential users

**Willingness to pay:** High. Expats already pay for translation services, medical interpreters (¥5,000-15,000/visit), and health navigation apps. ¥1,500/month is a fraction of one interpreter session.

**Pain intensity:** Very high. Medical miscommunication in a foreign language is a top-3 expat concern globally. Existing solutions (bring a friend, use Google Translate, hope for the best) are inadequate.

### Expansion Markets (Post-Validation)

| Market | Timing | Size | Notes |
|---|---|---|---|
| Japanese patients wanting better doctor communication | Stage 3 | ~30M adults who visit clinics annually | Requires Japanese-only mode, different value prop |
| Medical tourists to Japan | Stage 3 | Growing market, especially from Asia | Short-term high-value users |
| Expats in Korea, Singapore, Taiwan | Stage 4 | Similar dynamics, different languages | Requires new language pipelines |
| US/EU patients wanting health data ownership | Stage 5 | Massive but different regulatory environment | Longer-term opportunity |

---

## Unit Economics (Estimated — Pre-Validation)

### Cost Per User Per Month

| Item | Estimated Cost | Notes |
|---|---|---|
| Transcription (Whisper API) | ¥50-100/session | ~15 min audio per session, 1-2 sessions/month |
| LLM processing (report generation) | ¥30-80/session | Claude/GPT-4 API costs for extraction + report |
| Infrastructure (hosting, storage) | ¥100-200/user/month | Japan-region cloud, encrypted storage |
| **Total variable cost** | **¥200-500/user/month** | |

### Margins
- Revenue per user: ¥1,500/month
- Variable cost per user: ¥200-500/month
- **Gross margin: 65-85%**
- At scale, AI API costs decrease (bulk pricing, fine-tuned models, on-device processing)

### Path to Break-Even
- Fixed costs (team, infrastructure baseline, legal): ~¥2-3M/month initially (lean team)
- Break-even subscribers: ~1,500-2,000 paying users
- At expat market penetration of 1-3%: 700-4,500 users → break-even achievable within first year of launch if penetration exceeds 2%

---

## Customer Acquisition

### Channel Strategy (Expat Market)

| Channel | Cost | Expected Effectiveness |
|---|---|---|
| Expat community forums (Reddit Japan, GaijinPot, Japan subreddits) | Free-Low | High — word of mouth in tight community |
| International clinics in Tokyo/Osaka | Free (partnership) | High — clinics can recommend to patients |
| Expat Facebook groups | Low | Medium-High — large, active communities |
| Medical interpreter referrals | Free (partnership) | Medium — interpreters could recommend for follow-up |
| Content marketing (blog: "navigating Japanese healthcare") | Low | Medium — SEO for high-intent searches |
| App Store / Google Play organic | Free | Medium — if reviews are strong |

### Key Insight
The expat community in Japan is tight-knit and recommendation-driven. One viral post on r/japanlife or a recommendation from a popular expat blog could drive hundreds of signups. The product demo is inherently shareable: "Look at this report my app generated from my doctor's visit."

### Target: First 100 Paying Users
1. Personal network of expats (founder + contacts): 10-20 users
2. Reddit/community posts with Experiment Zero results: 20-50 users
3. Partnership with 2-3 international clinics in Tokyo: 30-50 users
4. Timeline: within 3 months of app launch

---

## Competitive Positioning

### What Exists Today

| Competitor | What They Do | What They Don't Do |
|---|---|---|
| Nuance DAX | Doctor-side documentation automation | Patient-facing, multilingual, psychological insight |
| Abridge | Visit recording + patient summary (English) | Japanese, doctor briefing, longitudinal profile |
| Google Translate | Real-time translation | Medical context, structured extraction, reports |
| Medical interpreters | In-visit translation | Post-visit reports, longitudinal tracking, affordability |
| Japan medical tourism apps | Booking, basic translation | Recording, analysis, ongoing care support |

### Kenkoumon's Unique Position
**The only product that turns a Japanese medical conversation into a structured, bilingual health record the patient owns and the doctor can use.**

No competitor does all of:
1. Japanese medical audio transcription
2. Structured entity extraction (bilingual)
3. Doctor-facing report in Japanese
4. Patient-facing summary in English
5. Patient-owned longitudinal profile
6. AI-agnostic data export

---

## Key Business Assumptions to Validate

| Assumption | Validation Method | Required Confidence |
|---|---|---|
| Doctors will read AI-generated patient reports | Experiment Zero: doctor feedback | Direct confirmation from 3+ doctors |
| Expats will pay ¥1,500/month | Validation phase: interviews + signup | >50% stated willingness, >5% conversion |
| Japanese transcription is accurate enough | Experiment Zero: accuracy measurement | >95% medical term accuracy |
| Patients will record regularly (not just once) | MVP tracking: repeat session rate | >40% of users record 2+ times in first 3 months |
| Word of mouth drives acquisition | MVP tracking: referral source | >30% of users from organic/referral |
