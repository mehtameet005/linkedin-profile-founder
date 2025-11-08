// Core Types
export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
}

export interface Job {
  id: string;
  user_id: string;
  website_url: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
  icp_id?: string;
}

export interface ICP {
  id: string;
  job_id: string;
  company_name: string;
  industry: string;
  sub_industries: string[];
  firmographics: {
    employee_range?: string;
    revenue_band?: string;
  };
  value_props: string[];
  pain_points: string[];
  trigger_events: string[];
  tech_stack: {
    [key: string]: string | string[];
  };
  embedding_id?: string;
  created_at: string;
}

export interface Persona {
  id: string;
  icp_id: string;
  persona_name: string;
  titles: string[];
  goals: string[];
  pains: string[];
  kpis: string[];
  keywords: string[];
  created_at: string;
  updated_at: string;
}

export interface Candidate {
  id: string;
  job_id: string;
  linkedin_url: string;
  inferred_name?: string;
  inferred_title?: string;
  inferred_location?: string;
  inferred_company?: string;
  result_snippet: string;
  scores: {
    semantic: number;
    role: number;
    industry: number;
    geo: number;
    final: number;
  };
  explainability: {
    keywords_matched: string[];
    feature_contributions: {
      semantic: number;
      role: number;
      industry: number;
      geo: number;
    };
  };
  created_at: string;
}

export interface ScoreExplanation {
  semantic: number;
  role: number;
  industry: number;
  geo: number;
  keywords_matched: string[];
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// Filter Types
export interface CandidateFilters {
  min_score?: number;
  max_score?: number;
  location?: string;
  company?: string;
  title_pattern?: string;
  persona_id?: string;
}
