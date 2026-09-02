# Lead CRM Web

Internal Next.js interface for the CRM API. It uses the existing API only; the browser never connects to Cloudflare D1.

## Run locally

1. Copy `.env.example` to `.env.local` and set `CRM_API_URL` to the CRM API Worker, or start the API at `http://localhost:8787`.
2. Run `npm install`.
3. Run `npm run dev`.

The app proxies `/api/*` through Next.js, so the Worker does not need browser CORS configuration. Companies and contacts are cached in local storage for five minutes and are invalidated after a create or update.
