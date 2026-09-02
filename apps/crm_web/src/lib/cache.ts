const CACHE_PREFIX = "crm-web:";
const CACHE_TTL_MS = 5 * 60 * 1000;

interface CachedValue<T> {
  savedAt: number;
  value: T;
}

/** Reads a still-fresh reference-data value from browser storage. */
export function readCachedValue<T>(key: string): T | null {
  if (typeof window === "undefined") return null;
  const raw = window.localStorage.getItem(`${CACHE_PREFIX}${key}`);
  if (!raw) return null;
  try {
    const cached = JSON.parse(raw) as CachedValue<T>;
    return Date.now() - cached.savedAt < CACHE_TTL_MS ? cached.value : null;
  } catch {
    return null;
  }
}

/** Stores reference data with a bounded freshness period. */
export function writeCachedValue<T>(key: string, value: T): void {
  if (typeof window !== "undefined") {
    window.localStorage.setItem(`${CACHE_PREFIX}${key}`, JSON.stringify({ savedAt: Date.now(), value }));
  }
}

/** Invalidates reference data after an explicit mutation. */
export function invalidateCachedValue(key: string): void {
  if (typeof window !== "undefined") window.localStorage.removeItem(`${CACHE_PREFIX}${key}`);
}
