import json
from pathlib import Path
import subprocess
import unittest
import zipfile

ROOT=Path(__file__).resolve().parents[1]

class PluginTests(unittest.TestCase):
    def test_manifest(self):
        cfg=json.loads((ROOT/"plugin/manifest.json").read_text())
        self.assertEqual(cfg["id"],"sp-deadline-watch")
        self.assertEqual(cfg["version"],"1.0.0")
        self.assertTrue(cfg["iFrame"])
        self.assertEqual(cfg["permissions"],["getAppState","selectTask"])

    def test_script_syntax_and_fields(self):
        html=(ROOT/"plugin/index.html").read_text()
        script=html.split("<script>",1)[1].split("</script>",1)[0]
        result=subprocess.run(["node","--check"],input=script,text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
        for term in ("deadlineDay","deadlineWithTime","repeatUntilDay","getAppState()","selectTask(","BEGIN_CORE","END_CORE","Series ends","deadline-entry","entry-number","rank-0"):
            self.assertIn(term,html)
        self.assertIn("background:transparent!important",html)
        self.assertIn("width:min(1220px,100%)",html)
        self.assertNotIn("On the horizon",html)
        self.assertNotIn("Know what\u0027s coming.",html)
        self.assertNotIn("id=\"series-section\"",html)
        self.assertNotIn("deadlineDay:task.dueDay",html)

    def test_installable_zip(self):
        cmd=["python",str(ROOT/"scripts/package.py"),"--tag","v1.0.0"]
        subprocess.run(cmd,capture_output=True,check=True)
        zip_path=ROOT/"dist/deadline-watch-super-productivity.zip"
        before=zip_path.read_bytes()
        subprocess.run(cmd,capture_output=True,check=True)
        self.assertEqual(before,zip_path.read_bytes())
        with zipfile.ZipFile(zip_path) as z:
            self.assertEqual(z.namelist(),["manifest.json","plugin.js","index.html","icon.svg"])
            self.assertIsNone(z.testzip())

if __name__=="__main__":
    unittest.main(verbosity=2)
