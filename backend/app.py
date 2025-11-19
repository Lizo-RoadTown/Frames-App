
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from datetime import datetime
import os
import json

from models import SystemState, Team, Faculty, Project, Interface
from analytics import FramesAnalytics
from flask import make_response
import traceback
from database import db

app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
CORS(app)  # Enable CORS for frontend-backend communication

# Configure SQLAlchemy (simple SQLite for dev; switch URI via env for Postgres later)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Use absolute path for SQLite by default so the DB file is created next to backend code
default_sqlite = f"sqlite:///{os.path.join(BASE_DIR, 'frames.db')}"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', default_sqlite)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Global system state (in production, use database)
system_state = SystemState()

# Program Health Dashboard
@app.route('/dashboard')
def program_health_dashboard():
    """Serve the Program Health dashboard (dynamic network graph)"""
    university = request.args.get('university')
    return render_template('dashboard.html', university=university)

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
    """Serve the multi-university comparative dashboard"""
    return send_from_directory('../frontend/templates', 'comparative_dashboard.html')


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
            project_id=data.get('project_id'),
            expertise_area=data.get('expertise_area'),
            graduation_term=data.get('graduation_term'),
            terms_remaining=data.get('terms_remaining', 4)
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
        if 'project_id' in data:
            student.project_id = data['project_id']
        if 'expertise_area' in data:
            student.expertise_area = data['expertise_area']
        if 'graduation_term' in data:
            student.graduation_term = data['graduation_term']
        if 'terms_remaining' in data:
            student.terms_remaining = data['terms_remaining']
            student.status = student.calculate_status()

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
