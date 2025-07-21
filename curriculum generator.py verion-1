import json
from datetime import datetime

class CurriculumGenerator:
    def __init__(self):
        self.files_data = 'static/data/generated_files.json'
    
    def get_generated_files(self):
        """Get list of generated curriculum files"""
        return [
            {
                'id': 'file_001',
                'name': 'Math_Grade_10_Algebra.pdf',
                'subject': 'Mathematics',
                'grade': 'Grade 10',
                'created_date': '2024-01-15',
                'file_size': '2.4 MB',
                'downloads': 15,
                'status': 'Ready'
            },
            {
                'id': 'file_002',
                'name': 'Science_Chemistry_Tests.docx',
                'subject': 'Science',
                'grade': 'Grade 11',
                'created_date': '2024-01-14',
                'file_size': '1.8 MB',
                'downloads': 8,
                'status': 'Ready'
            },
            {
                'id': 'file_003',
                'name': 'English_Literature_Analysis.pdf',
                'subject': 'English',
                'grade': 'Grade 12',
                'created_date': '2024-01-13',
                'file_size': '3.2 MB',
                'downloads': 22,
                'status': 'Processing'
            }
        ]
    
    def download_file(self, file_id):
        """Handle file download"""
        # Mock download logic
        return {
            'success': True,
            'download_url': f'/downloads/{file_id}',
            'expires_at': datetime.now().isoformat()
        }
    
    def delete_file(self, file_id):
        """Delete generated file"""
        return {'success': True, 'message': 'File deleted successfully'}
