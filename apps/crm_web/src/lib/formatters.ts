/** Formats an API date value for compact operational display. */
export function formatDate(value: string | null | undefined, includeTime = false): string {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("en", {
    day: "numeric", month: "short", year: "numeric", ...(includeTime ? { hour: "numeric", minute: "2-digit" } : {}),
  }).format(date);
}

/** Returns a human-readable due-state label without changing CRM records. */
export function dueState(value: string | null | undefined): "overdue" | "today" | "upcoming" | "none" {
  if (!value) return "none";
  const due = new Date(value);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const dueDate = new Date(due);
  dueDate.setHours(0, 0, 0, 0);
  if (dueDate < today) return "overdue";
  if (dueDate.getTime() === today.getTime()) return "today";
  return "upcoming";
}

/** Converts API timestamps to input-compatible local datetime values. */
export function toDateTimeInput(value: string | null | undefined): string {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";
  const offset = date.getTimezoneOffset() * 60000;
  return new Date(date.getTime() - offset).toISOString().slice(0, 16);
}
