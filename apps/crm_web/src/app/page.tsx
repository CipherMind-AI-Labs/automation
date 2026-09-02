"use client";

import { useEffect, useMemo, useState } from "react";
import { DashboardOverview } from "@/components/DashboardOverview";
import { LeadDetailPanel } from "@/components/LeadDetailPanel";
import { LeadForm } from "@/components/LeadForm";
import { LeadTable } from "@/components/LeadTable";
import styles from "@/components/crm.module.css";
import { ApiError, crmApi } from "@/lib/api";
import type { FullResearchProfile, LeadDraft, LeadRecord, Opportunity } from "@/lib/types";

const initialLoadError = "We couldn’t load the CRM data. Check that the API is running and try again.";

function buildLeadRecords(data: Awaited<ReturnType<typeof loadData>>): LeadRecord[] {
  const { companies, contacts, opportunities, threads, reminders, profileMap } = data;
  const companyById = new Map(companies.map((company) => [company.id, company]));
  return opportunities.flatMap((opportunity) => {
    const company = companyById.get(opportunity.company_id);
    if (!company) return [];
    const researchProfile = opportunity.research_profile_id
      ? profileMap.get(opportunity.research_profile_id) ?? null
      : null;
    return [
      {
        company,
        opportunity,
        contacts: contacts.filter((contact) => contact.company_id === company.id),
        threads: threads.filter(
          (thread) => thread.opportunity_id === opportunity.id || (!thread.opportunity_id && thread.company_id === company.id)
        ),
        reminders: reminders.filter((reminder) => reminder.opportunity_id === opportunity.id),
        researchProfile,
      },
    ];
  });
}

async function loadData() {
  const [companies, contacts, opportunities, threads, reminders] = await Promise.all([
    crmApi.listCompanies(),
    crmApi.listContacts(),
    crmApi.listOpportunities(),
    crmApi.listThreads(),
    crmApi.listReminders(),
  ]);

  const profileIds = Array.from(
    new Set(opportunities.map((opp) => opp.research_profile_id).filter((id): id is number => id != null))
  );

  const profilesList = await Promise.all(
    profileIds.map((id) => crmApi.getResearchProfile(id).catch(() => null))
  );

  const profileMap = new Map<number, FullResearchProfile>();
  profilesList.forEach((profile) => {
    if (profile && profile.id != null) {
      profileMap.set(profile.id, profile);
    }
  });

  return { companies, contacts, opportunities, threads, reminders, profileMap };
}

