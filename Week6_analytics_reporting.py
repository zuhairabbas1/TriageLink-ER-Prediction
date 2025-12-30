"""
RightER Internal Dashboard - Week 6: Analytics + Reporting + Rehearsal Prep
Author: Zuhair Abbas
Purpose: Build analytics scripts, generate summary stats, create QA report templates
Role: Analytics + Reporting + Rehearsal Prep Lead
Deliverable: analytics_dashboard.py + qa_report_template.py + demo_materials/
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple

class RightERAnalytics:
    """
    Analytics system for RightER internal QA dashboard.
    NOT clinical advice, NOT triage, NOT diagnosis - QA tool only.
    """
    
    def __init__(self):
        print("=" * 80)
        print("RIGHTER INTERNAL DASHBOARD - WEEK 6: ANALYTICS + REPORTING")
        print("=" * 80)
        print("\n⚠️  CRITICAL: This is an internal QA tool")
        print("   ❌ NOT clinical advice")
        print("   ❌ NOT triage or diagnosis")
        print("   ❌ NOT public-facing")
        print("   ❌ NOT dependent on PHI")
        print("   ✅ Decision-support & QA tool for clinicians")
        print("\n" + "-" * 80)
        
        self.data = None
        self.metrics = {}
        
    def generate_fake_dataset(self, num_records=200):
        """
        Generate realistic fake/de-identified dataset for demo.
        NO PHI - all data is synthetic.
        """
        print(f"\n📊 GENERATING FAKE DATASET ({num_records} records)")
        print("-" * 80)
        
        np.random.seed(42)  # Reproducible fake data
        
        # CTAS distribution (realistic ER mix)
        ctas_distribution = [0.02, 0.15, 0.40, 0.35, 0.08]  # CTAS 1-5
        ctas_levels = np.random.choice([1, 2, 3, 4, 5], size=num_records, p=ctas_distribution)
        
        # Age bands
        age_bands = np.random.choice(
            ['0-17', '18-40', '41-65', '66-80', '80+'],
            size=num_records,
            p=[0.15, 0.30, 0.35, 0.15, 0.05]
        )
        
        # Chief complaints (de-identified, general categories)
        complaints = np.random.choice([
            'Chest pain', 'Abdominal pain', 'Shortness of breath', 'Injury - fall',
            'Headache', 'Fever', 'Nausea/vomiting', 'Back pain',
            'Laceration', 'Psychiatric', 'Allergic reaction', 'Minor trauma'
        ], size=num_records)
        
        # Abnormal vitals (Y/N)
        abnormal_vitals = np.random.choice(['Y', 'N'], size=num_records, p=[0.35, 0.65])
        
        # Timestamps (last 24 hours)
        base_time = datetime.now() - timedelta(hours=24)
        triage_times = [base_time + timedelta(minutes=np.random.randint(0, 1440)) 
                       for _ in range(num_records)]
        
        # Reassessment times (some patients reassessed, some not yet)
        reassess_times = []
        for i in range(num_records):
            if np.random.random() < 0.70:  # 70% have been reassessed
                reassess_delay = np.random.randint(15, 180)  # 15 min to 3 hours
                reassess_times.append(triage_times[i] + timedelta(minutes=reassess_delay))
            else:
                reassess_times.append(None)  # Not yet reassessed
        
        # Seen by MD (some yes, some waiting)
        seen_by_md = np.random.choice(['Y', 'N'], size=num_records, p=[0.60, 0.40])
        
        # Create DataFrame
        data = pd.DataFrame({
            'patient_id': [f'PT-{i+1:04d}' for i in range(num_records)],
            'ctas_level': ctas_levels,
            'chief_complaint': complaints,
            'age_band': age_bands,
            'abnormal_vitals': abnormal_vitals,
            'triage_timestamp': triage_times,
            'reassess_timestamp': reassess_times,
            'seen_by_md': seen_by_md
        })
        
        # Compute derived fields
        data = self._compute_derived_fields(data)
        
        self.data = data
        
        print(f"✅ Generated {len(data)} fake patient records")
        print(f"\n📋 Dataset Schema:")
        print(f"   - patient_id: De-identified ID")
        print(f"   - ctas_level: 1-5 (1=Resuscitation, 5=Non-urgent)")
        print(f"   - chief_complaint: General category")
        print(f"   - age_band: Age range (de-identified)")
        print(f"   - abnormal_vitals: Y/N")
        print(f"   - triage_timestamp: When triaged")
        print(f"   - reassess_timestamp: When reassessed (if applicable)")
        print(f"   - seen_by_md: Y/N")
        print(f"   - elapsed_wait_minutes: Time since triage")
        print(f"   - overdue_flag: Y/N (exceeds CTAS target)")
        print(f"   - risk_level: Low/Medium/High/Critical")
        
        return data
    
    def _compute_derived_fields(self, data):
        """
        Compute analytics fields: elapsed wait, overdue flag, risk level.
        """
        # CTAS target times (in minutes)
        ctas_targets = {1: 0, 2: 15, 3: 30, 4: 60, 5: 120}
        
        # Elapsed wait time (minutes since triage)
        current_time = datetime.now()
        data['elapsed_wait_minutes'] = data['triage_timestamp'].apply(
            lambda x: int((current_time - x).total_seconds() / 60)
        )
        
        # Target time for CTAS level
        data['target_time_minutes'] = data['ctas_level'].map(ctas_targets)
        
        # Overdue flag (Y/N)
        data['overdue_flag'] = data.apply(
            lambda row: 'Y' if row['elapsed_wait_minutes'] > row['target_time_minutes'] else 'N',
            axis=1
        )
        
        # Reassessment compliance (if not seen by MD, should be reassessed)
        data['reassess_compliance'] = data.apply(
            lambda row: 'N/A' if row['seen_by_md'] == 'Y' 
            else ('Y' if row['reassess_timestamp'] is not None else 'N'),
            axis=1
        )
        
        # Risk level (for QA dashboard visualization)
        def calculate_risk_level(row):
            if row['ctas_level'] == 1:
                return 'Critical'
            elif row['ctas_level'] == 2 and row['overdue_flag'] == 'Y':
                return 'High'
            elif row['overdue_flag'] == 'Y' and row['abnormal_vitals'] == 'Y':
                return 'High'
            elif row['overdue_flag'] == 'Y':
                return 'Medium'
            else:
                return 'Low'
        
        data['risk_level'] = data.apply(calculate_risk_level, axis=1)
        
        return data
    
    def compute_summary_statistics(self):
        """
        Compute summary statistics for dashboard tiles.
        """
        print(f"\n📊 COMPUTING SUMMARY STATISTICS")
        print("-" * 80)
        
        if self.data is None:
            print("❌ No data loaded. Generate dataset first.")
            return None
        
        stats = {
            'total_patients': len(self.data),
            'currently_waiting': len(self.data[self.data['seen_by_md'] == 'N']),
            'overdue_count': len(self.data[self.data['overdue_flag'] == 'Y']),
            'overdue_percentage': (len(self.data[self.data['overdue_flag'] == 'Y']) / len(self.data)) * 100,
            'high_risk_count': len(self.data[self.data['risk_level'] == 'High']),
            'critical_risk_count': len(self.data[self.data['risk_level'] == 'Critical']),
            'average_wait_time': self.data['elapsed_wait_minutes'].mean(),
            'median_wait_time': self.data['elapsed_wait_minutes'].median(),
            'max_wait_time': self.data['elapsed_wait_minutes'].max()
        }
        
        # CTAS distribution
        ctas_dist = self.data['ctas_level'].value_counts().sort_index()
        stats['ctas_distribution'] = {
            f'CTAS {level}': int(count) 
            for level, count in ctas_dist.items()
        }
        
        # Reassessment compliance
        reassess_compliance = self.data[self.data['reassess_compliance'] != 'N/A']['reassess_compliance'].value_counts()
        if len(reassess_compliance) > 0:
            stats['reassessment_compliance_rate'] = (reassess_compliance.get('Y', 0) / reassess_compliance.sum()) * 100
        else:
            stats['reassessment_compliance_rate'] = 0
        
        # Overdue by CTAS level
        stats['overdue_by_ctas'] = {}
        for ctas in [1, 2, 3, 4, 5]:
            ctas_data = self.data[self.data['ctas_level'] == ctas]
            if len(ctas_data) > 0:
                overdue_count = len(ctas_data[ctas_data['overdue_flag'] == 'Y'])
                stats['overdue_by_ctas'][f'CTAS {ctas}'] = {
                    'total': len(ctas_data),
                    'overdue': overdue_count,
                    'percentage': (overdue_count / len(ctas_data)) * 100
                }
        
        self.metrics = stats
        
        print(f"✅ Summary Statistics Computed:")
        print(f"\n🏥 Overall Metrics:")
        print(f"   Total patients (24h): {stats['total_patients']}")
        print(f"   Currently waiting: {stats['currently_waiting']}")
        print(f"   Overdue patients: {stats['overdue_count']} ({stats['overdue_percentage']:.1f}%)")
        print(f"   High risk: {stats['high_risk_count']}")
        print(f"   Critical risk: {stats['critical_risk_count']}")
        print(f"\n⏱️  Wait Time Metrics:")
        print(f"   Average wait: {stats['average_wait_time']:.1f} minutes")
        print(f"   Median wait: {stats['median_wait_time']:.1f} minutes")
        print(f"   Max wait: {stats['max_wait_time']:.0f} minutes")
        print(f"\n🔄 Reassessment Compliance: {stats['reassessment_compliance_rate']:.1f}%")
        
        return stats
    
    def generate_risk_radar_table(self, output_file='risk_radar_table.csv'):
        """
        Generate Risk Radar Table for dashboard display.
        Sorted by risk level + wait time.
        """
        print(f"\n⚠️  GENERATING RISK RADAR TABLE")
        print("-" * 80)
        
        # Filter to waiting patients only
        waiting = self.data[self.data['seen_by_md'] == 'N'].copy()
        
        # Sort by risk level (Critical > High > Medium > Low) then wait time
        risk_order = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4}
        waiting['risk_sort'] = waiting['risk_level'].map(risk_order)
        waiting = waiting.sort_values(['risk_sort', 'elapsed_wait_minutes'], ascending=[True, False])
        
        # Select columns for display
        radar_table = waiting[[
            'patient_id', 'ctas_level', 'chief_complaint', 'age_band',
            'abnormal_vitals', 'elapsed_wait_minutes', 'overdue_flag', 'risk_level'
        ]].copy()
        
        # Save to CSV
        radar_table.to_csv(output_file, index=False)
        
        print(f"✅ Saved: {output_file}")
        print(f"   Rows: {len(radar_table)}")
        print(f"   Sorted by: Risk Level (desc) → Wait Time (desc)")
        print(f"\n🔴 Top 5 Highest Risk Patients:")
        print(radar_table.head(5).to_string(index=False))
        
        return radar_table
    
    def generate_qa_summary_report(self, output_file='qa_summary_report.txt'):
        """
        Generate QA Summary Report for hospital presentation.
        """
        print(f"\n📄 GENERATING QA SUMMARY REPORT")
        print("-" * 80)
        
        if self.metrics is None:
            self.compute_summary_statistics()
        
        report = f"""
