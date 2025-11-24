
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from datetime import datetime
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from models import SystemState, Team, Faculty, Project, Interface
from analytics import FramesAnalytics
from flask import make_response
import traceback
from backend.database import db

app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
CORS(app)  # Enable CORS for frontend-backend communication

# Configure SQLAlchemy (simple SQLite for dev; switch URI via env for Postgres later)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise RuntimeError("DATABASE_URL is required. Please set it in your .env (Neon connection string).")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Global system state (in production, use database)
system_state = SystemState()

# Program Health Dashboard
@app.route('/dashboard')
def program_health_dashboard():
    """Serve the Program Health dashboard (3D molecular visualization)"""
    university = request.args.get('university')
    return render_template('dashboard.html', university=university)


@app.route('/api/network-data')
def get_network_data():
    """
    Get network data for 3D molecular visualization.
    Returns preset sample data for demo purposes.
    """
    # Preset sample data - no database required
    sample_data = {
        'projects': [
            {'id': 'proves', 'name': 'PROVES', 'type': 'collaborative', 'is_nucleus': True, 'team_size': 6},
            {'id': 'contract', 'name': 'Funded Contract Project', 'type': 'contract', 'is_nucleus': False, 'team_size': 15},
            {'id': 'proposal', 'name': 'Contract Proposal Project', 'type': 'proposal', 'is_nucleus': False, 'team_size': 60}
        ],
        'teams': [
            # PROVES teams (6 members total)
            {'id': 'proves_team1', 'name': 'PROVES Core Team', 'project_id': 'proves', 'discipline': 'Multidisciplinary', 'size': 6},
            # Contract project teams (15 members total)
            {'id': 'contract_team1', 'name': 'Contract Engineering Team', 'project_id': 'contract', 'discipline': 'Engineering', 'size': 8},
            {'id': 'contract_team2', 'name': 'Contract Research Team', 'project_id': 'contract', 'discipline': 'Research', 'size': 7},
            # Proposal project teams (60 members total)
            {'id': 'proposal_team1', 'name': 'Proposal Lead Team', 'project_id': 'proposal', 'discipline': 'Engineering', 'size': 20},
            {'id': 'proposal_team2', 'name': 'Proposal Development Team', 'project_id': 'proposal', 'discipline': 'Computer Science', 'size': 20},
            {'id': 'proposal_team3', 'name': 'Proposal Support Team', 'project_id': 'proposal', 'discipline': 'Design', 'size': 20}
        ],
        'faculty': [
            {'id': 'fac1', 'name': 'Dr. Sarah Chen', 'role': 'Faculty Advisor - Engineering'},
            {'id': 'fac2', 'name': 'Dr. James Rodriguez', 'role': 'Faculty Advisor - Computer Science'},
            {'id': 'staff1', 'name': 'Maria Garcia', 'role': 'Program Coordinator'}
        ],
        'interfaces': [
            # PROVES to other projects (nucleus connections) - healthy
            {'from': 'proves', 'to': 'contract', 'energy_loss': 0.1, 'type': 'knowledge_transfer'},
            {'from': 'proves', 'to': 'proposal', 'energy_loss': 0.15, 'type': 'knowledge_transfer'},
            # Project to team connections
            {'from': 'proves', 'to': 'proves_team1', 'energy_loss': 0.12, 'type': 'project_team'},
            {'from': 'contract', 'to': 'contract_team1', 'energy_loss': 0.2, 'type': 'project_team'},
            {'from': 'contract', 'to': 'contract_team2', 'energy_loss': 0.25, 'type': 'project_team'},
            {'from': 'proposal', 'to': 'proposal_team1', 'energy_loss': 0.4, 'type': 'project_team'},
            {'from': 'proposal', 'to': 'proposal_team2', 'energy_loss': 0.5, 'type': 'project_team'},
            {'from': 'proposal', 'to': 'proposal_team3', 'energy_loss': 0.45, 'type': 'project_team'},
            # Faculty/staff mentoring
            {'from': 'fac1', 'to': 'proves_team1', 'energy_loss': 0.15, 'type': 'mentoring'},
            {'from': 'fac1', 'to': 'contract_team1', 'energy_loss': 0.2, 'type': 'mentoring'},
            {'from': 'fac2', 'to': 'contract_team2', 'energy_loss': 0.25, 'type': 'mentoring'},
            {'from': 'fac2', 'to': 'proposal_team2', 'energy_loss': 0.6, 'type': 'mentoring'},
            {'from': 'staff1', 'to': 'proposal_team1', 'energy_loss': 0.35, 'type': 'coordination'},
            {'from': 'staff1', 'to': 'proposal_team3', 'energy_loss': 0.4, 'type': 'coordination'},
            # Cross-project collaboration
            {'from': 'contract', 'to': 'proposal', 'energy_loss': 0.5, 'type': 'collaboration'}
        ]
    }
    
    return jsonify(sample_data)

# Data persistence file
DATA_FILE = 'frames_data.json'


def load_data():
    """Load data from file if exists"""
    if os.path.exists(DATA_FILE):
        try:
            system_state.load_from_file(DATA_FILE)
            print(f"Loaded data from {DATA_FILE}")
        except Exception as e:
            print(f"Error loading data: {e}")


def save_data():
    """Save data to file"""
    try:
        system_state.save_to_file(DATA_FILE)
    except Exception as e:
        print(f"Error saving data: {e}")


def _log_audit(actor, action, entity_type, entity_id, before, after, meta=None):
    """Append an audit log row to the DB (best-effort)."""
    try:
        # lazy import to avoid circular issues during startup edits
        from db_models import AuditLog
        from app import db
        import json

        a = AuditLog(
            actor=(actor or 'system'),
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            payload_before=json.dumps(before) if before is not None else None,
            payload_after=json.dumps(after) if after is not None else None,
            meta=meta,
        )
        with app.app_context():
            db.session.add(a)
            db.session.commit()
    except Exception:
        # Audit should not block normal flow; log errors to stdout
        import traceback
        print('Audit log error:', traceback.format_exc())


# Load data on startup
load_data()

# Ensure database tables exist (use app_context to be compatible across Flask versions)
def ensure_tables():
    """Ensure database tables exist before serving requests."""
    try:
        with app.app_context():
            db.create_all()
        print('Database tables ensured (db.create_all).')
    except Exception as e:
        print('Could not create DB tables:', e)

# NOTE: table creation will be invoked after model definitions (below)

# Import DB-backed models so they are available for db.create_all()
try:
    import db_models  # noqa: F401 - registers models with SQLAlchemy
except Exception as _e:
    # If import fails (during editing), continue; tables will be created when possible
    print('Warning: could not import db_models at startup:', _e)


# ============================================================================
# ROUTES - Serve Frontend
# ============================================================================

@app.route('/')
def index():
    """Serve the landing page"""
    return send_from_directory('../frontend/templates', 'landing.html')


@app.route('/test')
def test_page():
    """Serve the developer test page"""
    return send_from_directory('../frontend/templates', 'index.html')


@app.route('/full')
def full_index():
    """Serve the full original application page for migration/testing"""
    return send_from_directory('../frontend/templates', 'index_original.html')


@app.route('/comparative')
def comparative_dashboard():
    """Serve the multi-university comparative dashboard (table/chart view)"""
    return send_from_directory('../frontend/templates', 'comparative_dashboard.html')


@app.route('/multi-university-network')
def multi_university_network():
    """Serve the multi-university 3D network visualization"""
    return send_from_directory('../frontend/templates', 'multi_university_network.html')


