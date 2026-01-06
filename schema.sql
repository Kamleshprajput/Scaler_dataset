-- =========================
-- ORGANIZATION & SNAPSHOTS
-- =========================

CREATE TABLE organizations (
  organization_id TEXT PRIMARY KEY,
  name TEXT,
  domain TEXT,
  created_at TIMESTAMP
);

CREATE TABLE snapshots (
  snapshot_id TEXT PRIMARY KEY,
  organization_id TEXT,
  snapshot_time TIMESTAMP,
  description TEXT,
  created_at TIMESTAMP
);

-- =========================
-- USERS & TEAMS
-- =========================

CREATE TABLE users (
  user_id TEXT,
  snapshot_id TEXT,
  name TEXT,
  email TEXT,
  department TEXT,
  role TEXT,
  is_active BOOLEAN,
  PRIMARY KEY (user_id, snapshot_id)
);

CREATE TABLE teams (
  team_id TEXT,
  snapshot_id TEXT,
  name TEXT,
  department TEXT,
  PRIMARY KEY (team_id, snapshot_id)
);

CREATE TABLE team_memberships (
  team_id TEXT,
  user_id TEXT,
  snapshot_id TEXT,
  role TEXT,
  PRIMARY KEY (team_id, user_id, snapshot_id)
);

-- =========================
-- PROJECTS & SECTIONS
-- =========================

CREATE TABLE projects (
  project_id TEXT,
  snapshot_id TEXT,
  team_id TEXT,
  name TEXT,
  project_type TEXT,
  industry TEXT,
  created_via TEXT,
  status TEXT,
  created_at TIMESTAMP,
  PRIMARY KEY (project_id, snapshot_id)
);

CREATE TABLE sections (
  section_id TEXT,
  project_id TEXT,
  snapshot_id TEXT,
  name TEXT,
  position INTEGER,
  PRIMARY KEY (section_id, snapshot_id)
);

-- =========================
-- TASKS & COMMENTS
-- =========================

CREATE TABLE tasks (
  task_id TEXT,
  snapshot_id TEXT,
  project_id TEXT,
  section_id TEXT,
  parent_task_id TEXT,
  name TEXT,
  description TEXT,
  assignee_id TEXT,
  created_via TEXT,
  external_source TEXT,
  due_date DATE,
  completed BOOLEAN,
  created_at TIMESTAMP,
  completed_at TIMESTAMP,
  PRIMARY KEY (task_id, snapshot_id)
);

CREATE TABLE comments (
  comment_id TEXT,
  snapshot_id TEXT,
  task_id TEXT,
  author_id TEXT,
  author_type TEXT,
  body TEXT,
  created_at TIMESTAMP,
  PRIMARY KEY (comment_id, snapshot_id)
);

-- =========================
-- CUSTOM FIELDS
-- =========================

CREATE TABLE custom_field_definitions (
  field_id TEXT PRIMARY KEY,
  name TEXT,
  field_type TEXT,
  scope TEXT,
  is_active BOOLEAN
);

CREATE TABLE custom_field_settings (
  field_id TEXT,
  project_id TEXT,
  snapshot_id TEXT,
  enabled BOOLEAN,
  PRIMARY KEY (field_id, project_id, snapshot_id)
);

CREATE TABLE custom_field_values (
  task_id TEXT,
  field_id TEXT,
  snapshot_id TEXT,
  value TEXT,
  enabled BOOLEAN,
  PRIMARY KEY (task_id, field_id, snapshot_id)
);

-- =========================
-- TAGS & ATTACHMENTS
-- =========================

CREATE TABLE tags (
  tag_id TEXT PRIMARY KEY,
  name TEXT
);

CREATE TABLE task_tags (
  task_id TEXT,
  tag_id TEXT,
  snapshot_id TEXT,
  PRIMARY KEY (task_id, tag_id, snapshot_id)
);

CREATE TABLE attachments (
  attachment_id TEXT PRIMARY KEY,
  task_id TEXT,
  snapshot_id TEXT,
  source TEXT,
  url TEXT,
  created_at TIMESTAMP
);

-- =========================
-- AUTOMATION / API / MCP
-- =========================

CREATE TABLE automation_rules (
  rule_id TEXT PRIMARY KEY,
  trigger_type TEXT,
  trigger_payload TEXT,
  action_type TEXT,
  action_payload TEXT,
  implemented_via TEXT
);

CREATE TABLE api_call_traces (
  trace_id TEXT PRIMARY KEY,
  snapshot_id TEXT,
  actor_type TEXT,
  method TEXT,
  endpoint TEXT,
  request_payload TEXT,
  response_payload TEXT,
  success BOOLEAN,
  latency_ms REAL
);

CREATE TABLE mcp_tool_calls (
  call_id TEXT PRIMARY KEY,
  snapshot_id TEXT,
  natural_language_query TEXT,
  tool_name TEXT,
  tool_arguments TEXT,
  tool_response TEXT
);
