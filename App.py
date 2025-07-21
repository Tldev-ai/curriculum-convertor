from flask import Flask, render_template, request, jsonify
from src.components.dashboard import Dashboard
from src.components.curriculum_converter import CurriculumConverter
from src.components.curriculum_generator import CurriculumGenerator
import json
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Claude API Configuration
CLAUDE_API_KEY = ""
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

# Initialize components
dashboard = Dashboard()
converter = CurriculumConverter()
generator = CurriculumGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard_page():
    stats = dashboard.get_user_stats()
    recent_activity = dashboard.get_recent_activity()
    return render_template('dashboard.html', stats=stats, activity=recent_activity)

@app.route('/converter')
def converter_page():
    return render_template('converter.html')

@app.route('/generated')
def generated_page():
    files = generator.get_generated_files()
    return render_template('generated.html', files=files)

@app.route('/reviews')
def reviews_page():
    return render_template('reviews.html')

@app.route('/comparison-result')
def comparison_result():
    from_board = request.args.get('from', 'CBSE')
    to_board = request.args.get('to', 'IB')
    grade = request.args.get('grade', 'Grade 10')
    subject = request.args.get('subject', 'Mathematics')
    
    return render_template('comparison_result.html', 
                         from_board=from_board, 
                         to_board=to_board, 
                         grade=grade, 
                         subject=subject)

@app.route('/api/convert', methods=['POST'])
def convert_curriculum():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        result = converter.process_file(file)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard-stats')
def get_dashboard_stats():
    try:
        return jsonify(dashboard.get_stats())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-comprehensive-comparison', methods=['POST'])
