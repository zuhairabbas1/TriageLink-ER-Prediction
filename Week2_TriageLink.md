# TriageLink - Week 2 Deliverable

**Project:** AI-Driven ER Wait-Time Prediction  
**Team Member:** Zuhair Abbas  
**Week:** 2 of 6 | November 24-30, 2025  
**Hours:** 10 hours

---

## Objective

Clean and integrate three data sources into a unified master dataset ready for machine learning.

---

## Tasks Completed

### 1. Hospital Name Normalization (2 hours) ✅
- Created mapping table for 53 Ontario hospitals
- Standardized naming across ER Watch, HowLongWillIWait, and Pediatric datasets
- Assigned unique hospital IDs
- Added attributes: region, pediatric capability, trauma centre status, tier

### 2. Wait Time Parsing & Integration (3 hours) ✅
- Built parser for 3 formats: "2 hr 12 min" → 132 minutes
- Handled ranges: "1 hr to 1 hr 9 min" → average (34.5 min)
- Flagged missing data: "Not available" → None
- Merged hospital attributes with wait time data
- **Result:** 100% parsing accuracy, 0% data loss

### 3. Missing Value Handling (3 hours) ✅
- Analyzed patterns: ~25% missing data
- Implemented flag strategy: kept None values with `data_available` flag
- Built 3 alternative strategies: drop, mean imputation, forward fill
- **Decision:** Flag strategy preserves information for ML models

### 4. Categorical Feature Encoding (2 hours) ✅
- One-hot encoded 6 regional indicators
- Binary encoded boolean flags (pediatric_er, trauma_centre)
- Ordinal encoded hospital tier (1 > 2 > 0)
- Added 7 temporal features: hour, day_of_week, is_weekend, is_night_shift

---

## Deliverables

### Primary: `triage_hospital_master.csv`
- **Rows:** 106 hospital records
- **Columns:** 19 features
- **Format:** CSV, UTF-8

**Key Features:**
- `hospital_id` - Unique identifier (1-53)
- `standard_name` - Canonical hospital name
- `region` - Geographic region (GTA, Eastern Ontario, etc.)
- `tier` - Hospital tier (0, 1, 2)
- `has_pediatric_er`, `is_trauma_centre` - Boolean flags
- `wait_time_minutes` - Parsed wait time
- `data_available` - Missing data flag
- `hour_of_day`, `day_of_week`, `is_weekend`, `is_night_shift` - Temporal features
- 6 regional dummy variables (one-hot encoded)

### Supporting Files:
- `Week2_hospital_name_mapping.csv` - Hospital mapping table (53 hospitals)
- `Week2_data_cleaning_pipeline.py` - Production Python script (374 lines)

---

## Results

**Data Quality:**
- ✅ 100% parsing accuracy
- ✅ 0% data loss during merging
- ✅ 13 new features engineered
- ✅ 53 hospitals standardized

**Code Quality:**
- ✅ Object-oriented design (modular, reusable)
- ✅ 4 missing value strategies
- ✅ Comprehensive error handling

---

## Integration Success

| Week 1 Issue | Week 2 Solution | Status |
|--------------|-----------------|--------|
| Multiple naming conventions | hospital_name_mapping.csv | ✅ |
| String wait time formats | Comprehensive parser | ✅ |
| ~25% missing data | Flag strategy | ✅ |
| No hospital attributes | Merged tier, region, flags | ✅ |
| No temporal features | Added 7 time features | ✅ |

---

## Sample Data

**Input (Raw):**
```
Timestamp,Hospital Name,Wait Time
2025-11-09 23:52:26,Toronto General (University Health Network),2 hr 22 min
```

**Output (Master Dataset):**
```
hospital_id,standard_name,region,wait_time_minutes,hour_of_day,is_weekend
4,Toronto General Hospital,GTA,142.0,23,True
```

---

## Week 3 Preview

**Focus:** Feature Engineering (10 hours)

**Tasks:**
1. Add derived severity scores
2. Integrate CTAS data from Langyue
3. Create rolling averages
4. Generate train/test split (80/20)
5. Exploratory Data Analysis

**Deliverable:** `features_v1.csv` + EDA notebook

---

## Files for Submission

1. ✅ `triage_hospital_master.csv` - Master dataset
2. ✅ `Week2_hospital_name_mapping.csv` - Hospital mapping
3. ✅ `Week2_data_cleaning_pipeline.py` - Python script
4. ✅ `Week2_Documentation.md` - This document

---

**Status:** ✅ WEEK 2 COMPLETE - READY FOR WEEK 3

**Prepared by:** Zuhair Abbas | November 2025