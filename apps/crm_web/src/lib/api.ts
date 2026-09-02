import { invalidateCachedValue, readCachedValue, writeCachedValue } from "@/lib/cache";
import type { Communication, Company, CommunicationThread, Contact, FullResearchProfile, Opportunity, Reminder } from "@/lib/types";

const PAGE_SIZE = 500;

/** Error returned when the CRM API rejects a request. */
export class ApiError extends Error {}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });
  if (response.status === 204) return undefined as T;
  const body = await response.json() as T | { error?: string; details?: string };
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
