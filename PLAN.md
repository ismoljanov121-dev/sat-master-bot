# Learning platform upgrade

Branch `feature/learning-platform`, developed in the `sat-master-bot-dev` worktree.
Merging to `main` deploys to production (Render auto-deploy), so that step waits for Otabek's approval.

Real Listening audio (idea 1) was built separately on `feat/listening-mp3-audio` and is merged here.

## Definition of done

- The bot records users, and the Mini App saves results to a database behind `initData` auth.
- SAT mocks are adaptive and follow the official blueprint, with Math formulas, grid-in questions,
  figures and exam tools.
- Students get a score report, short practice sets, a mistake notebook, a diagnostic, a daily plan,
  reminders and a weekly report.
- IELTS Writing has AI feedback through Gemini.
- The channel posts without repeats, and results can be shared.
- Learning centers have a working panel, and the sales docs describe only what exists.
- Tests and CI pass on SQLite and Postgres, on the Python version Render uses.

## Stages

- [x] 1. Cleanup: real `handlers` package, remove dead code, config, tests, CI (idea 3)
- [x] 2. Database and `/api/v1` with `initData` auth (idea 2)
- [x] 3. Content: normalized bank, LaTeX, grid-in, figures, new questions, Reading tests (ideas 4, 6)
- [x] 4. Adaptive mock assembly and IRT score ranges (idea 5)
- [x] 5. Mini App rebuild: split files, compiled CSS, exam tools, Telegram theme and navigation (ideas 4, 15)
- [x] 6. Score report, practice, mistake notebook (ideas 7, 8)
- [x] 7. Diagnostic, study plan, reminders, weekly report (idea 9)
- [x] 8. AI Writing with Gemini (idea 10)
- [x] 9. Channel without repeats, share card, referrals (idea 12)
- [x] 10. Learning center panel: sessions, join codes, results, CSV (idea 14)
- [x] 11. Monitoring, health check, full verification, docs (idea 15)

## Decisions

- Postgres through `DATABASE_URL`, with SQLite as the local and fallback store. Render's disk is wiped on
  every deploy, so SQLite there is only a stopgap.
- Secrets live in environment variables only.
- Gemini Developer API (`generativelanguage.googleapis.com`). The provided key is rejected by Vertex AI.
- Keys of open tests stay in the client data, so they keep working on a bad connection. The server re-grades
  every submitted attempt, and its result is the one stored.
- Sealed exams are for centers: data/sealed_exams.json is never served, the phone gets the paper without keys,
  and the server picks the second module. This only hides keys if the GitHub repository is private.
- Practice never uses the next open mock, and a mock question a student has already seen does not count
  towards the score, unless most of the section is familiar, in which case the report warns instead.
