import type { NextConfig } from "next";

/** Proxies browser API requests to the CRM API without exposing database access. */
const nextConfig: NextConfig = {
  allowedDevOrigins: ["localhost:3000", "127.0.0.1:3000", "192.168.29.242:3000", "192.168.29.242"],
  async rewrites() {
    const apiUrl = process.env.CRM_API_URL ?? "http://localhost:8787";

    return [{ source: "/api/:path*", destination: `${apiUrl}/api/:path*` }];
  },
};

export default nextConfig;
