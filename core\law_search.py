"""
审思明辨——智判法案双擎系统
法规检索模块
对接得理开放平台法规检索API
"""
from typing import List, Dict, Any, Optional
from services.deli_service import DeliService
from loguru import logger


class LawSearch:
    """法规检索类"""
    
    def __init__(self):
        self.deli_service = DeliService()
    
    def search(self, keyword: str, search_type: str = "semantic", 
               page_no: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        检索法规
        
        Args:
            keyword: 检索关键词
            search_type: 检索类型 "title"(关键词) 或 "semantic"(语义)
            page_no: 页码
            page_size: 每页数量
            
        Returns:
            {
                "success": bool,
                "total": int,
                "data": List[dict]  # 法规列表
            }
        """
        return self.deli_service.search_laws(
            keyword=keyword,
            search_type=search_type,
            page_no=page_no,
            page_size=page_size
        )
    
    def get_law_detail(self, law_id: str) -> Dict[str, Any]:
        """
        获取法规详情
        
        Args:
            law_id: 法规ID
            
        Returns:
            {
                "success": bool,
                "data": dict  # 法规详情
            }
        """
        return self.deli_service.get_law_detail(law_id)
    
    def search_by_category(self, category: str, page_size: int = 10) -> Dict[str, Any]:
        """
        按类别检索法规
        
        Args:
            category: 法规类别（如"合同法"、"劳动法"等）
            page_size: 返回数量
            
        Returns:
            法规列表
        """
        # 类别关键词映射
        category_keywords = {
            "民法典": "中华人民共和国民法典",
            "合同法": "合同法",
            "劳动法": "中华人民共和国劳动法",
            "刑法": "中华人民共和国刑法",
            "婚姻法": "婚姻法",
            "继承法": "继承法",
            "公司法": "公司法",
            "知识产权": "知识产权",
            "交通事故": "道路交通安全法",
            "工伤": "工伤保险条例"
        }
        
        keyword = category_keywords.get(category, category)
        return self.search(keyword, page_size=page_size)
    
    def build_rag_context(self, laws: List[Dict]) -> str:
        """
        构建RAG检索增强上下文
        
        Args:
            laws: 法规列表
            
        Returns:
            格式化的法规上下文字符串
        """
        if not laws:
            return ""
        
        context = "## 相关法律条文:\n\n"
        for i, law in enumerate(laws, 1):
            title = law.get("title", "未知标题")
            level = law.get("levelName", "")
            publisher = law.get("publisherName", "")
            active_date = law.get("activeDate", "")
            
            context += f"**{i}. {title}**\n"
            if level:
                context += f"- 层级: {level}\n"
            if publisher:
                context += f"- 发布机关: {publisher}\n"
            if active_date:
                context += f"- 生效日期: {active_date}\n"
            
            # 如果有详情内容
            if law.get("lawDetailContent"):
                content = law["lawDetailContent"]
                # 截取前500字
                if len(content) > 500:
                    content = content[:500] + "..."
                context += f"- 内容摘要: {content}\n"
            
            context += "\n"
        
        return context


# 便捷函数
def search_laws(keyword: str, search_type: str = "semantic") -> Dict[str, Any]:
    """便捷函数：检索法规"""
    searcher = LawSearch()
    return searcher.search(keyword, search_type)


def get_law_detail(law_id: str) -> Dict[str, Any]:
    """便捷函数：获取法规详情"""
    searcher = LawSearch()
    return searcher.get_law_detail(law_id)
