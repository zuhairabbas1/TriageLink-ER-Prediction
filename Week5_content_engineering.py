"""
TriageLink Phase 1.2 - Week 5: Content Engineering for RightER Flow
Author: Zuhair Abbas
Purpose: Create educational content, facility type definitions, and analytics schema
Deliverable: education_content.json + facility_types.json + analytics_schema.json
"""

import json
from datetime import datetime

class RightERContentEngineer:
    """
    Content engineering for RightER Flow.
    Focus: Education + Expectation-setting + Non-directive navigation
    """
    
    def __init__(self):
        print("=" * 80)
        print("TRIAGELINK PHASE 1.2 - WEEK 5: CONTENT ENGINEERING")
        print("=" * 80)
        print("\n🎯 RightER Flow Principles:")
        print("   ✅ Education (inform users)")
        print("   ✅ Expectation-setting (manage expectations)")
        print("   ✅ Non-directive navigation (present options, no recommendations)")
        print("\n" + "-" * 80)
        
        self.education_cards = []
        self.facility_types = []
        self.external_directories = []
        self.analytics_events = {}
    
    def create_education_cards(self):
        """
        Create educational content cards for user education.
        Topics: 911, triage, wait times, when to go to ER
        """
        print(f"\n📚 CREATING EDUCATION CARDS")
        print("-" * 80)
        
        self.education_cards = [
            {
                "card_id": "EDU-001",
                "title": "What Happens When You Call 911?",
                "category": "emergency_services",
                "tags": ["911", "emergency", "ambulance"],
                "content": "When you call 911 for a medical emergency, paramedics are dispatched to assess and stabilize you on-site. They determine the most appropriate hospital based on your condition and hospital capacity - not patient preference. 911 is for life-threatening emergencies only.",
                "key_points": [
                    "Paramedics assess your condition on-site",
                    "They choose the hospital based on medical need and capacity",
                    "You cannot request a specific hospital via 911",
                    "Only call 911 for life-threatening emergencies"
                ],
                "call_to_action": "If unsure whether to call 911, err on the side of caution and call.",
                "last_updated": "2025-12-14"
            },
            {
                "card_id": "EDU-002",
                "title": "What is Triage?",
                "category": "emergency_process",
                "tags": ["triage", "priority", "waiting"],
                "content": "Triage is the process hospitals use to prioritize patients based on medical urgency, not arrival time. A nurse assesses your condition when you arrive and assigns a priority level (CTAS 1-5). More urgent cases are seen first, even if they arrived after you.",
                "key_points": [
                    "Patients are prioritized by medical urgency, not arrival order",
                    "CTAS Level 1 (Resuscitation) - immediate",
                    "CTAS Level 2 (Emergent) - within 15 minutes",
                    "CTAS Level 3 (Urgent) - within 30 minutes",
                    "CTAS Level 4-5 (Less urgent) - may wait hours"
                ],
                "call_to_action": "Your wait time depends on how urgent your condition is compared to others.",
                "last_updated": "2025-12-14"
            },
            {
                "card_id": "EDU-003",
                "title": "Why Do ER Wait Times Vary?",
                "category": "wait_times",
                "tags": ["wait_times", "factors", "expectations"],
                "content": "Emergency department wait times fluctuate based on multiple unpredictable factors: current patient volume, severity of cases, available staff, incoming ambulances, and hospital bed availability. Wait times are estimates and can change suddenly.",
                "key_points": [
                    "Wait times are estimates, not guarantees",
                    "Multiple emergencies can arrive simultaneously",
                    "Staff availability affects wait times",
                    "Hospital capacity changes throughout the day",
                    "Your condition may change, affecting priority"
                ],
                "call_to_action": "Expect variability - ERs handle unpredictable emergencies 24/7.",
                "last_updated": "2025-12-14"
            },
            {
                "card_id": "EDU-004",
                "title": "When Should You Go to the Emergency Room?",
                "category": "decision_making",
                "tags": ["emergency", "symptoms", "decision"],
                "content": "Visit the ER for serious, potentially life-threatening conditions: chest pain, difficulty breathing, severe bleeding, head injury with confusion, sudden numbness or weakness, severe allergic reactions, or loss of consciousness. For minor issues, consider urgent care or walk-in clinics.",
                "key_points": [
                    "ER is for serious, potentially life-threatening conditions",
                    "Chest pain, breathing difficulty → ER",
                    "Severe bleeding, head injury → ER",
                    "Minor cuts, sprains, colds → Urgent care or walk-in clinic",
                    "When in doubt, call Telehealth Ontario (1-866-797-0000)"
                ],
                "call_to_action": "Not sure? Call Telehealth Ontario for guidance: 1-866-797-0000",
                "last_updated": "2025-12-14"
            },
            {
                "card_id": "EDU-005",
                "title": "What to Expect in the Emergency Department",
                "category": "emergency_process",
                "tags": ["process", "expectations", "experience"],
                "content": "Your ER visit typically involves: registration, triage assessment, waiting, seeing a doctor, tests or treatment, and discharge or admission. The process can take several hours even for non-emergency cases. Bring your health card, medication list, and be prepared to wait.",
                "key_points": [
                    "Process: Registration → Triage → Waiting → Doctor → Tests → Discharge",
                    "Bring: Health card, medication list, family contact",
                    "Expect several hours, even for minor issues",
                    "You may see multiple staff members",
                    "Tests and procedures take time to complete"
                ],
                "call_to_action": "Prepare for a multi-hour visit and bring essentials.",
                "last_updated": "2025-12-14"
            },
            {
                "card_id": "EDU-006",
                "title": "Understanding CTAS Levels (Canadian Triage Acuity Scale)",
                "category": "triage_system",
                "tags": ["CTAS", "triage", "priority", "urgency"],
                "content": "Canada's emergency departments use the CTAS system to prioritize patients. Level 1 (Resuscitation) is immediate life-threatening, Level 2 (Emergent) is very urgent, Level 3 (Urgent) should be seen within 30 minutes, Level 4 (Less Urgent) within 1-2 hours, and Level 5 (Non-Urgent) within 2-4 hours.",
                "key_points": [
                    "CTAS 1 - Resuscitation (immediate): cardiac arrest, major trauma",
                    "CTAS 2 - Emergent (15 min): chest pain, severe breathing difficulty",
                    "CTAS 3 - Urgent (30 min): moderate pain, minor fractures",
                    "CTAS 4 - Less Urgent (60 min): minor injuries, stable chronic conditions",
                    "CTAS 5 - Non-Urgent (120 min): minor complaints, prescription refills"
                ],
                "call_to_action": "Your triage level determines your wait time priority.",
                "last_updated": "2025-12-14"
            },
            {
                "card_id": "EDU-007",
                "title": "Alternatives to the Emergency Room",
                "category": "alternatives",
                "tags": ["urgent_care", "walk_in", "telehealth", "alternatives"],
                "content": "For non-life-threatening issues, consider alternatives to the ER: Urgent Care Centres (sprains, minor cuts, fever), Walk-in Clinics (cold, flu, rash), Telehealth Ontario (medical advice by phone), or your Family Doctor. These options often have shorter wait times for non-emergencies.",
                "key_points": [
                    "Urgent Care: Open evenings/weekends, no appointment needed",
                    "Walk-in Clinics: Minor illnesses, prescription refills",
                    "Telehealth Ontario: 1-866-797-0000 (free, 24/7 nurse advice)",
                    "Family Doctor: Best for ongoing care and follow-ups",
                    "Pharmacist: Can help with minor ailments and medication questions"
                ],
                "call_to_action": "Save ER visits for true emergencies - explore alternatives for minor issues.",
                "last_updated": "2025-12-14"
            },
            {
                "card_id": "EDU-008",
                "title": "What Information to Bring to the ER",
                "category": "preparation",
                "tags": ["preparation", "documents", "medication"],
                "content": "Arriving prepared helps speed up your ER visit. Bring your Ontario Health Card, photo ID, list of current medications (including dosages), list of allergies, recent test results if applicable, and emergency contact information. Having this ready saves time during registration and triage.",
                "key_points": [
                    "Ontario Health Card (OHIP card) - essential",
                    "Photo ID (driver's license or passport)",
                    "Medication list with dosages and frequency",
                    "Allergy list (medications, foods, environmental)",
                    "Emergency contact phone numbers",
                    "Recent medical records or test results (if relevant)"
                ],
                "call_to_action": "Keep a prepared ER information card in your wallet or phone.",
                "last_updated": "2025-12-14"
            }
        ]
        
        print(f"✅ Created {len(self.education_cards)} education cards")
        for card in self.education_cards:
            print(f"   - {card['card_id']}: {card['title']}")
        
        return self.education_cards
    
    def create_facility_type_definitions(self):
        """
        Create facility type definitions (ED vs Urgent Care vs Walk-in).
        """
        print(f"\n🏥 CREATING FACILITY TYPE DEFINITIONS")
        print("-" * 80)
        
        self.facility_types = [
            {
                "facility_type": "emergency_department",
                "display_name": "Emergency Department (ED)",
                "short_name": "ER/ED",
                "description": "Hospital emergency departments provide 24/7 care for serious, life-threatening conditions. Equipped to handle major trauma, heart attacks, strokes, and severe illnesses. Staffed by emergency physicians, specialists, and equipped with advanced diagnostic tools.",
                "when_to_use": [
                    "Life-threatening emergencies (chest pain, difficulty breathing)",
                    "Severe injuries (major trauma, head injury with loss of consciousness)",
                    "Suspected heart attack or stroke",
                    "Severe allergic reactions",
                    "Severe bleeding that won't stop",
                    "Poisoning or overdose"
                ],
                "services_available": [
                    "24/7 emergency care",
                    "Advanced diagnostic imaging (CT, MRI, X-ray)",
                    "Emergency surgery capability",
                    "Intensive care units",
                    "Specialist consultations",
                    "Ambulance access"
                ],
                "typical_wait_time": "Variable (15 min to 8+ hours based on triage level)",
                "cost": "Covered by OHIP (Ontario Health Insurance)",
                "icon": "hospital",
                "priority_level": 1
            },
            {
                "facility_type": "urgent_care_centre",
                "display_name": "Urgent Care Centre",
                "short_name": "Urgent Care",
                "description": "Urgent care centres handle non-life-threatening injuries and illnesses that require same-day attention but aren't severe enough for the ER. Walk-in, no appointment needed. Extended hours including evenings and weekends.",
                "when_to_use": [
                    "Minor fractures or sprains",
                    "Cuts requiring stitches (not severe bleeding)",
                    "Moderate fever or flu symptoms",
                    "Minor burns",
                    "Infections (ear, urinary tract)",
                    "Allergic reactions (non-severe)"
                ],
                "services_available": [
                    "X-rays and basic diagnostics",
                    "Stitches and wound care",
                    "Splinting for minor fractures",
                    "IV fluids",
                    "Prescription medications",
                    "Extended hours (evenings/weekends)"
                ],
                "typical_wait_time": "30 minutes to 3 hours",
                "cost": "Covered by OHIP (Ontario Health Insurance)",
                "icon": "urgent_care",
                "priority_level": 2
            },
            {
                "facility_type": "walk_in_clinic",
                "display_name": "Walk-in Clinic",
                "short_name": "Walk-in",
                "description": "Walk-in clinics provide same-day care for minor illnesses and injuries. No appointment needed, but hours are typically limited to daytime/early evening. Good for issues that aren't urgent but need attention within 24-48 hours.",
                "when_to_use": [
                    "Cold, flu, or sore throat",
                    "Minor rashes or skin irritations",
                    "Prescription refills",
                    "Minor cuts or scrapes",
                    "Vaccination or travel medicine",
                    "Physical examinations or forms"
                ],
                "services_available": [
                    "Basic medical assessments",
                    "Prescription medications",
                    "Minor wound care",
                    "Vaccinations and immunizations",
                    "Lab requisitions",
                    "Medical notes and forms"
                ],
                "typical_wait_time": "15 minutes to 2 hours",
                "cost": "Covered by OHIP (Ontario Health Insurance)",
                "icon": "clinic",
                "priority_level": 3
            },
            {
                "facility_type": "telehealth",
                "display_name": "Telehealth Ontario",
                "short_name": "Telehealth",
                "description": "Free, confidential telephone service providing health advice and information from registered nurses 24 hours a day, 7 days a week. Can help you decide if you need to see a doctor, go to an ER, or if you can care for yourself at home.",
                "when_to_use": [
                    "Unsure if you need medical attention",
                    "Health questions or concerns",
                    "Medication information",
                    "Help deciding where to seek care",
                    "Advice on managing symptoms at home"
                ],
                "services_available": [
                    "24/7 registered nurse consultation by phone",
                    "Confidential health advice",
                    "Language interpretation available (multiple languages)",
                    "TTY service for hearing impaired (1-866-797-0007)"
                ],
                "typical_wait_time": "Immediate to 15 minutes",
                "cost": "Free",
                "phone": "1-866-797-0000",
                "icon": "phone",
                "priority_level": 4
            }
        ]
        
        print(f"✅ Created {len(self.facility_types)} facility type definitions")
        for ftype in self.facility_types:
            print(f"   - {ftype['facility_type']}: {ftype['display_name']}")
        
        return self.facility_types
    
    def create_external_directory_links(self):
        """
        Create external directory links for handoff to authoritative sources.
        """
        print(f"\n🔗 CREATING EXTERNAL DIRECTORY LINKS")
        print("-" * 80)
        
        self.external_directories = [
            {
                "directory_id": "EXT-001",
                "name": "Ontario Health - Find Healthcare Services",
                "description": "Official Ontario government tool to find hospitals, clinics, and healthcare providers in your area.",
                "url": "https://www.ontario.ca/page/find-healthcare-services",
                "category": "government",
                "reliability": "authoritative",
                "last_verified": "2025-12-14"
            },
            {
                "directory_id": "EXT-002",
                "name": "Health Care Connect",
                "description": "Free service to help you find a family doctor or nurse practitioner in Ontario.",
                "url": "https://www.ontario.ca/page/find-family-doctor-or-nurse-practitioner",
                "category": "primary_care",
                "reliability": "authoritative",
                "last_verified": "2025-12-14"
            },
            {
                "directory_id": "EXT-003",
                "name": "Telehealth Ontario",
                "description": "24/7 free health advice from registered nurses by phone.",
                "url": "https://www.ontario.ca/page/get-medical-advice-telehealth-ontario",
                "phone": "1-866-797-0000",
                "category": "telehealth",
                "reliability": "authoritative",
                "last_verified": "2025-12-14"
            },
            {
                "directory_id": "EXT-004",
                "name": "College of Physicians and Surgeons of Ontario - Doctor Search",
                "description": "Verify a physician's credentials and find doctors by location or specialty.",
                "url": "https://www.cpso.on.ca/Public-Information-Services/Find-a-Doctor",
                "category": "physician_lookup",
                "reliability": "authoritative",
                "last_verified": "2025-12-14"
            },
            {
                "directory_id": "EXT-005",
                "name": "Ontario Hospitals - OHA Member Directory",
                "description": "Ontario Hospital Association's directory of member hospitals.",
                "url": "https://www.oha.com/",
                "category": "hospital_directory",
                "reliability": "professional_association",
                "last_verified": "2025-12-14"
            }
        ]
        
        print(f"✅ Created {len(self.external_directories)} external directory links")
        for directory in self.external_directories:
            print(f"   - {directory['directory_id']}: {directory['name']}")
        
        return self.external_directories
    
    def create_analytics_event_schema(self):
        """
        Create analytics event schema for measuring KPIs.
        Focus: page views, link clicks, navigation patterns
        """
        print(f"\n📊 CREATING ANALYTICS EVENT SCHEMA")
        print("-" * 80)
        
        self.analytics_events = {
            "schema_version": "1.0",
            "last_updated": "2025-12-14",
            "events": [
                {
                    "event_name": "page_view",
                    "description": "User views a page",
                    "properties": {
                        "page_url": "string (required)",
                        "page_title": "string (required)",
                        "referrer": "string (optional)",
                        "session_id": "string (required)",
                        "user_id": "string (optional - anonymous if not logged in)",
                        "timestamp": "datetime (required)",
                        "device_type": "string (mobile|tablet|desktop)",
                        "browser": "string"
                    },
                    "example": {
                        "event_name": "page_view",
                        "page_url": "/map",
                        "page_title": "GTA Hospital Map",
                        "referrer": "/home",
                        "session_id": "abc123",
                        "timestamp": "2025-12-14T15:30:00Z",
                        "device_type": "mobile",
                        "browser": "Chrome"
                    }
                },
                {
                    "event_name": "education_card_view",
                    "description": "User views an education card",
                    "properties": {
                        "card_id": "string (required)",
                        "card_title": "string (required)",
                        "category": "string (required)",
                        "session_id": "string (required)",
                        "timestamp": "datetime (required)",
                        "view_duration_seconds": "integer (optional)"
                    },
                    "example": {
                        "event_name": "education_card_view",
                        "card_id": "EDU-001",
                        "card_title": "What Happens When You Call 911?",
                        "category": "emergency_services",
                        "session_id": "abc123",
                        "timestamp": "2025-12-14T15:31:00Z",
                        "view_duration_seconds": 45
                    }
                },
                {
                    "event_name": "link_out_click",
                    "description": "User clicks an external link",
                    "properties": {
                        "link_url": "string (required)",
                        "link_text": "string (required)",
                        "link_category": "string (government|hospital|directory|telehealth)",
                        "source_page": "string (required)",
                        "session_id": "string (required)",
                        "timestamp": "datetime (required)"
                    },
                    "example": {
                        "event_name": "link_out_click",
                        "link_url": "https://www.ontario.ca/page/find-healthcare-services",
                        "link_text": "Ontario Health - Find Healthcare Services",
                        "link_category": "government",
                        "source_page": "/resources",
                        "session_id": "abc123",
                        "timestamp": "2025-12-14T15:32:00Z"
                    }
                },
                {
                    "event_name": "hospital_marker_click",
                    "description": "User clicks a hospital marker on the map",
                    "properties": {
                        "facility_id": "string (required)",
                        "facility_name": "string (required)",
                        "region": "string (required)",
                        "session_id": "string (required)",
                        "timestamp": "datetime (required)",
                        "user_lat": "float (optional - user location if shared)",
                        "user_lng": "float (optional)",
                        "distance_km": "float (optional - calculated distance)"
                    },
                    "example": {
                        "event_name": "hospital_marker_click",
                        "facility_id": "GTA-H-001",
                        "facility_name": "Toronto General Hospital",
                        "region": "Toronto",
                        "session_id": "abc123",
                        "timestamp": "2025-12-14T15:33:00Z",
                        "distance_km": 5.2
                    }
                },
                {
                    "event_name": "facility_filter_applied",
                    "description": "User filters hospitals by region or type",
                    "properties": {
                        "filter_type": "string (region|facility_type)",
                        "filter_value": "string (required)",
                        "results_count": "integer (required)",
                        "session_id": "string (required)",
                        "timestamp": "datetime (required)"
                    },
                    "example": {
                        "event_name": "facility_filter_applied",
                        "filter_type": "region",
                        "filter_value": "Toronto",
                        "results_count": 10,
                        "session_id": "abc123",
                        "timestamp": "2025-12-14T15:34:00Z"
                    }
                },
                {
                    "event_name": "survey_complete",
                    "description": "User completes a feedback survey",
                    "properties": {
                        "survey_id": "string (required)",
                        "survey_type": "string (satisfaction|usability|feedback)",
                        "responses": "object (question_id: answer)",
                        "session_id": "string (required)",
                        "timestamp": "datetime (required)"
                    },
                    "example": {
                        "event_name": "survey_complete",
                        "survey_id": "survey_2025_12",
                        "survey_type": "satisfaction",
                        "responses": {
                            "q1_helpful": 5,
                            "q2_clear": 4,
                            "q3_comments": "Very useful for finding hospitals"
                        },
                        "session_id": "abc123",
                        "timestamp": "2025-12-14T15:40:00Z"
                    }
                },
                {
                    "event_name": "distance_calculation",
                    "description": "User requests distance calculation from their location",
                    "properties": {
                        "facility_id": "string (required)",
                        "distance_km": "float (required)",
                        "calculation_method": "string (browser_geolocation|postal_code_entry)",
                        "session_id": "string (required)",
                        "timestamp": "datetime (required)"
                    },
                    "example": {
                        "event_name": "distance_calculation",
                        "facility_id": "GTA-H-001",
                        "distance_km": 5.2,
                        "calculation_method": "browser_geolocation",
                        "session_id": "abc123",
                        "timestamp": "2025-12-14T15:35:00Z"
                    }
                }
            ],
            "kpi_metrics": {
                "engagement": [
                    "total_page_views",
                    "unique_visitors",
                    "avg_session_duration",
                    "education_card_views_per_session"
                ],
                "navigation": [
                    "hospital_marker_clicks",
                    "filter_usage_rate",
                    "distance_calculations_per_session"
                ],
                "link_out": [
                    "total_external_link_clicks",
                    "link_out_click_rate",
                    "most_clicked_external_resources"
                ],
                "satisfaction": [
                    "survey_completion_rate",
                    "average_satisfaction_score",
                    "feedback_sentiment"
                ]
            }
        }
        
        print(f"✅ Created analytics event schema")
        print(f"   Events defined: {len(self.analytics_events['events'])}")
        for event in self.analytics_events['events']:
            print(f"   - {event['event_name']}")
        
        return self.analytics_events
    
    def create_non_directive_navigation_constraints(self):
        """
        Create constraints for non-directive navigation.
        NO recommendations, only display options.
        """
        print(f"\n⚠️  CREATING NON-DIRECTIVE NAVIGATION CONSTRAINTS")
        print("-" * 80)
        
        constraints = {
            "non_directive_principles": {
                "title": "Non-Directive Navigation Constraints",
                "description": "RightER Flow presents options without making recommendations or directing users to specific facilities.",
                "last_updated": "2025-12-14"
            },
            "forbidden_language": [
                "You should go to...",
                "We recommend...",
                "Best option for you is...",
                "This hospital is better than...",
                "Go here instead of...",
                "You need to visit...",
                "The right choice is..."
            ],
            "allowed_language": [
                "Here are hospitals in your area",
                "Options include...",
                "Facilities available:",
                "You can choose from...",
                "These facilities are available",
                "Sorted by distance",
                "Listed alphabetically"
            ],
            "sorting_options": {
                "allowed": [
                    "alphabetical (A-Z)",
                    "distance (nearest first)",
                    "region (grouped by area)"
                ],
                "forbidden": [
                    "recommended",
                    "best match",
                    "most suitable",
                    "highest rated",
                    "fastest wait time"
                ]
            },
            "display_rules": {
                "facility_listing": "Display all facilities equally with no visual hierarchy based on recommendation",
                "distance_calculation": "Show distance as neutral information, not as a suggestion",
                "facility_details": "Present factual information (address, contact, type) without editorial comments",
                "wait_time_display": "If available in future, show as estimate with disclaimer, not as decisive factor"
            },
            "backend_constraints": {
                "api_responses": "Return facilities in neutral order (alphabetical or distance-based) with no 'recommended' flag",
                "no_filtering_logic": "Do not filter out facilities based on assumed user preferences",
                "equal_representation": "All facilities receive equal data completeness and quality"
            },
            "educational_approach": {
                "inform": "Provide factual education about facility types and when to seek care",
                "empower": "Give users information to make their own informed decisions",
                "avoid_directing": "Do not tell users where to go or what to do"
            },
            "legal_disclaimers": [
                "This tool is for informational purposes only",
                "Not a substitute for medical advice",
                "In emergencies, call 911",
                "Consult healthcare professionals for medical decisions"
            ]
        }
        
        print(f"✅ Created non-directive navigation constraints")
        print(f"   Forbidden language patterns: {len(constraints['forbidden_language'])}")
        print(f"   Allowed sorting methods: {len(constraints['sorting_options']['allowed'])}")
        
        return constraints
    
    def save_all_content(self):
        """
        Save all content to JSON files.
        """
        print(f"\n💾 SAVING CONTENT FILES")
        print("-" * 80)
        
        # Save education cards
        with open('education_content.json', 'w') as f:
            json.dump({
                "content_type": "education_cards",
                "version": "1.0",
                "last_updated": "2025-12-14",
                "total_cards": len(self.education_cards),
                "cards": self.education_cards
            }, f, indent=2)
        print(f"✅ Saved: education_content.json ({len(self.education_cards)} cards)")
        
        # Save facility types
        with open('facility_types.json', 'w') as f:
            json.dump({
                "content_type": "facility_type_definitions",
                "version": "1.0",
                "last_updated": "2025-12-14",
                "total_types": len(self.facility_types),
                "facility_types": self.facility_types
            }, f, indent=2)
        print(f"✅ Saved: facility_types.json ({len(self.facility_types)} types)")
        
        # Save external directories
        with open('external_directories.json', 'w') as f:
            json.dump({
                "content_type": "external_directory_links",
                "version": "1.0",
                "last_updated": "2025-12-14",
                "total_directories": len(self.external_directories),
                "directories": self.external_directories
            }, f, indent=2)
        print(f"✅ Saved: external_directories.json ({len(self.external_directories)} links)")
        
        # Save analytics schema
        with open('analytics_schema.json', 'w') as f:
            json.dump(self.analytics_events, f, indent=2)
        print(f"✅ Saved: analytics_schema.json ({len(self.analytics_events['events'])} events)")
        
        # Save non-directive constraints
        constraints = self.create_non_directive_navigation_constraints()
        with open('non_directive_constraints.json', 'w') as f:
            json.dump(constraints, f, indent=2)
        print(f"✅ Saved: non_directive_constraints.json")
    
    def run_full_pipeline(self):
        """
        Run complete content engineering pipeline.
        """
        # Step 1: Create education cards
        self.create_education_cards()
        
        # Step 2: Create facility type definitions
        self.create_facility_type_definitions()
        
        # Step 3: Create external directory links
        self.create_external_directory_links()
        
        # Step 4: Create analytics event schema
        self.create_analytics_event_schema()
        
        # Step 5: Create non-directive navigation constraints
        constraints = self.create_non_directive_navigation_constraints()
        
        # Step 6: Save all content
        self.save_all_content()
        
        print("\n" + "=" * 80)
        print("✅ WEEK 5 CONTENT ENGINEERING COMPLETE!")
        print("=" * 80)
        print(f"\n📁 Deliverables:")
        print(f"   - education_content.json ({len(self.education_cards)} education cards)")
        print(f"   - facility_types.json ({len(self.facility_types)} facility types)")
        print(f"   - external_directories.json ({len(self.external_directories)} external links)")
        print(f"   - analytics_schema.json ({len(self.analytics_events['events'])} event types)")
        print(f"   - non_directive_constraints.json (navigation rules)")
        print(f"\n📊 Ready for Backend API Implementation (Vishaal)")
        print(f"📊 Ready for Frontend Integration")
        
        return {
            'education_cards': self.education_cards,
            'facility_types': self.facility_types,
            'external_directories': self.external_directories,
            'analytics_events': self.analytics_events,
            'constraints': constraints
        }


# Example usage
if __name__ == "__main__":
    engineer = RightERContentEngineer()
    results = engineer.run_full_pipeline()
    
    print("\n✅ Content engineering complete!")
    print(f"   Education cards: {len(results['education_cards'])}")
    print(f"   Facility types: {len(results['facility_types'])}")
    print(f"   External links: {len(results['external_directories'])}")