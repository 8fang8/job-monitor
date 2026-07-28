import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re

# ========== 招聘源配置区，可自行添加 ==========
SOURCES = [
    {
        "name": "贵州高校人才网",
        "url": "https://www.gxrcw.com/guizhou/",
        "type": "高校教职/行政"
    },
    {
        "name": "贵州事业单位招聘网",
        "url": "https://www.gzzzb.com/gy/",
        "type": "事业单位"
    },
    {
        "name": "贵阳国企招聘网",
        "url": "https://www.guizhourc.com/gy/gq/",
        "type": "国企"
    }
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extract_date(text, pattern):
    """通用日期提取"""
    match = re.search(pattern, text)
    return match.group(1) if match else ""

def fetch_single_source(source):
    """抓取单个招聘源的岗位列表"""
    job_list = []
    try:
        resp = requests.get(source["url"], headers=HEADERS, timeout=15)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 通用列表抓取：匹配所有带链接的列表项
        items = soup.select("li, .job-item, .list-item, tr")
        for item in items[:30]:
            try:
                title_tag = item.select_one("a[href]")
                if not title_tag:
                    continue
                    
                job_name = title_tag.get_text(strip=True)
                if len(job_name) < 4 or "招聘" not in job_name and "简章" not in job_name and "岗位" not in job_name:
                    continue
                
                apply_url = title_tag["href"]
                # 补全相对链接
                if apply_url.startswith("/"):
                    base_url = "/".join(source["url"].split("/")[:3])
                    apply_url = base_url + apply_url
                
                # 提取单位名称
                company_tag = item.select_one(".company, .unit, .dw")
                company = company_tag.get_text(strip=True) if company_tag else source["name"]
                
                # 提取发布日期、截止时间
                item_text = item.get_text()
                publish_date = extract_date(item_text, r"发布[:：]\s*(\d{4}-\d{2}-\d{2})")
                if not publish_date:
                    publish_date = extract_date(item_text, r"(\d{4}-\d{2}-\d{2})")
                if not publish_date:
                    publish_date = datetime.now().strftime("%Y-%m-%d")
                
                deadline = extract_date(item_text, r"截止[:：]\s*(\d{4}-\d{2}-\d{2})")
                
                job_list.append({
                    "岗位名称": job_name,
                    "公司/单位": company,
                    "投递网址": apply_url,
                    "发布日期": publish_date,
                    "网申截止时间": deadline,
                    "岗位类型": source["type"],
                    "抓取时间": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
            except Exception:
                continue
    except Exception as e:
        print(f"⚠️  抓取 {source['name']} 失败：{str(e)}")
    
    return job_list

def fetch_all_jobs():
    """抓取所有来源岗位，返回DataFrame"""
    all_jobs = []
    for src in SOURCES:
        jobs = fetch_single_source(src)
        all_jobs.extend(jobs)
        print(f"✅ {src['name']} 抓取到 {len(jobs)} 条岗位")
    
    df = pd.DataFrame(all_jobs)
    # 基础去重
    df = df.drop_duplicates(subset=["岗位名称", "公司/单位"], keep="last")
    return df.reset_index(drop=True)

if __name__ == "__main__":
    df = fetch_all_jobs()
    print(f"\n共抓取有效岗位：{len(df)} 条")
    print(df[["岗位名称", "公司/单位"]].head())
