# Troubleshooting Guide

**Solutions to common issues with the Corporate Text Pipeline**

---

## Quick Diagnostics

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| `command not found` | Package not installed | `pip install -e .` |
| `(venv)` not showing | Venv not activated | `source venv/bin/activate` |
| `ModuleNotFoundError` | Package not installed | `pip install -e .` |
| 403 Forbidden | Invalid SEC email | Update `user_agent` in config.yaml |
| Files not in Dropbox | Wrong data_root | Check `data_root` in config.yaml |
| `Permission denied` | File permissions | `chmod -R u+w {folder}` |

---

## Installation Issues

### "python3: command not found"

**Cause:** Python not installed or not in PATH.

**Solution:**
```bash
# Check if python (without 3) works
python --version

# If not, install Python:
# Mac: brew install python@3.11
# Windows: Download from python.org
```

### "pip: command not found"

**Solution:**
```bash
# Use python -m pip instead
python3 -m pip install -e .
```

### "ModuleNotFoundError: No module named 'src'"

**Cause:** Package not installed in editable mode.

**Solution:**
```bash
# Make sure venv is activated, then:
pip install -e .
```

### Virtual environment won't activate

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

**Still not working?** Delete and recreate:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## Download Issues

### "403 Forbidden" from SEC

**Cause:** SEC requires a valid email in requests.

**Solution:**
1. Open `config.yaml`
2. Find `sec_edgar.user_agent`
3. Change to YOUR real email:
   ```yaml
   sec_edgar:
     user_agent: "your.name@university.edu"
   ```
4. Save and retry

### Downloads are very slow

**This is normal.** SEC limits requests to 10 per second.

Expected times:
- 100 filings: ~15 seconds
- 1,000 filings: ~2-3 minutes
- 8,600 filings: ~15-30 minutes

### Some downloads failed

1. **Check the failure log:**
   ```bash
   cat {Dropbox}/raw/10k/download_logs/failed_*.csv
   ```

2. **Common reasons:**
   - Filing doesn't exist for that CIK/year
   - CIK is invalid
   - Temporary network error

3. **Retry failed downloads:**
   ```bash
   # Script will skip existing files and retry failed ones
   download-10k
   ```

### Files downloading to wrong location

**Cause:** `data_root` not set correctly.

**Solution:**
1. Check `config.yaml`:
   ```yaml
   data_root: "/Users/YourName/Dropbox/corporate-text-pipeline-data"
   ```
2. Make sure the path exists
3. Use absolute path (starts with `/` on Mac or `C:\` on Windows)

---

## Processing Issues

### "No input files found"

**Cause:** Processing can't find downloaded files.

**Solution:**
1. Verify downloads exist:
   ```bash
   ls {Dropbox}/raw/10k/*.html | head
   ```
2. Check `data_root` in config.yaml matches where files are

### Processing produces empty files

**Possible causes:**
- 10-K has non-standard format
- Section markers not found

**Solution:**
1. Check the specific file manually in a browser
2. Report to Will with the CIK and year
3. May need custom handling for that firm

### "UnicodeDecodeError"

**Cause:** File has unusual character encoding.

**Solution:**
The pipeline handles most encoding issues automatically. If you see this error:
1. Note the specific file
2. Report to Will
3. Continue with other files

---

## Git/GitHub Issues

### "fatal: not a git repository"

**Cause:** Not in the project directory.

**Solution:**
```bash
cd ~/path/to/corporate-text-pipeline
```

### "Your branch is behind 'origin/main'"

**Cause:** Others pushed changes you don't have.

**Solution:**
```bash
git pull origin main
```

### Merge conflict

**Cause:** You and someone else edited the same lines.

**Solution:**
1. Open conflicting file in VS Code
2. Look for `<<<<<<<`, `=======`, `>>>>>>>` markers
3. Keep the correct version, delete markers
4. Save, then:
   ```bash
   git add .
   git commit -m "Resolved merge conflict"
   git push
   ```

**Avoid conflicts:** Communicate with team about who's editing what.

### "Permission denied (publickey)"

**Cause:** SSH keys not set up.

**Solution:** Contact Will to set up repository access.

### Accidentally committed sensitive data

**If not yet pushed:**
```bash
git reset --soft HEAD~1
# Remove the file
git add .
git commit -m "Corrected commit"
```

**If already pushed:** Contact Will immediately.

---

## Configuration Issues

### Config file not found

**Solution:**
```bash
# Make sure you're in the project root
ls config.yaml

# If missing, copy from template
cp config.yaml.example config.yaml
```

### Dropbox path not working

**Check:**
1. Path is absolute (starts with `/` or `C:\`)
2. Path uses correct slashes for your OS
3. Folder actually exists
4. No typos in folder name

**Mac example:**
```yaml
data_root: "/Users/yourname/Dropbox/corporate-text-pipeline-data"
```

**Windows example:**
```yaml
data_root: "C:/Users/yourname/Dropbox/corporate-text-pipeline-data"
```

---

## Performance Issues

### Script seems stuck

1. **Check if it's actually running:**
   - Is there a progress bar updating?
   - Are new files appearing in output folder?

2. **Check logs:**
   ```bash
   tail -f logs/download_*.log
   ```

3. **If truly stuck:** Ctrl+C to cancel, then restart from where it left off:
   ```bash
   download-10k --start-index {last_successful}
   ```

### Running out of disk space

```bash
# Check available space
df -h

# Check data folder size
du -sh {Dropbox}/raw/10k/
du -sh {Dropbox}/processed/
```

Full dataset needs ~5-20 GB. Free up space or use external drive.

---

## Getting More Help

### Before contacting Will:

1. **Check this guide** for your specific error
2. **Check the logs** in `logs/` folder
3. **Note the exact error message** (screenshot if possible)
4. **Note what command you ran** and what you expected

### Contact information:

- **Will Diebel:** william.diebel@moore.sc.edu
- **GitHub Issues:** For code bugs

### Information to include:

- What command you ran
- The full error message
- Your operating system (Mac/Windows)
- Contents of relevant log file

---

*Last Updated: January 2026*
