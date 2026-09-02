import { invalidateCachedValue, readCachedValue, writeCachedValue } from "@/lib/cache";
import type { Communication, Company, CommunicationThread, Contact, FullResearchProfile, Opportunity, Reminder } from "@/lib/types";

const PAGE_SIZE = 500;
const TOKEN_KEY = "crm_access_token";

let unauthorizedHandler: (() => void) | null = null;

export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem(TOKEN_KEY, token);
  }
}

export function clearStoredToken(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem(TOKEN_KEY);
  }
}

export function setUnauthorizedHandler(handler: () => void): void {
  unauthorizedHandler = handler;
}

/** Error returned when the CRM API rejects a request. */
export class ApiError extends Error {}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const token = getStoredToken();
  const authHeaders: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {};

  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders,
      ...options?.headers,
    },
  });

  if (response.status === 401) {
    clearStoredToken();
    if (unauthorizedHandler) {
      unauthorizedHandler();
    }
    throw new ApiError("Session expired or invalid access token.");
  }

  if (response.status === 204) return undefined as T;
  const body = (await response.json()) as T | { error?: string; details?: string };
  if (!response.ok) {
    const error = body as { error?: string; details?: string };
    throw new ApiError(error.details ?? error.error ?? "The CRM API request failed.");
  }
  return body as T;
}

async function getReferenceData<T>(key: string, path: string): Promise<T> {
  const cached = readCachedValue<T>(key);
  if (cached) return cached;
  const result = await request<T>(path);
  writeCachedValue(key, result);
  return result;
}

const jsonRequest = <T>(method: string, body: T): RequestInit => ({ method, body: JSON.stringify(body) });

export const crmApi = {
  verifyToken: async (token?: string): Promise<boolean> => {
    const targetToken = token ?? getStoredToken();
    if (!targetToken) return false;
    try {
      await request<{ status: string; authenticated: boolean }>("/api/auth/verify", {
        headers: { Authorization: `Bearer ${targetToken}` },
      });
      return true;
    } catch {
      return false;
    }
  },
  listCompanies: () => getReferenceData<Company[]>("companies", `/api/companies?limit=${PAGE_SIZE}`),
  listContacts: () => getReferenceData<Contact[]>("contacts", `/api/contacts?limit=${PAGE_SIZE}`),
  listOpportunities: () => request<Opportunity[]>(`/api/opportunities?limit=${PAGE_SIZE}`),
  listThreads: () => request<CommunicationThread[]>(`/api/communication-threads?limit=${PAGE_SIZE}`),
  listReminders: () => request<Reminder[]>(`/api/reminders?limit=${PAGE_SIZE}`),
  getThread: (id: number) => request<CommunicationThread>(`/api/communication-threads/${id}`),
  getResearchProfile: (id: number) => request<FullResearchProfile>(`/api/research-profiles/${id}`),
  createResearchProfile: (data: Partial<FullResearchProfile>) => request<FullResearchProfile>("/api/research-profiles", jsonRequest("POST", data)),
  updateResearchProfile: (id: number, data: Partial<FullResearchProfile>) => request<FullResearchProfile>(`/api/research-profiles/${id}`, jsonRequest("PUT", data)),
  createCompany: async (data: Partial<Company>) => {
    const result = await request<Company>("/api/companies", jsonRequest("POST", data));
    invalidateCachedValue("companies");
    return result;
  },
  updateCompany: async (id: number, data: Partial<Company>) => {
    const result = await request<Company>(`/api/companies/${id}`, jsonRequest("PUT", data));
    invalidateCachedValue("companies");
    return result;
  },
  createContact: async (data: Partial<Contact>) => {
    const result = await request<Contact>("/api/contacts", jsonRequest("POST", data));
    invalidateCachedValue("contacts");
    return result;
  },
  updateContact: async (id: number, data: Partial<Contact>) => {
    const result = await request<Contact>(`/api/contacts/${id}`, jsonRequest("PUT", data));
    invalidateCachedValue("contacts");
    return result;
  },
  createOpportunity: (data: Partial<Opportunity>) => request<Opportunity>("/api/opportunities", jsonRequest("POST", data)),
  updateOpportunity: (id: number, data: Partial<Opportunity>) => request<Opportunity>(`/api/opportunities/${id}`, jsonRequest("PUT", data)),
  createReminder: (data: Partial<Reminder>) => request<Reminder>("/api/reminders", jsonRequest("POST", data)),
  updateReminder: (id: number, data: Partial<Reminder>) => request<Reminder>(`/api/reminders/${id}`, jsonRequest("PUT", data)),
  createThread: (data: Partial<CommunicationThread>) => request<CommunicationThread>("/api/communication-threads", jsonRequest("POST", data)),
  createCommunication: (data: Partial<Communication>) => request<Communication>("/api/communications", jsonRequest("POST", data)),
};

