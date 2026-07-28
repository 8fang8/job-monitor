import pandas as pd
from datetime import datetime, timedelta
from deduplicate import get_all_jobs

def get_deadline_alert(days=7):
    """
    返回days天内即将截止的岗位列表
    按剩余天数升序排列，越紧急越靠前
    """
    df = get_all_jobs()
    if df.empty:
        return pd.DataFrame()
    
    # 转换日期格式，无效值过滤
    df["网申截止时间"] = pd.to_datetime(df["网申截止时间"], errors="coerce")
    df = df[df["网申截止时间"].notna()]
    
    # 计算剩余天数
    now = datetime.now()
    threshold = now + timedelta(days=days)
    
    alert_df = df[
        (df["网申截止时间"] >= now) & 
        (df["网申截止时间"] <= threshold)
    ].copy()
    
    if alert_df.empty:
        return pd.DataFrame()
    
    alert_df["剩余天数"] = (alert_df["网申截止时间"] - now).dt.days
    alert_df = alert_df.sort_values("剩余天数", ascending=True)
    
    return alert_df[[
        "岗位名称", "公司/单位", "剩余天数", 
        "网申截止时间", "投递网址"
    ]].reset_index(drop=True)

if __name__ == "__main__":
    alert = get_deadline_alert(7)
    print(f"7天内截止岗位：{len(alert)} 条")
    print(alert)
