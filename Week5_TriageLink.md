# TriageLink Phase 1.2 - Week 5 Deliverable

**Project:** TriageLink - RightER Flow Content Engineering  
**Team Member:** Zuhair Abbas (Content Engineering Support)  
**Week:** 5 of 6 | December 15-21, 2025  
**Hours:** 10 hours  
**Phase:** 1.2 - Backend Content + Analytics Preparation

---

## Objective

Create educational content, facility type definitions, external directory links, and analytics schema to support **RightER Flow**: Education + Expectation-setting + Non-directive navigation.

---

## RightER Flow Principles (Per Tony's Direction)

### ✅ **Education**
Inform users about emergency services, triage, alternatives

### ✅ **Expectation-Setting**
Manage user expectations about wait times, processes, variability

### ✅ **Non-Directive Navigation**
Present options without recommendations or "go here" language

---

## Tasks Completed

### Task 1: Education Content Cards (3 hours) ✅

Created **8 educational content cards** covering key topics:

1. **EDU-001: What Happens When You Call 911?**
   - Target: Users unsure about 911 vs self-transport
   - Key message: Paramedics choose hospital, not patient
   
2. **EDU-002: What is Triage?**
   - Target: Users frustrated by wait times
   - Key message: Priority by urgency, not arrival time

3. **EDU-003: Why Do ER Wait Times Vary?**
   - Target: Managing expectations
   - Key message: Wait times are estimates with many variables

4. **EDU-004: When Should You Go to the Emergency Room?**
   - Target: Decision-making support
   - Key message: ER for life-threatening, alternatives for minor

5. **EDU-005: What to Expect in the Emergency Department**
   - Target: First-time ER visitors
   - Key message: Multi-hour process with multiple steps

6. **EDU-006: Understanding CTAS Levels**
   - Target: Understanding priority system
   - Key message: 5 levels from immediate to 2-4 hours

7. **EDU-007: Alternatives to the Emergency Room**
   - Target: Redirecting non-emergencies
   - Key message: Urgent care, walk-in, Telehealth options

8. **EDU-008: What Information to Bring to the ER**
   - Target: Preparation guidance
   - Key message: Health card, medications, allergies, contacts

**Content Structure:**
- Title, category, tags
- Main content (2-3 paragraphs)
- Key points (bullet list)
- Call to action
- Last updated date

### Task 2: Facility Type Definitions (2 hours) ✅

Created **4 facility type definitions** for user education:

1. **Emergency Department (ED)**
   - When to use: Life-threatening emergencies
   - Services: 24/7, advanced diagnostics, surgery, ICU
   - Typical wait: Variable (15 min to 8+ hours)
   - Priority level: 1

2. **Urgent Care Centre**
   - When to use: Non-life-threatening but same-day needs
   - Services: X-rays, stitches, minor fractures, extended hours
   - Typical wait: 30 min to 3 hours
   - Priority level: 2

3. **Walk-in Clinic**
   - When to use: Minor illnesses, prescription refills
   - Services: Basic assessments, vaccinations, forms
   - Typical wait: 15 min to 2 hours
   - Priority level: 3

4. **Telehealth Ontario**
   - When to use: Health advice, unsure where to go
   - Services: 24/7 nurse consultation by phone
   - Typical wait: Immediate to 15 min
   - Priority level: 4
   - Phone: 1-866-797-0000

**Purpose:** Help users understand which facility type matches their needs

### Task 3: External Directory Links (1 hour) ✅

Created **5 external directory links** for handoff to authoritative sources:

1. **Ontario Health - Find Healthcare Services**
   - Official government directory
   - Category: government
   - Reliability: authoritative

2. **Health Care Connect**
   - Find family doctor/nurse practitioner
   - Category: primary_care
   - Reliability: authoritative

3. **Telehealth Ontario**
   - 24/7 health advice by phone
   - Category: telehealth
   - Phone: 1-866-797-0000
   - Reliability: authoritative

4. **College of Physicians and Surgeons of Ontario - Doctor Search**
   - Verify physician credentials
   - Category: physician_lookup
   - Reliability: authoritative

5. **Ontario Hospital Association Member Directory**
   - Hospital directory
   - Category: hospital_directory
   - Reliability: professional_association

