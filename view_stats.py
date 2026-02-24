from database import SessionLocal, ProcessedAd, ScraperLog, ReferenceModel
from sqlalchemy import func, desc
from datetime import datetime, timedelta

def view_stats():
    db = SessionLocal()
    
    print("=" * 80)
    print("OLX PARSER STATISTICS")
    print("=" * 80)
    
    print("\n📊 DATABASE OVERVIEW")
    print("-" * 80)
    
    total_models = db.query(func.count(ReferenceModel.id)).scalar()
    active_models = db.query(func.count(ReferenceModel.id)).filter(ReferenceModel.active == True).scalar()
    print(f"Reference Models: {total_models} total, {active_models} active")
    
    total_ads = db.query(func.count(ProcessedAd.id)).scalar()
    print(f"Processed Ads: {total_ads}")
    
    total_logs = db.query(func.count(ScraperLog.id)).scalar()
    print(f"Scraper Runs: {total_logs}")
    
    print("\n💰 GOOD DEALS")
    print("-" * 80)
    
    good_deals = db.query(ProcessedAd).filter(
        ProcessedAd.discount_percent >= 20
    ).order_by(desc(ProcessedAd.discount_percent)).all()
    
    print(f"Total good deals found: {len(good_deals)}")
    
    if good_deals:
        print("\nTop 10 best deals:")
        for i, deal in enumerate(good_deals[:10], 1):
            model = db.query(ReferenceModel).filter(ReferenceModel.id == deal.matched_model_id).first()
            if model:
                print(f"\n{i}. {model.brand} {model.model_name}")
                print(f"   Price: {int(deal.price)} ₸ (base: {int(model.base_price)} ₸)")
                print(f"   Discount: {deal.discount_percent:.1f}%")
                print(f"   Savings: {int(model.base_price - deal.price)} ₸")
                print(f"   Date: {deal.first_seen.strftime('%Y-%m-%d %H:%M')}")
                print(f"   Notified: {'✓' if deal.notification_sent else '✗'}")
    
    print("\n\n📈 SCRAPER PERFORMANCE (Last 10 runs)")
    print("-" * 80)
    
    recent_logs = db.query(ScraperLog).order_by(desc(ScraperLog.timestamp)).limit(10).all()
    
    if recent_logs:
        for log in recent_logs:
            status_icon = "✓" if log.status == "success" else "✗"
            print(f"\n{status_icon} {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {log.category}")
            print(f"   Ads found: {log.ads_found}, New: {log.new_ads}, Deals: {log.good_deals}")
            if log.errors:
                print(f"   Errors: {log.errors[:100]}...")
    else:
        print("No scraper runs yet. Run: python main.py --once")
    
    print("\n\n📊 STATISTICS BY CATEGORY")
    print("-" * 80)
    
    category_stats = db.query(
        ProcessedAd.category,
        func.count(ProcessedAd.id).label('total'),
        func.sum(func.case((ProcessedAd.discount_percent >= 20, 1), else_=0)).label('deals')
    ).group_by(ProcessedAd.category).all()
    
    if category_stats:
        for cat, total, deals in category_stats:
            print(f"{cat}: {total} ads, {deals} deals")
    
    print("\n\n🔍 UNMATCHED ADS (Last 20)")
    print("-" * 80)
    
    unmatched = db.query(ProcessedAd).filter(
        ProcessedAd.matched_model_id == None
    ).order_by(desc(ProcessedAd.first_seen)).limit(20).all()
    
    if unmatched:
        print(f"Total unmatched: {len(unmatched)}")
        print("\nRecent unmatched ads:")
        for ad in unmatched[:10]:
            print(f"  - {ad.title} ({ad.price} ₸)")
    else:
        print("No unmatched ads!")
    
    print("\n" + "=" * 80)
    
    db.close()

if __name__ == '__main__':
    view_stats()
