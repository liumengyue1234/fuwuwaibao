"""
审思明辨——智判法案双擎系统
案例匹配模块
对接得理开放平台类案检索API
"""
from typing import List, Dict, Any, Optional
from services.deli_service import DeliService
from loguru import logger


class CaseMatching:
    """案例匹配类"""
    
    def __init__(self):
        self.deli_service = DeliService()
    
    def search(self, keyword: str, court_level: List[str] = None,
               case_year_start: int = None, case_year_end: int = None,
               judgement_type: List[str] = None,
               sort_field: str = "correlation", sort_order: str = "desc",
               page_no: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        检索相似案例
        
        Args:
            keyword: 检索关键词（可以是案情描述）
            court_level: 法院层级列表 ["0":最高院, "1":高院, "2":中院, "3":基层院]
            case_year_start: 案例裁判年份起始
            case_year_end: 案例裁判年份结束
            judgement_type: 文书类型 ["30":判决书, "31":裁决书, "32":调解书, "33":决定书]
            sort_field: 排序字段 "correlation"(相关性) 或 "time"(时间)
            sort_order: 排序方式 "asc" 或 "desc"
            page_no: 页码
            page_size: 每页数量
            
        Returns:
            {
                "success": bool,
                "total": int,
                "data": List[dict]  # 案例列表
            }
        """
        return self.deli_service.search_cases(
            keyword=keyword,
            court_level=court_level,
            case_year_start=case_year_start,
            case_year_end=case_year_end,
            judgement_type=judgement_type,
            sort_field=sort_field,
            sort_order=sort_order,
            page_no=page_no,
            page_size=page_size
        )
    
    def search_similar(self, case_description: str, page_size: int = 5) -> Dict[str, Any]:
        """
        语义检索相似案例（直接传入案情描述）
        
        Args:
            case_description: 案情描述
            page_size: 返回数量
            
        Returns:
            相似案例列表
        """
        return self.search(
            keyword=case_description,
            sort_field="correlation",
            sort_order="desc",
            page_size=page_size
        )
    
    def search_by_case_type(self, case_type: str, page_size: int = 10) -> Dict[str, Any]:
        """
        按案件类型检索
        
        Args:
            case_type: 案件类型
            page_size: 返回数量
            
        Returns:
            案例列表
        """
        # 案件类型关键词映射
        type_keywords = {
            "劳动争议": "劳动争议 劳动合同",
            "交通事故": "交通事故 机动车事故",
            "医疗纠纷": "医疗纠纷 医疗事故",
            "合同纠纷": "合同纠纷 违约",
            "婚姻家庭": "离婚 抚养权 财产分割",
            "房产纠纷": "房产 房屋买卖 拆迁",
            "借贷纠纷": "借贷 借款 民间借贷",
            "知识产权": "商标 专利 著作权",
            "刑事案件": "刑事 盗窃 诈骗",
            "行政诉讼": "行政诉讼 行政处罚"
        }
        
        keyword = type_keywords.get(case_type, case_type)
        return self.search(keyword, page_size=page_size)
    
    def build_rag_context(self, cases: List[Dict]) -> str:
        """
        构建RAG检索增强上下文
        
        Args:
            cases: 案例列表
            
        Returns:
            格式化的案例上下文字符串
        """
        if not cases:
            return ""
        
        context = "## 相关案例参考:\n\n"
        for i, case in enumerate(cases, 1):
            case_name = case.get("caseName", case.get("case_title", "未知案例"))
            court = case.get("court", case.get("courtName", ""))
            judge_date = case.get("judgeDate", case.get("caseYear", ""))
            case_type = case.get("caseType", case.get("judgementType", ""))
            reason = case.get("reason", case.get("caseReason", ""))
            result = case.get("result", case.get("judgementResult", ""))
            
            context += f"**案例 {i}: {case_name}**\n"
            if court:
                context += f"- 审理法院: {court}\n"
            if judge_date:
                context += f"- 裁判日期: {judge_date}\n"
            if reason:
                context += f"- 案由: {reason}\n"
            if result:
                # 截取结果摘要
                if len(result) > 300:
                    result = result[:300] + "..."
                context += f"- 裁判结果: {result}\n"
            context += "\n"
        
        return context
    
    def analyze_case_patterns(self, cases: List[Dict]) -> Dict[str, Any]:
        """
        分析案例模式
        
        Args:
            cases: 案例列表
            
        Returns:
            案例模式分析结果
        """
        patterns = {
            "total_count": len(cases),
            "courts": {},
            "case_types": {},
            "common_reasons": [],
            "win_rates": {"plaintiff": 0, "defendant": 0}
        }
        
        for case in cases:
            # 统计法院
            court = case.get("court", case.get("courtName", "未知"))
            if court in patterns["courts"]:
                patterns["courts"][court] += 1
            else:
                patterns["courts"][court] = 1
            
            # 统计案由
            reason = case.get("reason", case.get("caseReason", "其他"))
            if reason in patterns["case_types"]:
                patterns["case_types"][reason] += 1
            else:
                patterns["case_types"][reason] = 1
        
        # 排序
        patterns["courts"] = dict(sorted(
            patterns["courts"].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5])
        patterns["case_types"] = dict(sorted(
            patterns["case_types"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5])
        
        return patterns


# 便捷函数
def search_cases(keyword: str, page_size: int = 10) -> Dict[str, Any]:
    """便捷函数：检索相似案例"""
    matcher = CaseMatching()
    return matcher.search(keyword, page_size=page_size)


def find_similar_cases(case_description: str, page_size: int = 5) -> Dict[str, Any]:
    """便捷函数：查找相似案例"""
    matcher = CaseMatching()
    return matcher.search_similar(case_description, page_size)