@app.route('/teams')
def teams_page():
    """Serve the teams management page"""
    return send_from_directory('../frontend/templates', 'teams.html')


@app.route('/students')
def students_page():
    """Serve the student roster management page"""
    return send_from_directory('../frontend/templates', 'students.html')


@app.route('/faculty')
def faculty_page():
    """Serve the faculty management page"""
    return send_from_directory('../frontend/templates', 'faculty.html')


@app.route('/projects')
def projects_page():
    """Serve the projects management page"""
    return send_from_directory('../frontend/templates', 'projects.html')


@app.route('/analytics')
def analytics_page():
    """Serve the analytics dashboard page"""
    return send_from_directory('../frontend/templates', 'analytics.html')


@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('../frontend/static', path)


# ============================================================================
# API ENDPOINTS - Teams
# ============================================================================

@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get all teams - optionally filtered by university"""
    from db_models import TeamModel

    try:
        university_id = request.args.get('university_id')

        if university_id:
            teams = TeamModel.query.filter_by(university_id=university_id).all()
        else:
            teams = TeamModel.query.all()

        return jsonify([t.to_dict() for t in teams])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/teams', methods=['POST'])
def create_team():
    """Create a new team"""
    from db_models import TeamModel

    try:
        data = request.json

        # Get actor's university from header
        actor_university = request.headers.get('X-University-ID', 'CalPolyPomona')

        # Generate ID if not provided
        if 'id' not in data:
            data['id'] = f"team_{int(datetime.now().timestamp() * 1000)}"

        # Set university_id if not provided (defaults to actor's university)
        if 'university_id' not in data:
            data['university_id'] = actor_university

        # Permission check: can only create teams for your own university (unless researcher)
        is_researcher = request.headers.get('X-Is-Researcher', 'false').lower() == 'true'
        if not is_researcher and data['university_id'] != actor_university:
            return jsonify({'error': 'Can only create teams for your own university'}), 403

        team = TeamModel(**data)
        db.session.add(team)
        db.session.commit()

        # Audit: record create
        try:
            _log_audit(actor_university, 'create', 'team', team.id, None, team.to_dict())
        except Exception:
            pass

        return jsonify(team.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/teams/<team_id>', methods=['GET'])
def get_team(team_id):
    """Get a specific team"""
    from db_models import TeamModel

    try:
        team = TeamModel.query.filter_by(id=team_id).first()
        if not team:
            return jsonify({'error': 'Team not found'}), 404
        return jsonify(team.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/teams/<team_id>', methods=['PUT'])
def update_team(team_id):
    """Update a team"""
    from db_models import TeamModel

    try:
        team = TeamModel.query.filter_by(id=team_id).first()
        if not team:
            return jsonify({'error': 'Team not found'}), 404

        before = team.to_dict()

        # Get actor's university
        actor_university = request.headers.get('X-University-ID', 'CalPolyPomona')
        is_researcher = request.headers.get('X-Is-Researcher', 'false').lower() == 'true'

        # Permission check: can only update your own university's teams
        if not is_researcher and team.university_id != actor_university:
            return jsonify({'error': 'Can only update teams from your own university'}), 403

        # Update fields
        data = request.json
        for key, value in data.items():
            if key != 'id' and hasattr(team, key):  # Don't change ID
                setattr(team, key, value)

        db.session.commit()

        # Audit: record update
        try:
            _log_audit(actor_university, 'update', 'team', team_id, before, team.to_dict())
        except Exception:
            pass

        return jsonify(team.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/teams/<team_id>', methods=['DELETE'])
def delete_team(team_id):
    """Delete a team"""
    from db_models import TeamModel

    try:
        team = TeamModel.query.filter_by(id=team_id).first()
        if not team:
            return jsonify({'error': 'Team not found'}), 404

        before = team.to_dict()

        # Get actor's university
        actor_university = request.headers.get('X-University-ID', 'CalPolyPomona')
        is_researcher = request.headers.get('X-Is-Researcher', 'false').lower() == 'true'

        # Permission check: can only delete your own university's teams
        if not is_researcher and team.university_id != actor_university:
            return jsonify({'error': 'Can only delete teams from your own university'}), 403

        db.session.delete(team)
        db.session.commit()

        try:
            _log_audit(actor_university, 'delete', 'team', team_id, before, None)
        except Exception:
            pass

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# API ENDPOINTS - Students
# ============================================================================

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students, optionally filtered by university, team, or project"""
    from db_models import StudentModel

    university_id = request.args.get('university_id')
    team_id = request.args.get('team_id')
    project_id = request.args.get('project_id')
    active_only = request.args.get('active', 'true').lower() == 'true'

    try:
        query = StudentModel.query

        if university_id:
            query = query.filter_by(university_id=university_id)
        if team_id:
            query = query.filter_by(team_id=team_id)
        if project_id:
            query = query.filter_by(project_id=project_id)
        if active_only:
            query = query.filter_by(active=True)

        students = query.all()
        return jsonify([s.to_dict() for s in students])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students', methods=['POST'])
