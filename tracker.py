import pandas as pd
import os
from datetime import datetime

TRACKER_FILE = "data/application.csv"
STATUS_OPTIONS = ["待投递", "已投递", "笔试", "面试", "淘汰", "Offer"]

def ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")

def init_tracker():
    """初始化台账文件"""
    ensure_data_dir()
    if not os.path.exists(TRACKER_FILE):
        df = pd.DataFrame(columns=[
            "岗位名称", "公司/单位", "投递网址", "当前状态",
            "标记时间", "备注"
        ])
        df.to_csv(TRACKER_FILE, index=False, encoding="utf-8-sig")

def add_job(job_name, company, url, status="待投递", remark=""):
    """添加岗位到投递台账"""
    init_tracker()
    df = pd.read_csv(TRACKER_FILE)
    
    # 避免重复添加
    if len(df) > 0 and job_name in df["岗位名称"].values:
        return "⚠️  该岗位已在台账中，可直接更新状态"
    
    new_row = {
        "岗位名称": job_name,
        "公司/单位": company,
        "投递网址": url,
        "当前状态": status,
        "标记时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "备注": remark
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(TRACKER_FILE, index=False, encoding="utf-8-sig")
    return f"✅ 已添加「{job_name}」，状态：{status}"

def update_status(job_keyword, new_status, remark=""):
    """更新岗位投递状态"""
    init_tracker()
    if new_status not in STATUS_OPTIONS:
        return f"❌ 无效状态，可选：{', '.join(STATUS_OPTIONS)}"
    
    df = pd.read_csv(TRACKER_FILE)
    mask = df["岗位名称"].str.contains(job_keyword, case=False, na=False)
    
    if mask.sum() == 0:
        return "❌ 未找到匹配的岗位"
    
    df.loc[mask, "当前状态"] = new_status
    df.loc[mask, "标记时间"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    if remark:
        df.loc[mask, "备注"] = remark
    
    df.to_csv(TRACKER_FILE, index=False, encoding="utf-8-sig")
    return f"✅ 已更新 {mask.sum()} 条岗位状态为「{new_status}」"

def get_tracker(status_filter=None):
    """查询投递台账，可按状态筛选"""
    init_tracker()
    df = pd.read_csv(TRACKER_FILE)
    if status_filter:
        df = df[df["当前状态"] == status_filter]
    return df

if __name__ == "__main__":
    print("当前投递台账：")
    print(get_tracker())
