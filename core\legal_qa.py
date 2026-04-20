"""
审思明辨——智判法案双擎系统
法律智能问答模块
基于腾讯混元大模型和得理法律知识库
"""
import json
import requests
from typing import List, Dict, Optional, Any
from config import config
from loguru import logger


class LegalQA:
    """法律智能问答类"""
    
    def __init__(self):
        self.app_id = config.HUNYUAN_APP_ID
        self.app_key = config.HUNYUAN_APP_KEY
        self.api_url = config.HUNYUAN_API_URL
        self.max_history = config.MAX_HISTORY_LENGTH
        
    def chat(self, user_message: str, history: List[Dict] = None) -> Dict[str, Any]:
        """
        发送对话请求
        
        Args:
            user_message: 用户消息
            history: 对话历史 [{role: "user"/"assistant", content: str}]
            
        Returns:
            {
                "success": bool,
                "content": str,  # 回复内容
                "error": str    # 错误信息（如果有）
            }
        """
        if history is None:
            history = []
            
        # 构建消息列表
        messages = history.copy()
        messages.append({
            "role": "user",
            "content": [{"type": "text", "text": user_message}]
        })
        
        # 如果历史超过限制，截取最近的对话
        if len(messages) > self.max_history:
            messages = messages[-self.max_history:]
        
        payload = {
            "assistant_id": self.app_id,
            "user_id": "legal_user",
            "stream": False,
            "messages": messages
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.app_key}"
        }
        
        try:
            logger.info(f"发送问答请求: {user_message[:50]}...")
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("choices"):
                content = result["choices"][0]["message"]["content"]
                logger.info(f"问答回复成功，长度: {len(content)}")
                return {
                    "success": True,
                    "content": content
                }
            else:
                return {
                    "success": False,
                    "content": "",
                    "error": "未获取到有效回复"
                }
                
        except requests.exceptions.Timeout:
            logger.error("问答请求超时")
            return {
                "success": False,
                "content": "",
                "error": "请求超时，请稍后重试"
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"问答请求失败: {e}")
            return {
                "success": False,
                "content": "",
                "error": f"网络请求失败: {str(e)}"
            }
        except json.JSONDecodeError:
            logger.error("响应JSON解析失败")
            return {
                "success": False,
                "content": "",
                "error": "服务器响应格式错误"
            }
    
    def legal_consult(self, question: str, case_context: str = None) -> Dict[str, Any]:
        """
        法律咨询（增强版，带案例和法条上下文）
        
        Args:
            question: 法律问题
            case_context: 案情上下文（可选）
            
        Returns:
            包含法条引用和案例分析的回复
        """
        from services.deli_service import DeliService
        
        deli = DeliService()
        results = {"success": False, "content": "", "laws": [], "cases": []}
        
        # 1. 检索相关法条
        try:
            law_result = deli.search_laws(question, page_size=5)
            if law_result["success"]:
                results["laws"] = law_result["data"]
        except Exception as e:
            logger.warning(f"法条检索失败: {e}")
        
        # 2. 检索相关案例
        try:
            case_result = deli.search_cases(question, page_size=3)
            if case_result["success"]:
                results["cases"] = case_result["data"]
        except Exception as e:
            logger.warning(f"案例检索失败: {e}")
        
        # 3. 构建增强提示词
        enhanced_prompt = question
        if case_context:
            enhanced_prompt = f"案情: {case_context}\n\n问题: {question}"
        
        # 4. 调用大模型（带RAG增强）
        rag_context = ""
        if results["laws"] or results["cases"]:
            rag_context = "\n\n## 参考资料:\n"
            if results["laws"]:
                rag_context += "### 相关法规:\n"
                for i, law in enumerate(results["laws"], 1):
                    title = law.get("title", "")
                    if title:
                        rag_context += f"{i}. {title}\n"
            if results["cases"]:
                rag_context += "### 相关案例:\n"
                for i, case in enumerate(results["cases"], 1):
                    case_name = case.get("caseName", case.get("case_title", ""))
                    if case_name:
                        rag_context += f"{i}. {case_name}\n"
        
        full_prompt = enhanced_prompt + rag_context if rag_context else enhanced_prompt
        
        # 5. 调用大模型
        response = self.chat(full_prompt)
        results.update(response)
        
        return results


# 导出便捷函数
def legal_chat(message: str, history: List[Dict] = None) -> Dict[str, Any]:
    """便捷函数：法律问答"""
    qa = LegalQA()
    return qa.chat(message, history)


def legal_consult(question: str, case_context: str = None) -> Dict[str, Any]:
    """便捷函数：法律咨询（带RAG增强）"""
    qa = LegalQA()
    return qa.legal_consult(question, case_context)