def create_student():
    """Create a new student"""
    from db_models import StudentModel
    import uuid

    data = request.json
    student_id = f"student_{uuid.uuid4().hex[:12]}"

    try:
        student = StudentModel(
            id=student_id,
            university_id=data['university_id'],
            name=data['name'],
            team_id=data.get('team_id'),
            expertise_area=data.get('expertise_area'),
            graduation_term=data.get('graduation_term'),
            terms_remaining=data.get('terms_remaining', 4),
            is_lead=data.get('is_lead', False)
        )

        # Auto-calculate status
        student.status = student.calculate_status()

        db.session.add(student)
        db.session.commit()

        return jsonify(student.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student"""
    from db_models import StudentModel

    try:
        student = StudentModel.query.filter_by(id=student_id).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        db.session.delete(student)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    """Update a student"""
    from db_models import StudentModel

    try:
        student = StudentModel.query.filter_by(id=student_id).first()
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        data = request.json

        if 'name' in data:
            student.name = data['name']
        if 'team_id' in data:
            student.team_id = data['team_id']
        if 'expertise_area' in data:
            student.expertise_area = data['expertise_area']
        if 'graduation_term' in data:
            student.graduation_term = data['graduation_term']
        if 'terms_remaining' in data:
            student.terms_remaining = data['terms_remaining']
            student.status = student.calculate_status()
        if 'is_lead' in data:
            student.is_lead = data['is_lead']

        db.session.commit()
        return jsonify(student.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/university/<university_id>/advance-term', methods=['POST'])
def advance_term(university_id):
    """Advance all students in a university by one term"""
    from db_models import StudentModel

    try:
        students = StudentModel.query.filter_by(university_id=university_id, active=True).all()

        graduated_count = 0
        updated_count = 0

        for student in students:
            student.terms_remaining -= 1

            if student.terms_remaining <= 0:
                student.active = False
                student.graduated_at = datetime.now().isoformat()
                graduated_count += 1
            else:
                student.status = student.calculate_status()
                updated_count += 1

        db.session.commit()

        return jsonify({
            'success': True,
            'graduated': graduated_count,
            'updated': updated_count,
            'message': f'{updated_count} students advanced, {graduated_count} graduated'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# API ENDPOINTS - Faculty
# ============================================================================

@app.route('/api/faculty', methods=['GET'])
def get_faculty():
    """Get all faculty - optionally filtered by university"""
    from db_models import FacultyModel

    try:
        university_id = request.args.get('university_id')

        if university_id:
            faculty = FacultyModel.query.filter_by(university_id=university_id).all()
        else:
            faculty = FacultyModel.query.all()

        return jsonify([f.to_dict() for f in faculty])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/faculty', methods=['POST'])
def create_faculty():
    """Create a new faculty member"""
    from db_models import FacultyModel

    try:
        data = request.json

        # Get actor's university from header
        actor_university = request.headers.get('X-University-ID', 'CalPolyPomona')

        # Generate ID if not provided
        if 'id' not in data:
            data['id'] = f"faculty_{int(datetime.now().timestamp() * 1000)}"

        # Set university_id if not provided
        if 'university_id' not in data:
            data['university_id'] = actor_university

        # Permission check
        is_researcher = request.headers.get('X-Is-Researcher', 'false').lower() == 'true'
        if not is_researcher and data['university_id'] != actor_university:
            return jsonify({'error': 'Can only create faculty for your own university'}), 403

        faculty = FacultyModel(**data)
        db.session.add(faculty)
        db.session.commit()

        try:
            _log_audit(actor_university, 'create', 'faculty', faculty.id, None, faculty.to_dict())
        except Exception:
            pass

        return jsonify(faculty.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/faculty/<faculty_id>', methods=['DELETE'])
def delete_faculty(faculty_id):
    """Delete a faculty member"""
    from db_models import FacultyModel

    try:
        faculty = FacultyModel.query.filter_by(id=faculty_id).first()
        if not faculty:
            return jsonify({'error': 'Faculty not found'}), 404

        before = faculty.to_dict()

        # Permission check
        actor_university = request.headers.get('X-University-ID', 'CalPolyPomona')
        is_researcher = request.headers.get('X-Is-Researcher', 'false').lower() == 'true'

        if not is_researcher and faculty.university_id != actor_university:
            return jsonify({'error': 'Can only delete faculty from your own university'}), 403

        db.session.delete(faculty)
        db.session.commit()

        try:
            _log_audit(actor_university, 'delete', 'faculty', faculty_id, before, None)
        except Exception:
            pass

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# API ENDPOINTS - Projects
# ============================================================================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects - optionally filtered by university"""
    from db_models import ProjectModel

    try:
        university_id = request.args.get('university_id')

        if university_id:
            projects = ProjectModel.query.filter_by(university_id=university_id).all()
        else:
            projects = ProjectModel.query.all()

        return jsonify([p.to_dict() for p in projects])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    from db_models import ProjectModel

    try:
        data = request.json

        # Get actor's university from header
        actor_university = request.headers.get('X-University-ID', 'CalPolyPomona')

        # Generate ID if not provided
        if 'id' not in data:
            data['id'] = f"project_{int(datetime.now().timestamp() * 1000)}"

        # Set university_id if not provided (unless creating PROVES or collaborative project)
        if 'university_id' not in data:
            if data.get('is_collaborative'):
                data['university_id'] = None  # Shared collaborative projects have NULL university_id
            else:
                data['university_id'] = actor_university

        # Permission check
        is_researcher = request.headers.get('X-Is-Researcher', 'false').lower() == 'true'
        if not is_researcher and data.get('university_id') and data['university_id'] != actor_university:
            return jsonify({'error': 'Can only create projects for your own university'}), 403

        project = ProjectModel(**data)
        db.session.add(project)
        db.session.commit()

        try:
            _log_audit(actor_university, 'create', 'project', project.id, None, project.to_dict())
        except Exception:
            pass

        return jsonify(project.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project"""
    from db_models import ProjectModel

    try:
        project = ProjectModel.query.filter_by(id=project_id).first()
        if not project:
            return jsonify({'error': 'Project not found'}), 404

        before = project.to_dict()

        # Permission check
        actor_university = request.headers.get('X-University-ID', 'CalPolyPomona')
        is_researcher = request.headers.get('X-Is-Researcher', 'false').lower() == 'true'

        # Can't delete shared collaborative projects unless researcher
        if project.is_collaborative and not is_researcher:
            return jsonify({'error': 'Only researchers can delete collaborative projects'}), 403

        # Can only delete your own university's projects
        if not is_researcher and project.university_id and project.university_id != actor_university:
            return jsonify({'error': 'Can only delete projects from your own university'}), 403

        db.session.delete(project)
        db.session.commit()

        try:
            _log_audit(actor_university, 'delete', 'project', project_id, before, None)
        except Exception:
            pass

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# API ENDPOINTS - Interfaces
# ============================================================================

@app.route('/api/interfaces', methods=['GET'])
def get_interfaces():
    """Get all interfaces - optionally filtered by university or cross-university"""
    from db_models import InterfaceModel

    try:
        university_id = request.args.get('university_id')
        cross_university = request.args.get('cross_university')

        query = InterfaceModel.query

        # Filter by university (interfaces where this university is involved)
        if university_id:
            query = query.filter(
                (InterfaceModel.from_university == university_id) |
                (InterfaceModel.to_university == university_id)
            )

        # Filter by cross-university flag
        if cross_university and cross_university.lower() == 'true':
            query = query.filter_by(is_cross_university=True)
        elif cross_university and cross_university.lower() == 'false':
            query = query.filter_by(is_cross_university=False)

        interfaces = query.all()
        return jsonify([i.to_dict() for i in interfaces])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/interfaces', methods=['POST'])
def create_interface():
    """Create a new interface"""
    from db_models import InterfaceModel

    try:
        data = request.json

        # Get actor's university from header
        actor_university = request.headers.get('X-University-ID', 'CalPolyPomona')

        # Generate ID if not provided
        if 'id' not in data:
            data['id'] = f"interface_{int(datetime.now().timestamp() * 1000)}"

        # Extract university IDs from entity IDs (format: UniversityID_entity_name)
        from_entity = data.get('from_entity', '')
        to_entity = data.get('to_entity', '')

        # Parse universities from entity IDs
        if '_' in from_entity:
            from_uni = from_entity.split('_')[0]
        else:
            from_uni = actor_university

        if '_' in to_entity:
            to_uni = to_entity.split('_')[0]
        else:
            to_uni = actor_university

        # Set university fields
        data['from_university'] = from_uni
        data['to_university'] = to_uni
        data['is_cross_university'] = (from_uni != to_uni)

        # Permission check: can create interfaces involving your university
        is_researcher = request.headers.get('X-Is-Researcher', 'false').lower() == 'true'
        if not is_researcher and from_uni != actor_university and to_uni != actor_university:
            return jsonify({'error': 'Can only create interfaces involving your own university'}), 403

        interface = InterfaceModel(**data)
        db.session.add(interface)
        db.session.commit()

        try:
            _log_audit(actor_university, 'create', 'interface', interface.id, None, interface.to_dict())
        except Exception:
            pass

        return jsonify(interface.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/interfaces/<interface_id>', methods=['DELETE'])
def delete_interface(interface_id):
    """Delete an interface"""
    from db_models import InterfaceModel

    try:
        interface = InterfaceModel.query.filter_by(id=interface_id).first()
        if not interface:
            return jsonify({'error': 'Interface not found'}), 404

        before = interface.to_dict()

        # Permission check
        actor_university = request.headers.get('X-University-ID', 'CalPolyPomona')
        is_researcher = request.headers.get('X-Is-Researcher', 'false').lower() == 'true'

        # Can only delete interfaces involving your university
        if not is_researcher and interface.from_university != actor_university and interface.to_university != actor_university:
            return jsonify({'error': 'Can only delete interfaces involving your own university'}), 403

        db.session.delete(interface)
        db.session.commit()

        try:
            _log_audit(actor_university, 'delete', 'interface', interface_id, before, None)
        except Exception:
            pass

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# API ENDPOINTS - Analytics
# ============================================================================

@app.route('/api/analytics/statistics', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    analytics = FramesAnalytics(system_state)
    return jsonify(analytics.calculate_statistics())


@app.route('/api/analytics/nda-diagnostic', methods=['GET'])
def get_nda_diagnostic():
    """Get NDA diagnostic analysis"""
    analytics = FramesAnalytics(system_state)
    return jsonify(analytics.get_nda_diagnostic_analysis())


@app.route('/api/analytics/backward-tracing', methods=['GET'])
def get_backward_tracing():
    """Get backward tracing analysis"""
    analytics = FramesAnalytics(system_state)
    return jsonify(analytics.get_backward_tracing_analysis())


@app.route('/api/analytics/team-lifecycle', methods=['GET'])
def get_team_lifecycle():
    """Get team lifecycle analysis"""
    analytics = FramesAnalytics(system_state)
    return jsonify(analytics.analyze_team_lifecycle())


# ============================================================================
# API ENDPOINTS - System State
# ============================================================================

@app.route('/api/state', methods=['GET'])
def get_state():
    """Get complete system state"""
    return jsonify(system_state.to_dict())


@app.route('/api/state', methods=['POST'])
def set_state():
    """Set complete system state (for load/import)"""
    data = request.json
    system_state.from_dict(data)
    save_data()
    return jsonify({'success': True})


@app.route('/api/state/reset', methods=['POST'])
def reset_state():
    """Reset system to empty state"""
    global system_state
    system_state = SystemState()
    save_data()
    return jsonify({'success': True})


# ============================================================================
# API ENDPOINTS - Sandboxes
# ============================================================================

def _now_ts():
    return datetime.now().isoformat()


class Sandbox(db.Model):
    __tablename__ = 'sandboxes'
    id = db.Column(db.String, primary_key=True)
    university_id = db.Column(db.String, index=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    data = db.Column(db.Text)  # JSON string of state
    created_at = db.Column(db.String, default=_now_ts)
    updated_at = db.Column(db.String, default=_now_ts, onupdate=_now_ts)

    def to_dict(self):
        try:
            payload = json.loads(self.data) if self.data else {}
        except Exception:
            payload = {}
        return {
            'id': self.id,
            'university_id': self.university_id,
            'name': self.name,
            'data': payload,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


@app.route('/api/sandboxes', methods=['GET'])
def list_sandboxes():
    university_id = request.args.get('university_id')
    if university_id:
        rows = Sandbox.query.filter_by(university_id=university_id).all()
    else:
        rows = Sandbox.query.all()
    return jsonify([r.to_dict() for r in rows])


@app.route('/api/sandboxes', methods=['POST'])
def create_sandbox():
    data = request.json or {}
    if 'id' not in data:
        data['id'] = f"sandbox_{int(datetime.now().timestamp() * 1000)}"
    if 'university_id' not in data:
        return jsonify({'error': 'university_id is required'}), 400
    sandbox = Sandbox(
        id=data['id'],
        university_id=data['university_id'],
        name=data.get('name', 'Play Sandbox'),
        data=json.dumps(data.get('data', {})),
        created_at=_now_ts(),
        updated_at=_now_ts()
    )
    db.session.add(sandbox)
    db.session.commit()
    try:
        _log_audit(request.headers.get('X-Actor', 'system'), 'create', 'sandbox', sandbox.id, None, {
            'name': sandbox.name,
            'university_id': sandbox.university_id,
            'data': json.loads(sandbox.data) if sandbox.data else {}
        })
    except Exception:
        pass
    return jsonify(sandbox.to_dict()), 201


@app.route('/api/sandboxes/<sandbox_id>', methods=['GET'])
def get_sandbox(sandbox_id):
    s = Sandbox.query.get(sandbox_id)
    if not s:
        return jsonify({'error': 'Sandbox not found'}), 404
    return jsonify(s.to_dict())


@app.route('/api/sandboxes/<sandbox_id>', methods=['PUT'])
def update_sandbox(sandbox_id):
    s = Sandbox.query.get(sandbox_id)
    if not s:
        return jsonify({'error': 'Sandbox not found'}), 404
    data = request.json or {}
    s.name = data.get('name', s.name)
    s.university_id = data.get('university_id', s.university_id)
    if 'data' in data:
        s.data = json.dumps(data.get('data') or {})
    before = {
        'name': s.name,
        'university_id': s.university_id,
        'data': json.loads(s.data) if s.data else {}
    }
    s.updated_at = _now_ts()
    db.session.commit()
    try:
        _log_audit(request.headers.get('X-Actor', 'system'), 'update', 'sandbox', sandbox_id, before, {
            'name': s.name,
            'university_id': s.university_id,
            'data': json.loads(s.data) if s.data else {}
        })
    except Exception:
        pass
    return jsonify(s.to_dict())


@app.route('/api/sandboxes/<sandbox_id>', methods=['DELETE'])
def delete_sandbox(sandbox_id):
    s = Sandbox.query.get(sandbox_id)
    if not s:
        return jsonify({'error': 'Sandbox not found'}), 404
    before = {
        'name': s.name,
        'university_id': s.university_id,
        'data': json.loads(s.data) if s.data else {}
    }
    db.session.delete(s)
    db.session.commit()
    try:
        _log_audit(request.headers.get('X-Actor', 'system'), 'delete', 'sandbox', sandbox_id, before, None)
    except Exception:
        pass
    return jsonify({'success': True})


@app.route('/api/sandboxes/<sandbox_id>/copy-live', methods=['POST'])
def copy_live_to_sandbox(sandbox_id):
    s = Sandbox.query.get(sandbox_id)
    if not s:
        return jsonify({'error': 'Sandbox not found'}), 404
    s.data = json.dumps(system_state.to_dict())
    s.updated_at = _now_ts()
    db.session.commit()
    return jsonify(s.to_dict())


# Ensure database tables exist now that models are defined
try:
    with app.app_context():
        db.create_all()
        print('Database tables ensured (db.create_all) after model definitions.')
except Exception as e:
    print('Could not create DB tables after model definitions:', e)


# ============================================================================
# API ENDPOINTS - Sample Data
# ============================================================================

@app.route('/api/sample-data', methods=['POST'])
def load_sample_data():
    """Load sample data based on Bronco Space Lab structure"""
    print('DEBUG: /api/sample-data endpoint HIT')

    # Import DB models (imports are fine inside route functions)
    from db_models import TeamModel, FacultyModel, ProjectModel, InterfaceModel

    # Clear existing data from DB
    TeamModel.query.delete()
    FacultyModel.query.delete()
    ProjectModel.query.delete()
    InterfaceModel.query.delete()
    db.session.commit()

    # Add sample teams
    sample_teams = [
        {'id': 'team_1', 'discipline': 'electrical', 'lifecycle': 'established',
         'name': 'Power Systems', 'size': 4, 'experience': 18,
         'description': 'Power and avionics systems - experienced team'},
        {'id': 'team_2', 'discipline': 'electrical', 'lifecycle': 'incoming',
         'name': 'Electrical Beta', 'size': 3, 'experience': 6,
         'description': 'New electrical team in training phase'},
        {'id': 'team_3', 'discipline': 'software', 'lifecycle': 'established',
         'name': 'Flight Software', 'size': 5, 'experience': 24,
         'description': 'Flight software and data processing'},
        {'id': 'team_4', 'discipline': 'software', 'lifecycle': 'outgoing',
         'name': 'Software Legacy', 'size': 2, 'experience': 36,
         'description': 'Graduating software team with critical knowledge'},
        {'id': 'team_5', 'discipline': 'mission-ops', 'lifecycle': 'incoming',
         'name': 'Mission Ops New', 'size': 3, 'experience': 3,
         'description': 'New mission operations team'},
        {'id': 'team_6', 'discipline': 'mission-ops', 'lifecycle': 'established',
         'name': 'Mission Ops Core', 'size': 4, 'experience': 15,
         'description': 'Established operations team'},
        {'id': 'team_7', 'discipline': 'mechanical', 'lifecycle': 'established',
         'name': 'Mechanical Systems', 'size': 3, 'experience': 12,
         'description': 'Mechanical systems and structures'},
        {'id': 'team_8', 'discipline': 'communications', 'lifecycle': 'incoming',
         'name': 'Comm Systems', 'size': 2, 'experience': 4,
         'description': 'New communications team'}
    ]
    for team_data in sample_teams:
        print('Inserting team:', team_data)
        db.session.add(TeamModel(**team_data))

    # Add sample faculty
    sample_faculty = [
        {'id': 'faculty_1', 'name': 'Dr. Principal Investigator',
         'role': 'Principal Investigator',
         'description': 'Project oversight and coordination, institutional interface'},
        {'id': 'faculty_2', 'name': 'Dr. Technical Lead',
         'role': 'Technical Lead',
         'description': 'Technical guidance and mentoring, knowledge transfer'},
        {'id': 'faculty_3', 'name': 'Program Director',
         'role': 'Program Director',
         'description': 'Program continuity and institutional support'}
    ]
    for faculty_data in sample_faculty:
        print('Inserting faculty:', faculty_data)
        db.session.add(FacultyModel(**faculty_data))

    # Add sample projects
    sample_projects = [
        {'id': 'project_1', 'name': 'JPL CubeSat Mission',
         'type': 'jpl-contract', 'duration': 3,
         'description': 'Primary satellite mission with JPL contract'},
        {'id': 'project_2', 'name': 'Multi-University Research',
         'type': 'multiversity', 'duration': 2,
         'description': 'Multi-university collaborative research project'},
        {'id': 'project_3', 'name': 'Contract Pursuit',
         'type': 'contract-pursuit', 'duration': 1,
         'description': 'New contract opportunity being pursued'}
    ]
    for project_data in sample_projects:
        print('Inserting project:', project_data)
        db.session.add(ProjectModel(**project_data))

    # Add sample interfaces (field names must match model)
    sample_interfaces = [
        # Faculty connections (codified interfaces)
        {'id': 'interface_1', 'from_entity': 'team_1', 'to_entity': 'faculty_1',
         'interface_type': 'team-to-faculty', 'bond_type': 'codified-strong', 'energy_loss': 5},
        {'id': 'interface_2', 'from_entity': 'team_3', 'to_entity': 'faculty_2',
         'interface_type': 'team-to-faculty', 'bond_type': 'codified-strong', 'energy_loss': 5},
        {'id': 'interface_3', 'from_entity': 'team_6', 'to_entity': 'faculty_3',
         'interface_type': 'team-to-faculty', 'bond_type': 'codified-moderate', 'energy_loss': 15},

        # Institutional knowledge interfaces (weaker bonds)
        {'id': 'interface_4', 'from_entity': 'team_4', 'to_entity': 'team_3',
         'interface_type': 'team-to-team', 'bond_type': 'institutional-weak', 'energy_loss': 35},
        {'id': 'interface_5', 'from_entity': 'team_2', 'to_entity': 'team_1',
         'interface_type': 'team-to-team', 'bond_type': 'institutional-weak', 'energy_loss': 35},
        {'id': 'interface_6', 'from_entity': 'team_5', 'to_entity': 'team_6',
         'interface_type': 'team-to-team', 'bond_type': 'institutional-weak', 'energy_loss': 35},

        # Project interfaces
        {'id': 'interface_7', 'from_entity': 'team_1', 'to_entity': 'project_1',
         'interface_type': 'team-to-project', 'bond_type': 'codified-strong', 'energy_loss': 5},
        {'id': 'interface_8', 'from_entity': 'team_3', 'to_entity': 'project_1',
         'interface_type': 'team-to-project', 'bond_type': 'codified-strong', 'energy_loss': 5},
        {'id': 'interface_9', 'from_entity': 'team_6', 'to_entity': 'project_2',
         'interface_type': 'team-to-project', 'bond_type': 'codified-moderate', 'energy_loss': 15},
        {'id': 'interface_10', 'from_entity': 'team_7', 'to_entity': 'project_2',
         'interface_type': 'team-to-project', 'bond_type': 'codified-moderate', 'energy_loss': 15},
        {'id': 'interface_11', 'from_entity': 'team_8', 'to_entity': 'project_3',
         'interface_type': 'team-to-project', 'bond_type': 'fragile-temporary', 'energy_loss': 60}
    ]
    for interface_data in sample_interfaces:
        print('Inserting interface:', interface_data)
        db.session.add(InterfaceModel(**interface_data))

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Sample data loaded into database successfully',
    })


# ============================================================================
# API ENDPOINTS - Multi-University Support
# ============================================================================

@app.route('/api/universities', methods=['GET'])
def get_universities():
    """Get all universities"""
    from db_models import University

    try:
        universities = University.query.filter_by(active=True).all()
        return jsonify([uni.to_dict() for uni in universities])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/universities/<university_id>', methods=['GET'])
def get_university(university_id):
    """Get a specific university"""
    from db_models import University

    try:
        university = University.query.filter_by(id=university_id).first()
        if not university:
            return jsonify({'error': 'University not found'}), 404
        return jsonify(university.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# API ENDPOINTS - Outcomes
# ============================================================================

@app.route('/api/outcomes', methods=['GET'])
def get_outcomes():
    """Get outcomes - optionally filtered by university"""
    from db_models import Outcome

    try:
        university_id = request.args.get('university_id')

        if university_id:
            outcomes = Outcome.query.filter_by(university_id=university_id).all()
        else:
            outcomes = Outcome.query.all()

        return jsonify([outcome.to_dict() for outcome in outcomes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/outcomes', methods=['POST'])
def create_outcome():
    """Record a new outcome (mission success or program success)"""
    from db_models import Outcome

    try:
        data = request.json

        # Get actor's university from header (for now)
        actor_university = request.headers.get('X-University-ID', 'system')

        # Ensure outcome belongs to actor's university (unless system/researcher)
        is_researcher = request.headers.get('X-Is-Researcher', 'false').lower() == 'true'
        if not is_researcher and 'university_id' in data and data['university_id'] != actor_university:
            return jsonify({'error': 'Can only create outcomes for your own university'}), 403

        outcome = Outcome(**data)
        db.session.add(outcome)
        db.session.commit()

        # Audit log
        try:
            _log_audit(actor_university, 'create', 'outcome', outcome.id, None, outcome.to_dict())
        except Exception:
            pass

        return jsonify(outcome.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# API ENDPOINTS - Comparative Dashboard
# ============================================================================

@app.route('/api/dashboard/comparative', methods=['GET'])
def get_comparative_dashboard():
    """
    Return aggregated data for all universities for side-by-side comparison.

    This is the main endpoint for the collaborative learning dashboard where
    all 8 universities can see each other's data to learn from patterns.
    """
    from db_models import University, TeamModel, FacultyModel, ProjectModel, InterfaceModel

    try:
        # Get all active universities
        universities = University.query.filter_by(active=True).all()

        result = {
            'universities': {},
            'cross_university_interfaces': [],
            'proves_project': None,
            'aggregate_metrics': {}
        }

        # Aggregate totals across all universities
        total_teams = 0
        total_faculty = 0
        total_projects = 0
        total_interfaces = 0

        # Build data for each university
        for uni in universities:
            uni_id = uni.id

            # Get all entities for this university
            teams = TeamModel.query.filter_by(university_id=uni_id).all()
            faculty = FacultyModel.query.filter_by(university_id=uni_id).all()
            projects = ProjectModel.query.filter_by(university_id=uni_id).all()

            # Get interfaces involving this university (both from and to)
            interfaces = InterfaceModel.query.filter(
                (InterfaceModel.from_university == uni_id) |
                (InterfaceModel.to_university == uni_id)
            ).all()

            # Count internal vs cross-university interfaces
            internal_interfaces = [i for i in interfaces if not i.is_cross_university]
            cross_interfaces = [i for i in interfaces if i.is_cross_university]

            result['universities'][uni_id] = {
                'info': uni.to_dict(),
                'teams': [t.to_dict() for t in teams],
                'faculty': [f.to_dict() for f in faculty],
                'projects': [p.to_dict() for p in projects],
                'interfaces': {
                    'internal': [i.to_dict() for i in internal_interfaces],
                    'cross_university': [i.to_dict() for i in cross_interfaces],
                },
                'metrics': {
                    'team_count': len(teams),
                    'faculty_count': len(faculty),
                    'project_count': len(projects),
                    'interface_count': len(interfaces),
                    'cross_university_interface_count': len(cross_interfaces),
                }
            }

            # Aggregate totals
            total_teams += len(teams)
            total_faculty += len(faculty)
            total_projects += len(projects)
            total_interfaces += len(interfaces)

        # Get PROVES shared project
        proves = ProjectModel.query.filter_by(id='PROVES').first()
        if proves:
            result['proves_project'] = proves.to_dict()

        # Get all cross-university interfaces
        all_cross_interfaces = InterfaceModel.query.filter_by(is_cross_university=True).all()
        result['cross_university_interfaces'] = [i.to_dict() for i in all_cross_interfaces]

        # Aggregate metrics
        result['aggregate_metrics'] = {
            'university_count': len(universities),
            'total_teams': total_teams,
            'total_faculty': total_faculty,
            'total_projects': total_projects,
            'total_interfaces': total_interfaces,
            'cross_university_interfaces': len(all_cross_interfaces),
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/dashboard/proves', methods=['GET'])
def get_proves_dashboard():
    """Get PROVES collaborative project details with all university participation"""
    from db_models import ProjectModel, TeamModel, InterfaceModel

    try:
        # Get PROVES project
        proves = ProjectModel.query.filter_by(id='PROVES').first()
        if not proves:
            return jsonify({'error': 'PROVES project not found'}), 404

        # Get all teams working on PROVES (teams with 'proves' in their ID)
        proves_teams = TeamModel.query.filter(TeamModel.id.like('%_proves')).all()

        # Get all PROVES-related interfaces (cross-university only)
        proves_interfaces = InterfaceModel.query.filter(
            InterfaceModel.is_cross_university == True
        ).all()

        result = {
            'project': proves.to_dict(),
            'participating_teams': [t.to_dict() for t in proves_teams],
            'collaboration_interfaces': [i.to_dict() for i in proves_interfaces],
            'metrics': {
                'university_count': len(set([t.university_id for t in proves_teams])),
                'team_count': len(proves_teams),
                'interface_count': len(proves_interfaces),
            }
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# API ENDPOINTS - Analytics (Dynamic Dashboard)
# ============================================================================

@app.route('/api/analytics/data', methods=['POST'])
def get_analytics_data():
    """
    Flexible analytics endpoint that returns aggregated data based on user selections.

    Request body:
    {
        "metric": "student_count" | "team_count" | "faculty_count" | "avg_terms_remaining" | "expertise_distribution",
        "groupBy": "university" | "project" | "team" | "expertise_area" | "status" | "role",
        "filters": {
            "university_id": "CalPolyPomona",
            "project_id": "PROVES",
            "team_id": "team_abc",
            "status": "established",
            "expertise_area": "Software"
        },
        "timeRange": {
            "start": "2024-01-01",
            "end": "2024-12-31"
        }
    }
    """
    from db_models import StudentModel, TeamModel, FacultyModel, ProjectModel
    from sqlalchemy import func

    try:
        data = request.json
        metric = data.get('metric', 'student_count')
        group_by = data.get('groupBy')
        filters = data.get('filters', {})

        result = []

        # ==== STUDENT METRICS ====
        if metric == 'student_count':
            query = db.session.query(
                StudentModel.university_id if group_by == 'university' else
                StudentModel.team_id if group_by == 'team' else
                StudentModel.expertise_area if group_by == 'expertise_area' else
                StudentModel.status if group_by == 'status' else
                func.count().label('value'),
                func.count(StudentModel.id).label('count')
            )

            # Apply filters
            if filters.get('university_id'):
                query = query.filter(StudentModel.university_id == filters['university_id'])
            if filters.get('team_id'):
                query = query.filter(StudentModel.team_id == filters['team_id'])
            if filters.get('status'):
                query = query.filter(StudentModel.status == filters['status'])
            if filters.get('expertise_area'):
                query = query.filter(StudentModel.expertise_area == filters['expertise_area'])

            # Group by dimension
            if group_by:
                if group_by == 'university':
                    query = query.group_by(StudentModel.university_id)
                elif group_by == 'team':
                    query = query.group_by(StudentModel.team_id)
                elif group_by == 'expertise_area':
                    query = query.group_by(StudentModel.expertise_area)
                elif group_by == 'status':
                    query = query.group_by(StudentModel.status)

                results = query.all()
                result = [{'label': str(r[0] or 'Unknown'), 'value': r[1]} for r in results]
            else:
                # Total count without grouping
                count = query.filter(StudentModel.active == True).count()
                result = [{'label': 'Total Students', 'value': count}]

        elif metric == 'avg_terms_remaining':
            query = db.session.query(
                StudentModel.university_id if group_by == 'university' else
                StudentModel.team_id if group_by == 'team' else
                StudentModel.status if group_by == 'status' else
                func.avg(StudentModel.terms_remaining).label('avg_terms'),
                func.avg(StudentModel.terms_remaining).label('value')
            )

            # Apply filters
            if filters.get('university_id'):
                query = query.filter(StudentModel.university_id == filters['university_id'])
            if filters.get('team_id'):
                query = query.filter(StudentModel.team_id == filters['team_id'])
            if filters.get('status'):
                query = query.filter(StudentModel.status == filters['status'])

            query = query.filter(StudentModel.active == True)

            # Group by dimension
            if group_by:
                if group_by == 'university':
                    query = query.group_by(StudentModel.university_id)
                elif group_by == 'team':
                    query = query.group_by(StudentModel.team_id)
                elif group_by == 'status':
                    query = query.group_by(StudentModel.status)

                results = query.all()
                result = [{'label': str(r[0] or 'Unknown'), 'value': round(float(r[1] or 0), 2)} for r in results]
            else:
                avg = query.scalar() or 0
                result = [{'label': 'Average Terms Remaining', 'value': round(float(avg), 2)}]

        elif metric == 'status_distribution':
            query = db.session.query(
                StudentModel.status,
                func.count(StudentModel.id).label('count')
            ).filter(StudentModel.active == True)

            # Apply filters
            if filters.get('university_id'):
                query = query.filter(StudentModel.university_id == filters['university_id'])
            if filters.get('team_id'):
                query = query.filter(StudentModel.team_id == filters['team_id'])

            query = query.group_by(StudentModel.status)
            results = query.all()

            result = [{'label': str(r[0] or 'Unknown').title(), 'value': r[1]} for r in results]

        # ==== TEAM METRICS ====
        elif metric == 'team_count':
            query = db.session.query(
                TeamModel.university_id if group_by == 'university' else
                TeamModel.project_id if group_by == 'project' else
                TeamModel.discipline if group_by == 'discipline' else
                func.count().label('value'),
                func.count(TeamModel.id).label('count')
            )

            # Apply filters
            if filters.get('university_id'):
                query = query.filter(TeamModel.university_id == filters['university_id'])
            if filters.get('project_id'):
                query = query.filter(TeamModel.project_id == filters['project_id'])
            if filters.get('discipline'):
                query = query.filter(TeamModel.discipline == filters['discipline'])

            # Group by dimension
            if group_by:
                if group_by == 'university':
                    query = query.group_by(TeamModel.university_id)
                elif group_by == 'project':
                    query = query.group_by(TeamModel.project_id)
                elif group_by == 'discipline':
                    query = query.group_by(TeamModel.discipline)

                results = query.all()
                result = [{'label': str(r[0] or 'Unknown'), 'value': r[1]} for r in results]
            else:
                count = query.count()
                result = [{'label': 'Total Teams', 'value': count}]

        # ==== FACULTY METRICS ====
        elif metric == 'faculty_count':
            query = db.session.query(
                FacultyModel.university_id if group_by == 'university' else
                FacultyModel.role if group_by == 'role' else
                func.count().label('value'),
                func.count(FacultyModel.id).label('count')
            )

            # Apply filters
            if filters.get('university_id'):
                query = query.filter(FacultyModel.university_id == filters['university_id'])
            if filters.get('role'):
                query = query.filter(FacultyModel.role == filters['role'])

            # Group by dimension
            if group_by:
                if group_by == 'university':
                    query = query.group_by(FacultyModel.university_id)
                elif group_by == 'role':
                    query = query.group_by(FacultyModel.role)

                results = query.all()
                result = [{'label': str(r[0] or 'Unknown'), 'value': r[1]} for r in results]
            else:
                count = query.count()
                result = [{'label': 'Total Faculty/Mentors', 'value': count}]

        # ==== PROJECT METRICS ====
        elif metric == 'project_count':
            query = db.session.query(
                ProjectModel.university_id if group_by == 'university' else
                ProjectModel.type if group_by == 'type' else
                func.count().label('value'),
                func.count(ProjectModel.id).label('count')
            )

            # Apply filters
            if filters.get('university_id'):
                query = query.filter(ProjectModel.university_id == filters['university_id'])
            if filters.get('type'):
                query = query.filter(ProjectModel.type == filters['type'])

            # Group by dimension
            if group_by:
                if group_by == 'university':
                    query = query.group_by(ProjectModel.university_id)
                elif group_by == 'type':
                    query = query.group_by(ProjectModel.type)

                results = query.all()
                result = [{'label': str(r[0] or 'Unknown'), 'value': r[1]} for r in results]
            else:
                count = query.count()
                result = [{'label': 'Total Projects', 'value': count}]

        # ==== CROSS-TABULATION (Two dimensions) ====
        elif metric == 'students_by_status_and_expertise':
            query = db.session.query(
                StudentModel.status,
                StudentModel.expertise_area,
                func.count(StudentModel.id).label('count')
            ).filter(StudentModel.active == True)

            if filters.get('university_id'):
                query = query.filter(StudentModel.university_id == filters['university_id'])

            query = query.group_by(StudentModel.status, StudentModel.expertise_area)
            results = query.all()

            # Format for grouped bar chart or heatmap
            result = [
                {
                    'status': str(r[0] or 'Unknown'),
                    'expertise': str(r[1] or 'Unknown'),
                    'value': r[2]
                }
                for r in results
            ]

        return jsonify({
            'metric': metric,
            'groupBy': group_by,
            'data': result
        })

    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500


@app.route('/api/analytics/dimensions', methods=['GET'])
def get_analytics_dimensions():
    """Return available dimensions and metrics for the analytics dashboard"""
    return jsonify({
        'metrics': [
            {'value': 'student_count', 'label': 'Student Count', 'description': 'Total number of students'},
            {'value': 'avg_terms_remaining', 'label': 'Average Terms to Graduation', 'description': 'Average terms remaining until graduation'},
            {'value': 'status_distribution', 'label': 'Student Status Distribution', 'description': 'Breakdown by incoming/established/outgoing'},
            {'value': 'team_count', 'label': 'Team Count', 'description': 'Total number of teams'},
            {'value': 'faculty_count', 'label': 'Faculty/Mentor Count', 'description': 'Total number of faculty and mentors'},
            {'value': 'project_count', 'label': 'Project Count', 'description': 'Total number of projects'},
            {'value': 'students_by_status_and_expertise', 'label': 'Students by Status & Expertise', 'description': 'Cross-tabulation of status and expertise area'}
        ],
        'dimensions': [
            {'value': 'university', 'label': 'University', 'applicableTo': ['student_count', 'avg_terms_remaining', 'team_count', 'faculty_count', 'project_count']},
            {'value': 'project', 'label': 'Project', 'applicableTo': ['team_count']},
            {'value': 'team', 'label': 'Team', 'applicableTo': ['student_count', 'avg_terms_remaining']},
            {'value': 'status', 'label': 'Student Status', 'applicableTo': ['student_count', 'avg_terms_remaining']},
            {'value': 'expertise_area', 'label': 'Expertise Area', 'applicableTo': ['student_count']},
            {'value': 'discipline', 'label': 'Team Discipline', 'applicableTo': ['team_count']},
            {'value': 'role', 'label': 'Faculty Role', 'applicableTo': ['faculty_count']},
            {'value': 'type', 'label': 'Project Type', 'applicableTo': ['project_count']}
        ],
        'filters': [
            {'value': 'university_id', 'label': 'Filter by University', 'type': 'select'},
            {'value': 'project_id', 'label': 'Filter by Project', 'type': 'select'},
            {'value': 'team_id', 'label': 'Filter by Team', 'type': 'select'},
            {'value': 'status', 'label': 'Filter by Status', 'type': 'select', 'options': ['incoming', 'established', 'outgoing']},
            {'value': 'expertise_area', 'label': 'Filter by Expertise', 'type': 'select'},
            {'value': 'role', 'label': 'Filter by Role', 'type': 'select'}
        ]
    })


# ============================================================================
# Research Dashboard & Factor Management API
# ============================================================================

@app.route('/research')
def research_dashboard():
    """Serve the Research Dashboard landing page with multiple analysis tools"""
    return send_from_directory('../frontend/templates', 'researcher_dashboard.html')


@app.route('/university-dashboard')
def university_dashboard():
    """Serve the University Dashboard page - hub for managing a specific university's program"""
    university = request.args.get('university')
    role = request.args.get('role', 'faculty')
    return render_template('university_dashboard.html', university=university, role=role)


# --- Risk Factor Management ---

@app.route('/api/research/factors', methods=['GET'])
def get_risk_factors():
    """Get all risk factors with their values"""
    try:
        from db_models import RiskFactor, FactorValue

        factors = RiskFactor.query.filter_by(active=True).all()
        result = []

        for factor in factors:
            factor_data = factor.to_dict()

            # Get factor values
            values = FactorValue.query.filter_by(factor_id=factor.id).order_by(FactorValue.sort_order).all()
            factor_data['values'] = [v.to_dict() for v in values]

            result.append(factor_data)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/research/factors', methods=['POST'])
def create_risk_factor():
    """Create a new risk factor"""
    try:
        from db_models import RiskFactor, FactorValue

        data = request.json

        # Create the factor
        factor = RiskFactor(
            factor_name=data['factor_name'],
            display_name=data['display_name'],
            description=data.get('description'),
            category=data['category'],
            confidence_level=data.get('confidence_level', 'exploratory'),
            research_notes=data.get('research_notes'),
            active=True
        )
        db.session.add(factor)
        db.session.flush()

        # Create factor values
        for value_data in data.get('values', []):
            factor_value = FactorValue(
                factor_id=factor.id,
                value_name=value_data['value_name'],
                display_name=value_data['display_name'],
                description=value_data.get('description'),
                energy_loss_contribution=value_data['energy_loss_contribution'],
                sort_order=value_data.get('sort_order', 0)
            )
            db.session.add(factor_value)

        db.session.commit()

        return jsonify({'success': True, 'factor_id': factor.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/research/factors/<int:factor_id>', methods=['PUT'])
def update_risk_factor(factor_id):
    """Update an existing risk factor"""
    try:
        from db_models import RiskFactor

        factor = RiskFactor.query.get_or_404(factor_id)
        data = request.json

        # Update fields
        if 'display_name' in data:
            factor.display_name = data['display_name']
        if 'description' in data:
            factor.description = data['description']
        if 'confidence_level' in data:
            factor.confidence_level = data['confidence_level']
        if 'research_notes' in data:
            factor.research_notes = data['research_notes']
        if 'active' in data:
            factor.active = data['active']

        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# --- Factor Model Management ---

@app.route('/api/research/models', methods=['GET'])
def get_factor_models():
    """Get all factor models"""
    try:
        from db_models import FactorModel, ModelFactor, RiskFactor

        models = FactorModel.query.all()
        result = []

        for model in models:
            model_data = model.to_dict()

            # Get model factors with weights
            model_factors = db.session.query(ModelFactor, RiskFactor).join(
                RiskFactor, ModelFactor.factor_id == RiskFactor.id
            ).filter(ModelFactor.model_id == model.id).all()

            model_data['factors'] = [
                {
                    'factor_id': rf.id,
                    'factor_name': rf.factor_name,
                    'display_name': rf.display_name,
                    'weight': mf.weight,
                    'enabled': mf.enabled
                }
                for mf, rf in model_factors
            ]

            result.append(model_data)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/research/models', methods=['POST'])
def create_factor_model():
    """Create a new factor model"""
    try:
        from db_models import FactorModel, ModelFactor

        data = request.json

        # Deactivate other models if this one is being set as active
        if data.get('is_active'):
            FactorModel.query.update({'is_active': False})

        # Create the model
        model = FactorModel(
            model_name=data['model_name'],
            display_name=data['display_name'],
            description=data.get('description'),
            is_active=data.get('is_active', False),
            is_baseline=data.get('is_baseline', False),
            hypothesis=data.get('hypothesis'),
            validation_status=data.get('validation_status', 'testing')
        )
        db.session.add(model)
        db.session.flush()

        # Add factors with weights
        for factor_data in data.get('factors', []):
            model_factor = ModelFactor(
                model_id=model.id,
                factor_id=factor_data['factor_id'],
                weight=factor_data.get('weight', 1.0),
                enabled=factor_data.get('enabled', True)
            )
            db.session.add(model_factor)

        db.session.commit()

        return jsonify({'success': True, 'model_id': model.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/research/models/<int:model_id>/activate', methods=['POST'])
def activate_model(model_id):
    """Set a model as the active model"""
    try:
        from db_models import FactorModel

        # Deactivate all models
        FactorModel.query.update({'is_active': False})

        # Activate the specified model
        model = FactorModel.query.get_or_404(model_id)
        model.is_active = True

        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/research/models/<int:model_id>/factors/<int:factor_id>/weight', methods=['PUT'])
def update_model_factor_weight(model_id, factor_id):
    """Update the weight of a factor in a specific model"""
    try:
        from db_models import ModelFactor

        data = request.json
        new_weight = data['weight']

        model_factor = ModelFactor.query.filter_by(
            model_id=model_id,
            factor_id=factor_id
        ).first_or_404()

        model_factor.weight = new_weight

        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# --- Energy Calculation API ---

@app.route('/api/research/energy/interface/<interface_id>', methods=['GET'])
def calculate_interface_energy(interface_id):
    """Calculate energy loss for a specific interface"""
    try:
        from energy_engine import EnergyCalculationEngine

        model_id = request.args.get('model_id', type=int)

        engine = EnergyCalculationEngine(model_id=model_id)
        result = engine.calculate_interface_energy_loss(interface_id, model_id)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/research/energy/network', methods=['GET'])
def calculate_network_energy():
    """Calculate energy loss for entire network or specific university"""
    try:
        from energy_engine import EnergyCalculationEngine

        university_id = request.args.get('university_id')
        model_id = request.args.get('model_id', type=int)

        engine = EnergyCalculationEngine(model_id=model_id)
        result = engine.calculate_network_energy(university_id, model_id)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/research/interface/<interface_id>/factors', methods=['POST'])
def assign_interface_factors(interface_id):
    """Assign factor values to an interface"""
    try:
        from energy_engine import EnergyCalculationEngine

        data = request.json
        factor_assignments = data.get('factors', [])

        engine = EnergyCalculationEngine()
        success = engine.assign_factor_values_to_interface(interface_id, factor_assignments)

        return jsonify({'success': success})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/api/research/migrate-legacy-interfaces', methods=['POST'])
def migrate_legacy_interfaces():
    """
    Migrate all legacy interfaces to use the factor system.
    This auto-assigns factors based on bond_type.
    """
    try:
        from db_models import InterfaceModel
        from energy_engine import EnergyCalculationEngine

        engine = EnergyCalculationEngine()

        # Get all interfaces without factor assignments
        interfaces = InterfaceModel.query.all()

        migrated = 0
        failed = 0

        for interface in interfaces:
            try:
                success = engine.auto_assign_factors_from_legacy(interface.id)
                if success:
                    migrated += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"Failed to migrate interface {interface.id}: {e}")
                failed += 1

        db.session.commit()

        return jsonify({
            'success': True,
            'migrated': migrated,
            'failed': failed,
            'total': len(interfaces)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# --- Model Comparison & Validation ---

@app.route('/api/research/compare-models', methods=['POST'])
def compare_models():
    """
    Compare multiple models by calculating energy loss across the same dataset.
    Used for model validation and selection.
    """
    try:
        from energy_engine import EnergyCalculationEngine

        data = request.json
        model_ids = data.get('model_ids', [])
        university_id = data.get('university_id')

        results = []

        for model_id in model_ids:
            engine = EnergyCalculationEngine(model_id=model_id)
            network_result = engine.calculate_network_energy(university_id, model_id)
            results.append(network_result)

        return jsonify({
            'success': True,
            'comparisons': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# Run Application
# ============================================================================

if __name__ == '__main__':
    print("Starting FRAMES Flask application...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)


@app.errorhandler(Exception)
def handle_exception(e):
    # Return JSON for unhandled exceptions on API routes
    tb = traceback.format_exc()
    # Only return JSON for API paths to avoid breaking normal pages
    if request.path.startswith('/api'):
        response = jsonify({'error': str(e), 'trace': tb})
        response.status_code = 500
        return response
    # Otherwise use default HTML error page
    return make_response(str(e), 500)
