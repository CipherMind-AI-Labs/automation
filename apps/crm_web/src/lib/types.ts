export interface Company {
  id: number;
  name: string;
  website_url: string | null;
  linkedin_url: string | null;
  headquarters: string | null;
  offices_summary: string | null;
  geographic_coverage: string | null;
  industry: string | null;
  business_type: string | null;
  employee_range: string | null;
  founded_year: number | null;
  ownership: string | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface Contact {
  id: number;
  company_id: number;
  first_name: string | null;
  last_name: string | null;
  full_name: string | null;
  job_title: string | null;
  email: string | null;
  phone: string | null;
  linkedin_url: string | null;
  is_decision_maker: number;
  notes: string | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface Opportunity {
  id: number;
  company_id: number;
  research_profile_id: number | null;
  current_pain: string | null;
  business_impact: string | null;
  automation_potential: string | null;
  recurring_revenue_potential: string | null;
  opportunity_score: number | null;
  primary_opportunity: string | null;
  recommended_service: string | null;
  pitch_angle: string | null;
  tailored_value_proposition: string | null;
  quick_win_offer: string | null;
  expected_business_value: string | null;
  estimated_initial_deal_size: string | null;
  decision_maker_roles: string | null;
  buying_trigger: string | null;
  likely_objections: string | null;
  counter_position: string | null;
  discovery_questions: string | null;
  recommended_first_contact: string | null;
  probability_of_success: string | null;
  lead_status: string | null;
  priority: string | null;
  first_outreach_at: string | null;
  next_action: string | null;
  follow_up_cadence: string | null;
  follow_up_notes: string | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface Communication {
  id: number;
  thread_id: number;
  contact_id: number | null;
  channel: string;
  direction: string;
  subject: string | null;
  body_text: string | null;
  message_status: string;
  sent_at: string | null;
  received_at: string | null;
  created_at: string | null;
}

export interface CommunicationThread {
  id: number;
  company_id: number;
  opportunity_id: number | null;
  channel: string;
  subject: string | null;
  thread_status: string;
  last_outbound_at: string | null;
  last_inbound_at: string | null;
  reply_due_at: string | null;
  next_follow_up_due_at: string | null;
  created_at: string | null;
  messages?: Communication[];
}

export interface Reminder {
  id: number;
  opportunity_id: number | null;
  thread_id: number | null;
  contact_id: number | null;
  reminder_type: string;
  status: string;
  due_at: string;
  completed_at: string | null;
  notes: string | null;
}

export interface DigitalAssessment {
  research_profile_id?: number | null;
  website_quality_score?: number | null;
  mobile_friendly?: string | null;
  blog_status?: string | null;
  product_search_status?: string | null;
  product_filters_status?: string | null;
  product_catalog_status?: string | null;
  ecommerce_status?: string | null;
  quote_request_method?: string | null;
  public_pricing_status?: string | null;
  cms?: string | null;
  pim_detection?: string | null;
  dam_detection?: string | null;
  technology_clues?: string | null;
  digital_maturity?: string | null;
}

export interface ProductAssessment {
  research_profile_id?: number | null;
  manufacturers_represented?: string | null;
  estimated_brands?: string | null;
  product_pages?: string | null;
  product_search_experience?: string | null;
  product_filters_quality?: string | null;
  images_status?: string | null;
  product_descriptions_status?: string | null;
  specifications_status?: string | null;
  cad_revit_status?: string | null;
  brochures_status?: string | null;
  sustainability_warranty_docs_status?: string | null;
  product_attributes_completeness_score?: number | null;
  data_ownership?: string | null;
  product_information_quality_score?: number | null;
  estimated_catalog_size?: string | null;
}

export interface ResearchSource {
  id?: number;
  research_profile_id?: number | null;
  source_type?: string | null;
  source_name: string;
  source_url?: string | null;
  notes?: string | null;
  created_at?: string | null;
}

export interface FullResearchProfile {
  id?: number;
  company_id?: number | null;
  company_overview?: string | null;
  owners_summary?: string | null;
  core_services?: string | null;
  primary_customers?: string | null;
  business_model?: string | null;
  competitive_position?: string | null;
  showroom_status?: string | null;
  growth_indicators?: string | null;
  research_confidence?: string | null;
  researched_on?: string | null;
  analyst_notes?: string | null;
  created_at?: string | null;
  digital_assessment?: DigitalAssessment | null;
  product_assessment?: ProductAssessment | null;
  sources?: ResearchSource[];
}

export interface LeadRecord {
  company: Company;
  opportunity: Opportunity;
  contacts: Contact[];
  threads: CommunicationThread[];
  reminders: Reminder[];
  researchProfile?: FullResearchProfile | null;
}

export type LeadDraft = {
  // Company fields
  companyName: string;
  websiteUrl: string;
  linkedinUrl: string;
  headquarters: string;
  officesSummary: string;
  geographicCoverage: string;
  industry: string;
  businessType: string;
  employeeRange: string;
  foundedYear: string;
  ownership: string;

  // Contact fields
  contactName: string;
  contactTitle: string;
  contactEmail: string;
  contactPhone: string;

  // Lead / Opportunity fields
  status: string;
  priority: string;
  opportunity: string;
  recommendedService: string;
  estimatedDealSize: string;
  opportunityScore: string;
  probabilityOfSuccess: string;
  automationPotential: string;
  recurringRevenuePotential: string;
  buyingTrigger: string;

  // Pain Points & Value Proposition
  currentPain: string;
  pitchAngle: string;
  tailoredValueProposition: string;
  quickWinOffer: string;

  // Decision Makers & Objections
  decisionMakerRoles: string;
  likelyObjections: string;
  counterPosition: string;
  discoveryQuestions: string;

  // Research Profile - Company Intelligence
  companyOverview: string;
  ownersSummary: string;
  coreServices: string;
  primaryCustomers: string;
  businessModel: string;
  competitivePosition: string;
  showroomStatus: string;
  growthIndicators: string;
  researchConfidence: string;
  researchedOn: string;
  analystNotes: string;

  // Research Profile - Digital Intelligence
  websiteQualityScore: string;
  mobileFriendly: string;
  blogStatus: string;
  productSearchStatus: string;
  productFiltersStatus: string;
  productCatalogStatus: string;
  ecommerceStatus: string;
  quoteRequestMethod: string;
  publicPricingStatus: string;
  cms: string;
  pimDetection: string;
  damDetection: string;
  technologyClues: string;
  digitalMaturity: string;

  // Research Profile - Product Information Intelligence
  manufacturersRepresented: string;
  estimatedBrands: string;
  productPages: string;
  productSearchExperience: string;
  productFiltersQuality: string;
  imagesStatus: string;
  productDescriptionsStatus: string;
  specificationsStatus: string;
  cadRevitStatus: string;
  brochuresStatus: string;
  sustainabilityWarrantyDocsStatus: string;
  productAttributesCompletenessScore: string;
  dataOwnership: string;
  productInformationQualityScore: string;
  estimatedCatalogSize: string;

  // Next steps & Notes
  nextAction: string;
  followUpAt: string;
  notes: string;
};
