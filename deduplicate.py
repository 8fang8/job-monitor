import pandas as pd
import os

DATA_FILE = "data/all_jobs.csv"

def ensure_data_dir():
    if not os.path.exists("data"):
        os.makedirs("data")

def get_new_jobs(new_df):
    """
    输入新抓取的岗位DataFrame
    返回本次新增的岗位（即未在历史库中出现过的）
    """
    ensure_data_dir()
    
    # 生成唯一键
    new_df["唯一键"] = new_df["岗位名称"] + "_" + new_df["公司/单位"]
    
    if not os.path.exists(DATA_FILE):
        # 首次运行：全量保存，全部视为新增
        new_df.drop(columns=["唯一键"]).to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
        return new_df.drop(columns=["唯一键"])
    
    # 读取历史岗位库
    old_df = pd.read_csv(DATA_FILE)
    old_df["唯一键"] = old_df["岗位名称"] + "_" + old_df["公司/单位"]
    
    # 筛选新增岗位
    new_only = new_df[~new_df["唯一键"].isin(old_df["唯一键"])].copy()
    new_only = new_only.drop(columns=["唯一键"])
    
    # 合并更新全量库
    all_df = pd.concat([old_df.drop(columns=["唯一键"]), new_only], ignore_index=True)
    all_df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
    
    return new_only.reset_index(drop=True)

def get_all_jobs():
    """获取全量历史岗位"""
    ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    return pd.read_csv(DATA_FILE)
