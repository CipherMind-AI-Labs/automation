"""Unit tests for single entry point launcher run.py."""

from unittest.mock import MagicMock, patch
import pytest

from run import create_agent_goal, display_summary
from apps.agents.base_agent.models import AgentGoal, AgentResult, AgentStatus
from apps.agents.lead_discovery_agent.models import LeadDiscoverySummary


def test_create_agent_goal() -> None:
    """Test create_agent_goal builds a valid AgentGoal."""
    prompt = "Find 10 contract furniture dealers in California"
    goal = create_agent_goal(prompt)

    assert isinstance(goal, AgentGoal)
    assert goal.description == prompt
    assert goal.goal_id.startswith("goal_lead_disc_")


def test_display_summary_successful(capsys: pytest.CaptureFixture[str]) -> None:
    """Test display_summary formats output correctly for successful results."""
    summary = LeadDiscoverySummary(
        companies_evaluated=3,
        companies_qualified=2,
        companies_rejected=1,
        companies_saved=2,
        evaluated_list=[],
        qualified_list=[],
        rejected_list=[],
        saved_list=[
            {"name": "CalWest Solutions", "website_url": "https://calwest.com", "industry": "Furniture"}
        ],
        rejection_reasons={"TechDesk": "Catalog required"},
        execution_statistics={"companies_evaluated": 3},
    )
    result = AgentResult(
        success=True,
        status=AgentStatus.SUCCESS,
        output=summary,
    )

    display_summary(result, elapsed_seconds=2.45)
    captured = capsys.readouterr().out

    assert "EXECUTION SUMMARY" in captured
    assert "Status:              SUCCESS" in captured
    assert "Elapsed Time:        2.45s" in captured
    assert "Companies Evaluated: 3" in captured
    assert "Companies Saved:     2" in captured
    assert "CalWest Solutions" in captured
    assert "TechDesk" in captured
