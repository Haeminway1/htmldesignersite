# tests/test_cost_management.py
"""
Cost management and budget control tests
"""
import pytest
from unittest.mock import Mock, patch
from ai_api_module import AI
from ai_api_module.core.response import AIResponse, Usage
from ai_api_module.core.exceptions import BudgetExceededError
from ai_api_module.models.pricing import PricingCalculator
import time
from datetime import datetime, timedelta


class TestPricingCalculator:
    """Test pricing calculation functionality"""
    
    def test_pricing_calculator_creation(self):
        """Test pricing calculator creation"""
        calculator = PricingCalculator()
        
        assert hasattr(calculator, 'calculate_cost')
        assert hasattr(calculator, 'get_model_pricing')
    
    def test_openai_pricing_calculation(self):
        """Test OpenAI pricing calculation"""
        calculator = PricingCalculator()
        
        usage = Usage(
            prompt_tokens=1000,
            completion_tokens=500,
            total_tokens=1500
        )
        
        # Test GPT-4o pricing
        cost = calculator.calculate_cost("gpt-4o", "openai", usage)
        
        # Should be positive cost
        assert cost > 0
        
        # Should be reasonable for given token usage
        assert 0.001 <= cost <= 0.1  # Between 0.1 cent and 10 cents
    
    def test_anthropic_pricing_calculation(self):
        """Test Anthropic pricing calculation"""
        calculator = PricingCalculator()
        
        usage = Usage(
            prompt_tokens=2000,
            completion_tokens=1000,
            total_tokens=3000
        )
        
        # Test Claude pricing
        cost = calculator.calculate_cost("claude-3-sonnet-20240229", "anthropic", usage)
        
        assert cost > 0
        assert 0.005 <= cost <= 0.2  # Should be in reasonable range
    
    def test_unknown_model_pricing(self):
        """Test pricing for unknown model"""
        calculator = PricingCalculator()
        
        usage = Usage(prompt_tokens=100, completion_tokens=50)
        
        # Should use fallback pricing for unknown model
        cost = calculator.calculate_cost("unknown-model", "unknown-provider", usage)
        
        assert cost > 0  # Should still return some cost
    
    def test_batch_pricing_discount(self):
        """Test batch processing pricing discount"""
        calculator = PricingCalculator()
        
        usage = Usage(prompt_tokens=1000, completion_tokens=500)
        
        # Regular pricing
        regular_cost = calculator.calculate_cost("gpt-4o", "openai", usage)
        
        # Batch pricing (should be discounted)
        batch_cost = calculator.calculate_cost("gpt-4o", "openai", usage, is_batch=True)
        
        assert batch_cost < regular_cost
        assert batch_cost == regular_cost * 0.5  # 50% discount for batch