**Purpose:** Link out to comprehensive directories (we don't maintain one)

### Task 4: Analytics Event Schema (3 hours) ✅

Created **analytics schema** with **7 event types** for KPI measurement:

1. **page_view** - User views a page
   - Properties: page_url, page_title, referrer, session_id, timestamp, device_type

2. **education_card_view** - User views education card
   - Properties: card_id, card_title, category, view_duration_seconds

3. **link_out_click** - User clicks external link
   - Properties: link_url, link_text, link_category, source_page

4. **hospital_marker_click** - User clicks hospital on map
   - Properties: facility_id, facility_name, region, distance_km

5. **facility_filter_applied** - User filters by region/type
   - Properties: filter_type, filter_value, results_count

6. **survey_complete** - User completes feedback survey
   - Properties: survey_id, survey_type, responses

7. **distance_calculation** - User requests distance calculation
   - Properties: facility_id, distance_km, calculation_method

**KPI Metrics Defined:**
- **Engagement:** page_views, unique_visitors, session_duration
- **Navigation:** marker_clicks, filter_usage, distance_calculations
- **Link-out:** external_link_clicks, click_rate, top_resources
- **Satisfaction:** survey_completion_rate, satisfaction_score

### Task 5: Non-Directive Navigation Constraints (1 hour) ✅

Created **navigation constraints** ensuring RightER Flow compliance:

**Forbidden Language:**
- ❌ "You should go to..."
- ❌ "We recommend..."
- ❌ "Best option for you is..."
- ❌ "This hospital is better than..."

**Allowed Language:**
- ✅ "Here are hospitals in your area"
- ✅ "Options include..."
- ✅ "Sorted by distance"
- ✅ "Listed alphabetically"

**Allowed Sorting:**
- ✅ Alphabetical (A-Z)
- ✅ Distance (nearest first)
- ✅ Region (grouped by area)

**Forbidden Sorting:**
- ❌ Recommended
- ❌ Best match
- ❌ Fastest wait time
- ❌ Highest rated

**Legal Disclaimers:**
- "This tool is for informational purposes only"
- "Not a substitute for medical advice"
- "In emergencies, call 911"
- "Consult healthcare professionals for medical decisions"

---

## Deliverables

### Primary Content Files:

1. **education_content.json** (7.9 KB)
   - 8 education cards
   - Structured with card_id, title, category, tags, content, key_points
   - Ready for backend `/education` endpoint

2. **facility_types.json** (4.5 KB)
   - 4 facility type definitions
   - ED, Urgent Care, Walk-in, Telehealth
   - Ready for backend `/facility-types` endpoint

3. **external_directories.json** (2.1 KB)
   - 5 authoritative external links
   - Government and professional sources
   - Ready for backend `/external-links` endpoint

4. **analytics_schema.json** (5.8 KB)
   - 7 event types defined
   - Complete property schemas with examples
   - Ready for analytics implementation

5. **non_directive_constraints.json** (2.3 KB)
   - Navigation rules and forbidden language
   - Sorting constraints
   - Legal disclaimers

### Supporting Code:

6. **Week5_content_engineering.py**
   - Automated content generation pipeline
   - Reusable for future content updates

---

## Content Quality Metrics

### Education Cards:
- ✅ 8/8 cards complete
- ✅ All cards tagged and categorized
- ✅ Key points extracted for scanning
- ✅ Call-to-action included
- ✅ Medically accurate (reviewed against authoritative sources)

### Facility Types:
- ✅ 4/4 types defined
- ✅ "When to use" guidance clear
- ✅ Services listed comprehensively
- ✅ Wait time expectations set realistically

### External Links:
- ✅ 5/5 links verified active
- ✅ All links authoritative (government/professional)
- ✅ Reliability ratings assigned
- ✅ Last verified dates included

### Analytics Schema:
- ✅ 7 core event types defined
- ✅ All properties documented
- ✅ Examples provided
- ✅ KPI metrics mapped

---

## Backend API Recommendations (For Vishaal)

### Suggested Endpoints:

**1. GET /api/education**
- Returns all education cards
- Optional filter by category or tag
```json
{
  "cards": [...],
  "total": 8
}
```

**2. GET /api/education/:card_id**
- Returns specific education card
```json
{
  "card_id": "EDU-001",
  "title": "What Happens When You Call 911?",
  ...
}
```

**3. GET /api/facility-types**
- Returns all facility type definitions
```json
{
  "facility_types": [...],
  "total": 4
}
```

**4. GET /api/external-links**
- Returns external directory links
```json
{
  "directories": [...],
  "total": 5
}
```

**5. POST /api/analytics/event**
- Records analytics event
- Request body matches event schema
```json
{
  "event_name": "page_view",
  "properties": {...}
}
```

**6. GET /api/hospitals** (from Week 4)
- Returns GTA hospital list
- Supports filtering by region
- Supports distance-based sorting

---

## Non-Directive Navigation Implementation

### Backend Constraints:

**API Response Design:**
```json
{
  "hospitals": [
    {
      "facility_id": "GTA-H-001",
      "name": "Toronto General Hospital",
      "distance_km": 5.2,
      // NO "recommended": true
      // NO "best_match_score": 0.95
    }
  ],
  "sort_order": "distance_ascending", // neutral description
  "total": 25
}
```

**What NOT to Include:**
- ❌ Recommendation flags
- ❌ Quality scores or ratings
- ❌ "Best for you" labels
- ❌ Predictive matching algorithms

**What TO Include:**
- ✅ Neutral sorting (alphabetical, distance)
- ✅ Complete facility information
- ✅ Equal representation of all facilities

---

## Frontend Integration Notes

### Education Cards Display:
- Display in categorized sections or searchable list
- Show key points as expandable/collapsible
- Track `education_card_view` events
- Include "Last updated" dates for transparency

### Facility Type Selector:
- Present 4 types as decision aid (not recommendation)
- Show "When to use" and "Typical wait" for expectations
- Link to detailed definitions

### Hospital Map:
- Display markers without visual hierarchy
- Sort by distance OR alphabetical (user choice)
- Show distance as factual data, not suggestion
- Track `hospital_marker_click` events

### External Link Handoff:
- Clear labels: "For comprehensive hospital directory, visit..."
- Track `link_out_click` events
- Open in new tab

---

## Sample Content Examples

### Education Card (EDU-001):
```json
{
  "card_id": "EDU-001",
  "title": "What Happens When You Call 911?",
  "category": "emergency_services",
  "content": "When you call 911 for a medical emergency, paramedics are dispatched to assess and stabilize you on-site. They determine the most appropriate hospital based on your condition and hospital capacity - not patient preference. 911 is for life-threatening emergencies only.",
  "key_points": [
    "Paramedics assess your condition on-site",
    "They choose the hospital based on medical need and capacity",
    "You cannot request a specific hospital via 911",
    "Only call 911 for life-threatening emergencies"
  ]
}
```

### Facility Type (Emergency Department):
```json
{
  "facility_type": "emergency_department",
  "display_name": "Emergency Department (ED)",
  "when_to_use": [
    "Life-threatening emergencies (chest pain, difficulty breathing)",
    "Severe injuries (major trauma, head injury)",
    "Suspected heart attack or stroke"
  ],
  "typical_wait_time": "Variable (15 min to 8+ hours based on triage level)"
}
```

---

## Alignment with Tony's Direction

### ✅ NOT Building a Full Facility Directory
- Week 4 dataset = demo/pilot only (25 hospitals)
- External links handoff to authoritative directories
- No ongoing directory maintenance

### ✅ RightER Flow Principles
- Education: 8 cards inform users
- Expectation-setting: Realistic wait times, process explanations
- Non-directive: Constraints prevent recommendations

### ✅ Backend + Content Engineering Focus
- Content models defined
- API endpoints recommended
- Analytics schema ready

### ✅ Measuring KPIs
- 7 event types track engagement, navigation, link-outs
- Survey completion for satisfaction
- Analytics ready for implementation

---

## Time Breakdown

| Task | Planned | Actual | Status |
|------|---------|--------|--------|
| Education cards | 3h | 3h | ✅ |
| Facility types | 2h | 2h | ✅ |
| External links | 1h | 1h | ✅ |
| Analytics schema | 3h | 3h | ✅ |
| Navigation constraints | 1h | 1h | ✅ |
| **TOTAL** | **10h** | **10h** | **✅ On schedule** |

---

## Files for Submission

1. ✅ **education_content.json** - 8 education cards
2. ✅ **facility_types.json** - 4 facility type definitions
3. ✅ **external_directories.json** - 5 external links
4. ✅ **analytics_schema.json** - 7 event types
5. ✅ **non_directive_constraints.json** - Navigation rules
6. ✅ **Week5_content_engineering.py** - Content pipeline
7. ✅ **Week5_Phase1.2_Documentation.md** - This document

---

## Next Steps (Week 6)

**Backend (Vishaal):**
- Implement content API endpoints
- Serve JSON files via static endpoints or API
- Add analytics event logging endpoint
- Ensure non-directive constraints in responses

**Frontend:**
- Integrate education cards into UI
- Display facility type selector
- Implement external link handoffs
- Add analytics event tracking

**Testing:**
- Verify no recommendation language
- Test analytics event collection
- Validate education content accuracy

---

**Status:** ✅ WEEK 5 COMPLETE - CONTENT READY FOR BACKEND

**Prepared by:** Zuhair Abbas | December, 2025  
**Next:** Week 6 - Integration Testing & Demo Preparation