def generate_comprehensive_comparison():
    try:
        data = request.get_json()
        from_board = data.get('fromBoard', 'CBSE')
        to_board = data.get('toBoard', 'IB')
        grade = data.get('grade', 'Grade 10')
        subject = data.get('subject', 'Mathematics')
        
        print(f"Generating comprehensive analysis for: {from_board} to {to_board}, {subject}, {grade}")
        
        comparison_result = generate_complete_curriculum_analysis(from_board, to_board, grade, subject)
        
        return jsonify({
            'success': True,
            'comparison': comparison_result
        })
        
    except Exception as e:
        print(f"Error in generate_comprehensive_comparison: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-specific-guidance', methods=['POST'])
def generate_specific_guidance():
    try:
        data = request.get_json()
        from_board = data.get('fromBoard', 'CBSE')
        to_board = data.get('toBoard', 'IB')
        grade = data.get('grade', 'Grade 10')
        subject = data.get('subject', 'Mathematics')
        audience = data.get('audience', 'parent')
        
        print(f"Generating {audience} guidance for: {from_board} to {to_board}, {subject}, {grade}")
        
        if audience == 'parent':
            guidance = generate_parent_guidance(from_board, to_board, grade, subject)
        else:
            guidance = generate_teacher_guidance(from_board, to_board, grade, subject)
        
        return jsonify({
            'success': True,
            'guidance': guidance
        })
        
    except Exception as e:
        print(f"Error in generate_specific_guidance: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def generate_complete_curriculum_analysis(from_board, to_board, grade, subject):
    comprehensive_prompt = f"""You are a world-renowned educational consultant with 20+ years of experience in international curriculum systems. A family is considering transitioning their child from {from_board} to {to_board} for {subject} in {grade}.

Provide an EXTREMELY COMPREHENSIVE, DETAILED analysis covering EVERY SINGLE IMPORTANT DIFFERENCE between these curricula. This is a critical decision that will impact the child's entire academic future. Leave NO STONE UNTURNED.

For EACH category below, provide:
- DETAILED explanations (minimum 3-4 sentences per point)
- SPECIFIC examples relevant to {subject} in {grade}
- PRACTICAL implications for students, parents, and teachers
- CONCRETE comparisons between {from_board} and {to_board}
- ACTIONABLE advice and recommendations

## 1. FUNDAMENTAL EDUCATIONAL PHILOSOPHY & APPROACH
Explain in detail how each curriculum views learning, knowledge acquisition, and student development. What are the core educational philosophies? How do they approach critical thinking vs. memorization? What is the balance between breadth vs. depth of knowledge?

## 2. CURRICULUM STRUCTURE & ORGANIZATION
Detail how subjects are organized, sequenced, and integrated. How many subjects? How are they divided? What is the academic year structure? How do prerequisites work? How flexible is subject selection?

## 3. NOMENCLATURE & TERMINOLOGY
Explain all the different terms, naming conventions, and educational vocabulary used in each system. How are courses named? What do different terms mean? How are levels and divisions described?

## 4. GRADING & ASSESSMENT SYSTEMS
Provide detailed comparison of how students are evaluated. What are the grading scales? How are marks calculated? What do different grades mean? How is academic progress measured and reported?

## 5. EXAMINATION PATTERNS & ASSESSMENT METHODS
Explain in detail how students are tested. What types of exams? When are they held? How long are they? What is the format? How much weightage to different assessment types?

## 6. INTERNAL ASSESSMENT & CONTINUOUS EVALUATION
Detail how ongoing assessment works. What percentage is internal vs. external? How are assignments graded? What about projects, presentations, and coursework?

## 7. TEACHING METHODOLOGIES & PEDAGOGICAL APPROACHES
Explain how teachers actually conduct classes. What teaching methods are emphasized? How student-centered vs. teacher-centered? What about hands-on learning, group work, individual study?

## 8. LEARNING OBJECTIVES & OUTCOMES
Detail what students are expected to achieve by the end of the course. What specific skills, knowledge, and competencies? How are learning outcomes defined and measured?

## 9. TEXTBOOKS, RESOURCES & MATERIALS
Explain what study materials are used. Are textbooks prescribed or recommended? What about digital resources? How much freedom do schools have in choosing materials?

## 10. HOMEWORK, ASSIGNMENTS & PROJECT REQUIREMENTS
Detail the workload and expectations outside of class. How much homework? What types of assignments? How are projects structured? What is the time commitment required?

## 11. PRACTICAL COMPONENTS & LABORATORY WORK
For {subject}, explain any hands-on requirements. Lab work, experiments, field trips, practical assessments? How much time? What equipment needed?

## 12. TECHNOLOGY INTEGRATION & DIGITAL LEARNING
Detail how technology is used in learning. What digital tools are required? Online platforms? Educational software? How much screen time?

## 13. LANGUAGE REQUIREMENTS & COMMUNICATION SKILLS
Explain language expectations. What is the medium of instruction? Are there additional language requirements? How are communication skills developed?

## 14. CULTURAL CONTEXT & GLOBAL PERSPECTIVE
Detail how each curriculum addresses cultural awareness and global citizenship. What is the international perspective? How are different cultures represented?

## 15. SCHOOL TYPES & INSTITUTIONAL REQUIREMENTS
Explain what types of schools offer each curriculum. Affiliation requirements? Teacher qualifications? Infrastructure needs? Accreditation processes?

## 16. TEACHER TRAINING & PROFESSIONAL DEVELOPMENT
Detail what qualifications teachers need. What training is required? Ongoing professional development? Certification processes?

## 17. CLASS SIZE & STUDENT-TEACHER RATIOS
Explain typical classroom environments. How many students per class? What is the student-teacher interaction like? How does this affect learning?

## 18. UNIVERSITY RECOGNITION & PATHWAYS
Detail how each curriculum prepares students for higher education. Which universities accept the credentials? Application processes? Grade conversion? International recognition?

## 19. CAREER PREPARATION & SKILL DEVELOPMENT
Explain how each system prepares students for future careers. What skills are emphasized? How is career guidance provided? Industry connections?

## 20. EXTRACURRICULAR INTEGRATION & HOLISTIC DEVELOPMENT
Detail how non-academic activities are incorporated. Sports, arts, clubs? How much time? How are they evaluated? Impact on overall development?

## 21. STUDENT SUPPORT SERVICES & GUIDANCE
Explain what support is available. Academic counseling? Career guidance? Special needs support? Mental health resources?

## 22. PARENT INVOLVEMENT & COMMUNICATION
Detail expectations for parent participation. How are parents kept informed? What involvement is expected? Communication channels and frequency?

## 23. COST IMPLICATIONS & FINANCIAL REQUIREMENTS
Explain the financial aspects. Tuition differences? Books and materials? Additional fees? Hidden costs? Financial aid availability?

## 24. TRANSITION CHALLENGES & ADAPTATION PERIOD
Detail specific difficulties students face when switching. Academic gaps? Social adjustment? Timeline for full adaptation? Support strategies?

## 25. SUPPLEMENTARY EDUCATION & ADDITIONAL SUPPORT
Explain what external support might be needed. Tutoring requirements? Coaching classes? Additional resources? Preparation programs?

## 26. QUALITY ASSURANCE & STANDARDS MONITORING
Detail how quality is maintained. Inspection processes? Standardization measures? Performance monitoring? Accountability systems?

## 27. INTERNATIONAL MOBILITY & TRANSFERABILITY
Explain how easy it is to transfer between schools and countries. Credit transfer? Grade recognition? Documentation requirements?

## 28. TIMELINE & IMPLEMENTATION STRATEGY
Provide a detailed roadmap for the transition. What steps to take when? How long for full transition? Critical milestones and checkpoints?

For the transition from {from_board} to {to_board} in {subject} for {grade}, provide SPECIFIC, ACTIONABLE recommendations that address the unique challenges and opportunities of this exact combination.

Make this analysis so comprehensive and detailed that parents and teachers have every piece of information they need to make an informed decision and successfully manage the transition."""

    try:
        analysis = call_claude_api(comprehensive_prompt)
        return {
            'fromBoard': from_board,
            'toBoard': to_board,
            'grade': grade,
            'subject': subject,
            'analysis': analysis
        }
    except Exception as e:
        return {
            'fromBoard': from_board,
            'toBoard': to_board,
            'grade': grade,
            'subject': subject,
            'analysis': f'Error generating comprehensive analysis: {str(e)}'
        }

def generate_parent_guidance(from_board, to_board, grade, subject):
    detailed_parent_prompt = f"""You are an educational counselor specializing in curriculum transitions. A parent is seeking detailed guidance for their child's transition from {from_board} to {to_board} for {subject} in {grade}.

Provide COMPREHENSIVE, DETAILED guidance covering every aspect parents need to know:

## IMMEDIATE PREPARATION (What to do RIGHT NOW)
- Detailed steps to prepare their child academically and mentally
- Documents and paperwork required (be specific)
- Timeline for application and enrollment processes
- How to research and select the right school
- Financial planning and budgeting considerations

## ACADEMIC PREPARATION STRATEGY
- Specific knowledge gaps that need to be addressed
- Skills their child needs to develop before transition
- Study habits and learning strategies to establish
- How to bridge curriculum differences in {subject}
- Recommended preparatory materials and resources

## UNDERSTANDING THE NEW LEARNING ENVIRONMENT
- How daily school life will change for their child
- New expectations for homework and study time
- Different assessment methods their child will face
- Changes in teacher-student interaction styles
- Peer interaction and social dynamics

## SUPPORTING YOUR CHILD THROUGH THE TRANSITION
- How to identify and address adjustment difficulties
- Warning signs of academic or social struggles
- Communication strategies with teachers and school
- How to maintain motivation during challenging periods
- Building confidence in the new system

## PRACTICAL CHANGES TO EXPECT
- Daily routine modifications needed
- Technology requirements and digital platforms
- Study space setup and learning environment at home
- Transportation and logistics considerations
- Extracurricular activity changes

## LONG-TERM IMPLICATIONS & PLANNING
- University admission pathway changes
- Career preparation differences
- International opportunities and recognition
- Skills development trajectory
- Global competency building

## FINANCIAL PLANNING & RESOURCE MANAGEMENT
- Detailed cost breakdown (tuition, books, materials, extras)
- Hidden expenses to budget for
- Financial aid and scholarship opportunities
- Long-term educational investment planning
- Cost comparison strategies

## COMMUNICATION & RELATIONSHIP BUILDING
- How to establish positive relationships with new teachers
- Parent-teacher conference expectations and preparation
- School community involvement opportunities
- Building support networks with other parents
- Advocating effectively for your child's needs

## MONITORING PROGRESS & SUCCESS METRICS
- How to track your child's adaptation and progress
- Key milestones to watch for in the first year
- When to seek additional support or intervention
- Success indicators vs. warning signs
- Adjustment timeline expectations

## ADDRESSING COMMON CHALLENGES
Specific solutions for typical difficulties in transitioning from {from_board} to {to_board} in {subject} for {grade}:
- Academic content gaps and how to fill them
- Learning style adjustments
- Social integration challenges
- Performance anxiety and confidence issues
- Time management and organizational skills

Provide specific, actionable advice that empowers parents to confidently support their child through this important transition."""

    try:
        return call_claude_api(detailed_parent_prompt)
    except Exception as e:
        return f"Error generating detailed parent guidance: {str(e)}"

def generate_teacher_guidance(from_board, to_board, grade, subject):
    detailed_teacher_prompt = f"""You are providing comprehensive professional development guidance to teachers transitioning from teaching {from_board} curriculum to {to_board} curriculum for {subject} in {grade}.

Provide DETAILED, PRACTICAL guidance covering every aspect teachers need to master:

## PEDAGOGICAL TRANSFORMATION
- Detailed comparison of teaching philosophies between {from_board} and {to_board}
- Specific methodology changes required for {subject} in {grade}
- Student engagement strategies unique to {to_board} approach
- Classroom management adaptations needed
- How to shift from teacher-centered to student-centered approaches (or vice versa)

## CURRICULUM CONTENT MASTERY
- Detailed content differences in {subject} for {grade}
- New topics to master and teach
- Depth vs. breadth adjustments in content coverage
- Integration strategies with other subjects
- Scope and sequence modifications

## ASSESSMENT & EVALUATION TRANSFORMATION
- Complete overhaul of assessment strategies
- New rubrics and grading criteria to implement
- Formative vs. summative assessment balance
- Portfolio and project-based assessment techniques
- Student self-assessment and peer evaluation methods

## LESSON PLANNING & CURRICULUM DELIVERY
- Step-by-step lesson plan restructuring
- Pacing guide modifications for {to_board} system
- Resource allocation and material selection
- Technology integration requirements
- Differentiation strategies for diverse learners

## PROFESSIONAL DEVELOPMENT PATHWAY
- Specific certifications and qualifications needed for {to_board}
- Training programs and workshops to attend
- Mentorship and coaching opportunities
- Professional learning community engagement
- Ongoing skill development requirements

## STUDENT SUPPORT STRATEGIES
- How to identify students struggling with transition
- Individualized support plan development
- Learning gap assessment and remediation
- Building student confidence in new system
- Fostering growth mindset and resilience

## CLASSROOM ENVIRONMENT & CULTURE
- Physical classroom setup modifications
- Creating inclusive and collaborative learning spaces
- Establishing new routines and procedures
- Building positive teacher-student relationships
- Encouraging student voice and choice

## PARENT & COMMUNITY ENGAGEMENT
- Communication strategies with parents unfamiliar with {to_board}
- Parent education and involvement techniques
- Community partnership building
- Cultural sensitivity and awareness
- Managing parent expectations and concerns

## RESOURCE DEVELOPMENT & MANAGEMENT
- Creating and adapting teaching materials for {to_board}
- Digital tool integration and platform management
- Budget planning for new resources
- Collaborative resource sharing with colleagues
- Continuous material improvement and updates

## QUALITY ASSURANCE & REFLECTION
- Self-evaluation and improvement strategies
- Peer observation and feedback systems
- Student feedback collection and analysis
- Data-driven instruction implementation
- Continuous professional growth planning

## SPECIFIC CHALLENGES FOR {subject} IN {grade}
Detailed solutions for common difficulties teachers face when transitioning {subject} curriculum from {from_board} to {to_board} for {grade}:
- Content knowledge gaps and professional learning needs
- Assessment method adaptations
- Student engagement strategy modifications
- Technology integration requirements
- Collaboration and interdisciplinary connections

## IMPLEMENTATION TIMELINE & MILESTONES
- Year-by-year professional development plan
- Quarter-by-quarter implementation goals
- Monthly reflection and adjustment periods
- Weekly planning and preparation strategies
- Daily practice modifications and improvements

Provide specific, actionable professional guidance that enables teachers to excel in delivering {to_board} curriculum for {subject} in {grade}."""

    try:
        return call_claude_api(detailed_teacher_prompt)
    except Exception as e:
        return f"Error generating detailed teacher guidance: {str(e)}"

def call_claude_api(prompt):
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
    }
    
    payload = {
        'model': 'claude-3-5-sonnet-20241022',
        'max_tokens': 8000,  # Increased for comprehensive responses
        'messages': [
            {
                'role': 'user',
                'content': prompt
            }
        ]
    }
    
    try:
        print(f"Making comprehensive API call to Claude...")
        response = requests.post(CLAUDE_API_URL, headers=headers, json=payload, timeout=120)  # Increased timeout
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            return result['content'][0]['text']
        else:
            error_text = response.text
            print(f"API Error: {error_text}")
            return f"API request failed with status {response.status_code}: {error_text}"
            
    except Exception as e:
        print(f"API call error: {str(e)}")
        return f"API call failed: {str(e)}"

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001
    )