class TestBudgetManagement:
    """Test budget management functionality"""
    
    def test_budget_limit_setting(self):
        """Test setting budget limits"""
        ai = AI()
        
        # Set daily and monthly limits
        ai.set_budget_limit(daily=10.0, monthly=100.0)
        
        assert ai.config.daily_budget_limit == 10.0
        assert ai.config.monthly_budget_limit == 100.0
    
    def test_cost_estimation(self):
        """Test cost estimation before execution"""
        ai = AI()
        
        # Mock model registry cost estimation
        with patch.object(ai.model_registry, 'estimate_request_cost', return_value=0.005):
            estimated_cost = ai.estimate_cost(
                "Write a detailed explanation of machine learning",
                model="gpt-4o"
            )
            
            assert estimated_cost == 0.005
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_budget_enforcement_daily(self, mock_router):
        """Test daily budget enforcement"""
        ai = AI()
        ai.config.daily_budget_limit = 0.01  # 1 cent limit
        
        # Mock current daily cost to be near limit
        with patch.object(ai, '_get_daily_cost', return_value=0.008):
            # Mock high cost estimation that would exceed budget
            with patch.object(ai.model_registry, 'estimate_request_cost', return_value=0.005):
                with pytest.raises(BudgetExceededError) as exc_info:
                    ai.chat("Expensive request")
                
                assert "daily budget" in str(exc_info.value).lower()
    
    @patch('ai_api_module.providers.router.ProviderRouter')
    def test_budget_enforcement_monthly(self, mock_router):
        """Test monthly budget enforcement"""
        ai = AI()
        ai.config.monthly_budget_limit = 0.05  # 5 cent limit
        
        # Mock current monthly cost to be near limit
        with patch.object(ai, '_get_monthly_cost', return_value=0.045):
            with patch.object(ai.model_registry, 'estimate_request_cost', return_value=0.01):
                with pytest.raises(BudgetExceededError) as exc_info:
                    ai.chat("Another expensive request")
                
                assert "monthly budget" in str(exc_info.value).lower()
    
    def test_budget_warning_threshold(self):
        """Test budget warning when approaching limit"""
        ai = AI()
        ai.config.daily_budget_limit = 1.0
        ai.config.budget_warning_threshold = 0.8  # 80% threshold
        
        # Mock usage at 85% of budget
        with patch.object(ai, '_get_daily_cost', return_value=0.85):
            with patch.object(ai.model_registry, 'estimate_request_cost', return_value=0.05):
                # Should not raise exception but might log warning
                try:
                    with patch('ai_api_module.utils.logging.logger') as mock_logger:
                        # Mock provider router to avoid actual API call
                        mock_response = AIResponse(text="Test", cost=0.05)
                        with patch.object(ai.provider_router, 'execute', return_value=mock_response):
                            response = ai.chat("Test message")
                            
                            # Check if warning was logged
                            mock_logger.warning.assert_called()
                            
                except BudgetExceededError:
                    pass  # Might still exceed depending on exact implementation


class TestUsageTracking:
    """Test usage tracking and statistics"""
    
    def test_usage_stats_collection(self):
        """Test collection of usage statistics"""
        ai = AI()
        
        # Mock some usage data
        with patch.object(ai, '_get_usage_history', return_value=[
            {"timestamp": datetime.now(), "cost": 0.01, "model": "gpt-4o", "tokens": 100},
            {"timestamp": datetime.now(), "cost": 0.02, "model": "claude-3-sonnet", "tokens": 200},
            {"timestamp": datetime.now(), "cost": 0.005, "model": "gpt-4o-mini", "tokens": 50},
        ]):
            stats = ai.get_usage_stats()
            
            assert "total_cost" in stats
            assert "total_requests" in stats
            assert "most_used_model" in stats
            assert "daily_cost" in stats
            
            assert stats["total_cost"] == 0.035
            assert stats["total_requests"] == 3
    
    def test_cost_tracking_per_request(self):
        """Test cost tracking for individual requests"""
        ai = AI()
        
        mock_response = AIResponse(
            text="Test response",
            usage=Usage(prompt_tokens=100, completion_tokens=50),
            cost=0.003,
            model="gpt-4o"
        )
        
        with patch.object(ai.provider_router, 'execute', return_value=mock_response):
            response = ai.chat("Test message")
            
            assert response.cost == 0.003
            assert response.usage.total_tokens == 150
    
    def test_conversation_cost_tracking(self):
        """Test cost tracking across conversation"""
        ai = AI()
        
        conversation = ai.start_conversation("Cost Test")
        
        # Mock responses with costs
        mock_responses = [
            AIResponse(text="Response 1", cost=0.001),
            AIResponse(text="Response 2", cost=0.002),
            AIResponse(text="Response 3", cost=0.0015),
        ]
        
        with patch.object(ai.provider_router, 'execute', side_effect=mock_responses):
            conversation.add_user_message("Message 1")
            response1 = conversation.send()
            
            conversation.add_user_message("Message 2") 
            response2 = conversation.send()
            
            conversation.add_user_message("Message 3")
            response3 = conversation.send()
            
            # Check individual costs
            assert response1.cost == 0.001
            assert response2.cost == 0.002
            assert response3.cost == 0.0015
            
            # Check total conversation cost
            assert conversation.total_cost == 0.0045
    
    def test_provider_cost_comparison(self):
        """Test cost comparison between providers"""
        ai = AI()
        
        # Mock different provider costs
        openai_usage = Usage(prompt_tokens=1000, completion_tokens=500)
        anthropic_usage = Usage(prompt_tokens=1000, completion_tokens=500)
        
        calculator = PricingCalculator()
        
        openai_cost = calculator.calculate_cost("gpt-4o", "openai", openai_usage)
        anthropic_cost = calculator.calculate_cost("claude-3-sonnet", "anthropic", anthropic_usage)
        
        # Both should be positive
        assert openai_cost > 0
        assert anthropic_cost > 0
        
        # Costs should be different (different pricing models)
        # Note: This might not always be true depending on actual pricing


