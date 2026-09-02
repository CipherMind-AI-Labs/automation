"use client";

import { useEffect, useState } from "react";
import styles from "@/components/crm.module.css";
import { FollowUpIndicator } from "@/components/FollowUpIndicator";
import { StatusBadge } from "@/components/StatusBadge";
import { crmApi } from "@/lib/api";
import { formatDate } from "@/lib/formatters";
import type { Communication, LeadRecord } from "@/lib/types";

interface LeadDetailPanelProps {
  lead: LeadRecord | null;
  onClose: () => void;
  onEdit: () => void;
  onRefresh: () => Promise<void>;
}

/** Shows complete available lead information, full research intelligence dataset, and communication logging. */
export function LeadDetailPanel({
  lead,
  onClose,
  onEdit,
  onRefresh,
}: LeadDetailPanelProps): React.JSX.Element | null {
  const [messages, setMessages] = useState<Communication[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showCommForm, setShowCommForm] = useState(false);
  const [showAnalysisModal, setShowAnalysisModal] = useState(false);

  // New communication form state
  const [commChannel, setCommChannel] = useState("email");
  const [commDirection, setCommDirection] = useState("outbound");
  const [commSubject, setCommSubject] = useState("");
  const [commBody, setCommBody] = useState("");
  const [isSubmittingComm, setIsSubmittingComm] = useState(false);

  const fetchMessages = () => {
    if (!lead) return;
    setIsLoading(true);
    Promise.all(lead.threads.map((thread) => crmApi.getThread(thread.id)))
      .then((threads) => {
        setMessages(
          threads
            .flatMap((thread) => thread.messages ?? [])
            .sort((a, b) =>
              (b.received_at ?? b.sent_at ?? b.created_at ?? "").localeCompare(
                a.received_at ?? a.sent_at ?? a.created_at ?? ""
              )
            )
        );
      })
      .catch(() => setMessages([]))
      .finally(() => setIsLoading(false));
  };

  useEffect(() => {
    fetchMessages();
    setShowCommForm(false);
  }, [lead]);

  if (!lead) return null;

  const contact = lead.contacts[0];
  const reminder = lead.reminders.find((item) => item.status === "pending");
  const threadFollowUp = lead.threads.find((thread) => thread.next_follow_up_due_at)?.next_follow_up_due_at;
  const rp = lead.researchProfile;
  const da = rp?.digital_assessment;
  const pa = rp?.product_assessment;

  const handleAddCommunication = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commSubject.trim()) return;

    setIsSubmittingComm(true);
    try {
      let threadId: number;
      if (lead.threads.length > 0) {
        threadId = lead.threads[0].id;
      } else {
        const newThread = await crmApi.createThread({
          company_id: lead.company.id,
          opportunity_id: lead.opportunity.id,
          channel: commChannel,
          subject: commSubject,
        });
        threadId = newThread.id;
      }

      await crmApi.createCommunication({
        thread_id: threadId,
        contact_id: contact?.id ?? null,
        channel: commChannel,
        direction: commDirection,
        subject: commSubject,
        body_text: commBody || null,
        message_status: commDirection === "outbound" ? "sent" : "received",
        sent_at: commDirection === "outbound" ? new Date().toISOString() : null,
        received_at: commDirection === "inbound" ? new Date().toISOString() : null,
      });

      setCommSubject("");
      setCommBody("");
      setShowCommForm(false);
      await onRefresh();
      fetchMessages();
    } catch {
      alert("Failed to log communication record.");
    } finally {
      setIsSubmittingComm(false);
    }
  };

  const fields = [
    ["Opportunity", lead.opportunity.primary_opportunity],
    ["Priority", lead.opportunity.priority],
    ["Deal size", lead.opportunity.estimated_initial_deal_size],
    ["Next action", lead.opportunity.next_action],
    ["Industry", lead.company.industry],
    ["Coverage", lead.company.geographic_coverage],
    ["Employees", lead.company.employee_range],
    ["Ownership", lead.company.ownership],
    ["Contact email", contact?.email],
    ["Contact phone", contact?.phone],
  ];

  return (
    <>
      <aside className={styles.detailPanel}>
        <div className={styles.panelHeader}>
          <div>
            <p className={styles.eyebrow}>Lead Detail</p>
            <h2>{lead.company.name}</h2>
            <StatusBadge status={lead.opportunity.lead_status} />
          </div>
          <button className={styles.iconButton} onClick={onClose} aria-label="Close lead details">
            ×
          </button>
        </div>

        <div className={styles.detailContent}>
          <div className={styles.followUpCard}>
            <span>Next follow-up</span>
            <FollowUpIndicator dueAt={reminder?.due_at ?? threadFollowUp} />
            <p>{reminder?.notes || lead.opportunity.next_action || "No action recorded."}</p>
          </div>

          <div style={{ display: "flex", gap: "8px" }}>
            <button className={styles.primaryButton} onClick={onEdit} style={{ flex: 1 }}>
              Edit lead
            </button>
            <button
              className={styles.outlineButton}
              onClick={() => setShowAnalysisModal(true)}
              title="View complete research profile dataset"
            >
              🔍 Deep Dive Analysis
            </button>
          </div>

          <section>
            <h3>Contact / Key Roles</h3>
            {contact ? (
              <p>
                <strong>{contact.full_name}</strong>
                <br />
                {contact.job_title || "No role recorded"}
                {contact.is_decision_maker ? " · Decision Maker" : ""}
                {contact.email && (
                  <>
                    <br />
                    <span className={styles.muted}>{contact.email}</span>
                  </>
                )}
              </p>
            ) : rp?.owners_summary || lead.opportunity.decision_maker_roles || lead.opportunity.recommended_first_contact ? (
              <p>
                <strong>Owners / Decision Maker Roles:</strong>
                <br />
                {rp?.owners_summary || lead.opportunity.decision_maker_roles}
                {lead.opportunity.recommended_first_contact && (
                  <>
                    <br />
                    <span className={styles.muted}>
                      First Contact Approach: {lead.opportunity.recommended_first_contact}
                    </span>
                  </>
                )}
              </p>
            ) : (
              <p className={styles.muted}>No contact recorded.</p>
            )}
          </section>

          <section>
            <h3>Overview</h3>
            <dl className={styles.detailsList}>
              {fields
                .filter(([, value]) => value)
                .map(([label, value]) => (
                  <div key={label}>
                    <dt>{label}</dt>
                    <dd>{value}</dd>
                  </div>
                ))}
            </dl>
          </section>

          {lead.opportunity.follow_up_notes && (
            <section>
              <h3>Notes</h3>
              <p className={styles.preserve}>{lead.opportunity.follow_up_notes}</p>
            </section>
          )}

          <section>
            <div className={styles.sectionHeader}>
              <h3>Communication History</h3>
              <button
                className={styles.outlineButton}
                onClick={() => setShowCommForm(!showCommForm)}
                style={{ padding: "4px 8px", fontSize: "11px" }}
              >
                {showCommForm ? "Cancel" : "+ Log Communication"}
              </button>
            </div>

            {showCommForm && (
              <form className={styles.commForm} onSubmit={handleAddCommunication}>
                <div className={styles.commFormGrid}>
                  <label>
                    Channel
                    <select value={commChannel} onChange={(e) => setCommChannel(e.target.value)}>
                      <option value="email">Email</option>
                      <option value="phone">Phone Call</option>
                      <option value="meeting">Meeting</option>
                      <option value="linkedin">LinkedIn Message</option>
                    </select>
                  </label>
                  <label>
                    Direction
                    <select value={commDirection} onChange={(e) => setCommDirection(e.target.value)}>
                      <option value="outbound">Sent (Outbound)</option>
                      <option value="inbound">Received (Inbound)</option>
                    </select>
                  </label>
                </div>
                <label>
                  Subject / Summary
                  <input
                    required
                    placeholder="e.g. Sent intro deck & pitch"
                    value={commSubject}
                    onChange={(e) => setCommSubject(e.target.value)}
                  />
                </label>
                <label>
                  Details / Content
                  <textarea
                    rows={3}
                    placeholder="Key discussion points or response notes..."
                    value={commBody}
                    onChange={(e) => setCommBody(e.target.value)}
                  />
                </label>
                <button className={styles.primaryButton} disabled={isSubmittingComm} style={{ padding: "6px 12px" }}>
                  {isSubmittingComm ? "Saving..." : "Save Communication"}
                </button>
              </form>
            )}

            {isLoading ? (
              <p className={styles.muted}>Loading communications…</p>
            ) : messages.length ? (
              <div className={styles.timeline}>
                {messages.map((message) => (
                  <article key={message.id} className={styles.message}>
                    <div>
                      <span className={message.direction === "inbound" ? styles.inbound : styles.outbound}>
                        {message.direction === "inbound" ? "Received" : "Sent"} · {message.channel}
                      </span>
                      <time>
                        {formatDate(message.received_at ?? message.sent_at ?? message.created_at, true)}
                      </time>
                    </div>
                    <strong>{message.subject || `${message.channel} communication`}</strong>
                    {message.body_text && <p className={styles.preserve}>{message.body_text}</p>}
                  </article>
                ))}
              </div>
            ) : (
              <p className={styles.muted}>No communications recorded yet.</p>
            )}
          </section>
        </div>
      </aside>

      {/* Deep Dive Analysis Modal: Displays complete research profile dataset */}
      {showAnalysisModal && (
        <div className={styles.modalBackdrop} role="presentation">
          <div className={styles.analysisModal}>
            <div className={styles.panelHeader}>
              <div>
                <p className={styles.eyebrow}>Deep Dive Analysis</p>
                <h2>{lead.company.name} — Full Research Intelligence Dataset</h2>
              </div>
              <button
                className={styles.iconButton}
                onClick={() => setShowAnalysisModal(false)}
                aria-label="Close modal"
              >
                ×
              </button>
            </div>

            <div className={styles.analysisContent}>
              {/* Section 1: Company Intelligence */}
              <div className={styles.analysisSection}>
                <h4>🏢 Company Intelligence</h4>
                <div className={styles.analysisGrid}>
                  <div className={styles.analysisItem} style={{ gridColumn: "1 / -1" }}>
                    <label>Company Overview</label>
                    <span>{rp?.company_overview || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Ownership</label>
                    <span>{lead.company.ownership || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Owners / Leadership</label>
                    <span>{rp?.owners_summary || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Offices Summary</label>
                    <span>{lead.company.offices_summary || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Geographic Coverage</label>
                    <span>{lead.company.geographic_coverage || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Core Services</label>
                    <span>{rp?.core_services || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Primary Customers</label>
                    <span>{rp?.primary_customers || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Business Model</label>
                    <span>{rp?.business_model || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Competitive Position</label>
                    <span>{rp?.competitive_position || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Showroom</label>
                    <span>{rp?.showroom_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Growth Indicators</label>
                    <span>{rp?.growth_indicators || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Research Confidence</label>
                    <span>{rp?.research_confidence || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Research Date</label>
                    <span>{rp?.researched_on || "—"}</span>
                  </div>
                  <div className={styles.analysisItem} style={{ gridColumn: "1 / -1" }}>
                    <label>Analyst Notes</label>
                    <span>{rp?.analyst_notes || "—"}</span>
                  </div>
                </div>
              </div>

              {/* Section 2: Digital Intelligence */}
              <div className={styles.analysisSection}>
                <h4>💻 Digital Intelligence</h4>
                <div className={styles.analysisGrid}>
                  <div className={styles.analysisItem}>
                    <label>Website Quality</label>
                    <span>{da?.website_quality_score != null ? `${da.website_quality_score}/10` : "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Mobile Friendly</label>
                    <span>{da?.mobile_friendly || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Blog Status</label>
                    <span>{da?.blog_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Product Search</label>
                    <span>{da?.product_search_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Product Filters</label>
                    <span>{da?.product_filters_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Product Catalog</label>
                    <span>{da?.product_catalog_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Ecommerce Status</label>
                    <span>{da?.ecommerce_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Quote Request Method</label>
                    <span>{da?.quote_request_method || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Public Pricing</label>
                    <span>{da?.public_pricing_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>CMS</label>
                    <span>{da?.cms || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>PIM Detection</label>
                    <span>{da?.pim_detection || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>DAM Detection</label>
                    <span>{da?.dam_detection || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Digital Maturity</label>
                    <span>{da?.digital_maturity || "—"}</span>
                  </div>
                  <div className={styles.analysisItem} style={{ gridColumn: "1 / -1" }}>
                    <label>Technology Clues</label>
                    <span>{da?.technology_clues || "—"}</span>
                  </div>
                </div>
              </div>

              {/* Section 3: Product Information Intelligence */}
              <div className={styles.analysisSection}>
                <h4>📦 Product Information Intelligence</h4>
                <div className={styles.analysisGrid}>
                  <div className={styles.analysisItem}>
                    <label>Manufacturers Represented</label>
                    <span>{pa?.manufacturers_represented || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Estimated Brands</label>
                    <span>{pa?.estimated_brands || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Product Pages</label>
                    <span>{pa?.product_pages || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Product Search Experience</label>
                    <span>{pa?.product_search_experience || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Product Filters Quality</label>
                    <span>{pa?.product_filters_quality || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Images Status</label>
                    <span>{pa?.images_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Product Descriptions</label>
                    <span>{pa?.product_descriptions_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Specifications Status</label>
                    <span>{pa?.specifications_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>CAD / Revit Status</label>
                    <span>{pa?.cad_revit_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Brochures Status</label>
                    <span>{pa?.brochures_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Sustainability & Warranty Docs</label>
                    <span>{pa?.sustainability_warranty_docs_status || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Attributes Completeness Score</label>
                    <span>{pa?.product_attributes_completeness_score != null ? `${pa.product_attributes_completeness_score}/10` : "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Data Ownership</label>
                    <span>{pa?.data_ownership || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Product Information Quality Score</label>
                    <span>{pa?.product_information_quality_score != null ? `${pa.product_information_quality_score}/10` : "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Estimated Catalog Size</label>
                    <span>{pa?.estimated_catalog_size || "—"}</span>
                  </div>
                </div>
              </div>

              {/* Section 4: Commercial & Opportunity Intelligence */}
              <div className={styles.analysisSection}>
                <h4>🎯 Commercial & Opportunity Intelligence</h4>
                <div className={styles.analysisGrid}>
                  <div className={styles.analysisItem}>
                    <label>Primary Opportunity</label>
                    <span>{lead.opportunity.primary_opportunity || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Recommended Service</label>
                    <span>{lead.opportunity.recommended_service || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Expected Business Value</label>
                    <span>{lead.opportunity.expected_business_value || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Estimated Initial Deal Size</label>
                    <span>{lead.opportunity.estimated_initial_deal_size || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Opportunity Score</label>
                    <span>{lead.opportunity.opportunity_score != null ? `${lead.opportunity.opportunity_score}/10` : "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Probability of Success</label>
                    <span>{lead.opportunity.probability_of_success || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Automation Potential</label>
                    <span>{lead.opportunity.automation_potential || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Recurring Revenue Potential</label>
                    <span>{lead.opportunity.recurring_revenue_potential || "—"}</span>
                  </div>
                  <div className={styles.analysisItem}>
                    <label>Buying Trigger</label>
                    <span>{lead.opportunity.buying_trigger || "—"}</span>
                  </div>
                  <div className={styles.analysisItem} style={{ gridColumn: "1 / -1" }}>
                    <label>Tailored Value Proposition</label>
                    <span>{lead.opportunity.tailored_value_proposition || "—"}</span>
                  </div>
                  <div className={styles.analysisItem} style={{ gridColumn: "1 / -1" }}>
                    <label>Quick Win Offer</label>
                    <span>{lead.opportunity.quick_win_offer || "—"}</span>
                  </div>
                  <div className={styles.analysisItem} style={{ gridColumn: "1 / -1" }}>
                    <label>Decision Maker Roles</label>
                    <span>{lead.opportunity.decision_maker_roles || "—"}</span>
                  </div>
                  <div className={styles.analysisItem} style={{ gridColumn: "1 / -1" }}>
                    <label>Likely Objections</label>
                    <span>{lead.opportunity.likely_objections || "—"}</span>
                  </div>
                  <div className={styles.analysisItem} style={{ gridColumn: "1 / -1" }}>
                    <label>Counter Position</label>
                    <span>{lead.opportunity.counter_position || "—"}</span>
                  </div>
                  <div className={styles.analysisItem} style={{ gridColumn: "1 / -1" }}>
                    <label>Discovery Questions</label>
                    <span>{lead.opportunity.discovery_questions || "—"}</span>
                  </div>
                </div>
              </div>

              {/* Section 5: Research Metadata & Evidence / Sources */}
              {rp?.sources && rp.sources.length > 0 && (
                <div className={styles.analysisSection}>
                  <h4>📚 Research Evidence & Sources</h4>
                  <div className={styles.timeline}>
                    {rp.sources.map((source) => (
                      <article key={source.id} className={styles.message}>
                        <div>
                          <strong style={{ color: "#0284c7" }}>{source.source_name}</strong>
                          {source.source_type && <span className={styles.inbound}>{source.source_type}</span>}
                        </div>
                        {source.source_url && (
                          <a href={source.source_url} target="_blank" rel="noreferrer" style={{ fontSize: "12px" }}>
                            {source.source_url} ↗
                          </a>
                        )}
                        {source.notes && <p className={styles.preserve}>{source.notes}</p>}
                      </article>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className={styles.formActions}>
              <button className={styles.primaryButton} onClick={() => setShowAnalysisModal(false)}>
                Close Analysis
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
