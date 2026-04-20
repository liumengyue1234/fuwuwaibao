"""
审思明辨——智判法案双擎系统
Streamlit 主应用
面向法律从业者的智能辅助平台
"""
import streamlit as st
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config
from core.legal_qa import LegalQA
from core.law_search import LawSearch
from core.case_matching import CaseMatching
from core.strategy import StrategyAnalysis
from services.tencent_doc import TencentDocService
from utils.helpers import format_legal_text, validate_case_description

# 页面配置
st.set_page_config(
    page_title="审思明辨 - 智判法案双擎系统",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1a365d;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #4a5568;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f7fafc;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #3182ce;
    }
    .result-box {
        background-color: #edf2f7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #c6f6d5;
        border-left: 4px solid #38a169;
        padding: 1rem;
        border-radius: 4px;
    }
    .warning-box {
        background-color: #fefcbf;
        border-left: 4px solid #d69e2e;
        padding: 1rem;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)


# 初始化会话状态
def init_session_state():
    """初始化会话状态"""
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "法律问答"
    if "search_results" not in st.session_state:
        st.session_state.search_results = {"laws": [], "cases": []}


init_session_state()


# 侧边栏
def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.markdown("## ⚖️ 功能导航")
        
        tabs = [
            "法律问答",
            "法条检索",
            "案例匹配",
            "诉讼策略"
        ]
        
        selected = st.radio(
            "选择功能",
            tabs,
            index=tabs.index(st.session_state.current_tab) if st.session_state.current_tab in tabs else 0
        )
        
        st.session_state.current_tab = selected
        
        st.markdown("---")
        
        # 竞赛信息
        st.markdown("### 🎯 参赛信息")
        st.markdown("""
        **赛道**: D06 - 腾讯开悟  
        **作品**: 审思明辨  
        **团队**: 服创赛D06赛道
        """)
        
        st.markdown("---")
        
        # 配置检查
        st.markdown("### ⚙️ 配置状态")
        cfg = config.check_config()
        if cfg["complete"]:
            st.success("✓ 配置完整")
        else:
            st.warning(f"⚠ 缺少: {', '.join(cfg['missing'][:2])}")
            st.info("请配置 .env 文件")


# 主页面头部
def render_header():
    """渲染页面头部"""
    st.markdown('<p class="main-header">⚖️ 审思明辨</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">智判法案双擎系统 · 法律从业者智能辅助平台</p>', unsafe_allow_html=True)
    
    # 四大核心能力
    cols = st.columns(4)
    features = [
        ("💬", "对话式问答", "自然语言咨询法律问题"),
        ("📖", "精准法条检索", "相关法规快速定位"),
        ("📋", "相似案例匹配", "类案裁判要旨分析"),
        ("🎯", "诉讼策略推演", "智能生成应诉方案")
    ]
    
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <h4>{icon} {title}</h4>
                <p style="color: #718096; font-size: 0.9rem;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)


