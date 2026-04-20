"""
审思明辨——智判法案双擎系统
得理开放平台服务
提供法律案例检索和法规检索API
"""
import requests
from typing import List, Dict, Any, Optional
from config import config
from loguru import logger


class DeliService:
    """得理开放平台服务类"""
    
    def __init__(self):
        self.app_id = config.DELILEGAL_APP_ID
        self.secret = config.DELILEGAL_SECRET
        self.api_base = config.DELILEGAL_API_BASE
    
    def _make_request(self, endpoint: str, data: dict) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        Args:
            endpoint: API端点
            data: 请求数据
            
        Returns:
            API响应
        """
        url = f"{self.api_base}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "appid": self.app_id,
            "secret": self.secret
        }
        
        try:
            logger.info(f"调用得理API: {endpoint}")
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            logger.debug(f"API响应: {result}")
            
            return result
            
        except requests.exceptions.Timeout:
            logger.error("得理API请求超时")
            return {"success": False, "error": "请求超时"}
        except requests.exceptions.RequestException as e:
            logger.error(f"得理API请求失败: {e}")
            return {"success": False, "error": str(e)}
    
    def search_cases(
        self,
        keyword: str,
        court_level: List[str] = None,
        case_year_start: int = None,
        case_year_end: int = None,
        judgement_type: List[str] = None,
        sort_field: str = "correlation",
        sort_order: str = "desc",
        page_no: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        检索相似案例
        
        API文档: https://open.delilegal.com/
        
        Args:
            keyword: 检索关键词（可以是法律问题、案情描述）
            court_level: 法院层级 ["0":最高院, "1":高院, "2":中院, "3":基层院]
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
        condition = {"keywordArr": [keyword]}
        
        if court_level:
            condition["courtLevelArr"] = court_level
        if case_year_start:
            condition["caseYearStart"] = case_year_start
        if case_year_end:
            condition["caseYearEnd"] = case_year_end
        if judgement_type:
            condition["judgementTypeArr"] = judgement_type
        
        payload = {
            "pageNo": page_no,
            "pageSize": page_size,
            "sortField": sort_field,
            "sortOrder": sort_order,
            "condition": condition
        }
        
        result = self._make_request("search/queryListCase", payload)
        
        if result.get("success"):
            return {
                "success": True,
                "total": result.get("body", {}).get("total", 0),
                "data": result.get("body", {}).get("dataList", [])
            }
        else:
            return {
                "success": False,
                "total": 0,
                "data": [],
                "error": result.get("msg", "检索失败")
            }
    
    def search_laws(
        self,
        keyword: str,
        search_type: str = "semantic",
        page_no: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        检索法规
        
        API文档: https://open.delilegal.com/
        
        Args:
            keyword: 检索关键词
            search_type: 检索方式 "title"(关键词) 或 "semantic"(语义)
            page_no: 页码
            page_size: 每页数量
            
        Returns:
            {
                "success": bool,
                "total": int,
                "data": List[dict]  # 法规列表
            }
        """
        payload = {
            "pageNo": page_no,
            "pageSize": page_size,
            "sortField": "correlation",
            "sortOrder": "desc",
            "condition": {
                "keywords": [keyword],
                "fieldName": search_type  # "title" 或 "semantic"
            }
        }
        
        result = self._make_request("search/queryListLaw", payload)
        
        if result.get("success"):
            return {
                "success": True,
                "total": result.get("body", {}).get("total", 0),
                "data": result.get("body", {}).get("dataList", [])
            }
        else:
            return {
                "success": False,
                "total": 0,
                "data": [],
                "error": result.get("msg", "检索失败")
            }
    
    def get_law_detail(self, law_id: str, merge: bool = True) -> Dict[str, Any]:
        """
        获取法规详情
        
        API文档: https://open.delilegal.com/
        
        Args:
            law_id: 法规ID（从法规检索列表获取）
            merge: 是否合并法规内容不作拆分
            
        Returns:
            {
                "success": bool,
                "data": dict  # 法规详情
            }
        """
        url = f"{self.api_base}/search/lawInfo"
        headers = {
            "Content-Type": "application/json",
            "appid": self.app_id,
            "secret": self.secret
        }
        params = {
            "lawId": law_id,
            "merge": str(merge).lower()
        }
        
        try:
            logger.info(f"获取法规详情: {law_id}")
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("success"):
                return {
                    "success": True,
                    "data": result.get("body", {})
                }
            else:
                return {
                    "success": False,
                    "error": result.get("msg", "获取详情失败")
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"获取法规详情失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_batch_law_details(self, law_ids: List[str]) -> List[Dict[str, Any]]:
        """
        批量获取法规详情
        
        Args:
            law_ids: 法规ID列表
            
        Returns:
            法规详情列表
        """
        results = []
        for law_id in law_ids:
            result = self.get_law_detail(law_id)
            if result["success"]:
                results.append(result["data"])
        return results


# 便捷函数
def search_legal_cases(keyword: str, page_size: int = 10) -> Dict[str, Any]:
    """便捷函数：检索法律案例"""
    service = DeliService()
    return service.search_cases(keyword, page_size=page_size)


def search_legal_laws(keyword: str, search_type: str = "semantic") -> Dict[str, Any]:
    """便捷函数：检索法律条文"""
    service = DeliService()
    return service.search_laws(keyword, search_type=search_type)
