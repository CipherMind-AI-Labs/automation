"use client";

import { useEffect, useState } from "react";
import styles from "@/components/crm.module.css";
import { toDateTimeInput } from "@/lib/formatters";
import type { LeadDraft, LeadRecord } from "@/lib/types";

const stages = ["New", "Qualified", "Contacted", "Proposal Sent", "Negotiation", "Won", "Lost"];
const priorities = ["", "High", "Medium", "Low"];

interface LeadFormProps {
  lead: LeadRecord | null;
  isSaving: boolean;
  onClose: () => void;
  onSave: (draft: LeadDraft) => Promise<void>;
}

function draftFromLead(lead: LeadRecord | null): LeadDraft {
  const contact = lead?.contacts[0];
  const reminder = lead?.reminders.find((item) => item.status === "pending");
  const rp = lead?.researchProfile;
  const da = rp?.digital_assessment;
  const pa = rp?.product_assessment;

  return {
    // Company fields
    companyName: lead?.company.name ?? "",
    websiteUrl: lead?.company.website_url ?? "",
    linkedinUrl: lead?.company.linkedin_url ?? "",
    headquarters: lead?.company.headquarters ?? "",
    officesSummary: lead?.company.offices_summary ?? "",
    geographicCoverage: lead?.company.geographic_coverage ?? "",
    industry: lead?.company.industry ?? "",
    businessType: lead?.company.business_type ?? "",
    employeeRange: lead?.company.employee_range ?? "",
    foundedYear: lead?.company.founded_year ? String(lead.company.founded_year) : "",
    ownership: lead?.company.ownership ?? "",

    // Contact fields
    contactName: contact?.full_name ?? "",
    contactTitle: contact?.job_title ?? "",
    contactEmail: contact?.email ?? "",
    contactPhone: contact?.phone ?? "",

    // Lead / Opportunity fields
    status: lead?.opportunity.lead_status ?? "New",
    priority: lead?.opportunity.priority ?? "",
    opportunity: lead?.opportunity.primary_opportunity ?? "",
    recommendedService: lead?.opportunity.recommended_service ?? "",
    estimatedDealSize: lead?.opportunity.estimated_initial_deal_size ?? "",
    opportunityScore: lead?.opportunity.opportunity_score ? String(lead.opportunity.opportunity_score) : "",
    probabilityOfSuccess: lead?.opportunity.probability_of_success ?? "",
    automationPotential: lead?.opportunity.automation_potential ?? "",
    recurringRevenuePotential: lead?.opportunity.recurring_revenue_potential ?? "",
    buyingTrigger: lead?.opportunity.buying_trigger ?? "",

    // Pain Points & Value Proposition
    currentPain: lead?.opportunity.current_pain ?? "",
    pitchAngle: lead?.opportunity.pitch_angle ?? "",
    tailoredValueProposition: lead?.opportunity.tailored_value_proposition ?? "",
    quickWinOffer: lead?.opportunity.quick_win_offer ?? "",

    // Decision Makers & Objections
    decisionMakerRoles: lead?.opportunity.decision_maker_roles ?? "",
    likelyObjections: lead?.opportunity.likely_objections ?? "",
    counterPosition: lead?.opportunity.counter_position ?? "",
    discoveryQuestions: lead?.opportunity.discovery_questions ?? "",

    // Research Profile - Company Intelligence
    companyOverview: rp?.company_overview ?? "",
    ownersSummary: rp?.owners_summary ?? "",
    coreServices: rp?.core_services ?? "",
    primaryCustomers: rp?.primary_customers ?? "",
    businessModel: rp?.business_model ?? "",
    competitivePosition: rp?.competitive_position ?? "",
    showroomStatus: rp?.showroom_status ?? "",
    growthIndicators: rp?.growth_indicators ?? "",
    researchConfidence: rp?.research_confidence ?? "",
    researchedOn: rp?.researched_on ?? "",
    analystNotes: rp?.analyst_notes ?? "",

    // Digital Intelligence
    websiteQualityScore: da?.website_quality_score != null ? String(da.website_quality_score) : "",
    mobileFriendly: da?.mobile_friendly ?? "",
    blogStatus: da?.blog_status ?? "",
    productSearchStatus: da?.product_search_status ?? "",
    productFiltersStatus: da?.product_filters_status ?? "",
    productCatalogStatus: da?.product_catalog_status ?? "",
    ecommerceStatus: da?.ecommerce_status ?? "",
    quoteRequestMethod: da?.quote_request_method ?? "",
    publicPricingStatus: da?.public_pricing_status ?? "",
    cms: da?.cms ?? "",
    pimDetection: da?.pim_detection ?? "",
    damDetection: da?.dam_detection ?? "",
    technologyClues: da?.technology_clues ?? "",
    digitalMaturity: da?.digital_maturity ?? "",

    // Product Information Intelligence
    manufacturersRepresented: pa?.manufacturers_represented ?? "",
    estimatedBrands: pa?.estimated_brands ?? "",
    productPages: pa?.product_pages ?? "",
    productSearchExperience: pa?.product_search_experience ?? "",
    productFiltersQuality: pa?.product_filters_quality ?? "",
    imagesStatus: pa?.images_status ?? "",
    productDescriptionsStatus: pa?.product_descriptions_status ?? "",
    specificationsStatus: pa?.specifications_status ?? "",
    cadRevitStatus: pa?.cad_revit_status ?? "",
    brochuresStatus: pa?.brochures_status ?? "",
    sustainabilityWarrantyDocsStatus: pa?.sustainability_warranty_docs_status ?? "",
    productAttributesCompletenessScore: pa?.product_attributes_completeness_score != null ? String(pa.product_attributes_completeness_score) : "",
    dataOwnership: pa?.data_ownership ?? "",
    productInformationQualityScore: pa?.product_information_quality_score != null ? String(pa.product_information_quality_score) : "",
    estimatedCatalogSize: pa?.estimated_catalog_size ?? "",

    // Next steps & Notes
    nextAction: lead?.opportunity.next_action ?? "",
    followUpAt: toDateTimeInput(reminder?.due_at ?? lead?.threads[0]?.next_follow_up_due_at),
    notes: lead?.opportunity.follow_up_notes ?? "",
  };
}