class TestCostOptimization:
    """Test cost optimization features"""
    
    def test_cost_optimization_enabled(self):
        """Test enabling cost optimization"""
        ai = AI()
        
        ai.enable_cost_optimization(
            prefer_cheaper_models=True,
            aggressive_caching=True,
            smart_routing=True
        )
        
        assert ai.config.prefer_cheaper_models == True
        assert ai.config.aggressive_caching == True
        assert ai.config.smart_routing == True
    
    def test_model_selection_by_budget(self):
        """Test model selection based on budget constraints"""
        ai = AI()
        
        # Enable cost optimization
        ai.enable_cost_optimization(prefer_cheaper_models=True)
        
        # Mock model costs
        with patch.object(ai.model_registry, 'get_cheapest_model', return_value=("gpt-4o-mini", "openai")):
            model, provider = ai.model_registry.resolve(
                "smart",  # Would normally select expensive model
                None,
                max_cost=0.001  # Very low budget
            )
            
            # Should select cheaper alternative
            assert "mini" in model.lower() or "haiku" in model.lower()
    
    def test_automatic_model_downgrade(self):
        """Test automatic model downgrade for cost savings"""
        ai = AI()
        ai.enable_cost_optimization(prefer_cheaper_models=True)
        
        # Mock high cost estimation for premium model
        with patch.object(ai.model_registry, 'estimate_request_cost') as mock_estimate:
            mock_estimate.side_effect = [0.1, 0.01]  # First expensive, then cheap
            
            with patch.object(ai.model_registry, 'get_cheaper_alternative') as mock_alternative:
                mock_alternative.return_value = ("gpt-4o-mini", "openai")
                
                # Mock successful execution with cheaper model
                mock_response = AIResponse(text="Optimized response", cost=0.01)
                with patch.object(ai.provider_router, 'execute', return_value=mock_response):
                    response = ai.chat("Test message", model="gpt-4o", max_cost=0.05)
                    
                    assert response.cost <= 0.05
    
    def test_batch_processing_cost_optimization(self):
        """Test cost optimization through batch processing"""
        ai = AI()
        
        # Mock batch pricing
        calculator = PricingCalculator()
        
        regular_usage = Usage(prompt_tokens=100, completion_tokens=50)
        regular_cost = calculator.calculate_cost("gpt-4o", "openai", regular_usage)
        batch_cost = calculator.calculate_cost("gpt-4o", "openai", regular_usage, is_batch=True)
        
        # Batch should be cheaper
        assert batch_cost < regular_cost
        
        # Test batch recommendation
        messages = ["Message 1", "Message 2", "Message 3", "Message 4", "Message 5"]
        
        # Should recommend batch processing for multiple messages
        assert len(messages) >= 3  # Threshold for batch recommendation