================================================================================
RIGHTER INTERNAL QA DASHBOARD - SUMMARY REPORT
================================================================================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Time Period: Last 24 hours
Hospital: Demo Hospital (Fake Data)

⚠️  IMPORTANT: This is an internal QA tool for clinicians
   - NOT clinical advice, NOT triage, NOT diagnosis
   - Uses de-identified/fake data for demonstration
   - For retrospective QA and risk awareness only

================================================================================
EXECUTIVE SUMMARY
================================================================================

Total Patients Triaged (24h):     {self.metrics['total_patients']}
Currently Waiting:                 {self.metrics['currently_waiting']}
Patients Over Target Time:         {self.metrics['overdue_count']} ({self.metrics['overdue_percentage']:.1f}%)
High Risk Patients:                {self.metrics['high_risk_count']}
Critical Risk Patients:            {self.metrics['critical_risk_count']}

Average Wait Time:                 {self.metrics['average_wait_time']:.1f} minutes
Median Wait Time:                  {self.metrics['median_wait_time']:.1f} minutes
Maximum Wait Time:                 {self.metrics['max_wait_time']:.0f} minutes

Reassessment Compliance Rate:     {self.metrics['reassessment_compliance_rate']:.1f}%

================================================================================
CTAS DISTRIBUTION
================================================================================

