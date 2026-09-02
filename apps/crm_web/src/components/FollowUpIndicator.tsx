import styles from "@/components/crm.module.css";
import { dueState, formatDate } from "@/lib/formatters";

/** Highlights when a lead's next follow-up needs attention. */
export function FollowUpIndicator({ dueAt }: { dueAt: string | null | undefined }): React.JSX.Element {
  const state = dueState(dueAt);
  if (state === "none") return <span className={styles.muted}>Not scheduled</span>;
  const label = state === "overdue" ? "Overdue" : state === "today" ? "Due today" : "Upcoming";
  return <span className={`${styles.followUp} ${styles[state]}`}>{label} · {formatDate(dueAt)}</span>;
}
