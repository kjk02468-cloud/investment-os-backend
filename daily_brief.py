"""
Daily runner for cron / GitHub Actions.
  python daily_brief.py
Runs the integrated brief, then sweeps each holding's 6-condition health-check.
RISK verdicts trigger a Telegram alert from inside agent.thesis_check.
"""
import agent


def main():
    print("== 일일 브리프 ==")
    res = agent.daily_brief(notify=True)
    print(res["ts"])
    print(res["text"])
    if res.get("audit"):
        print("\n[감사노트]\n" + res["audit"])

    print("\n== Thesis 헬스체크 스윕 ==")
    for ticker in agent.HOLDINGS:
        try:
            r = agent.thesis_check(ticker, notify=True)
            flag = "⚠️ " + ",".join(r["risk_conditions"]) if r["risk_conditions"] else "ok"
            print(f"  {ticker}: {flag}")
        except Exception as e:  # noqa
            print(f"  {ticker}: error {e}")


if __name__ == "__main__":
    main()