/** Provides the complete operational CRM workspace. */
export default function HomePage(): React.JSX.Element {
  const [leads, setLeads] = useState<LeadRecord[]>([]);
  const [selectedLead, setSelectedLead] = useState<LeadRecord | null>(null);
  const [editingLead, setEditingLead] = useState<LeadRecord | null | undefined>(undefined);
  const [search, setSearch] = useState("");
  const [stage, setStage] = useState("all");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const nextLeads = buildLeadRecords(await loadData());
      setLeads(nextLeads);
      setSelectedLead((current) =>
        current ? nextLeads.find((lead) => lead.opportunity.id === current.opportunity.id) ?? null : null
      );
    } catch {
      setError(initialLoadError);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void refresh();
  }, []);

  const stages = useMemo(
    () => Array.from(new Set(leads.map((lead) => lead.opportunity.lead_status || "New"))).sort(),
    [leads]
  );

  const filteredLeads = useMemo(
    () =>
      leads.filter((lead) => {
        const searchable = [
          lead.company.name,
          lead.company.headquarters,
          lead.company.website_url,
          lead.opportunity.primary_opportunity,
          ...lead.contacts.map((contact) => `${contact.full_name} ${contact.email}`),
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();
        return searchable.includes(search.toLowerCase()) && (stage === "all" || (lead.opportunity.lead_status || "New") === stage);
      }),
    [leads, search, stage]
  );

  const saveLead = async (draft: LeadDraft) => {
    setIsSaving(true);
    setError(null);
    try {
      const companyData = {
        name: draft.companyName,
        website_url: draft.websiteUrl || null,
        linkedin_url: draft.linkedinUrl || null,
        headquarters: draft.headquarters || null,
        offices_summary: draft.officesSummary || null,
        geographic_coverage: draft.geographicCoverage || null,
        industry: draft.industry || null,
        business_type: draft.businessType || null,
        employee_range: draft.employeeRange || null,
        founded_year: draft.foundedYear ? parseInt(draft.foundedYear, 10) : null,
        ownership: draft.ownership || null,
      };

      const opportunityData: Partial<Opportunity> = {
        lead_status: draft.status,
        priority: draft.priority || null,
        primary_opportunity: draft.opportunity || null,
        recommended_service: draft.recommendedService || null,
        estimated_initial_deal_size: draft.estimatedDealSize || null,
        opportunity_score: draft.opportunityScore ? parseInt(draft.opportunityScore, 10) : null,
        probability_of_success: draft.probabilityOfSuccess || null,
        automation_potential: draft.automationPotential || null,
        recurring_revenue_potential: draft.recurringRevenuePotential || null,
        buying_trigger: draft.buyingTrigger || null,

        current_pain: draft.currentPain || null,
        pitch_angle: draft.pitchAngle || null,
        tailored_value_proposition: draft.tailoredValueProposition || null,
        quick_win_offer: draft.quickWinOffer || null,

        decision_maker_roles: draft.decisionMakerRoles || null,
        likely_objections: draft.likelyObjections || null,
        counter_position: draft.counterPosition || null,
        discovery_questions: draft.discoveryQuestions || null,

        next_action: draft.nextAction || null,
        follow_up_notes: draft.notes || null,
      };

      const researchPayload = {
        company_overview: draft.companyOverview || null,
        owners_summary: draft.ownersSummary || null,
        core_services: draft.coreServices || null,
        primary_customers: draft.primaryCustomers || null,
        business_model: draft.businessModel || null,
        competitive_position: draft.competitivePosition || null,
        showroom_status: draft.showroomStatus || null,
        growth_indicators: draft.growthIndicators || null,
        research_confidence: draft.researchConfidence || null,
        researched_on: draft.researchedOn || null,
        analyst_notes: draft.analystNotes || null,
        digital_assessment: {
          website_quality_score: draft.websiteQualityScore ? parseInt(draft.websiteQualityScore, 10) : null,
          mobile_friendly: draft.mobileFriendly || null,
          blog_status: draft.blogStatus || null,
          product_search_status: draft.productSearchStatus || null,
          product_filters_status: draft.productFiltersStatus || null,
          product_catalog_status: draft.productCatalogStatus || null,
          ecommerce_status: draft.ecommerceStatus || null,
          quote_request_method: draft.quoteRequestMethod || null,
          public_pricing_status: draft.publicPricingStatus || null,
          cms: draft.cms || null,
          pim_detection: draft.pimDetection || null,
          dam_detection: draft.damDetection || null,
          technology_clues: draft.technologyClues || null,
          digital_maturity: draft.digitalMaturity || null,
        },
        product_assessment: {
          manufacturers_represented: draft.manufacturersRepresented || null,
          estimated_brands: draft.estimatedBrands || null,
          product_pages: draft.productPages || null,
          product_search_experience: draft.productSearchExperience || null,
          product_filters_quality: draft.productFiltersQuality || null,
          images_status: draft.imagesStatus || null,
          product_descriptions_status: draft.productDescriptionsStatus || null,
          specifications_status: draft.specificationsStatus || null,
          cad_revit_status: draft.cadRevitStatus || null,
          brochures_status: draft.brochuresStatus || null,
          sustainability_warranty_docs_status: draft.sustainabilityWarrantyDocsStatus || null,
          product_attributes_completeness_score: draft.productAttributesCompletenessScore
            ? parseInt(draft.productAttributesCompletenessScore, 10)
            : null,
          data_ownership: draft.dataOwnership || null,
          product_information_quality_score: draft.productInformationQualityScore
            ? parseInt(draft.productInformationQualityScore, 10)
            : null,
          estimated_catalog_size: draft.estimatedCatalogSize || null,
        },
      };

      let companyId: number;
      let opportunityId: number;
      let contactId: number | null = null;

      if (editingLead) {
        companyId = editingLead.company.id;
        opportunityId = editingLead.opportunity.id;
        await crmApi.updateCompany(companyId, companyData);

        const contact = editingLead.contacts[0];
        if (contact) {
          contactId = contact.id;
          await crmApi.updateContact(contact.id, {
            full_name: draft.contactName || null,
            job_title: draft.contactTitle || null,
            email: draft.contactEmail || null,
            phone: draft.contactPhone || null,
          });
        } else if (draft.contactName) {
          const created = await crmApi.createContact({
            company_id: companyId,
            full_name: draft.contactName,
            job_title: draft.contactTitle || null,
            email: draft.contactEmail || null,
            phone: draft.contactPhone || null,
          });
          contactId = created.id;
        }

        const profileId = editingLead.opportunity.research_profile_id;
        if (profileId) {
          await crmApi.updateResearchProfile(profileId, researchPayload);
        } else {
          const createdProfile = await crmApi.createResearchProfile({ company_id: companyId, ...researchPayload });
          opportunityData.research_profile_id = createdProfile.id;
        }

        await crmApi.updateOpportunity(opportunityId, opportunityData);

        const reminder = editingLead.reminders.find((item) => item.status === "pending");
        if (draft.followUpAt) {
          const reminderData = {
            opportunity_id: opportunityId,
            contact_id: contactId,
            due_at: new Date(draft.followUpAt).toISOString(),
            notes: draft.nextAction || draft.notes || null,
            status: "pending",
          };
          if (reminder) await crmApi.updateReminder(reminder.id, reminderData);
          else await crmApi.createReminder(reminderData);
        }
      } else {
        const company = await crmApi.createCompany(companyData);
        companyId = company.id;

        const contact = draft.contactName
          ? await crmApi.createContact({
              company_id: companyId,
              full_name: draft.contactName,
              job_title: draft.contactTitle || null,
              email: draft.contactEmail || null,
              phone: draft.contactPhone || null,
            })
          : null;
        contactId = contact?.id ?? null;

        const createdProfile = await crmApi.createResearchProfile({ company_id: companyId, ...researchPayload });
        opportunityData.research_profile_id = createdProfile.id;

        const opportunity = await crmApi.createOpportunity({
          company_id: companyId,
          ...opportunityData,
        });
        opportunityId = opportunity.id;

        if (draft.followUpAt) {
          await crmApi.createReminder({
            opportunity_id: opportunityId,
            contact_id: contactId,
            due_at: new Date(draft.followUpAt).toISOString(),
            notes: draft.nextAction || draft.notes || null,
            status: "pending",
          });
        }
      }

      setEditingLead(undefined);
      await refresh();
    } catch (saveError) {
      setError(saveError instanceof ApiError ? saveError.message : "Your changes could not be saved.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <main className={styles.appShell}>
      <header className={styles.header}>
        <div className={styles.brandGroup}>
          <img src="/logo-full.png" alt="CipherMind AI Labs" className={styles.brandLogo} />
          <div className={styles.brandInfo}>
            <p className={styles.eyebrow}>CipherMind AI Labs LLC</p>
            <h1>Lead Discovery & CRM Workspace</h1>
          </div>
        </div>
        <button className={styles.primaryButton} onClick={() => setEditingLead(null)}>
          + Add Lead
        </button>
      </header>

      <DashboardOverview leads={leads} />

      <section className={styles.workspace}>
        <div className={styles.listArea}>
          <div className={styles.toolbar}>
            <label className={styles.searchLabel}>
              <span>Search</span>
              <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Company, contact, location, opportunity…"
              />
            </label>
            <label className={styles.filterLabel}>
              <span>Stage</span>
              <select value={stage} onChange={(event) => setStage(event.target.value)}>
                <option value="all">All stages</option>
                {stages.map((item) => (
                  <option key={item}>{item}</option>
                ))}
              </select>
            </label>
            <span className={styles.resultCount}>
              {filteredLeads.length} lead{filteredLeads.length === 1 ? "" : "s"}
            </span>
          </div>

          {error && (
            <div className={styles.errorBanner}>
              {error}
              <button onClick={() => void refresh()}>Try again</button>
            </div>
          )}

          {isLoading ? (
            <div className={styles.emptyState}>
              <strong>Loading leads…</strong>
              <span>Fetching operational data from database.</span>
            </div>
          ) : (
            <LeadTable
              leads={filteredLeads}
              selectedLeadId={selectedLead?.opportunity.id ?? null}
              onSelect={setSelectedLead}
            />
          )}
        </div>

        <LeadDetailPanel
          lead={selectedLead}
          onClose={() => setSelectedLead(null)}
          onEdit={() => setEditingLead(selectedLead)}
          onRefresh={refresh}
        />
      </section>

      {editingLead !== undefined && (
        <LeadForm
          lead={editingLead}
          isSaving={isSaving}
          onClose={() => setEditingLead(undefined)}
          onSave={saveLead}
        />
      )}
    </main>
  );
}
