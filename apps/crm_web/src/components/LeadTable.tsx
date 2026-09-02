import styles from "@/components/crm.module.css";
import { FollowUpIndicator } from "@/components/FollowUpIndicator";
import { StatusBadge } from "@/components/StatusBadge";
import { formatDate } from "@/lib/formatters";
import type { LeadRecord } from "@/lib/types";

interface LeadTableProps {
  leads: LeadRecord[];
  selectedLeadId: number | null;
  onSelect: (lead: LeadRecord) => void;
}

/** Renders the primary operational lead table with internal vertical scroll. */
export function LeadTable({ leads, selectedLeadId, onSelect }: LeadTableProps): React.JSX.Element {
  if (!leads.length) {
    return (
      <div className={styles.emptyState}>
        <strong>No matching leads</strong>
        <span>Try a different search or add a lead to get started.</span>
      </div>
    );
  }

  return (
    <div className={styles.tableWrap}>
      <table className={styles.leadTable}>
        <thead>
          <tr>
            <th>Company</th>
            <th>Contact / Key Roles</th>
            <th>Location</th>
            <th>Stage</th>
            <th>Last contact</th>
            <th>Next follow-up</th>
            <th>Website</th>
          </tr>
        </thead>
        <tbody>
          {leads.map((lead) => {
            const contact = lead.contacts[0];
            const decisionMakerText = lead.opportunity.decision_maker_roles || lead.opportunity.recommended_first_contact;
            const latestThread = lead.threads[0];
            const reminder = lead.reminders.find((item) => item.status === "pending");
            const followUp = reminder?.due_at ?? latestThread?.next_follow_up_due_at;

            return (
              <tr
                key={lead.opportunity.id}
                className={selectedLeadId === lead.opportunity.id ? styles.selectedRow : ""}
                onClick={() => onSelect(lead)}
              >
                <td>
                  <strong>{lead.company.name}</strong>
                  <span className={styles.cellSubtext}>
                    {lead.opportunity.primary_opportunity || "No opportunity summary"}
                  </span>
                </td>
                <td>
                  {contact ? (
                    <>
                      <span>{contact.full_name || "Unnamed contact"}</span>
                      <span className={styles.cellSubtext}>{contact.job_title || ""}</span>
                    </>
                  ) : decisionMakerText ? (
                    <>
                      <span>{decisionMakerText.split(";")[0]}</span>
                      <span className={styles.cellSubtext} title={decisionMakerText}>
                        {decisionMakerText}
                      </span>
                    </>
                  ) : (
                    <span className={styles.muted}>No contact recorded</span>
                  )}
                </td>
                <td>{lead.company.headquarters || "—"}</td>
                <td>
                  <StatusBadge status={lead.opportunity.lead_status} />
                </td>
                <td>
                  {formatDate(
                    latestThread?.last_inbound_at ??
                      latestThread?.last_outbound_at ??
                      lead.opportunity.first_outreach_at
                  )}
                </td>
                <td>
                  <FollowUpIndicator dueAt={followUp} />
                </td>
                <td>
                  {lead.company.website_url ? (
                    <a
                      href={lead.company.website_url}
                      target="_blank"
                      rel="noreferrer"
                      onClick={(event) => event.stopPropagation()}
                    >
                      Visit ↗
                    </a>
                  ) : (
                    "—"
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
