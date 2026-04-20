"""
审思明辨——智判法案双擎系统
测试文件
"""
import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.legal_qa import LegalQA
from core.law_search import LawSearch
from core.case_matching import CaseMatching
from core.strategy import StrategyAnalysis
from utils.helpers import format_legal_text, parse_case_info, validate_case_description


class TestLegalQA:
    """法律问答测试"""
    
    def test_qa_initialization(self):
        """测试初始化"""
        qa = LegalQA()
        assert qa is not None
        assert hasattr(qa, 'chat')
        assert hasattr(qa, 'legal_consult')


class TestLawSearch:
    """法条检索测试"""
    
    def test_search_initialization(self):
        """测试初始化"""
        searcher = LawSearch()
        assert searcher is not None
        assert hasattr(searcher, 'search')
        assert hasattr(searcher, 'get_law_detail')


class TestCaseMatching:
    """案例匹配测试"""
    
    def test_matching_initialization(self):
        """测试初始化"""
        matcher = CaseMatching()
        assert matcher is not None
        assert hasattr(matcher, 'search')
        assert hasattr(matcher, 'search_similar')


class TestStrategyAnalysis:
    """策略分析测试"""
    
    def test_strategy_initialization(self):
        """测试初始化"""
        analyzer = StrategyAnalysis()
        assert analyzer is not None
        assert hasattr(analyzer, 'analyze_from_opposing_view')


class TestHelpers:
    """辅助函数测试"""
    
    def test_format_legal_text_short(self):
        """测试格式化短文本"""
        text = "这是一段测试文本"
        result = format_legal_text(text, max_length=500)
        assert result == text
    
    def test_format_legal_text_long(self):
        """测试格式化长文本"""
        text = "A" * 600
        result = format_legal_text(text, max_length=500)
        assert len(result) == 503  # 500 + "..."
        assert result.endswith("...")
    
    def test_format_legal_text_empty(self):
        """测试格式化空文本"""
        result = format_legal_text("", max_length=500)
        assert result == ""
    
    def test_parse_case_info_labor(self):
        """测试解析劳动争议案件"""
        text = "员工要求公司支付加班工资和解除合同的经济补偿金"
        result = parse_case_info(text)
        assert "加班" in result["key_entities"]
        assert "劳动争议" in result["case_type"]
    
    def test_parse_case_info_traffic(self):
        """测试解析交通事故案件"""
        text = "发生交通事故，对方车辆损坏，需要赔偿"
        result = parse_case_info(text)
        assert "交通事故" in result["key_entities"]
        assert "交通事故" in result["case_type"]
    
    def test_validate_case_description_short(self):
        """测试验证过短描述"""
        result = validate_case_description("测试")
        assert result["valid"] == False
        assert len(result["suggestions"]) > 0
    
    def test_validate_case_description_good(self):
        """测试验证完整描述"""
        text = """
        2023年5月1日，原告张三在下班途中被一辆汽车撞伤。
        地点：北京市朝阳区某路口
        人物：原告张三，被告李四（司机）
        事件：交通事故
        原因：被告闯红灯
        结果：原告受伤住院
        请问这算工伤吗？
        """
        result = validate_case_description(text)
        assert result["completeness"] >= 0.5
    
    def test_sanitize_filename(self):
        """测试文件名清理"""
        from utils.helpers import sanitize_filename
        filename = 'test<>:"/\\|?*.txt'
        result = sanitize_filename(filename)
        assert '<' not in result
        assert '>' not in result
        assert '|' not in result


class TestIntegration:
    """集成测试"""
    
    def test_module_imports(self):
        """测试模块导入"""
        from core import LegalQA, LawSearch, CaseMatching, StrategyAnalysis
        from services import DeliService, HunyuanService, TencentDocService
        from utils import format_legal_text, parse_case_info, validate_case_description
        
        assert LegalQA is not None
        assert LawSearch is not None
        assert CaseMatching is not None
        assert StrategyAnalysis is not None
    
    def test_config_loading(self):
        """测试配置加载"""
        from config import config
        assert config is not None
        assert hasattr(config, 'DELILEGAL_APP_ID')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