"""
        
        for ctas, count in self.metrics['ctas_distribution'].items():
            percentage = (count / self.metrics['total_patients']) * 100
            report += f"{ctas}: {count:3d} patients ({percentage:5.1f}%)\n"
        
        report += f"""
================================================================================
OVERDUE ANALYSIS BY CTAS LEVEL
================================================================================

"""
        
        for ctas, data in self.metrics['overdue_by_ctas'].items():
            report += f"{ctas}:\n"
            report += f"  Total: {data['total']} | Overdue: {data['overdue']} ({data['percentage']:.1f}%)\n"
        
        report += f"""
================================================================================
RISK FLAGS EXPLANATION
================================================================================

CRITICAL: CTAS 1 patients (immediate life-threatening)
HIGH:     CTAS 2 overdue OR overdue + abnormal vitals
MEDIUM:   Any overdue patient
LOW:      Within target time

"Overdue" means: Elapsed wait time > CTAS target time
  - CTAS 1: 0 min (immediate)
  - CTAS 2: 15 min
  - CTAS 3: 30 min
  - CTAS 4: 60 min
  - CTAS 5: 120 min

================================================================================
KEY INSIGHTS
================================================================================

1. Overdue Rate: {self.metrics['overdue_percentage']:.1f}% of patients are over target time
   → This is a QA metric, not a clinical severity indicator
   
2. High Priority Focus: {self.metrics['high_risk_count']} patients flagged as high risk
   → Includes CTAS 2 overdue + patients with abnormal vitals
   
3. Reassessment Compliance: {self.metrics['reassessment_compliance_rate']:.1f}%
   → Percentage of waiting patients who have been reassessed
   
