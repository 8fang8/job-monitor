from job_spider import fetch_all_jobs
from deduplicate import get_new_jobs
from alert import get_deadline_alert

def daily_task():
    print("=" * 50)
    print("📅 每日岗位更新任务启动")
    print("=" * 50)
    
    # 1. 抓取全量新岗位
    print("\n🔍 正在抓取招聘网站...")
    all_new = fetch_all_jobs()
    
    # 2. 去重，筛选今日新增
    print("\n🔄 正在去重处理...")
    new_only = get_new_jobs(all_new)
    
    # 3. 截止预警
    print("\n⏰ 正在计算截止预警...")
    alert_jobs = get_deadline_alert(7)
    
    # ========== 输出结果 ==========
    print("\n" + "=" * 50)
    print(f"✅ 今日新增岗位：{len(new_only)} 条")
    print("=" * 50)
    if len(new_only) > 0:
        print(new_only[["岗位名称", "公司/单位", "岗位类型", "投递网址"]].to_string(index=False))
    else:
        print("暂无新增岗位")
    
    print("\n" + "=" * 50)
    print(f"⚠️  7天内截止预警：{len(alert_jobs)} 条")
    print("=" * 50)
    if len(alert_jobs) > 0:
        print(alert_jobs.to_string(index=False))
    else:
        print("暂无即将截止的岗位")

if __name__ == "__main__":
    daily_task()
