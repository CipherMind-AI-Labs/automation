from __future__ import annotations

from typing import Any

from src.database.base import DatabaseAdapter
from src.models.opportunity import Opportunity


class OpportunityRepository:
    """Repository for Opportunity entity SQL operations."""

    def __init__(self, database: DatabaseAdapter) -> None:
        """Initialize repository with DatabaseAdapter."""
        self.database = database

    def list(
        self,
        company_id: int | None = None,
        lead_status: str | None = None,
        priority: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Opportunity]:
        """Fetch list of commercial opportunities with optional filtering.

        Args:
            company_id: Company ID filter.
            lead_status: Lead status string filter (e.g. 'New', 'Qualified').
            priority: Priority string filter (e.g. 'High').
            limit: Page size limit.
            offset: Page offset.

        Returns:
            List of Opportunity models.
        """
        sql = """
            SELECT id, company_id, research_profile_id, current_pain, business_impact,
                   automation_potential, recurring_revenue_potential, opportunity_score,
                   primary_opportunity, recommended_service, pitch_angle, tailored_value_proposition,
                   quick_win_offer, expected_business_value, estimated_initial_deal_size,
                   decision_maker_roles, buying_trigger, likely_objections, counter_position,
                   discovery_questions, recommended_first_contact, probability_of_success,
                   lead_status, priority, first_outreach_at, next_action, follow_up_cadence,
                   follow_up_notes, created_at, updated_at
            FROM opportunities WHERE 1=1
        """
        params: list[Any] = []

        if company_id is not None:
            sql += " AND company_id = ?"
            params.append(company_id)

        if lead_status:
            sql += " AND lead_status = ?"
            params.append(lead_status)

        if priority:
            sql += " AND priority = ?"
            params.append(priority)

        sql += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = self.database.execute(sql, params)
        return [Opportunity.from_row(row) for row in rows]

    def get_by_id(self, opportunity_id: int) -> Opportunity | None:
        """Fetch a single opportunity by primary key ID.

        Args:
            opportunity_id: Opportunity ID.

        Returns:
            Opportunity model or None.
        """
        sql = """
            SELECT id, company_id, research_profile_id, current_pain, business_impact,
                   automation_potential, recurring_revenue_potential, opportunity_score,
                   primary_opportunity, recommended_service, pitch_angle, tailored_value_proposition,
                   quick_win_offer, expected_business_value, estimated_initial_deal_size,
                   decision_maker_roles, buying_trigger, likely_objections, counter_position,
                   discovery_questions, recommended_first_contact, probability_of_success,
                   lead_status, priority, first_outreach_at, next_action, follow_up_cadence,
                   follow_up_notes, created_at, updated_at
            FROM opportunities WHERE id = ?
        """
        rows = self.database.execute(sql, [opportunity_id])
        if not rows:
            return None
        return Opportunity.from_row(rows[0])

    def create(self, opportunity: Opportunity) -> Opportunity:
        """Create a new opportunity record.

        Args:
            opportunity: Opportunity instance to persist.

        Returns:
            Opportunity model with generated ID.
        """
        sql = """
            INSERT INTO opportunities (
                company_id, research_profile_id, current_pain, business_impact,
                automation_potential, recurring_revenue_potential, opportunity_score,
                primary_opportunity, recommended_service, pitch_angle, tailored_value_proposition,
                quick_win_offer, expected_business_value, estimated_initial_deal_size,
                decision_maker_roles, buying_trigger, likely_objections, counter_position,
                discovery_questions, recommended_first_contact, probability_of_success,
                lead_status, priority, first_outreach_at, next_action, follow_up_cadence,
                follow_up_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [
            opportunity.company_id,
            opportunity.research_profile_id,
            opportunity.current_pain,
            opportunity.business_impact,
            opportunity.automation_potential,
            opportunity.recurring_revenue_potential,
            opportunity.opportunity_score,
            opportunity.primary_opportunity,
            opportunity.recommended_service,
            opportunity.pitch_angle,
            opportunity.tailored_value_proposition,
            opportunity.quick_win_offer,
            opportunity.expected_business_value,
            opportunity.estimated_initial_deal_size,
            opportunity.decision_maker_roles,
            opportunity.buying_trigger,
            opportunity.likely_objections,
            opportunity.counter_position,
            opportunity.discovery_questions,
            opportunity.recommended_first_contact,
            opportunity.probability_of_success,
            opportunity.lead_status or "New",
            opportunity.priority,
            opportunity.first_outreach_at,
            opportunity.next_action,
            opportunity.follow_up_cadence,
            opportunity.follow_up_notes,
        ]
        inserted = self.database.execute(sql, params)
        if inserted and "id" in inserted[0]:
            opportunity.id = inserted[0]["id"]
        return opportunity

    def update(self, opportunity: Opportunity) -> Opportunity | None:
        """Update an existing opportunity record.

        Args:
            opportunity: Opportunity model with updated fields.

        Returns:
            Updated Opportunity model or None.
        """
        if opportunity.id is None:
            return None

        sql = """
            UPDATE opportunities SET
                company_id = ?, research_profile_id = ?, current_pain = ?, business_impact = ?,
                automation_potential = ?, recurring_revenue_potential = ?, opportunity_score = ?,
                primary_opportunity = ?, recommended_service = ?, pitch_angle = ?,
                tailored_value_proposition = ?, quick_win_offer = ?, expected_business_value = ?,
                estimated_initial_deal_size = ?, decision_maker_roles = ?, buying_trigger = ?,
                likely_objections = ?, counter_position = ?, discovery_questions = ?,
                recommended_first_contact = ?, probability_of_success = ?, lead_status = ?,
                priority = ?, first_outreach_at = ?, next_action = ?, follow_up_cadence = ?,
                follow_up_notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        params = [
            opportunity.company_id,
            opportunity.research_profile_id,
            opportunity.current_pain,
            opportunity.business_impact,
            opportunity.automation_potential,
            opportunity.recurring_revenue_potential,
            opportunity.opportunity_score,
            opportunity.primary_opportunity,
            opportunity.recommended_service,
            opportunity.pitch_angle,
            opportunity.tailored_value_proposition,
            opportunity.quick_win_offer,
            opportunity.expected_business_value,
            opportunity.estimated_initial_deal_size,
            opportunity.decision_maker_roles,
            opportunity.buying_trigger,
            opportunity.likely_objections,
            opportunity.counter_position,
            opportunity.discovery_questions,
            opportunity.recommended_first_contact,
            opportunity.probability_of_success,
            opportunity.lead_status,
            opportunity.priority,
            opportunity.first_outreach_at,
            opportunity.next_action,
            opportunity.follow_up_cadence,
            opportunity.follow_up_notes,
            opportunity.id,
        ]
        self.database.execute(sql, params)
        return self.get_by_id(opportunity.id)

    def delete(self, opportunity_id: int) -> bool:
        """Delete opportunity by ID.

        Args:
            opportunity_id: Target ID.

        Returns:
            True if deletion was executed.
        """
        self.database.execute("DELETE FROM opportunities WHERE id = ?", [opportunity_id])
        return True
