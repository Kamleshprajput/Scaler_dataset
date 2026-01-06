# Asana Dataset Generator

A comprehensive Python tool for generating realistic Asana work management simulation datasets. This tool creates a SQLite database containing synthetic data that mimics real-world Asana usage patterns, including users, teams, projects, tasks, comments, custom fields, automation rules, and more.

## Features

- **Realistic Data Generation**: Creates human-like project names, task descriptions, and comments
- **Industry-Specific Content**: Generates projects and workflows based on 15 different industries with accurate distribution ratios
- **Temporal Evolution**: Simulates data across multiple snapshots to show how work evolves over time
- **Complete Work Graph**: Includes all major Asana entities:
  - Organizations, Teams, Users
  - Projects, Sections, Tasks
  - Comments, Attachments, Tags
  - Custom Fields (workspace and project-level)
  - Automation Rules
  - API Traces and MCP Tool Calls
- **Data Validation**: Built-in temporal consistency validation
- **Rich Relationships**: Proper foreign key relationships and realistic data distributions

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

The required packages are:
- `faker` - For generating realistic names and emails
- `numpy` - For numerical operations
- `pandas` - For data manipulation
- `sqlalchemy` - For database operations
- `tqdm` - For progress bars (optional)

## Usage

### Basic Usage

Run the generator from the project root:

```bash
python run.py
```

This will:
1. Create a new SQLite database at `output/asana_simulation.sqlite`
2. Generate initial snapshot with users, teams, projects, tasks, and related data
3. Evolve through 7 additional snapshots showing temporal changes
4. Validate data consistency at each step

### Configuration

You can customize the generation by setting environment variables:

```bash
# Set number of users (default: 7500)
export NUM_USERS=10000

# Set number of snapshots (default: 8)
export NUM_SNAPSHOTS=10

# Set output database path (default: output/asana_simulation.sqlite)
export DB_PATH=output/my_custom_db.sqlite

# Run with custom settings
python run.py
```

Or modify `src/config.py` directly:

```python
NUM_USERS = 10000
NUM_SNAPSHOTS = 10
DB_PATH = "output/custom_path.sqlite"
```

## Project Structure

```
Scaler_asana_dataset/
├── src/
│   ├── config.py              # Configuration settings
│   ├── main.py                # Main pipeline orchestration
│   ├── generators/            # Data generation modules
│   │   ├── users.py           # User generation
│   │   ├── teams.py           # Team and membership generation
│   │   ├── projects.py        # Project generation (industry-specific)
│   │   ├── sections.py        # Section generation
│   │   ├── tasks.py           # Task generation
│   │   ├── comments.py        # Comment generation
│   │   ├── custom_fields.py   # Custom field generation
│   │   ├── tags.py            # Tag generation
│   │   ├── attachments.py    # Attachment generation
│   │   ├── automation_rules.py # Automation rule generation
│   │   ├── api_traces.py      # API trace generation
│   │   └── mcp_calls.py       # MCP tool call generation
│   ├── evolvers/              # Snapshot evolution modules
│   │   ├── task_evolver.py    # Task state evolution
│   │   └── automation_evolver.py # Automation artifact generation
│   └── validators/            # Data validation modules
│       └── temporal.py        # Temporal consistency validation
├── schema.sql                 # Database schema definition
├── run.py                     # Entry point script
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Output Database

The generator creates a SQLite database with the following tables:

### Core Entities
- **organizations**: Organization metadata
- **snapshots**: Snapshot metadata with timestamps
- **users**: User information (name, email, department, role)
- **teams**: Team definitions
- **team_memberships**: User-team relationships with roles

### Projects & Tasks
- **projects**: Projects with industry, type, status
- **sections**: Project sections (To Do, In Progress, Done, etc.)
- **tasks**: Tasks with assignments, due dates, completion status
- **comments**: User and system comments on tasks

### Customization
- **custom_field_definitions**: Custom field metadata
- **custom_field_settings**: Project-level field settings
- **custom_field_values**: Task field values

### Organization
- **tags**: Global tag definitions
- **task_tags**: Task-tag relationships
- **attachments**: File attachments on tasks

### Automation & Integration
- **automation_rules**: Automation rule definitions
- **api_call_traces**: API call logs
- **mcp_tool_calls**: Model Context Protocol tool calls

## Industry Distribution

The dataset follows industry distribution ratios based on real-world Asana customer data:

| Industry | Percentage |
|----------|------------|
| Technology | 26.7% |
| Nonprofit | 20.5% |
| Retail and consumer | 15.5% |
| Media and entertainment | 10.6% |
| Education | 3.7% |
| Finance | 3.7% |
| Food and Hospitality | 3.7% |
| Marketing and Creative service | 3.7% |
| Manufacturing | 3.1% |
| Healthcare | 1.9% |
| Telecommunications | 1.9% |
| Automotive | 1.2% |
| Energy | 1.2% |
| Government | 1.2% |
| Travel and transport | 1.2% |

Projects are generated with industry-specific names and workflows that reflect real use cases.

## Example Queries

After generating the database, you can query it using SQLite:

```bash
sqlite3 output/asana_simulation.sqlite
```

### Sample Queries

```sql
-- Count projects by industry
SELECT industry, COUNT(*) as count 
FROM projects 
WHERE industry IS NOT NULL 
GROUP BY industry 
ORDER BY count DESC;

