import styles from "@/components/crm.module.css";
import type { LeadRecord } from "@/lib/types";
import { dueState } from "@/lib/formatters";

/** Presents a concise operational count of the current lead workload. */
export function DashboardOverview({ leads }: { leads: LeadRecord[] }): React.JSX.Element {
  const stageCounts = leads.reduce<Record<string, number>>((counts, lead) => {
    const stage = lead.opportunity.lead_status || "New";
    counts[stage] = (counts[stage] || 0) + 1;
    return counts;
  }, {});
  const attention = leads.filter((lead) => {
    const due = lead.reminders.find((reminder) => reminder.status === "pending")?.due_at ?? lead.threads.find((thread) => thread.next_follow_up_due_at)?.next_follow_up_due_at;
    return dueState(due) === "overdue" || dueState(due) === "today";
  }).length;

  return <section className={styles.overview} aria-label="Lead overview"><div className={styles.overviewTotal}><span>All leads</span><strong>{leads.length}</strong></div>{Object.entries(stageCounts).map(([stage, count]) => <div className={styles.overviewItem} key={stage}><span>{stage}</span><strong>{count}</strong></div>)}<div className={`${styles.overviewItem} ${styles.attentionCard}`}><span>Need attention</span><strong>{attention}</strong></div></section>;
}
