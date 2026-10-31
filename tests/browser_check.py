#!/usr/bin/env python3
"""Responsive Deadline Watch checks using synthetic tasks only."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
HTML=ROOT/"plugin/index.html"
MOCK=r"""
const day=n=>{let d=new Date();d.setHours(12,0,0,0);d.setDate(d.getDate()+n);return [d.getFullYear(),String(d.getMonth()+1).padStart(2,"0"),String(d.getDate()).padStart(2,"0")].join("-");};
window.__selected=null;
window.PluginAPI={
 getAppState:async()=>({
  projects:{p:{title:"Work"},q:{title:"Personal"}},
  tasks:{
   overdue:{id:"overdue",title:"Overdue invoice",deadlineDay:day(-3),projectId:"p",isDone:false},
   today:{id:"today",title:"Due today",deadlineDay:day(0),projectId:"p",isDone:false},
   soon:{id:"soon",title:"An intentionally very long report title with a Vietnamese project context to test wrapping trên màn hình nhỏ",deadlineDay:day(2),projectId:"p",isDone:false},
   later:{id:"later",title:"Later task",deadlineDay:day(20),projectId:"q",isDone:false},
   scheduled:{id:"scheduled",title:"Scheduled only",dueDay:day(1),isDone:false},
   finished:{id:"finished",title:"Completed",deadlineDay:day(-5),isDone:true}
  },
  taskRepeatCfgs:{
   active:{id:"active",title:"Recurring activity",repeatUntilDay:day(5),isPaused:false,projectId:"q"},
   paused:{id:"paused",title:"Paused recurrence",repeatUntilDay:day(3),isPaused:true}
  }
 }),
 selectTask:async id=>{window.__selected=id;},
 registerHook:()=>{},Hooks:{TASK_UPDATE:"update",TASK_COMPLETE:"complete"}
};
"""
class BrowserTest(unittest.TestCase):
 def test_neo_timeline_at_mobile_and_desktop_sizes(self):
  from playwright.sync_api import sync_playwright
  with sync_playwright() as p:
   browser=p.chromium.launch(headless=True)
   for width in (320,360,390,430,480,600,768,1024,1200):
    page=browser.new_page(viewport={"width":width,"height":850},has_touch=width<500)
    errors=[]
    page.on("pageerror",lambda err:errors.append(str(err)))
    page.add_init_script(MOCK)
    page.goto(HTML.as_uri())
    page.locator("#list .deadline-entry").first.wait_for()
    self.assertEqual(page.locator(".deadline-entry").count(),5)
    self.assertEqual(page.locator("#list .deadline-entry").first.locator(".entry-title").inner_text(),"Overdue invoice")
    self.assertEqual(page.locator("[data-entry-key='series:active']").count(),1)
    self.assertEqual(page.locator(".kind-series .entry-tag").inner_text(),"Repeats until")
    self.assertIn("days left",page.locator(".kind-series .entry-unit").inner_text())
    self.assertIn("Last repeat",page.locator(".kind-series .entry-date").inner_text())
    self.assertEqual(page.locator(".deadline-entry.rank-0").count(),1)
    self.assertEqual(page.locator(".deadline-entry.rank-1").count(),1)
    self.assertEqual(page.locator(".deadline-entry.rank-2").count(),1)
    self.assertEqual(page.locator("#overdue-count").inner_text(),"1")
    self.assertEqual(page.locator("#total-count").inner_text(),"5")
    self.assertEqual(page.locator(".intent-line").inner_text(),"All your important dates, in one place.")
    self.assertEqual(page.locator(".kind-task .entry-tag").first.inner_text(),"Task")
    self.assertEqual(page.locator(".kind-series .entry-tag").first.inner_text(),"Repeats until")
    self.assertTrue(page.locator(".entry-date").first.inner_text().startswith("Due"))
    self.assertEqual(page.locator("[data-entry-key='task:today'] .entry-number").inner_text(),"0")
    self.assertEqual(page.locator("[data-entry-key='task:today'] .entry-unit").inner_text(),"days left")
    self.assertEqual(page.locator("text=Scheduled only").count(),0)
    self.assertEqual(page.locator("text=Completed").count(),0)
    self.assertEqual(page.locator("text=On the horizon").count(),0)
    # Neubrutalism: crisp outlines, hard offset shadows, near-square corners.
    css=page.locator(".deadline-entry").first.evaluate("""e=>{
      const s=getComputedStyle(e);
      return {border:parseFloat(s.borderTopWidth),radius:parseFloat(s.borderTopLeftRadius),shadow:s.boxShadow,bg:s.backgroundColor}
    }""")
    self.assertGreaterEqual(css["border"],2,(width,css))
    self.assertLessEqual(css["radius"],6,(width,css))
    self.assertNotEqual(css["shadow"],"none",(width,css))
    self.assertNotIn("rgba(0, 0, 0, 0)",css["bg"])
    self.assertEqual(page.locator("text=Know what's coming.").count(),0)
    self.assertFalse(page.locator(".entry-action[data-task-id='']").count())
    sizes=page.locator(".entry-title").evaluate_all("(nodes)=>nodes.map(n=>parseFloat(getComputedStyle(n).fontSize))")
    self.assertGreater(sizes[0],sizes[1])
    self.assertGreater(sizes[1],sizes[2])
    self.assertGreater(sizes[2],sizes[3])
    # Nothing may extend past the mobile viewport, including very long titles.
    metrics=page.evaluate("""() => ({
      doc:document.documentElement.scrollWidth,
      viewport:innerWidth,
      cards:[...document.querySelectorAll('.deadline-entry')].map(e=>{
        const r=e.getBoundingClientRect();return {left:r.left,right:r.right,width:r.width}
      }),
      counters:[...document.querySelectorAll('.entry-countdown')].map(e=>e.getBoundingClientRect().right)
    })""")
    self.assertLessEqual(metrics["doc"],width+1,(width,metrics))
    self.assertLessEqual(page.locator(".summary-line").evaluate("e=>e.getBoundingClientRect().right"),width+1)
    for card in metrics["cards"]:
     self.assertGreaterEqual(card["left"],-1,(width,card))
     self.assertLessEqual(card["right"],width+1,(width,card))
    for right in metrics["counters"]:
     self.assertLessEqual(right,width+1,(width,right))
    gaps=page.locator(".deadline-entry").evaluate_all("nodes=>nodes.map(e=>e.querySelector('.entry-title').getBoundingClientRect().left-e.querySelector('.entry-index').getBoundingClientRect().right)")
    for gap in gaps:
     self.assertGreaterEqual(gap,7,(width,gap))
    page.locator("[data-task-id='overdue']").click()
    page.wait_for_function("window.__selected==='overdue'")
    page.locator("[data-task-id='today']").click()
    page.wait_for_function("window.__selected==='today'")
    self.assertEqual(errors,[],(width,errors))
    if width in (320,390,768,1200):
     screenshots=ROOT/"artifacts";screenshots.mkdir(exist_ok=True)
     page.screenshot(path=str(screenshots/("deadline-watch-"+str(width)+".png")),full_page=True)
    page.close()
   browser.close()

if __name__=="__main__":
 unittest.main(verbosity=2)