# 法律问答模块
def render_legal_qa():
    """法律问答模块"""
    st.markdown("### 💬 法律智能问答")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        question = st.text_area(
            "请输入您的法律问题",
            placeholder="例如：劳动合同解除的经济补偿金如何计算？",
            height=100,
            key="qa_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        include_context = st.checkbox("包含案例/法条上下文", value=True)
        analyze = st.button("🔍 智能分析", type="primary", use_container_width=True)
    
    if analyze and question:
        with st.spinner("正在分析您的问题..."):
            qa = LegalQA()
            
            if include_context:
                result = qa.legal_consult(question)
            else:
                result = qa.chat(question)
            
            if result["success"]:
                # 显示相关法规
                if result.get("laws"):
                    with st.expander("📖 相关法规", expanded=True):
                        for i, law in enumerate(result["laws"][:5], 1):
                            title = law.get("title", "未知")
                            st.markdown(f"**{i}. {title}**")
                
                # 显示相关案例
                if result.get("cases"):
                    with st.expander("📋 相关案例", expanded=True):
                        for i, case in enumerate(result["cases"][:3], 1):
                            name = case.get("caseName", "未知")
                            st.markdown(f"**{i}. {name}**")
                
                # 显示回答
                st.markdown("#### 💡 智能回答")
                st.markdown(f'<div class="result-box">{result["content"]}</div>', unsafe_allow_html=True)
                
                # 保存到历史
                st.session_state.qa_history.append({
                    "question": question,
                    "answer": result["content"]
                })
            else:
                st.error(result.get("error", "分析失败"))
    
    # 问答历史
    if st.session_state.qa_history:
        with st.expander("📜 问答历史", expanded=False):
            for i, item in enumerate(reversed(st.session_state.qa_history[-5:])):
                st.markdown(f"**Q: {item['question'][:50]}...**")
                st.markdown(f"A: {item['answer'][:100]}...")
                st.markdown("---")


# 法条检索模块
def render_law_search():
    """法条检索模块"""
    st.markdown("### 📖 精准法条检索")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        keyword = st.text_input(
            "检索关键词",
            placeholder="输入法律问题或关键词，如：工伤保险、房屋买卖合同",
            key="law_search_input"
        )
    
    with col2:
        search_type = st.selectbox("检索方式", ["语义检索", "关键词检索"])
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        search = st.button("🔍 检索", type="primary", use_container_width=True)
    
    if search and keyword:
        with st.spinner("正在检索法规..."):
            law_search = LawSearch()
            stype = "semantic" if search_type == "语义检索" else "title"
            result = law_search.search(keyword, search_type=stype)
            
            if result["success"]:
                st.session_state.search_results["laws"] = result.get("data", [])
                
                st.success(f"找到 {result.get('total', 0)} 条相关法规")
                
                for i, law in enumerate(result.get("data", [])[:10], 1):
                    with st.expander(f"📜 {i}. {law.get('title', '未知标题')}", expanded=i<=3):
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                            st.markdown(f"**层级**: {law.get('levelName', '未知')}")
                            st.markdown(f"**机关**: {law.get('publisherName', '未知')}")
                        with col_info2:
                            st.markdown(f"**生效日期**: {law.get('activeDate', '未知')}")
                            st.markdown(f"**时效性**: {law.get('timelinessName', '未知')}")
                        
                        if law.get("lawDetailContent"):
                            st.markdown("**内容摘要**:")
                            st.markdown(format_legal_text(law["lawDetailContent"], 800))
            else:
                st.error("检索失败，请稍后重试")


# 案例匹配模块
def render_case_matching():
    """案例匹配模块"""
    st.markdown("### 📋 相似案例匹配")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        case_desc = st.text_area(
            "输入案情描述",
            placeholder="描述您的案件情况，例如：我在下班途中发生交通事故，公司不承认工伤...",
            height=120,
            key="case_input"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        court_level = st.multiselect(
            "法院层级",
            ["最高院", "高级法院", "中级法院", "基层法院"],
            default=["中级法院", "基层法院"]
        )
        match = st.button("🔍 匹配案例", type="primary", use_container_width=True)
    
    if match and case_desc:
        # 验证案情描述
        validation = validate_case_description(case_desc)
        
        if validation["suggestions"]:
            for suggestion in validation["suggestions"]:
                st.warning(suggestion)
        
        with st.spinner("正在匹配相似案例..."):
            matcher = CaseMatching()
            
            # 转换法院层级
            level_map = {"最高院": "0", "高级法院": "1", "中级法院": "2", "基层法院": "3"}
            court_level_codes = [level_map[c] for c in court_level if c in level_map]
            
            result = matcher.search(
                case_desc,
                court_level=court_level_codes if court_level_codes else None
            )
            
            if result["success"]:
                st.session_state.search_results["cases"] = result.get("data", [])
                
                st.success(f"找到 {result.get('total', 0)} 个相似案例")
                
                # 案例分析
                if result.get("data"):
                    patterns = matcher.analyze_case_patterns(result["data"])
                    st.markdown("#### 📊 案例分析")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("案例总数", patterns["total_count"])
                    with col2:
                        courts = list(patterns["courts"].keys())
                        st.metric("涉及法院", len(courts))
                    with col3:
                        st.metric("主要案由", list(patterns["case_types"].keys())[0] if patterns["case_types"] else "其他")
                
                # 案例列表
                for i, case in enumerate(result.get("data", [])[:10], 1):
                    with st.expander(f"⚖️ 案例 {i}: {case.get('caseName', case.get('case_title', '未知'))}", expanded=i<=3):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**法院**: {case.get('court', '未知')}")
                            st.markdown(f"**裁判日期**: {case.get('judgeDate', '未知')}")
                        with col2:
                            st.markdown(f"**案由**: {case.get('reason', '未知')}")
                            st.markdown(f"**文书类型**: {case.get('judgementType', '未知')}")
                        
                        result_text = case.get("result", case.get("judgementResult", ""))
                        if result_text:
                            st.markdown("**裁判结果**:")
                            st.markdown(format_legal_text(result_text, 300))
            else:
                st.error("案例匹配失败，请稍后重试")


# 诉讼策略模块
def render_strategy():
    """诉讼策略模块"""
    st.markdown("### 🎯 诉讼策略推演")
    st.markdown("*智能切换\"对方律师\"视角，生成质证意见与应诉策略*")
    
    tab1, tab2 = st.tabs(["📝 策略分析", "📄 报告导出"])
    
    with tab1:
        case_desc = st.text_area(
            "输入案件描述",
            placeholder="详细描述您的案件情况和立场...",
            height=150,
            key="strategy_case"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            client_role = st.radio("您的角色", ["原告", "被告"], horizontal=True)
        
        with col2:
            show_risk = st.checkbox("包含风险评估", value=True)
        
        analyze_btn = st.button("🎯 生成策略分析", type="primary", use_container_width=True)
        
        if analyze_btn and case_desc:
            with st.spinner("正在生成诉讼策略分析，请稍候..."):
                analyzer = StrategyAnalysis()
                result = analyzer.analyze_from_opposing_view(
                    case_desc,
                    client_role=client_role,
                    include_risk_analysis=show_risk
                )
                
                if result["success"]:
                    # 风险评估
                    if result.get("risk_analysis"):
                        st.markdown("#### ⚠️ 风险评估")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("胜诉概率", result["risk_analysis"].get("win_rate_estimate", "未知"))
                        with col2:
                            st.metric("风险等级", result["risk_analysis"].get("risk_level", "未知"))
                        with col3:
                            st.metric("参考案例", result["risk_analysis"].get("similar_case_count", 0))
                    
                    # 对方视角分析
                    st.markdown("#### 👁️ 对方视角分析")
                    st.markdown(result.get("opposing_view_analysis", "暂无分析"))
                    
                    # 完整报告
                    st.markdown("#### 📋 完整策略报告")
                    st.markdown(result.get("report", "暂无报告"))
                    
                    # 保存报告到session
                    st.session_state["current_report"] = result.get("report", "")
                else:
                    st.error(result.get("error", "分析失败"))
    
    with tab2:
        st.markdown("#### 📤 导出策略报告")
        st.info("将诉讼策略报告导出至腾讯文档，便于团队协作")
        
        if st.session_state.get("current_report"):
            if st.button("📤 一键导出到腾讯文档", use_container_width=True):
                with st.spinner("正在导出..."):
                    doc_service = TencentDocService()
                    export_result = doc_service.export_report_to_doc(
                        st.session_state["current_report"],
                        "诉讼策略分析报告"
                    )
                    
                    if export_result["success"]:
                        st.success(export_result["message"])
                        st.markdown(f"[打开文档]({export_result['doc_url']})")
                    else:
                        st.info("腾讯文档功能需要完整配置，请查看.env.example")
                        st.code("TENCENT_DOC_APP_ID=xxx\nTENCENT_DOC_SECRET=xxx")
        else:
            st.warning("请先在「策略分析」中生成报告")


# 主函数
def main():
    """主函数"""
    render_sidebar()
    render_header()
    
    # 根据当前选项卡渲染不同模块
    tab = st.session_state.current_tab
    
    if tab == "法律问答":
        render_legal_qa()
    elif tab == "法条检索":
        render_law_search()
    elif tab == "案例匹配":
        render_case_matching()
    elif tab == "诉讼策略":
        render_strategy()
    
    # 页脚
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #718096; font-size: 0.85rem;">
            <p>审思明辨——智判法案双擎系统 | 服创赛D06赛道参赛作品</p>
            <p>技术栈：腾讯混元大模型 · 得理开放平台 · 腾讯云向量数据库</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
