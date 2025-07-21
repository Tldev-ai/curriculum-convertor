import json
from datetime import datetime, timedelta

class Dashboard:
    def __init__(self):
        self.data_file = 'static/data/dashboard_data.json'
    
    def get_stats(self):
        """Get overall platform statistics"""
        return {
            'total_conversions': 3678,
            'total_users': 1250,
            'success_rate': 98.5,
            'avg_conversion_time': '2.3 minutes'
        }
    
    def get_user_stats(self):
        """Get current user's statistics"""
        return {
            'user_conversions': 45,
            'files_generated': 67,
            'last_login': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'account_type': 'Premium',
            'storage_used': '2.3 GB',
            'storage_limit': '10 GB'
        }
    
    def get_recent_activity(self):
        """Get user's recent activity"""
        return [
            {
                'action': 'Converted Math Curriculum',
                'timestamp': '2 hours ago',
                'status': 'completed',
                'file_name': 'algebra_grade_10.pdf'
            },
            {
                'action': 'Generated Science Tests',
                'timestamp': '1 day ago',
                'status': 'completed',
                'file_name': 'chemistry_chapter_5.docx'
            },
            {
                'action': 'Uploaded English Content',
                'timestamp': '2 days ago',
                'status': 'processing',
                'file_name': 'literature_analysis.pdf'
            }
        ]
    
    def get_conversion_trends(self):
        """Get conversion trends for charts"""
        return {
            'daily_conversions': [12, 15, 8, 22, 18, 25, 20],
            'subjects': {
                'Math': 35,
                'Science': 28,
                'English': 22,
                'History': 15
            }
        }