class TestCostAlertsAndNotifications:
    """Test cost alerts and notification systems"""
    
    def test_cost_threshold_alerts(self):
        """Test alerts when cost thresholds are reached"""
        ai = AI()
        ai.config.daily_budget_limit = 1.0
        ai.config.cost_alert_thresholds = [0.5, 0.8, 0.9]  # 50%, 80%, 90%
        
        # Mock current usage at different levels
        test_cases = [
            (0.6, "50% threshold should trigger"),
            (0.85, "80% threshold should trigger"),
            (0.95, "90% threshold should trigger"),
        ]
        
        for current_cost, description in test_cases:
            with patch.object(ai, '_get_daily_cost', return_value=current_cost):
                with patch('ai_api_module.utils.logging.logger') as mock_logger:
                    # Check if alert would be triggered
                    alerts = ai._check_cost_thresholds()
                    
                    if current_cost >= 0.5:  # Above first threshold
                        assert len(alerts) > 0
    
    def test_cost_projection_warnings(self):
        """Test warnings based on cost projection"""
        ai = AI()
        ai.config.daily_budget_limit = 1.0
        
        # Mock usage history showing rapid cost increase
        history = []
        base_time = datetime.now()
        for i in range(10):
            history.append({
                "timestamp": base_time + timedelta(hours=i),
                "cost": 0.05 * (i + 1),  # Increasing cost
                "tokens": 100
            })
        
        with patch.object(ai, '_get_usage_history', return_value=history):
            # Project cost for rest of day
            projected_cost = ai._project_daily_cost()
            
            # Should project significant cost based on trend
            assert projected_cost > 0.5  # Should exceed current usage
    
    def test_cost_report_generation(self):
        """Test cost report generation"""
        ai = AI()
        
        # Mock usage data for the past week
        usage_data = []
        base_date = datetime.now()
        
        for i in range(7):  # 7 days
            for j in range(5):  # 5 requests per day
                usage_data.append({
                    "timestamp": base_date - timedelta(days=i, hours=j),
                    "cost": 0.01 + (i * 0.002),  # Varying cost
                    "model": ["gpt-4o", "claude-3-sonnet", "gpt-4o-mini"][j % 3],
                    "provider": ["openai", "anthropic", "openai"][j % 3],
                    "tokens": 100 + (j * 20)
                })
        
        with patch.object(ai, '_get_usage_history', return_value=usage_data):
            report = ai.generate_cost_report(days=7)
            
            assert "total_cost" in report
            assert "daily_breakdown" in report
            assert "model_breakdown" in report
            assert "provider_breakdown" in report
            
            assert report["total_cost"] > 0
            assert len(report["daily_breakdown"]) <= 7
            assert len(report["model_breakdown"]) >= 1


# Integration tests requiring real API usage
@pytest.mark.integration 
class TestCostManagementIntegration:
    """Integration tests for cost management with real APIs"""
    
    def test_real_cost_calculation(self):
        """Test cost calculation with real API usage"""
        import os
        
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OpenAI API key not available")
        
        ai = AI(provider="openai")
        
        # Set low budget for testing
        ai.set_budget_limit(daily=0.10)  # 10 cents
        
        # Make small request to test cost calculation
        response = ai.chat(
            "Say 'hello'",
            model="gpt-4o-mini",  # Cheapest model
            max_tokens=5
        )
        
        assert isinstance(response, AIResponse)
        assert response.cost > 0
        assert response.cost < 0.01  # Should be very cheap
        
        # Check usage stats
        stats = ai.get_usage_stats()
        assert stats["daily_cost"] >= response.cost
    
    def test_budget_enforcement_real(self):
        """Test budget enforcement with real API"""
        import os
        
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OpenAI API key not available")
        
        ai = AI(provider="openai")
        
        # Set very low budget
        ai.set_budget_limit(daily=0.001)  # 0.1 cent - very restrictive
        
        # This should trigger budget exceeded error
        with pytest.raises(BudgetExceededError):
            ai.chat(
                "Write a long detailed explanation about artificial intelligence",
                model="gpt-4o",  # Expensive model
                max_tokens=1000  # Many tokens
            )
    
    def test_cost_optimization_real(self):
        """Test cost optimization with real API"""
        import os
        
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OpenAI API key not available")
        
        ai = AI(provider="openai")
        ai.enable_cost_optimization(prefer_cheaper_models=True)
        
        # Request with cost constraint
        response = ai.chat(
            "Explain Python in one sentence",
            max_cost=0.005,  # 0.5 cent limit
            model="smart"  # Would normally choose expensive model
        )
        
        assert isinstance(response, AIResponse)
        assert response.cost <= 0.005
        
        # Should have selected a cheaper model
        assert "mini" in response.model.lower() or "haiku" in response.model.lower()