4. Wait Time Variability: Max wait is {self.metrics['max_wait_time']:.0f} minutes
   → Large variation suggests capacity/flow challenges

================================================================================
DISCLAIMER
================================================================================

This report is for internal quality assurance purposes only. It does not:
  - Provide clinical advice or medical recommendations
  - Replace clinical judgment or triage decisions
  - Diagnose or assess individual patient conditions
  - Serve as a patient-facing tool

RightER is a retrospective QA tool to help hospital teams identify:
  - Wait time patterns
  - Reassessment compliance gaps
  - Potential risk indicators for review

All data in this demo is FAKE and de-identified for demonstration purposes.
No real patient information (PHI) is used or required.

================================================================================
END OF REPORT
================================================================================
"""
        
        # Save report
        with open(output_file, 'w') as f:
            f.write(report)
        
        print(f"✅ Saved: {output_file}")
        
        return report
    
    def save_analytics_json(self, output_file='analytics_summary.json'):
        """
        Save analytics in JSON format for dashboard API consumption.
        """
        print(f"\n💾 SAVING ANALYTICS JSON")
        print("-" * 80)
        
        if self.metrics is None:
            self.compute_summary_statistics()
        
        # Convert numpy types to native Python types for JSON serialization
        json_metrics = {
            'timestamp': datetime.now().isoformat(),
            'time_period': 'Last 24 hours',
            'disclaimer': 'Internal QA tool only - NOT clinical advice',
            'summary': {
                'total_patients': int(self.metrics['total_patients']),
                'currently_waiting': int(self.metrics['currently_waiting']),
                'overdue_count': int(self.metrics['overdue_count']),
                'overdue_percentage': float(self.metrics['overdue_percentage']),
                'high_risk_count': int(self.metrics['high_risk_count']),
                'critical_risk_count': int(self.metrics['critical_risk_count']),
                'average_wait_time': float(self.metrics['average_wait_time']),
                'median_wait_time': float(self.metrics['median_wait_time']),
                'max_wait_time': float(self.metrics['max_wait_time']),
                'reassessment_compliance_rate': float(self.metrics['reassessment_compliance_rate'])
            },
            'ctas_distribution': self.metrics['ctas_distribution'],
            'overdue_by_ctas': self.metrics['overdue_by_ctas']
        }
        
        with open(output_file, 'w') as f:
            json.dump(json_metrics, f, indent=2)
        
        print(f"✅ Saved: {output_file}")
        
        return json_metrics
    
    def save_dataset_csv(self, output_file='fake_er_data.csv'):
        """
        Save fake dataset to CSV for backend/frontend loading.
        """
        print(f"\n💾 SAVING DATASET CSV")
        print("-" * 80)
        
        if self.data is None:
            print("❌ No data to save. Generate dataset first.")
            return
        
        self.data.to_csv(output_file, index=False)
        
        print(f"✅ Saved: {output_file}")
        print(f"   Rows: {len(self.data)}")
        print(f"   Columns: {len(self.data.columns)}")
        
    def run_full_analytics_pipeline(self):
        """
        Run complete analytics pipeline.
        """
        # Step 1: Generate fake dataset
        self.generate_fake_dataset(num_records=200)
        
        # Step 2: Compute summary statistics
        self.compute_summary_statistics()
        
        # Step 3: Generate risk radar table
        self.generate_risk_radar_table('risk_radar_table.csv')
        
        # Step 4: Generate QA summary report
        self.generate_qa_summary_report('qa_summary_report.txt')
        
        # Step 5: Save analytics JSON
        self.save_analytics_json('analytics_summary.json')
        
        # Step 6: Save dataset CSV
        self.save_dataset_csv('fake_er_data.csv')
        
        print("\n" + "=" * 80)
        print("✅ WEEK 6 ANALYTICS PIPELINE COMPLETE!")
        print("=" * 80)
        print(f"\n📁 Deliverables:")
        print(f"   - fake_er_data.csv (200 patient records)")
        print(f"   - risk_radar_table.csv (waiting patients, sorted by risk)")
        print(f"   - analytics_summary.json (metrics for dashboard API)")
        print(f"   - qa_summary_report.txt (hospital presentation report)")
        print(f"\n📊 Ready for:")
        print(f"   - Catherine: Dashboard UI integration")
        print(f"   - Vishaal: Backend data loading")
        print(f"   - Demo rehearsal with Tony")
        
        return {
            'data': self.data,
            'metrics': self.metrics
        }


# Example usage
if __name__ == "__main__":
    analytics = RightERAnalytics()
    results = analytics.run_full_analytics_pipeline()
    
    print("\n✅ Analytics + Reporting complete!")
    print(f"   Total patients: {len(results['data'])}")
    print(f"   Overdue: {results['metrics']['overdue_count']}")
    print(f"   High risk: {results['metrics']['high_risk_count']}")