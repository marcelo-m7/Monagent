create schema if not exists app;

create extension if not exists pgcrypto;
create extension if not exists citext;

do $$ begin
  create type app.lead_stage as enum ('new','contacted','qualified','won','lost','spam');
exception
  when duplicate_object then null;
end $$;

create table if not exists app.leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  -- identidade (SEM UNIQUE)
  email citext not null,
  name text null,
  company text null,

  -- qualificação
  revenue integer null check (revenue >= 0),
  pain text null,

  -- tracking (UTM)
  utm_source text null,
  utm_medium text null,
  utm_campaign text null,
  utm_content text null,
  utm_term text null,

  -- meta
  landing_path text null,
  referrer text null,
  ip inet null,
  user_agent text null,
  locale text null,
  timezone text null,

  -- consentimento
  marketing_opt_in boolean not null default false,
  terms_accepted boolean not null default false,
  consent_at timestamptz null,

  -- funil
  stage app.lead_stage not null default 'new',
  notes text null,

  -- payload flexível
  json_data jsonb null,

  -- idempotência opcional (ÚNICO quando existir)
  dedupe_key text null
);

create or replace function app.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists trg_leads_updated_at on app.leads;
create trigger trg_leads_updated_at
before update on app.leads
for each row execute function app.set_updated_at();

-- índices úteis
create index if not exists leads_created_at_idx on app.leads (created_at desc);
create index if not exists leads_email_idx on app.leads (email);
create index if not exists leads_stage_idx on app.leads (stage);
create index if not exists leads_campaign_idx on app.leads (utm_campaign);

-- busca em json
create index if not exists leads_json_gin_idx on app.leads using gin (json_data);

-- dedupe opcional: único apenas quando preenchido
create unique index if not exists leads_dedupe_key_unique
on app.leads (dedupe_key)
where dedupe_key is not null;

alter table app.leads enable row level security;
revoke all on table app.leads from anon, authenticated;

-- Simplifyed views for the API (optional)
create or replace view app.leads_view as 
select 
  id,
  created_at,
  updated_at,
  email,
  name,
  company,
  revenue,
  pain,
  stage,
  json_data
from app.leads;
