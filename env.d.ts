/// <reference types="vite/client" />

interface ImportMetaEnv {
  // Define each custom variable here with 'readonly'
  readonly VITE_SUPABASE_URL: string
  readonly VITE_SUPABASE_ANON_KEY: string// Environment variables are always strings
  // more variables...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
