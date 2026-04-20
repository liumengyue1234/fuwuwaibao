"""
审思明辨——智判法案双擎系统
腾讯混元大模型服务
通过腾讯元器智能体API调用
"""
import json
import requests
from typing import List, Dict, Any, Optional
from config import config
from loguru import logger


class HunyuanService:
    """腾讯混元大模型服务类"""
    
    def __init__(self):
        self.app_id = config.HUNYUAN_APP_ID
        self.app_key = config.HUNYUAN_APP_KEY
        self.api_url = config.HUNYUAN_API_URL
    
    def chat(
        self,
        message: str,
        user_id: str = "legal_user",
        stream: bool = False,
        history: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        发送对话请求
        
        Args:
            message: 用户消息
            user_id: 用户ID
            stream: 是否流式返回
            history: 对话历史
            
        Returns:
            {
                "success": bool,
                "content": str,
                "error": str
            }
        """
        # 构建消息列表
        messages = []
        if history:
            messages = history.copy()
        messages.append({
            "role": "user",
            "content": [{"type": "text", "text": message}]
        })
        
        # 截取历史
        if len(messages) > config.MAX_HISTORY_LENGTH:
            messages = messages[-config.MAX_HISTORY_LENGTH:]
        
        payload = {
            "assistant_id": self.app_id,
            "user_id": user_id,
            "stream": stream,
            "messages": messages
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.app_key}"
        }
        
        try:
            logger.info(f"调用混元API，用户: {user_id}")
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
                return {
                    "success": True,
                    "content": content,
                    "usage": result.get("usage", {})
                }
            else:
                return {
                    "success": False,
                    "content": "",
                    "error": "未获取到有效回复"
                }
                
        except requests.exceptions.Timeout:
            logger.error("混元API请求超时")
            return {
                "success": False,
                "content": "",
                "error": "请求超时，请稍后重试"
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"混元API请求失败: {e}")
            return {
                "success": False,
                "content": "",
                "error": f"网络请求失败: {str(e)}"
            }
    
    def chat_with_workflow(
        self,
        message: str,
        custom_variables: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """
        通过工作流发送对话请求
        
        Args:
            message: 用户消息
            custom_variables: 自定义变量（传递给工作流）
            
        Returns:
            {
                "success": bool,
                "content": str,
                "error": str
            }
        """
        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": message}]
            }
        ]
        
        payload = {
            "assistant_id": self.app_id,
            "user_id": "legal_workflow_user",
            "stream": False,
            "messages": messages
        }
        
        if custom_variables:
            payload["custom_variables"] = custom_variables
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.app_key}"
        }
        
        try:
            logger.info(f"调用混元工作流API")
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=90
            )
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("choices"):
                content = result["choices"][0]["message"]["content"]
                return {
                    "success": True,
                    "content": content,
                    "usage": result.get("usage", {})
                }
            else:
                return {
                    "success": False,
                    "content": "",
                    "error": "未获取到有效回复"
                }
                
        except Exception as e:
            logger.error(f"混元工作流API调用失败: {e}")
            return {
                "success": False,
                "content": "",
                "error": str(e)
            }


# 便捷函数
def chat(message: str, user_id: str = "legal_user") -> Dict[str, Any]:
    """便捷函数：对话"""
    service = HunyuanService()
    return service.chat(message, user_id)
