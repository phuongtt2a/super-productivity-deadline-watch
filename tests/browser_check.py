#!/usr/bin/env python3
"""Browser checks using synthetic tasks only, never real user data."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/"plugin/index.html"
MOCK=r"""
const day=n=>{let d=new Date();d.setHours(12,0,0,0);d.setDate(d.getDate()+n);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,"0"),String(d.getDate()).padStart(2,"0")].join("-");};
window.__selected=null;
window.PluginAPI={
  getAppState:async()=>({
    projects:{p:{title:"Work"}},
    tasks:{
      overdue:{id:"overdue",title:"Overdue invoice",deadlineDay:day(-3),projectId:"p",isDone:false},
      today:{id:"today",title:"Due today",deadlineDay:day(0),projectId:"p",isDone:false},
      soon:{id:"soon",title:"Upcoming report",deadlineDay:day(2),projectId:"p",isDone:false},
      later:{id:"later",title:"Later task",deadlineDay:day(20),projectId:"p",isDone:false},
      scheduled:{id:"scheduled",title:"Scheduled only",dueDay:day(1),isDone:false},
      finished:{id:"finished",title:"Completed",deadlineDay:day(-5),isDone:true}
    },taskRepeatCfgs:{
      active:{id:"active",title:"Recurring activity",repeatUntilDay:day(5),isPaused:false},
      paused:{id:"paused",title:"Paused recurrence",repeatUntilDay:day(3),isPaused:true}
    }
  }),
  selectTask:async id=>{window.__selected=id;},
  registerHook:()=>{},Hooks:{TASK_UPDATE:"update",TASK_COMPLETE:"complete"}
};
"""
class BrowserTest(unittest.TestCase):
    def test_layout_navigation_and_separate_series(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            for width in (320,390,900,1200):
                page=browser.new_page(viewport={"width":width,"height":850},has_touch=width<500)
                page.add_init_script(MOCK)
                page.goto(HTML.as_uri())
                page.locator("#featured .featured-title").wait_for()
                self.assertEqual(page.locator("#featured .featured-title").inner_text(),"Overdue invoice")
                self.assertIn("Overdue",page.locator("#featured").inner_text())
                self.assertEqual(page.locator("#list .item").count(),3)
                self.assertEqual(page.locator("#series-list .series-row").count(),1)
                self.assertEqual(page.locator("#overdue-count").inner_text(),"1")
                self.assertEqual(page.locator("#total-count").inner_text(),"4")
                self.assertEqual(page.locator("text=Scheduled only").count(),0)
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"),width+1)
                page.locator("[data-task-id='overdue']").click()
                page.wait_for_function("window.__selected==='overdue'")
                page.locator("[data-task-id='today']").click()
                page.wait_for_function("window.__selected==='today'")
                page.close()
            browser.close()
if __name__=="__main__":
    unittest.main(verbosity=2)
