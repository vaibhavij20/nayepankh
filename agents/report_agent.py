"""
Report agent module for NayePankh AI Assistant.
Generates reports with proper error handling and formatting.
"""

from typing import Optional
from datetime import datetime, timedelta
from database.db import get_all_volunteers, get_volunteer_count
from logger import get_logger

logger = get_logger(__name__)


class ReportAgent:
    """Generates various reports for the NayePankh system."""
    
    def generate_weekly_report(self) -> str:
        """
        Generate a weekly volunteer report.
        
        Returns:
            Formatted weekly report string
        """
        try:
            volunteers = get_all_volunteers()
            total_count = get_volunteer_count()
            
            # Calculate week range
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            
            # Get new volunteers this week
            new_volunteers = [
                v for v in volunteers 
                if v.get('created_at') and week_start <= datetime.fromisoformat(v['created_at']) <= week_end
            ]
            
            # Extract skills
            all_skills = []
            for volunteer in volunteers:
                skills = volunteer.get('skills', '').split(',')
                all_skills.extend([s.strip() for s in skills if s.strip()])
            
            # Count skills
            from collections import Counter
            skill_counts = Counter(all_skills)
            top_skills = skill_counts.most_common(10)
            
            # Build report
            report = f"""
{'='*60}
NAYEPANKH FOUNDATION - WEEKLY REPORT
{'='*60}

Report Period: {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}
Generated: {today.strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
SUMMARY
{'='*60}

Total Volunteers: {total_count}
New Volunteers This Week: {len(new_volunteers)}
Active Skills: {len(skill_counts)}

{'='*60}
NEW VOLUNTEERS THIS WEEK
{'='*60}
"""
            
            if new_volunteers:
                for volunteer in new_volunteers[:10]:  # Show max 10
                    report += f"\n- {volunteer.get('name', 'N/A')} ({volunteer.get('email', 'N/A')})"
                    report += f"\n  Skills: {volunteer.get('skills', 'N/A')}"
                if len(new_volunteers) > 10:
                    report += f"\n... and {len(new_volunteers) - 10} more"
            else:
                report += "\nNo new volunteers this week."
            
            report += f"""

{'='*60}
TOP SKILLS
{'='*60}
"""
            
            if top_skills:
                for skill, count in top_skills:
                    report += f"\n{skill}: {count} volunteer(s)"
            else:
                report += "\nNo skills data available."
            
            report += f"""

{'='*60}
RECOMMENDATIONS
{'='*60}

1. Focus recruitment efforts on high-demand skill areas
2. Organize skill-specific workshops for volunteers
3. Follow up with new volunteers for onboarding
4. Update mentor matching based on skill distribution

{'='*60}
END OF REPORT
{'='*60}
"""
            
            logger.info("Weekly report generated successfully")
            return report
            
        except Exception as e:
            logger.error(f"Error generating weekly report: {e}")
            return f"Error generating report: {str(e)}"
    
    def generate_summary_report(self) -> str:
        """
        Generate a summary report of the system.
        
        Returns:
            Formatted summary report string
        """
        try:
            total_volunteers = get_volunteer_count()
            volunteers = get_all_volunteers()
            
            # Get memory count
            from memory_manager import memory_manager
            memory_count = memory_manager.get_memory_count()
            
            report = f"""
{'='*60}
NAYEPANKH FOUNDATION - SYSTEM SUMMARY
{'='*60}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
SYSTEM METRICS
{'='*60}

Total Volunteers: {total_volunteers}
Memory Entries: {memory_count}

{'='*60}
VOLUNTEER DISTRIBUTION
{'='*60}
"""
            
            if volunteers:
                # Skills distribution
                from collections import Counter
                all_skills = []
                for volunteer in volunteers:
                    skills = volunteer.get('skills', '').split(',')
                    all_skills.extend([s.strip() for s in skills if s.strip()])
                
                skill_counts = Counter(all_skills)
                
                for skill, count in skill_counts.most_common(5):
                    percentage = (count / total_volunteers) * 100 if total_volunteers > 0 else 0
                    report += f"\n{skill}: {count} ({percentage:.1f}%)"
            else:
                report += "\nNo volunteer data available."
            
            report += f"""

{'='*60}
END OF SUMMARY
{'='*60}
"""
            
            logger.info("Summary report generated successfully")
            return report
            
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
            return f"Error generating summary: {str(e)}"


# Global report agent instance
report_agent = ReportAgent()

# Backward compatibility function
def generate_report() -> str:
    """
    Generate a weekly report.
    
    Returns:
        Formatted weekly report string
    """
    return report_agent.generate_weekly_report()