# Publishing to GitHub (run only when you decide to)

Nothing has been committed or pushed. The local repository has no commits and no remote.

```powershell
cd "D:\Project Internship\pathfinder-ai"
git status --short                      # check: no .env, outputs/, .venv/ or evaluations/snapshots* listed
git check-ignore .env outputs           # must print both
git add -A
git status --short | Select-String "\.env$"   # must print nothing
git commit -m "Pathfinder AI 3.2: decision-flip research agent, evaluations V1-V3.2"
# create an EMPTY repository on github.com (no README/licence), then:
git branch -M main
git remote add origin https://github.com/<YOUR-USER>/pathfinder-ai.git
git push -u origin main
```

After the push, the GitHub Actions workflow (`.github/workflows/ci.yml`) runs Ruff, the offline tests and the SYNTHETIC demo on Ubuntu with Python 3.11. No keys are needed.

To verify the published repository, do a fresh clone into a new folder and follow `docs/RELEASE_CHECKLIST.md` sections A and B.
