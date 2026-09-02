from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Opportunity:
    """Domain model representing a commercial deal opportunity."""

    id: int | None = None
    company_id: int | None = None
    research_profile_id: int | None = None
    current_pain: str | None = None
    business_impact: str | None = None
    automation_potential: str | None = None
    recurring_revenue_potential: str | None = None
    opportunity_score: int | None = None
    primary_opportunity: str | None = None
    recommended_service: str | None = None
    pitch_angle: str | None = None
    tailored_value_proposition: str | None = None
    quick_win_offer: str | None = None
    expected_business_value: str | None = None
    estimated_initial_deal_size: str | None = None
    decision_maker_roles: str | None = None
    buying_trigger: str | None = None
    likely_objections: str | None = None
    counter_position: str | None = None
    discovery_questions: str | None = None
    recommended_first_contact: str | None = None
    probability_of_success: str | None = None
    lead_status: str | None = "New"
    priority: str | None = None
    first_outreach_at: str | None = None
    next_action: str | None = None
    follow_up_cadence: str | None = None
    follow_up_notes: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> Opportunity:
        """Construct Opportunity from database row dict."""
        return cls(
            id=row.get("id"),
            company_id=row.get("company_id"),
            research_profile_id=row.get("research_profile_id"),
            current_pain=row.get("current_pain"),
            business_impact=row.get("business_impact"),
            automation_potential=row.get("automation_potential"),
            recurring_revenue_potential=row.get("recurring_revenue_potential"),
            opportunity_score=row.get("opportunity_score"),
            primary_opportunity=row.get("primary_opportunity"),
            recommended_service=row.get("recommended_service"),
            pitch_angle=row.get("pitch_angle"),
            tailored_value_proposition=row.get("tailored_value_proposition"),
            quick_win_offer=row.get("quick_win_offer"),
            expected_business_value=row.get("expected_business_value"),
            estimated_initial_deal_size=row.get("estimated_initial_deal_size"),
            decision_maker_roles=row.get("decision_maker_roles"),
            buying_trigger=row.get("buying_trigger"),
            likely_objections=row.get("likely_objections"),
            counter_position=row.get("counter_position"),
            discovery_questions=row.get("discovery_questions"),
            recommended_first_contact=row.get("recommended_first_contact"),
            probability_of_success=row.get("probability_of_success"),
            lead_status=row.get("lead_status") or "New",
            priority=row.get("priority"),
            first_outreach_at=row.get("first_outreach_at"),
            next_action=row.get("next_action"),
            follow_up_cadence=row.get("follow_up_cadence"),
            follow_up_notes=row.get("follow_up_notes"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize Opportunity into a dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "research_profile_id": self.research_profile_id,
            "current_pain": self.current_pain,
            "business_impact": self.business_impact,
            "automation_potential": self.automation_potential,
            "recurring_revenue_potential": self.recurring_revenue_potential,
            "opportunity_score": self.opportunity_score,
            "primary_opportunity": self.primary_opportunity,
            "recommended_service": self.recommended_service,
            "pitch_angle": self.pitch_angle,
            "tailored_value_proposition": self.tailored_value_proposition,
            "quick_win_offer": self.quick_win_offer,
            "expected_business_value": self.expected_business_value,
            "estimated_initial_deal_size": self.estimated_initial_deal_size,
            "decision_maker_roles": self.decision_maker_roles,
            "buying_trigger": self.buying_trigger,
            "likely_objections": self.likely_objections,
            "counter_position": self.counter_position,
            "discovery_questions": self.discovery_questions,
            "recommended_first_contact": self.recommended_first_contact,
            "probability_of_success": self.probability_of_success,
            "lead_status": self.lead_status,
            "priority": self.priority,
            "first_outreach_at": self.first_outreach_at,
            "next_action": self.next_action,
            "follow_up_cadence": self.follow_up_cadence,
            "follow_up_notes": self.follow_up_notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
