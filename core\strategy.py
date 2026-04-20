"""
审思明辨——智判法案双擎系统
诉讼策略分析模块
智能切换"对方律师"视角，生成质证意见、风险提示及诉讼策略报告
"""
from typing import List, Dict, Any, Optional
from core.legal_qa import LegalQA
from core.law_search import LawSearch
from core.case_matching import CaseMatching
from loguru import logger


class StrategyAnalysis:
    """诉讼策略分析类"""
    
    def __init__(self):
        self.legal_qa = LegalQA()
        self.law_search = LawSearch()
        self.case_matching = CaseMatching()
    
    def analyze_from_opposing_view(
        self, 
        case_description: str,
        client_role: str = "原告",
        include_risk_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        从对方律师视角分析案件
        
        Args:
            case_description: 案件描述
            client_role: 己方角色 ("原告" 或 "被告")
            include_risk_analysis: 是否包含风险分析
            
        Returns:
            {
                "success": bool,
                "opposing_view_analysis": str,    # 对方视角分析
                "cross_examination_points": List,   # 质证要点
                "risk_analysis": Dict,              # 风险分析
                "strategy_recommendations": List,   # 策略建议
                "report": str                       # 完整报告
            }
        """
        results = {
            "success": False,
            "case_description": case_description,
            "client_role": client_role,
            "opposing_view_analysis": "",
            "cross_examination_points": [],
            "risk_analysis": {},
            "strategy_recommendations": [],
            "report": ""
        }
        
        try:
            # 1. 检索相关法条
            law_result = self.law_search.search(case_description)
            results["related_laws"] = law_result.get("data", [])
            
            # 2. 检索相似案例
            case_result = self.case_matching.search_similar(case_description)
            results["similar_cases"] = case_result.get("data", [])
            
            # 3. 构建分析提示词
            opposing_role = "被告" if client_role == "原告" else "原告"
            
            analysis_prompt = f"""你是一位经验丰富的{opposing_role}律师。

## 案件背景
{case_description}

## 你的任务
请从{opposing_role}律师的角度，分析这个案件并给出应对策略。

## 分析维度
1. **对方主张预测**: 假设对方（{client_role}）可能提出的诉讼请求和理由
2. **己方抗辩要点**: 作为{opposing_role}，可以提出的抗辩理由和法律依据
3. **质证要点**: 针对对方可能提供的证据，指出可能的漏洞和质疑点
4. **风险提示**: 分析{opposing_role}面临的法律风险
5. **策略建议**: 提出对{opposing_role}有利的诉讼策略

## 输出格式
请用结构化的方式输出分析报告，包含上述五个维度的详细分析。"""

            # 4. 调用大模型分析
            response = self.legal_qa.chat(analysis_prompt)
            
            if response["success"]:
                results["success"] = True
                results["opposing_view_analysis"] = response["content"]
                
                # 5. 生成风险分析
                if include_risk_analysis:
                    results["risk_analysis"] = self._generate_risk_analysis(
                        case_description, client_role, results["similar_cases"]
                    )
                
                # 6. 生成完整报告
                results["report"] = self._generate_full_report(results)
            else:
                results["error"] = response.get("error", "分析失败")
                
        except Exception as e:
            logger.error(f"诉讼策略分析失败: {e}")
            results["error"] = str(e)
        
        return results
    
    def generate_cross_examination(self, case_description: str, evidence_list: List[str]) -> Dict[str, Any]:
        """
        生成质证意见
        
        Args:
            case_description: 案件描述
            evidence_list: 证据列表
            
        Returns:
            质证意见
        """
        evidence_text = "\n".join([f"{i+1}. {e}" for i, e in enumerate(evidence_list)])
        
        prompt = f"""你是一位经验丰富的律师，请针对以下证据生成质证意见。

## 案件背景
{case_description}

## 需要质证的证据
{evidence_text}

## 质证要求
请从证据的真实性、合法性、关联性三个维度进行分析：
1. **真实性质疑**: 证据是否真实？是否存在伪造可能？
2. **合法性质疑**: 证据的取得方式是否合法？取证程序是否存在瑕疵？
3. **关联性质疑**: 证据与案件事实是否有关联？证明力如何？

请给出每项证据的详细质证意见。"""
        
        response = self.legal_qa.chat(prompt)
        return response
    
    def generate_risk_report(self, case_description: str, client_position: str) -> Dict[str, Any]:
        """
        生成风险评估报告
        
        Args:
            case_description: 案件描述
            client_position: 当事人立场
            
        Returns:
            风险评估报告
        """
        prompt = f"""请对以下案件进行法律风险评估。

## 案件描述
{case_description}

## 当事人立场
{client_position}

## 风险评估维度
1. **败诉风险**: 分析可能的败诉因素
2. **赔偿风险**: 可能的赔偿范围和金额
3. **时间成本**: 诉讼周期预估
4. **执行风险**: 判决执行的可能性
5. **声誉风险**: 对当事人声誉的影响

请给出量化的风险评估（高/中/低）和详细分析。"""
        
        response = self.legal_qa.chat(prompt)
        
        return {
            "success": response["success"],
            "content": response.get("content", ""),
            "risk_level": self._estimate_risk_level(response.get("content", ""))
        }
    
    def _generate_risk_analysis(
        self, 
        case_description: str, 
        client_role: str,
        similar_cases: List[Dict]
    ) -> Dict[str, Any]:
        """内部方法：生成风险分析"""
        
        # 基于相似案例计算胜诉率
        favorable_count = 0
        for case in similar_cases:
            result = case.get("result", "").lower()
            # 简化判断逻辑
            if "驳回" in result and client_role == "原告":
                favorable_count += 0.5
            elif "支持" in result and client_role == "被告":
                favorable_count += 0.5
            elif "驳回" in result and client_role == "被告":
                favorable_count += 1
        
        if similar_cases:
            win_rate = favorable_count / len(similar_cases)
        else:
            win_rate = 0.5
        
        return {
            "win_rate_estimate": f"{win_rate:.1%}",
            "risk_level": "高" if win_rate < 0.3 else ("中" if win_rate < 0.6 else "低"),
            "similar_case_count": len(similar_cases)
        }
    
    def _estimate_risk_level(self, analysis_text: str) -> str:
        """内部方法：根据分析文本估算风险等级"""
        high_risk_keywords = ["高风险", "败诉", "不利", "严重", "重大损失"]
        low_risk_keywords = ["低风险", "有利", "胜诉", "支持", "可控"]
        
        high_count = sum(1 for k in high_risk_keywords if k in analysis_text)
        low_count = sum(1 for k in low_risk_keywords if k in analysis_text)
        
        if high_count > low_count:
            return "高"
        elif low_count > high_count:
            return "低"
        else:
            return "中"
    
    def _generate_full_report(self, analysis_data: Dict) -> str:
        """内部方法：生成完整策略报告"""
        
        report = f"""# 诉讼策略分析报告

## 案件概述
{analysis_data.get('case_description', '')}

## 当事人角色
{analysis_data.get('client_role', '')}

---

## 一、对方视角分析

{analysis_data.get('opposing_view_analysis', '')}

---

## 二、相关法律依据

"""
        
        laws = analysis_data.get("related_laws", [])
        if laws:
            for i, law in enumerate(laws[:5], 1):
                title = law.get("title", "未知")
                report += f"{i}. **{title}**\n"
        else:
            report += "暂未检索到相关法规\n"
        
        report += "\n## 三、相似案例参考\n\n"
        
        cases = analysis_data.get("similar_cases", [])
        if cases:
            for i, case in enumerate(cases[:3], 1):
                name = case.get("caseName", case.get("case_title", "未知案例"))
                result = case.get("result", case.get("judgementResult", ""))
                report += f"**案例 {i}: {name}**\n"
                if result:
                    report += f"裁判结果: {result[:200]}...\n"
                report += "\n"
        else:
            report += "暂未检索到相似案例\n"
        
        report += "\n## 四、风险评估\n\n"
        
        risk = analysis_data.get("risk_analysis", {})
        if risk:
            report += f"- 胜诉概率预估: {risk.get('win_rate_estimate', '未知')}\n"
            report += f"- 风险等级: {risk.get('risk_level', '未知')}\n"
            report += f"- 参考案例数: {risk.get('similar_case_count', 0)}\n"
        else:
            report += "暂无详细风险评估\n"
        
        return report


# 便捷函数
def analyze_strategy(case_description: str, client_role: str = "原告") -> Dict[str, Any]:
    """便捷函数：诉讼策略分析"""
    analyzer = StrategyAnalysis()
    return analyzer.analyze_from_opposing_view(case_description, client_role)


def generate_cross_examination(case_description: str, evidence_list: List[str]) -> Dict[str, Any]:
    """便捷函数：生成质证意见"""
    analyzer = StrategyAnalysis()
    return analyzer.generate_cross_examination(case_description, evidence_list)
