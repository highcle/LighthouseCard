export interface User {
  id: string;
  username: string;
  email: string;
  created_at: string;
}

export interface Lighthouse {
  id: number;
  name: string;
  name_kana: string | null;
  region: string;
  prefecture: string;
  latitude: number;
  longitude: number;
  description: string | null;
  card_image_url: string | null;
  jcg_page_url: string | null;
  established_year: number | null;
  is_climbable: boolean;
  is_collected: boolean | null;
}

export interface LighthouseListResponse {
  items: Lighthouse[];
  total: number;
}

export interface Card {
  id: string;
  user_id: string;
  lighthouse_id: number;
  collected_at: string;
  note: string | null;
  lighthouse: Lighthouse | null;
}

export interface RegionStat {
  region: string;
  total: number;
  collected: number;
  rate: number;
}

export interface Stats {
  total_lighthouses: number;
  collected_count: number;
  achievement_rate: number;
  region_stats: RegionStat[];
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}