/** Provides the complete create and edit workflow exposing all Research Intelligence and CRM data fields. */
export function LeadForm({ lead, isSaving, onClose, onSave }: LeadFormProps): React.JSX.Element {
  const [draft, setDraft] = useState<LeadDraft>(() => draftFromLead(lead));

  useEffect(() => setDraft(draftFromLead(lead)), [lead]);

  const update =
    (field: keyof LeadDraft) =>
    (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
      setDraft((current) => ({ ...current, [field]: event.target.value }));

  const submit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await onSave(draft);
  };

  return (
    <div className={styles.modalBackdrop} role="presentation">
      <form className={styles.formModal} onSubmit={submit}>
        <div className={styles.panelHeader}>
          <div>
            <p className={styles.eyebrow}>{lead ? "Edit Lead & Research Profile" : "New Lead"}</p>
            <h2>{lead ? lead.company.name : "Add a Lead"}</h2>
          </div>
          <button type="button" className={styles.iconButton} onClick={onClose} aria-label="Close form">
            ×
          </button>
        </div>

        <div className={styles.formContent}>
          {/* Section 1: Company Profile */}
          <fieldset>
            <legend>🏢 Company Profile</legend>
            <label>
              Company Name *
              <input required value={draft.companyName} onChange={update("companyName")} />
            </label>

            <div className={styles.formGrid}>
              <label>
                Website URL
                <input type="url" value={draft.websiteUrl} onChange={update("websiteUrl")} placeholder="https://" />
              </label>
              <label>
                LinkedIn URL
                <input type="url" value={draft.linkedinUrl} onChange={update("linkedinUrl")} placeholder="https://" />
              </label>
              <label>
                Headquarters
                <input value={draft.headquarters} onChange={update("headquarters")} placeholder="City, State, Country" />
              </label>
              <label>
                Offices Summary
                <input value={draft.officesSummary} onChange={update("officesSummary")} placeholder="Locations summary" />
              </label>
              <label>
                Geographic Coverage
                <input value={draft.geographicCoverage} onChange={update("geographicCoverage")} placeholder="e.g. Midwest, USA" />
              </label>
              <label>
                Industry
                <input value={draft.industry} onChange={update("industry")} />
              </label>
              <label>
                Business Type
                <input value={draft.businessType} onChange={update("businessType")} placeholder="e.g. Independent Dealer" />
              </label>
              <label>
                Employee Range
                <input value={draft.employeeRange} onChange={update("employeeRange")} placeholder="e.g. 50-200" />
              </label>
              <label>
                Founded Year
                <input type="number" value={draft.foundedYear} onChange={update("foundedYear")} placeholder="e.g. 1989" />
              </label>
              <label>
                Ownership Structure
                <input value={draft.ownership} onChange={update("ownership")} placeholder="e.g. Privately Held / Family-owned" />
              </label>
            </div>
          </fieldset>

          {/* Section 2: Primary Contact */}
          <fieldset>
            <legend>👤 Primary Contact</legend>
            <div className={styles.formGrid}>
              <label>
                Full Name
                <input value={draft.contactName} onChange={update("contactName")} />
              </label>
              <label>
                Job Title / Role
                <input value={draft.contactTitle} onChange={update("contactTitle")} />
              </label>
              <label>
                Email Address
                <input type="email" value={draft.contactEmail} onChange={update("contactEmail")} />
              </label>
              <label>
                Phone Number
                <input type="tel" value={draft.contactPhone} onChange={update("contactPhone")} />
              </label>
            </div>
          </fieldset>

          {/* Section 3: Strategic Commercial Opportunity */}
          <fieldset>
            <legend>🎯 Strategic Commercial Opportunity</legend>
            <div className={styles.formGrid}>
              <label>
                Lead Stage
                <select value={draft.status} onChange={update("status")}>
                  {stages.map((stage) => (
                    <option key={stage}>{stage}</option>
                  ))}
                </select>
              </label>
              <label>
                Priority
                <select value={draft.priority} onChange={update("priority")}>
                  {priorities.map((priority) => (
                    <option value={priority} key={priority}>
                      {priority || "Not set"}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Estimated Deal Size
                <input value={draft.estimatedDealSize} onChange={update("estimatedDealSize")} placeholder="e.g. $10k-$25k" />
              </label>
              <label>
                Opportunity Score (1-10)
                <input type="number" min="1" max="10" value={draft.opportunityScore} onChange={update("opportunityScore")} placeholder="e.g. 8" />
              </label>
              <label>
                Probability of Success
                <input value={draft.probabilityOfSuccess} onChange={update("probabilityOfSuccess")} placeholder="e.g. High / Medium" />
              </label>
              <label>
                Automation Potential
                <input value={draft.automationPotential} onChange={update("automationPotential")} placeholder="e.g. High" />
              </label>
              <label>
                Recurring Revenue Potential
                <input value={draft.recurringRevenuePotential} onChange={update("recurringRevenuePotential")} placeholder="e.g. High" />
              </label>
              <label>
                Buying Trigger
                <input value={draft.buyingTrigger} onChange={update("buyingTrigger")} placeholder="e.g. Website redesign / SEO" />
              </label>
            </div>

            <label>
              Primary Opportunity
              <input value={draft.opportunity} onChange={update("opportunity")} placeholder="e.g. Searchable digital catalog" />
            </label>

            <label>
              Recommended Service
              <input value={draft.recommendedService} onChange={update("recommendedService")} placeholder="e.g. Digital Catalog Experience" />
            </label>
          </fieldset>

          {/* Section 4: Pain Points & Value Proposition */}
          <fieldset>
            <legend>💡 Pain Points & Value Proposition</legend>
            <label>
              Current Pain Point
              <textarea rows={2} value={draft.currentPain} onChange={update("currentPain")} placeholder="Current operational or website pain..." />
            </label>

            <label>
              Pitch Angle
              <input value={draft.pitchAngle} onChange={update("pitchAngle")} placeholder="Strategic pitch angle..." />
            </label>

            <label>
              Tailored Value Proposition
              <textarea rows={2} value={draft.tailoredValueProposition} onChange={update("tailoredValueProposition")} placeholder="Tailored value prop..." />
            </label>

            <label>
              Quick Win Offer
              <input value={draft.quickWinOffer} onChange={update("quickWinOffer")} placeholder="e.g. Pilot one brand catalog" />
            </label>
          </fieldset>

          {/* Section 5: Decision Makers & Objections */}
          <fieldset>
            <legend>👥 Decision Makers & Objections</legend>
            <label>
              Decision Maker Roles
              <input value={draft.decisionMakerRoles} onChange={update("decisionMakerRoles")} placeholder="e.g. CEO, CFO, VP Sales" />
            </label>

            <label>
              Likely Objections
              <textarea rows={2} value={draft.likelyObjections} onChange={update("likelyObjections")} placeholder="Common objections..." />
            </label>

            <label>
              Counter Position
              <textarea rows={2} value={draft.counterPosition} onChange={update("counterPosition")} placeholder="Recommended counter positioning..." />
            </label>

            <label>
              Discovery Questions
              <textarea rows={2} value={draft.discoveryQuestions} onChange={update("discoveryQuestions")} placeholder="Key discovery questions..." />
            </label>
          </fieldset>

          {/* Section 6: Company Intelligence */}
          <fieldset>
            <legend>🔬 Company Intelligence</legend>
            <label>
              Company Overview
              <textarea rows={2} value={draft.companyOverview} onChange={update("companyOverview")} placeholder="High-level overview..." />
            </label>

            <div className={styles.formGrid}>
              <label>
                Owners / Leadership Summary
                <input value={draft.ownersSummary} onChange={update("ownersSummary")} placeholder="e.g. Michael Troia; Hilary Troia" />
              </label>
              <label>
                Showroom Status
                <input value={draft.showroomStatus} onChange={update("showroomStatus")} placeholder="e.g. Yes / No" />
              </label>
              <label>
                Research Confidence
                <input value={draft.researchConfidence} onChange={update("researchConfidence")} placeholder="e.g. High / Medium" />
              </label>
              <label>
                Researched On Date
                <input type="date" value={draft.researchedOn} onChange={update("researchedOn")} />
              </label>
            </div>

            <label>
              Core Services
              <input value={draft.coreServices} onChange={update("coreServices")} placeholder="e.g. Furniture sales; Interior design; Space planning" />
            </label>

            <label>
              Primary Customers
              <input value={draft.primaryCustomers} onChange={update("primaryCustomers")} placeholder="e.g. Corporate; Healthcare; Education" />
            </label>

            <label>
              Business Model
              <input value={draft.businessModel} onChange={update("businessModel")} placeholder="e.g. Consultative dealership" />
            </label>

            <label>
              Competitive Position
              <input value={draft.competitivePosition} onChange={update("competitivePosition")} placeholder="Competitive advantages..." />
            </label>

            <label>
              Growth Indicators
              <input value={draft.growthIndicators} onChange={update("growthIndicators")} placeholder="e.g. Recent acquisitions, expansion" />
            </label>

            <label>
              Analyst Notes
              <textarea rows={2} value={draft.analystNotes} onChange={update("analystNotes")} placeholder="Analyst key takeaways..." />
            </label>
          </fieldset>

          {/* Section 7: Digital Capability Audit */}
          <fieldset>
            <legend>💻 Digital Capability Audit</legend>
            <div className={styles.formGrid}>
              <label>
                Website Quality Score (1-10)
                <input type="number" min="1" max="10" value={draft.websiteQualityScore} onChange={update("websiteQualityScore")} placeholder="e.g. 8" />
              </label>
              <label>
                Mobile Friendly
                <input value={draft.mobileFriendly} onChange={update("mobileFriendly")} placeholder="e.g. Yes / No" />
              </label>
              <label>
                Blog Status
                <input value={draft.blogStatus} onChange={update("blogStatus")} placeholder="e.g. Active / None" />
              </label>
              <label>
                Product Search Status
                <input value={draft.productSearchStatus} onChange={update("productSearchStatus")} placeholder="e.g. None / Global" />
              </label>
              <label>
                Product Filters Status
                <input value={draft.productFiltersStatus} onChange={update("productFiltersStatus")} placeholder="e.g. Limited / Advanced" />
              </label>
              <label>
                Product Catalog Status
                <input value={draft.productCatalogStatus} onChange={update("productCatalogStatus")} placeholder="e.g. Partial / Full" />
              </label>
              <label>
                Ecommerce Status
                <input value={draft.ecommerceStatus} onChange={update("ecommerceStatus")} placeholder="e.g. No / Full" />
              </label>
              <label>
                Quote Request Method
                <input value={draft.quoteRequestMethod} onChange={update("quoteRequestMethod")} placeholder="e.g. Contact form" />
              </label>
              <label>
                Public Pricing Status
                <input value={draft.publicPricingStatus} onChange={update("publicPricingStatus")} placeholder="e.g. No / Yes" />
              </label>
              <label>
                CMS
                <input value={draft.cms} onChange={update("cms")} placeholder="e.g. WordPress / Craft" />
              </label>
              <label>
                PIM Detection
                <input value={draft.pimDetection} onChange={update("pimDetection")} placeholder="e.g. None / Akeneo" />
              </label>
              <label>
                DAM Detection
                <input value={draft.damDetection} onChange={update("damDetection")} placeholder="e.g. None" />
              </label>
              <label>
                Digital Maturity
                <input value={draft.digitalMaturity} onChange={update("digitalMaturity")} placeholder="e.g. Low / Medium / High" />
              </label>
            </div>
            <label>
              Technology Clues
              <input value={draft.technologyClues} onChange={update("technologyClues")} placeholder="e.g. Google Cloud, reCAPTCHA" />
            </label>
          </fieldset>

          {/* Section 8: Product Data Maturity Audit */}
          <fieldset>
            <legend>📦 Product Data Maturity Audit</legend>
            <div className={styles.formGrid}>
              <label>
                Manufacturers Represented
                <input value={draft.manufacturersRepresented} onChange={update("manufacturersRepresented")} placeholder="e.g. 100+" />
              </label>
              <label>
                Estimated Brands
                <input value={draft.estimatedBrands} onChange={update("estimatedBrands")} placeholder="e.g. 50+" />
              </label>
              <label>
                Product Pages
                <input value={draft.productPages} onChange={update("productPages")} placeholder="e.g. Yes / No" />
              </label>
              <label>
                Search Experience
                <input value={draft.productSearchExperience} onChange={update("productSearchExperience")} placeholder="e.g. Basic" />
              </label>
              <label>
                Filters Quality
                <input value={draft.productFiltersQuality} onChange={update("productFiltersQuality")} placeholder="e.g. Limited" />
              </label>
              <label>
                Images Status
                <input value={draft.imagesStatus} onChange={update("imagesStatus")} placeholder="e.g. High quality" />
              </label>
              <label>
                Product Descriptions
                <input value={draft.productDescriptionsStatus} onChange={update("productDescriptionsStatus")} placeholder="e.g. Full" />
              </label>
              <label>
                Specifications Status
                <input value={draft.specificationsStatus} onChange={update("specificationsStatus")} placeholder="e.g. Limited PDF" />
              </label>
              <label>
                CAD / Revit Status
                <input value={draft.cadRevitStatus} onChange={update("cadRevitStatus")} placeholder="e.g. Available" />
              </label>
              <label>
                Brochures Status
                <input value={draft.brochuresStatus} onChange={update("brochuresStatus")} placeholder="e.g. Available" />
              </label>
              <label>
                Sustainability & Warranty Docs
                <input value={draft.sustainabilityWarrantyDocsStatus} onChange={update("sustainabilityWarrantyDocsStatus")} placeholder="e.g. Available" />
              </label>
              <label>
                Attributes Completeness Score (1-10)
                <input type="number" min="1" max="10" value={draft.productAttributesCompletenessScore} onChange={update("productAttributesCompletenessScore")} placeholder="e.g. 7" />
              </label>
              <label>
                Data Ownership
                <input value={draft.dataOwnership} onChange={update("dataOwnership")} placeholder="e.g. Manufacturer-sourced" />
              </label>
              <label>
                Information Quality Score (1-10)
                <input type="number" min="1" max="10" value={draft.productInformationQualityScore} onChange={update("productInformationQualityScore")} placeholder="e.g. 8" />
              </label>
              <label>
                Estimated Catalog Size
                <input value={draft.estimatedCatalogSize} onChange={update("estimatedCatalogSize")} placeholder="e.g. 5,000 SKUs" />
              </label>
            </div>
          </fieldset>

          {/* Section 9: Next Action & Follow-up */}
          <fieldset>
            <legend>📅 Next Action & Follow-up</legend>
            <div className={styles.formGrid}>
              <label>
                Next Action
                <input value={draft.nextAction} onChange={update("nextAction")} placeholder="e.g. Schedule demo with leadership" />
              </label>
              <label>
                Next Follow-up Date/Time
                <input type="datetime-local" value={draft.followUpAt} onChange={update("followUpAt")} />
              </label>
            </div>

            <label>
              Follow-up Notes / History
              <textarea rows={3} value={draft.notes} onChange={update("notes")} placeholder="Operational notes..." />
            </label>
          </fieldset>
        </div>

        <div className={styles.formActions}>
          <button type="button" className={styles.secondaryButton} onClick={onClose}>
            Cancel
          </button>
          <button className={styles.primaryButton} disabled={isSaving}>
            {isSaving ? "Saving…" : lead ? "Save Changes" : "Create Lead"}
          </button>
        </div>
      </form>
    </div>
  );
}
