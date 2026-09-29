from src.agents_v2 import AgentRuntime, ROLE_PROMPTS

def test_specialized_roles_exist():
    expected={"TrendScout","OpportunityAnalyzer","ProductStrategist","ContentProducer","QAAgent","Optimizer"}
    assert expected.issubset(ROLE_PROMPTS)

def test_runtime_reports_provider_state():
    result=AgentRuntime().execute("test",{},agent="TrendScout")
    assert result["agent"]=="TrendScout"
    assert result["status"] in {"provider_not_configured","completed"}
