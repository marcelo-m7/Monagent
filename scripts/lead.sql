-- schema
create schema if not exists monagent;

-- extensões úteis
create extension if not exists pgcrypto;

-- tabela principal
create table if not exists monagent.leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),

  email text not null,
  name text null,
  company text null,
  pain text null,

  source text null,       -- ex: "monynha.com"
  campaign text null,     -- utm_campaign
  medium text null,       -- utm_medium
  content text null,      -- utm_content
  term text null,         -- utm_term

  ip inet null,
  user_agent text null,

  status text not null default 'new',  -- new, contacted, qualified, discarded
  notes text null
);

-- evitar duplicado por email (ajusta conforme sua regra)
create unique index if not exists leads_unique_email
on monagent.leads (lower(email));

-- performance
create index if not exists leads_created_at_idx on monagent.leads (created_at desc);
create index if not exists leads_status_idx on monagent.leads (status);

-- rls

alter table monagent.leads enable row level security;

-- bloqueia geral por padrão (sem policies não passa nada)
revoke all on table monagent.leads from anon, authenticated;

-- opcional: permitir INSERT só via anon (se você for inserir do frontend direto)
-- mas como você quer produção e controle, eu recomendo inserir via Monagent (backend)
-- então não crie policy de insert para anon.

-- se você quiser permitir leitura apenas para usuários autenticados com role interna
-- aí você cria policies depois (ex: admin panel).
