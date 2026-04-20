"""
审思明辨——智判法案双擎系统
辅助工具函数
"""
import re
from typing import Dict, List, Any, Optional
from datetime import datetime


def format_legal_text(text: str, max_length: int = 500) -> str:
    """
    格式化法律文本，截断过长内容
    
    Args:
        text: 原始文本
        max_length: 最大长度
        
    Returns:
        格式化后的文本
    """
    if not text:
        return ""
    
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # 截断
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text


def parse_case_info(case_text: str) -> Dict[str, Any]:
    """
    解析案情文本，提取关键信息
    
    Args:
        case_text: 案情描述文本
        
    Returns:
        {
            "original_text": str,
            "key_entities": List[str],
            "case_type": str,
            "estimated_risk": str
        }
    """
    # 关键词匹配
    keywords = {
        "劳动争议": ["劳动", "工资", "加班", "解除合同", "工伤"],
        "合同纠纷": ["合同", "违约", "违约金", "解除", "履行"],
        "交通事故": ["交通事故", "撞", "赔偿", "保险", "责任"],
        "婚姻家庭": ["离婚", "抚养", "财产分割", "彩礼", "家暴"],
        "房产纠纷": ["房产", "房屋", "买卖", "拆迁", "物业"],
        "借贷纠纷": ["借款", "贷款", "利息", "逾期", "还款"],
        "知识产权": ["商标", "专利", "著作权", "侵权", "版权"],
        "医疗纠纷": ["医疗", "手术", "诊断", "赔偿", "医院"]
    }
    
    case_type = "其他"
    key_entities = []
    
    for category, words in keywords.items():
        for word in words:
            if word in case_text:
                key_entities.append(word)
                if case_type == "其他":
                    case_type = category
    
    return {
        "original_text": case_text,
        "key_entities": list(set(key_entities)),
        "case_type": case_type,
        "estimated_risk": "中"  # 默认风险等级
    }


def validate_case_description(case_text: str) -> Dict[str, Any]:
    """
    验证案情描述的完整性和规范性
    
    Args:
        case_text: 案情描述
        
    Returns:
        {
            "valid": bool,
            "suggestions": List[str],
            "completeness": float  # 0.0 - 1.0
        }
    """
    suggestions = []
    completeness = 0.5
    
    # 检查长度
    if len(case_text) < 20:
        suggestions.append("案情描述过短，建议提供更详细的案件信息")
        completeness -= 0.2
    elif len(case_text) > 5000:
        suggestions.append("案情描述较长，建议突出关键事实")
        completeness += 0.1
    else:
        completeness += 0.2
    
    # 检查是否包含关键要素
    key_elements = ["时间", "地点", "人物", "事件", "原因", "结果"]
    found_elements = sum(1 for e in key_elements if e in case_text)
    completeness += found_elements * 0.05
    
    # 检查问号
    if "？" not in case_text and "?" not in case_text:
        suggestions.append("建议明确您的法律问题或诉求")
    
    # 检查人物描述
    if not re.search(r'[甲乙丙丁】\u4e00-\u9fa5]{2,}', case_text):
        if "原告" not in case_text and "被告" not in case_text:
            suggestions.append("建议明确当事人身份（原告/被告）")
    
    completeness = min(1.0, max(0.0, completeness))
    
    return {
        "valid": completeness >= 0.5,
        "suggestions": suggestions,
        "completeness": completeness
    }


def format_case_list(cases: List[Dict]) -> str:
    """
    格式化案例列表为可读文本
    
    Args:
        cases: 案例列表
        
    Returns:
        格式化的文本
    """
    if not cases:
        return "暂无相关案例"
    
    result = []
    for i, case in enumerate(cases, 1):
        title = case.get("caseName", case.get("case_title", "未知案例"))
        court = case.get("court", case.get("courtName", ""))
        date = case.get("judgeDate", case.get("caseYear", ""))
        
        item = f"**{i}. {title}**"
        if court:
            item += f"\n   法院: {court}"
        if date:
            item += f"\n   日期: {date}"
        
        result.append(item)
    
    return "\n\n".join(result)


def format_law_list(laws: List[Dict]) -> str:
    """
    格式化法规列表为可读文本
    
    Args:
        laws: 法规列表
        
    Returns:
        格式化的文本
    """
    if not laws:
        return "暂无相关法规"
    
    result = []
    for i, law in enumerate(laws, 1):
        title = law.get("title", "未知法规")
        level = law.get("levelName", "")
        publisher = law.get("publisherName", "")
        
        item = f"**{i}. {title}**"
        if level:
            item += f"\n   层级: {level}"
        if publisher:
            item += f"\n   机关: {publisher}"
        
        result.append(item)
    
    return "\n\n".join(result)


def generate_timestamp() -> str:
    """生成当前时间戳"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        清理后的文件名
    """
    # 移除非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 移除前后空格
    filename = filename.strip()
    # 限制长度
    if len(filename) > 100:
        filename = filename[:100]
    return filename
