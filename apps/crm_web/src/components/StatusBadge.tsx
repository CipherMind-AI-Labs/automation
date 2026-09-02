import styles from "@/components/crm.module.css";

/** Displays a lead stage with a consistent visual treatment. */
export function StatusBadge({ status }: { status: string | null }): React.JSX.Element {
  const value = status || "New";
  const tone = value.toLowerCase().replaceAll(" ", "-");
  return <span className={`${styles.statusBadge} ${styles[`status${tone}`] ?? ""}`}>{value}</span>;
}
