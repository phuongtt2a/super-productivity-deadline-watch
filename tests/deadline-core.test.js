const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const path=require("node:path");
const html=fs.readFileSync(path.join(__dirname,"../plugin/index.html"),"utf8");
const core=html.split("/* BEGIN_CORE */")[1].split("/* END_CORE */")[0];
assert.ok(core,"Pure helper region is missing");
const lib=vm.runInNewContext(core+";({localDay,parseDay,calendarNumber,dateInfo,calculateCountdown,buildEntries})");
const now=new Date(2026,9,31,14);
const day=n=>lib.localDay(new Date(2026,9,31+n,12));
assert.equal(day(0),"2026-10-31");
assert.equal(lib.parseDay("2026-02-30"),null);
assert.equal(lib.parseDay("invalid"),null);
assert.equal(lib.calendarNumber(lib.parseDay(day(1)))-lib.calendarNumber(now),1);
assert.equal(lib.dateInfo(day(0),null).timestamp,new Date(2026,9,31,23,59,59,999).getTime());
const early=new Date(2026,9,31,9).getTime();
assert.equal(lib.calculateCountdown(lib.dateInfo(null,early),now,"task").label,"Overdue today");
assert.equal(lib.calculateCountdown(lib.dateInfo(day(-2),null),now,"task").label,"Overdue · 2d");
assert.equal(lib.calculateCountdown(lib.dateInfo(day(0),null),now,"task").label,"Due today");
assert.equal(lib.calculateCountdown(lib.dateInfo(day(1),null),now,"task").label,"1 day left");
assert.equal(lib.calculateCountdown(lib.dateInfo(day(0),null),now,"series").label,"Series ends today");
const data={projects:{p:{title:"Work"}},tasks:{
  planned:{id:"planned",title:"Scheduled only",dueDay:day(0),isDone:false},
  done:{id:"done",title:"Finished",deadlineDay:day(-3),isDone:true},
  timed:{id:"timed",title:"Timed",deadlineWithTime:early,projectId:"p",isDone:false},
  allDay:{id:"allDay",title:"All day",deadlineDay:day(0),isDone:false},
  recurring:{id:"recurring",title:"Actual recurring instance",deadlineDay:day(2),repeatCfgId:"rule",isDone:false},
  subtask:{id:"subtask",title:"Child with deadline",parentId:"allDay",deadlineDay:day(5),isDone:false}
},taskRepeatCfgs:{
  rule:{id:"rule",title:"Series",repeatUntilDay:day(8),isPaused:false},
  paused:{id:"paused",title:"Paused",repeatUntilDay:day(2),isPaused:true},
  ended:{id:"ended",title:"Finished series",repeatUntilDay:day(-1),isPaused:false}
}};
const rows=lib.buildEntries(data,now);
assert.equal(rows.length,5);
assert.deepEqual(Array.from(rows,x=>x.key),["task:timed","task:allDay","task:recurring","task:subtask","series:rule"]);
assert.equal(rows[0].project,"Work");
assert.equal(rows[0].remaining.label,"Overdue today");
assert.equal(rows[2].isRecurring,true);
assert.equal(rows.filter(x=>x.kind==="series").length,1);
assert.equal(rows.some(x=>x.key==="task:planned"),false);
console.log("Deadline Watch core tests passed");
