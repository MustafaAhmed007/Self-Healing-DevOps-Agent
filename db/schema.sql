-- PostgreSQL durable model (reference schema)
CREATE TABLE IF NOT EXISTS repair_runs (
  id UUID PRIMARY KEY,
  repository_url TEXT NOT NULL,
  repository_commit TEXT,
  issue_number INTEGER NOT NULL,
  status TEXT NOT NULL,
  iteration INTEGER NOT NULL DEFAULT 0,
  cost_usd NUMERIC(12,6) NOT NULL DEFAULT 0,
  input_tokens BIGINT NOT NULL DEFAULT 0,
  output_tokens BIGINT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS repair_events (
  id BIGSERIAL PRIMARY KEY,
  run_id UUID NOT NULL REFERENCES repair_runs(id) ON DELETE CASCADE,
  node TEXT NOT NULL,
  event_type TEXT NOT NULL,
  payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS verification_results (
  id BIGSERIAL PRIMARY KEY,
  run_id UUID NOT NULL REFERENCES repair_runs(id) ON DELETE CASCADE,
  passed BOOLEAN NOT NULL,
  checks JSONB NOT NULL,
  failures JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS repair_events_run_idx ON repair_events(run_id, created_at);
