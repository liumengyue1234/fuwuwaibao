"""
审思明辨——智判法案双擎系统
配置管理模块
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Config:
    """系统配置类"""
    
    # ============ 腾讯云配置 ============
    TC_SECRET_ID: Optional[str] = os.getenv("TC_SECRET_ID")
    TC_SECRET_KEY: Optional[str] = os.getenv("TC_SECRET_KEY")
    TC_REGION: str = os.getenv("TC_REGION", "ap-guangzhou")
    
    # ============ 腾讯混元大模型配置 ============
    HUNYUAN_APP_ID: Optional[str] = os.getenv("HUNYUAN_APP_ID")
    HUNYUAN_APP_KEY: Optional[str] = os.getenv("HUNYUAN_APP_KEY")
    HUNYUAN_API_URL: str = "https://yuanqi.tencent.com/openapi/v1/agent/chat/completions"
    
    # ============ 得理开放平台配置 ============
    DELILEGAL_APP_ID: str = os.getenv("DELILEGAL_APP_ID", "QthdBErlyaYvyXul")
    DELILEGAL_SECRET: str = os.getenv("DELILEGAL_SECRET", "EC5D455E6BD348CE8E18BE05926D2EBE")
    DELILEGAL_API_BASE: str = "https://openapi.delilegal.com/api/qa/v3"
    
    # ============ 腾讯文档配置 ============
    TENCENT_DOC_APP_ID: Optional[str] = os.getenv("TENCENT_DOC_APP_ID")
    TENCENT_DOC_SECRET: Optional[str] = os.getenv("TENCENT_DOC_SECRET")
    
    # ============ 应用配置 ============
    APP_PORT: int = int(os.getenv("APP_PORT", "8501"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
    MAX_HISTORY_LENGTH: int = int(os.getenv("MAX_HISTORY_LENGTH", "40"))
    
    @classmethod
    def check_config(cls) -> dict:
        """检查配置完整性"""
        missing = []
        if not cls.TC_SECRET_ID:
            missing.append("TC_SECRET_ID")
        if not cls.TC_SECRET_KEY:
            missing.append("TC_SECRET_KEY")
        if not cls.HUNYUAN_APP_ID:
            missing.append("HUNYUAN_APP_ID")
        if not cls.HUNYUAN_APP_KEY:
            missing.append("HUNYUAN_APP_KEY")
            
        return {
            "complete": len(missing) == 0,
            "missing": missing
        }


# 全局配置实例
config = Config()