-- Find incomplete tasks with due dates
SELECT t.name, t.due_date, p.name as project_name
FROM tasks t
JOIN projects p ON t.project_id = p.project_id AND t.snapshot_id = p.snapshot_id
WHERE t.completed = 0 AND t.due_date IS NOT NULL
LIMIT 10;

-- Count custom fields by type
SELECT field_type, COUNT(*) as count
FROM custom_field_definitions
GROUP BY field_type;

-- Find tasks with attachments
SELECT COUNT(DISTINCT task_id) as tasks_with_attachments
FROM attachments;

-- View automation rules
SELECT trigger_type, action_type, implemented_via
FROM automation_rules
LIMIT 10;
```

## Data Characteristics

### Default Generation (NUM_USERS=7500, NUM_SNAPSHOTS=8)

- **Users**: 7,500 across 5 departments (Engineering, Marketing, Operations, IT, Support)
- **Teams**: ~20-30 teams with varied roles (member, admin, viewer)
- **Projects**: ~90 projects across 15 industries
- **Tasks**: ~24,000 tasks with realistic names and descriptions
- **Sections**: ~240 project sections
- **Comments**: ~8,400 comments (user and system-generated)
- **Attachments**: ~8,800 file attachments
- **Custom Fields**: ~100 field definitions with ~3,150 values
- **Tags**: 25 global tags with ~19,500 task assignments
- **Automation Rules**: 25 automation rules
- **API Traces**: 310 API call traces
- **MCP Calls**: 30 MCP tool calls

### Data Quality Features

- **Temporal Consistency**: All `completed_at` dates are validated to be after `created_at`
- **Realistic Naming**: Human-like project and task names (not generic placeholders)
- **Industry Alignment**: Projects reflect industry-specific workflows and use cases
- **Relationship Integrity**: Proper foreign key relationships maintained
- **Snapshot Evolution**: Tasks evolve across snapshots showing realistic state changes

## Customization

### Adding New Project Types

Edit `src/generators/projects.py`:

```python
PROJECT_TYPES = {
    "product": 0.25,
    "marketing": 0.15,
    "your_new_type": 0.10,  # Add here
    # ...
}
```

### Adding Industry-Specific Projects

Edit `INDUSTRY_PROJECTS` in `src/generators/projects.py`:

```python
INDUSTRY_PROJECTS = {
    "Your Industry": {
        "project_type": [
            "Project Name 1",
            "Project Name 2",
        ],
    },
}
```

### Modifying Task Templates

Edit `TASK_TEMPLATES` and `TASK_ITEMS` in `src/generators/tasks.py` to add more task name patterns.

## Validation

The generator includes built-in validation:

- **Temporal Validation**: Ensures `completed_at >= created_at` for all completed tasks
- **Relationship Validation**: Foreign key constraints enforced
- **Data Completeness**: All tables populated with non-zero entries

Validation runs automatically after each snapshot evolution.

## Troubleshooting

### Database Already Exists Error

The script automatically removes existing databases. If you encounter issues, manually delete `output/asana_simulation.sqlite` before running.

### Import Errors

Ensure you're running from the project root directory and all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Unicode Encoding Errors (Windows)

The code uses ASCII-compatible characters to avoid Windows console encoding issues. If you see encoding errors, ensure your terminal supports UTF-8.

## License

This project is provided as-is for research and development purposes.

## References

The dataset generation is based on:
- Asana API documentation patterns
- Real-world industry distribution data
- Common Asana workflows and use cases
- Integration and automation patterns

## Contributing

To extend the generator:

1. Add new generators in `src/generators/`
2. Add evolvers in `src/evolvers/` for snapshot changes
3. Add validators in `src/validators/` for data quality checks
4. Update `src/main.py` to integrate new components

## Support

For issues or questions, please refer to the code comments and documentation within each module.

